import re,json,sys,glob,html
SKIP=('script','style','svg')
def segments(h):
    # yields (start,end,text) of text nodes outside script/style/svg
    out=[];i=0;n=len(h)
    pat=re.compile(r'<(script|style|svg)\b.*?</\1>|<!--.*?-->|<[^>]+>',re.S)
    pos=0
    for m in pat.finditer(h):
        if m.start()>pos:
            t=h[pos:m.start()]
            if t.strip(): out.append((pos,m.start(),t))
        pos=m.end()
    return out
ATTR=re.compile(r'\b(alt|aria-label|placeholder|title|content|data-en)="([^"]*)"')
def strings(h):
    S=[]
    for a,b,t in segments(h):
        s=html.unescape(t.strip())
        if re.search('[A-Za-z]{2,}',s): S.append(s)
    for m in ATTR.finditer(h):
        name,v=m.groups()
        if name=='content':
            pre=h[max(0,m.start()-80):m.start()]
            if not re.search(r'name="description"|property="og:(title|description)"|name="twitter:(title|description)"',pre): continue
        v=html.unescape(v)
        if re.search('[A-Za-z]{3,}',v): S.append(v)
    return S
if __name__=='__main__':
    allS={}
    for f in sorted(glob.glob('/home/claude/vdp/s65/*.html')):
        h=open(f).read(); ss=strings(h)
        for s in ss: allS.setdefault(s,[]).append(f.split('/')[-1])
        print(f.split('/')[-1],len(set(ss)))
    print('unique',len(allS), 'chars',sum(len(s) for s in allS))
    json.dump(sorted(allS),open('/home/claude/vdp/strings_en.json','w'),ensure_ascii=False,indent=0)
