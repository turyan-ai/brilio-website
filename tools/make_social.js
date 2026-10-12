const { chromium } = require('playwright'); const fs = require('fs');
const B = '/home/user/brilio-website/brand', OUT = B + '/marketing';
const uri = f => 'data:image/svg+xml;base64,' + fs.readFileSync(`${B}/${f}`).toString('base64');
const NAVY = '#0d2233', SKY = '#41b6e6', MIST = '#9cb8ca', LIGHT = '#f6f9fb';
const SPARK = c => `<svg viewBox="-10 -10 20 20" style="width:34px;height:34px;flex:none"><path fill="${c}" d="M0,-10 C1.2,-3 3,-1.2 10,0 C3,1.2 1.2,3 0,10 C-1.2,3 -3,1.2 -10,0 C-3,-1.2 -1.2,-3 0,-10Z"/></svg>`;
const base = (bg, fg, body, footLogo, footColor) => `<!doctype html><html><head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap">
<style>*{box-sizing:border-box}body{margin:0}
.c{width:1080px;height:1080px;background:${bg};color:${fg};font-family:'Plus Jakarta Sans',sans-serif;padding:90px;display:flex;flex-direction:column}
.eyebrow{font-size:30px;font-weight:700;letter-spacing:.16em;color:${SKY}}
h1{font-size:96px;line-height:1.02;font-weight:800;letter-spacing:-.03em;margin:28px 0 0}
.sub{font-size:38px;line-height:1.35;font-weight:500;margin-top:30px;opacity:.85}
ul{list-style:none;padding:0;margin:56px 0 0;display:grid;gap:26px}
li{display:flex;gap:22px;align-items:center;font-size:40px;font-weight:600}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;color:${footColor};font-size:30px;font-weight:600}
.foot img{height:92px}</style></head><body><div class="c" id="c">${body}
<div class="foot"><img src="${footLogo}"><span>brilioclean.com</span></div></div></body></html>`;

const posts = {
  'brilio-post-str': base(NAVY, '#fff', `<div class="eyebrow">SHORT-TERM RENTAL HOSTS</div>
    <h1>Same-day turnovers, done right.</h1>
    <ul>${['Cleaning and restocking', 'Linen rental and laundry', 'Damage photos after every clean', 'Open daily, 6 AM to midnight'].map(t => `<li>${SPARK(SKY)}${t}</li>`).join('')}</ul>`,
    uri('brilio-logo-white.svg'), MIST),
  'brilio-post-72000': base(LIGHT, NAVY, `<div class="eyebrow">BY THE NUMBERS</div>
    <div style="font-size:250px;font-weight:800;letter-spacing:-.05em;color:${SKY};line-height:1;margin-top:70px">72,000+</div>
    <div style="font-size:56px;font-weight:700;line-height:1.2;margin-top:34px;letter-spacing:-.01em">short-term rental and residential cleanings completed.</div>`,
    uri('brilio-logo.svg'), '#4d6475'),
  'brilio-post-linen': base(SKY, NAVY, `<div class="eyebrow" style="color:#fff">FOR SHORT-TERM RENTALS</div>
    <h1>Fresh linens. Zero laundry.</h1>
    <div class="sub">Rent our linens and we handle everything: pickup, washing, drop-off, and making the beds.</div>
    <div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:54px">${['Sheets', 'Pillowcases', 'Duvet covers', 'Towels', 'Mattress protectors'].map(t => `<span style="background:#fff;border-radius:999px;padding:14px 28px;font-size:32px;font-weight:700">${t}</span>`).join('')}</div>`,
    uri('brilio-logo.svg'), NAVY),
  'brilio-post-services': base('#ffffff', NAVY, `<h1 style="margin:0">Every space, <span style="color:${SKY}">brilliantly</span> clean.</h1>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:52px">${['Residential', 'Short-term rentals', 'Commercial', 'Floor care', 'Post-construction', 'Move-in / move-out'].map(t => `<div style="border:3px solid #d6e2ea;border-radius:22px;padding:28px 26px;font-size:33px;font-weight:700;display:flex;gap:16px;align-items:center;white-space:nowrap">${SPARK(SKY)}${t}</div>`).join('')}</div>
    <div style="margin:40px 0 44px;font-size:30px;font-weight:600;color:#4d6475">Insured and bonded · 24-hour re-clean guarantee</div>`,
    uri('brilio-logo.svg'), '#4d6475'),
  'brilio-post-postconstruction': base(NAVY, '#fff', `<div class="eyebrow">POST-CONSTRUCTION CLEANING</div>
    <h1>Renovation done? We'll make it move-in ready.</h1>
    <ul>${['Dust and debris removed', 'Vents, ledges, and fixtures', 'Floors scrubbed and finished', 'Free walkthrough and quote'].map(t => `<li>${SPARK(SKY)}${t}</li>`).join('')}</ul>`,
    uri('brilio-logo-white.svg'), MIST),
};
const cover = (w, h, logoW) => `<!doctype html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600&display=swap">
<style>body{margin:0}.c{width:${w}px;height:${h}px;background:${NAVY};display:grid;place-items:center;font-family:'Plus Jakarta Sans',sans-serif}</style></head>
<body><div class="c" id="c"><div style="display:grid;justify-items:center;gap:${Math.round(h * .06)}px">
<img src="${uri('brilio-logo-white.svg')}" style="width:${logoW}px">
<div style="color:${MIST};font-size:${Math.round(h * .05)}px;font-weight:600">Homes · Short-term rentals · Commercial · Floor care</div>
<div style="color:${SKY};font-size:${Math.round(h * .042)}px;font-weight:600;letter-spacing:.16em">BRILIOCLEAN.COM</div></div></div></body></html>`;
const covers = { 'brilio-facebook-cover': [1640, 624, 460], 'brilio-google-cover': [1600, 900, 600] };
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1700, height: 1100 } });
  for (const [name, html] of Object.entries(posts)) { await p.setContent(html, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    const ov = await p.evaluate(() => { const c = document.getElementById('c'); return c.scrollHeight > c.clientHeight + 1; });
    await p.locator('#c').screenshot({ path: `${OUT}/${name}.png` }); console.log(name, ov ? 'OVERFLOW' : 'ok'); }
  for (const [name, [w, h, lw]] of Object.entries(covers)) { await p.setContent(cover(w, h, lw), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    await p.locator('#c').screenshot({ path: `${OUT}/${name}.png` }); console.log(name, `${w}x${h}`); }
  const img = f => 'data:image/png;base64,' + fs.readFileSync(`${OUT}/${f}.png`).toString('base64');
  await p.setViewportSize({ width: 1400, height: 900 });
  await p.setContent(`<body style="margin:0;padding:12px;background:#ccc;display:flex;flex-wrap:wrap;gap:12px">${Object.keys(posts).map(n => `<img src="${img(n)}" style="width:260px">`).join('')}${Object.keys(covers).map(n => `<img src="${img(n)}" style="height:240px">`).join('')}</body>`);
  await p.screenshot({ path: 'social-sheet.png', fullPage: true }); await b.close(); })();
