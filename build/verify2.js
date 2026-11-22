const fs=require('fs'); global.atob=s=>Buffer.from(s,'base64').toString('latin1');
eval(fs.readFileSync('terroir.orig.js','utf8').replace('const TERR_D','global.A'));
eval(fs.readFileSync('terroir.new.js','utf8').replace('const TERR_D','global.B'));
const zb=Buffer.from(A.zb64,'base64'); const za=new Int16Array(zb.buffer,zb.byteOffset,zb.length/2);
const eq=(x,y,p)=>{ if(Array.isArray(x)){ if(x.length!==y.length) throw p+' len'; x.forEach((v,i)=>eq(v,y[i],p+'['+i+']')); } else if(x!==y) throw p+' '+x+' vs '+y; };
for(const k of ['w','h','lon0','lat0','d','bbox','cells','outline','park','doc','btri','geol']) eq(A[k],B[k],k);
console.log('vectors bit-identical');
// every DEM sample that rendering can read
const T=A,W=T.w,used=new Set();
const el=(lon,lat)=>{let c=(lon-T.lon0)/T.d,r=(T.lat0-lat)/T.d;c=Math.min(Math.max(c,0),T.w-1.001);r=Math.min(Math.max(r,0),T.h-1.001);const c0=c|0,r0=r|0;[r0*W+c0,r0*W+c0+1,(r0+1)*W+c0,(r0+1)*W+c0+1].forEach(k=>used.add(k));};
const cb=Buffer.from(T.cells,'base64'),CW=W-1;
for(let r=0;r<T.h-1;r++)for(let c=0;c<CW;c++){const bit=r*CW+c;if(cb[bit>>3]&(128>>(bit&7)))[r*W+c,r*W+c+1,(r+1)*W+c,(r+1)*W+c+1].forEach(k=>used.add(k));}
for(let i=0;i<T.btri.length;i+=2) el(T.btri[i],T.btri[i+1]);
const dens=r=>{for(let i=0;i<r.length-1;i++){const a=r[i],b=r[i+1];for(let j=0;j<=50;j++)el(a[0]+(b[0]-a[0])*j/50,a[1]+(b[1]-a[1])*j/50);}};
[T.outline,T.park,T.doc,...T.geol].forEach(dens);
[[-7.3594,39.3131],[-7.42917,39.29537],[-7.39276,39.29817],[-7.3904,39.2921]].forEach(p=>el(...p));
let bad=0;for(const k of used) if(za[k]!==B.z[k]) bad++;
console.log('DEM samples used by 3D',used.size,'differences',bad);
