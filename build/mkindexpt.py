import re
S='/home/claude/vdp/s65/'
SITE='https://www.vinhadospadres.com'
h=open(S+'index.html').read()
h=re.sub(r'<script id="estlang">.*?</script>','',h,flags=re.S)
h=re.sub(r'<meta name="description"[^>]*>|<link rel="canonical"[^>]*>|<link rel="alternate"[^>]*>|<meta property="og:[^>]*>','',h)
DESC_EN='Vinha dos Padres: six vineyard properties of centenary bush vines around Reguengo, Portalegre, in the Serra de São Mamede. Explore the estate map and 3D parcels, with harvest and climate data.'
DESC_PT='Vinha dos Padres: seis propriedades de vinhas centenárias em vaso à volta do Reguengo, Portalegre, na Serra de São Mamede. Explore o mapa da propriedade e as parcelas em 3D, com dados de vindima e clima.'
ALTS=f'<link rel="alternate" hreflang="en" href="{SITE}/"><link rel="alternate" hreflang="pt-PT" href="{SITE}/pt/"><link rel="alternate" hreflang="x-default" href="{SITE}/">'
def head(desc,url,locale):
    return (f'<meta name="description" content="{desc}"><link rel="canonical" href="{url}">{ALTS}'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Vinha dos Padres"><meta property="og:locale" content="{locale}">'
            f'<meta property="og:title" content="Vinha dos Padres"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">')
JS='''<script id="estlang">(function(){
var forcePT=/-pt\\.html$/.test(location.pathname);var pref=null;try{pref=localStorage.getItem('vdpLang')}catch(_){}
function cur(){var b=document.querySelector('button[data-lang][aria-pressed="true"]');return b?b.dataset.lang:'en';}
function setL(l){var b=document.querySelector('button[data-lang="'+l+'"]');if(b&&cur()!==l)b.click();}
document.querySelectorAll('button[data-lang]').forEach(function(b){b.addEventListener('click',function(){try{localStorage.setItem('vdpLang',b.dataset.lang)}catch(_){}});});
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var u=a.getAttribute('href');
 if(!/^[a-z0-9-]+\\.html/.test(u))return;var pt=cur()==='pt',isPt=/-pt\\.html/.test(u);
 if(pt&&!isPt)a.setAttribute('href',u.replace(/\\.html/,'-pt.html'));else if(!pt&&isPt)a.setAttribute('href',u.replace(/-pt\\.html/,'.html'));},true);
function go(){setL(forcePT?'pt':(pref==='pt'?'pt':'en'));}
if(document.readyState==='complete')go();else addEventListener('load',go);
})();</script>'''
def build(lang):
    x=h.replace('</title>','</title>'+(head(DESC_PT,SITE+'/pt/','pt_PT') if lang=='pt' else head(DESC_EN,SITE+'/','en_GB')),1)
    if lang=='pt': x=re.sub(r'<html lang="[^"]*"','<html lang="pt-PT"',x,count=1)
    i=x.rfind('</body>'); x=x[:i]+JS+x[i:]
    return x
open(S+'index.html','w').write(build('en'))
open(S+'index-pt.html','w').write(build('pt'))
print('ok')
