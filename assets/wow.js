// Общий интерактивный слой концептов. Подключается последним скриптом страницы.
(function(){
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;

// Заголовки по словам: [data-split]
document.querySelectorAll('[data-split]').forEach(el=>{
 const walk=n=>{[...n.childNodes].forEach(c=>{
  if(c.nodeType===3&&c.textContent.trim()){const f=document.createDocumentFragment();
   c.textContent.split(/(\s+)/).forEach(w=>{if(!w)return;if(/^\s+$/.test(w)){f.append(w);return}
    const o=document.createElement('span');o.className='wd';const i=document.createElement('span');i.textContent=w;o.append(i);f.append(o)});
   c.replaceWith(f)}else if(c.nodeType===1&&!c.classList.contains('wd'))walk(c)})};
 walk(el);el.querySelectorAll('.wd>span').forEach((s,i)=>s.style.transitionDelay=(i*.06+(+el.dataset.delay||0))+'s')});

// Появление при прокрутке, с задержкой по порядку внутри [data-stagger]
document.querySelectorAll('[data-stagger]').forEach(g=>[...g.querySelectorAll('[data-reveal]')].forEach((c,i)=>c.style.transitionDelay=i*.08+'s'));
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('[data-reveal],[data-split]').forEach(el=>reduce?el.classList.add('in'):io.observe(el));

// Счётчики: <b data-count="1250" data-suffix=" ₽">
const cio=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;cio.unobserve(e.target);const el=e.target,to=+el.dataset.count,suf=el.dataset.suffix||'',fmt=v=>Math.round(v).toLocaleString('ru-RU')+suf;
 if(reduce){el.textContent=fmt(to);return}let t0=null;(function a(t){t0??=t;const k=Math.min(1,(t-t0)/1400);el.textContent=fmt(to*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(a)})(performance.now())}),{threshold:.5});
document.querySelectorAll('[data-count]').forEach(el=>cio.observe(el));

if(reduce)return;

// 3D-наклон с бликом: [data-tilt="10"]
if(fine)document.querySelectorAll('[data-tilt]').forEach(el=>{const m=+el.dataset.tilt||8;
 if(getComputedStyle(el).position==='static')el.style.position='relative';
 const g=document.createElement('span');g.className='glare';el.append(g);
 el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;el.classList.add('tilting');
  el.style.transform=`perspective(900px) rotateY(${(x-.5)*m*2}deg) rotateX(${(.5-y)*m*2}deg) translateZ(0)`;el.style.setProperty('--gx',x*100+'%');el.style.setProperty('--gy',y*100+'%')});
 el.addEventListener('pointerleave',()=>{el.classList.remove('tilting');el.style.transform=''})});

// Магнитные кнопки: [data-mag]
if(fine)document.querySelectorAll('[data-mag]').forEach(b=>{const s=+b.dataset.mag||.3;
 b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.classList.add('magging');b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*s}px,${(e.clientY-r.top-r.height/2)*s}px)`});
 b.addEventListener('pointerleave',()=>{b.classList.remove('magging');b.style.transform=''})});

// Параллакс: [data-parallax="0.15"]
const par=[...document.querySelectorAll('[data-parallax]')];
// Полоса прогресса прокрутки, если на странице есть .wow-progress
const bar=document.querySelector('.wow-progress');
if(par.length||bar){let ticking=false;const run=()=>{ticking=false;
 par.forEach(el=>{const r=el.getBoundingClientRect(),c=r.top+r.height/2-innerHeight/2;el.style.translate=`0 ${-c*(+el.dataset.parallax)}px`});
 if(bar){const h=document.documentElement.scrollHeight-innerHeight;bar.style.transform=`scaleX(${h>0?scrollY/h:0})`}};
 addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(run)}},{passive:true});run()}
})();
