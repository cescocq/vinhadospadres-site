"""Adds the terroir layer (2D geology toggle + 3D block) to site/index.html and site/index-pt.html.
Run from repo root. Idempotent: skips a page that already has it."""
import re
SRC=open('/home/claude/vdp/s65/estate-terroir.html').read()
mod=SRC[SRC.find('/* ---------------- Terroir 3D'):SRC.find("const loader=document.getElementById('loader');")]
# 3D module: drop the old standalone button, remember where we came from
mod=mod.replace("function terrBtnSync(){ const b=document.getElementById('terrBtn'); if(!b) return; b.hidden=!(level==='pg'||level==='vdp')||inAxo; b.querySelector('span').textContent=t('terr3d'); }\n","")
mod=mod.replace("document.getElementById('terrBtn').onclick=()=>enterTerroir();\n","")
mod=mod.replace("let TERR=null, terrGo=null, TERRX=null;","var TERR=null, terrGo=null, TERRX=null, terrFrom='pg';").replace('const GEO_U=','var GEO_U=')
mod=mod.replace("  terrGo=null;\n","  terrGo=null; terrFrom=(level==='vdp')?'vdp':'pg';\n",1)
mod=mod.replace("crumbs(); terrBtnSync();","crumbs(); terrCtl();")
assert 'terrBtn' not in mod, 'terrBtn left'
layer=r"""
/* ---------------- Terroir 2D layer: geology on the map, on from the 10 km scale down ---------------- */
var terrOn=false, terrAvail=false, gGeo=null, geoPaths=null;
var GEO_COL=Object.fromEntries(GEO_U.map(u=>[u[0],u[1]]).concat([['urra','#F5D7D9'],['water','#8EC8EC']]));
async function terrSet(on){
  terrOn=!!on;
  if(terrOn && typeof GEO_D==='undefined'){ try{ await loadJS('data/geology.js'); }catch(e){ terrOn=false; } }
  if(terrOn && !gGeo){
    gGeo=d3.select('#map').insert('g','#g-reg').attr('id','g-geo').style('pointer-events','none');
    geoPaths=gGeo.selectAll('path').data(GEO_D).join('path').attr('class',d=>'geo geo-'+d.u)
      .attr('fill',d=>(d.u==='portalegre'||d.u==='nisa')?`url(#geo-${d.u})`:GEO_COL[d.u]||'#ddd');
  }
  if(gGeo) gGeo.style('display',terrOn?null:'none');
  render(); legend(); terrCtl();
}
function terrScale(best){ const av = best<=10000; if(av!==terrAvail){ terrAvail=av; if(!av && terrOn){ terrOn=false; if(gGeo) gGeo.style('display','none'); legend(); } terrCtl(); } }
function terrCtl(){
  const el=document.getElementById('terrCtl'); if(!el) return;
  el.hidden = !terrAvail || inAxo;
  el.querySelector('.tsw').setAttribute('aria-checked',String(terrOn));
  el.querySelector('.tsw span').textContent=t('terroir');
  el.querySelector('.v3d').textContent=t('terr3dv');
  el.classList.toggle('on',terrOn);
}
"""
CSS="""
#terrCtl{position:absolute;z-index:6;right:22px;bottom:calc(var(--sheet-h,0px) + 86px + env(safe-area-inset-bottom,0px));display:flex;align-items:center;gap:4px;padding:4px;border-radius:999px;background:var(--panel);border:1px solid var(--hair);box-shadow:0 2px 10px rgba(35,31,32,.08);font-family:var(--serif-i);font-style:italic}
#terrCtl[hidden]{display:none}body.axo-on #terrCtl{display:none}
#terrCtl button{font:inherit;font-size:16px;color:var(--ink);background:none;border:0;border-radius:999px;padding:7px 13px;cursor:pointer;display:flex;align-items:center;gap:8px}
#terrCtl .tsw i{position:relative;width:30px;height:17px;border-radius:999px;background:rgba(35,31,32,.18);transition:background .2s}
#terrCtl .tsw i::after{content:"";position:absolute;left:2px;top:2px;width:13px;height:13px;border-radius:50%;background:#fff;transition:transform .2s}
#terrCtl.on .tsw i{background:var(--gold,#C76653)}#terrCtl.on .tsw i::after{transform:translateX(13px)}
#terrCtl .v3d{border-left:1px solid var(--hair);border-radius:0 999px 999px 0;padding-left:12px}#terrCtl .v3d:hover,#terrCtl .tsw:hover{background:rgba(35,31,32,.05)}
#g-geo path{stroke:#231F20;stroke-opacity:.35;stroke-width:.6;fill-opacity:.62;vector-effect:non-scaling-stroke}
"""
PATTERNS='<pattern id="geo-portalegre" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#E289B7"/><path d="M7 4v6M4 7h6" stroke="#8E3E6E" stroke-width=".9" opacity=".55"/></pattern><pattern id="geo-nisa" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#F3A5A9"/><path d="M7 4v6M4 7h6" stroke="#B5546A" stroke-width=".9" opacity=".55"/></pattern>'
def patch(p):
    h=open(p).read()
    if 'id="terrCtl"' in h: print('skip',p); return
    def R(a,b,n=1):
        nonlocal h; assert h.count(a)==n,(p,h.count(a),a[:70]); h=h.replace(a,b)
    # CSS (3D bits from the prototype + 2D toggle)
    css3d=SRC[SRC.find('#terrLbl{position:absolute'):SRC.find('.tstats div{')]+SRC[SRC.find('.tstats div{'):SRC.find('\n',SRC.find('.tstats div{'))]
    i=h.find('</style>'); h=h[:i]+'\n'+css3d+CSS+h[i:]
    # svg patterns
    R('<pattern id="hatch-white"',PATTERNS+'<pattern id="hatch-white"')
    # DOM: toggle + 3D label layer
    R('<section id="axo" aria-hidden="true">\n    <canvas id="gl"></canvas>','<div id="terrCtl" hidden><button class="tsw" role="switch" aria-checked="false"><i aria-hidden="true"></i><span>Terroir</span></button><button class="v3d">3D view</button></div>\n  <section id="axo" aria-hidden="true">\n    <canvas id="gl"></canvas><div id="terrLbl"></div>')
    # strings
    en=SRC[SRC.find("terroir:'Terroir',terr3d:'Terroir in 3D'"):SRC.find("terrGrid:'5 km grid · heights ×{e}',")+len("terrGrid:'5 km grid · heights ×{e}',")]
    pt=SRC[SRC.find("terroir:'Terroir',terr3d:'Terroir em 3D'"):SRC.find("terrGrid:'grelha de 5 km · altura ×{e}',")+len("terrGrid:'grelha de 5 km · altura ×{e}',")]
    R("soldOut:'Sold out',","soldOut:'Sold out',"+en+"terr3dv:'3D view',geoLg:'Geology (indicative)',")
    R("soldOut:'Esgotado',","soldOut:'Esgotado',"+pt+"terr3dv:'Vista 3D',geoLg:'Geologia (indicativa)',")
    # outline click at Portalegre level opens the 3D terroir
    R("""p.on('mousemove',ev=>{ if(level==='al'||level==='pg') showTip(ev,`<h4>${t(key)}</h4><div class="sub">${t('clickZoom')}</div>`); })
   .on('mouseleave',hideTip).on('click',ev=>{ if(level==='al'||level==='pg') tapGate(key,ev,e=>showTip(e,`<h4>${t(key)}</h4><div class="sub">${t('clickZoom')}</div>`),()=>{ hideTip(); fly(fitK(g)); }); }); });""",
"""const sub=()=>level==='pg'?t('terrClick'):t('clickZoom');
  p.on('mousemove',ev=>{ if(level==='al'||level==='pg') showTip(ev,`<h4>${t(key)}</h4><div class="sub">${sub()}</div>`); })
   .on('mouseleave',hideTip).on('click',ev=>{ if(level==='al'||level==='pg') tapGate(key,ev,e=>showTip(e,`<h4>${t(key)}</h4><div class="sub">${sub()}</div>`),()=>{ hideTip(); if(level==='pg') enterTerroir(); else fly(fitK(g)); }); }); });""")
    # hooks
    R("if(el){ el.querySelector('.bar').style.width=px+'px';","terrScale(best);\n  if(el){ el.querySelector('.bar').style.width=px+'px';")
    R("docPath.attr('d',regO>0?path(F(R.doc)):null).style('opacity',regO);","docPath.attr('d',regO>0?path(F(R.doc)):null).style('opacity',regO);\n  if(terrOn&&geoPaths) geoPaths.attr('d',d=>path(F(d.g)));")
    R("controls.update(); renderer.render(scene,camera);","controls.update(); renderer.render(scene,camera); if(TERR) terrLabels();")
    R("""function exitAxo(to='vdp'){
  if(!inAxo) return;""","""function exitAxo(to='vdp'){
  if(!inAxo) return;
  if(TERR){ to=terrGo||terrFrom; terrGo=null; TERR=null; axo.classList.remove('terr'); document.getElementById('terrLbl').innerHTML=''; setTimeout(terrCtl,50); }""")
    R("if(inAxo && P3){ items.push({l:'prop',txt:P3.prop.name});","if(inAxo && TERR){ items.push({l:'terr',txt:t('terroir')}); }\n  if(inAxo && P3){ items.push({l:'prop',txt:P3.prop.name});")
    R("else b.onclick=()=>{ if(inAxo) exitAxo(it.l); else if(it.l==='prop') return;","else b.onclick=()=>{ if(inAxo){ terrGo=it.l; exitAxo(it.l); } else if(it.l==='prop') return;")
    R("if(inAxo){ if(P3&&P3.sel) select(null); else exitAxo('vdp'); }","if(inAxo){ if(P3&&P3.sel) select(null); else exitAxo(TERR?terrFrom:'vdp'); }")
    R('function axoUI(){\n  if(!P3) return;','function axoUI(){\n  if(TERR){ terrUI(); return; }\n  if(!P3) return;')
    # legend: geology entries when the layer is on
    R("  const sc=`<div id=\"scale\"><div class=\"bar\"></div><span></span></div>`;","  if(terrOn && typeof GEO_U!=='undefined'){ const pi=lang==='pt'?3:2; h+=`<div class=\"lg\" style=\"margin-top:4px\"><b>${t('geoLg')}</b></div>`+GEO_U.map(u=>`<div class=\"lg\"><span class=\"sw\" style=\"background:${u[1]};opacity:.8\"></span>${u[pi]}</div>`).join(''); }\n  const sc=`<div id=\"scale\"><div class=\"bar\"></div><span></span></div>`;")
    # module + bindings
    R("const loader=document.getElementById('loader');",mod+layer+"""document.querySelector('#terrCtl .tsw').onclick=()=>terrSet(!terrOn);
document.querySelector('#terrCtl .v3d').onclick=()=>enterTerroir();
const loader=document.getElementById('loader');""")
    open(p,'w').write(h); print('patched',p)
for p in ['site/index.html','site/index-pt.html']: patch(p)
