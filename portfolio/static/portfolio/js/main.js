(function () {
  const d = document;

  // Year in footer
  const yearEl = d.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  // Dark mode toggle (persisted)
  const root = d.documentElement;
  const toggle = d.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) root.setAttribute('data-theme', savedTheme);
  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', current);
      localStorage.setItem('theme', current);
      toggle.setAttribute('aria-pressed', String(current === 'dark'));
    });
  }

  // Consent banner + analytics load
  const banner = d.getElementById('consent-banner');
  const accepted = localStorage.getItem('consent') === 'true';
  if (banner && !accepted) banner.hidden = false;
  const acceptBtn = d.getElementById('consent-accept');
  const declineBtn = d.getElementById('consent-decline');
  if (acceptBtn) acceptBtn.addEventListener('click', () => {
    localStorage.setItem('consent', 'true');
    banner.hidden = true;
    if (typeof window.enableAnalytics === 'function') window.enableAnalytics();
  });
  if (declineBtn) declineBtn.addEventListener('click', () => {
    localStorage.setItem('consent', 'false');
    banner.hidden = true;
  });

  // IntersectionObserver reveal
  const ro = 'IntersectionObserver' in window ? new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('is-visible');
        ro.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 }) : null;
  d.querySelectorAll('[data-io-reveal] .card').forEach((el) => {
    el.classList.add('reveal');
    if (ro) ro.observe(el);
  });

  // Client-side project search (title contains)
  const projSearch = d.getElementById('projectSearch');
  if (projSearch) {
    projSearch.addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      d.querySelectorAll('#projectGrid .project-card').forEach((card) => {
        const title = card.getAttribute('data-title');
        card.style.display = !q || (title && title.includes(q)) ? '' : 'none';
      });
    });
  }

  // Case study overlay (deep-link)
  const overlay = d.getElementById('caseOverlay');
  if (overlay) {
    const closeBtn = overlay.querySelector('.overlay-close');
    closeBtn.addEventListener('click', () => closeOverlay());
    d.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeOverlay(); });

    function openOverlay(html, url) {
      overlay.hidden = false;
      overlay.setAttribute('aria-hidden', 'false');
      d.getElementById('overlayContent').innerHTML = html;
      history.pushState({ overlay: true }, '', url);
      d.getElementById('overlayContent').focus();
    }
    function closeOverlay() {
      overlay.hidden = true;
      overlay.setAttribute('aria-hidden', 'true');
      if (history.state && history.state.overlay) history.back();
    }
    d.querySelectorAll('.case-link').forEach((a) => {
      a.addEventListener('click', (ev) => {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
        ev.preventDefault();
        const url = a.getAttribute('href');
        fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
          .then((r) => r.text())
          .then((html) => {
            // Extract main content (simple)
            const match = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
            openOverlay(match ? match[1] : html, url);
          }).catch(() => { window.location.href = url; });
      });
    });
    window.addEventListener('popstate', () => {
      if (!(history.state && history.state.overlay)) closeOverlay();
    });
  }

  // Lightbox
  d.querySelectorAll('a.lightbox').forEach((link) => {
    link.addEventListener('click', (e) => {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      e.preventDefault();
      const img = new Image();
      img.src = link.href;
      const viewer = d.createElement('div');
      viewer.className = 'overlay';
      const btn = d.createElement('button');
      btn.className = 'overlay-close';
      btn.textContent = '×';
      const wrap = d.createElement('div');
      wrap.className = 'overlay-content';
      wrap.appendChild(img);
      viewer.appendChild(btn);
      viewer.appendChild(wrap);
      d.body.appendChild(viewer);
      btn.addEventListener('click', () => viewer.remove());
    });
  });

  // Contact AJAX submit
  const contactForm = d.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const status = d.getElementById('contactStatus');
      status.textContent = 'Sending…';
      const fd = new FormData(contactForm);
      // CSRF
      const csrf = d.querySelector('input[name=csrfmiddlewaretoken]').value;
      // Optional reCAPTCHA v3
      const recaptchaScript = d.querySelector('script[src*="recaptcha"]');
      if (recaptchaScript && window.grecaptcha) {
        const siteKey = (new URLSearchParams(recaptchaScript.src.split('?')[1])).get('render');
        try {
          const token = await window.grecaptcha.execute(siteKey, { action: 'submit' });
          fd.set('recaptcha_token', token);
        } catch (_) {}
      }
      fetch(contactForm.action, { method: 'POST', headers: { 'X-CSRFToken': csrf }, body: fd })
        .then(r => r.json().then((body) => ({ ok: r.ok, body })))
        .then(({ ok, body }) => {
          status.textContent = body.message || (ok ? 'Sent!' : 'Error. Try again.');
          if (ok) contactForm.reset();
        })
        .catch(() => { status.textContent = 'Network error. Please try again.'; });
    });
  }

  // Client-side search (instant)
  const blogSearch = d.getElementById('blogSearch');
  if (blogSearch) {
    blogSearch.addEventListener('input', () => {
      const q = blogSearch.value.trim();
      fetch(`/search.json?q=${encodeURIComponent(q)}`)
        .then(r => r.json())
        .then(data => {
          const container = d.getElementById('blogResults');
          if (!container) return;
          container.innerHTML = '';
          (data.posts || []).forEach((p) => {
            const el = d.createElement('article');
            el.className = 'card';
            el.innerHTML = `<a href="${p.url}"><h3>${p.title}</h3><p class="muted">${p.excerpt || ''}</p><p class="muted">${p.readingTime} min read</p></a>`;
            container.appendChild(el);
          });
        });
    });
  }
})();