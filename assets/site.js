const toggle=document.querySelector('.nav-toggle');
const links=document.querySelector('.nav-links');
if(toggle&&links){toggle.addEventListener('click',()=>{const open=links.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});links.addEventListener('click',event=>{if(event.target.closest('a')){links.classList.remove('open');toggle.setAttribute('aria-expanded','false');}});}
// Nav dropdowns are <details>, so open/close/keyboard already work without JS.
// These handlers only add the polish browsers do not give us: one open at a time,
// close on outside click, close on Escape, and hover-to-open on real pointers.
const menus=[...document.querySelectorAll('.menu')];
if(menus.length){
  const shut=except=>menus.forEach(m=>{if(m!==except)m.open=false;});
  menus.forEach(m=>{
    m.addEventListener('toggle',()=>{if(m.open)shut(m);});
    m.addEventListener('click',e=>{if(e.target.closest('.menu-panel a'))m.open=false;});
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.menu'))shut(null);});
  document.addEventListener('keydown',e=>{
    if(e.key!=='Escape')return;
    const open=menus.find(m=>m.open);
    if(open){open.open=false;open.querySelector('summary').focus();}
  });
  // Hover only where hovering is meaningful and there is room for a dropdown.
  if(window.matchMedia('(hover:hover) and (min-width:901px)').matches){
    menus.forEach(m=>{
      let t;
      m.addEventListener('mouseenter',()=>{clearTimeout(t);shut(m);m.open=true;});
      m.addEventListener('mouseleave',()=>{t=setTimeout(()=>{m.open=false;},220);});
    });
  }
}
