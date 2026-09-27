#!/usr/bin/env python3
"""EXPORTER VUE 3D — embed le champ |ψ(z,y)|² dans une page HTML autonome.

Rendu 3D en JavaScript PUR (Canvas 2D + algorithme du peintre) — pas de
Three.js, aucune dépendance externe, fonctionne hors ligne. Rotation à la
souris, zoom à la molette, couleur = phase du champ (identité du labo).

Usage : python3 outils/exporter_vue3d.py   → visualisation.html
"""
from __future__ import annotations

import base64
import pathlib

import numpy as np

RACINE = pathlib.Path(__file__).resolve().parent.parent

pile = np.load(RACINE / "champs" / "pile_reference.npy").astype(np.complex64)
zs = np.load(RACINE / "champs" / "pile_reference_z.npy")

# decimation : 1 point sur 2 en z (47 -> 24 plans), 1 sur 2 en y (320 -> 160)
pile = pile[::2, ::2]
amp = np.abs(pile)
amp = (amp / amp.max() * 255).astype(np.uint8)
phase = ((np.angle(pile) + np.pi) / (2 * np.pi) * 255).astype(np.uint8)

b_amp = base64.b64encode(amp.tobytes()).decode()
b_ph = base64.b64encode(phase.tobytes()).decode()
NZ, NY = amp.shape

HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>RATISS-PHOTON — le couloir du photon en 3D (JS pur)</title>
<style>
  html,body{margin:0;height:100%;background:#060813;color:#e2e8f0;font-family:Georgia,serif;overflow:hidden}
  #ui{position:fixed;top:10px;left:14px;z-index:5;background:rgba(6,8,19,.82);border:1px solid #1e2a45;
      border-radius:10px;padding:10px 14px;max-width:430px}
  h1{font-size:15px;margin:0 0 4px;color:#99f6e4;letter-spacing:.5px}
  p{margin:2px 0;font-size:11.5px;color:#8ba3c7;line-height:1.45}
  b{color:#e2e8f0}
  .aide{color:#5b6b8c;font-size:10.5px;margin-top:6px}
  canvas{display:block}
  input[type=range]{accent-color:#2dd4bf;width:150px}
</style>
</head>
<body>
<div id="ui">
  <h1>🧮 RATISS-PHOTON — le couloir du photon (JS pur, zéro dépendance)</h1>
  <p><b>Hauteur</b> = |ψ(z,y)|² — la densité de présence du photon unique.<br>
     <b>Couleur</b> = phase de ψ : cyan → turquoise → blanc (un tour complet = 2π).<br>
     Deux fentes à z = 360 : la lumière emprunte tous les chemins, et ça se voit.</p>
  <p><b>Rotation :</b> glisser la souris · <b>Zoom :</b> molette ·
     <label>Relief <input id="relief" type="range" min="0" max="300" value="120"></label>
     <label><input id="auto" type="checkbox" checked> rotation auto</label></p>
  <p class="aide">Étiquette de terrain : 🧮 calcul — monde simulé RATISS, aucun photon matériel blessé. 😉</p>
</div>
<canvas id="c"></canvas>
<script>
const NZ=__NZ__, NY=__NY__, DZ=__DZ__, DY=1.0;
const amp=Uint8Array.from(atob("__AMP__"),c=>c.charCodeAt(0));
const pha=Uint8Array.from(atob("__PHASE__"),c=>c.charCodeAt(0));
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W,H;function rs(){W=cv.width=innerWidth;H=cv.height=innerHeight;}rs();onresize=rs;
let yaw=-0.5,pitch=0.42,zoom=1.0,drag=false,lx=0,ly=0;
cv.onmousedown=e=>{drag=true;lx=e.clientX;ly=e.clientY;};
onmouseup=()=>drag=false;
onmousemove=e=>{if(!drag)return;yaw+=(e.clientX-lx)*0.008;pitch+=(e.clientY-ly)*0.006;
  pitch=Math.max(-0.1,Math.min(1.25,pitch));lx=e.clientX;ly=e.clientY;};
onwheel=e=>{e.preventDefault();zoom*=e.deltaY<0?1.12:0.89;zoom=Math.max(0.3,Math.min(6,zoom));};
// palette de phase (identite labo : cyan -> turquoise -> blanc)
function coul(t){const s=Math.PI*2*t;
  const r=40+90*Math.max(0,Math.sin(s))**2+120*t*t;
  const g=150+90*Math.sin(s*0.5+1);
  const b=140+90*Math.cos(s*0.7);
  return [Math.min(255,r),Math.min(255,Math.max(90,g)),Math.min(255,Math.max(160,b))];}
const PAL=[];for(let i=0;i<256;i++)PAL.push(coul(i/255));
const A=[],P=[];for(let i=0;i<NZ;i++){A.push(Array.from(amp.slice(i*NY,(i+1)*NY)));
                                 P.push(Array.from(pha.slice(i*NY,(i+1)*NY)));}
function proj(x,y,z){
  const cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
  let X=x*cy-z*sy, Z=x*sy+z*cy, Y=y;
  let Y2=Y*cp-Z*sp, Z2=Y*sp+Z*cp;
  const f=H*0.55*zoom;
  return [W/2+X*f, H*0.62-Y2*f, Z2];
}
function dessiner(){
  ctx.fillStyle='#060813';ctx.fillRect(0,0,W,H);
  const relief=+document.getElementById('relief').value/100;
  const hmax=140*relief;
  const quads=[];
  for(let i=0;i<NZ-1;i++){
    const z0=i*DZ, z1=(i+1)*DZ;
    for(let j=0;j<NY-1;j++){
      const y0=(j-NY/2)*DY, y1=(j+1-NY/2)*DY;
      const a00=A[i][j]/255, a10=A[i+1][j]/255, a01=A[i][j+1]/255, a11=A[i+1][j+1]/255;
      const lum=(a00+a10+a01+a11)/4;
      if(lum<0.012)continue;
      const p00=proj(z0-NZ*DZ/2,y0,a00*hmax), p10=proj(z1-NZ*DZ/2,y0,a10*hmax),
            p01=proj(z0-NZ*DZ/2,y1,a01*hmax), p11=proj(z1-NZ*DZ/2,y1,a11*hmax);
      const depth=(p00[2]+p10[2]+p01[2]+p11[2])/4;
      const pi=Math.round((P[i][j]+P[i+1][j]+P[i][j+1]+P[i+1][j+1])/4);
      quads.push([depth,p00,p10,p11,p01,pi,lum]);
    }
  }
  quads.sort((u,v)=>v[0]-u[0]);
  for(const q of quads){
    const c=PAL[q[5]], l=0.35+0.65*q[6];
    ctx.fillStyle=`rgb(${c[0]*l|0},${c[1]*l|0},${c[2]*l|0})`;
    ctx.beginPath();
    ctx.moveTo(q[1][0],q[1][1]);ctx.lineTo(q[2][0],q[2][1]);
    ctx.lineTo(q[3][0],q[3][1]);ctx.lineTo(q[4][0],q[4][1]);
    ctx.closePath();ctx.fill();
  }
  // fentes + ecran
  ctx.font='11px Georgia';
  for(const [z,nom,c] of [[360,'fentes','#f1f5f9'],[640,'plaque','#fbbf24'],[920,'écran','#4ade80']]){
    const p=proj(z-NZ*DZ/2,-NY/2,0), p2=proj(z-NZ*DZ/2,NY/2,0);
    if((p[1]-p2[1])*(p[1]-p2[1])<1e9){
      ctx.strokeStyle=c;ctx.lineWidth=1;ctx.globalAlpha=0.6;
      ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(p2[0],p2[1]);ctx.stroke();ctx.globalAlpha=1;
      ctx.fillStyle=c;ctx.fillText(nom,p[0]+4,Math.max(p[1],p2[1])+14);
    }
  }
}
let t=0;
function boucle(){
  if(document.getElementById('auto').checked&&!drag){t+=0.003;yaw=Math.sin(t)*0.7-0.2;}
  dessiner();requestAnimationFrame(boucle);
}
boucle();
</script>
</body>
</html>
"""

html = (HTML.replace("__NZ__", str(NZ)).replace("__NY__", str(NY))
            .replace("__DZ__", str(float(zs[1] - zs[0]) * 2))
            .replace("__AMP__", b_amp).replace("__PHASE__", b_ph))
(RACINE / "visualisation.html").write_text(html, encoding="utf-8")
print(f"visualisation.html écrit ({(RACINE / 'visualisation.html').stat().st_size // 1024} Ko) — "
      f"{NZ} plans × {NY} points, JS pur, zéro dépendance.")
