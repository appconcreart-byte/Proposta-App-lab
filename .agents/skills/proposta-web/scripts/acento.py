#!/usr/bin/env python3
"""Deriva os 3 tokens de acento de uma proposta a partir da cor da marca do cliente.

Uso:
    python3 acento.py "#91714B"          -> imprime os tokens
    python3 acento.py "#91714B" --css    -> imprime as 3 linhas prontas para o :root
    python3 acento.py "#91714B" --neutro -> ignora a marca e usa o acento neutro (marca verde ou sem cor)

Regra (DESIGN.md, "Cor Emprestada"):
- mantém a matiz da marca, limita a saturação (nada de neon) e clareia até
  o acento chegar a ~8.5:1 de contraste no canvas #08090a (mínimo aceito: 7:1);
- accent-2 (hover) é um passo mais claro;
- accent-ink é a mesma matiz quase preta, com pelo menos 7:1 sobre o acento
  (texto do botão principal).
Se a marca for cinza ou quase cinza, avisa e usa um acento neutro-frio.
"""
import colorsys
import sys

CANVAS = "#08090a"
TARGET = 8.5  # contraste-alvo do acento no canvas (o bronze da Suzano ficou em 8.7)
FALLBACK = "#9aa3c7"  # cinza-azulado neutro, para marca sem cor


def hex2rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb2hex(rgb):
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02x}" for c in rgb)


def lum(rgb):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def derive(brand):
    rgb = hex2rgb(brand)
    h, l, s = colorsys.rgb_to_hls(*rgb)
    aviso = None
    if s < 0.12:
        aviso = f"marca quase sem cor (saturação {s:.2f}); usando acento neutro {FALLBACK}"
        h, l, s = colorsys.rgb_to_hls(*hex2rgb(FALLBACK))
    if s >= 0.12 and 0.21 <= h <= 0.49:   # matiz entre ~75 e ~175 graus: verde
        aviso = ("marca verde: o acento vai se confundir com o verde de 'concluído' da página. "
                 "Use a cor secundária da marca (rode de novo com ela) ou --neutro, e decida com o Victor")
    if "--neutro" in sys.argv:
        aviso = f"acento neutro {FALLBACK} por escolha"
        h, l, s = colorsys.rgb_to_hls(*hex2rgb(FALLBACK))
    s = min(s, 0.55)          # teto de saturação: acento sóbrio, não neon
    canvas = hex2rgb(CANVAS)
    acc = None
    for step in range(0, 101):
        L = max(l, 0.35) + step * 0.005
        cand = colorsys.hls_to_rgb(h, min(L, 0.86), s)
        if contrast(cand, canvas) >= TARGET:
            acc = cand
            break
    if acc is None:
        acc = colorsys.hls_to_rgb(h, 0.86, s)
    ah, al, as_ = colorsys.rgb_to_hls(*acc)
    hover = colorsys.hls_to_rgb(ah, min(al + 0.08, 0.92), as_)
    ink = None
    for i in range(0, 12):
        L = 0.12 - i * 0.01
        cand = colorsys.hls_to_rgb(ah, L, min(as_ + 0.25, 0.7))
        if contrast(cand, acc) >= 7.5:
            ink = cand
            break
    ink = ink or (0.03, 0.03, 0.03)
    return {
        "accent": rgb2hex(acc),
        "accent-2": rgb2hex(hover),
        "accent-ink": rgb2hex(ink),
        "contraste_no_canvas": round(contrast(acc, canvas), 2),
        "contraste_texto_botao": round(contrast(ink, acc), 2),
        "aviso": aviso,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    d = derive(sys.argv[1])
    if "--css" in sys.argv:
        print(f"  --accent:{d['accent']};\n  --accent-2:{d['accent-2']};\n  --accent-ink:{d['accent-ink']};")
    else:
        for k, v in d.items():
            if v is not None:
                print(f"{k}: {v}")
