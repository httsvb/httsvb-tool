// ==UserScript==
// @name         Ultimate Speed & Auto Click (V11.0 Anti-CSP)
// @namespace    http://tampermonkey.net/
// @version      11.0
// @description  V11.0: Fix lỗi UI 100% bằng Inline Styles (Bất chấp CSP).
// @author       httsvb
// @match        *://*/*
// @run-at       document-start
// @grant        none
// ==/UserScript==

(function(){'use strict';
const K="GM_ULT_V11",U="cyb-ui",M="cyb-min",O="pick-ov";
function _Run(){
const w=window,d=document,l=localStorage;
const _css=`html,body{scroll-behavior:auto!important;transition:none!important}`;
const _s=d.createElement('style');_s.innerHTML=_css;(d.head||d.documentElement).appendChild(_s);
if(["google.com/recaptcha","hcaptcha","cloudflare","turnstile"].some(x=>w.location.href.includes(x)))return;
const _L=()=>{try{return JSON.parse(l.getItem(K))||{}}catch(e){return{}}};
const S=Object.assign({s:100,e:false,bd:200,bo:false,cx:-1,cy:-1,ut:"50px",ul:"50px",mt:"10px",ml:"10px",im:false},_L());
const _SV=()=>{try{const u=d.getElementById(U),m=d.getElementById(M);l.setItem(K,JSON.stringify({s:w.G.s,e:w.G.e,bd:parseInt(d.getElementById('id').value)||200,bo:w.B.r,cx:w.B.x,cy:w.B.y,ut:u?u.style.top:S.ut,ul:u?u.style.left:S.ul,mt:m?m.style.top:S.mt,ml:m?m.style.left:S.ml,im:w.U.m}))}catch(e){}};
const N={p:w.performance.now.bind(w.performance),r:w.requestAnimationFrame.bind(w),t:w.setTimeout.bind(w),i:w.setInterval.bind(w),ci:w.clearInterval.bind(w)};
w.G={s:S.s,e:S.e,r:N.p(),v:N.p()};
const V=()=>{const n=N.p();return w.G.e?w.G.v+(n-w.G.r)*w.G.s:n};
if(w.performance){try{Object.defineProperty(Object.getPrototypeOf(w.performance),'now',{value:()=>V()})}catch(e){w.performance.now=()=>V()}}
const OF=Date.now()-N.p();Date.now=()=>Math.floor(V()+OF);w.Date=new Proxy(Date,{construct(t,a){return a.length===0?new t(Math.floor(V()+OF)):new t(...a)}});
w.requestAnimationFrame=c=>N.r(t=>c(V()));w.setTimeout=(f,d,...a)=>N.t(f,(w.G.e&&d>50)?d/w.G.s:d,...a);w.setInterval=(f,d,...a)=>N.i(f,(w.G.e&&d>50)?d/w.G.s:d,...a);
w.B={r:S.bo,t:null,s:0,x:S.cx,y:S.cy};w.U={m:S.im};
function _T(e,x,y,t){try{const o=new Touch({identifier:Date.now(),target:e,clientX:x,clientY:y,screenX:x,screenY:y,radiusX:1,radiusY:1,force:1});e.dispatchEvent(new TouchEvent(t,{bubbles:true,cancelable:true,view:w,touches:[o],targetTouches:[o],changedTouches:[o]}))}catch(z){}}
function _C(){const x=(w.B.x===-1)?w.innerWidth/2:w.B.x,y=(w.B.y===-1)?w.innerHeight/2:w.B.y;const u=d.getElementById(U),m=d.getElementById(M);if(u)u.style.display='none';if(m)m.style.display='none';let e=d.elementFromPoint(x,y);if(e&&!['BUTTON','A','INPUT','TEXTAREA'].includes(e.tagName)){const p=e.closest('button,a,[role="button"],input');if(p)e=p}if(u)u.style.display=w.U.m?'none':'flex';if(m)m.style.display=w.U.m?'flex':'none';if(e){e.focus?.();_T(e,x,y,'touchstart');_T(e,x,y,'touchend');e.click?.();_D(x,y,'#00ffcc')}else{d.body.click();_D(x,y,'#ff0055')}}
function _SC(t){const g=t?0:10000000;w.scrollTo({top:g,left:0,behavior:'auto'});if(d.scrollingElement)d.scrollingElement.scrollTop=g;d.documentElement.scrollTop=g;d.body.scrollTop=g}
function _BL(){if(!w.B.r)return;const lg=d.getElementById('bst');try{switch(w.B.s){case 0:_SC(true);if(lg)lg.innerText="🔼 TOP";w.B.s=1;break;case 1:_C();if(lg)lg.innerText="⚡ CLICK";w.B.s=2;break;case 2:_SC(false);if(lg)lg.innerText="🔽 BOT";w.B.s=3;break;case 3:_C();if(lg)lg.innerText="⚡ CLICK";w.B.s=0;break}}catch(e){}}
function _D(x,y,c){const z=d.createElement('div');z.style.cssText=`position:fixed;left:${x}px;top:${y}px;width:12px;height:12px;background:${c};border-radius:50%;z-index:2147483647;pointer-events:none;box-shadow:0 0 8px ${c};border:2px solid #fff`;(d.body||d.documentElement).appendChild(z);setTimeout(()=>z.remove(),250)}
function _R(){if(d.getElementById(U))return;
const ST_B="box-sizing:border-box!important;margin:0!important;padding:0!important;border:none!important;font-family:sans-serif!important;line-height:normal!important;";
const ST_F="display:flex!important;align-items:center!important;justify-content:center!important;";
const r=d.createElement('div');r.id=U;
r.style.cssText=`${ST_B}position:fixed!important;top:${S.ut};left:${S.ul};width:260px!important;z-index:2147483647!important;background:rgba(15,15,20,0.98)!important;backdrop-filter:blur(15px)!important;border:1px solid rgba(0,255,204,0.3)!important;border-radius:12px!important;box-shadow:0 0 20px rgba(0,0,0,0.9)!important;display:${S.im?'none':'flex'}!important;flex-direction:column!important;color:#fff!important;visibility:visible!important;opacity:1!important;`;
r.innerHTML=`
<div id="hd" style="${ST_B}height:38px!important;padding:0 14px!important;background:linear-gradient(90deg,rgba(0,255,204,0.1),transparent)!important;border-bottom:1px solid rgba(255,255,255,0.1)!important;cursor:move!important;display:flex!important;justify-content:space-between!important;align-items:center!important">
<span style="${ST_B}font-weight:700!important;font-size:13px!important;color:#00ffcc!important;letter-spacing:1px!important">⚡ SPEED WEB | httsvb</span>
<div id="bm" style="${ST_B}font-size:16px!important;font-weight:bold!important;cursor:pointer!important;padding:5px 12px!important;background:rgba(255,255,255,0.05)!important;margin-right:-14px!important;border-left:1px solid rgba(255,255,255,0.1)!important;color:#fff!important;height:100%!important;${ST_F}">__</div>
</div>
<div style="${ST_B}padding:20px 20px!important;display:flex!important;flex-direction:column!important;gap:15px!important">
<div style="${ST_B}display:flex!important;align-items:center!important;justify-content:space-between!important;gap:10px!important;width:100%!important">
<span style="${ST_B}font-size:11px!important;color:#ccc!important;font-weight:600!important;width:80px!important">SPEED WEB</span>
<input type="number" id="is" value="${S.s}" style="${ST_B}background:#0a0a0a!important;border:1px solid #333!important;color:#fff!important;border-radius:6px!important;text-align:center!important;font-weight:bold!important;font-size:13px!important;width:60px!important;height:30px!important;outline:none!important">
<button id="bs" style="${ST_B}border-radius:6px!important;font-weight:700!important;font-size:11px!important;cursor:pointer!important;color:#fff!important;flex:1!important;height:30px!important;${ST_F}background:${S.e?'linear-gradient(135deg,#00b894,#00cec9)':'rgba(255,255,255,0.1)'}!important">${S.e?'ON':'OFF'}</button>
</div>
<div style="${ST_B}display:flex!important;align-items:center!important;justify-content:space-between!important;gap:10px!important;width:100%!important">
<span style="${ST_B}font-size:11px!important;color:#ccc!important;font-weight:600!important;width:80px!important">SCROLL DELAY</span>
<input type="number" id="id" value="${S.bd}" style="${ST_B}background:#0a0a0a!important;border:1px solid #333!important;color:#fff!important;border-radius:6px!important;text-align:center!important;font-weight:bold!important;font-size:13px!important;width:60px!important;height:30px!important;outline:none!important">
<span style="${ST_B}font-size:10px;width:auto;color:#666">MS</span>
</div>
<div id="tc" style="${ST_B}text-align:center!important;font-size:11px!important;color:#ccc!important;font-family:monospace!important;margin:4px 0!important;border:1px dashed #444!important;padding:6px!important;border-radius:4px!important">${S.cx!==-1?`POS: [${S.cx}, ${S.cy}]`:'-- NO POINT --'}</div>
<div style="${ST_B}display:flex!important;align-items:center!important;justify-content:space-between!important;gap:10px!important;width:100%!important">
<button id="bp" style="${ST_B}border-radius:6px!important;font-weight:700!important;font-size:11px!important;cursor:pointer!important;color:#74b9ff!important;flex:1!important;height:30px!important;${ST_F}background:rgba(9,132,227,0.2)!important;border:1px solid #0984e3!important">🎯 SET</button>
<button id="br" style="${ST_B}border-radius:6px!important;font-weight:700!important;font-size:11px!important;cursor:pointer!important;color:#fff!important;flex:1!important;height:30px!important;${ST_F}background:${S.bo?'linear-gradient(135deg,#FF512F,#DD2476)':'rgba(255,255,255,0.1)'}!important;color:${S.bo?'#000':'#aaa'}!important">${S.bo?'STOP':'START'}</button>
</div>
<div id="bst" style="${ST_B}font-size:11px!important;text-align:center!important;color:#00ffcc!important;margin-top:4px!important;font-weight:bold!important">${S.bo?'RUNNING...':'READY'}</div>
</div>
<div style="${ST_B}height:34px!important;${ST_F}background:rgba(88,101,242,0.1)!important;border-top:1px solid rgba(88,101,242,0.2)!important">
<a href="https://discord.gg/8wPm9eMS" target="_blank" style="${ST_B}color:#5865F2!important;text-decoration:none!important;font-size:11px!important;font-weight:700!important;display:flex!important;align-items:center!important;gap:5px!important"><span>💬</span> Join Discord</a>
</div>`;
const m=d.createElement('div');m.id=M;m.innerHTML='⚡';
m.style.cssText=`${ST_B}position:fixed!important;top:${S.mt};left:${S.ml};width:45px!important;height:45px!important;z-index:2147483647!important;background:rgba(0,0,0,0.9)!important;border:2px solid #00ffcc!important;border-radius:50%!important;display:${S.im?'flex':'none'}!important;${ST_F}cursor:pointer!important;box-shadow:0 0 15px #00ffcc!important;font-size:24px!important;user-select:none!important;visibility:visible!important;opacity:1!important;`;
const ov=d.createElement('div');ov.id=O;
ov.style.cssText=`position:fixed!important;top:0!important;left:0!important;width:100vw!important;height:100vh!important;background:rgba(0,0,0,0.5)!important;z-index:2147483647!important;cursor:crosshair!important;touch-action:none!important;display:none!important;`;
const root=d.documentElement;root.appendChild(r);root.appendChild(m);root.appendChild(ov);_Ev(r,m,ov)}
function _Ev(r,m,ov){
const is=d.getElementById('is'),bs=d.getElementById('bs'),br=d.getElementById('br'),bp=d.getElementById('bp'),id=d.getElementById('id'),tc=d.getElementById('tc'),st=d.getElementById('bst'),bm=d.getElementById('bm');
const _tg=()=>{w.U.m=!w.U.m;r.style.setProperty('display',w.U.m?'none':'flex','important');m.style.setProperty('display',w.U.m?'flex':'none','important');_SV()};
const _sp=e=>e.stopPropagation();bm.onmousedown=_sp;bm.ontouchstart=_sp;bm.onclick=e=>{e.stopPropagation();_tg()};
let sx,sy;m.onmousedown=e=>{sx=e.clientX;sy=e.clientY};m.ontouchstart=e=>{sx=e.touches[0].clientX;sy=e.touches[0].clientY};
const _ic=e=>{const ex=e.changedTouches?e.changedTouches[0].clientX:e.clientX,ey=e.changedTouches?e.changedTouches[0].clientY:e.clientY;if(Math.hypot(ex-sx,ey-sy)<5)_tg()};m.onmouseup=_ic;m.ontouchend=_ic;
is.onchange=e=>{const n=N.p();w.G.v+=(n-w.G.r)*w.G.s;w.G.r=n;w.G.s=parseFloat(e.target.value)||1;_SV()};
bs.onclick=()=>{const n=N.p();w.G.v+=(n-w.G.r)*w.G.s;w.G.r=n;w.G.e=!w.G.e;bs.style.background=w.G.e?'linear-gradient(135deg,#00b894,#00cec9)':'rgba(255,255,255,0.1)';bs.innerText=w.G.e?'ON':'OFF';_SV()};
br.onclick=()=>{w.B.r=!w.B.r;if(w.B.r){br.style.background='linear-gradient(135deg,#FF512F,#DD2476)';br.style.color='#000';br.innerText="STOP";st.innerText="RUNNING...";_BL();N.ci(w.B.t);w.B.t=N.i(_BL,parseInt(id.value)||200)}else{br.style.background='rgba(255,255,255,0.1)';br.style.color='#aaa';br.innerText="START";st.innerText="STOPPED";N.ci(w.B.t)}_SV()};
id.onchange=()=>{if(w.B.r){N.ci(w.B.t);w.B.t=N.i(_BL,parseInt(id.value)||200)}_SV()};
bp.onclick=()=>{ov.style.setProperty('display','block','important');st.innerText="TAP TO SELECT...";const rs=e=>{e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();const x=Math.round(e.touches?e.touches[0].clientX:e.clientX),y=Math.round(e.touches?e.touches[0].clientY:e.clientY);w.B.x=x;w.B.y=y;tc.innerText=`POS: [${x}, ${y}]`;_D(x,y,'#00ffcc');st.innerText="SAVED!";ov.style.setProperty('display','none','important');_SV()};ov.onclick=rs;ov.ontouchstart=rs;ov.onmousedown=rs};
_Dr(r,d.getElementById('hd'));_Dr(m,m)}
function _Dr(e,h){let d=false,sx,sy,ix,iy;const s=v=>{d=true;sx=v.touches?v.touches[0].clientX:v.clientX;sy=v.touches?v.touches[0].clientY:v.clientY;const b=e.getBoundingClientRect();ix=b.left;iy=b.top;document.addEventListener('mousemove',mv);document.addEventListener('touchmove',mv);document.addEventListener('mouseup',en);document.addEventListener('touchend',en)};const mv=v=>{if(!d)return;const cx=v.touches?v.touches[0].clientX:v.clientX,cy=v.touches?v.touches[0].clientY:v.clientY;e.style.left=(ix+cx-sx)+'px';e.style.top=(iy+cy-sy)+'px';v.preventDefault()};const en=()=>{d=false;document.removeEventListener('mousemove',mv);document.removeEventListener('touchmove',mv);_SV()};h.addEventListener('mousedown',s);h.addEventListener('touchstart',s)}
const _Z=N.i(()=>{if(!d.body)return;if(!d.getElementById(U)){_R();if(w.B.r&&!w.B.t)w.B.t=N.i(_BL,S.bd)}},500)}_Run()})();
