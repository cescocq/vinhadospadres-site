import re,os,glob,html
S='/home/claude/vdp/s65/'
SITE='https://www.vinhadospadres.com'
base=open(S+'wines.html').read()
basept=open(S+'wines-pt.html').read()
def page(src,title,desc,body,name,pt):
    h=src
    h=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',h,count=1,flags=re.S)
    h=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{html.escape(desc)}">',h)
    h=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{html.escape(title)}">',h)
    h=re.sub(r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{html.escape(desc)}">',h)
    h=re.sub(r'<script type="application/ld\+json">.*?</script>','',h,flags=re.S)
    a=h.find('<main'); b=h.rfind('</main>')+7
    h=h[:a]+'<main class="cpage lpage">'+body+'</main>'+h[b:]
    # remove page-specific scripts that target wines content
    h=re.sub(r'<script>const B=\[\.\.\.document\.querySelectorAll\(\'\.chips button\'\)\].*?</script>','',h,flags=re.S)
    h=h.replace('aria-current="page"','')
    h=h.replace('</head>','<style>.lpage{max-width:820px}.lpage h1{margin-bottom:4px}.lpage h2{font-family:var(--serif);font-size:24px;margin:30px 0 8px}.lpage p,.lpage li{font-size:17.5px;line-height:1.55}.lpage .upd{color:var(--dim);font-size:15px}</style></head>',1)
    if name=='404': h=re.sub(r'<link rel="(canonical|alternate)"[^>]*>','',h).replace('</title>','</title><meta name="robots" content="noindex">',1)
    open(S+name+('-pt' if pt and name!='404' else '')+'.html','w').write(h)
PRIV_EN='''<h1>privacy policy</h1><p class="upd">Last updated: November 2026</p>
<p>This website is run by <b>Vinha dos Padres, Lda.</b>, Reguengo, Portalegre, Portugal. Contact for any privacy question: <b>vdp@silimosa.com</b>.</p>
<h2>what we collect</h2><ul><li><b>Contact form:</b> your name, email, phone (optional) and message, used only to reply to you.</li><li><b>Mailing list:</b> your email address, used only to send news about our wines and new releases, a few times a year.</li></ul>
<p>Both forms are delivered to our inbox by the form service FormSubmit. We do not sell or share your data, and we do not use it for any other purpose.</p>
<h2>legal basis and retention</h2><p>We process this data with your consent (art. 6(1)(a) GDPR). Contact messages are kept while the conversation is useful and for no longer than 2 years; mailing-list addresses are kept until you unsubscribe.</p>
<h2>cookies and local storage</h2><p>We do not use advertising or tracking cookies. The site stores a few preferences in your own browser (your language, that you confirmed your age, that you closed the welcome note). They never leave your device and you can clear them at any time in your browser settings.</p>
<h2>third-party services</h2><ul><li>Code libraries (d3, three.js) are loaded from public CDNs (cdnjs, jsDelivr), which see your IP address as part of the request.</li><li>Links to Google Maps, Instagram and Facebook take you to those services, under their own privacy policies.</li></ul>
<h2>your rights</h2><p>You can ask to access, correct or delete your data, or withdraw your consent, at any time by writing to vdp@silimosa.com. Each mailing-list email also has an unsubscribe link. You may also complain to the Portuguese data protection authority, CNPD (www.cnpd.pt).</p>
<h2>responsible drinking</h2><p>Our wines are for adults of legal drinking age (18+). Please drink responsibly.</p>'''
PRIV_PT='''<h1>política de privacidade</h1><p class="upd">Última atualização: novembro de 2026</p>
<p>Este site é gerido pela <b>Vinha dos Padres, Lda.</b>, Reguengo, Portalegre, Portugal. Contacto para qualquer questão de privacidade: <b>vdp@silimosa.com</b>.</p>
<h2>que dados recolhemos</h2><ul><li><b>Formulário de contacto:</b> nome, email, telefone (opcional) e mensagem, usados apenas para lhe responder.</li><li><b>Lista de envio:</b> o seu email, usado apenas para enviar notícias sobre os nossos vinhos e novos lançamentos, algumas vezes por ano.</li></ul>
<p>Os dois formulários chegam à nossa caixa de correio através do serviço FormSubmit. Não vendemos nem partilhamos os seus dados, nem os usamos para outro fim.</p>
<h2>fundamento e conservação</h2><p>Tratamos estes dados com o seu consentimento (art. 6.º, n.º 1, alínea a) do RGPD). As mensagens de contacto são guardadas enquanto forem úteis e nunca mais de 2 anos; os emails da lista de envio são guardados até cancelar a inscrição.</p>
<h2>cookies e armazenamento local</h2><p>Não usamos cookies de publicidade nem de rastreamento. O site guarda algumas preferências no seu próprio navegador (o idioma, a confirmação da idade e o fecho da nota de boas-vindas). Não saem do seu dispositivo e pode apagá-las a qualquer momento nas definições do navegador.</p>
<h2>serviços de terceiros</h2><ul><li>Bibliotecas de código (d3, three.js) são carregadas de CDN públicas (cdnjs, jsDelivr), que veem o seu endereço IP como parte do pedido.</li><li>As ligações para o Google Maps, Instagram e Facebook levam-no a esses serviços, sujeitos às suas próprias políticas de privacidade.</li></ul>
<h2>os seus direitos</h2><p>Pode pedir acesso, retificação ou eliminação dos seus dados, ou retirar o consentimento, a qualquer momento, escrevendo para vdp@silimosa.com. Cada email da lista tem também uma ligação para cancelar a inscrição. Pode ainda apresentar reclamação à Comissão Nacional de Proteção de Dados, CNPD (www.cnpd.pt).</p>
<h2>consumo responsável</h2><p>Os nossos vinhos destinam-se a adultos com idade legal para consumir álcool (18+). Beba com moderação.</p>'''
page(base,'Privacy policy · Vinha dos Padres','How Vinha dos Padres handles personal data from its contact form and mailing list.',PRIV_EN,'privacy',False)
page(basept,'Política de privacidade · Vinha dos Padres','Como a Vinha dos Padres trata os dados pessoais do formulário de contacto e da lista de envio.',PRIV_PT,'privacy',True)
B404='''<div style="text-align:center;padding:40px 0"><h1 style="font-size:64px;margin:0">404</h1><p style="font-size:20px">This page doesn’t exist, or has moved.<br><i>Esta página não existe, ou mudou de lugar.</i></p>
<p style="margin-top:26px"><a class="btn404" href="index.html">explore the estate →</a> &nbsp; <a class="btn404" href="wines.html">our wines →</a> &nbsp; <a class="btn404" href="index-pt.html">versão portuguesa →</a></p></div>
<style>.btn404{display:inline-block;border:1.5px solid #231F20;border-radius:999px;padding:8px 18px;color:#231F20;text-decoration:none;font-size:17px;margin:4px}.btn404:hover{border-color:#C76653;color:#C76653}</style>'''
page(base,'Page not found · Vinha dos Padres','Page not found.',B404,'404',False)

# ---------- favicon (derived from the Loader tile motif, logo untouched) ----------
FAV='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#E6DED0"/><g fill="#C56552" transform="translate(8.6 10.2) scale(0.88)">
<rect x="0" y="14.05" width="9.9" height="13.72" rx=".9"/><rect x="10.86" y="6.86" width="9.9" height="27.43" rx=".9"/><rect x="21.73" y="0" width="9.9" height="13.72" rx=".9"/>
<rect x="21.73" y="27.43" width="9.9" height="13.72" rx=".9"/><rect x="32.59" y="6.86" width="9.9" height="27.43" rx=".9"/><rect x="43.46" y="14.05" width="9.9" height="13.72" rx=".9"/></g></svg>'''
open(S+'favicon.svg','w').write(FAV)
# ---------- age gate + footer on every page ----------
AG_CSS='''<style id="agcss">#ageGate{position:fixed;inset:0;z-index:1000;display:grid;place-items:center;background:rgba(230,222,208,.97);font-family:var(--serif);color:#231F20;padding:20px}
#ageGate[hidden]{display:none}#ageGate .b{max-width:440px;text-align:center}#ageGate h2{font-family:var(--serif);font-weight:600;font-style:italic;font-size:30px;margin:14px 0 8px}
#ageGate p{font-size:17px;margin:0 0 18px;color:#4a433f}#ageGate .a{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
#ageGate button{font:inherit;font-size:17px;font-weight:600;padding:9px 24px;border-radius:999px;border:1.5px solid #231F20;background:none;color:#231F20;cursor:pointer}#ageGate button.y{background:#231F20;color:#E6DED0}
#ageGate small{display:block;margin-top:18px;font-size:13px;color:#6b625b}#ageGate small a{color:inherit}#ageGate .no{display:none;margin-top:14px;font-size:16px}#ageGate.denied .no{display:block}#ageGate.denied .a{display:none}
#ageGate h2.lg{margin:0 0 26px}#ageGate .lg svg{width:min(420px,82vw);height:auto;display:block;margin:0 auto}
.sfoot{max-width:1180px;margin:0 auto;padding:26px 48px 34px;border-top:1px solid rgba(35,31,32,.15);display:flex;flex-wrap:wrap;gap:6px 18px;justify-content:center;font-family:var(--serif);font-size:13.5px;color:#6b625b}
.sfoot a{color:inherit}@media(max-width:760px){.sfoot{padding:22px 20px 30px}}</style>'''
def ag_html(pt,logo):
    if pt: t=('Bem-vindo à Vinha dos Padres','Tem idade legal para consumir bebidas alcoólicas (18 anos ou mais)?','Sim, tenho 18+','Não','Lamentamos, este site destina-se a maiores de 18 anos.','Não usamos cookies de rastreamento; só guardamos as suas preferências no navegador.','Política de privacidade','privacy-pt.html')
    else: t=('Welcome to Vinha dos Padres','Are you of legal drinking age (18 or over)?','Yes, I am 18+','No','Sorry, this site is for adults of legal drinking age.','We use no tracking cookies; only your preferences are stored in your browser.','Privacy policy','privacy.html')
    return f'''<div id="ageGate" role="dialog" aria-modal="true" aria-labelledby="agt" hidden><div class="b"><h2 id="agt" class="lg" aria-label="{t[0]}">{logo}</h2><p>{t[1]}</p><div class="a"><button class="y" id="agY">{t[2]}</button><button id="agN">{t[3]}</button></div><div class="no">{t[4]}</div></div></div>'''
AG_JS='''<script id="agjs">(function(){var G=document.getElementById('ageGate'),ok=false;try{ok=localStorage.getItem('vdpAge')==='1'}catch(_){}
if(/privacy|404/.test(location.pathname)||ok)return;G.hidden=false;document.getElementById('agY').focus();
document.getElementById('agY').onclick=function(){try{localStorage.setItem('vdpAge','1')}catch(_){}G.hidden=true;};
document.getElementById('agN').onclick=function(){G.classList.add('denied');};})();</script>'''
def foot(pt):
    if pt: return '<footer class="sfoot"><span>© Vinha dos Padres, Lda. 2026</span><a href="privacy-pt.html">Política de privacidade</a><span>Beba com moderação · 18+</span><a href="contact-pt.html">Contacto</a></footer>'
    return '<footer class="sfoot"><span>© Vinha dos Padres, Lda. 2026</span><a href="privacy.html">Privacy policy</a><span>Please drink responsibly · 18+</span><a href="contact.html">Contact</a></footer>'
FAVL='<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="apple-touch-icon.png">'
for f in glob.glob(S+'*.html'):
    fn=os.path.basename(f); pt=fn.endswith('-pt.html'); h=open(f).read()
    h=re.sub(r'<link rel="(icon|apple-touch-icon|shortcut icon)"[^>]*>','',h)
    h=h.replace('</title>','</title>'+FAVL,1)
    for tag in ('agcss','agjs'): h=re.sub(rf'<(style|script) id="{tag}">.*?</\1>','',h,flags=re.S)
    h=re.sub(r'<div id="ageGate".*?<div class="no">.*?</div>(?:<small>.*?</small>)?</div></div>','',h,flags=re.S)
    h=re.sub(r'<footer class="sfoot">.*?</footer>','',h,flags=re.S)
    m=re.search(r'<svg[^>]*viewBox="0 0 327\.75 47\.65".*?</svg>',h,re.S)
    logo=m.group(0) if m else ''
    h=h.replace('</head>',AG_CSS+'</head>',1)
    h=re.sub(r'(<body[^>]*>)',lambda mm:mm.group(1)+ag_html(pt,logo),h,count=1)
    if fn.split('-pt')[0].replace('.html','') not in ('index','history','404'):
        i=h.rfind('</main>')
        j=h.find('<script',i); j=j if j>0 else h.rfind('</body>')
        # place footer after any post-main blocks (newsletter etc.) but before scripts
        h=h[:j]+foot(pt)+h[j:]
    if fn.startswith('history'):
        h=h.replace('<section class="faq" id="faq">','<section class="faq" id="faq">',1)
        a=h.find('<div class="nxt">')
        if a>0:
            b=h.find('</div></div>',a)+12
            h=h[:b]+foot(pt).replace('class="sfoot"','class="sfoot" style="padding-left:0;padding-right:0;margin-top:40px"')+h[b:]
    i=h.rfind('</body>'); h=h[:i]+AG_JS+h[i:]
    open(f,'w').write(h)
# ---------- sitemap + robots ----------
NAMES=['index','history','wines','qdvdp-3m12m-2022-white','qdvdp-3m12m-2022-red','qdvdp-3m3m-2023-white','qdvdp-3m3m4m-2023-red','code','recognition','contact','privacy']
def u(n,pt): return SITE+('/' if n=='index' and not pt else ('/index-pt' if n=='index' else f'/{n}{"-pt" if pt else ""}'))
xs=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for n in NAMES:
    for pt in (False,True):
        xs.append(f'<url><loc>{u(n,pt)}</loc><xhtml:link rel="alternate" hreflang="en" href="{u(n,False)}"/><xhtml:link rel="alternate" hreflang="pt-PT" href="{u(n,True)}"/><xhtml:link rel="alternate" hreflang="x-default" href="{u(n,False)}"/><lastmod>2026-11-20</lastmod></url>')
xs.append('</urlset>')
open(S+'sitemap.xml','w').write('\n'.join(xs))
open(S+'robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('legal ok')
