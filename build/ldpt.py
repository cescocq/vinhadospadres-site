import re,json,glob,sys,os
sys.path.insert(0,'/home/claude/vdp'); from pt import PT
SITE='https://www.vinhadospadres.com'
EXTRA={'Wine':'Vinho','Vintage':'Colheita','Colour':'Cor','Label code':'Código do rótulo','Alcohol':'Álcool','Bottles produced':'Garrafas produzidas','Appellation':'Denominação','White':'Branco','Red':'Tinto'}
SKIPK={'@type','@context','@id','name_en','author','brand'}
for f in glob.glob('/home/claude/vdp/s65/*-pt.html'):
    name=os.path.basename(f)[:-8]; h=open(f).read()
    def walk(o,key=''):
        if isinstance(o,dict): return {k:(v if k in SKIPK or k.startswith('@') else walk(v,k)) for k,v in o.items()}
        if isinstance(o,list): return [walk(v,key) for v in o]
        if isinstance(o,str) and key in ('name','text','description','value','headline','alternateName','category','acceptedAnswer'):
            if o in PT: return PT[o]
            if o in EXTRA: return EXTRA[o]
        if isinstance(o,str) and key in ('url','@id','item') and re.fullmatch(SITE+r'/[a-z0-9-]+',o) and not o.endswith('-pt'): return o+'-pt'
        return o
    def fix(m):
        d=json.loads(m.group(2)); d=walk(d)
        return m.group(1)+json.dumps(d,ensure_ascii=False)+'</script>'
    h=re.sub(r'(<script type="application/ld\+json">)(.*?)</script>',fix,h,flags=re.S)
    open(f,'w').write(h)
print('ld ok')
# pt number format on wine pages
for f in glob.glob('/home/claude/vdp/s65/qdvdp-*-pt.html'):
    h=open(f).read()
    def dd(m):
        v=re.sub(r'(\d),(\d{3})',r'\1\2',m.group(1)); v=re.sub(r'(\d)\.(\d)',r'\1,\2',v)
        return '<dd>'+v+'</dd>'
    h=re.sub(r'<dd>([^<]*\d[^<]*)</dd>',dd,h)
    open(f,'w').write(h)
