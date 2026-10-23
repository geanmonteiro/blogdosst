#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica o próximo artigo do blog blogdosst.com.br.

Fluxo completo (executado pelo agente no turno do cron):
1. Escolhe tema: 1º não publicado cujo 'mes' contém o mês atual; senão 1º não publicado.
2. Pesquisa web (3+ buscas) para dados oficiais atualizados do tema.
3. Escreve artigo 700-1200 palavras em content/artigos/<slug>.md (front matter:
   titulo, resumo, categoria, tags, data=hoje).
4. python3 work/blogdosst/gerar_blog.py
5. Deploy Vercel: POST /v2/files?sha=<sha1> (x-vercel-digest) por arquivo +
   POST /v13/deployments {name:"blogdosst", project:"blogdosst", target:"production",
   files:[...], meta:{githubCommitMessage}}. NUNCA subconjunto (derruba produção).
6. Verifica HTTP 200 em https://www.blogdosst.com.br/artigo/<slug>/
7. Registra tema em work/blogdosst/fila/publicados.json + memory/MEMORY.md + append_today.
8. Se restarem <5 temas não publicados: gerar 10 novos (Google Trends BR, sazonalidade,
   perguntas do SERP) e anexar em fila/temas.json.

Credenciais: work/vercel_token.txt (chmod 600). Nunca ecoar.
"""
import json, os, sys
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "blogdosst")
BASE = os.path.abspath(BASE)
fila = os.path.join(BASE, "fila")
temas = json.load(open(os.path.join(fila, "temas.json"), encoding="utf-8"))["temas"]
pub_path = os.path.join(fila, "publicados.json")
publicados = json.load(open(pub_path, encoding="utf-8")) if os.path.exists(pub_path) else []

mes_atual = int(sys.argv[1]) if len(sys.argv) > 1 else 1
pend = [t for t in temas if t["slug"] not in publicados]
sazonal = [t for t in pend if not t.get("mes") or mes_atual in t["mes"]]
escolhido = (sazonal or pend)[0] if pend else None
restantes = len(pend) - 1 if escolhido else len(pend)
print(json.dumps({"escolhido": escolhido, "restantes": restantes}, ensure_ascii=False))