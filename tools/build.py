#!/usr/bin/env python3
"""Build angel-number pages, hub page and sitemap from tools/numbers.json.

Usage: python3 tools/build.py
"""
import html
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://keepseeingnumbers.com"
DATA = json.load(open(os.path.join(ROOT, "tools", "numbers.json"), encoding="utf-8"))
TODAY = date.today().isoformat()

CSS = """
:root{--gold:#ffcc66;--gold2:#ff9a3c;--ink:#f4efe6;--mute:#a59f93;--card:#0d0b09;--line:rgba(255,204,102,.18)}
*{margin:0;padding:0;box-sizing:border-box}
html{background:#000}
body{font-family:Montserrat,system-ui,sans-serif;color:var(--ink);background:#000;min-height:100vh;overflow-x:hidden}
#stars{position:fixed;inset:0;z-index:0;pointer-events:none}
.wrap{position:relative;z-index:1;max-width:680px;margin:0 auto;padding:22px 22px 80px}
nav.top{display:flex;justify-content:space-between;align-items:center;font-size:11px;letter-spacing:3px;text-transform:uppercase;white-space:nowrap;gap:12px}
nav.top a{color:var(--mute);text-decoration:none}
nav.top a.brand{color:var(--ink)}
.crumbs{font-size:12px;color:var(--mute);margin-top:22px}
.crumbs a{color:var(--mute)}
.eclipse{position:relative;width:200px;height:200px;margin:40px auto 26px}
.eclipse .corona{position:absolute;inset:-56px;border-radius:50%;background:radial-gradient(circle,#fff 38%,#ffd27a 44%,rgba(255,138,42,.28) 58%,rgba(255,90,0,0) 72%);animation:breathe 4s ease-in-out infinite}
.eclipse .disk{position:absolute;inset:0;border-radius:50%;background:#000;display:flex;align-items:center;justify-content:center;font-weight:300;font-size:54px;letter-spacing:2px;color:var(--gold)}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
h1{font-family:"Cormorant Garamond",serif;font-weight:700;font-size:42px;line-height:1.1;text-align:center}
h1 em{color:var(--gold);font-style:italic}
.kw{text-align:center;color:var(--gold);font-size:12px;letter-spacing:5px;text-transform:uppercase;margin-top:12px}
.tag{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:24px;text-align:center;margin:18px auto 0;max-width:480px;line-height:1.3}
.intro{color:#d9d2c5;line-height:1.75;font-size:16px;margin-top:30px}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px 22px;margin-top:14px}
.card h2{font-size:12px;letter-spacing:4px;text-transform:uppercase;color:var(--gold);margin-bottom:10px;font-weight:700}
.card p{line-height:1.7;font-size:15.5px;color:#e6e0d4}
.steps{list-style:none;counter-reset:s}
.steps li{counter-increment:s;display:flex;gap:14px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.07);line-height:1.55;font-size:15.5px}
.steps li:last-child{border:0}
.steps li:before{content:counter(s);flex:0 0 30px;height:30px;border-radius:50%;border:1px solid var(--gold);color:var(--gold);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
h2.sec{font-family:"Cormorant Garamond",serif;font-size:30px;margin:40px 0 6px}
details{border-bottom:1px solid rgba(255,255,255,.08);padding:16px 0}
summary{cursor:pointer;font-weight:700;font-size:15.5px;list-style:none}
summary::-webkit-details-marker{display:none}
summary:after{content:"+";float:right;color:var(--gold)}
details[open] summary:after{content:"\\2212"}
details p{margin-top:10px;line-height:1.7;color:#d9d2c5;font-size:15px}
.cta{margin-top:40px;border:1px solid var(--line);border-radius:22px;padding:26px 22px;text-align:center;background:radial-gradient(ellipse at top,rgba(255,170,70,.14),transparent 70%),#050403}
.cta h2{font-family:"Cormorant Garamond",serif;font-size:30px;line-height:1.15}
.cta p{color:var(--mute);margin:10px 0 18px;line-height:1.6;font-size:15px}
.btn{display:inline-block;border-radius:999px;padding:15px 28px;font:800 14px Montserrat;letter-spacing:3px;text-transform:uppercase;color:#000;background:linear-gradient(90deg,#ffd27a,var(--gold2));text-decoration:none}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.chips a{border:1px solid var(--line);border-radius:999px;padding:10px 18px;color:var(--ink);text-decoration:none;font-weight:700;letter-spacing:2px}
.chips a:hover{border-color:var(--gold);color:var(--gold)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px;margin-top:24px}
.grid a{display:block;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 14px;text-decoration:none;color:var(--ink);text-align:center}
.grid a b{display:block;font-size:30px;font-weight:300;color:var(--gold);letter-spacing:2px}
.grid a span{display:block;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--mute);margin-top:6px}
.grid a:hover{border-color:var(--gold)}
.search{width:100%;margin-top:26px;background:#000;border:1px solid rgba(255,255,255,.18);color:var(--ink);border-radius:999px;padding:15px 20px;font:inherit;font-size:16px}
.search:focus{outline:none;border-color:var(--gold)}
.foot{text-align:center;color:#6d675e;font-size:11px;margin-top:50px;line-height:1.7}
.foot a{color:#8d867b}
"""

STARS_JS = """(function(){const s=document.getElementById('stars');const w=innerWidth,h=Math.max(innerHeight,1200);s.setAttribute('viewBox',`0 0 ${w} ${h}`);let out='';for(let i=0;i<120;i++){out+=`<circle cx="${Math.random()*w}" cy="${Math.random()*h}" r="${(Math.random()*1.4+.3).toFixed(2)}" fill="#fff" opacity="${(Math.random()*.7+.15).toFixed(2)}"/>`}s.innerHTML=out})();"""

e = html.escape


def head(title, desc, path, jsonld):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700;800&family=Cormorant+Garamond:ital,wght@0,500;0,700;1,500&display=swap" rel="stylesheet">
<style>{CSS}</style>
{''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)}
</head>
<body>
<svg id="stars" aria-hidden="true"></svg>
<div class="wrap">
<nav class="top"><a class="brand" href="/">Keep Seeing Numbers</a><a href="/angel-numbers/">All numbers</a></nav>
"""


def foot():
    return f"""<div class="foot">Numerology is a symbolic practice for reflection, not a prediction or professional advice.<br>
<a href="/">Free Life Path reading</a> · <a href="/angel-numbers/">Angel numbers</a> · Instagram <a href="https://www.instagram.com/keepseeingnumbers/">@keepseeingnumbers</a></div>
</div>
<script>{STARS_JS}</script>
</body>
</html>
"""


def number_page(n, d):
    path = f"/angel-number/{n}/"
    title = f"Angel Number {n} Meaning: {d['keyword']}, Love & What to Do Next"
    desc = f"Keep seeing {n}? Here is what angel number {n} means in numerology, in love, career and money, plus 3 simple steps to take today."
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    art_ld = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
              "dateModified": TODAY, "author": {"@type": "Organization", "name": "Keep Seeing Numbers"},
              "publisher": {"@type": "Organization", "name": "Keep Seeing Numbers"}, "mainEntityOfPage": SITE + path}
    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Angel numbers", "item": SITE + "/angel-numbers/"},
        {"@type": "ListItem", "position": 3, "name": f"Angel number {n}", "item": SITE + path}]}
    disp = f"{n[:2]}:{n[2:]}" if len(n) == 4 else n
    out = head(title, desc, path, [art_ld, faq_ld, crumb_ld])
    out += f"""<div class="crumbs"><a href="/">Home</a> / <a href="/angel-numbers/">Angel numbers</a> / {n}</div>
<div class="eclipse"><div class="corona"></div><div class="disk">{e(disp)}</div></div>
<h1>Angel Number <em>{n}</em> Meaning</h1>
<div class="kw">{e(d['keyword'])}</div>
<p class="tag">{e(d['tagline'])}</p>
<p class="intro">{e(d['intro'])}</p>
<div class="card"><h2>What {n} means</h2><p>{e(d['meaning'])}</p></div>
<div class="card"><h2>{n} in love</h2><p>{e(d['love'])}</p></div>
<div class="card"><h2>{n} in career</h2><p>{e(d['career'])}</p></div>
<div class="card"><h2>{n} and money</h2><p>{e(d['money'])}</p></div>
<h2 class="sec">What to do when you see {n}</h2>
<div class="card"><ol class="steps">{''.join(f'<li>{e(s)}</li>' for s in d['steps'])}</ol></div>
<div class="cta"><h2>Which number are <em style="color:var(--gold)">you</em>?</h2>
<p>Your Life Path number shapes how signs like {n} show up for you. Get your free reading in 10 seconds.</p>
<a class="btn" href="/">Get my free reading</a></div>
<h2 class="sec">Questions about {n}</h2>
{''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d['faq'])}
<h2 class="sec">Related numbers</h2>
<div class="chips">{''.join(f'<a href="/angel-number/{r}/">{r}</a>' for r in d['related'] if r in DATA)}</div>
"""
    out += foot()
    return path, out


def hub_page():
    path = "/angel-numbers/"
    title = "Angel Numbers Meaning: The Complete Guide to Repeating Numbers"
    desc = "Keep seeing 111, 222 or 11:11? Find the meaning of every repeating number, in love, career and money, with simple steps for each."
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc, "url": SITE + path}
    out = head(title, desc, path, [ld])
    items = "".join(f'<a href="/angel-number/{n}/" data-n="{n}"><b>{n}</b><span>{e(d["keyword"])}</span></a>' for n, d in sorted(DATA.items(), key=lambda x: (len(x[0]), x[0])))
    out += f"""<div class="eclipse"><div class="corona"></div><div class="disk">∞</div></div>
<h1>Angel <em>Numbers</em></h1>
<p class="tag">The numbers that keep finding you, and what to do about them.</p>
<p class="intro">Seeing the same number again and again, on a clock, a receipt or a licence plate, is one of the most common experiences people describe in numerology. Each repeating number carries its own message. Pick yours below.</p>
<input class="search" id="q" type="search" inputmode="numeric" placeholder="Type the number you keep seeing…" aria-label="Search numbers">
<div class="grid" id="grid">{items}</div>
<div class="cta"><h2>Start with <em style="color:var(--gold)">your</em> number</h2>
<p>Your Life Path number is the lens every other sign is read through.</p>
<a class="btn" href="/">Get my free reading</a></div>
<script>document.getElementById('q').addEventListener('input',function(){{const v=this.value.replace(/[^0-9]/g,'');document.querySelectorAll('#grid a').forEach(a=>{{a.style.display=!v||a.dataset.n.includes(v)?'':'none'}})}});</script>
"""
    out += foot()
    return path, out


def write(path, content):
    fp = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)


def main():
    paths = ["/"]
    p, c = hub_page(); write(p, c); paths.append(p)
    for n, d in DATA.items():
        p, c = number_page(n, d); write(p, c); paths.append(p)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in paths)
    sm += "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(paths), "urls")


if __name__ == "__main__":
    main()
