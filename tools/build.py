"""Generates the Brilio HTML pages, sitemap.xml and robots.txt.

Run from the repo root after editing: python3 tools/build.py .
"""
import json, sys, os, re

OUT = sys.argv[1]
SITE = "https://www.brilioclean.com"
PHONE = "(773) 766-5661"
TEL = "+17737665661"
EMAIL = "info@brilioclean.com"
HOURS = "Daily, 6 AM – midnight"

SERVICES = [
    ("residential-cleaning", "Residential cleaning"),
    ("short-term-rental-cleaning", "Short-term rental (STR) cleaning"),
    ("commercial-cleaning", "Office & commercial"),
    ("floor-care", "Floor care (strip, wax, buff)"),
    ("post-construction-cleaning", "Post-construction cleaning"),
    ("move-out-cleaning", "Move-in / move-out cleaning"),
    ("deep-cleaning", "Deep cleaning"),
    ("linen-rental-laundry", "Linen rental &amp; laundry (STR)"),
]

PRIMETIME = "Primetime Window Cleaners"
PRIMETIME_QUOTE = "https://primetimewindowcleaning.com/contact/"

STAR = '<svg class="star" aria-hidden="true"><use href="#star"/></svg>'


def logo_svg():
    """Inline wordmark from brand/brilio-logo.svg; the lettering follows the text color so it works in dark mode."""
    src = open(os.path.join(OUT, "brand", "brilio-logo.svg")).read()
    src = src.replace('fill="#0d2233"', 'fill="currentColor"').replace("<title>Brilio</title>", "")
    src = re.sub(r' width="\d+" height="\d+"', "", src, count=1)
    return src.replace("<svg ", '<svg class="logo-mark" role="img" aria-label="Brilio" ', 1).strip()


def head(title, desc, path, extra=""):
    url = SITE + path
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0d2233">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Brilio">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap">
<link rel="stylesheet" href="/styles.css">
{extra}</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="star" viewBox="-10 -10 20 20"><path d="M0,-10 C1.2,-3 3,-1.2 10,0 C3,1.2 1.2,3 0,10 C-1.2,3 -3,1.2 -10,0 C-3,-1.2 -1.2,-3 0,-10Z"/></symbol>
</svg>
'''


def header(active=""):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<header class="site">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Brilio home">{logo_svg()}</a>
    <nav class="main" aria-label="Main">
      {link("/residential-cleaning", "Residential", "residential-cleaning")}
      {link("/short-term-rental-cleaning", "Short-Term Rentals", "short-term-rental-cleaning")}
      {link("/commercial-cleaning", "Commercial", "commercial-cleaning")}
      {link("/floor-care", "Floor Care", "floor-care")}
      <a href="/#more-services">More Services</a>
    </nav>
    <div class="hdr-right">
      <a class="hdr-phone" href="tel:{TEL}">{PHONE}</a>
      <a class="btn" href="#quote">Free quote</a>
    </div>
  </div>
</header>
'''


def quote(selected, heading="Tell us about your space.", sub="Send us a few details and we’ll get back to you with a price. Commercial and floor jobs start with a free walkthrough."):
    opts = "\n".join(
        f'            <option{" selected" if slug == selected else ""}>{label}</option>' for slug, label in SERVICES
    )
    return f'''  <section class="block" id="quote" style="padding-top:24px">
    <div class="wrap quote">
      <div>
        <div class="head" style="margin-bottom:0">
          <p class="eyebrow">Free quote</p>
          <h2>{heading}</h2>
          <p>{sub}</p>
        </div>
        <div class="contact-lines">
          <div><span class="lbl">Call or text</span><a class="val" href="tel:{TEL}">{PHONE}</a></div>
          <div><span class="lbl">Email</span><a class="val" href="mailto:{EMAIL}">{EMAIL}</a></div>
          <div><span class="lbl">Hours</span><span class="val">{HOURS}</span></div>
        </div>
      </div>
      <form class="qf" id="quoteForm" action="https://formsubmit.co/ajax/df6a463ea6c9df99f22c3e2976bc7e55" method="POST" novalidate>
        <input type="hidden" name="_subject" value="New quote request from brilioclean.com">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <div class="hp" aria-hidden="true"><label for="q-honey">Leave this empty</label><input id="q-honey" name="_honey" tabindex="-1" autocomplete="off"></div>
        <div class="field"><label for="q-name">Name</label><input id="q-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" placeholder="(773) 000-0000"></div>
        <div class="field"><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email" placeholder="you@example.com"></div>
        <div class="field"><label for="q-zip">ZIP code</label><input id="q-zip" name="zip" inputmode="numeric" maxlength="5" autocomplete="postal-code"></div>
        <div class="field full"><label for="q-service">Service</label>
          <select id="q-service" name="service">
{opts}
          </select>
        </div>
        <div class="field full"><label for="q-details">Details <span class="req">(size of space, how often, preferred dates)</span></label><textarea id="q-details" name="details"></textarea></div>
        <button class="btn sky" type="submit">Request my quote</button>
        <p class="ok" id="quoteOk" role="status" hidden>Thanks! We got your request and will be in touch soon. Need us sooner? Call or text {PHONE}.</p>
        <p class="err" id="quoteErr" role="alert" hidden></p>
      </form>
    </div>
  </section>
'''


def footer():
    return f'''<footer class="site">
  <div class="wrap">
    <a class="logo logo-sm" href="/" aria-label="Brilio home">{logo_svg()}</a>
    <div class="contact">
      <a href="tel:{TEL}">{PHONE}</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <span>{HOURS}</span>
    </div>
    <span>Serving Illinois, Indiana &amp; Wisconsin · © 2026 Brilio</span>
  </div>
</footer>
<script src="/site.js"></script>
</body>
</html>
'''


def checklist(groups):
    out = []
    for title, items in groups:
        lis = "".join(f"<li>{i}</li>" for i in items)
        out.append(f'<div class="group"><h3>{title}</h3><ul>{lis}</ul></div>')
    return '<div class="checklist">' + "".join(out) + "</div>"


def faq(items):
    return '<div class="faq">' + "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items
    ) + "</div>"


def others(current):
    links = "".join(
        f'<a class="btn ghost" href="/{slug}">{label}</a>' for slug, label in SERVICES + [("window-cleaning", "Window cleaning")] if slug != current
    )
    return f'''  <section class="block" style="padding-top:0">
    <div class="wrap">
      <div class="head" style="margin-bottom:20px"><p class="eyebrow">Other services</p><h2>Need something else cleaned?</h2></div>
      <div class="other-services">{links}</div>
    </div>
  </section>
'''


FLOOR_STEPS = '''      <ol class="steps">
        <li><span class="n">Step 1</span><h3>Strip</h3><p>Remove old, yellowed finish down to the bare tile.</p></li>
        <li><span class="n">Step 2</span><h3>Rinse &amp; neutralize</h3><p>Clear stripper residue so the new finish bonds.</p></li>
        <li><span class="n">Step 3</span><h3>Seal</h3><p>Lay a base coat to fill pores in the tile.</p></li>
        <li><span class="n">Step 4</span><h3>Finish coats</h3><p>Apply several thin coats of floor finish, drying between each.</p></li>
        <li><span class="n">Step 5</span><h3>Burnish</h3><p>Use a high-speed burnisher for a hard, wet-look shine.</p></li>
      </ol>
      <div class="floors" aria-label="Floor types">
        <span>VCT</span><span>Sheet vinyl</span><span>LVT</span><span>Terrazzo</span><span>Sealed concrete</span><span>Ceramic tile</span>
      </div>'''

TICKET = '''      <article class="ticket" aria-label="Example short-term rental turnover schedule">
        <header>
          <div>
            <p class="eyebrow">Same-day turnover</p>
            <h3>2BR rental · Wicker Park</h3>
          </div>
          <span class="chip done">On time</span>
        </header>
        <ol class="timeline">
          <li><time>11:00 AM</time><span>Guest checks out</span><span class="chip">Checkout</span></li>
          <li><time>11:30 AM</time><span>Linens stripped, laundry started</span><span class="chip done">Done</span></li>
          <li><time>12:15 PM</time><span>Kitchen, baths, floors reset</span><span class="chip done">Done</span></li>
          <li><time>1:45 PM</time><span>Restock + photo report to host</span><span class="chip done">Sent</span></li>
          <li><time>4:00 PM</time><span>Next guest checks in</span><span class="chip">Ready</span></li>
        </ol>
        <footer><span>Damage &amp; supply notes included</span><span>~2 hr 45 min</span></footer>
        <p class="note">Example schedule</p>
      </article>'''

STATS = '''  <section class="stats-band" aria-label="Brilio by the numbers">
    <div class="wrap stats">
      <div class="stat"><b>72,000+</b><span>short-term rental and residential cleanings completed</span></div>
      <div class="stat"><b>7 days</b><span>a week, from 6 AM to midnight</span></div>
      <div class="stat"><b>3 states</b><span>served: Illinois, Indiana, and Wisconsin</span></div>
      <div class="stat"><b>24-hour</b><span>re-clean guarantee on every visit</span></div>
    </div>
  </section>
'''
STATS_PAGES = ("short-term-rental-cleaning", "residential-cleaning", "linen-rental-laundry")

TRUST = f'''<div class="trust">
          <span>{STAR}Insured &amp; bonded</span>
          <span>{STAR}24-hour re-clean guarantee</span>
          <span>{STAR}Open daily, 6 AM – midnight</span>
        </div>'''

LD = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Brilio",
    "url": SITE,
    "telephone": TEL,
    "email": EMAIL,
    "description": "Residential, short-term rental, commercial, post-construction, and floor care cleaning.",
    "address": {"@type": "PostalAddress", "addressLocality": "Chicago", "addressRegion": "IL", "addressCountry": "US"},
    "areaServed": [{"@type": "State", "name": s} for s in ("Illinois", "Indiana", "Wisconsin")],
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "06:00", "closes": "23:59",
    }],
}


def home():
    ld = f'<script type="application/ld+json">{json.dumps(LD)}</script>\n'
    return head(
        "Brilio | House, Short-Term Rental, Office &amp; Floor Cleaning in Chicago",
        "Brilio is a Chicago cleaning company offering residential cleaning, short-term rental (STR) turnovers, office and commercial cleaning, and floor stripping, waxing, and buffing. Insured and bonded. Free quotes.",
        "/", ld,
    ) + header() + f'''
<main id="top">
  <section class="hero">
    <div class="wrap">
      <div>
        <h1>Every space, <em>brilliantly</em> clean.</h1>
        <p class="lede">Brilio cleans homes, short-term rentals, offices, new construction, and commercial floors. Based in Chicago and serving Illinois, Indiana, and Wisconsin.</p>
        <div class="ctas">
          <a class="btn sky" href="#quote">Get a free quote</a>
          <a class="btn ghost" href="tel:{TEL}">Call {PHONE}</a>
        </div>
        {TRUST}
      </div>

{TICKET}
    </div>
  </section>

{STATS}
  <section class="block" id="services">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">What we clean</p>
        <h2>Every kind of clean, one standard.</h2>
        <p>Pick what you need. Every visit follows a written checklist, so you get the same result whichever crew shows up.</p>
      </div>
      <div class="services">
        <article class="svc">
          <p class="tag">Homes &amp; apartments</p>
          <h3>Residential cleaning</h3>
          <p>Weekly, biweekly, or one-time cleans for condos, apartments, and houses.</p>
          <ul><li>Standard and deep cleans</li><li>Move-in / move-out cleaning</li><li>Inside oven, fridge, and cabinets on request</li></ul>
          <a class="more" href="/residential-cleaning">Residential cleaning</a>
        </article>
        <article class="svc">
          <p class="tag">Hosts &amp; property managers</p>
          <h3>Short-term rental cleaning</h3>
          <p>Everything an STR needs between guests: turnovers, linens, restocking, inspections, and photo reports.</p>
          <ul><li>Same-day guest turnovers</li><li>Linen rental, laundry, and restocking</li><li>Inspections and damage reporting</li></ul>
          <a class="more" href="/short-term-rental-cleaning">STR cleaning services</a>
        </article>
        <article class="svc">
          <p class="tag">Offices &amp; commercial</p>
          <h3>Office &amp; commercial cleaning</h3>
          <p>Early-morning, evening, or weekend cleaning for offices, retail, clinics, and common areas.</p>
          <ul><li>Nightly, weekly, or custom schedules</li><li>Restrooms, break rooms, trash and recycling</li><li>High-touch surface disinfecting</li></ul>
          <a class="more" href="/commercial-cleaning">Commercial cleaning</a>
        </article>
        <article class="svc">
          <p class="tag">Hard floors</p>
          <h3>Commercial floor care</h3>
          <p>Stripping, waxing, buffing, and burnishing for VCT, vinyl, and other hard floors.</p>
          <ul><li>Full strip &amp; wax</li><li>Scrub-and-recoat between strips</li><li>Routine buffing and burnishing</li></ul>
          <a class="more" href="/floor-care">Floor care</a>
        </article>
      </div>
    </div>
  </section>

  <section class="block" id="more-services" style="padding-top:0">
    <div class="wrap">
      <div class="head" style="margin-bottom:24px">
        <p class="eyebrow">More services</p>
        <h2>Specialty services</h2>
      </div>
      <div class="mini-services">
        <a class="mini" href="/post-construction-cleaning"><h3>Post-construction cleaning</h3><p>Dust and debris removed after a renovation or new build, so the space is ready to use.</p></a>
        <a class="mini" href="/move-out-cleaning"><h3>Move-in / move-out cleaning</h3><p>Empty homes and apartments cleaned top to bottom for tenants, landlords, and sellers.</p></a>
        <a class="mini" href="/linen-rental-laundry"><h3>Linen rental &amp; laundry</h3><p>Fresh sheets and towels for every stay, or your own linens washed and folded. For short-term rentals.</p></a>
        <a class="mini" href="/deep-cleaning"><h3>Deep cleaning</h3><p>Detailed top-to-bottom cleaning for a first visit, a new season, or a fresh start.</p></a>
        <a class="mini" href="/window-cleaning"><h3>Window cleaning</h3><p>Provided by our partner company, Primetime Window Cleaners.</p></a>
      </div>
    </div>
  </section>

  <section class="block band" id="floors">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Floor care</p>
        <h2>How a strip &amp; wax works</h2>
        <p>We work early mornings, evenings, or weekends, so your floors are dry and walkable before you open.</p>
      </div>
{FLOOR_STEPS}
    </div>
  </section>

  <section class="block" id="areas">
    <div class="wrap split">
      <div>
        <div class="head" style="margin-bottom:28px">
          <p class="eyebrow">Why Brilio</p>
          <h2>Clean you can check.</h2>
        </div>
        <div class="why">
          <div>{STAR}<div><h3>Same crew, same checklist</h3><p>Recurring clients get a consistent team and a written list of what gets done each visit.</p></div></div>
          <div>{STAR}<div><h3>Photo proof for hosts</h3><p>Every rental turnover ends with photos, so you can see the unit is guest-ready from anywhere.</p></div></div>
          <div>{STAR}<div><h3>24-hour re-clean guarantee</h3><p>If something was missed, tell us within 24 hours and we’ll come back to fix it at no charge.</p></div></div>
          <div>{STAR}<div><h3>Insured &amp; bonded</h3><p>Your home, rental, or business is protected while we work.</p></div></div>
        </div>
      </div>
      <div>
        <div class="head" style="margin-bottom:28px">
          <p class="eyebrow">Service area</p>
          <h2>Based in Chicago, serving three states</h2>
        </div>
        <div class="states">
          <div class="state"><b>Illinois</b><span>Chicago headquarters</span></div>
          <div class="state"><b>Indiana</b><span>All services</span></div>
          <div class="state"><b>Wisconsin</b><span>All services</span></div>
        </div>
        <p class="areas-note">Not sure if we cover your address? Call or text <a href="tel:{TEL}">{PHONE}</a> and we’ll tell you right away.</p>
      </div>
    </div>
  </section>

{quote("")}
</main>
''' + footer()


def service_page(slug, title, desc, eyebrow, h1, lede, body, faqs):
    return head(title, desc, "/" + slug) + header(slug) + f'''
<main id="top">
  <section class="page-hero">
    <div class="wrap">
      <p class="crumbs"><a href="/">Home</a> / {eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
      <div class="ctas">
        <a class="btn sky" href="#quote">Get a free quote</a>
        <a class="btn ghost" href="tel:{TEL}">Call {PHONE}</a>
      </div>
      {TRUST}
    </div>
  </section>
{STATS if slug in STATS_PAGES else ""}{body}
  <section class="block">
    <div class="wrap">
      <div class="head"><p class="eyebrow">Questions</p><h2>Frequently asked</h2></div>
      {faq(faqs)}
    </div>
  </section>
{quote(slug)}
{others(slug)}
</main>
''' + footer()


def section(eyebrow, h2, p, inner, cls="block", style=""):
    st = f' style="{style}"' if style else ""
    para = f"<p>{p}</p>" if p else ""
    return f'''  <section class="{cls}"{st}>
    <div class="wrap">
      <div class="head"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2>{para}</div>
      {inner}
    </div>
  </section>
'''


PAGES = {
    "residential-cleaning": service_page(
        "residential-cleaning",
        "House &amp; Apartment Cleaning in Chicago | Brilio",
        "Recurring, one-time, deep, and move-in/move-out house cleaning in Chicago and across Illinois, Indiana, and Wisconsin. Insured and bonded with a 24-hour re-clean guarantee.",
        "Residential cleaning",
        "House cleaning that fits your schedule.",
        "Weekly, biweekly, monthly, or one-time cleaning for apartments, condos, and houses. We’re open every day from 6 AM to midnight, so you can book a time that works around yours.",
        section("What’s included", "Every room, on a checklist", "A standard clean covers the rooms below. Choose a deep clean or add extras when you need more.", checklist([
            ("Kitchen", ["Counters, backsplash, and sink", "Stovetop and outside of appliances", "Cabinet fronts and handles", "Floors swept and mopped"]),
            ("Bathrooms", ["Toilet, tub, and shower scrubbed", "Sinks, mirrors, and fixtures", "Floors and baseboards", "Trash emptied"]),
            ("Bedrooms &amp; living areas", ["Dusting of surfaces and decor", "Beds made (linen change on request)", "Vacuuming and mopping", "Light switches and door handles wiped"]),
            ("Deep clean &amp; extras", ["Inside oven and fridge", "Inside cabinets and drawers", "Baseboards and window sills", "Move-in / move-out cleaning"]),
        ])),
        [
            ("How often should I schedule a cleaning?", "Most homes do well with biweekly cleaning. Busy households or homes with pets often choose weekly. We also do one-time and deep cleans whenever you need them."),
            ("What’s the difference between a standard and a deep clean?", "A standard clean keeps a home in good shape. A deep clean adds detailed work like baseboards, inside appliances, and built-up grime. We recommend a deep clean for your first visit or before a move."),
            ("What if I’m not happy with something?", "Let us know within 24 hours and we’ll come back to re-clean it at no charge."),
            ("Are you insured?", "Yes. Brilio is insured and bonded."),
        ],
    ),
    "short-term-rental-cleaning": service_page(
        "short-term-rental-cleaning",
        "Short-Term Rental (STR) Cleaning in Chicago | Brilio",
        "Short-term and vacation rental cleaning in Chicago and across Illinois, Indiana, and Wisconsin: same-day turnovers, linen and laundry, restocking, inspections, and photo reports for hosts and property managers.",
        "Short-term rental cleaning",
        "Short-term rental cleaning, from checkout to five stars.",
        "With more than 72,000 short-term rental and residential cleanings behind us, we know what a five-star stay takes. We handle the cleaning side of your short-term rental: turnovers between guests, linens, restocking, inspections, and a photo report after every visit. We work every day from 6 AM to midnight, so tight same-day turnovers and last-minute bookings are covered.",
        f'''  <section class="block" style="padding-top:8px">
    <div class="wrap split" style="align-items:start">
      <div>
        <div class="head"><p class="eyebrow">Guest turnovers</p><h2>Every turnover covers</h2></div>
        {checklist([
            ("Guest-ready clean", ["Kitchen, bathrooms, and floors", "Dishes washed and put away", "Patios, balconies, and grills wiped down", "Trash and recycling out"]),
            ("Linens &amp; staging", ["Beds stripped and remade", "Fresh towels staged", "Welcome items and guidebook set out"]),
            ("Restock &amp; report", ["Toiletries, coffee, and paper goods restocked", "Photos sent to you after each clean", "Damage or missing items flagged"]),
        ])}
      </div>
{TICKET}
    </div>
  </section>
''' + section("STR services", "Everything your rental needs between guests", "Book turnovers on their own, or let us take care of the whole cleaning side of your listing.", checklist([
            ("Same-day turnovers", ["Cleaning between checkout and check-in", "Last-minute and back-to-back bookings", "Weekends and holidays included"]),
            ("Linen rental &amp; laundry", ["Rent our linens: we pick up, drop off, and change them", "Mattress protectors available", "Or we wash, dry, and fold your own linens", '<a href="/linen-rental-laundry">See linen rental &amp; laundry</a>']),
            ("Restocking &amp; supplies", ["Guest essentials restocked every visit", "Low-supply alerts before you run out", "Supply runs on request"]),
            ("Inspections &amp; damage reports", ["Pre-arrival checks before guests arrive", "Photos of damaged items and furniture", "Photos of damage to windows, doors, handles, bathrooms, and walls", "Missing items and lost-and-found logged"]),
            ("Deep cleans", ["Periodic deep cleans between bookings", "Inside appliances, baseboards, and vents", "Window cleaning through our partner company"]),
            ("Mid-stay &amp; new listings", ["Mid-stay cleans for longer bookings", "Launch cleans for new listings", "Photo-ready staging before listing photos"]),
        ])) + section("How it works", "Set up once, cleaned after every stay", "", '''<ol class="steps steps-light">
        <li><span class="n">Step 1</span><h3>Walkthrough</h3><p>We visit the property and build a checklist for your unit and your standards.</p></li>
        <li><span class="n">Step 2</span><h3>Share your calendar</h3><p>Send us your booking calendar so we can schedule a turnover after every checkout.</p></li>
        <li><span class="n">Step 3</span><h3>We clean</h3><p>Our team resets the unit, handles linens, and restocks supplies.</p></li>
        <li><span class="n">Step 4</span><h3>You get a report</h3><p>Photos of the finished unit, plus notes on damage, maintenance, and low supplies.</p></li>
      </ol>''') + section("Who we work with", "For one listing or a whole portfolio", "", '''<div class="states">
        <div class="state"><b>Hosts &amp; co-hosts</b><span>One unit or several, self-managed</span></div>
        <div class="state"><b>Property managers</b><span>Scheduled turnovers across a portfolio</span></div>
        <div class="state"><b>Vacation &amp; mid-term rentals</b><span>Weekly stays, monthly stays, and corporate housing</span></div>
      </div>'''),
        [
            ("Can you do same-day turnovers?", "Yes. We work from 6 AM to midnight every day, so we can fit a turnover between an 11 AM checkout and a 4 PM check-in, including weekends and holidays."),
            ("How do you know when to clean?", "Share your booking calendar with us and we schedule a turnover after every checkout. We also take one-off and last-minute requests by phone or text."),
            ("Do you restock supplies?", "Yes. We restock toiletries, paper goods, and kitchen basics from the supplies you keep at the property, and let you know before anything runs out."),
            ("Will I know when the unit is ready?", "Yes. After each turnover we send you photos of the finished unit. If anything is damaged, from linens and furniture to windows, doors, handles, bathrooms, or walls, we send you photos of that too."),
            ("What happens if a guest leaves something behind?", "We log it, send you a photo, and keep it safe at the property or with us until you tell us what to do with it."),
            ("Do you work with property managers who have several units?", "Yes. Tell us how many units you manage and how often they turn over, and we’ll set up a schedule and a checklist for each property."),
        ],
    ),
    "commercial-cleaning": service_page(
        "commercial-cleaning",
        "Office &amp; Commercial Cleaning in Chicago | Brilio",
        "Office and commercial cleaning in Chicago and across Illinois, Indiana, and Wisconsin. Early-morning, evening, and weekend schedules for offices, retail, clinics, and common areas.",
        "Office &amp; commercial cleaning",
        "Office and commercial cleaning, done before you open.",
        "We clean offices, retail spaces, clinics, and building common areas on your schedule, from 6 AM to midnight, seven days a week. Every new client starts with a free walkthrough and a written cleaning plan.",
        section("What’s included", "A plan built around your space", "We agree on the tasks and how often each one happens at your walkthrough. Here’s what a typical plan covers.", checklist([
            ("Workspaces", ["Desks and work surfaces wiped", "Trash and recycling emptied", "Vacuuming and mopping", "Glass doors and partitions"]),
            ("Restrooms", ["Toilets, urinals, and sinks sanitized", "Mirrors and fixtures", "Soap, paper towels, and toilet paper refilled", "Floors mopped and disinfected"]),
            ("Break rooms &amp; kitchens", ["Counters, sinks, and tables", "Outside of microwave and fridge", "Dishes and coffee area tidied"]),
            ("Common areas", ["Lobbies and entrances", "Hallways and stairwells", "High-touch disinfecting: handles, rails, elevator buttons"]),
        ])),
        [
            ("When do you clean?", "Whenever it works for your business. We’re available from 6 AM to midnight, seven days a week, so we can clean before you open, after you close, or on weekends."),
            ("How do you price commercial cleaning?", "We start with a free walkthrough of your space, then send a quote based on its size, the tasks you need, and how often you want us to come."),
            ("Can you also take care of our floors?", "Yes. We strip, wax, buff, and burnish hard floors, and can add floor care to your regular cleaning plan."),
            ("Are you insured?", "Yes. Brilio is insured and bonded."),
        ],
    ),
    "floor-care": service_page(
        "floor-care",
        "Floor Stripping, Waxing &amp; Buffing in Chicago | Brilio",
        "Commercial floor care in Chicago and across Illinois, Indiana, and Wisconsin: floor stripping and waxing, scrub and recoat, buffing, and burnishing for VCT, vinyl, LVT, and more.",
        "Floor care",
        "Floor stripping, waxing, and buffing.",
        "We restore and maintain hard floors in offices, stores, schools, and common areas. We work early mornings, evenings, or weekends so your floors are ready when you open.",
        section("Services", "Pick the level your floors need", "", checklist([
            ("Strip &amp; wax", ["Old finish fully removed", "Floor sealed and refinished", "Best for dull, yellowed, or damaged finish"]),
            ("Scrub &amp; recoat", ["Top layers of finish scrubbed off", "Fresh coats applied", "Extends the time between full strips"]),
            ("Buffing &amp; burnishing", ["High-speed polish of the existing finish", "Restores shine between recoats", "Can be scheduled weekly or monthly"]),
        ])) + section("The process", "How a strip &amp; wax works", "", "\n" + FLOOR_STEPS, cls="block band"),
        [
            ("How long until we can walk on the floor?", "It depends on the number of coats and the conditions in the space. We’ll give you a timeline at the walkthrough and schedule the work so the floor is ready before you open."),
            ("How often do floors need to be stripped and waxed?", "Busy commercial floors usually need a full strip and wax once or twice a year, with scrub-and-recoat and regular burnishing in between to keep the shine."),
            ("What types of floors do you work on?", "VCT, sheet vinyl, LVT, terrazzo, sealed concrete, and ceramic tile. If you’re not sure what you have, we’ll check at the walkthrough."),
            ("Is the walkthrough free?", "Yes. We look at your floors, recommend a plan, and send you a quote at no cost."),
        ],
    ),
    "post-construction-cleaning": service_page(
        "post-construction-cleaning",
        "Post-Construction Cleaning in Chicago | Brilio",
        "Post-construction and renovation cleaning in Chicago and across Illinois, Indiana, and Wisconsin. Dust, debris, and residue removed so new and remodeled spaces are ready for move-in.",
        "Post-construction cleaning",
        "Post-construction cleaning, ready for move-in.",
        "After a renovation or new build, we remove the dust, debris, and residue the work leaves behind. We clean homes, offices, retail build-outs, and new units for builders, contractors, property managers, and owners.",
        section("What’s included", "From rough clean to final clean", "We can clean once at the end of a project, or in phases as the trades finish.", checklist([
            ("Rough clean", ["Leftover debris and packaging cleared", "Floors swept and vacuumed throughout", "Stickers and labels removed from fixtures and windows"]),
            ("Dust removal", ["Walls, ledges, and door frames", "Vent covers, light fixtures, and ceiling fans", "Inside cabinets, closets, and drawers"]),
            ("Final clean", ["Windows and glass cleaned inside", "Paint, caulk, and adhesive spots removed from hard surfaces", "Kitchens and bathrooms detailed", "Hard floors scrubbed, and finished or burnished if needed"]),
        ])),
        [
            ("When should we schedule the cleaning?", "Book the final clean for when the trades have finished their work. On bigger projects we can also do a rough clean between phases, then a final clean before handover."),
            ("Do you work with contractors and builders?", "Yes. We work with general contractors, builders, property managers, and homeowners. Tell us your handover date and we’ll plan around it."),
            ("Can you refinish the floors too?", "Yes. Our floor care team can scrub, seal, wax, and burnish hard floors as part of the final clean."),
            ("How is post-construction cleaning priced?", "It depends on the size of the space and how much dust and debris is left. We do a free walkthrough and then send you a quote."),
        ],
    ),
    "move-out-cleaning": service_page(
        "move-out-cleaning",
        "Move-In &amp; Move-Out Cleaning in Chicago | Brilio",
        "Move-in and move-out cleaning in Chicago and across Illinois, Indiana, and Wisconsin for tenants, landlords, property managers, buyers, and sellers.",
        "Move-in / move-out cleaning",
        "Move-in and move-out cleaning.",
        "Moving is enough work. We clean empty homes and apartments top to bottom, inside every cabinet and appliance, so the next people walk into a spotless space. We work with tenants, landlords, property managers, and realtors.",
        section("What’s included", "Every surface of an empty home", "", checklist([
            ("Kitchen", ["Inside the oven, fridge, and microwave", "Inside all cabinets and drawers", "Counters, backsplash, sink, and stovetop", "Floors scrubbed"]),
            ("Bathrooms", ["Toilet, tub, shower, and glass scrubbed", "Inside vanities and medicine cabinets", "Mirrors, fixtures, and floors"]),
            ("Every room", ["Baseboards, doors, and door frames", "Light switches and outlets wiped", "Closets and shelves", "Window sills and tracks", "Floors vacuumed and mopped"]),
        ])),
        [
            ("Does the home need to be empty?", "It’s best if it is. With furniture and boxes gone, we can reach every corner, cabinet, and baseboard."),
            ("Can you clean on the same day as the move?", "Often, yes. We’re open every day from 6 AM to midnight, so we can usually fit a cleaning in after the movers leave."),
            ("Do you work with landlords and property managers?", "Yes. We can clean units between tenants on a regular basis. Tell us how many units you manage."),
            ("What if something was missed?", "Tell us within 24 hours and we’ll come back to re-clean it at no charge."),
        ],
    ),
    "deep-cleaning": service_page(
        "deep-cleaning",
        "Deep House Cleaning in Chicago | Brilio",
        "Deep cleaning for homes and apartments in Chicago and across Illinois, Indiana, and Wisconsin. Detailed top-to-bottom cleaning of kitchens, bathrooms, and every room.",
        "Deep cleaning",
        "Deep cleaning for a fresh start.",
        "A deep clean goes past the everyday surfaces to the grime that builds up over time. It’s the right choice for a first cleaning, a seasonal refresh, or before and after hosting guests.",
        section("What’s included", "Everything in a standard clean, plus", "", checklist([
            ("Kitchen", ["Stovetop and backsplash degreased", "Inside the microwave", "Inside the oven and fridge on request", "Cabinet fronts and handles detailed"]),
            ("Bathrooms", ["Grout scrubbed", "Soap scum and hard-water buildup removed", "Shower glass and fixtures descaled", "Behind and around the toilet"]),
            ("Whole home", ["Baseboards and door frames", "Vents, ceiling fans, and light fixtures", "Window sills and blinds", "Under and behind furniture we can move"]),
        ])),
        [
            ("How is a deep clean different from a standard clean?", "A standard clean keeps a home in good shape. A deep clean adds the detail work, like baseboards, grout, vents, and built-up grime, so it takes longer."),
            ("How often do I need a deep clean?", "Many homes get one every three to six months, with standard cleans in between. We also recommend one for your first visit with us."),
            ("Do I need to be home?", "No. Many clients leave a key or door code. Tell us what works for you when you book."),
            ("What if I’m not happy with something?", "Tell us within 24 hours and we’ll come back to re-clean it at no charge."),
        ],
    ),
    "linen-rental-laundry": service_page(
        "linen-rental-laundry",
        "Linen Rental &amp; Laundry for Short-Term Rentals in Chicago | Brilio",
        "Linen rental and laundry service for short-term rental hosts and property managers in Chicago and across Illinois, Indiana, and Wisconsin. Fresh sheets and towels for every stay, or your own linens washed and folded.",
        "Linen rental &amp; laundry",
        "Linen rental and laundry for short-term rentals.",
        "Skip buying, storing, and washing linens. When you rent linens from us, we handle everything: pickup, laundry, drop-off, and changing the beds. You don’t lift a finger. Prefer your own linens? We’ll wash and fold those too.",
        section("What you get", "Rent ours or we wash yours", "", checklist([
            ("Linen rental, fully hands-off", ["Sheets, pillowcases, duvet covers, and towels supplied by us", "Mattress protectors available", "We pick up, drop off, and change the linens", "Stained or worn items replaced by us"]),
            ("Laundry service", ["Your own bedding and towels washed, dried, and folded", "Stains pre-treated", "Sorted and packed by unit", "Damaged items flagged before they reach a guest"]),
            ("Damage checks every visit", ["Unit inspected each time we change linens", "Photos of damaged linens and furniture", "Photos of damage to windows, doors, handles, bathrooms, and walls", "Sent to you right away"]),
        ])) + section("How linen rental works", "Fresh linens, every stay", "", '''<ol class="steps steps-light">
        <li><span class="n">Step 1</span><h3>Tell us your units</h3><p>Share the bed sizes and bathrooms at each property.</p></li>
        <li><span class="n">Step 2</span><h3>We set your sets</h3><p>We work out how many linen sets each unit needs for your booking pace.</p></li>
        <li><span class="n">Step 3</span><h3>We change the beds</h3><p>We bring fresh linens, make the beds, stage the towels, and take the used set with us.</p></li>
        <li><span class="n">Step 4</span><h3>Report and wash</h3><p>You get photos of any damage in the unit. Every linen is washed, checked, and replaced if it’s stained or worn.</p></li>
      </ol>''') + section("Why hosts rent linens", "Less to buy, store, and wash", "", '''<div class="states">
        <div class="state"><b>No upfront cost</b><span>No buying sets for every bed in every unit</span></div>
        <div class="state"><b>Nothing for you to do</b><span>We pick up, wash, drop off, and change the linens</span></div>
        <div class="state"><b>Eyes on your unit</b><span>Photos of any damage after every visit</span></div>
        <div class="state"><b>Consistent for guests</b><span>Matching, inspected linens in every unit, every stay</span></div>
      </div>'''),
        [
            ("Can I use linen rental or laundry without your cleaning service?", "Yes. You can use linen rental or laundry on its own, or combine it with our turnover cleaning so the beds are made for you."),
            ("What’s included in a linen set?", "Sheets, pillowcases, duvet covers, and towels sized for your unit. Mattress protectors are available too. We put together the right set for each property when you sign up."),
            ("Do I need to do anything when I rent linens?", "No. We pick up the used linens, wash them, drop off fresh sets, and change the beds ourselves. You don’t have to handle any laundry."),
            ("What if something in the unit is damaged?", "We check the unit every time we’re there. If we find damaged linens, furniture, or damage to the unit itself, like windows, doors, handles, bathrooms, or walls, we send you photos right away."),
            ("Do you work with property managers?", "Yes. We set up linen sets and laundry schedules across all the units you manage."),
            ("How is it priced?", "It depends on the number of units, bed sizes, and how often they turn over. Request a quote and we’ll send you pricing."),
        ],
    ),
    "window-cleaning": head(
        "Window Cleaning | Primetime Window Cleaners, a Brilio Partner",
        "Window cleaning for Brilio clients is provided by our partner company, Primetime Window Cleaners. Request a window cleaning quote from Primetime.",
        "/window-cleaning",
    ) + header() + f'''
<main id="top">
  <section class="page-hero">
    <div class="wrap">
      <p class="crumbs"><a href="/">Home</a> / Window cleaning</p>
      <h1>Window cleaning by our partner company.</h1>
      <p class="lede">Window cleaning is handled by <b>{PRIMETIME}</b>, Brilio’s partner company. Request your window cleaning quote directly from them, and they’ll take it from there.</p>
      <div class="ctas">
        <a class="btn sky" href="{PRIMETIME_QUOTE}" target="_blank" rel="noopener">Get a window cleaning quote from Primetime</a>
      </div>
    </div>
  </section>
{others("window-cleaning")}
</main>
''' + footer(),
}

open(os.path.join(OUT, "index.html"), "w").write(home())
for slug, html in PAGES.items():
    open(os.path.join(OUT, slug + ".html"), "w").write(html)

urls = ["/"] + ["/" + s for s, _ in SERVICES] + ["/window-cleaning"]
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n"
)
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print("built", len(PAGES) + 1, "pages")
