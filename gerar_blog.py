#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o Blog da Saúde e Segurança do Trabalho (blogdosst.com.br) como site estático.
Fonte: content/artigos/*.md (front matter YAML simples). Saída: site-out/
Uso: python3 gerar_blog.py  (roda a partir de work/blogdosst/)"""
import os, json, html, re, shutil
import markdown

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "content", "artigos")
OUT = os.path.join(BASE, "site-out")
DOMINIO = "https://www.blogdosst.com.br"
NOME = "Blog da Saúde e Segurança do Trabalho"
NOME_CURTO = "Saúde e ST"

# Config de analytics/adsense (preencha quando aprovado)
CONF = {}
conf_path = os.path.join(BASE, "config.json")
if os.path.exists(conf_path):
    CONF = json.load(open(conf_path, encoding="utf-8"))
GA = CONF.get("ga4_id", "")          # ex.: G-XXXXXXX
ADSENSE = CONF.get("adsense_client", "")  # ex.: ca-pub-XXXX
SLOTS = CONF.get("adsense_slots", {})     # {"topo": "123", "fim": "456", "home": "789"}

def fm_parse(texto):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    if not m:
        return {}, texto
    meta = {}
    for linha in m.group(1).splitlines():
        if ":" in linha:
            k, v = linha.split(":", 1)
            k, v = k.strip(), v.strip().strip('"')
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip().strip('"') for x in v[1:-1].split(",")]
            meta[k] = v
    return meta, m.group(2)

def ad(slot, classe="ad-slot"):
    if not (ADSENSE and slot):
        return ""
    return f'''<div class="{classe}"><div class="ad-rotulo">Publicidade</div>
<ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE}" data-ad-slot="{slot}" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>'''

def head(titulo, desc):
    ga = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}};gtag('js',new Date());gtag('config','{GA}',{{anonymize_ip:true}});</script>""" if GA else ""
    ads = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>' if ADSENSE else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{DOMINIO}">
<link rel="stylesheet" href="/style.css">
{ga}{ads}
</head>"""

CHROME_TOP = f"""<header class="site"><div class="container-largo">
<a href="/" class="logo">Blog da <span>Saúde e ST</span></a>
<nav><a href="/categoria/verbas-rescisorias/">Verbas</a><a href="/categoria/fgts/">FGTS</a><a href="/categoria/seguro-desemprego/">Seguro-desemprego</a><a href="/categoria/sst/">SST</a><a href="/sobre/">Sobre</a></nav>
</div></header>"""

CHROME_BOT = f"""<footer class="site"><div class="container-largo">
<p>{NOME} — conteúdo informativo sobre direitos trabalhistas e previdenciários.</p>
<p>Não substitui a consulta a um advogado ou profissional habilitado. <a href="/politica-de-privacidade/">Política de Privacidade</a> · <a href="/contato/">Contato</a></p>
<p>© 2026 {NOME}</p>
</div></footer>"""

def card(a):
    return f'''<a href="/artigo/{a["slug"]}/" class="card"><span class="cat">{html.escape(a["categoria"])}</span><h3>{html.escape(a["titulo"])}</h3><p>{html.escape(a["resumo"])}</p><time>{a["data_fmt"]}</time></a>'''

def fmt_data(iso):
    ano, mes, dia = iso.split("-")
    meses = ["", "janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
    return f"{int(dia)} de {meses[int(mes)]} de {ano}"

# ---- carrega artigos ----
artigos = []
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".md"): continue
    meta, corpo = fm_parse(open(os.path.join(SRC, f), encoding="utf-8").read())
    artigos.append({
        "slug": f[:-3], "titulo": meta.get("titulo",""), "resumo": meta.get("resumo",""),
        "categoria": meta.get("categoria",""), "tags": meta.get("tags",[]),
        "data": meta.get("data",""), "data_fmt": fmt_data(meta.get("data","2026-01-01")),
        "corpo_md": corpo,
    })
artigos.sort(key=lambda a: a["data"], reverse=True)

def md2html(md):
    return markdown.markdown(md, extensions=["tables", "fenced_code"])

# ---- limpa saída ----
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)

# ---- CSS ----
open(os.path.join(OUT, "style.css"), "w").write(open(os.path.join(BASE, "style.css"), encoding="utf-8").read()) if os.path.exists(os.path.join(BASE, "style.css")) else None

# ---- home ----
destaque, resto = (artigos[0], artigos[1:]) if artigos else (None, [])
cards = "".join(card(a) for a in resto)
home = f"""{head(NOME + " — Direitos trabalhistas, verbas e SST explicados", "Verbas rescisórias, FGTS, seguro-desemprego, adicional de insalubridade e aposentadoria especial: guias claros e atualizados.")}
<body>
{CHROME_TOP}
<section class="hero"><div class="container-largo"><h1>Seus direitos trabalhistas explicados sem juridiquês</h1>
<p>Verbas rescisórias, FGTS, seguro-desemprego, adicional de insalubridade e aposentadoria especial: guias práticos, com valores e prazos atualizados.</p></div></section>
<main class="container-largo">
{f'<h2 class="secao">Destaque</h2>{card(destaque)}' if destaque else ""}
{ad(SLOTS.get("home",""))}
<h2 class="secao">Todos os artigos</h2>
<div class="grid">{cards}</div>
</main>
{CHROME_BOT}
</body></html>"""
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(home)

# ---- artigos ----
for a in artigos:
    d = os.path.join(OUT, "artigo", a["slug"])
    os.makedirs(d)
    relacionados = [x for x in artigos if x["slug"] != a["slug"]][:3]
    rel_html = "".join(f'<a href="/artigo/{r["slug"]}/" class="card"><span class="cat">{html.escape(r["categoria"])}</span><h3>{html.escape(r["titulo"])}</h3></a>' for r in relacionados)
    corpo = md2html(a["corpo_md"])
    minutos = max(1, round(len(a["corpo_md"].split()) / 220))
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": a["titulo"], "description": a["resumo"], "datePublished": a["data"], "author": {"@type": "Person", "name": "Gean Monteiro"}, "publisher": {"@type": "Organization", "name": NOME}}, ensure_ascii=False)
    pagina = f"""{head(a["titulo"] + " | " + NOME_CURTO, a["resumo"])}
<body>
{CHROME_TOP}
<main class="container"><article class="artigo">
<span class="cat" style="color:var(--verde);font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em">{html.escape(a["categoria"])}</span>
<h1>{html.escape(a["titulo"])}</h1>
<div class="meta">Atualizado em {a["data_fmt"]} · {minutos} min de leitura</div>
{ad(SLOTS.get("topo",""))}
{corpo}
<div class="aviso">⚠️ Conteúdo informativo, atualizado com as regras vigentes. Seu caso concreto pode ter particularidades — consulte um advogado trabalhista ou o próprio INSS antes de decidir.</div>
{ad(SLOTS.get("fim",""))}
</article>
{f'<h2 class="secao">Leia também</h2><div class="grid">{rel_html}</div>' if relacionados else ""}
</main>
{CHROME_BOT}
<script type="application/ld+json">{jsonld}</script>
</body></html>"""
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(pagina)

# ---- categorias ----
for cat in sorted({a["categoria"] for a in artigos}):
    slug_cat = cat.lower().replace(" ", "-")
    d = os.path.join(OUT, "categoria", slug_cat)
    os.makedirs(d)
    lista = "".join(card(a) for a in artigos if a["categoria"] == cat)
    p = f"""{head(cat + " | " + NOME_CURTO, "Artigos sobre " + cat)}
<body>{CHROME_TOP}<main class="container-largo"><h2 class="secao">Categoria: {html.escape(cat)}</h2><div class="grid">{lista}</div></main>{CHROME_BOT}</body></html>"""
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(p)

# ---- páginas fixas ----
def pagina_fixa(pasta, titulo, desc, conteudo_html):
    d = os.path.join(OUT, pasta); os.makedirs(d, exist_ok=True)
    p = f"""{head(titulo + " | " + NOME_CURTO, desc)}<body>{CHROME_TOP}<main class="container"><article class="artigo"><h1>{titulo}</h1>{conteudo_html}</article></main>{CHROME_BOT}</body></html>"""
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(p)

pagina_fixa("sobre", "Sobre o blog", "Quem escreve o Blog da Saúde e Segurança do Trabalho",
"""<p>O <strong>Blog da Saúde e Segurança do Trabalho</strong> nasceu para explicar, em linguagem simples, os direitos trabalhistas e previdenciários que mais geram dúvida no Brasil: verbas rescisórias, FGTS, seguro-desemprego, adicional de insalubridade e periculosidade, estabilidade e aposentadoria especial.</p>
<p>Os conteúdos são escritos por um Técnico em Segurança do Trabalho que atua com auditorias de SST, documentos trabalhistas e assistência técnica em perícia — quem lida com esses números e prazos no dia a dia.</p>
<p>Nosso compromisso: dados corretos, valores atualizados e fontes oficiais em cada artigo. Sem promessa milagrosa, sem juridiquês.</p>""")

pagina_fixa("contato", "Contato", "Fale com o Blog da Saúde e Segurança do Trabalho",
"""<p>Tem uma dúvida sobre um artigo ou uma sugestão de tema? Fale com a gente:</p>
<p>✉️ <strong>contato@blogdosst.com.br</strong></p>
<p>Respondemos em até 2 dias úteis. Importante: não fazemos análise de casos individuais — para o seu caso concreto, procure um advogado trabalhista ou ligue 135 (INSS).</p>""")

pagina_fixa("politica-de-privacidade", "Política de Privacidade", "Política de Privacidade e cookies",
"""<p><strong>1. Dados que coletamos.</strong> O blog não requer cadastro e não coleta dados pessoais diretamente. Usamos o Google Analytics (com IP anonimizado) para estatísticas agregadas e o Google AdSense para exibir anúncios.</p>
<p><strong>2. Cookies e publicidade.</strong> O Google e seus parceiros podem usar cookies para personalizar anúncios com base em suas visitas a este e outros sites. Você pode desativar anúncios personalizados em adssettings.google.com.</p>
<p><strong>3. Dados de terceiros.</strong> Consulte as políticas do Google: policies.google.com/privacy e support.google.com/adsense/answer/1348695.</p>
<p><strong>4. Seus direitos (LGPD).</strong> Como não mantemos base de dados pessoais própria, pedidos relacionados a cookies/anúncios devem ser feitos ao Google. Dúvidas: contato@blogdosst.com.br.</p>
<p><strong>5. Atualizações.</strong> Esta política pode ser atualizada a qualquer momento.</p>""")

# ---- sitemap + robots ----
urls = [f"{DOMINIO}/"] + [f"{DOMINIO}/artigo/{a['slug']}/" for a in artigos] + [f"{DOMINIO}/categoria/{c.lower().replace(' ','-')}/" for c in {a['categoria'] for a in artigos}] + [f"{DOMINIO}/sobre/", f"{DOMINIO}/contato/", f"{DOMINIO}/politica-de-privacidade/"]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>"
open(os.path.join(OUT, "sitemap.xml"), "w").write(sitemap)
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")

# ---- vercel config (site estático) ----
json.dump({"cleanUrls": True}, open(os.path.join(OUT, "vercel.json"), "w"))

print(f"OK: {len(artigos)} artigos gerados em {OUT}")