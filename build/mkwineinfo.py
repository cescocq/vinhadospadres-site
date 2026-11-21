# Builds s65/wineinfo.html: the unlinked QR-code page from the labels (technical sheets + nutrition declarations).
import re,os
S='/home/claude/vdp/s65/'
src=open(S+'privacy.html').read()
logo=re.search(r'<svg[^>]*viewBox="0 0 327.75 47.65".*?</svg>',src,re.S).group(0)
fonts=''.join(re.findall(r'@font-face\{[^}]*\}',src)[:2])
WINES=[  # year, code, colour
 (2022,'3M12M','white'),(2022,'3M12M','red'),
 (2023,'3M3M','white'),(2023,'3M3M4M','red')]
SOON=[2024,2025]
# Technical sheets live in Google Drive: (PT file id, EN file id). Single source of truth for the whole site.
DRIVE={(2022,'white'):('1TvKC__8R4bnKBQ2Opn4eQcbVTOVESNr9','1XTu2jIP-2QjerL7LrFdbFTJGNL1rA58G'),
       (2022,'red'):('1uTANde9F5EglLWwQqo0KqSJfKKp2QWry','1JIc3mabXtK97p1K7KeWP5gz-0MbzQOoF'),
       (2023,'white'):('1NdFjLVR-S5cJwAHuXJQWXpNFjBn0m1We','1wf0Gg1kcCpu-pVIkmcpKRqwvxQvcP3zZ'),
       (2023,'red'):('13ntR6pBt8l1IVArfieYRNwXW7l8KV6tf','1E-1vWhJYiBPHSR7Roix5cKXYncK1aWGf')}
def drive(i): return f'https://drive.google.com/file/d/{i}/view'
PTC={'white':'branco','red':'tinto'}; AC={'white':'#275FAC','red':'#C76653'}
def pdf(y,c,col,l): return f'pdf/QDVDP{c}_{y}_{l}_{col.upper()}_TS.pdf'
missing=[]
def link(y,c,col,l):
    ids=DRIVE.get((y,col))
    if ids: return f'<a href="{drive(ids[0] if l=="PT" else ids[1])}" target="_blank" rel="noopener">{l}</a>'
    missing.append((y,col,l)); return f'<span class="na" title="em breve / coming soon">{l}</span>'
cols=''
for y in sorted({w[0] for w in WINES}|set(SOON)):
    ws=[w for w in WINES if w[0]==y]
    rows=''.join(f'<li><span class="n">Quinta da Vinha dos Padres {y} {PTC[col]} <b style="color:{AC[col]}">{c}</b></span><span class="l">{link(y,c,col,"PT")} / {link(y,c,col,"EN")}</span></li>' for (_,c,col) in ws) or '<li class="soon">em breve · coming soon</li>'
    cols+=f'<section><h2>{y}</h2><ul>{rows}</ul></section>'
html=f'''<!DOCTYPE html><html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fichas técnicas e declarações nutricionais · Vinha dos Padres</title><meta name="robots" content="noindex">
<link rel="icon" href="favicon.ico" sizes="48x48"><link rel="icon" type="image/png" href="favicon-32.png" sizes="32x32"><link rel="icon" type="image/png" href="favicon-192x192.png" sizes="192x192">
<style>{fonts}:root{{--serif:'Arno Pro',Georgia,serif}}*{{box-sizing:border-box}}
body{{margin:0;background:#E6DED0;color:#231F20;font-family:var(--serif);font-style:italic}}
main{{max-width:1080px;margin:0 auto;padding:40px 28px 60px}}
.lg{{display:block;width:220px;margin:0 0 34px}}.lg svg{{width:100%;height:auto;display:block}}.lg .vdp-l{{fill:#231F20!important}}
h1{{font-weight:600;font-size:clamp(28px,4vw,40px);margin:0;line-height:1.1}}.sub{{font-size:18px;color:#6b625b;margin:6px 0 36px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:34px 48px}}
h2{{font-weight:600;font-size:30px;margin:0 0 14px;padding-bottom:6px;border-bottom:1px solid #231F20}}
ul{{list-style:none;margin:0;padding:0}}li{{display:flex;justify-content:space-between;gap:12px;font-size:17px;padding:8px 0;border-bottom:1px solid rgba(35,31,32,.12)}}
li b{{font-weight:600}}.l{{white-space:nowrap}}.l a{{color:#231F20;font-weight:600}}.na{{color:#a39a90}}.soon{{color:#6b625b}}
footer{{margin-top:48px;font-size:14px;color:#6b625b}}footer a{{color:inherit}}
</style></head><body><main>
<a class="lg" href="/" aria-label="Vinha dos Padres">{logo}</a>
<h1>Fichas técnicas e declarações nutricionais</h1><p class="sub">Technical sheets and nutrition declarations</p>
<div class="grid">{cols}</div>
<footer>© Vinha dos Padres, Lda. · <a href="/">vinhadospadres.com</a></footer>
</main></body></html>'''
open(S+'wineinfo.html','w').write(html)
print('missing sheets:',missing)
# PT wine pages: swap the EN sheet link for the PT one
import glob
for (y,col),(pt,en) in DRIVE.items():
    for f in glob.glob(S+f'qdvdp-*-{y}-{col}-pt.html'):
        h=open(f).read(); h2=h.replace(drive(en),drive(pt))
        if h2!=h: open(f,'w').write(h2)
