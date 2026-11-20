import re,glob,os
S='/home/claude/vdp/s65/'
SITE='https://www.vinhadospadres.com'
def url(name,pt):
    if name=='index': return SITE+('/index-pt' if pt else '/')
    return f'{SITE}/{name}{"-pt" if pt else ""}'
SLUG={'quinta-da-vinha-dos-padres-2022-white-3m12m':'qdvdp-3m12m-2022-white','quinta-da-vinha-dos-padres-2022-red-3m12m':'qdvdp-3m12m-2022-red',
      'quinta-da-vinha-dos-padres-2023-white-3m3m':'qdvdp-3m3m-2023-white','quinta-da-vinha-dos-padres-2023-red-3m3m4m':'qdvdp-3m3m4m-2023-red'}
for f in glob.glob(S+'*.html'):
    fn=os.path.basename(f)[:-5]
    if fn=='404': continue
    pt=fn.endswith('-pt'); name=fn[:-3] if pt else fn
    h=open(f).read()
    for k,v in SLUG.items(): h=h.replace(f'{SITE}/wines/{k}',f'{SITE}/{v}')
    h=h.replace(f'{SITE}/wines/compare',f'{SITE}/compare').replace(f'{SITE}/history-amphora-talha-wine',f'{SITE}/history')
    h=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{url(name,pt)}">',h)
    h=re.sub(r'<meta property="og:url" content="[^"]*">',f'<meta property="og:url" content="{url(name,pt)}">',h)
    h=re.sub(r'<link rel="alternate" hreflang[^>]*>','',h)
    alts=f'<link rel="alternate" hreflang="en" href="{url(name,False)}"><link rel="alternate" hreflang="pt-PT" href="{url(name,True)}"><link rel="alternate" hreflang="x-default" href="{url(name,False)}">'
    if '<link rel="canonical"' in h: h=h.replace('<link rel="canonical"',alts+'<link rel="canonical"',1)
    else: h=h.replace('</title>','</title>'+alts+f'<link rel="canonical" href="{url(name,pt)}">',1)
    if name=='compare':
        if '<meta name="robots"' not in h: h=h.replace('</title>','</title><meta name="robots" content="noindex, follow">',1)
    open(f,'w').write(h)
print('ok')
