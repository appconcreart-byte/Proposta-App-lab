#!/usr/bin/env python3
"""Cria a pasta de uma proposta nova a partir do template e preenche o que é mecânico.

Uso:
    python3 nova_proposta.py --slug acme-sdr --cliente "Acme" --artigo a \
        --cor "#0050C3" --logo /caminho/logo-cliente.svg [--mes "outubro de 2026"] [--force]

O que faz:
  1. copia template/ para <PROPOSTAS>/<slug>/ (PROPOSTAS = "pasta_propostas" do config.json da skill,
     ou a variável de ambiente PROPOSTAS_DIR; padrão ~/propostas-web)
  2. copia o logo do cliente para assets/logos/ com nome <slug-do-cliente>.<ext>
  3. calcula a proporção do logo (viewBox do SVG ou tamanho do PNG) e alturas equilibradas
     para capa, nav e nav no celular
  4. deriva os 3 tokens de acento da cor da marca (acento.py)
  5. troca os placeholders globais: CLIENTE, ARTIGO_CLIENTE, MES_ANO, ACENTO*, LOGO_*, e os dados
     fixos do config.json (WHATSAPP, EMAIL, RAZAO_SOCIAL, CNPJ)
  6. embute todos os logos no HTML como data URI (url(assets/logos/x) vira base64). Sem isso, abrir o
     index.html por file:// esconde os logos (o Chrome bloqueia CSS mask de arquivo externo)
Todo o resto ({{...}} de conteúdo) fica para a etapa de conteúdo, feita à mão.
Termina listando os placeholders que ainda faltam.
"""
import argparse
import base64
import json
import math
import os
import re
import shutil
import struct
import sys
import unicodedata
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
CONFIG = json.loads((SKILL / "config.json").read_text()) if (SKILL / "config.json").exists() else {}
PROPOSTAS = Path(os.environ.get("PROPOSTAS_DIR") or CONFIG.get("pasta_propostas") or "~/propostas-web").expanduser()
FIXOS = {"WHATSAPP": "whatsapp", "EMAIL": "email", "RAZAO_SOCIAL": "razao_social", "CNPJ": "cnpj"}
sys.path.insert(0, str(HERE))
from acento import derive  # noqa: E402

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]
REF_AR = 169 / 53  # logo da Suzano, referência visual já aprovada


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def aspect(path: Path):
    data = path.read_bytes()
    if path.suffix.lower() == ".svg":
        txt = data.decode("utf8", "ignore")
        m = re.search(r'viewBox="\s*([\d.\-]+)[\s,]+([\d.\-]+)[\s,]+([\d.]+)[\s,]+([\d.]+)', txt)
        if m:
            return float(m.group(3)), float(m.group(4))
        w = re.search(r'\swidth="([\d.]+)', txt)
        h = re.search(r'\sheight="([\d.]+)', txt)
        if w and h:
            return float(w.group(1)), float(h.group(1))
        raise SystemExit("SVG sem viewBox nem width/height: não dá para calcular a proporção.")
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return float(w), float(h)
    raise SystemExit("Logo precisa ser SVG (preferido) ou PNG com fundo transparente.")


def embutir_logos(html, dest):
    """Troca url(assets/logos/x) por data URI. Os logos são desenhados por CSS mask, e o Chrome
    bloqueia mask de arquivo externo quando a página é aberta por file:// (o Victor abre o
    index.html direto): os logos somem sem erro. Com data URI funciona em file://, localhost e Vercel."""
    tipos = {".svg": "image/svg+xml", ".png": "image/png"}

    def troca(m):
        f = dest / "assets" / "logos" / m.group(1)
        if not f.exists() or f.suffix.lower() not in tipos:
            return m.group(0)
        b64 = base64.b64encode(f.read_bytes()).decode()
        return f"url('data:{tipos[f.suffix.lower()]};base64,{b64}')"

    return re.subn(r"url\(assets/logos/([A-Za-z0-9._-]+)\)", troca, html)


def heights(ar):
    # mantém a "massa visual" parecida com a da Suzano: logos largos ficam mais baixos
    f = math.sqrt(REF_AR / ar)
    f = max(0.55, min(f, 1.45))
    lo, vw, hi = 38 * f, 4.4 * f, 60 * f
    capa = f"clamp({lo:.0f}px,{vw:.1f}vw,{hi:.0f}px)"
    nav = f"{max(16, min(34, 26 * f)):.0f}px"
    nav_m = f"{max(14, min(28, 22 * f)):.0f}px"
    return capa, nav, nav_m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="pasta da proposta, ex.: suzano ou acme-sdr")
    ap.add_argument("--cliente", required=True, help='nome como aparece na página, ex.: "Suzano"')
    ap.add_argument("--artigo", default="a", choices=["a", "o"], help='"a Suzano", "o Grupo X"')
    ap.add_argument("--cor", required=True, help="cor principal da marca do cliente, hex")
    ap.add_argument("--logo", required=True, help="arquivo do logo do cliente (SVG ou PNG transparente)")
    ap.add_argument("--mes", help='ex.: "outubro de 2026" (padrão: mês atual)')
    ap.add_argument("--force", action="store_true", help="sobrescreve a proposta se já existir")
    ap.add_argument("--neutro", action="store_true", help="acento neutro em vez da cor da marca (marca verde ou sem cor)")
    a = ap.parse_args()

    dest = PROPOSTAS / a.slug
    if (dest / "index.html").exists() and not a.force:
        raise SystemExit(f"{dest} já tem uma proposta. Use outro --slug ou --force (apaga a versão atual).")
    if (dest / "index.html").exists():
        shutil.rmtree(dest)
    # pasta sem index.html (ex.: só com anotações) é aproveitada: os arquivos dela ficam
    shutil.copytree(SKILL / "template", dest, dirs_exist_ok=True)

    logo = Path(a.logo).expanduser()
    if not logo.exists():
        raise SystemExit(f"logo não encontrado: {logo}")
    nome_logo = f"{slugify(a.cliente)}{logo.suffix.lower()}"
    shutil.copy(logo, dest / "assets" / "logos" / nome_logo)
    w, h = aspect(logo)
    ar = w / h
    capa, nav, nav_m = heights(ar)

    if a.neutro:
        sys.argv.append("--neutro")
    tokens = derive(a.cor)
    hoje = date.today()
    mes = a.mes or f"{MESES[hoje.month - 1]} de {hoje.year}"
    mes = mes[0].upper() + mes[1:]

    subs = {
        "CLIENTE": a.cliente,
        "ARTIGO_CLIENTE": a.artigo,
        "MES_ANO": mes,
        "ACENTO": tokens["accent"],
        "ACENTO_HOVER": tokens["accent-2"],
        "ACENTO_TINTA": tokens["accent-ink"],
        "LOGO_CLIENTE_ARQUIVO": nome_logo,
        "LOGO_CLIENTE_AR": f"{w:g}/{h:g}",
        "LOGO_CLIENTE_ALTURA_CAPA": capa,
        "LOGO_CLIENTE_ALTURA_NAV": nav,
        "LOGO_CLIENTE_ALTURA_NAV_MOBILE": nav_m,
    }
    pendentes = []
    for ph, chave in FIXOS.items():
        v = str(CONFIG.get(chave, ""))
        if not v or v.startswith("PREENCHA"):
            pendentes.append(chave)
        else:
            subs[ph] = re.sub(r"\D", "", v) if chave == "whatsapp" else v
    idx = dest / "index.html"
    html = idx.read_text()
    for k, v in subs.items():
        html = html.replace("{{" + k + "}}", v)
    html, n_logos = embutir_logos(html, dest)
    idx.write_text(html)

    faltam = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", html)))
    print(f"Criado: {idx}")
    print(f"Logo: assets/logos/{nome_logo} (proporção {ar:.2f}; capa {capa}, nav {nav}); {n_logos} logos embutidos no HTML (data URI)")
    print(f"Acento: {tokens['accent']} ({tokens['contraste_no_canvas']}:1 no fundo), texto do botão {tokens['accent-ink']}")
    if tokens.get("aviso"):
        print("AVISO:", tokens["aviso"])
    if pendentes:
        print(f"AVISO: config.json da skill sem {', '.join(pendentes)}. Preencha e rode de novo com --force.")
    print(f"Placeholders de conteúdo que faltam ({len(faltam)}): {', '.join(faltam)}")


if __name__ == "__main__":
    main()
