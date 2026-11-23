"""Google Analytics 4 (G-41RP4EYP2D) with Consent Mode v2 + cookie choice.
Idempotent: strips previous blocks (by id) and re-injects into every site/*.html.
- First visit: cookie line inside the age gate (separate Accept / Decline).
- Gate not shown (already 18+, or privacy/404/wineinfo) and no choice yet: bottom bar.
- Choice stored in localStorage 'vdpCk' ('1' accept / '0' decline).
- Privacy page: 'Cookie settings' button reopens the bar.
Run after seo_launch.py (seo_launch calls it at the end).
"""
import re, glob, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
GA = 'G-41RP4EYP2D'

HEAD = ('<script id="gacfg">window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
        "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500});"
        "try{if(localStorage.getItem('vdpCk')==='1')gtag('consent','update',{analytics_storage:'granted'});}catch(_){}"
        "gtag('js',new Date());gtag('config','" + GA + "');</script>"
        '<script id="gasrc" async src="https://www.googletagmanager.com/gtag/js?id=' + GA + '"></script>')

CSS = ('<style id="ckcss">#ageGate .ck{border-top:1px solid #b9ae9c;margin-top:26px;padding-top:16px}'
       '#ageGate .ck p{font-size:14px;margin:0 0 10px;line-height:1.4}#ageGate .ck a{color:inherit}'
       '#ageGate .ck button,#ckBar button{font-size:14px;font-weight:600;padding:5px 18px;background:none;color:#231F20}'
       '#ageGate.denied .ck,#ageGate .ck[hidden]{display:none}'
       '#ckBar{position:fixed;left:0;right:0;bottom:0;z-index:999;background:#E6DED0;color:#231F20;font-family:var(--serif,Georgia,serif);'
       'border-top:1px solid #b9ae9c;padding:12px 16px calc(12px + env(safe-area-inset-bottom));display:flex;gap:10px 16px;align-items:center;justify-content:center;flex-wrap:wrap}'
       '#ckBar[hidden]{display:none}#ckBar p{margin:0;font-size:15px;line-height:1.4;color:#4a433f}#ckBar a{color:inherit}#ckBar .a{display:flex;gap:8px}'
       '#ckBar button{font-family:inherit;border-radius:999px;border:1.5px solid #231F20;cursor:pointer}'
       'button[data-ckopen]{font:inherit;font-size:15px;font-weight:600;padding:3px 16px;margin-left:4px;border-radius:999px;border:1.5px solid #231F20;background:none;color:#231F20;cursor:pointer;font-style:normal}</style>')

T = {'en': ('We use analytics cookies to see how the site is used.', 'Privacy', 'privacy.html', 'Accept', 'Decline', 'Cookie settings'),
     'pt': ('Usamos cookies de análise para perceber como o site é utilizado.', 'Privacidade', 'privacy-pt.html', 'Aceitar', 'Recusar', 'Definições de cookies')}

def inner(t, pre):
    return (f'<p>{t[0]} <a href="{t[2]}">{t[1]}</a></p><div class="a">'
            f'<button type="button" data-ck="1" id="{pre}A">{t[3]}</button><button type="button" data-ck="0" id="{pre}D">{t[4]}</button></div>')

JS = ("<script id=\"ckjs\">(function(){var c=null;try{c=localStorage.getItem('vdpCk')}catch(_){}"
      "var G=document.getElementById('ageGate'),K=document.getElementById('ckG'),B=document.getElementById('ckBar');"
      "function set(v){try{localStorage.setItem('vdpCk',v)}catch(_){}c=v;"
      "if(typeof gtag==='function')gtag('consent','update',{analytics_storage:v==='1'?'granted':'denied'});"
      "if(K)K.hidden=true;B.hidden=true;}"
      "document.querySelectorAll('[data-ck]').forEach(function(b){b.addEventListener('click',function(){set(b.getAttribute('data-ck'))})});"
      "if(c!==null){if(K)K.hidden=true;}else if(!G||G.hidden){B.hidden=false;}"
      "document.querySelectorAll('[data-ckopen]').forEach(function(b){b.addEventListener('click',function(){B.hidden=false})});"
      "})();</script>")

PRIV = {
 'en': [("<h2>cookies and local storage</h2><p>We do not use advertising or tracking cookies. The site stores a few preferences in your own browser (your language, that you confirmed your age, that you closed the welcome note). They never leave your device and you can clear them at any time in your browser settings.</p>",
         "<h2>cookies and local storage</h2><p>With your consent, we use Google Analytics (Google Ireland Ltd.) to understand how the site is used: which pages are viewed, roughly from which country, and on what kind of device. It sets analytics cookies (_ga), which last up to 2 years. If you decline, no analytics cookies are set and Google receives only anonymous signals with no identifiers. We do not use advertising cookies. You can change your choice at any time: <button type=\"button\" data-ckopen>Cookie settings</button></p><p>The site also stores a few preferences in your own browser (your language, that you confirmed your age, your cookie choice, that you closed the welcome note). They never leave your device and you can clear them at any time in your browser settings.</p>"),
        ("<li>Code libraries (d3, three.js) are loaded from public CDNs (cdnjs, jsDelivr), which see your IP address as part of the request.</li>",
         "<li>Google Analytics, only if you accept analytics cookies (see above).</li>")],
 'pt': [("<h2>cookies e armazenamento local</h2><p>Não usamos cookies de publicidade nem de rastreamento. O site guarda algumas preferências no seu próprio navegador (o idioma, a confirmação da idade e o fecho da nota de boas-vindas). Não saem do seu dispositivo e pode apagá-las a qualquer momento nas definições do navegador.</p>",
         "<h2>cookies e armazenamento local</h2><p>Com o seu consentimento, usamos o Google Analytics (Google Ireland Ltd.) para perceber como o site é utilizado: que páginas são vistas, aproximadamente de que país e em que tipo de dispositivo. Coloca cookies de análise (_ga), que duram até 2 anos. Se recusar, não são colocados cookies de análise e a Google recebe apenas sinais anónimos, sem identificadores. Não usamos cookies de publicidade. Pode alterar a sua escolha a qualquer momento: <button type=\"button\" data-ckopen>Definições de cookies</button></p><p>O site guarda também algumas preferências no seu próprio navegador (o idioma, a confirmação da idade, a sua escolha de cookies e o fecho da nota de boas-vindas). Não saem do seu dispositivo e pode apagá-las a qualquer momento nas definições do navegador.</p>"),
        ("<li>Bibliotecas de código (d3, three.js) são carregadas de CDN públicas (cdnjs, jsDelivr), que veem o seu endereço IP como parte do pedido.</li>",
         "<li>Google Analytics, apenas se aceitar os cookies de análise (ver acima).</li>")]}

n = 0
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    fn = os.path.basename(f); lang = 'pt' if fn.endswith('-pt.html') else 'en'; t = T[lang]
    h = open(f, encoding='utf-8').read()
    for tag in ('gacfg', 'gasrc', 'ckcss', 'ckjs'):
        h = re.sub(rf'<(style|script) id="{tag}"[^>]*>.*?</\1>', '', h, flags=re.S)
    h = re.sub(r'<div class="ck" id="ckG".*?</div></div>', '', h, flags=re.S)
    h = re.sub(r'<div id="ckBar".*?</div></div>', '', h, flags=re.S)
    h = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + HEAD, h, count=1)
    h = h.replace('</head>', CSS + '</head>', 1)
    if 'id="ageGate"' in h:
        h = re.sub(r'(<div id="ageGate".*?<div class="no">.*?</div>)', lambda m: m.group(1) + '<div class="ck" id="ckG">' + inner(t, 'ckg') + '</div>', h, count=1, flags=re.S)
    bar = '<div id="ckBar" role="region" aria-label="' + t[5] + '" hidden>' + inner(t, 'ckb') + '</div>'
    i = h.rfind('</body>'); h = h[:i] + bar + JS + h[i:]
    if fn.startswith('privacy'):
        for a, b in PRIV[lang]:
            if a in h: h = h.replace(a, b, 1)
        h = h.replace(' class="wl" data-ckopen', ' data-ckopen')
    open(f, 'w', encoding='utf-8').write(h); n += 1
print('consent ok', n)
