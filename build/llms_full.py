"""Build site/llms-full.txt: plain-text content of every English page, for AI assistants.
Run from repo root after editing pages: python3 build/llms_full.py"""
import re, html
B='https://www.vinhadospadres.com/'
PAGES=['history','amphora-wine','code','wines','qdvdp-3m12m-2022-red','qdvdp-3m12m-2022-white','qdvdp-3m3m-2023-white','qdvdp-3m3m4m-2023-red','recognition','contact']
def text(f):
    s=open(f'site/{f}.html',encoding='utf-8').read()
    i=s.find('<main class='); s=s[i:s.index('</main>',i)] if i>=0 else s
    s=s.replace('</a><span>','</a> — <span>')
    s=re.sub(r'<(script|style|svg|noscript|button|figure)\b.*?</\1>','',s,flags=re.S)
    s=re.sub(r'<h1[^>]*>','\n\n# ',s); s=re.sub(r'<h2[^>]*>','\n\n## ',s); s=re.sub(r'<h3[^>]*>','\n\n### ',s)
    s=re.sub(r'<summary[^>]*>','\n\n**',s); s=re.sub(r'</summary>','**\n',s)
    s=re.sub(r'<li[^>]*>','\n- ',s); s=re.sub(r'<(p|div|section|br|tr)[^>]*>','\n',s)
    s=html.unescape(re.sub(r'<[^>]+>','',s))
    s=re.sub(r'[ \t]+',' ',s); s=re.sub(r'\n\s*\n\s*\n+','\n\n',s)
    return '\n'.join(l.strip() for l in s.splitlines() if not (len(l.strip())>15 and ' ' not in l.strip())).strip()
intro=open('site/llms.txt',encoding='utf-8').read().split('\n## ')[0].strip()
ptnote='A Portuguese version is coming soon.' if 'coming soon' in intro else 'Portuguese versions add the suffix `-pt` to each address.'
out=[intro,'\nThis file contains the full text of the English pages. '+ptnote+'\n']
for p in PAGES:
    out.append(f'\n---\n\nSource: {B}{p if p!="index" else ""}\n\n'+text(p))
open('site/llms-full.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
print('llms-full.txt', sum(len(x) for x in out),'chars')
