#!/usr/bin/env python3
"""Build angel-number pages from content/angels/*.json.

Writes:
  angel-numbers/<n>/index.html   for each JSON file
  angel-numbers/index.html       hub with search + all live numbers
  angel-numbers/numbers.json     list used by the search box
  sitemap.xml                    adds/updates angel-number URLs
Run from the repo root:  python3 tools/build_angels.py
"""
import json, os, re, html, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://keepseeingnumbers.com"
os.chdir(ROOT)

# Pages that existed before this generator (hand-made); keep their files, list them in the hub.
LEGACY = {
    "000": "Infinite potential", "111": "New beginnings", "222": "Balance and harmony",
    "333": "Creativity and support", "444": "Stability and protection", "555": "Change and freedom",
    "666": "Rebalance and care", "777": "Luck and spiritual growth", "888": "Abundance and success",
    "999": "Completion and release", "1111": "Awakening and alignment", "1212": "Growth and positive momentum",
    "1010": "Spiritual awakening", "1234": "Step-by-step progress", "2222": "Harmony and faith",
}

DIGITS = {
    "0": "potential and new cycles", "1": "new beginnings and independence", "2": "balance and partnership",
    "3": "creativity and expression", "4": "structure and steady work", "5": "change and freedom",
    "6": "home, care and responsibility", "7": "reflection and inner wisdom", "8": "abundance and personal power",
    "9": "completion and compassion",
}

def esc(s):
    return html.escape(s, quote=True)

def root_line(n):
    if n in ("11", "22", "33"):
        r = str(sum(int(d) for d in n))
        return f"{'+'.join(n)} = {r} (kept as master number {n})"
    if set(n) == {"0"}:
        return "0 (zero has no root: pure potential)"
    parts, cur = [], n
    while len(cur) > 1:
        s = str(sum(int(d) for d in cur))
        parts.append(f"{'+'.join(cur)} = {s}")
        cur = s
        if cur in ("11", "22"):
            parts.append(f"kept as master number {cur}")
            break
    return ", ".join(parts)

def root_of(n):
    if n in ("11", "22", "33"):
        return n
    cur = n
    while len(cur) > 1:
        cur = str(sum(int(d) for d in cur))
        if cur in ("11", "22"):
            break
    return cur

STYLE = open("angel-numbers/444/index.html", encoding="utf-8").read().split("<style>")[1].split("</style>")[0]
STYLE += (".facts{width:100%;border-collapse:collapse;margin:6px 0 22px;font-size:14px}"
          ".facts td{border-bottom:1px solid rgba(255,255,255,.08);padding:9px 4px;vertical-align:top}"
          ".facts td:first-child{color:var(--mute);width:38%}"
          ".asearch{display:flex;gap:8px;margin:8px 0 6px}"
          ".asearch input{flex:1;min-width:0;background:#000;border:1px solid rgba(255,204,102,.45);color:var(--ink);border-radius:999px;padding:14px 20px;font:inherit;font-size:16px}"
          ".asearch button{border:0;border-radius:999px;padding:0 22px;font-weight:800;letter-spacing:2px;color:#000;background:linear-gradient(90deg,#ffd27a,#ff9a3c);cursor:pointer}"
          "#aout{font-size:15px;margin-top:8px}#aout .card{border:1px solid var(--line);border-radius:16px;padding:16px;margin-top:10px;background:rgba(255,204,102,.04)}"
          ".updated{font-size:12px;color:var(--mute);margin-top:26px}"
          ".hubsec{margin-top:30px}")

HEAD_TAIL = ('<meta name="google-adsense-account" content="ca-pub-6114034797382677">\n'
             '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6114034797382677" crossorigin="anonymous"></script>\n'
             '<meta name="p:domain_verify" content="e557ff94ff2ae544cc8be2c93fc00e20"/>')

HEADER = ('<header><a class="logo" href="/"><i></i>KEEP SEEING NUMBERS</a><nav><a href="/angel-numbers/">Angel Numbers</a>'
          '<a href="/life-path/">Life Path</a><a href="/numerology-2027/">2027</a><a href="/journal/">Journal</a></nav></header>')

FOOTER = ('<footer><a href="/">Free Life Path reading</a><a href="/angel-numbers/">Angel numbers</a><a href="/life-path/">Life Path numbers</a>'
          '<a href="/numerology-2027/">Numerology 2027</a><br><br><a href="/about/">About</a><a href="/contact/">Contact</a>'
          '<a href="/privacy/">Privacy Policy</a><a href="/terms/">Terms</a><a href="/disclaimer/">Disclaimer</a><br><br>'
          'For self-reflection and entertainment. Numbers are a map, not a verdict. © 2026 Keep Seeing Numbers</footer>')

SEARCH = ('<form class="asearch" action="/angel-numbers/" method="get" role="search" onsubmit="return ksnSearch(event)">'
          '<input name="q" id="aq" inputmode="numeric" autocomplete="off" placeholder="Type a number, e.g. 1717 or 11:11" aria-label="Search angel numbers">'
          '<button type="submit">Search</button></form><div id="aout" aria-live="polite"></div>'
          '<script src="/js/angel-search.js" defer></script>')

def head(title, desc, url, extra_ld):
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in extra_ld)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="article"><meta property="og:site_name" content="Keep Seeing Numbers">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&family=Cormorant+Garamond:wght@700&display=swap" rel="stylesheet">
<style>{STYLE}</style>
{ld}{HEAD_TAIL}
</head>
<body>
{HEADER}
"""

def keyword_of(n, pages):
    if n in pages:
        return pages[n]["keyword"]
    return LEGACY.get(n, "")

def build_page(p, pages, live):
    n = p["number"]
    url = f"{SITE}/angel-numbers/{n}/"
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    art_ld = {"@context": "https://schema.org", "@type": "Article", "headline": re.sub("<[^>]+>", "", p["h1"]),
              "description": p["desc"], "datePublished": p["published"], "dateModified": p["modified"],
              "author": {"@type": "Organization", "name": "Keep Seeing Numbers", "url": SITE + "/about/"},
              "publisher": {"@type": "Organization", "name": "Keep Seeing Numbers",
                            "logo": {"@type": "ImageObject", "url": SITE + "/favicon.png"}},
              "image": SITE + "/og.png", "mainEntityOfPage": url, "inLanguage": "en"}
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Angel Numbers", "item": SITE + "/angel-numbers/"},
        {"@type": "ListItem", "position": 3, "name": n, "item": url}]}
    core = sorted(set(n), key=n.index)
    core_txt = "; ".join(f"{d} = {DIGITS[d]}" for d in core)
    r = root_of(n)
    facts = (f'<table class="facts"><tr><td>Number</td><td>{n}</td></tr>'
             f'<tr><td>Core digit meaning</td><td>{esc(core_txt)}</td></tr>'
             f'<tr><td>Root number</td><td>{esc(root_line(n))}</td></tr>'
             f'<tr><td>Key message</td><td>{esc(p["keyword"])}</td></tr>'
             f'<tr><td>Where people see it</td><td>{esc(p["clock"])}</td></tr></table>')
    body = "".join(f"<h2>{esc(h)}</h2>{c}" for h, c in p["sections"])
    steps = "".join(f"<li>{esc(s)}</li>" for s in p["steps"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in p["faq"])
    rel = "".join(f'<a href="/angel-numbers/{x}/"><b>{x}</b><span>{esc(keyword_of(x, pages))}</span></a>'
                  for x in p["related"] if x in live)
    pub = datetime.date.fromisoformat(p["modified"]).strftime("%B %-d, %Y")
    out = head(p["title"], p["desc"], url, [art_ld, faq_ld, bc_ld])
    out += f"""<main><div class="crumbs"><a href="/">Home</a> › <a href="/angel-numbers/">Angel Numbers</a> › {n}</div><div class="big">{n}</div><span class="tag">{esc(p["tag"])}</span>
<h1>{p["h1"]}</h1>
<p class="lead">{esc(p["lead"])}</p>
<h2>{n} at a glance</h2>{facts}
{body}
<h2>What should I do when I see {n}?</h2>
<ol class="steps">{steps}</ol>
<p>A simple habit that works with any number: when {n} appears, write down what you were thinking in that exact moment. After a week or two, read the list back. The pattern in your own notes says more than any general meaning can.</p>
<h2>What does {n} mean for 2027?</h2>{p["y2027"]}
<div class="cta"><h2>What is <em style="color:var(--gold);font-style:normal">your</em> 2027 number?</h2><p>Enter your birthday and get your 2027 Personal Year number in 10 seconds. Free.</p><a class="btn" href="/numerology-2027/">Find my 2027 number</a></div>
<h2>Frequently asked questions about {n}</h2><div class="faq">{faq}</div>
<h2>Look up another number</h2>{SEARCH}
<h2>Related angel numbers</h2><div class="grid">{rel}</div>
<p class="updated">Updated {pub}. Meanings follow traditional Pythagorean numerology. They are for reflection and entertainment, not a prediction or professional advice.</p>
</main>
{FOOTER}
</body></html>"""
    os.makedirs(f"angel-numbers/{n}", exist_ok=True)
    open(f"angel-numbers/{n}/index.html", "w", encoding="utf-8").write(out)

def sort_key(n):
    rep = len(set(n)) == 1
    return (0 if rep and len(n) >= 3 else 1 if n in ("11", "22", "33") else 2, len(n), int(n))

def build_hub(pages, live):
    url = SITE + "/angel-numbers/"
    faqs = [
        ("What are angel numbers?", "Angel numbers are repeating number sequences, like 111, 444 or 11:11, that people notice again and again. In numerology each digit has its own meaning, and repetition is read as that meaning turned up."),
        ("How do I look up an angel number?", "Type the number into the search box on this page. Times work too: type 11:11 or 1111. If we have a full guide, you go straight to it; if not, you get a quick digit-by-digit reading."),
        ("How are angel number meanings worked out?", "Each digit from 0 to 9 has a traditional meaning in Pythagorean numerology. A sequence is read from its digits, how often they repeat, and its root number: the single digit you get by adding the digits together."),
        ("Are angel numbers real?", "There is no scientific evidence that numbers carry messages. Many people use them as a prompt for reflection: a moment to pause and notice what they are thinking and feeling."),
    ]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Angel Numbers", "item": url}]}
    nums = sorted(live, key=sort_key)
    list_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Angel number meanings",
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/angel-numbers/{n}/", "name": f"Angel number {n}"}
                                   for i, n in enumerate(nums)]}
    groups = [("Repeating numbers", [n for n in nums if len(set(n)) == 1 and len(n) >= 3]),
              ("Master numbers", [n for n in nums if n in ("11", "22", "33")]),
              ("Patterns and sequences", [n for n in nums if not (len(set(n)) == 1 and len(n) >= 3) and n not in ("11", "22", "33")])]
    secs = ""
    for name, items in groups:
        if not items:
            continue
        tiles = "".join(f'<a href="/angel-numbers/{n}/"><b>{n}</b><span>{esc(keyword_of(n, pages))}</span></a>' for n in items)
        secs += f'<div class="hubsec"><h2>{name}</h2><div class="grid">{tiles}</div></div>'
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
    title = "Angel Numbers: Look Up Any Number's Meaning | Keep Seeing Numbers"
    desc = "Search any angel number and read what it means in numerology: 0000, 1111, 4444, 11, 22 and more. Love, money, twin flames and what to do next."
    out = head(title, desc, url, [faq_ld, bc_ld, list_ld])
    out += f"""<main><div class="crumbs"><a href="/">Home</a> › Angel Numbers</div><h1>Angel Numbers: <em>Look Up Any Number</em></h1>
<p class="lead">Keep seeing the same number? Type it below to read what it means in numerology: for love, money, twin flames and your next step.</p>
{SEARCH}
{secs}
<div class="cta"><h2>What is <em style="color:var(--gold);font-style:normal">your</em> 2027 number?</h2><p>Enter your birthday and get your 2027 Personal Year number in 10 seconds. Free.</p><a class="btn" href="/numerology-2027/">Find my 2027 number</a></div>
<h2>Frequently asked questions</h2><div class="faq">{faq}</div></main>
{FOOTER}
</body></html>"""
    open("angel-numbers/index.html", "w", encoding="utf-8").write(out)
    json.dump({n: keyword_of(n, pages) for n in nums}, open("angel-numbers/numbers.json", "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))

def update_sitemap(pages, live):
    sm = open("sitemap.xml", encoding="utf-8").read()
    today = max(p["modified"] for p in pages.values())
    for n in sorted(pages):
        loc = f"{SITE}/angel-numbers/{n}/"
        entry = f"<url><loc>{loc}</loc><lastmod>{pages[n]['modified']}</lastmod></url>"
        if f"<loc>{loc}</loc>" in sm:
            sm = re.sub(rf"<url><loc>{re.escape(loc)}</loc><lastmod>[^<]*</lastmod></url>", entry, sm)
        else:
            sm = sm.replace("</urlset>", entry + "\n</urlset>")
    hub = f"{SITE}/angel-numbers/"
    sm = re.sub(rf"<url><loc>{re.escape(hub)}</loc><lastmod>[^<]*</lastmod></url>",
                f"<url><loc>{hub}</loc><lastmod>{today}</lastmod></url>", sm)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)

def main():
    # Only pages whose publish date has arrived (Baku time) are built.
    today = os.environ.get("KSN_TODAY") or (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)).date().isoformat()
    pages = {}
    for f in sorted(glob.glob("content/angels/*.json")):
        p = json.load(open(f, encoding="utf-8"))
        if p.get("published", "0000") <= today:
            pages[p["number"]] = p
    live = set(LEGACY) | set(pages)
    for p in pages.values():
        build_page(p, pages, live)
    build_hub(pages, live)
    update_sitemap(pages, live)
    print(f"built {len(pages)} pages, hub lists {len(live)} numbers")

if __name__ == "__main__":
    main()
