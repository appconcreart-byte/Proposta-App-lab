#!/usr/bin/env python3
"""Lista as cores de um logo (SVG ou PNG) da mais presente para a menos presente,
ignorando branco, preto e cinzas. É a fonte mais confiável da cor da marca: o
`branding` do firecrawl às vezes devolve cor de fundo ou de link no lugar da primária.

Uso:  python3 cores_logo.py logo.svg
Saída: hex, peso (quantas vezes aparece ou % de pixels), saturação. A primeira linha
costuma ser a cor da marca. Se o logo for monocromático (só branco ou preto), a cor
tem que vir do site (botão principal) ou de pergunta ao Victor.
"""
import colorsys
import re
import sys
from collections import Counter
from pathlib import Path


def norm(h):
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h


def sat(hexa):
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return s, l


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    p = Path(sys.argv[1])
    cont = Counter()
    if p.suffix.lower() == ".svg":
        txt = p.read_text(errors="ignore")
        for m in re.findall(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", txt):
            cont[norm(m)] += 1
        for r, g, b in re.findall(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", txt):
            cont["#%02x%02x%02x" % (int(r), int(g), int(b))] += 1
        unidade = "ocorrências"
    else:
        from PIL import Image
        im = Image.open(p).convert("RGBA").resize((200, 200))
        px = [c[:3] for c in im.getdata() if c[3] > 200]
        for r, g, b in px:
            cont["#%02x%02x%02x" % (r // 8 * 8, g // 8 * 8, b // 8 * 8)] += 1
        total = max(1, len(px))
        cont = Counter({k: round(v * 100 / total, 1) for k, v in cont.items()})
        unidade = "% dos pixels"
    linhas = []
    for hexa, n in cont.most_common():
        s, l = sat(hexa)
        if s < 0.15 or l < 0.08 or l > 0.95:
            continue
        linhas.append((hexa, n, s))
    if not linhas:
        print("Logo sem cor (só branco, preto ou cinza). Pegue a cor do botão principal do site ou pergunte ao Victor.")
        return
    print(f"cores do logo ({unidade}):")
    for hexa, n, s in linhas[:8]:
        print(f"  {hexa}  {n:>6}  saturação {s:.2f}")


if __name__ == "__main__":
    main()
