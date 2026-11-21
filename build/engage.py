import re
S='/home/claude/vdp/s63/'
def rd(f): return open(S+f).read()
def wr(f,h): open(S+f,'w').write(h)

# ---------- newsletter block ----------
NL_CSS='''<style id="nlcss">.nl{max-width:760px;margin:70px auto 0;padding:30px 28px 28px;border-top:1px solid rgba(35,31,32,.2);text-align:center;font-family:var(--serif)}
.nl h2{font-family:var(--serif);font-weight:600;font-style:italic;font-size:28px;margin:0 0 6px}.nl p{margin:0 0 16px;color:#6b625b;font-size:17px}
.nl form{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}.nl input{font:inherit;font-size:16px;padding:9px 16px;border:1.5px solid #231F20;border-radius:999px;background:rgba(255,255,255,.35);min-width:260px;color:#231F20}
.nl button{font:inherit;font-size:16px;font-weight:600;padding:9px 20px;border-radius:999px;border:1.5px solid #231F20;background:#231F20;color:#E6DED0;cursor:pointer}
.nl button:hover{background:#C76653;border-color:#C76653}.nl .ok{display:none;margin-top:12px;font-size:16px}.nl.done form{display:none}.nl.done .ok{display:block}
.nl small{display:block;margin-top:10px;font-size:12.5px;color:#8a8079}
.nxt{max-width:760px;margin:60px auto 0;text-align:center;font-family:var(--serif)}.nxt a{display:inline-flex;flex-direction:column;align-items:center;gap:2px;text-decoration:none;color:#231F20;padding:14px 30px;border:1.5px solid #231F20;border-radius:18px}
.nxt a:hover{border-color:#C76653;color:#C76653}.nxt small{font-size:13px;color:#6b625b;letter-spacing:.06em}.nxt b{font-size:24px;font-style:italic}
@media(max-width:760px){.nl{margin-top:50px;padding:24px 4px}.nl input{min-width:0;width:100%}.nl button{width:100%}}</style>'''
NL_HTML='''<section class="nl" id="newsletter"><h2>be first for the next release</h2><p>Our wines are made in tiny quantities. Join the list to hear about new vintages before they sell out.</p>
<form class="nlf" novalidate><input type="email" name="email" placeholder="your email" required aria-label="Email address"><button type="submit">join the list</button></form>
<div class="ok">Thank you, you’re on the list.</div><small>Only news about our wines, a few times a year. Unsubscribe any time.</small></section>'''
NL_JS='''<script id="nljs">document.querySelectorAll('.nlf').forEach(f=>f.addEventListener('submit',async e=>{e.preventDefault();const i=f.querySelector('input'),b=f.querySelector('button');
if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(i.value)){i.focus();i.style.borderColor='#C76653';return;}b.disabled=true;
try{await fetch('https://formsubmit.co/ajax/vdp@silimosa.com',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({email:i.value,_subject:'Mailing list sign-up: '+i.value,page:location.pathname.split('/').pop()||'index.html',_template:'table'})});}catch(_){}
f.closest('.nl').classList.add('done');}));</script>'''
def nxt(href,label): return f'<div class="nxt"><a href="{href}"><small>next chapter</small><b>{label} →</b></a></div>'

PAGES={
 'history.html':('code.html','the code'),
 'code.html':('wines.html','our wines'),
 'wines.html':('recognition.html','recognition'),
 'recognition.html':('contact.html','get in touch'),
}
NL_ON={'code.html','wines.html','contact.html','qdvdp-3m12m-2022-white.html','qdvdp-3m12m-2022-red.html','qdvdp-3m3m-2023-white.html','qdvdp-3m3m4m-2023-red.html'}
import glob
for f in sorted(set(PAGES)|NL_ON):
    h=rd(f)
    if 'id="nlcss"' in h: continue
    blk=(NL_HTML if f in NL_ON else '')+(nxt(*PAGES[f]) if f in PAGES else '')
    if f=='history.html':
        a=h.find('<section class="faq" id="faq">'); b=h.find('</section>',a)+10
        h=h[:b]+'<div style="padding:0 6%">'+blk+'</div>'+h[b:]
    elif f=='contact.html':
        a=h.rfind('</main>'); h=h[:a]+'</main><div style="padding:0 20px 80px">'+blk+'</div>'+h[a+7:]
    else:
        a=h.rfind('</main>'); h=h[:a]+blk+h[a:]
    h=h.replace('</head>',NL_CSS+'</head>',1)
    if f in NL_ON: h=h.replace('</body>',NL_JS+'</body>',1)
    wr(f,h); print('ok',f)

# ---------- Estate: welcome card + proof line ----------
h=rd('index.html')
if 'id="welcome"' not in h:
    W_CSS='''<style id="wlcss">#welcome{position:fixed;left:24px;bottom:calc(24px + env(safe-area-inset-bottom,0px));z-index:60;max-width:380px;background:#EDE6DA;border:1px solid rgba(35,31,32,.18);border-radius:18px;padding:20px 22px 18px;box-shadow:0 14px 40px rgba(0,0,0,.16);font-family:var(--serif);color:#231F20}
#welcome[hidden]{display:none}#welcome h2{font-family:var(--serif);font-weight:600;font-style:italic;font-size:26px;margin:0 0 6px;line-height:1.1}#welcome p{margin:0 0 12px;font-size:15.5px;line-height:1.4;color:#4a433f}
#welcome .proof{display:block;margin:0 0 14px;font-size:14.5px;color:#231F20;text-decoration:none;border-left:3px solid #C76653;padding-left:10px}#welcome .proof b{color:#C76653}
#welcome .acts{display:flex;gap:8px;flex-wrap:wrap}#welcome .acts a,#welcome .acts button{font:inherit;font-size:14.5px;font-weight:600;padding:7px 15px;border-radius:999px;border:1.5px solid #231F20;background:none;color:#231F20;cursor:pointer;text-decoration:none}
#welcome .acts .solid{background:#231F20;color:#E6DED0}#welcome .x2{position:absolute;top:10px;right:12px;border:0;background:none;font-size:20px;cursor:pointer;color:#6b625b;line-height:1}
#proofTag{position:fixed;left:18px;bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:40;font-family:var(--serif);font-size:14px;color:#231F20;text-decoration:none;background:rgba(237,230,218,.94);border:1px solid rgba(35,31,32,.15);border-radius:999px;padding:6px 14px}
#proofTag b{color:#C76653}#proofTag:hover{border-color:#C76653}body.in-axo #proofTag,body.in-axo #welcome{display:none}
body.phone #welcome{left:12px;right:12px;max-width:none;bottom:auto;top:calc(70px + env(safe-area-inset-top,0px))}body.phone #proofTag{display:none}</style>'''
    W_HTML='''<div id="welcome" hidden role="dialog" aria-label="Welcome"><button class="x2" aria-label="Close">×</button><h2 data-en="Welcome to Vinha dos Padres" data-pt="Bem-vindo à Vinha dos Padres">Welcome to Vinha dos Padres</h2>
<p data-en="Altitude centenary bush vines in the Serra de São Mamede, made into wine in centenary amphoras. Click any property on the map to explore it in 3D." data-pt="Vinhas velhas centenárias em altitude na Serra de São Mamede, vinificadas em talhas centenárias. Clique numa propriedade no mapa para a explorar em 3D.">Altitude centenary bush vines in the Serra de São Mamede, made into wine in centenary amphoras. Click any property on the map to explore it in 3D.</p>
<a class="proof" href="recognition.html"><span data-en="Our first harvest was" data-pt="A nossa primeira colheita foi">Our first harvest was</span> <b>#32 Top 100 Portugal</b> · <b>94–95 pts</b></a>
<div class="acts"><button class="solid" id="wlgo" data-en="Explore the vineyard" data-pt="Explorar a vinha">Explore the vineyard</button><a href="history.html" data-en="Read our story" data-pt="A nossa história">Read our story</a></div></div>
<a id="proofTag" href="recognition.html" hidden><span data-en="Our first harvest was" data-pt="A nossa primeira colheita foi">Our first harvest was</span> <b>#32 Top 100 Portugal</b> · <b>94–95 pts</b></a>'''
    W_JS='''<script id="wljs">(function(){const W=document.getElementById('welcome'),P=document.getElementById('proofTag');let seen=false;try{seen=localStorage.getItem('vdpWelcome')==='1'}catch(_){}
const lang=()=>document.documentElement.lang&&document.documentElement.lang.startsWith('pt')?'pt':'en';
const tr=()=>[W,P].forEach(r=>r.querySelectorAll('[data-en]').forEach(e=>e.textContent=e.dataset[lang()]));
function close(){W.hidden=true;P.hidden=false;try{localStorage.setItem('vdpWelcome','1')}catch(_){}}
W.querySelector('.x2').onclick=close;document.getElementById('wlgo').onclick=close;
if(location.hash){W.hidden=true;P.hidden=false;}else if(seen){P.hidden=false;}else{W.hidden=false;}
tr();new MutationObserver(tr).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
const ax=document.getElementById('axo');if(ax)new MutationObserver(()=>document.body.classList.toggle('in-axo',ax.classList.contains('on'))).observe(ax,{attributes:true,attributeFilter:['class']});})();</script>'''
    h=h.replace('</head>',W_CSS+'</head>',1)
    i=h.rfind('</body>'); h=h[:i]+W_HTML+W_JS+h[i:]
    wr('index.html',h); print('ok index')
