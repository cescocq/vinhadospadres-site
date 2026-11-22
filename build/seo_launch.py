"""Pre-launch SEO pass (Nov 2026): titles, descriptions, share tags, favicons, JSON-LD.
Run from repo root: python3 build/seo_launch.py  (idempotent)."""
import re, glob, html
SITE='site'
BASE='https://www.vinhadospadres.com'
T={  # page -> (title or None to keep, description or None to keep)
 'index':("Vinha dos Padres | Centenary Vines & Talha Wine, Serra de São Mamede",
          "Altitude centenary bush vines in the Serra de São Mamede, made into wine in centenary amphoras. Click any property on the map to explore it in 3D."),
 'index-pt':("Vinha dos Padres | Vinhas centenárias e vinho de talha, Serra de São Mamede",
          "Vinhas velhas centenárias em altitude na Serra de São Mamede, vinificadas em talhas centenárias. Clique numa propriedade no mapa para a explorar em 3D."),
 'history':(None,"From the Jesuits' 1534 vow in Paris to an altitude talha wine estate in Reguengo, Portalegre: the history of Vinha dos Padres in the Serra de São Mamede."),
 'history-pt':(None,"Do voto jesuíta de 1534 em Paris a uma propriedade de vinho de talha em altitude no Reguengo, Portalegre: a história da Vinha dos Padres."),
 'code':(None,"How to read the code on every Vinha dos Padres label: months of skin maceration and ageing in centenary amphoras (talhas), plus ageing in other vessels."),
 'code-pt':(None,"Como ler o código de cada rótulo da Vinha dos Padres: meses de maceração e de estágio em talhas centenárias, e estágio adicional noutro recipiente."),
 'recognition':(None,"Reviews, awards and press for Vinha dos Padres, including #32 with 94 points in James Suckling's Top 100 Wines of Portugal 2025."),
 'recognition-pt':(None,"Críticas, prémios e imprensa sobre a Vinha dos Padres, incluindo o 32.º lugar com 94 pontos no Top 100 Wines of Portugal 2025 de James Suckling."),
 'contact':(None,"Get in touch with Vinha dos Padres in Reguengo, Portalegre, Serra de São Mamede, or sign up for news and new releases."),
 'amphora-wine':(None,None),
 'contact-pt':(None,"Contacte a Vinha dos Padres no Reguengo, Portalegre, Serra de São Mamede, ou subscreva as novidades e os novos lançamentos."),
}
ICONS=('<link rel="icon" href="favicon.ico" sizes="48x48">'
       '<link rel="icon" type="image/png" href="favicon-32.png" sizes="32x32">'
       '<link rel="icon" type="image/png" href="favicon-192x192.png" sizes="192x192">')
ALT={'en':"Vinha dos Padres: centenary bush vines in the morning mist, Serra de São Mamede",
     'pt':"Vinha dos Padres: vinhas centenárias em vaso na neblina da manhã, Serra de São Mamede"}
LD='''<script type="application/ld+json">{"@context":"https://schema.org","@type":"Winery","@id":"%s/#winery","name":"Vinha dos Padres","legalName":"Vinha dos Padres, Lda.","url":"%s/","logo":"%s/logo-est.svg","image":"%s/og-image.jpg","foundingDate":"1795","description":"%s","address":{"@type":"PostalAddress","addressLocality":"Reguengo","addressRegion":"Portalegre","addressCountry":"PT"}}</script>'''
LDD={'en':"Altitude amphora (talha) wine estate with centenary bush vines in the Serra de São Mamede, DOC Alentejo Portalegre.",
     'pt':"Propriedade de vinho de talha em altitude, com vinhas centenárias em vaso na Serra de São Mamede, DOC Alentejo Portalegre."}
def setmeta(h,attr,key,val):
    tag=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}">'
    pat=re.compile(rf'<meta {attr}="{re.escape(key)}" content="[^"]*">')
    if pat.search(h): return pat.sub(lambda m:tag,h,count=1)
    return h.replace('</head>',tag+'\n</head>',1)
for f in sorted(glob.glob(f'{SITE}/*.html')):
    page=f.split('/')[-1][:-5]; h=open(f,encoding='utf-8').read()
    lang='pt' if 'lang="pt' in h[:300] else 'en'
    noindex='name="robots"' in h and 'noindex' in (re.search(r'name="robots" content="([^"]*)"',h) or [0,''])[1]
    # favicons
    h=re.sub(r'<link rel="icon" href="favicon\.svg" type="image/svg\+xml"><link rel="icon" href="favicon-32\.png" sizes="32x32">',ICONS,h)
    title,desc=T.get(page,(None,None))
    if title: h=re.sub(r'<title>[^<]*</title>',f'<title>{html.escape(title,quote=False)}</title>',h,count=1)
    if desc: h=setmeta(h,'name','description',desc)
    t=html.unescape(re.search(r'<title>([^<]*)</title>',h)[1])
    d=html.unescape((re.search(r'<meta name="description" content="([^"]*)"',h) or [0,''])[1])
    if page not in ('index','index-pt') and 'og:title' in h: h=setmeta(h,'property','og:title',t)
    if d and 'og:description' in h: h=setmeta(h,'property','og:description',d)
    if not noindex or page=='404':
        for k,v in [('og:image',BASE+'/og-image.jpg'),('og:image:width','1200'),('og:image:height','630'),('og:image:alt',ALT[lang])]:
            h=setmeta(h,'property',k,v)
        h=setmeta(h,'name','twitter:card','summary_large_image')
        h=setmeta(h,'name','twitter:image',BASE+'/og-image.jpg')

    # Amphora guide: footer link + contextual links (idempotent)
    if page not in ('amphora-wine','amphora-wine-pt'):
        ah,at=('amphora-wine-pt.html','Vinho de talha') if lang=='pt' else ('amphora-wine.html','Amphora wine')
        if '<footer class="sfoot">' in h and f'href="{ah}"' not in h.split('<footer class="sfoot">',1)[1]:
            h=re.sub(r'(<footer class="sfoot">.*?<a href="privacy(?:-pt)?\.html">[^<]*</a>)',lambda m:m.group(1)+f'<a href="{ah}">{at}</a>',h,count=1,flags=re.S)
    CTX={'code':(' Vinha dos Padres is at the forefront of scientifically investigating the use of old amphoras and their winemaking qualities.</p>',' <a class="wl" href="amphora-wine.html">What is amphora (talha) wine? →</a>'),
         'code-pt':(' A Vinha dos Padres está na vanguarda da investigação científica sobre o uso de ânforas antigas e as suas qualidades enológicas.</p>',' <a class="wl" href="amphora-wine-pt.html">O que é o vinho de talha? →</a>'),
         'history':("a tradition practised in Portugal's Alentejo region for more than 2,000 years.</p></details>",' <a class="wl" href="amphora-wine.html">Read our guide to amphora wine →</a>'),
         'history-pt':('uma tradição praticada no Alentejo há mais de 2000 anos.</p></details>',' <a class="wl" href="amphora-wine-pt.html">Leia o nosso guia do vinho de talha →</a>')}
    if page in CTX:
        a,lnk=CTX[page]; key=lnk.split('href="')[1].split('"')[0]
        if a in h and lnk not in h:
            h=h.replace(a,a.replace('</p>',lnk+'</p>',1),1)
    if page in ('index','index-pt') and '"@type":"Winery"' not in h:
        h=h.replace('</head>',LD%(BASE,BASE,BASE,BASE,LDD[lang])+'\n</head>',1)
    open(f,'w',encoding='utf-8').write(h)
print('done')
