/* Cohen & McMullen, P.A. — motion layer.
   Everything degrades: without GSAP/Lenis, or with reduced motion, content stays readable and films show posters. */
(function () {
  window.__cmReady = true;
  const doc = document.documentElement;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const hasGsap = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  if (reduced) doc.classList.add('reduced');
  if (!hasGsap) doc.classList.add('no-motion');
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  /* ---------- Smooth scroll ---------- */
  let lenis = null;
  if (!reduced && typeof window.Lenis !== 'undefined') {
    lenis = new Lenis({ duration: 1.15, easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
    if (hasGsap) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((time) => lenis.raf(time * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }

  /* ---------- Films: lazy load, play only while visible ---------- */
  const conn = navigator.connection || {};
  const saveData = !!conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '');
  const loadVideo = (v) => {
    if (v.dataset.loaded || saveData) return;
    const src = (v.dataset.srcSm && window.innerWidth < 900) ? v.dataset.srcSm : v.dataset.src;
    if (!src) return;
    v.src = src;
    v.dataset.loaded = '1';
  };
  const playVideo = (v) => {
    if (reduced || saveData) return;
    loadVideo(v);
    const p = v.play();
    if (p && p.catch) p.catch(() => {});
  };
  const vio = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      const v = e.target;
      if (e.isIntersecting) playVideo(v);
      else if (v.dataset.loaded) v.pause();
    });
  }, { rootMargin: '200px 0px', threshold: 0.1 });
  // Background tabs defer media; resume whatever is on screen once the tab is shown.
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) return;
    document.querySelectorAll('video[data-loaded]').forEach((v) => {
      const r = v.getBoundingClientRect();
      if (r.bottom > 0 && r.top < innerHeight && v.paused && (!v.closest('.menu') || v.classList.contains('is-on'))) playVideo(v);
    });
  });
  document.querySelectorAll('video[data-src]').forEach((v) => {
    if (v.closest('.menu')) return;
    vio.observe(v);
    const tile = v.closest('.tile');
    if (tile) v.addEventListener('playing', () => tile.classList.add('is-playing'));
  });

  /* ---------- Curtain: page intro + blade transition between pages ---------- */
  const curtain = document.querySelector('.curtain');
  const panel = curtain && curtain.querySelector('.curtain__panel');
  const edge = curtain && curtain.querySelector('.curtain__edge');
  const crest = curtain && curtain.querySelector('.curtain__crest');
  // Visitors arriving from search or another site go straight to content; the crest plays once per session.
  const fromOutside = !document.referrer || new URL(document.referrer, location.href).origin !== location.origin;
  const firstVisit = (() => { try { const f = !sessionStorage.getItem('cm-seen'); sessionStorage.setItem('cm-seen', '1'); return f; } catch (e) { return false; } })();

  function intro() {
    if (!hasGsap || reduced || !curtain) { doc.classList.remove('is-loading'); heroIn(); return; }
    const tl = gsap.timeline({ onComplete: () => doc.classList.remove('is-loading') });
    if (firstVisit && !fromOutside) {
      tl.fromTo(crest, { opacity: 0, scale: 0.92, clipPath: 'inset(0 0 100% 0)' }, { opacity: 1, scale: 1, clipPath: 'inset(0 0 0% 0)', duration: 0.6, ease: 'power3.out' })
        .to(crest, { opacity: 0, y: -24, duration: 0.3, ease: 'power2.in' }, '+=0.1');
    } else {
      tl.set(crest, { opacity: 0 });
    }
    tl.set(panel, { transformOrigin: 'top' })
      .set(edge, { top: '100%', opacity: 1 })
      .to(panel, { scaleY: 0, duration: fromOutside ? 0.6 : 0.85, ease: 'expo.inOut' })
      .to(edge, { top: '0%', duration: fromOutside ? 0.6 : 0.85, ease: 'expo.inOut' }, '<')
      .to(edge, { opacity: 0, duration: 0.3 })
      .add(heroIn, fromOutside ? '-=0.7' : '-=0.9');
  }

  function leave(href) {
    if (!hasGsap || reduced || !curtain) { window.location.href = href; return; }
    doc.classList.add('is-loading');
    gsap.set(crest, { opacity: 0 });
    gsap.set(panel, { transformOrigin: 'bottom', scaleY: 0 });
    gsap.set(edge, { top: '100%', opacity: 1 });
    gsap.timeline({ onComplete: () => { window.location.href = href; } })
      .to(panel, { scaleY: 1, duration: 0.75, ease: 'expo.inOut' })
      .to(edge, { top: '0%', duration: 0.75, ease: 'expo.inOut' }, '<');
  }

  document.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || a.target === '_blank' || a.hasAttribute('download') || /^(mailto|tel):/.test(href)) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin) return;
    if (url.pathname === location.pathname && url.hash) return;
    e.preventDefault();
    closeMenu();
    leave(url.href);
  });
  window.addEventListener('pageshow', (e) => {
    if (e.persisted) { doc.classList.remove('is-loading'); if (hasGsap && panel) { gsap.set(panel, { scaleY: 0 }); gsap.set(edge, { opacity: 0 }); } }
  });

  /* ---------- Word splitting ---------- */
  const splitWords = (el, cls) => {
    const walk = (node) => {
      [...node.childNodes].forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            const outer = document.createElement('span');
            outer.className = cls;
            if (cls === 'reveal-line') {
              const inner = document.createElement('span');
              inner.textContent = part;
              outer.appendChild(inner);
              outer.style.display = 'inline-block';
            } else outer.textContent = part;
            frag.appendChild(outer);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) walk(n);
      });
    };
    walk(el);
  };

  /* ---------- Hero headline: word-by-word blade reveal ---------- */
  const heroTitle = document.querySelector('[data-split]');
  if (heroTitle && hasGsap && !reduced) { splitWords(heroTitle, 'reveal-line'); gsap.set(heroTitle.querySelectorAll('.reveal-line > span'), { yPercent: 115 }); }
  let heroDone = false;
  function heroIn() {
    if (heroDone || !hasGsap || reduced) return; heroDone = true;
    const words = heroTitle ? heroTitle.querySelectorAll('.reveal-line > span') : [];
    gsap.timeline({ delay: 0.15 })
      .to(words, { yPercent: 0, duration: 1.3, ease: 'expo.out', stagger: 0.05 })
      .from('.film__content [data-hero-fade]', { opacity: 0, y: 24, duration: 1, ease: 'power3.out', stagger: 0.1 }, '-=0.9')
      .from('.film:first-of-type .film__media video, .film:first-of-type .film__media img', { scale: 1.18, duration: 2.4, ease: 'expo.out' }, 0)
      .from('.film__rail', { opacity: 0, duration: 1 }, 0.4);
  }

  /* ---------- Scroll choreography ---------- */
  if (hasGsap && !reduced) {
    document.querySelectorAll('.film').forEach((film) => {
      const media = film.querySelector('.film__media');
      gsap.to(media, { yPercent: 16, ease: 'none', scrollTrigger: { trigger: film, start: 'top top', end: 'bottom top', scrub: true } });
      const content = film.querySelector('.film__content');
      if (content) gsap.to(content, { yPercent: -25, opacity: 0, ease: 'none', scrollTrigger: { trigger: film, start: '40% top', end: 'bottom top', scrub: true } });
    });

    document.querySelectorAll('.cta .film__media, .manifesto .film__media').forEach((m) => {
      gsap.fromTo(m, { yPercent: -6, scale: 1.12 }, { yPercent: 6, scale: 1.02, ease: 'none', scrollTrigger: { trigger: m.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
    });

    document.querySelectorAll('.blade__line').forEach((l) => {
      gsap.fromTo(l, { scaleY: 0 }, { scaleY: 1, ease: 'none', scrollTrigger: { trigger: l, start: 'top 85%', end: 'bottom 45%', scrub: true } });
    });

    ScrollTrigger.batch('[data-reveal]', {
      start: 'top 90%',
      onEnter: (els) => gsap.to(els, { opacity: 1, y: 0, duration: 1.2, ease: 'expo.out', stagger: 0.09, overwrite: true }),
    });

    ScrollTrigger.batch('.tile, .people-grid .person', {
      start: 'top 94%',
      onEnter: (els) => gsap.fromTo(els, { clipPath: 'inset(16% 0% 0% 0%)', y: 60 }, { clipPath: 'inset(0% 0% 0% 0%)', y: 0, duration: 1.4, ease: 'expo.out', stagger: 0.1, overwrite: true }),
    });

    document.querySelectorAll('.manifesto').forEach((m) => {
      const text = m.querySelector('.manifesto__text');
      splitWords(text, 'w');
      const words = text.querySelectorAll('.w');
      ScrollTrigger.create({
        trigger: m, start: 'top top', end: 'bottom bottom', scrub: true,
        onUpdate: (self) => {
          const n = Math.round(self.progress * 1.3 * words.length);
          words.forEach((w, i) => { w.style.opacity = i < n ? 1 : 0.14; });
        },
      });
      const body = m.querySelector('.manifesto__body');
      if (body) gsap.from(body, { opacity: 0, y: 40, ease: 'none', scrollTrigger: { trigger: m, start: '45% top', end: '65% top', scrub: true } });
    });

    const pin = document.querySelector('.people-pin');
    if (pin) {
      ScrollTrigger.matchMedia({
        '(min-width: 901px)': () => {
          const track = pin.querySelector('.people-track');
          const dist = () => Math.max(0, track.scrollWidth - pin.clientWidth);
          if (dist() < 40) return;
          gsap.to(track, {
            x: () => -dist(), ease: 'none',
            scrollTrigger: { trigger: pin.closest('section'), start: 'top top', end: () => '+=' + dist() * 1.2, pin: true, scrub: 0.8, invalidateOnRefresh: true },
          });
        },
      });
    }

    document.querySelectorAll('.footer__big').forEach((b) => {
      gsap.fromTo(b, { xPercent: 4 }, { xPercent: -16, ease: 'none', scrollTrigger: { trigger: b, start: 'top bottom', end: 'bottom top', scrub: true } });
    });

    if (finePointer) {
      document.querySelectorAll('.btn, .cta__phone').forEach((b) => {
        b.addEventListener('mousemove', (e) => {
          const r = b.getBoundingClientRect();
          gsap.to(b, { x: (e.clientX - r.left - r.width / 2) * 0.2, y: (e.clientY - r.top - r.height / 2) * 0.3, duration: 0.6, ease: 'power3.out' });
        });
        b.addEventListener('mouseleave', () => gsap.to(b, { x: 0, y: 0, duration: 0.9, ease: 'elastic.out(1, 0.4)' }));
      });
    }
    window.addEventListener('load', () => ScrollTrigger.refresh());
  } else {
    document.querySelectorAll('[data-reveal]').forEach((el) => { el.style.opacity = 1; el.style.transform = 'none'; });
  }

  /* ---------- Tile spotlight ---------- */
  document.querySelectorAll('.tile').forEach((t) => {
    t.addEventListener('pointermove', (e) => {
      const r = t.getBoundingClientRect();
      t.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      t.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* ---------- Header ---------- */
  const header = document.querySelector('.header');
  let lastY = 0;
  const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 40);
    // Header (and its case-evaluation button) stays visible at all times.
    lastY = y;
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Menu with film previews ---------- */
  const menuBtn = document.querySelector('.menu-btn');
  const menu = document.querySelector('.menu');
  const menuFilms = menu ? [...menu.querySelectorAll('.menu__films video')] : [];
  function setFilm(key) {
    menuFilms.forEach((v) => {
      const on = v.dataset.key === key;
      v.classList.toggle('is-on', on);
      if (on) playVideo(v); else if (v.dataset.loaded) v.pause();
    });
  }
  function openMenu() {
    doc.classList.add('menu-open');
    menuBtn.setAttribute('aria-expanded', 'true');
    menuBtn.querySelector('.menu-btn__label').textContent = 'Close';
    menu.removeAttribute('inert');
    if (lenis) lenis.stop();
    const current = menu.querySelector('[aria-current="page"]');
    setFilm(current ? current.dataset.film : (menuFilms[0] && menuFilms[0].dataset.key));
  }
  function closeMenu() {
    if (!menu || !doc.classList.contains('menu-open')) return;
    doc.classList.remove('menu-open');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.querySelector('.menu-btn__label').textContent = 'Menu';
    menu.setAttribute('inert', '');
    if (lenis) lenis.start();
    menuFilms.forEach((v) => v.dataset.loaded && v.pause());
  }
  if (menuBtn && menu) {
    menu.setAttribute('inert', '');
    menuBtn.addEventListener('click', () => (doc.classList.contains('menu-open') ? closeMenu() : openMenu()));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });
    menu.querySelectorAll('[data-film]').forEach((a) => {
      a.addEventListener('mouseenter', () => setFilm(a.dataset.film));
      a.addEventListener('focus', () => setFilm(a.dataset.film));
    });
  }

  /* ---------- Accordions: animate open/close ---------- */
  document.querySelectorAll('.qa details').forEach((d) => {
    const s = d.querySelector('summary');
    const body = d.querySelector('.qa__a');
    s.addEventListener('click', (e) => {
      if (reduced || !body.animate) return;
      e.preventDefault();
      const refresh = () => { if (hasGsap) ScrollTrigger.refresh(); };
      if (d.open) {
        const a = body.animate([{ height: body.offsetHeight + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 450, easing: 'cubic-bezier(.22,1,.36,1)' });
        a.onfinish = () => { d.open = false; refresh(); };
      } else {
        d.open = true;
        const h = body.offsetHeight;
        body.animate([{ height: '0px', opacity: 0 }, { height: h + 'px', opacity: 1 }], { duration: 600, easing: 'cubic-bezier(.22,1,.36,1)' }).onfinish = refresh;
      }
    });
  });

  /* ---------- Case evaluation form ---------- */
  document.querySelectorAll('form[data-evaluation]').forEach((form) => {
    const status = form.querySelector('.form__status');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const data = Object.fromEntries(new FormData(form).entries());
      const endpoint = form.dataset.endpoint;
      if (endpoint) {
        status.textContent = 'Sending your request…';
        try {
          const res = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
          if (!res.ok) throw new Error(String(res.status));
          form.reset();
          status.textContent = 'Thank you. An attorney will contact you soon.';
        } catch (err) {
          status.textContent = 'Your request did not go through. Please call (954) 523-7774.';
        }
        return;
      }
      const body = `Name: ${data.name}\nEmail: ${data.email}\nPhone: ${data.phone}\nPractice area: ${data.area || ''}\n\n${data.message}`;
      window.location.href = `mailto:info@floridajusticefirm.com?subject=${encodeURIComponent('Free case evaluation request')}&body=${encodeURIComponent(body)}`;
      status.textContent = 'Your email app is opening with your request ready to send.';
    });
  });

  /* ---------- Start ---------- */
  // Start as soon as the display face is ready; never wait on films or maps.
  const fontsReady = (document.fonts && document.fonts.ready) ? document.fonts.ready : Promise.resolve();
  Promise.race([fontsReady, new Promise((r) => setTimeout(r, 800))]).then(intro);
  // If animation frames are not running (hidden tab, prerender, link preview), show everything statically.
  if (hasGsap && !reduced) {
    let frames = 0;
    const count = () => { frames += 1; };
    gsap.ticker.add(count);
    setTimeout(() => {
      gsap.ticker.remove(count);
      if (frames > 5) return;
      doc.classList.remove('is-loading');
      doc.classList.add('no-motion');
      document.querySelectorAll('.reveal-line > span, [data-hero-fade], .tile, .person, .curtain__panel').forEach((el) => {
        el.style.transform = el.classList.contains('curtain__panel') ? 'scaleY(0)' : 'none';
        el.style.opacity = '';
        el.style.clipPath = 'none';
      });
      document.querySelectorAll('.manifesto__text .w').forEach((w) => { w.style.opacity = 1; });
    }, 2500);
  }
  setTimeout(() => {
    if (doc.classList.contains('is-loading')) {
      doc.classList.remove('is-loading');
      if (hasGsap && panel) gsap.set(panel, { scaleY: 0 });
      heroIn();
    }
  }, 4500);
})();
