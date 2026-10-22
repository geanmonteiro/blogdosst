# Blog da Saúde e Segurança do Trabalho — blogdosst.com.br

## O que é isto
Site estático pronto (HTML puro, sem build): 5 artigos completos, SEO (sitemap, robots, dados estruturados), páginas Sobre/Contato/Privacidade (exigência do AdSense), e blocos de anúncio que ATIVAM SOZINHOS quando você preencher o ID do AdSense.

## Deploy na Vercel (5 minutos, grátis)
1. Acesse vercel.com → sign up/login com sua conta Google
2. "Add New..." → "Project" → arraste a pasta `site-out` (ou use "Deploy without Git" / CLI)
   - Alternativa com GitHub: crie um repositório `blogdosst`, suba estes arquivos, e importe na Vercel (aí eu consigo publicar artigos novos direto no repo — me convide como collaborator ou gere outro fine-grained token para esse repo)
3. Depois do deploy: Project → Settings → Domains → adicione `blogdosst.com.br` e `www.blogdosst.com.br`
4. No registro.br (onde você registrou o domínio): DNS → aponte para a Vercel (a própria Vercel mostra os records: A 76.76.21.21 e CNAME www → cname.vercel-dns.com)

## Google: Search Console + AdSense
1. Search Console (search.google.com/search-console): adicione o domínio, verifique por DNS (TXT), envie o sitemap: https://www.blogdosst.com.br/sitemap.xml
2. AdSense (adsense.google.com): adicione o site, aguarde os ~30 artigos (as automações geram), e quando aprovado:
   - Pegue o ID do cliente (ca-pub-...) e os IDs dos blocos
   - Crie o arquivo `config.json` ao lado do gerador: {"ga4_id":"G-...","adsense_client":"ca-pub-...","adsense_slots":{"home":"...","topo":"...","fim":"..."}}
   - Rode `python3 gerar_blog.py` e republique — anúncios e GA4 ativam sozinhos

## Artigos novos
Os artigos ficam em `content/artigos/*.md` (Markdown com cabeçalho titulo/resumo/categoria/tags/data). Depois de adicionar: `python3 gerar_blog.py` regenera o site inteiro. A automação do assistente faz isso sozinha.
