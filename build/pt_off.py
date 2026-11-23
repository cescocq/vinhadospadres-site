"""Switch the Portuguese version of the live site off or back on.  Idempotent.
    python3 build/pt_off.py off   # PT button shows "coming soon", -pt URLs redirect (302) to English, PT out of sitemap/hreflang/llms
    python3 build/pt_off.py on    # undo everything
Run from the repo root, then python3 build/seo_launch.py as usual."""
import re, sys, glob, os
MODE = (sys.argv[1] if len(sys.argv) > 1 else 'off').lower(); assert MODE in ('off', 'on')
S = 'site/'; B = 'https://www.vinhadospadres.com/'
PT = sorted(os.path.basename(f)[:-8] for f in glob.glob(S + '*-pt.html'))           # base names that have a -pt page
EN = [f for f in glob.glob(S + '*.html') if not f.endswith('-pt.html') and not f.endswith('wineinfo.html')]  # wineinfo (label QR page) stays bilingual

GUARD = '''<script id="ptsoon">(function(){var t;try{localStorage.setItem('vdpLang','en')}catch(_){}function soon(e){var b=e.target.closest&&e.target.closest('button,a');if(!b||!b.closest('.seg'))return;
var k=(b.getAttribute('data-lang')||b.getAttribute('data-l')||b.textContent||'').trim().toLowerCase();if(k!=='pt')return;
e.preventDefault();e.stopImmediatePropagation();if(!e.isTrusted)return;var d=document.getElementById('ptsoonT');
if(!d){d=document.createElement('div');d.id='ptsoonT';d.setAttribute('role','status');d.innerHTML='<b>Português em breve</b><span>Portuguese version coming soon</span>';
d.style.cssText='position:fixed;left:50%;top:calc(18px + env(safe-area-inset-top,0px));transform:translate(-50%,-8px);z-index:2147483000;background:#231F20;color:#E6DED0;border-radius:999px;padding:9px 18px;font-family:var(--serif,Georgia,serif);font-style:italic;font-size:15px;display:flex;flex-direction:column;align-items:center;line-height:1.25;text-align:center;white-space:nowrap;box-shadow:0 8px 24px rgba(35,31,32,.25);opacity:0;transition:opacity .2s,transform .2s;pointer-events:none';
d.lastChild.style.cssText='font-size:12.5px;opacity:.75;white-space:nowrap';d.firstChild.style.whiteSpace='nowrap';document.body.appendChild(d);}
requestAnimationFrame(function(){d.style.opacity='1';d.style.transform='translate(-50%,0)';});clearTimeout(t);t=setTimeout(function(){d.style.opacity='0';d.style.transform='translate(-50%,-8px)';},2200);}
['click','pointerup','touchend'].forEach(function(ev){document.addEventListener(ev,function(e){if(ev==='click')soon(e);else{var b=e.target.closest&&e.target.closest('.seg button');if(b&&/^pt$/i.test((b.getAttribute('data-lang')||b.getAttribute('data-l')||b.textContent).trim())){e.stopImmediatePropagation();}}},true);});
document.querySelectorAll('.seg button').forEach(function(b){if(/^pt$/i.test((b.getAttribute('data-lang')||b.getAttribute('data-l')||b.textContent).trim())){b.title='Português em breve · Portuguese coming soon';b.style.opacity='.55';}});})();</script>'''

ALT_RE = re.compile(r'\s*<link rel="alternate" hreflang="pt-PT" href="[^"]*">')

def page_alt(name):
    slug = '' if name == 'index' else name
    return f'<link rel="alternate" hreflang="pt-PT" href="{B}{name}-pt">' if name != 'index' else f'<link rel="alternate" hreflang="pt-PT" href="{B}index-pt">'

changed = 0
for f in EN:
    h = open(f, encoding='utf-8').read(); o = h; name = os.path.basename(f)[:-5]
    h = re.sub(r'\n?<!--pt-alt (<link rel="alternate" hreflang="pt-PT" href="[^"]*">) -->', r'\n\1', h)   # normalise first
    if MODE == 'off':
        h = re.sub(r'<script id="ptsoon">.*?</script>\n?', '', h, flags=re.S)
        h = h.replace('</body>', GUARD + '\n</body>', 1)
        if name in PT:
            m = ALT_RE.search(h)
            if m:
                h = h.replace(m.group(0), '\n<!--pt-alt ' + m.group(0).strip() + ' -->', 1)
    else:
        h = re.sub(r'<script id="ptsoon">.*?</script>\n?', '', h, flags=re.S)
        h = re.sub(r'\n?<!--pt-alt (<link rel="alternate" hreflang="pt-PT" href="[^"]*">) -->', r'\n\1', h)
    if h != o: open(f, 'w', encoding='utf-8').write(h); changed += 1

# _redirects: temporary redirects for every -pt address
R = S + '_redirects'; r = open(R, encoding='utf-8').read()
r = re.sub(r'\n?# PT-OFF START.*?# PT-OFF END\n?', '\n', r, flags=re.S)
if MODE == 'off':
    lines = ['# PT-OFF START (Portuguese temporarily disabled; remove with build/pt_off.py on)']
    for n in PT:
        en = '/' if n == 'index' else '/' + n
        lines += [f'/{n}-pt {en} 302', f'/{n}-pt.html {en} 302']
    lines.append('# PT-OFF END')
    r = '\n'.join(lines) + '\n' + r.lstrip('\n')      # first so they win
open(R, 'w', encoding='utf-8').write(r)

# sitemap: drop PT urls and PT alternates (kept in build/sitemap_full.xml for 'on')
SM = S + 'sitemap.xml'; FULL = 'build/sitemap_full.xml'
if MODE == 'off':
    sm = open(SM, encoding='utf-8').read()
    if '-pt</loc>' in sm:
        open(FULL, 'w', encoding='utf-8').write(sm)
        sm = re.sub(r'<url><loc>[^<]*-pt</loc>.*?</url>\n?', '', sm, flags=re.S)
        sm = re.sub(r'<xhtml:link rel="alternate" hreflang="pt-PT" href="[^"]*"/>', '', sm)
        open(SM, 'w', encoding='utf-8').write(sm)
elif os.path.exists(FULL):
    open(SM, 'w', encoding='utf-8').write(open(FULL, encoding='utf-8').read())

# llms.txt / llms-full.txt wording
for L in (S + 'llms.txt', S + 'llms-full.txt'):
    if not os.path.exists(L): continue
    t = open(L, encoding='utf-8').read()
    on_txt = 'The site is bilingual: English pages are at the paths below; Portuguese versions add the suffix `-pt` (the Portuguese homepage is `/index-pt`).'
    off_txt = 'The site is in English; a Portuguese version is coming soon.'
    t = t.replace(on_txt, off_txt) if MODE == 'off' else t.replace(off_txt, on_txt)
    t = t.replace('Portuguese versions add the suffix `-pt` to each address.', 'A Portuguese version is coming soon.') if MODE == 'off' else t.replace('A Portuguese version is coming soon.', 'Portuguese versions add the suffix `-pt` to each address.')
    open(L, 'w', encoding='utf-8').write(t)
print(f'PT {MODE}: {changed} English pages updated; {len(PT)} PT pages', 'redirected' if MODE == 'off' else 'restored')
