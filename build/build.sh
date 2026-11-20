set -e
cd /home/claude/vdp
python3 mkpt.py 2>/dev/null | tail -3
python3 ptjs.py >/dev/null
python3 mkindexpt.py >/dev/null
python3 urls.py >/dev/null
python3 ldpt.py >/dev/null
python3 mkwineinfo.py >/dev/null
python3 legal.py >/dev/null
python3 urls.py >/dev/null
python3 - <<'PY'
import glob
for f in glob.glob('/home/claude/vdp/s65/*.html'):
    h=open(f).read()
    a='Only news about our wines, a few times a year. Unsubscribe any time.</small>'
    b='Só notícias sobre os nossos vinhos, algumas vezes por ano. Pode cancelar a qualquer momento.</small>'
    h=h.replace(a,a[:-8]+' <a href="privacy.html" style="color:inherit">Privacy policy</a></small>').replace(b,b[:-8]+' <a href="privacy-pt.html" style="color:inherit">Política de privacidade</a></small>')
    open(f,'w').write(h)
PY
echo built
