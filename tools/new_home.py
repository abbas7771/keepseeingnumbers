#!/usr/bin/env python3
"""Wrap the existing calculator homepage in the new multi-section layout.

Keeps the original <head> (SEO, JSON-LD, AdSense), the calculator form,
result section, offer and checkout modal and all their scripts untouched,
and adds: ticker, sticky nav, quick-find chips, Today's Number, Portal
Dates countdown, Angel Numbers grid, Life Path + 2027, Reels, Learn,
Blueprint banner and a new footer.

Usage: python3 tools/new_home.py index.html  (rewrites in place)
"""
import sys

src = open(sys.argv[1], encoding="utf-8").read()
if "k-nav" in src:
    sys.exit("already converted")

head_end = src.index("</head>")
head = src[:head_end]
body_start = src.index("<body>") + len("<body>")
wrap_start = src.index('<div class="wrap">')
foot_p = src.index('<p class="foot">')
modal = src.index('<div id="nm" class="modal">')
footer_links = src.index('<div style="text-align:center;font-size:13px;margin:30px 0 10px')
body_end = src.index("</body>")

stars_svg = src[body_start:wrap_start]
calc_inner = src[wrap_start + len('<div class="wrap">'):foot_p]
main_script = src[src.index("</div>", foot_p) + len("</div>"):modal]
modal_and_script = src[modal:footer_links]

CSS = """
<style>
.k-ticker{position:relative;z-index:2;background:linear-gradient(90deg,#ffd27a,#ff9a3c);color:#000;text-align:center;font:700 12px Montserrat,sans-serif;letter-spacing:2px;text-transform:uppercase;padding:10px 16px}
.k-ticker a{color:#000}
.k-head{position:sticky;top:0;z-index:20;background:rgba(0,0,0,.88);backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,204,102,.14)}
.k-nav{max-width:1200px;margin:0 auto;padding:16px 24px;display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center;justify-content:space-between}
.k-logo{font-size:12px;letter-spacing:6px;text-transform:uppercase;color:var(--ink);text-decoration:none;font-weight:700}
.k-links{display:flex;flex-wrap:wrap;gap:6px 22px;font-size:13px}
.k-links a{color:#d9d2c5;text-decoration:none}.k-links a:hover{color:var(--gold)}
.k-cta{border:1px solid var(--gold);border-radius:999px;padding:9px 18px;font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--gold);text-decoration:none}
.k-chips-sec{position:relative;z-index:1;border-top:1px solid rgba(255,204,102,.14);border-bottom:1px solid rgba(255,204,102,.14);background:#070605}
.k-in{max-width:1200px;margin:0 auto;padding:0 24px}
.k-chips{display:flex;flex-wrap:wrap;gap:14px;align-items:center;padding:26px 24px;max-width:1200px;margin:0 auto}
.k-chips p{margin:0;font-family:"Cormorant Garamond",serif;font-size:24px;font-weight:700;flex:1 1 260px}
.k-chip{border:1px solid rgba(255,204,102,.3);border-radius:999px;padding:9px 16px;color:var(--ink);text-decoration:none;font-size:15px;letter-spacing:1px}
.k-chip:hover{border-color:var(--gold);color:var(--gold)}
.k-sec{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:88px 24px 0}
.k-eyebrow{margin:0;font-size:12px;letter-spacing:5px;text-transform:uppercase;color:var(--gold)}
.k-h2{margin:10px 0 0;font-family:"Cormorant Garamond",serif;font-weight:700;font-size:44px;line-height:1.08;text-align:left}
.k-row{display:flex;flex-wrap:wrap;gap:20px;margin-top:26px}
.k-box{flex:1 1 380px;border-radius:24px;padding:30px;background:#0d0b09;border:1px solid rgba(255,255,255,.1)}
.k-glow{background:radial-gradient(ellipse at top left,rgba(255,170,70,.18),transparent 70%),#0d0b09;border-color:rgba(255,204,102,.25)}
.k-big{width:116px;height:116px;flex:none;border-radius:50%;border:2px solid var(--gold);box-shadow:0 0 40px rgba(255,180,80,.35);display:flex;align-items:center;justify-content:center;font-size:58px;font-weight:300;color:var(--gold)}
.k-mute{color:#a59f93;font-size:12px;letter-spacing:3px;text-transform:uppercase;margin:0}
.k-p{margin:10px 0 0;font-size:17px;line-height:1.6}
.k-sel{background:#000;color:var(--ink);border:1px solid rgba(255,255,255,.2);border-radius:10px;padding:10px 12px;font:500 15px Montserrat;width:auto;margin-left:6px}
.k-count{display:flex;gap:18px;margin-top:18px}
.k-count b{display:block;font-size:40px;font-weight:300}
.k-count span{font-size:11px;letter-spacing:2px;color:#a59f93}
.k-list{flex:1 1 380px;display:flex;flex-direction:column;gap:10px}
.k-item{display:flex;align-items:center;gap:16px;padding:15px 18px;border-radius:16px;background:#0d0b09;border:1px solid rgba(255,255,255,.08);text-decoration:none;color:var(--ink)}
.k-item:hover{border-color:rgba(255,204,102,.4)}
.k-item i{font-style:normal;width:70px;flex:none;font-size:19px;color:var(--gold);font-weight:300}
.k-item small{display:block;color:#a59f93;font-size:13px;margin-top:2px}
.k-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-top:26px}
.k-tile{display:block;padding:22px 14px;border-radius:18px;background:#0d0b09;border:1px solid rgba(255,204,102,.18);text-decoration:none;text-align:center;color:var(--ink)}
.k-tile:hover{border-color:var(--gold)}
.k-tile b{display:block;font-size:30px;font-weight:300;color:var(--gold);letter-spacing:2px}
.k-tile span{display:block;margin-top:6px;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#a59f93}
.k-dots{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.k-dot{width:50px;height:50px;border-radius:50%;border:1px solid rgba(255,204,102,.35);display:flex;align-items:center;justify-content:center;text-decoration:none;color:var(--ink);font-size:17px}
.k-dot:hover{border-color:var(--gold);color:var(--gold)}
.k-yr{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:18px}
.k-yr a{padding:12px;border-radius:12px;background:#000;border:1px solid rgba(255,255,255,.1);text-decoration:none;color:var(--ink);font-size:13px}
.k-yr a b{color:var(--gold)}
.k-reel{display:flex;flex-direction:column;justify-content:space-between;aspect-ratio:9/16;border-radius:20px;padding:18px;text-decoration:none;color:var(--ink);background:radial-gradient(circle at 50% 38%,#000 22%,#ffd27a 25%,rgba(255,138,42,.25) 34%,#050403 52%);border:1px solid rgba(255,204,102,.2)}
.k-reel b{text-align:center;font-size:32px;font-weight:300;color:var(--gold)}
.k-reel span{font-size:14px;line-height:1.4}
.k-guide{display:block;padding:26px;border-radius:20px;background:#0d0b09;border:1px solid rgba(255,255,255,.08);text-decoration:none;color:var(--ink)}
.k-guide:hover{border-color:rgba(255,204,102,.4)}
.k-guide em{font-style:normal;font-size:13px;letter-spacing:3px;color:var(--gold)}
.k-guide strong{display:block;margin-top:10px;font-family:"Cormorant Garamond",serif;font-size:26px}
.k-guide span{display:block;margin-top:8px;font-size:14px;line-height:1.55;color:#b9b2a5}
.k-offer{display:flex;flex-wrap:wrap;gap:30px;align-items:center;border-radius:28px;padding:42px;background:radial-gradient(ellipse at 85% 10%,rgba(255,170,70,.22),transparent 60%),#050403;border:1px solid rgba(255,204,102,.3)}
.k-btn{display:inline-block;text-decoration:none;border-radius:999px;padding:17px 32px;font:800 14px Montserrat;letter-spacing:3px;text-transform:uppercase;color:#000;background:linear-gradient(90deg,#ffd27a,var(--gold2))}
.k-foot{position:relative;z-index:1;margin-top:96px;border-top:1px solid rgba(255,204,102,.14);background:#050403}
.k-fgrid{max-width:1200px;margin:0 auto;padding:48px 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:28px;font-size:14px}
.k-fgrid div{display:flex;flex-direction:column;gap:10px}
.k-fgrid b{font-size:12px;letter-spacing:3px;color:var(--gold)}
.k-fgrid a{color:#b9b2a5;text-decoration:none}.k-fgrid a:hover{color:var(--gold)}
@media(max-width:640px){.k-h2{font-size:34px}.k-offer{padding:28px}.k-big{width:90px;height:90px;font-size:44px}}
</style>
"""

NAV = """
<div class="k-ticker">Today adds up to <b id="kTick">·</b> · 12/12 portal in <b id="kTickDays">·</b> days · <a href="#portals">See dates</a></div>
<header class="k-head"><nav class="k-nav" aria-label="Main">
  <a class="k-logo" href="/">Keep Seeing Numbers</a>
  <div class="k-links"><a href="#today">Today</a><a href="/angel-numbers/">Angel Numbers</a><a href="#portals">Portal Dates</a><a href="/life-path/">Life Path</a><a href="/numerology-2027/">2027</a><a href="#learn">Learn</a></div>
  <a class="k-cta" href="#blueprint">Blueprint</a>
</nav></header>
"""

ANGELS = [("000", "Potential"), ("111", "Manifest"), ("222", "Balance"), ("333", "Expression"), ("444", "Foundation"),
          ("555", "Change"), ("666", "Rebalance"), ("777", "Luck"), ("888", "Abundance"), ("999", "Completion"),
          ("1010", "Level up"), ("1111", "Portal"), ("1212", "Step up"), ("1234", "Progress"), ("2222", "Harmony")]
YEARS = ["Beginnings", "Balance", "Expression", "Foundation", "Change", "Care", "Insight", "Results", "Completion"]

chips = "".join(f'<a class="k-chip" href="/angel-numbers/{n}/">{n[:2] + ":" + n[2:] if len(n) == 4 else n}</a>'
                for n in ["1111", "111", "222", "333", "444", "555", "777", "1212"])
tiles = "".join(f'<a class="k-tile" href="/angel-numbers/{n}/"><b>{n}</b><span>{k}</span></a>' for n, k in ANGELS)
dots = "".join(f'<a class="k-dot" href="/life-path/{n}/">{n}</a>' for n in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "22", "33"])
yrs = "".join(f'<a href="/numerology-2027/personal-year-{i}/"><b>{i}</b> · {w}</a>' for i, w in enumerate(YEARS, 1))
months = "".join(f'<option value="{i}">{m}</option>' for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1))
days = "".join(f'<option value="{i}">{i}</option>' for i in range(1, 32))

SECTIONS = f"""
<section class="k-chips-sec"><div class="k-chips"><p>Which number keeps finding you?</p>{chips}</div></section>

<section class="k-sec" id="today">
  <p class="k-eyebrow">Today · <span id="kDate"></span></p>
  <h2 class="k-h2">Today's Number</h2>
  <div class="k-row">
    <div class="k-box k-glow" style="display:flex;gap:26px;align-items:center">
      <div class="k-big" id="kDay">·</div>
      <div><p class="k-mute">Universal day <span id="kDay2"></span> · <span id="kWord"></span></p><p class="k-p" id="kText"></p></div>
    </div>
    <div class="k-box">
      <p class="k-eyebrow" style="letter-spacing:3px">Your personal day</p>
      <p style="margin:8px 0 0;color:#b9b2a5;font-size:14px">Pick your birthday. It changes every day.</p>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:14px;align-items:center">
        <label style="font-size:12px;color:#a59f93;letter-spacing:1px;text-transform:none;margin:0">Month<select class="k-sel" id="kpm">{months}</select></label>
        <label style="font-size:12px;color:#a59f93;letter-spacing:1px;text-transform:none;margin:0">Day<select class="k-sel" id="kpd">{days}</select></label>
      </div>
      <p class="k-p">Personal day <b id="kPDay" style="color:var(--gold);font-size:22px"></b>: <span id="kPText"></span></p>
    </div>
  </div>
</section>

<section class="k-sec" id="portals">
  <p class="k-eyebrow">Portal dates</p>
  <h2 class="k-h2">The next doors to open</h2>
  <div class="k-row">
    <div class="k-box k-glow" style="background:radial-gradient(ellipse at 80% 0%,rgba(255,170,70,.2),transparent 70%),#050403">
      <p class="k-mute">Next portal</p>
      <p style="margin:6px 0 0;font-family:'Cormorant Garamond',serif;font-size:72px;font-weight:700;line-height:1;color:var(--gold)">12/12</p>
      <div class="k-count"><div><b id="kcD">·</b><span>DAYS</span></div><div><b id="kcH">·</b><span>HOURS</span></div><div><b id="kcM">·</b><span>MIN</span></div><div><b id="kcS">·</b><span>SEC</span></div></div>
      <p style="margin:18px 0 0;color:#b9b2a5;font-size:15px;line-height:1.6">12 is 1 + 2 = 3, the number of growth and voice. Twice in one date.</p>
      <a href="/angel-numbers/1212/" style="display:inline-block;margin-top:12px;font-size:13px;color:var(--gold)">What 12:12 means →</a>
    </div>
    <div class="k-list">
      <a class="k-item" href="/angel-numbers/1212/"><i>12/12</i><span style="flex:1"><b>12/12 portal</b><small>Growth and voice. Set one intention.</small></span>→</a>
      <a class="k-item" href="#portals"><i>Dec 24</i><span style="flex:1"><b>Full Moon (Cold Moon)</b><small>Release what is finished before the year ends.</small></span>→</a>
      <a class="k-item" href="/numerology-2027/"><i>1/1</i><span style="flex:1"><b>2027 begins</b><small>An 11/2 universal year: intuition and partnership.</small></span>→</a>
      <a class="k-item" href="/angel-numbers/1111/"><i>1/11</i><span style="flex:1"><b>1/11 portal</b><small>Stacked ones: a strong start-over date.</small></span>→</a>
      <a class="k-item" href="/angel-numbers/222/"><i>2/2</i><span style="flex:1"><b>2/2 portal</b><small>Balance and connection. Reach out.</small></span>→</a>
    </div>
  </div>
</section>

<section class="k-sec" id="angel">
  <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px">
    <div><p class="k-eyebrow">Angel numbers</p><h2 class="k-h2">What your number means</h2></div>
    <a href="/angel-numbers/" style="font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--gold)">All numbers →</a>
  </div>
  <div class="k-grid">{tiles}</div>
</section>

<section class="k-sec">
  <div class="k-row" style="margin-top:0">
    <div class="k-box">
      <p class="k-eyebrow">Life Path</p><h2 class="k-h2" style="font-size:36px">Who you came here to be</h2>
      <div class="k-dots">{dots}</div>
      <a href="/life-path/" style="display:inline-block;margin-top:16px;font-size:13px;color:var(--gold)">All Life Path meanings →</a>
    </div>
    <div class="k-box k-glow">
      <p class="k-eyebrow">Numerology 2027</p><h2 class="k-h2" style="font-size:36px">Your personal year ahead</h2>
      <div class="k-yr">{yrs}</div>
    </div>
  </div>
</section>

<section class="k-sec">
  <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px">
    <div><p class="k-eyebrow">Watch</p><h2 class="k-h2">Numbers in 30 seconds</h2></div>
    <a href="https://www.instagram.com/keepseeingnumbers/" style="font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--gold)">@keepseeingnumbers →</a>
  </div>
  <div class="k-grid" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr))">
    <a class="k-reel" href="https://www.instagram.com/keepseeingnumbers/"><small style="font-size:11px;letter-spacing:3px;color:#a59f93">REEL</small><b>12/12</b><span>Nobody tells you what to do on 12/12</span></a>
    <a class="k-reel" href="https://www.instagram.com/keepseeingnumbers/"><small style="font-size:11px;letter-spacing:3px;color:#a59f93">REEL</small><b>111</b><span>Stop wishing. Start writing.</span></a>
    <a class="k-reel" href="https://www.instagram.com/keepseeingnumbers/"><small style="font-size:11px;letter-spacing:3px;color:#a59f93">REEL</small><b>444</b><span>444 isn't a warning</span></a>
    <a class="k-reel" href="https://www.instagram.com/keepseeingnumbers/"><small style="font-size:11px;letter-spacing:3px;color:#a59f93">REEL</small><b>11:11</b><span>POV: it's 11:11 again</span></a>
  </div>
</section>

<section class="k-sec" id="learn">
  <p class="k-eyebrow">Numerology 101</p>
  <h2 class="k-h2">Don't know where to start?</h2>
  <div class="k-grid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px">
    <a class="k-guide" href="#top"><em>01</em><strong>Find your Life Path</strong><span>The one number that shapes how every other sign shows up for you. Free, in 10 seconds.</span></a>
    <a class="k-guide" href="/angel-numbers/"><em>02</em><strong>Why you see repeating numbers</strong><span>What 111, 222 or 11:11 means, and what to do when you see it.</span></a>
    <a class="k-guide" href="/numerology-2027/"><em>03</em><strong>Plan your 2027</strong><span>Your personal year number and the theme it sets for the year ahead.</span></a>
  </div>
</section>

<section class="k-sec" id="blueprint">
  <div class="k-offer">
    <div style="flex:1 1 440px">
      <p class="k-eyebrow">Your Numerology Blueprint</p>
      <h2 class="k-h2">Personal report + 2027 workbook</h2>
      <p style="margin:14px 0 0;color:#b9b2a5;font-size:16px;line-height:1.6">Your love and money patterns, Expression and Soul Urge numbers, love compatibility, what 111, 222, 333 mean for you, and your 2027 month by month. 15-page PDF, instant download.</p>
    </div>
    <div style="flex:0 1 300px;text-align:center">
      <p style="margin:0"><span style="color:#8a8478;text-decoration:line-through;font-size:18px">$19</span> <span style="font-size:40px;font-weight:800;color:var(--gold)">$9</span></p>
      <p style="margin:4px 0 0;font-size:12px;letter-spacing:2px;color:#a59f93">LAUNCH PRICE</p>
      <a class="k-btn k-buy" href="https://meherremov7.gumroad.com/l/evpeqb/WELCOME10" style="margin-top:16px">Get my Blueprint</a>
      <p style="margin:10px 0 0;font-size:12px;color:#8a8478">Secure checkout via Gumroad</p>
    </div>
  </div>
</section>
"""

FOOT = """
<footer class="k-foot"><div class="k-fgrid">
  <div><span style="font-size:12px;letter-spacing:5px;text-transform:uppercase">Keep Seeing Numbers</span><span style="color:#8a8478;font-size:13px;line-height:1.6">For self-reflection and entertainment. Numbers don't decide your life. You do.</span></div>
  <div><b>EXPLORE</b><a href="#today">Today's Number</a><a href="/angel-numbers/">Angel Numbers</a><a href="#portals">Portal Dates</a><a href="/life-path/">Life Path</a><a href="/numerology-2027/">Numerology 2027</a></div>
  <div><b>LEARN</b><a href="#learn">Numerology 101</a><a href="#blueprint">Blueprint PDF</a><a href="https://www.instagram.com/keepseeingnumbers/">Instagram</a></div>
  <div><b>ABOUT</b><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy Policy</a><a href="/terms/">Terms</a><a href="/disclaimer/">Disclaimer</a></div>
</div></footer>
"""

JS = """
<script>
(function(){
  const $=id=>document.getElementById(id);
  const words=['','Beginnings','Balance','Expression','Foundation','Change','Care','Insight','Results','Completion'];
  const texts=['','Start the thing. One visible first step beats a perfect plan.','Cooperate. Follow up once, then let timing work.','Say it, make it, share it. Your voice is the move today.','Do the unglamorous work. Routines carry you.','Something shifts. Say yes to one new thing.','Come back to home and the people who matter.','Slow down and listen. The answer is quiet today.','A day for results. Ask for what your work is worth.','Close one open loop before you start another.'];
  const sum=s=>String(s).split('').reduce((a,b)=>a+Number(b),0);
  const red=n=>{while(n>9)n=sum(n);return n};
  const now=new Date(),y=now.getFullYear(),mo=now.getMonth()+1,dd=now.getDate();
  const mn=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const day=red(sum(mo)+sum(dd)+sum(y));
  $('kDay').textContent=day;$('kDay2').textContent=day;$('kTick').textContent=day;
  $('kWord').textContent=words[day];$('kText').textContent=texts[day];
  $('kDate').textContent=mn[mo-1]+' '+dd+', '+y;
  const pm=$('kpm'),pd=$('kpd');
  let saved={};try{saved=JSON.parse(localStorage.getItem('ksn_bday')||'{}')}catch(e){}
  if(saved.m){pm.value=saved.m;pd.value=saved.d}
  function pday(){const p=red(sum(pm.value)+sum(pd.value)+sum(y)+sum(mo)+sum(dd));$('kPDay').textContent=p;$('kPText').textContent=texts[p];try{localStorage.setItem('ksn_bday',JSON.stringify({m:pm.value,d:pd.value}))}catch(e){}}
  pm.addEventListener('change',pday);pd.addEventListener('change',pday);pday();
  function target(){let t=new Date(y,11,12);if(now>new Date(y,11,13))t=new Date(y+1,11,12);return t}
  const T=target();
  function tick(){const d=Math.max(0,T-new Date());$('kcD').textContent=Math.floor(d/864e5);$('kcH').textContent=Math.floor(d/36e5)%24;$('kcM').textContent=Math.floor(d/6e4)%60;$('kcS').textContent=Math.floor(d/1e3)%60;$('kTickDays').textContent=Math.floor(d/864e5)}
  tick();setInterval(tick,1000);
  document.querySelectorAll('.k-buy').forEach(b=>b.addEventListener('click',e=>{const m=document.querySelector('.buybtn');if(m){e.preventDefault();m.click()}}));
})();
</script>
"""

out = (head + CSS + "</head>\n<body>\n" + stars_svg + NAV
       + '<div class="wrap" id="top">' + calc_inner + "</div>\n"
       + SECTIONS + FOOT + main_script + modal_and_script + JS + "</body>\n</html>\n")
open(sys.argv[1], "w", encoding="utf-8").write(out)
print("ok", len(out))
