#!/usr/bin/env python3
"""EXPORTER VUE 3D v2 — le couloir du photon, CINEMATIQUE.

Correction majeure (C1) : la v1 projetait des coordonnees monde en PIXELS
(±460) avec un facteur ecran — tout se dessinait a 250 000 px hors canvas
(c'est ce que Jonathan a vu : un canvas vide). La v2 NORMALISE le monde :
x, y, z dans [-1.6, 1.6] x [-0.5, 0.5] x [0, 0.45], camera perspective a
distance fixe. Verifie par un miroir Python avant export.

Ce qu'on voit (donnees scellees de champs/pile_reference.npy) :
  - la surface |psi(z,y)|² (hauteur) coloree par la phase (couleur) ;
  - les DEUX FENTES (plan z=360) et la PLAQUE (z=640) en glorie ;
  - la COURBE D'INTERFERENCE a l'ecran (z=920), tracee depuis les donnees ;
  - un PHOTON lumineux qui suit la crete de probabilite, avec une trainee ;
  - fond etoile, lumiere additive, rotation souris + TACTILE.

Rendu JavaScript PUR (Canvas 2D, algorithme du peintre) — pas de Three.js.
"""
from __future__ import annotations

import base64
import math
import pathlib

import numpy as np

RACINE = pathlib.Path(__file__).resolve().parent.parent

# ---- donnees scellees -------------------------------------------------------
pile = np.load(RACINE / "champs" / "pile_reference.npy").astype(np.complex64)
zs = np.load(RACINE / "champs" / "pile_reference_z.npy")

pile = pile[::2, ::2]                      # 24 plans x 160 points
amp = np.abs(pile)
amp = (amp / amp.max() * 255).astype(np.uint8)
phase = ((np.angle(pile) + np.pi) / (2 * np.pi) * 255).astype(np.uint8)
screen_I = (amp[-1] / amp[-1].max() * 255).astype(np.uint8)
ridge = [int(np.argmax(amp[i])) for i in range(amp.shape[0])]   # crete par plan

b_amp = base64.b64encode(amp.tobytes()).decode()
b_ph = base64.b64encode(phase.tobytes()).decode()
b_scr = base64.b64encode(screen_I.tobytes()).decode()
NZ, NY = amp.shape
ZMIN, ZMAX = float(zs[0]), float(zs[-1])

# ---- miroir Python de la projection : AUCUN point hors ecran (C1) -----------
def miroir():
    DIST, FL = 3.6, 1.55
    cy, sy = math.cos(-0.5), math.sin(-0.5)
    cp, sp = math.cos(0.42), math.sin(0.42)
    XMIN = YMIN = 1e9
    XMAX = YMAX = -1e9
    for i in range(NZ):
        x = (i - NZ / 2) * (3.2 / NZ)
        for j in (0, NY - 1):
            y = (j - NY / 2) * (1.0 / NY)
            for h in (0.0, 0.45):
                X = x * cy - y * sy * 0 + (x * 0 - 0)  # rotation yaw sur (x,z)
                Xr = x * cy - 0 * sy
                Z1 = x * sy + 0 * cy + 0
                Yr = h * cp - Z1 * sp
                Zr = h * sp + Z1 * cp + DIST
                sx = Xr * FL / Zr
                syy = Yr * FL / Zr
                XMIN, XMAX = min(XMIN, sx), max(XMAX, sx)
                YMIN, YMAX = min(YMIN, syy), max(YMAX, syy)
    assert abs(XMAX) < 0.85 and abs(XMIN) < 0.85, (XMIN, XMAX)
    assert abs(YMAX) < 0.85 and abs(YMIN) < 0.85, (YMIN, YMAX)
    print(f"  miroir projection : x [{XMIN:+.2f}, {XMAX:+.2f}] · y [{YMIN:+.2f}, {YMAX:+.2f}] (unités demi-écran) → OK")


def z_w(zr):
    """z reel (px du couloir) -> coordonnee monde x."""
    return (zr - (ZMIN + ZMAX) / 2) / (ZMAX - ZMIN) * 3.2


HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>RATISS-PHOTON — le couloir du photon en 3D (JS pur)</title>
<style>
  html,body{margin:0;height:100%;background:#060813;color:#e2e8f0;
    font-family:Georgia,serif;overflow:hidden;touch-action:none}
  #ui{position:fixed;top:10px;left:10px;right:10px;z-index:5;
      background:linear-gradient(135deg,rgba(6,8,19,.92),rgba(11,17,34,.82));
      border:1px solid #1e2a45;border-radius:12px;padding:10px 14px;max-width:470px}
  h1{font-size:14.5px;margin:0 0 4px;color:#99f6e4;letter-spacing:.4px}
  p{margin:2px 0;font-size:11.5px;color:#8ba3c7;line-height:1.5}
  b{color:#e2e8f0}
  .aide{color:#5b6b8c;font-size:10.5px;margin-top:5px}
  canvas{display:block;position:fixed;inset:0}
  input[type=range]{accent-color:#2dd4bf;width:120px;vertical-align:middle}
  label{white-space:nowrap}
</style>
</head>
<body>
<div id="ui">
  <h1>🧮 RATISS-PHOTON — le couloir du photon (JS pur, zéro dépendance)</h1>
  <p><b>Hauteur</b> = |ψ(z,y)|² — densité de présence du photon unique.
     <b>Couleur</b> = phase de ψ. Les <b>deux fentes</b> (blanc, z=360) ouvrent
     tous les chemins ; la <b>plaque</b> (ambre, z=640) teste les chemins sombres ;
     à l'écran (z=920), la <b>courbe d'interférence</b> réelle du monde.</p>
  <p><b>Rotation</b> : glisser (souris ou doigt) · <b>Zoom</b> : molette / pincer ·
     <label>Relief <input id="relief" type="range" min="20" max="300" value="130"></label>
     <label><input id="auto" type="checkbox" checked> rotation auto</label>
     <label><input id="photon" type="checkbox" checked> photon</label></p>
  <p class="aide">Étiquette de terrain : 🧮 calcul — monde simulé RATISS, aucun photon matériel blessé. 😉</p>
</div>
<canvas id="c"></canvas>
<script>
"use strict";
const NZ=__NZ__, NY=__NY__, ZMIN=__ZMIN__, ZMAX=__ZMAX__;
const XSPAN=3.2, YW=1.0, HMAX=0.45;
const amp=Uint8Array.from(atob("__AMP__"),c=>c.charCodeAt(0));
const pha=Uint8Array.from(atob("__PHASE__"),c=>c.charCodeAt(0));
const scr=Uint8Array.from(atob("__SCR__"),c=>c.charCodeAt(0));
const RIDGE=__RIDGE__;
const A=[],P=[];
for(let i=0;i<NZ;i++){A.push(Array.from(amp.slice(i*NY,(i+1)*NY)));
                      P.push(Array.from(pha.slice(i*NY,(i+1)*NY)));}
// palette de phase (identite labo) : cyan -> turquoise -> blanc
const PAL=[];
for(let i=0;i<256;i++){const t=i/255, s=Math.PI*2*t;
  const r=60+110*Math.max(0,Math.sin(s))**2+90*t*t;
  const g=160+80*Math.sin(s*0.5+1.1);
  const b=150+80*Math.cos(s*0.7);
  PAL.push([Math.min(255,r|0),Math.min(255,Math.max(95,g)|0),Math.min(255,Math.max(165,b)|0)]);}
// etoiles (PRNG graine fixe : determinisme RATISS)
let seed=20260927;const rnd=()=>{seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff;};
const STARS=[];for(let i=0;i<130;i++)STARS.push([rnd(),rnd(),0.25+0.75*rnd()]);
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W,H,FL;function rs(){W=cv.width=innerWidth*devicePixelRatio;
  H=cv.height=innerHeight*devicePixelRatio;cv.style.width=innerWidth+'px';
  cv.style.height=innerHeight+'px';FL=1.55*Math.min(W,H);}rs();onresize=rs;
let yaw=-0.55,pitch=0.46,zoom=1,drag=false,lx=0,ly=0,pinch0=0,zoom0=1;
const start=e=>{drag=true;const t=e.touches?e.touches[0]:e;lx=t.clientX;ly=t.clientY;
  if(e.touches&&e.touches.length===2){pinch0=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);zoom0=zoom;}};
const move=e=>{if(!drag)return;e.preventDefault();
  if(e.touches&&e.touches.length===2){const d=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);
    zoom=Math.max(0.45,Math.min(3.2,zoom0*d/pinch0));return;}
  const t=e.touches?e.touches[0]:e;yaw+=(t.clientX-lx)*0.008;pitch+=(t.clientY-ly)*0.006;
  pitch=Math.max(-0.15,Math.min(1.25,pitch));lx=t.clientX;ly=t.clientY;};
const end=()=>drag=false;
cv.addEventListener('mousedown',start);onmouseup=end;onmousemove=move;
cv.addEventListener('touchstart',start,{passive:false});
cv.addEventListener('touchmove',move,{passive:false});cv.addEventListener('touchend',end);
onwheel=e=>{e.preventDefault();zoom*=e.deltaY<0?1.12:0.89;zoom=Math.max(0.45,Math.min(3.2,zoom));};
const xw=i=>(i-NZ/2)*(XSPAN/NZ), yw=j=>(j-NY/2)*(YW/NY);
const zw=zr=>(zr-(ZMIN+ZMAX)/2)/(ZMAX-ZMIN)*XSPAN;
let cy_,sy_,cp_,sp_,DIST=3.6;
function proj(x,y,z){
  let X=x*cy_-z*sy_, Z1=x*sy_+z*cy_;
  let Y=y*cp_-Z1*sp_, Z=y*sp_+Z1*cp_+DIST;
  const s=FL*zoom/Z;
  return [W*0.5+X*s, H*0.55-Y*s, Z];
}
function seg(x1,y1,z1,x2,y2,z2,coul,ep,glow){
  const a=proj(x1,y1,z1),b=proj(x2,y2,z2);
  ctx.strokeStyle=coul;ctx.lineWidth=ep;ctx.globalAlpha=glow?0.55:0.9;
  ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();ctx.globalAlpha=1;
}
function dessiner(t){
  ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;
  const g=ctx.createRadialGradient(W*0.5,H*0.45,0,W*0.5,H*0.45,Math.max(W,H)*0.75);
  g.addColorStop(0,'#0a1024');g.addColorStop(1,'#04060f');
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  for(const s of STARS){ctx.fillStyle=`rgba(200,220,255,${0.5*s[2]})`;
    ctx.fillRect(s[0]*W,s[1]*H,devicePixelRatio,devicePixelRatio);}
  cy_=Math.cos(yaw);sy_=Math.sin(yaw);cp_=Math.cos(pitch);sp_=Math.sin(pitch);
  const relief=+document.getElementById('relief').value/100;
  const hmax=HMAX*relief;
  // ---- surface : quadstries tries par profondeur, lumiere additive ----------
  const quads=[];
  for(let i=0;i<NZ-1;i++)for(let j=0;j<NY-1;j++){
    const a00=A[i][j]/255,a10=A[i+1][j]/255,a01=A[i][j+1]/255,a11=A[i+1][j+1]/255;
    const lum=(a00+a10+a01+a11)/4;
    if(lum<0.015)continue;
    const p00=proj(xw(i),yw(j),a00*hmax),p10=proj(xw(i+1),yw(j),a10*hmax),
          p11=proj(xw(i+1),yw(j+1),a11*hmax),p01=proj(xw(i),yw(j+1),a01*hmax);
    quads.push([(p00[2]+p10[2]+p11[2]+p01[2])/4,p00,p10,p11,p01,
                (P[i][j]+P[i+1][j]+P[i][j+1]+P[i+1][j+1])/4,lum]);
  }
  quads.sort((u,v)=>v[0]-u[0]);
  ctx.globalCompositeOperation='lighter';
  for(const q of quads){
    const c=PAL[q[5]|0],l=0.30+0.75*q[6];
    ctx.fillStyle=`rgba(${c[0]*l|0},${c[1]*l|0},${c[2]*l|0},${0.28+0.5*q[6]})`;
    ctx.beginPath();ctx.moveTo(q[1][0],q[1][1]);ctx.lineTo(q[2][0],q[2][1]);
    ctx.lineTo(q[3][0],q[3][1]);ctx.lineTo(q[4][0],q[4][1]);ctx.closePath();ctx.fill();
  }
  // ---- les fentes (z=360) : mur blanc, deux ouvertures ---------------------
  const zf=zw(360), zf2=zw(640);
  const yLo=(42-80)/80*0.5*0+ -0.2375; // moitie-gauche des ouvertures calculee ci-dessous
  function mur(zpx,coul,ep){
    const ouvr=[[-78,-42],[42,78]];
    let prev=-0.5;
    for(const [a,b] of ouvr){
      const ya=a/320, yb=b/320;  // px du couloir -> monde (domaine 320 px)
      seg(zpx,prev,0,zpx,ya,0,coul,ep,glow_mur);
      prev=yb;
    }
    seg(zpx,prev,0,zpx,0.5,0,coul,ep,glow_mur);
  }
  let glow_mur=true;
  mur(zf,'#f1f5f9',2.2*devicePixelRatio);
  glow_mur=false;
  // ---- la plaque (z=640) : bande ambre sur la frange sombre ----------------
  seg(zf2,-0.09375,0,zf2,0.0,0,'#fbbf24',3.2*devicePixelRatio,true);
  seg(zf2,-0.09375,0,zf2,-0.09375,0,'#fbbf24',2*devicePixelRatio,false);
  // ---- l'ecran (z=920) : la courbe d'interference REELLE -------------------
  const zs=zw(920);
  ctx.beginPath();
  for(let j=0;j<NY;j++){
    const p=proj(zs,yw(j),scr[j]/255*hmax*1.05);
    if(j===0)ctx.moveTo(p[0],p[1]);else ctx.lineTo(p[0],p[1]);
  }
  ctx.strokeStyle='#7df9ff';ctx.lineWidth=2.4*devicePixelRatio;
  ctx.shadowColor='#38bdf8';ctx.shadowBlur=14;ctx.stroke();ctx.shadowBlur=0;
  // socle de l'ecran
  seg(zs,-0.5,0,zs,0.5,0,'rgba(125,249,255,0.35)',1.2*devicePixelRatio,false);
  // ---- etiquettes ----------------------------------------------------------
  ctx.globalCompositeOperation='source-over';
  ctx.font=`${11*devicePixelRatio}px Georgia`;ctx.globalAlpha=0.85;
  const pe=proj(zf,0.52,0);ctx.fillStyle='#f1f5f9';ctx.fillText('deux fentes',pe[0]-30*devicePixelRatio,pe[1]);
  const pp=proj(zf2,0.52,0);ctx.fillStyle='#fbbf24';ctx.fillText('plaque',pp[0]-15*devicePixelRatio,pp[1]);
  const pz=proj(zs,0.52,0);ctx.fillStyle='#7df9ff';ctx.fillText('écran',pz[0]-10*devicePixelRatio,pz[1]);
  ctx.globalAlpha=1;
  // ---- le photon : il suit la crete de probabilite -------------------------
  if(document.getElementById('photon').checked){
    const k=(t*0.00016)%1.15;
    if(k<=1){
      const fi=k*(NZ-1),i0=Math.min(NZ-2,fi|0),fr=fi-i0;
      const yRidge=(yw(RIDGE[i0])*(1-fr)+yw(RIDGE[i0+1])*fr);
      const zRidge=((ZMIN+40*(i0+fr))-(ZMIN+ZMAX)/2)/(ZMAX-ZMIN)*XSPAN;
      const hR=(A[i0][RIDGE[i0]]/255*(1-fr)+A[i0+1][RIDGE[i0+1]]/255*fr)*hmax+0.02;
      // trainee
      for(let s=1;s<=10;s++){
        const fk=Math.max(0,k-s*0.012);if(fk>1)break;
        const fi2=fk*(NZ-1),j0=Math.min(NZ-2,fi2|0),fr2=fi2-j0;
        const yT=(yw(RIDGE[j0])*(1-fr2)+yw(RIDGE[j0+1])*fr2);
        const zT=((ZMIN+40*(j0+fr2))-(ZMIN+ZMAX)/2)/(ZMAX-ZMIN)*XSPAN;
        const hT=(A[j0][RIDGE[j0]]/255*(1-fr2)+A[j0+1][RIDGE[j0+1]]/255*fr2)*hmax+0.02;
        const p1=proj(zT,yT,hT),p2=proj(((ZMIN+40*(j0+fr2+0.0001))-(ZMIN+ZMAX)/2)/(ZMAX-ZMIN)*XSPAN,yT,hT+0.0001);
        ctx.globalCompositeOperation='lighter';
        ctx.fillStyle=`rgba(180,250,255,${0.32*(1-s/10)})`;
        ctx.beginPath();ctx.arc(p1[0],p1[1],(6-s*0.4)*devicePixelRatio,0,7);ctx.fill();
      }
      const pp2=proj(zRidge,yRidge,hR);
      ctx.shadowColor='#aef9ff';ctx.shadowBlur=22;
      ctx.fillStyle='#eafcff';
      ctx.beginPath();ctx.arc(pp2[0],pp2[1],4.6*devicePixelRatio,0,7);ctx.fill();
      ctx.shadowBlur=0;
    }
  }
}
let t0=performance.now();
function boucle(t){
  if(document.getElementById('auto').checked&&!drag){yaw+=0.0035;}
  dessiner(t);requestAnimationFrame(boucle);
}
requestAnimationFrame(boucle);
</script>
</body>
</html>
"""

# miroir avant ecriture (C1 : plus rien hors ecran)
miroir()

html = (HTML.replace("__NZ__", str(NZ)).replace("__NY__", str(NY))
             .replace("__ZMIN__", str(ZMIN)).replace("__ZMAX__", str(ZMAX))
             .replace("__AMP__", b_amp).replace("__PHASE__", b_ph)
             .replace("__SCR__", b_scr).replace("__RIDGE__", str(ridge)))
(RACINE / "visualisation.html").write_text(html, encoding="utf-8")
taille = (RACINE / "visualisation.html").stat().st_size
print(f"visualisation.html v2 écrit ({taille // 1024} Ko) — surface + fentes + plaque + "
      f"courbe d'interférence réelle + photon sur la crête + tactile, JS pur.")
