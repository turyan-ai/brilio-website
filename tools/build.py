"""Generates the Brilio HTML pages, sitemap.xml and robots.txt.

Run from the repo root after editing: python3 tools/build.py .
"""
import json, sys, os

OUT = sys.argv[1]
SITE = "https://brilioclean.com"
PHONE = "(773) 766-5661"
TEL = "+17737665661"
EMAIL = "info@brilioclean.com"
HOURS = "Daily, 6 AM – midnight"

SERVICES = [
    ("residential-cleaning", "Residential cleaning"),
    ("airbnb-cleaning", "Airbnb & short-term rentals"),
    ("commercial-cleaning", "Office & commercial"),
    ("floor-care", "Floor care (strip, wax, buff)"),
]

STAR = '<svg class="star" aria-hidden="true"><use href="#star"/></svg>'


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
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap">
<link rel="stylesheet" href="/styles.css">
{extra}</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="star" viewBox="-10 -10 20 20"><polygon points="0,-10 2.25,-3.9 8.66,-5 4.5,0 8.66,5 2.25,3.9 0,10 -2.25,3.9 -8.66,5 -4.5,0 -8.66,-5 -2.25,-3.9"/></symbol>
</svg>
'''


def header(active=""):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<header class="site">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Brilio home">{STAR}brilio</a>
    <nav class="main" aria-label="Main">
      {link("/residential-cleaning", "Residential", "residential-cleaning")}
      {link("/airbnb-cleaning", "Airbnb", "airbnb-cleaning")}
      {link("/commercial-cleaning", "Commercial", "commercial-cleaning")}
      {link("/floor-care", "Floor Care", "floor-care")}
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
    <a class="logo" href="/" style="font-size:1.2rem">{STAR}brilio</a>
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
        f'<a class="btn ghost" href="/{slug}">{label}</a>' for slug, label in SERVICES if slug != current
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

TICKET = '''      <article class="ticket" aria-label="Example Airbnb turnover schedule">
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
    "description": "Residential, Airbnb and short-term rental, commercial, and floor care cleaning.",
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
        "Brilio | House, Airbnb, Office &amp; Floor Cleaning in Chicago",
        "Brilio is a Chicago cleaning company offering residential cleaning, Airbnb and short-term rental turnovers, office and commercial cleaning, and floor stripping, waxing, and buffing. Insured and bonded. Free quotes.",
        "/", ld,
    ) + header() + f'''
<main id="top">
  <section class="hero">
    <div class="wrap">
      <div>
        <p class="eyebrow">Chicago cleaning company</p>
        <h1 style="margin-top:14px">Every space, <em>brilliantly</em> clean.</h1>
        <p class="lede">Brilio cleans homes, Airbnb and short-term rentals, offices, and commercial floors. Based in Chicago and serving Illinois, Indiana, and Wisconsin.</p>
        <div class="ctas">
          <a class="btn sky" href="#quote">Get a free quote</a>
          <a class="btn ghost" href="tel:{TEL}">Call {PHONE}</a>
        </div>
        {TRUST}
      </div>

{TICKET}
    </div>
  </section>

  <section class="block" id="services" style="padding-top:24px">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">What we clean</p>
        <h2>Four services, one standard.</h2>
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
          <h3>Airbnb &amp; short-term rentals</h3>
          <p>Turnovers that fit between checkout and check-in, with a photo report after every clean.</p>
          <ul><li>Linen change and laundry</li><li>Restocking of guest supplies</li><li>Damage and missing-item reporting</li></ul>
          <a class="more" href="/airbnb-cleaning">Airbnb turnovers</a>
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
{body}
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
    "airbnb-cleaning": service_page(
        "airbnb-cleaning",
        "Airbnb &amp; Short-Term Rental Cleaning in Chicago | Brilio",
        "Airbnb and VRBO turnover cleaning in Chicago and across Illinois, Indiana, and Wisconsin. Same-day turnovers, linen changes, restocking, and photo reports for hosts.",
        "Airbnb &amp; short-term rentals",
        "Turnovers done between checkout and check-in.",
        "We reset your rental after every guest: cleaning, linens, restocking, and a photo report so you know it’s ready. With hours from 6 AM to midnight every day, we can handle tight same-day turnovers.",
        f'''  <section class="block" style="padding-top:8px">
    <div class="wrap split" style="align-items:start">
      <div>
        <div class="head"><p class="eyebrow">What’s included</p><h2>Every turnover covers</h2></div>
        {checklist([
            ("Guest-ready clean", ["Kitchen, bathrooms, and floors", "Dishes washed and put away", "Trash and recycling out"]),
            ("Linens &amp; laundry", ["Beds stripped and remade", "Fresh towels staged", "Laundry started or swapped"]),
            ("Restock &amp; report", ["Toiletries, coffee, and paper goods restocked", "Photos sent to you after each clean", "Damage or missing items flagged"]),
        ])}
      </div>
{TICKET}
    </div>
  </section>
''',
        [
            ("Can you do same-day turnovers?", "Yes. We work from 6 AM to midnight every day, so we can fit a turnover between an 11 AM checkout and a 4 PM check-in."),
            ("Do you restock supplies?", "Yes. We restock toiletries, paper goods, and kitchen basics from the supplies you keep at the property, and tell you when you’re running low."),
            ("Will I know when the unit is ready?", "Yes. After each turnover we send you photos of the finished unit, plus notes on any damage or missing items."),
            ("Do you work with property managers who have several units?", "Yes. Tell us how many units you manage and how often they turn over, and we’ll set up a schedule."),
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
}

open(os.path.join(OUT, "index.html"), "w").write(home())
for slug, html in PAGES.items():
    open(os.path.join(OUT, slug + ".html"), "w").write(html)

urls = ["/"] + ["/" + s for s, _ in SERVICES]
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n"
)
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print("built", len(PAGES) + 1, "pages")
