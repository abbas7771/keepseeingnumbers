#!/usr/bin/env python3
"""Build the Journal from content/journal/*.md.

Each post is Markdown with a small front matter block:

    ---
    title: Beaver Supermoon on November 24, 2026: What It Means
    description: One-sentence summary for search results (150-160 chars).
    date: 2026-11-23
    number: 9
    tags: full moon, portal dates
    ---
    Body in Markdown...

Writes:
  journal/<slug>/index.html   one page per post (slug = file name)
  journal/index.html          the list page
  journal/feed.xml            RSS
  sitemap.xml                 journal URLs refreshed inside the JOURNAL markers
  index.html                  homepage "Latest from the journal" block between markers

Usage: python3 tools/build_journal.py
"""
import datetime
import glob
import html
import json
import os
import re

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://keepseeingnumbers.com"
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6114034797382677" crossorigin="anonymous"></script>'
e = html.escape


def load_posts():
    posts = []
    for fp in sorted(glob.glob(os.path.join(ROOT, "content", "journal", "*.md"))):
        raw = open(fp, encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        if not m:
            raise SystemExit(f"missing front matter: {fp}")
        meta = {}
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
        for req in ("title", "description", "date"):
            if not meta.get(req):
                raise SystemExit(f"{fp}: missing {req}")
        meta["slug"] = os.path.splitext(os.path.basename(fp))[0]
        meta["body"] = m.group(2).strip()
        meta["dt"] = datetime.date.fromisoformat(meta["date"])
        posts.append(meta)
    posts.sort(key=lambda p: (p["dt"], p["slug"]), reverse=True)
    return posts


CSS = """
:root{--gold:#ffcc66;--gold2:#ff9a3c;--ink:#f4efe6;--mute:#a59f93;--card:#0d0b09;--line:rgba(255,204,102,.18)}
*{margin:0;padding:0;box-sizing:border-box}
html{background:#000}
body{font-family:Montserrat,system-ui,sans-serif;color:var(--ink);background:#000;min-height:100vh}
.k-head{position:sticky;top:0;z-index:20;background:rgba(0,0,0,.9);border-bottom:1px solid rgba(255,204,102,.14)}
.k-nav{max-width:1200px;margin:0 auto;padding:16px 24px;display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center;justify-content:space-between}
.k-logo{font-size:12px;letter-spacing:6px;text-transform:uppercase;color:var(--ink);text-decoration:none;font-weight:700}
.k-links{display:flex;flex-wrap:wrap;gap:6px 22px;font-size:13px}
.k-links a{color:#d9d2c5;text-decoration:none}.k-links a:hover{color:var(--gold)}
.k-cta{border:1px solid var(--gold);border-radius:999px;padding:9px 18px;font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--gold);text-decoration:none}
.wrap{max-width:720px;margin:0 auto;padding:40px 22px 40px}
.crumbs{font-size:12px;color:var(--mute)}.crumbs a{color:var(--mute)}
.eyebrow{font-size:12px;letter-spacing:5px;text-transform:uppercase;color:var(--gold);margin-top:28px}
h1{font-family:"Cormorant Garamond",serif;font-weight:700;font-size:46px;line-height:1.08;margin-top:12px}
.lede{font-size:18px;line-height:1.65;color:#d9d2c5;margin-top:18px}
.meta{display:flex;align-items:center;gap:16px;margin-top:24px;padding:16px 0;border-top:1px solid rgba(255,255,255,.08);border-bottom:1px solid rgba(255,255,255,.08);font-size:13px;color:var(--mute)}
.num{width:54px;height:54px;flex:none;border-radius:50%;border:1.5px solid var(--gold);display:flex;align-items:center;justify-content:center;color:var(--gold);font-size:24px;font-weight:300;box-shadow:0 0 24px rgba(255,180,80,.3)}
.post{margin-top:28px;font-size:17px;line-height:1.75;color:#e6e0d4}
.post h2{font-family:"Cormorant Garamond",serif;font-size:32px;line-height:1.15;color:var(--ink);margin:40px 0 12px}
.post h3{font-size:13px;letter-spacing:4px;text-transform:uppercase;color:var(--gold);margin:30px 0 10px}
.post p{margin:0 0 18px}
.post a{color:var(--gold)}
.post ul,.post ol{margin:0 0 18px 22px}.post li{margin:6px 0}
.post strong{color:var(--ink)}
.post blockquote{margin:26px 0;padding:18px 22px;border-radius:16px;background:var(--card);border:1px solid var(--line);font-family:"Cormorant Garamond",serif;font-style:italic;font-size:22px;line-height:1.4}
.post blockquote p{margin:0}
.cta{margin-top:40px;border:1px solid var(--line);border-radius:22px;padding:26px 22px;text-align:center;background:radial-gradient(ellipse at top,rgba(255,170,70,.14),transparent 70%),#050403}
.cta h2{font-family:"Cormorant Garamond",serif;font-size:30px;line-height:1.15}
.cta p{color:var(--mute);margin:10px 0 18px;line-height:1.6;font-size:15px}
.btn{display:inline-block;border-radius:999px;padding:15px 28px;font:800 14px Montserrat;letter-spacing:3px;text-transform:uppercase;color:#000;background:linear-gradient(90deg,#ffd27a,var(--gold2));text-decoration:none}
.more{margin-top:44px}
.more h2{font-family:"Cormorant Garamond",serif;font-size:28px;margin-bottom:8px}
.card{display:block;padding:18px 0;border-top:1px solid rgba(255,204,102,.2);text-decoration:none;color:var(--ink)}
.card small{display:block;color:var(--mute);font-size:12px}
.card b{display:block;margin-top:6px;font-size:18px;line-height:1.35}
.card span{display:block;margin-top:6px;color:#b9b2a5;font-size:14px;line-height:1.55}
.foot{max-width:1200px;margin:60px auto 0;padding:32px 24px;border-top:1px solid rgba(255,204,102,.14);display:flex;flex-wrap:wrap;gap:10px 22px;justify-content:center;font-size:13px}
.foot a{color:#a59f93;text-decoration:none}.foot a:hover{color:var(--gold)}
.note{max-width:1200px;margin:0 auto;padding:0 24px 40px;text-align:center;color:#6d675e;font-size:12px}
@media(max-width:640px){h1{font-size:36px}.post h2{font-size:27px}}
"""


def head(title, desc, path, og_type, jsonld):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Keep Seeing Numbers">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Keep Seeing Numbers Journal" href="{SITE}/journal/feed.xml">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700;800&family=Cormorant+Garamond:ital,wght@0,500;0,700;1,500&display=swap" rel="stylesheet">
<style>{CSS}</style>
{''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)}
{ADSENSE}
</head>
<body>
<header class="k-head"><nav class="k-nav" aria-label="Main">
  <a class="k-logo" href="/">Keep Seeing Numbers</a>
  <div class="k-links"><a href="/#today">Today</a><a href="/angel-numbers/">Angel Numbers</a><a href="/#portals">Portal Dates</a><a href="/life-path/">Life Path</a><a href="/numerology-2027/">2027</a><a href="/journal/">Journal</a></div>
  <a class="k-cta" href="/#blueprint">Blueprint</a>
</nav></header>
"""


FOOT = """<div class="foot"><a href="/">Free Life Path reading</a><a href="/angel-numbers/">Angel Numbers</a><a href="/life-path/">Life Path</a><a href="/numerology-2027/">Numerology 2027</a><a href="/journal/">Journal</a><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/disclaimer/">Disclaimer</a></div>
<p class="note">For self-reflection and entertainment. Numbers don't decide your life. You do.</p>
</body>
</html>
"""


def nice(d):
    return d.strftime("%B %-d, %Y")


def post_page(p, posts):
    path = f"/journal/{p['slug']}/"
    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    body = md.convert(p["body"])
    paras = re.findall(r"<p>(.*?)</p>", body, re.S)
    lede = re.sub(r"<[^>]+>", "", paras[0]) if paras else p["description"]
    body = body.replace(f"<p>{paras[0]}</p>", "", 1) if paras else body
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["description"],
           "datePublished": p["date"], "dateModified": p["date"], "image": SITE + "/og.png",
           "author": {"@type": "Organization", "name": "Keep Seeing Numbers", "url": SITE + "/about/"},
           "publisher": {"@type": "Organization", "name": "Keep Seeing Numbers", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.png"}},
           "mainEntityOfPage": SITE + path}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Journal", "item": SITE + "/journal/"},
        {"@type": "ListItem", "position": 3, "name": p["title"], "item": SITE + path}]}
    others = [o for o in posts if o["slug"] != p["slug"]][:3]
    num = p.get("number", "")
    out = head(p["title"] + " | Keep Seeing Numbers", p["description"], path, "article", [art, crumbs])
    out += f"""<main class="wrap">
<div class="crumbs"><a href="/">Home</a> / <a href="/journal/">Journal</a></div>
<p class="eyebrow">{e(p.get('tags', 'Journal').split(',')[0].strip())}</p>
<h1>{e(p['title'])}</h1>
<p class="lede">{lede}</p>
<div class="meta">{f'<div class="num">{e(num)}</div>' if num else ''}<div>Keep Seeing Numbers · {nice(p['dt'])}<br>{max(1, round(words / 220))} min read</div></div>
<article class="post">{body}</article>
<div class="cta"><h2>What is <em style="color:var(--gold)">your</em> number?</h2>
<p>Your Life Path number is the lens every date, moon and repeating number is read through. Free, in 10 seconds.</p>
<a class="btn" href="/">Get my free reading</a></div>
{('<section class="more"><h2>More from the journal</h2>' + ''.join(f'<a class="card" href="/journal/{o["slug"]}/"><small>{nice(o["dt"])}</small><b>{e(o["title"])}</b></a>' for o in others) + '</section>') if others else ''}
</main>
"""
    out += FOOT
    return path, out


def list_page(posts):
    path = "/journal/"
    title = "Journal: Numerology for Today's Dates, Moons and Signs | Keep Seeing Numbers"
    desc = "Short, practical reads on today's numbers: portal dates, full moons, repeating numbers in the news and what to do with them."
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Keep Seeing Numbers Journal", "url": SITE + path,
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "datePublished": p["date"], "url": f"{SITE}/journal/{p['slug']}/"} for p in posts[:20]]}
    out = head(title, desc, path, "website", [ld])
    items = "".join(f'<a class="card" href="/journal/{p["slug"]}/"><small>{nice(p["dt"])}</small><b>{e(p["title"])}</b><span>{e(p["description"])}</span></a>' for p in posts)
    out += f"""<main class="wrap">
<p class="eyebrow">Journal</p>
<h1>The numbers of <em style="color:var(--gold)">right now</em></h1>
<p class="lede">Portal dates, full moons and the repeating numbers people are talking about, read through numerology, with one thing to do about each.</p>
<section style="margin-top:30px">{items or '<p class="lede">First posts are on the way.</p>'}</section>
</main>
"""
    out += FOOT
    return path, out


def feed(posts):
    items = "".join(f"""<item><title>{e(p['title'])}</title><link>{SITE}/journal/{p['slug']}/</link><guid>{SITE}/journal/{p['slug']}/</guid><pubDate>{p['dt'].strftime('%a, %d %b %Y')} 09:00:00 +0000</pubDate><description>{e(p['description'])}</description></item>""" for p in posts[:30])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Keep Seeing Numbers Journal</title><link>{SITE}/journal/</link><description>Numerology for today's dates, moons and signs.</description>{items}</channel></rss>
"""


def replace_between(text, start, end, new):
    if start in text and end in text:
        a = text.index(start) + len(start)
        b = text.index(end)
        return text[:a] + new + text[b:]
    return None


def main():
    posts = load_posts()
    for p in posts:
        path, out = post_page(p, posts)
        fp = os.path.join(ROOT, path.strip("/"), "index.html")
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(out)
    path, out = list_page(posts)
    os.makedirs(os.path.join(ROOT, "journal"), exist_ok=True)
    open(os.path.join(ROOT, "journal", "index.html"), "w", encoding="utf-8").write(out)
    open(os.path.join(ROOT, "journal", "feed.xml"), "w", encoding="utf-8").write(feed(posts))

    sm_fp = os.path.join(ROOT, "sitemap.xml")
    sm = open(sm_fp, encoding="utf-8").read()
    urls = "\n".join(f"  <url><loc>{SITE}/journal/{p['slug']}/</loc><lastmod>{p['date']}</lastmod></url>" for p in posts)
    block = f"\n  <url><loc>{SITE}/journal/</loc><lastmod>{posts[0]['date'] if posts else datetime.date.today()}</lastmod></url>\n{urls}\n  "
    new = replace_between(sm, "<!-- JOURNAL -->", "<!-- /JOURNAL -->", block)
    if new is None:
        new = sm.replace("</urlset>", f"  <!-- JOURNAL -->{block}<!-- /JOURNAL -->\n</urlset>")
    open(sm_fp, "w", encoding="utf-8").write(new)

    home_fp = os.path.join(ROOT, "index.html")
    home = open(home_fp, encoding="utf-8").read()
    cards = "".join(f'<a class="k-guide" href="/journal/{p["slug"]}/"><em>{p["dt"].strftime("%b %-d")}</em><strong>{e(p["title"])}</strong><span>{e(p["description"])}</span></a>' for p in posts[:3])
    block = ('' if not posts else f"""
<section class="k-sec" id="journal">
  <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px">
    <div><p class="k-eyebrow">Journal</p><h2 class="k-h2">The numbers of right now</h2></div>
    <a href="/journal/" style="font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--gold)">All posts →</a>
  </div>
  <div class="k-grid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px">{cards}</div>
</section>
""")
    new = replace_between(home, "<!-- JOURNAL -->", "<!-- /JOURNAL -->", block)
    if new is None:
        anchor = '<section class="k-sec" id="blueprint">'
        if anchor not in home:
            raise SystemExit("homepage anchor not found")
        new = home.replace(anchor, f"<!-- JOURNAL -->{block}<!-- /JOURNAL -->\n{anchor}", 1)
    open(home_fp, "w", encoding="utf-8").write(new)
    print("built", len(posts), "posts")


if __name__ == "__main__":
    main()
