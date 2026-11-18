#!/usr/bin/env python3
"""Checagem mecânica de uma proposta antes de mostrar ao Victor.

Uso:  python3 validar.py <pasta-das-propostas>/<slug>/index.html

ERRO  = bloqueia (conserte antes de mostrar)
AVISO = revise com julgamento (pode ser intencional)
Sai com código 1 se houver ERRO.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"meta", "link", "img", "br", "use", "path", "rect", "circle", "ellipse", "input", "hr", "source"}

# limites de texto (caracteres, sem tags). Acima disso a seção começa a poluir.
LIMITES = {
    "hero-t": 95, "lede": 140, "statement": 75, "sub": 170, "conclusion": 90,
    "bignum-cap": 70, "cta h2": 55, "deliv h3": 36, "deliv p": 110, "node h3": 24,
    "node p": 60, "step d": 70, "gbar": 90, "need p": 120, "incl li": 60,
}


class Nest(HTMLParser):
    def __init__(self):
        super().__init__()
        self.st, self.err = [], []

    def handle_starttag(self, t, a):
        if t not in VOID:
            self.st.append((t, self.getpos()[0]))

    def handle_endtag(self, t):
        if t in VOID:
            return
        if self.st and self.st[-1][0] == t:
            self.st.pop()
        else:
            self.err.append(f"</{t}> inesperado na linha {self.getpos()[0]}")


def txt(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    p = Path(sys.argv[1])
    html = p.read_text()
    erros, avisos = [], []

    # 1. placeholders
    ph = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", html)))
    if ph:
        erros.append(f"placeholders não trocados: {', '.join(ph)}")

    # 2. travessão (regra do Victor)
    corpo = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    for i, linha in enumerate(html.splitlines(), 1):
        if "\u2014" in linha:
            erros.append(f"travessão (em-dash) na linha {i}: troque por vírgula, ponto ou dois-pontos")

    # 3. aninhamento HTML
    n = Nest()
    n.feed(html)
    erros += n.err[:5]
    if n.st:
        erros.append(f"tags sem fechar: {[t for t, _ in n.st[-5:]]}")

    # 4. acento só por variável
    m = re.search(r"--accent:\s*(#[0-9a-fA-F]{6})", html)
    if m:
        hexa = m.group(1).lower()
        fora = html.lower().count(hexa) - 1
        if fora > 0:
            erros.append(f"cor do acento {hexa} escrita à mão {fora}x fora do :root; use var(--accent)")
        r, g, b = (int(hexa[i:i + 2], 16) for i in (1, 3, 5))
        if re.search(rf"rgba\(\s*{r}\s*,\s*{g}\s*,\s*{b}\s*,", html):
            erros.append("rgba() com a cor do acento; use color-mix(in srgb,var(--accent) N%,transparent)")

    # 5. arquivos referenciados existem
    for ref in set(re.findall(r"url\((assets/[^)]+)\)|src=\"(assets/[^\"]+)\"", html)):
        f = ref[0] or ref[1]
        if not (p.parent / f).exists():
            erros.append(f"arquivo não existe: {f}")

    # 5b. logo por arquivo externo some quando a página abre por file:// (CSS mask + CORS)
    externos = sorted(set(re.findall(r"url\(assets/logos/[^)]+\)", html)))
    if externos:
        erros.append(f"logo por arquivo externo ({len(externos)}): some ao abrir por file://. Embuta como data URI (nova_proposta.py faz isso)")

    # 6. obrigatórios da estrutura
    for sel, nome in [('id="capa"', "capa"), ('class="proof"', "prova social"), ('id="quem-somos"', "quem somos"),
                      ('id="aprovar"', "fechamento"), ('noindex', "meta robots noindex"), ("wa.me", "link do WhatsApp")]:
        if sel not in html:
            erros.append(f"falta: {nome}")
    if not re.search(r"whatsapp:\s*'\d{12,13}'", html):
        erros.append("CFG.whatsapp sem número válido (só dígitos, com DDI e DDD). Preencha o config.json da skill")

    # 7. DEMO coerente
    dm = re.search(r"const DEMO = (\{.*?\n  \});", html, re.S)
    if dm:
        bloco = dm.group(1)
        chaves = re.findall(r"\{\s*k:\s*'([a-z0-9_]+)'", bloco)
        for i, val in enumerate(re.findall(r"valores:\s*\{([^}]*)\}", bloco), 1):
            ks = re.findall(r"([a-z0-9_]+)\s*:\s*'([^']*)'", val)
            got = {k for k, _ in ks}
            if set(chaves) != got:
                erros.append(f"DEMO item {i}: chaves {sorted(got)} diferentes dos campos {sorted(chaves)}")
            vazios = [k for k, v in ks if not v.strip()]
            if vazios:
                erros.append(f"DEMO item {i}: valores vazios em {vazios}")
        if len(chaves) % 2:
            avisos.append(f"DEMO com {len(chaves)} campos (ímpar): a grade de 2 colunas fica com um buraco")
        if len(chaves) > 8:
            avisos.append("DEMO com mais de 8 campos: painel pesado, corte para 4 a 6")

    # 8. excesso de texto por bloco
    def trecho(marca):
        i = corpo.find(marca)
        if i < 0:
            return ""
        fim = corpo.find("</section>", i)
        return corpo[i:fim if fim > 0 else None]

    def dentro(marca, tag, classe=None):
        t = trecho(marca)
        if classe:
            pat = rf'<{tag}[^>]*class="[^"]*\b{classe}\b[^"]*"[^>]*>(.*?)</{tag}>'
        else:
            pat = rf"<{tag}(?:\s[^>]*)?>(.*?)</{tag}>"
        return [txt(x) for x in re.findall(pat, t, re.S)]

    medidas = {
        "hero-t": dentro('id="resumo"', "h2", "hero-t"),
        "lede": dentro('id="resumo"', "p", "lede"),
        "statement": dentro('id="problema"', "p", "statement") + dentro('id="solucao"', "p", "statement"),
        "sub": dentro('id="solucao"', "p", "sub"),
        "conclusion": dentro('id="problema"', "p", "conclusion"),
        "bignum-cap": dentro('id="problema"', "p", "bignum-cap"),
        "cta h2": dentro('id="aprovar"', "h2"),
        "deliv h3": dentro('id="deliv"', "h3"),
        "deliv p": dentro('id="deliv"', "p"),
        "node h3": dentro('id="fluxo"', "h3"),
        "node p": dentro('id="fluxo"', "p"),
        "step d": dentro('class="flow-today"', "div", "d"),
        "gbar": dentro('id="phases"', "span"),
        "need p": dentro('class="needs"', "p"),
        "incl li": dentro('class="incl"', "li"),
    }
    for chave, textos in medidas.items():
        for t in textos:
            if len(t) > LIMITES[chave]:
                avisos.append(f"{chave}: {len(t)} caracteres (limite {LIMITES[chave]}): \"{t[:60]}...\"")

    # 9. orçamento de movimento
    loops = len(re.findall(r"animation:[^;]*infinite", html))
    if loops > 14:
        avisos.append(f"{loops} animações em loop no CSS (o template tem 13): confira se alguma nova é necessária")
    if html.count("data-r") > 70:
        avisos.append("muitos elementos com entrada no scroll; agrupe (1 data-r por bloco, não por frase)")

    # 10. vícios de layout
    if re.search(r'class="[^"]*\b(eyebrow|kicker|overline)\b', corpo):
        erros.append("rótulo acima do título (eyebrow/kicker) não entra: o título fala sozinho")
    if re.search(r">\s*0[1-9]\s*[/.<]", corpo):
        avisos.append("numeração 01/02/03 em seções: só use se a ordem for informação")
    if "lorem" in html.lower():
        erros.append("texto lorem ipsum na página")

    print(f"Validação: {p}")
    for e in erros:
        print("  ERRO ", e)
    for a in avisos:
        print("  AVISO", a)
    if not erros and not avisos:
        print("  OK, nada a apontar")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
