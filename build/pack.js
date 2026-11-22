const fs=require('fs');
eval(fs.readFileSync(process.argv[2],'utf8').replace('const TERR_D','global.TERR_D'));
const T=TERR_D;
// DEM
const zb=Buffer.from(T.zb64,'base64'); const z=new Int16Array(zb.buffer,zb.byteOffset,zb.length/2);
const mask=fs.readFileSync(__dirname+'/mask.bin'); const W=T.w, zz=new Int16Array(z);
const pred=(i)=>{ const r=(i/W)|0, c=i%W; if(r===0) return c>0?zz[i-1]:0; if(c===0) return zz[i-W]; return (zz[i-1]+zz[i-W])>>1; };
const out=[];
for(let i=0;i<zz.length;i++){ const p=pred(i); if(!mask[i]) zz[i]=p; const dd=zz[i]-p;
  if(dd>-128&&dd<128) out.push(dd&255); else { out.push(128); out.push(zz[i]&255,(zz[i]>>8)&255); } }
fs.writeFileSync(__dirname+'/zmasked.bin',Buffer.from(zz.buffer));
const zd=Buffer.from(out).toString('base64');
const q=v=>{const n=Math.round(v*1e6); if(n/1e6!==v) throw 'lossy '+v; return n;};
const ring=r=>{let a=0,b=0;const o=[];for(const [x,y] of r){const X=q(x),Y=q(y);o.push(X-a,Y-b);a=X;b=Y;}return o;};
const flat=f=>{let a=0,b=0;const o=[];for(let i=0;i<f.length;i+=2){const X=q(f[i]),Y=q(f[i+1]);o.push(X-a,Y-b);a=X;b=Y;}return o;};
const btriPack=f=>{const map=new Map(),U=[],I=[];for(let i=0;i<f.length;i+=2){const k=f[i]+','+f[i+1];if(!map.has(k)){map.set(k,U.length/2);U.push(q(f[i]),q(f[i+1]));}I.push(map.get(k));}
 let a=0,b=0;const ud=[];for(let i=0;i<U.length;i+=2){ud.push(U[i]-a,U[i+1]-b);a=U[i];b=U[i+1];} let p=0;return [ud,I.map(v=>{const d=v-p;p=v;return d})];};
const P={w:T.w,h:T.h,lon0:T.lon0,lat0:T.lat0,d:T.d,bbox:T.bbox,cells:T.cells,zd,
  outline:ring(T.outline),park:ring(T.park),doc:ring(T.doc),btri:btriPack(T.btri),geol:T.geol.map(ring)};
for(const k of Object.keys(T)) if(!(k in P)&&k!=='zb64') throw 'missing key '+k;
const dec=`const TERR_D=(function(P){
const b=atob(P.zd),n=P.w*P.h,z=new Int16Array(n);let j=0;
const W=P.w;for(let i=0;i<n;i++){const r=(i/W)|0,c0=i%W,p=r===0?(c0>0?z[i-1]:0):(c0===0?z[i-W]:(z[i-1]+z[i-W])>>1);let c=b.charCodeAt(j++);
 if(c===128){z[i]=(b.charCodeAt(j)|(b.charCodeAt(j+1)<<8))<<16>>16;j+=2;}else z[i]=p+(c<<24>>24);}
const ring=a=>{const o=[];let x=0,y=0;for(let i=0;i<a.length;i+=2){x+=a[i];y+=a[i+1];o.push([x/1e6,y/1e6]);}return o;};
return {w:P.w,h:P.h,lon0:P.lon0,lat0:P.lat0,d:P.d,bbox:P.bbox,cells:P.cells,z,
 outline:ring(P.outline),park:ring(P.park),doc:ring(P.doc),btri:(function(u,ix){const U=[];let x=0,y=0;for(let i=0;i<u.length;i+=2){x+=u[i];y+=u[i+1];U.push(x/1e6,y/1e6);}const o=new Array(ix.length*2);let p=0;for(let i=0;i<ix.length;i++){p+=ix[i];o[2*i]=U[2*p];o[2*i+1]=U[2*p+1];}return o;})(P.btri[0],P.btri[1]),geol:P.geol.map(ring)};
})(${JSON.stringify(P)});
`;
fs.writeFileSync(process.argv[3],dec);
