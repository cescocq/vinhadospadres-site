import re,json,html,glob,sys
sys.path.insert(0,'/home/claude/vdp')
from pt import PT
from extract import segments
PT['Field blend']='Castas (vinha misturada)'
S='/home/claude/vdp/s65/'
SITE='https://www.vinhadospadres.com'
PAGES=['history','code','wines','recognition','contact','compare','qdvdp-3m12m-2022-white','qdvdp-3m12m-2022-red','qdvdp-3m3m-2023-white','qdvdp-3m3m4m-2023-red']
OURS=['index']+PAGES+['privacy','404']
missing=set()
def tr(s):
    k=html.unescape(s.strip())
    if not re.search('[A-Za-z]{2,}',k): return s
    if k in PT:
        lead=s[:len(s)-len(s.lstrip())]; trail=s[len(s.rstrip()):]
        return lead+html.escape(PT[k],quote=False)+trail
    missing.add(k); return s
def tr_attr(m):
    name,v=m.group(1),m.group(2); k=html.unescape(v)
    if name=='content':
        pre=PAGEH[max(0,m.start()-80):m.start()]
        if not re.search(r'name="description"|property="og:(title|description)"|name="twitter:(title|description)"',pre): return m.group(0)
    if k in PT: return f'{name}="{html.escape(PT[k])}"'
    if re.search('[A-Za-z]{3,}',k) and name!='data-en': missing.add(k)
    return m.group(0)
def relink(h,to_pt):
    def r(m):
        q,u=m.group(1),m.group(2)
        base=re.match(r'([a-z0-9-]+)\.html(.*)',u)
        if not base: return m.group(0)
        name,rest=base.groups()
        if to_pt and name in OURS and not name.endswith('-pt'): return f'href={q}{name}-pt.html{rest}{q}'
        return m.group(0)
    return re.sub(r'href=(["\'])([^"\']+)\1',r,h)
def alt_links(name):
    en=SITE+'/' if name=='index' else f'{SITE}/{name}.html'
    pt=SITE+'/pt/' if name=='index' else f'{SITE}/pt/{name}.html'
    return en,pt,f'<link rel="alternate" hreflang="en" href="{en}"><link rel="alternate" hreflang="pt-PT" href="{pt}"><link rel="alternate" hreflang="x-default" href="{en}">'
LANGJS='''<script id="langjs">(function(){var pt=document.documentElement.lang.indexOf('pt')===0,me=location.pathname.split('/').pop()||'index';
var base=me.replace(/\\.html$/,'').replace(/-pt$/,''),en=base+'.html',ptp=base+'-pt.html';
document.querySelectorAll('.seg button').forEach(function(b){var l=b.textContent.trim();if(l!=='EN'&&l!=='PT')return;b.setAttribute('aria-pressed',String((l==='PT')===pt));
b.addEventListener('click',function(){try{localStorage.setItem('vdpLang',l.toLowerCase())}catch(_){}if((l==='PT')!==pt)location.href=(l==='PT'?ptp:en)+location.search+location.hash;});});
try{localStorage.setItem('vdpLang',pt?'pt':'en')}catch(_){}})();</script>'''
for name in PAGES:
    src=S+name+'.html'; h=open(src).read()
    h=re.sub(r'<script id="langjs">.*?</script>','',h,flags=re.S)
    en,pt,alts=alt_links(name)
    # EN page: hreflang + lang switch script
    he=re.sub(r'<link rel="alternate" hreflang[^>]*>','',h)
    he=re.sub(r'<link rel="alternate"[^>]*>','',he)
    he=he.replace('</title>','</title>'+alts,1)
    i=he.rfind('</body>'); he=he[:i]+LANGJS+he[i:]
    open(src,'w').write(he)
    # PT page
    global PAGEH; PAGEH=he
    out=[];pos=0
    for a,b,t in segments(he):
        out.append(he[pos:a]); out.append(tr(t)); pos=b
    out.append(he[pos:]); p=''.join(out)
    PAGEH=p
    p=re.sub(r'\b(alt|aria-label|placeholder|title|content)="([^"]*)"',tr_attr,p)
    p=re.sub(r'<title>(.*?)</title>',lambda m:'<title>'+html.escape(PT.get(html.unescape(m.group(1)),html.unescape(m.group(1))),quote=False)+'</title>',p,1)
    p=re.sub(r'<html lang="[^"]*"','<html lang="pt-PT"',p,1)
    p=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{pt}">',p)
    p=re.sub(r'<meta property="og:url" content="[^"]*">',f'<meta property="og:url" content="{pt}">',p)
    p=p.replace('<meta property="og:type"','<meta property="og:locale" content="pt_PT"><meta property="og:type"',1)
    p=relink(p,True)
    open(S+name+'-pt.html','w').write(p)
print('MISSING',len(missing)); [print(repr(m)) for m in sorted(missing)]
