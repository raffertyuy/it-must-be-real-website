/* Dependency-free, accessible page turns. Narration is always DOM text, never pixels. */
export default function renderBook(component) {
  const {parentElement, data} = component;
  let root = parentElement.querySelector('.reader');
  if (!root) {
    root = document.createElement('section');
    root.className = 'reader';
    root.tabIndex = 0;
    root.setAttribute('aria-label', 'Illustrated storybook');
    parentElement.appendChild(root);
  }
  let state = root.__book;
  const incoming = Math.max(1, Math.min(data.page || 1, data.story.pages.length));
  if (state && state.revision === data.revision) {
    state.bridge = component;
    // A late acknowledgement must not rewind a more recent local page turn.
    if ((data.sequence || 0) >= state.sequence && incoming !== state.page && !state.turning) {
      state.page = incoming;
      state.paint();
    }
    state.motion.addEventListener("change",state.onMotion);
    return () => state.motion.removeEventListener("change",state.onMotion);
  }
  if (state) state.dispose();
  root.replaceChildren();
  state = {bridge:component, revision:data.revision, story:data.story,
    page:incoming, sequence:data.sequence || 0, turning:false, all:false,
    animation:null, disposed:false, touch:null, timers:new Set()};
  root.__book = state;
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const narrow = {get matches() {return root.getBoundingClientRect().width <= 740;}};
  const abort = new AbortController();
  const listen = (element, event, fn) => element.addEventListener(event, fn, {signal:abort.signal});
  const el = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const button = (text, label, cls='') => {
    const b = el('button',cls,text); b.type='button'; b.setAttribute('aria-label',label); return b;
  };
  const toolbar=el('div','toolbar');
  const label=el('label','', 'Page');
  const select=el('select'); select.setAttribute('aria-label','Go to page');
  state.story.pages.forEach((p,i)=> {const o=el('option','',`${i+1}. ${p.title}`); o.value=String(i+1); select.append(o);});
  label.append(select); toolbar.append(label);
  const tools=el('div','tools');
  const allButton=button('Read all pages','Read all pages'); allButton.setAttribute('aria-pressed','false');
  const share=button('Share page','Share current page');
  tools.append(allButton,share); toolbar.append(tools);
  const settings=el('div','settings');
  const motionLabel=el('label');
  const motionInput=el('input'); motionInput.type='checkbox'; motionInput.checked=!motion.matches;
  motionInput.setAttribute('aria-label','Animate page turns');
  motionLabel.append(motionInput,el('span','','Animate page turns'));
  const reducedNote=el('span','','Reduced-motion preference is respected.');
  reducedNote.hidden=!motion.matches;
  settings.append(motionLabel,reducedNote);
  const stage=el('div','book-stage');
  const footer=el('nav','reader-footer page-controls'); footer.setAttribute('aria-label','Book pages');
  const previous=button('← Previous','Previous page');
  const next=button('Next →','Next page','primary');
  const progressWrap=el('div','reader-progress');
  const count=el('span'); count.setAttribute('aria-live','polite');
  const progress=el('progress'); progress.max=state.story.pages.length;
  progress.setAttribute('aria-label','Reading progress'); progressWrap.append(count,progress);
  footer.append(previous,progressWrap,next);
  const hint=el('p','reader-hint','Use the buttons or ← → keys. Swipe the illustration on touch screens.');
  const status=el('p','book-status'); status.setAttribute('role','status'); status.setAttribute('aria-live','polite');
  const shareInput=el('input','share-field'); shareInput.type='url'; shareInput.readOnly=true; shareInput.setAttribute('aria-label','Current page link');
  root.append(toolbar,settings,stage,footer,hint,status,shareInput);

  function spread(number) {
    const p=state.story.pages[number-1];
    const article=el('article','book-spread'); article.setAttribute('aria-label',`Page ${number}: ${p.title}`);
    const art=el('figure','book-art');
    const img=el('img'); img.src=p.src; img.alt=p.alt; img.width=p.width || 640; img.height=p.height || 960;
    img.draggable=false; img.loading=state.all?'lazy':'eager';
    listen(img,'error',()=> { img.alt=`Illustration unavailable. ${p.alt}`; });
    art.append(img);
    const copy=el('div','book-copy');
    copy.append(el('div','book-eyebrow',`PAGE ${String(number).padStart(2,'0')} / ${String(state.story.pages.length).padStart(2,'0')}`),el('h2','',p.title));
    p.paragraphs.forEach(text=>copy.append(el('p','',text)));
    copy.append(el('p','book-caption',p.caption));
    article.append(art,copy);
    return article;
  }
  function controls() {
    select.value=String(state.page);
    previous.disabled=state.turning || state.page===1;
    next.disabled=state.turning || state.page===state.story.pages.length;
    count.textContent=`${state.page} / ${state.story.pages.length}`;
    progress.value=state.page;
    next.textContent=state.page===state.story.pages.length?'The end':'Next →';
    allButton.textContent=state.all?'Back to page turns':'Read all pages';
    allButton.setAttribute('aria-pressed',String(state.all));
  }
  function preload() {
    for (const n of [state.page-1,state.page+1]) if (n>=1 && n<=state.story.pages.length) {
      const img=new Image(); img.src=state.story.pages[n-1].src;
    }
  }
  state.paint = () => {
    root.classList.toggle('reading-all',state.all);
    if (state.all) {
      const collection=el('div','book-collection');
      state.story.pages.forEach((_,i)=>collection.append(spread(i+1)));
      stage.replaceChildren(collection);
    } else stage.replaceChildren(spread(state.page));
    controls(); preload();
  };
  function emit() {
    state.sequence += 1;
    state.bridge.setStateValue('position',{page:state.page,sequence:state.sequence});
  }
  async function turn(target) {
    target=Math.max(1,Math.min(Number(target),state.story.pages.length));
    if (!Number.isInteger(target) || state.turning || target===state.page) {controls();return;}
    if (state.all) {state.all=false;state.page=target;state.paint();emit();return;}
    shareInput.classList.remove('visible'); status.textContent='';
    state.turning=true; controls();
    const old=stage.querySelector('.book-spread');
    const incomingSpread=spread(target);
    const forward=target>state.page;
    const animate=motionInput.checked && !motion.matches && typeof old.animate==='function';
    try {
      if (animate) {
        stage.classList.add('is-turning');
        // Mobile turns the entire stacked spread; desktop turns a leaf at the spine.
        const mobile=narrow.matches;
        const leaf=el('div',`turn-leaf ${forward?'forward':'backward'}`); leaf.setAttribute('aria-hidden','true');
        const front=el('div','leaf-face front'); const back=el('div','leaf-face back');
        if (mobile) {
          stage.style.height=`${Math.max(old.offsetHeight,incomingSpread.offsetHeight)}px`;
          front.append(old.cloneNode(true)); back.append(incomingSpread.cloneNode(true));
          stage.replaceChildren(incomingSpread);
        } else {
          const oldArt=old.children[0],oldCopy=old.children[1];
          const newArt=incomingSpread.children[0],newCopy=incomingSpread.children[1];
          const originalHeight=old.offsetHeight;
          front.append((forward?oldCopy:oldArt).cloneNode(true));
          back.append((forward?newArt:newCopy).cloneNode(true));
          if (forward) oldCopy.replaceWith(newCopy); else oldArt.replaceWith(newArt);
          stage.style.height=`${Math.max(originalHeight,old.offsetHeight)}px`;
        }
        leaf.append(front,back); stage.append(leaf);
        // Explicit rotation is a real page-turn animation, not a scale/fade effect.
        state.animation=leaf.animate([
          {transform:'rotateY(0deg)',filter:'brightness(1)'},
          {transform:`rotateY(${forward?'-':'+'}90deg)`,filter:'brightness(.68)',offset:.5},
          {transform:`rotateY(${forward?'-':'+'}180deg)`,filter:'brightness(1)'}
        ],{duration:650,easing:'cubic-bezier(.3,.08,.25,1)',fill:'forwards'});
        await state.animation.finished;
      }
    } catch (error) {
      // A resize/unmount can cancel an animation; never strand the controls.
      if (state.disposed) return;
    } finally {
      if (!state.disposed && root.isConnected) {
        state.animation=null; state.page=target; state.turning=false;
        stage.classList.remove('is-turning'); stage.style.height='';
        state.paint();
        if (narrow.matches || root.getBoundingClientRect().top < 50) root.scrollIntoView({block:"start",behavior:"instant"});
        emit();
      }
    }
  }
  listen(previous,'click',()=>turn(state.page-1));
  listen(next,'click',()=>turn(state.page+1));
  listen(select,'change',()=>turn(select.value));
  listen(allButton,'click',()=> {
    if (state.turning) return;
    state.all=!state.all; state.paint();
  });
  listen(root,'keydown',event=> {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || state.all || ['SELECT','INPUT','TEXTAREA'].includes(event.target.tagName)) return;
    if (event.key==='ArrowRight') {event.preventDefault();turn(state.page+1);}
    if (event.key==='ArrowLeft') {event.preventDefault();turn(state.page-1);}
    if (event.key==='Home') {event.preventDefault();turn(1);}
    if (event.key==='End') {event.preventDefault();turn(state.story.pages.length);}
  });
  listen(stage,'pointerdown',event=> {
    if (event.pointerType==='touch' && event.target.closest('.book-art')) state.touch={x:event.clientX,y:event.clientY,time:Date.now()};
  });
  listen(stage,'pointerup',event=> {
    if (!state.touch) return;
    const {x,y,time}=state.touch; state.touch=null;
    const dx=event.clientX-x,dy=event.clientY-y;
    if (!state.all && Date.now()-time<1000 && Math.abs(dx)>65 && Math.abs(dx)>Math.abs(dy)*1.5) turn(state.page+(dx<0?1:-1));
  });
  listen(stage,'pointercancel',()=> {state.touch=null;});
  listen(share,'click',async()=> {
    const url=new URL(window.location.href);url.searchParams.set('story',state.story.id);url.searchParams.set('page',String(state.page));
    try {await navigator.clipboard.writeText(url.href);status.textContent='Page link copied.';}
    catch {shareInput.value=url.href;shareInput.classList.add('visible');shareInput.focus();shareInput.select();status.textContent='Copy the selected page link.';}
  });
  state.motion=motion;
  state.onMotion=()=> {reducedNote.hidden=!motion.matches;if(motion.matches){motionInput.checked=false;if(state.animation)state.animation.cancel();}};
  motion.addEventListener('change',state.onMotion);
  state.dispose=()=> {state.disposed=true;motion.removeEventListener('change',state.onMotion);abort.abort();if(state.animation)state.animation.cancel();state.timers.forEach(clearTimeout);};
  state.paint();
  return () => { motion.removeEventListener('change',state.onMotion); if(state.animation) state.animation.cancel(); };
  // No global key handlers or document-wide CSS to leak into other site pages.
}
