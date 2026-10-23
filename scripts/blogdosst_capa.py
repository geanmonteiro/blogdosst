#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa de artigo do blog blogdosst.com.br — 1200x675 (OG image).
Renderizada com Pillow, no estilo visual do site (azul/verde/dourado).
Uso: python3 scripts/blogdosst_capa.py "<titulo>" "<subtitulo>" <saida.png> [kicker]
O layout se adapta: título grande em até 4 linhas, subtítulo em até 3, kicker (categoria)."""
from PIL import Image, ImageDraw, ImageFont
import glob, sys, textwrap

W, H = 1200, 675
AZUL      = (15, 42, 74)     # --azul
AZUL_CLARO= (29, 78, 137)    # --azul-claro
VERDE     = (14, 159, 110)   # --verde
DOURADO   = (246, 173, 30)   # --dourado
TXT_LT    = (255, 255, 255)
TXT_MUT   = (203, 213, 225)

def font(size, bold=True):
    g = glob.glob("/usr/share/fonts/noto/NotoSans-%s.ttf" % ("Bold" if bold else "Regular"))
    return ImageFont.truetype(g[0], size) if g else ImageFont.load_default()

def F(size, bold=True):
    return font(size, bold)

def wrap(draw, texto, f, largura):
    palavras = texto.split()
    linhas, atual = [], ""
    for p in palavras:
        teste = (atual + " " + p).strip()
        if draw.textlength(teste, font=f) <= largura:
            atual = teste
        else:
            if atual: linhas.append(atual)
            atual = p
    if atual: linhas.append(atual)
    return linhas

def gerar(titulo, subtitulo, saida, kicker=""):
    img = Image.new("RGB", (W, H), AZUL)
    d = ImageDraw.Draw(img)

    # fundo: gradiente diagonal simulado com faixas + formas geométricas
    for i in range(0, 40):
        t = i / 40
        cor = tuple(int(AZUL[k] + (AZUL_CLARO[k] - AZUL[k]) * t) for k in range(3))
        d.polygon([(W - i * 30, 0), (W - i * 30 + 30, 0), (W, i * 16.875 + 30), (W, i * 16.875)], fill=cor)
    # círculos decorativos
    d.ellipse([W - 260, -120, W + 120, 260], outline=(255, 255, 255, 30), width=2)
    d.ellipse([W - 200, -60, W + 60, 200], outline=(255, 255, 255, 20), width=2)
    d.ellipse([-140, H - 180, 180, H + 140], fill=(14, 159, 110))

    # kicker (categoria)
    y = 64
    if kicker:
        kf = F(26, True)
        kw = d.textlength(kicker.upper(), font=kf)
        d.rounded_rectangle([80, y - 10, 80 + kw + 44, y + 40], radius=20, fill=VERDE)
        d.text((80 + 22, y + 2), kicker.upper(), font=kf, fill=TXT_LT)
        y += 78

    # título (até 4 linhas)
    tf = F(56, True)
    linhas_t = wrap(d, titulo, tf, W - 160 - 120)
    if len(linhas_t) > 4:
        tf = F(48, True)
        linhas_t = wrap(d, titulo, tf, W - 160 - 100)
    for ln in linhas_t[:4]:
        d.text((80, y), ln, font=tf, fill=TXT_LT)
        y += int(tf.size * 1.22)
    y += 26

    # linha dourada
    d.rectangle([80, y, 320, y + 6], fill=DOURADO)
    y += 34

    # subtítulo (até 3 linhas)
    if subtitulo:
        sf = F(30, False)
        linhas_s = wrap(d, subtitulo, sf, W - 160 - 200)
        for ln in linhas_s[:3]:
            d.text((80, y), ln, font=sf, fill=TXT_MUT)
            y += int(sf.size * 1.35)

    # rodapé: marca
    d.text((80, H - 72), "Blog da Saúde e ST", font=F(24, True), fill=TXT_LT)
    d.text((80 + d.textlength("Blog da Saúde e ST", font=F(24, True)) + 18, H - 72),
           "· blogdosst.com.br", font=F(24, False), fill=TXT_MUT)

    img.save(saida, "PNG", optimize=True)
    print(f"OK: {saida} ({W}x{H})")

if __name__ == "__main__":
    titulo = sys.argv[1]
    subtitulo = sys.argv[2] if len(sys.argv) > 2 else ""
    saida = sys.argv[3]
    kicker = sys.argv[4] if len(sys.argv) > 4 else ""
    gerar(titulo, subtitulo, saida, kicker)