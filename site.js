// Quote form: sends the request to info@brilioclean.com through FormSubmit.
(function () {
  var form = document.getElementById('quoteForm');
  if (!form) return;
  var ok = document.getElementById('quoteOk');
  var err = document.getElementById('quoteErr');
  var btn = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    ok.hidden = true;
    err.hidden = true;

    var name = form.name.value.trim();
    var phone = form.phone.value.trim();
    var email = form.email.value.trim();
    if (!name || (!phone && !email)) {
      err.textContent = 'Please add your name and a phone number or email so we can reach you.';
      err.hidden = false;
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Sending…';
    fetch(form.action, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
      .then(function (r) {
        return r.json().then(function (d) {
          // FormSubmit explains failures (e.g. "This form needs Activation") in d.message.
          if (!r.ok || String(d.success) !== 'true') throw new Error(d.message || 'HTTP ' + r.status);
        });
      })
      .then(function () {
        // Quote request conversion for Google Analytics / Google Ads (only when GA is configured)
        if (window.gtag) window.gtag('event', 'generate_lead', { service: form.service.value });
        form.reset();
        ok.hidden = false;
      })
      .catch(function (e) {
        console.warn('Quote form failed:', e.message);
        err.textContent = 'Your request didn’t go through. ' + form.dataset.fallback;
        err.hidden = false;
      })
      .finally(function () {
        btn.disabled = false;
        btn.textContent = 'Request my quote';
      });
  });
})();
