import re,os,glob,base64,hashlib,json
S='/home/claude/vdp/s64/'
os.chdir(S)
for d in ('fonts','img/bottles','data'): os.makedirs(d,exist_ok=True)
FONTNAME={}
def font_file(b64,weight):
    k=hashlib.md5(b64.encode()).hexdigest()[:8]
    if k not in FONTNAME:
        name=f'fonts/arno-pro-italic-{"bold" if weight.startswith("6") else "regular"}.woff2'
        open(name,'wb').write(base64.b64decode(b64)); FONTNAME[k]=name
    return FONTNAME[k]
IMG={}
def img_file(kind,b64):
    k=hashlib.md5(b64.encode()).hexdigest()[:10]
    if k not in IMG:
        name=f'img/bottles/{k}.{ "webp" if kind=="webp" else kind.split("+")[0]}'
        open(name,'wb').write(base64.b64decode(b64)); IMG[k]=name
    return IMG[k]
for f in sorted(glob.glob('*.html')):
    h=open(f).read(); n0=len(h)
    # fonts
    def ff(m):
        weight=m.group(1); path=font_file(m.group(2),weight)
        return f"@font-face{{font-family:'Arno Pro';font-style:italic;font-weight:{weight};font-display:swap;src:url({path}) format('woff2')}}"
    h=re.sub(r"@font-face\{font-family:'Arno Pro';font-style:italic;font-weight:([0-9 ]+);font-display:swap;src:url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)[^}]*\}",ff,h)
    # dedupe identical font-face blocks
    seen=set()
    def dd(m):
        if m.group(0) in seen: return ''
        seen.add(m.group(0)); return m.group(0)
    h=re.sub(r"@font-face\{font-family:'Arno Pro'[^}]*src:url\(fonts/[^}]*\}",dd,h)
    if 'rel="preload" href="fonts/' not in h:
        pre=''.join(f'<link rel="preload" href="{p}" as="font" type="font/woff2" crossorigin>' for p in sorted(set(re.findall(r'url\((fonts/[^)]+)\)',h))))
        h=h.replace('</title>','</title>'+pre,1)
    # images
    h=re.sub(r'data:image/(webp|png|jpeg);base64,([A-Za-z0-9+/=]{3000,})',lambda m:img_file(m.group(1),m.group(2)),h)
    # lazy-load non-critical imgs
    h=re.sub(r'<img (?![^>]*loading=)(?=[^>]*src="img/)',r'<img loading="lazy" ',h)
    open(f,'w').write(h); print(f,n0,'->',len(h))
# big data blocks to cached js files
def extract(f,start,out):
    h=open(f).read(); i=h.find(start)
    if i<0: return
    j=i+len(start); obj,end=json.JSONDecoder().raw_decode(h[j:])
    js=start+json.dumps(obj,separators=(',',':'),ensure_ascii=False)+';\n'
    open(out,'w').write(js)
    stop=j+end+(1 if h[j+end]==';' else 0)
    # close current script, load data file, reopen
    h=h[:i]+f'</script><script src="{out}"></script><script>'+h[stop:]
    open(f,'w').write(h); print('extracted',f,out,len(js))
extract('index.html','const D = ','data/estate.js')
extract('history.html','const G=','data/history-geo.js')
for f in ['index.html','history.html']:
    h=open(f).read(); h=re.sub(r'<script>\s*</script>','',h); open(f,'w').write(h)
print(FONTNAME,len(IMG))
