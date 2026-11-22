// renderReport(person) -> full HTML string (A4, print-ready)
function renderReport(p, D, W){
  const {DEEP, EXP_REFLECT, SOUL_REFLECT, PERS_REFLECT, PYEAR_MONTH_HINT} = W;
  const lines = n => `<div class="lines">${'<div></div>'.repeat(n)}</div>`;
  const qa = (q,n=3) => `<div class="q">${q}</div>${lines(n)}`;
  const tryBox = t => `<div class="try"><div class="tryk">✦ TRY THIS WEEK</div><div>${t}</div><div class="chk"><span class="box"></span> Done &nbsp;&nbsp; Date: ________________</div></div>`;
  const {calc, NAMES, KEYS, LIFE, EXPRESSION, SOUL, PERSONALITY, BIRTHDAY, PYEAR, PMONTH, COMPAT, ANGEL, ANGEL_MEAN, TRAITS, PYFOCUS} = D;
  const traits = n => `<div class="tr"><div><h4>Strengths</h4>${TRAITS[n].s.map(x=>`<span class="chip">${x}</span>`).join('')}</div><div><h4>Watch for</h4>${TRAITS[n].w.map(x=>`<span class="chip dim">${x}</span>`).join('')}</div></div>`;
  const r = calc(p.name, p.d, p.m, p.y);
  const L = LIFE[r.life];
  const monthsN = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  const base = n => n===11?2:n===22?4:n===33?6:n;
  const cp = COMPAT[base(r.life)];
  const first = p.name.trim().split(/\s+/)[0];
  const eclipse = (s=260)=>`<svg width="${s}" height="${s}" viewBox="0 0 1080 1080"><defs><radialGradient id="c${s}"><stop offset=".5" stop-color="#fff"/><stop offset=".57" stop-color="#ffd27a" stop-opacity=".95"/><stop offset=".75" stop-color="#ff8a2a" stop-opacity=".3"/><stop offset="1" stop-color="#ff5a00" stop-opacity="0"/></radialGradient><radialGradient id="f${s}"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#fff3d6" stop-opacity=".7"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient></defs><circle cx="540" cy="540" r="440" fill="url(#c${s})"/><circle cx="540" cy="540" r="222" fill="#000"/><circle cx="690" cy="390" r="110" fill="url(#f${s})"/><circle cx="690" cy="390" r="9" fill="#fff"/></svg>`;
  const master = n => n>9 ? '<span class="mtag">MASTER NUMBER</span>' : '';
  const head = (kicker, title, num) => `<div class="phead"><div class="kick">${kicker}</div><div class="ptitle">${title}</div>${num!==undefined?`<div class="bignum">${num}</div>`:''}</div>`;
  const foot = n => `<div class="pfoot"><span>KEEP SEEING NUMBERS</span><span>${p.name} · ${n}</span></div>`;
  let pg = 0; const page = (inner, cls='') => `<section class="page ${cls}">${inner}${cls==='cover'?'':foot(++pg)}</section>`;

  const coreCard = (label, n, sub) => `<div class="core"><div class="cnum">${n}</div><div class="clab">${label}</div><div class="csub">${NAMES[n]||''}</div><div class="cdesc">${sub}</div></div>`;

  const pages = [];
  // cover
  pages.push(page(`<div class="stars"></div><div class="cov">
    <div class="brand">KEEP SEEING NUMBERS</div>
    <div class="covecl">${eclipse(380)}<div class="covnum">${r.life}</div></div>
    <div class="covk">THE PERSONAL NUMEROLOGY REPORT OF</div>
    <div class="covname">${p.name}</div>
    <div class="covdate">Born ${p.d} ${monthsN[p.m-1]} ${p.y}</div>
    <div class="covinc">Life Path · Expression · Soul Urge · Personality · Birthday · 2027 Forecast · Love · Angel Numbers</div></div>`,'cover'));
  // welcome + core numbers
  pages.push(page(`${head('YOUR BLUEPRINT','Dear '+first+',')}
    <p class="lead">Every name and every birth date carries a pattern. Numerology reads that pattern — the strengths you were born with, the lessons you keep meeting, and the timing of the chapters ahead.</p>
    <p>This report was calculated personally for you from your full birth name and your date of birth. Read it slowly. Some parts will feel instantly familiar; others may only make sense months from now.</p>
    <div class="grid">
      ${coreCard('Life Path', r.life, 'Your purpose and the road you walk')}
      ${coreCard('Expression', r.expression, 'Your natural talents')}
      ${coreCard('Soul Urge', r.soul, 'What your heart truly wants')}
      ${coreCard('Personality', r.personality, 'How others see you')}
      ${coreCard('Birthday', r.birthday, 'Your special gift')}
      ${coreCard('2027 Year', r.pyear, 'The energy of your year ahead')}
    </div>`));
  // life path
  const DP = DEEP[r.life];
  pages.push(page(`${head('YOUR LIFE PATH NUMBER', NAMES[r.life], r.life)}${master(r.life)}
    <div class="keys">${KEYS[r.life]}</div>
    <div class="calcline">${monthsN[p.m-1]} → ${r.steps.a} &nbsp;·&nbsp; Day ${p.d} → ${r.steps.b} &nbsp;·&nbsp; ${p.y} → ${r.steps.c} &nbsp;·&nbsp; ${r.steps.a} + ${r.steps.b} + ${r.steps.c} → <b>${r.life}</b></div>
    <p class="lead">Your Life Path is the most important number in your chart — the road you came here to walk.</p>
    <h3>✦ The deeper story</h3><p>${DP.deep[0]}</p><p>${DP.deep[1]}</p>${traits(r.life)}`));
  pages.push(page(`${head('LIFE PATH '+r.life+' · LOVE, WORK & LESSON', 'How it shows up')}
    <h3>✦ In love</h3><p>${L.love}</p>
    <h3>✦ In work & money</h3><p>${L.work}</p>
    <h3>✦ Your life lesson</h3><p>${L.lesson}</p>
    <div class="aff">“${L.aff}”</div>
    ${tryBox('Read your affirmation aloud each morning this week. Write down one situation where it felt true — and one where it felt hard.')}
    ${qa('Where did my affirmation feel true this week?',2)}`));
  pages.push(page(`${head('WORKBOOK · LIFE PATH '+r.life, 'Make it personal')}
    <p>Take 15 quiet minutes. Answer honestly — nobody else will read this.</p>
    ${DP.reflect.map(q=>qa(q,3)).join('')}
    ${tryBox(DP.tryit)}`));
  // expression / soul / personality / birthday
  pages.push(page(`${head('YOUR EXPRESSION NUMBER', NAMES[r.expression], r.expression)}${master(r.expression)}
    <p class="lead">Calculated from every letter of your full birth name, your Expression Number reveals the talents you brought with you.</p>
    <p>${EXPRESSION[r.expression]}</p>
    <div class="note">Life Path ${r.life} + Expression ${r.expression}: ${r.life===r.expression?'the same number — a rare alignment that makes your direction unusually clear.':'your purpose and your talents are different energies. Your sweet spot is where they overlap.'}</div>
    ${traits(r.expression)}
    ${qa(EXP_REFLECT[r.expression][0],2)}
    ${tryBox(EXP_REFLECT[r.expression][1])}`));
  pages.push(page(`${head('YOUR SOUL URGE NUMBER', NAMES[r.soul], r.soul)}${master(r.soul)}
    <p class="lead">Drawn from the vowels of your name, the Soul Urge describes what your heart secretly longs for.</p>
    <p>${SOUL[r.soul]}</p>${traits(r.soul)}
    <div class="note">Your Soul Urge is often hidden — even from you. When a choice feels "right" for no logical reason, this number is usually speaking.</div>
    ${qa(SOUL_REFLECT[r.soul],3)}
    ${qa('Which of your current goals truly come from this inner wish — and which come from other people?',3)}`));
  pages.push(page(`${head('YOUR PERSONALITY NUMBER', NAMES[r.personality], r.personality)}${master(r.personality)}
    <p class="lead">Drawn from the consonants of your name — the first impression people get before they know you.</p>
    <p>${PERSONALITY[r.personality]}</p>${traits(r.personality)}
    <div class="note">${r.personality===r.soul?'Your Soul Urge and Personality share the same number — what people see is what you truly feel.':'Your inner self ('+r.soul+') and outer self ('+r.personality+') are different energies. People may not see your depths at first.'}</div>
    ${tryBox(PERS_REFLECT[r.personality])}
    ${qa('What did you notice?',2)}`));
  pages.push(page(`${head('YOUR BIRTHDAY NUMBER', 'Day '+p.d, r.birthday)}
    <p>${BIRTHDAY[r.birthday]}</p>
    ${head('YOUR PERSONAL YEAR · 2027', PYEAR[r.pyear].t, r.pyear)}
    <p class="lead">${PYEAR[r.pyear].d}</p>
    <div class="tr"><div><h4>Focus on</h4><ul>${PYFOCUS[r.pyear].f.map(x=>`<li>${x}</li>`).join('')}</ul></div><div><h4>Avoid</h4><ul>${PYFOCUS[r.pyear].a.map(x=>`<li>${x}</li>`).join('')}</ul></div></div>
    ${qa('My one big intention for 2027:',2)}`));
  // months
  pages.push(page(`${head('2027 PLANNER', 'Your Personal Months')}
    <p>${PYEAR_MONTH_HINT}</p>
    <div class="months">${r.months.map((n,i)=>`<div class="mo"><div class="moname">${monthsN[i]}</div><div class="monum">${n}</div><div class="motxt">${PMONTH[n]}</div><div class="mline"></div><div class="mline"></div></div>`).join('')}</div>`));
  // love
  pages.push(page(`${head('LOVE & COMPATIBILITY', 'Who matches your number')}
    <p class="lead">Compatibility is about how two Life Path energies naturally interact — never a verdict on who you can or can't love.</p>
    <div class="compat">
      <div><h4>Natural matches</h4><div class="cn">${cp.best.join(' · ')}</div><p>Easy chemistry. You understand each other without effort.</p></div>
      <div><h4>Good balance</h4><div class="cn">${cp.good.join(' · ')}</div><p>Different but complementary. You grow through each other.</p></div>
      <div><h4>Growth pairings</h4><div class="cn">${cp.grow.join(' · ')}</div><p>Strong attraction, real lessons. Works with patience and honesty.</p></div>
    </div>
    <h3>✦ What you need in love</h3><p>${L.love}</p>
    ${qa('Think of your closest relationship. Where do your energies match — and where do they clash?',3)}
    ${qa('What is one thing you could ask for in love that you never have?',2)}`));
  // angel numbers
  const an = ANGEL[r.life];
  pages.push(page(`${head('YOUR ANGEL NUMBERS', 'The numbers that follow you')}
    <p class="lead">Because your core number is ${r.life}, these sequences are especially meaningful for you. When they appear, pause — and notice what you were thinking about.</p>
    ${an.map(k=>`<div class="angel"><div class="anum">${k}</div><div>${ANGEL_MEAN[k]||''}</div></div>`).join('')}
    <h3>✦ When you see one</h3><p>Stop for a breath. Notice your thought in that moment. Ask: "What is this asking me to trust?" Then take one small action in that direction.</p>`));
  pages.push(page(`${head('30-DAY NUMBER JOURNAL', 'Notice the patterns')}
    <p>Each time a repeating number catches your eye, log it here. After 30 days, look back: what were you thinking about most often?</p>
    <table class="log"><tr><th>Day</th><th>Number seen</th><th>What I was thinking / feeling</th><th>Action I took</th></tr>${Array.from({length:15},(_,i)=>`<tr><td>${i+1}</td><td></td><td></td><td></td></tr>`).join('')}</table>`));
  pages.push(page(`${head('30-DAY NUMBER JOURNAL · CONTINUED', 'Days 16–30')}
    <table class="log"><tr><th>Day</th><th>Number seen</th><th>What I was thinking / feeling</th><th>Action I took</th></tr>${Array.from({length:15},(_,i)=>`<tr><td>${i+16}</td><td></td><td></td><td></td></tr>`).join('')}</table>
    ${qa('Looking back: what pattern do I notice?',3)}`));
  // closing
  pages.push(page(`<div class="close">${eclipse(220)}
    <div class="ptitle" style="text-align:center;margin-top:20px">Your numbers are a map,<br>not a verdict.</div>
    <p style="text-align:center;max-width:520px;margin:20px auto">They describe tendencies, gifts and timing — but every choice is still yours. Come back to this report whenever you need a reminder of who you are.</p>
    <div class="aff">“${L.aff}”</div>
    <p class="disc">This report is intended for self-reflection and entertainment. It is not medical, financial, legal or psychological advice.</p>
    <div class="brand" style="text-align:center;margin-top:24px">KEEPSEEINGNUMBERS.COM</div></div>`));

  return `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>${p.name} · Numerology Report</title>
<style>
@font-face{font-family:M;src:url("${p.fontBase||''}Montserrat.ttf");font-weight:100 900}
@font-face{font-family:L;src:url("${p.fontBase||''}Lora.ttf");font-weight:400 700}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#050403;font-family:M,sans-serif;color:#ece6da;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;padding:22mm 20mm 24mm;background:radial-gradient(ellipse at 50% 0%,#1a1208 0%,#050403 55%);page-break-after:always;overflow:hidden}
.page.cover{background:#000;padding:0}
.stars{position:absolute;inset:0;background-image:radial-gradient(1.5px 1.5px at 10% 20%,#fff,transparent),radial-gradient(1px 1px at 30% 70%,#fff,transparent),radial-gradient(1.2px 1.2px at 80% 30%,#fff,transparent),radial-gradient(1px 1px at 60% 85%,#fff,transparent),radial-gradient(1.4px 1.4px at 90% 75%,#fff,transparent),radial-gradient(1px 1px at 20% 90%,#fff,transparent),radial-gradient(1px 1px at 45% 12%,#fff,transparent),radial-gradient(1.2px 1.2px at 70% 55%,#fff,transparent);opacity:.7}
.cov{position:relative;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20mm}
.brand{font-size:10pt;letter-spacing:6px;color:#a59f93}
.covecl{position:relative;margin:14mm 0 10mm}
.covnum{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:L;font-size:64pt;color:#ffcc66}
.covk{font-size:9pt;letter-spacing:5px;color:#a59f93}
.covname{font-family:L;font-weight:700;font-size:34pt;color:#fff;margin:5mm 0 3mm}
.covdate{color:#ffcc66;letter-spacing:2px}
.covinc{margin-top:16mm;font-size:8.5pt;color:#7e776c;letter-spacing:1px;max-width:140mm;line-height:1.6}
.phead{position:relative;margin-bottom:6mm}
.kick{font-size:8.5pt;letter-spacing:5px;color:#ffcc66;font-weight:700}
.ptitle{font-family:L;font-weight:700;font-size:30pt;color:#fff;margin-top:2mm;line-height:1.15}
.bignum{position:absolute;right:0;top:-6mm;font-family:L;font-size:72pt;color:#ffcc66;text-shadow:0 0 30px rgba(255,190,90,.45)}
.mtag{display:inline-block;font-size:7.5pt;letter-spacing:3px;color:#ffcc66;border:1px solid #ffcc66;border-radius:20px;padding:1.2mm 3.5mm;margin-bottom:4mm}
.keys{font-size:9pt;letter-spacing:3px;color:#a59f93;text-transform:uppercase;margin-bottom:4mm}
.calcline{font-size:9pt;color:#cfc6b6;background:rgba(255,204,102,.07);border:1px solid rgba(255,204,102,.2);border-radius:3mm;padding:3mm 4mm;margin-bottom:6mm}
p{font-size:12pt;line-height:1.7;margin-bottom:4mm;color:#ddd5c6}
p.lead{font-family:L;font-style:italic;font-size:14pt;color:#f1ead9;line-height:1.55}
h3{font-size:9.5pt;letter-spacing:4px;color:#ffcc66;margin:6mm 0 2mm;text-transform:uppercase}
.aff{font-family:L;font-style:italic;font-size:18pt;text-align:center;color:#fff;margin:10mm 0 0}
.note{border-left:2px solid #ffcc66;padding:2mm 0 2mm 5mm;margin-top:6mm;font-size:10pt;color:#cfc6b6;line-height:1.6}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:8mm}
.core{border:1px solid rgba(255,204,102,.22);border-radius:4mm;padding:5mm;background:rgba(255,204,102,.04)}
.cnum{font-family:L;font-size:30pt;color:#ffcc66;line-height:1}
.clab{font-size:8pt;letter-spacing:4px;color:#fff;margin-top:2mm;font-weight:700;text-transform:uppercase}
.csub{font-family:L;font-style:italic;color:#cfc6b6;font-size:10pt;margin-top:1mm}
.cdesc{font-size:8.5pt;color:#8f887c;margin-top:1.5mm}
.months{display:grid;grid-template-columns:repeat(3,1fr);gap:3.5mm;margin-top:6mm}
.mo{border:1px solid rgba(255,204,102,.2);border-radius:3mm;padding:3.5mm;min-height:44mm}
.moname{font-size:8pt;letter-spacing:3px;color:#a59f93;text-transform:uppercase}
.monum{font-family:L;font-size:24pt;color:#ffcc66;line-height:1.2}
.motxt{font-size:9pt;color:#ddd5c6;line-height:1.4}
.compat{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin:6mm 0}
.compat>div{border:1px solid rgba(255,204,102,.2);border-radius:3mm;padding:4mm}
.compat h4{font-size:8pt;letter-spacing:3px;color:#a59f93;text-transform:uppercase}
.cn{font-family:L;font-size:22pt;color:#ffcc66;margin:2mm 0}
.compat p{font-size:9pt;line-height:1.5}
.angel{display:flex;gap:6mm;align-items:center;border-bottom:1px solid rgba(255,255,255,.08);padding:5mm 0;font-size:11pt}
.anum{font-family:L;font-size:28pt;color:#ffcc66;min-width:40mm}
.close{display:flex;flex-direction:column;align-items:center;padding-top:20mm}
.disc{font-size:8pt;color:#6f685d;text-align:center;margin-top:14mm}
.tr{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:8mm;border-top:1px solid rgba(255,204,102,.18);padding-top:6mm}
.tr h4{font-size:8pt;letter-spacing:3px;color:#a59f93;text-transform:uppercase;margin-bottom:3mm}
.chip{display:inline-block;border:1px solid rgba(255,204,102,.45);color:#ffdc8c;border-radius:20px;padding:1.5mm 4mm;margin:0 2mm 2.5mm 0;font-size:9.5pt}
.chip.dim{border-color:rgba(255,255,255,.2);color:#cfc6b6}
.tr ul{list-style:none}.tr li{font-size:11pt;line-height:1.5;padding:1.5mm 0 1.5mm 5mm;position:relative;color:#ddd5c6}.tr li:before{content:'✦';position:absolute;left:0;color:#ffcc66;font-size:8pt;top:2.6mm}
.lines div{border-bottom:1px solid rgba(255,255,255,.16);height:9mm}
.q{font-family:L;font-style:italic;font-size:12.5pt;color:#f1ead9;margin-top:7mm}
.try{margin-top:8mm;border:1px solid rgba(255,204,102,.45);border-radius:4mm;padding:5mm 6mm;background:rgba(255,204,102,.06);font-size:11pt;line-height:1.6;color:#efe7d6}
.tryk{font-size:8pt;letter-spacing:4px;color:#ffcc66;font-weight:700;margin-bottom:2mm}
.chk{margin-top:3mm;font-size:9pt;color:#a59f93}.box{display:inline-block;width:3.5mm;height:3.5mm;border:1px solid #ffcc66;vertical-align:middle}
.mline{border-bottom:1px solid rgba(255,255,255,.14);height:6mm}
.log{width:100%;border-collapse:collapse;margin-top:6mm;font-size:9pt}
.log th{text-align:left;font-size:7.5pt;letter-spacing:2px;color:#ffcc66;padding:2mm;border-bottom:1px solid rgba(255,204,102,.4);text-transform:uppercase}
.log td{border-bottom:1px solid rgba(255,255,255,.12);height:10.5mm;padding:0 2mm;color:#8f887c}
.log td:first-child{width:12mm;font-family:L;color:#ffcc66}
.pfoot{position:absolute;left:20mm;right:20mm;bottom:10mm;display:flex;justify-content:space-between;font-size:7pt;letter-spacing:3px;color:#5f594f;border-top:1px solid rgba(255,255,255,.07);padding-top:3mm}
</style></head><body>${pages.join('')}</body></html>`;
}

