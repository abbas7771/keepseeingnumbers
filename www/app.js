// Keep Seeing Numbers Android app.
// Content comes from keepseeingnumbers.com (read-only). Full readings unlock with a rewarded ad.
(function () {
  const SITE = "https://keepseeingnumbers.com";
  // AdMob ids. Test ids until the real AdMob app is set up (see ADMOB.md).
  const AD_UNIT_REWARDED = window.KSN_REWARDED_ID || "ca-app-pub-3940256099942544/5224354917";
  const AD_TESTING = !window.KSN_REWARDED_ID;
  const FREE_PER_DAY = 2;

  const $ = id => document.getElementById(id);
  const P = (window.Capacitor && window.Capacitor.Plugins) || {};
  const AdMob = P.AdMob, Browser = P.Browser;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const sum = n => String(n).split("").reduce((a, b) => a + +b, 0);
  const red = (n, m) => { while (n > 9 && !(m && (n === 11 || n === 22 || n === 33))) n = sum(n); return n; };
  const today = () => new Date().toISOString().slice(0, 10);
  const store = {
    get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  const openUrl = url => { url = url.startsWith("http") ? url : SITE + url; if (Browser) Browser.open({ url }); else window.open(url, "_blank"); };
  document.addEventListener("click", e => {
    const a = e.target.closest("a[href]");
    if (a && !a.dataset.n) { e.preventDefault(); openUrl(a.getAttribute("href")); }
  });

  /* ---------- ads ---------- */
  let adReady = false;
  async function initAds() {
    if (!AdMob) return;
    try {
      await AdMob.initialize({ initializeForTesting: AD_TESTING });
      try {
        const c = await AdMob.requestConsentInfo();
        if (c && c.isConsentFormAvailable && c.status === "REQUIRED") await AdMob.showConsentForm();
      } catch (e) {}
      preload();
    } catch (e) {}
  }
  async function preload() {
    if (!AdMob) return;
    try { await AdMob.prepareRewardVideoAd({ adId: AD_UNIT_REWARDED, isTesting: AD_TESTING }); adReady = true; } catch (e) { adReady = false; }
  }
  // Resolves true when the reading may be shown. If no ad can be shown, the reading still opens.
  async function watchAd() {
    if (!AdMob) return true;
    try {
      if (!adReady) await AdMob.prepareRewardVideoAd({ adId: AD_UNIT_REWARDED, isTesting: AD_TESTING });
      adReady = false;
      const reward = await AdMob.showRewardVideoAd();
      preload();
      return !!reward;
    } catch (e) { preload(); return true; }
  }
  function canOpenFree(n) {
    const u = store.get("ksn_unlocks", {});
    if (u.day !== today()) { u.day = today(); u.free = 0; u.nums = []; }
    if (u.nums.includes(n)) return true;
    if (u.free < FREE_PER_DAY) { u.free++; u.nums.push(n); store.set("ksn_unlocks", u); return true; }
    store.set("ksn_unlocks", u); return false;
  }
  function markUnlocked(n) {
    const u = store.get("ksn_unlocks", {}); if (u.day !== today()) { u.day = today(); u.free = 0; u.nums = []; }
    if (!u.nums.includes(n)) u.nums.push(n); store.set("ksn_unlocks", u);
  }

  /* ---------- tabs ---------- */
  document.querySelectorAll("nav.tabs button").forEach(b => b.onclick = () => {
    document.querySelectorAll("nav.tabs button").forEach(x => x.classList.toggle("on", x === b));
    document.querySelectorAll(".view").forEach(v => v.classList.toggle("on", v.id === b.dataset.v));
    scrollTo(0, 0);
  });

  /* ---------- number lookup ---------- */
  let list = null;
  const load = () => list ? Promise.resolve(list) :
    fetch(SITE + "/angel-numbers/numbers.json").then(r => r.json()).then(j => (list = j)).catch(() => (list = {}));

  ["111", "222", "333", "444", "555", "777", "1111", "1212"].forEach(n => {
    const c = document.createElement("button"); c.textContent = n; c.onclick = () => { $("q").value = n; look(n); }; $("chips").appendChild(c);
  });

  function freePart(d) {
    return '<div class="big">' + esc(d.number) + '</div><span class="tag">' + esc(d.tag) + '</span>' +
      '<p>' + esc(d.lead) + '</p>' + (d.meaning ? '<p>' + esc(d.meaning) + '</p>' : '') +
      '<div class="kv"><span>Key message</span><span>' + esc(d.keyword) + '</span></div>' +
      '<div class="kv"><span>Root number</span><span>' + esc(d.root) + '</span></div>' +
      '<div class="kv"><span>Where you see it</span><span>' + esc(d.seen) + '</span></div>';
  }
  function lockedPart(d, full) {
    let h = '';
    if (d.love) h += '<h3>Love</h3><p>' + esc(d.love) + '</p>';
    if (d.career) h += '<h3>Money & career</h3><p>' + esc(d.career) + '</p>';
    if (d.y2027) h += '<h3>2027</h3><p>' + esc(d.y2027) + '</p>';
    h += '<h3>What to do today</h3><ol>' + d.steps.map(s => "<li>" + esc(s) + "</li>").join("") + '</ol>';
    if (d.faq) h += '<h3>Questions</h3>' + d.faq.map(f => "<details><summary>" + esc(f[0]) + "</summary><p>" + esc(f[1]) + "</p></details>").join("");
    if (full) h += '<a class="more" href="' + d.url + '">Read the full guide on the website →</a>';
    else h += '<p class="note">This quick reading is built from the standard meaning of each digit. A full guide to ' + esc(d.number) + ' is on its way.</p>';
    return h;
  }
  function render(d, full) {
    const out = $("out");
    const open = canOpenFree(d.number);
    out.innerHTML = '<div class="card">' + freePart(d) + '<div id="rest">' + (open ? lockedPart(d, full) :
      '<div class="lock"><p>Love, money, 2027 and your 3 steps for today</p><button class="btn w" id="unlock">Watch a short ad to unlock</button><p class="note">You get ' + FREE_PER_DAY + ' free full readings every day.</p></div>') + '</div></div>';
    const b = $("unlock");
    if (b) b.onclick = async () => {
      b.disabled = true; b.textContent = "Loading…";
      if (await watchAd()) { markUnlocked(d.number); $("rest").innerHTML = lockedPart(d, full); }
      else { b.disabled = false; b.textContent = "Watch a short ad to unlock"; }
    };
  }
  function look(n) {
    n = n || ($("q").value || "").replace(/\D/g, "").slice(0, 6);
    const out = $("out");
    if (!n) { out.innerHTML = '<p class="err">Type a number with 1 to 6 digits.</p>'; return; }
    out.innerHTML = '<p class="sub">Looking up ' + esc(n) + '…</p>';
    load().then(() => fetch(SITE + "/angel-numbers/data/" + n + ".json"))
      .then(r => { if (!r.ok) throw 0; return r.json(); })
      .then(d => render(d, true))
      .catch(() => { const q = window.ksnQuick(n); q.url = SITE + "/angel-numbers/" + n + "/"; render(q, false); });
  }
  $("f-num").onsubmit = e => { e.preventDefault(); look(); };

  /* ---------- my numbers ---------- */
  const M = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const LP = { 1: "The Leader", 2: "The Peacemaker", 3: "The Communicator", 4: "The Builder", 5: "The Free Spirit", 6: "The Nurturer", 7: "The Seeker", 8: "The Powerhouse", 9: "The Old Soul", 11: "The Intuitive Messenger", 22: "The Master Builder", 33: "The Master Teacher" };
  const PY = { 1: "A Year of New Beginnings", 2: "A Year of Patience & Partnership", 3: "A Year of Expression & Joy", 4: "A Year of Building", 5: "A Year of Change & Freedom", 6: "A Year of Love & Responsibility", 7: "A Year of Reflection", 8: "A Year of Power & Results", 9: "A Year of Completion" };
  $("bd").add(new Option("Day", "")); for (let i = 1; i <= 31; i++) $("bd").add(new Option(i, i));
  $("bm").add(new Option("Month", "")); M.forEach((x, i) => $("bm").add(new Option(x, i + 1)));
  const saved = store.get("ksn_bday", {});
  if (saved.d) $("bd").value = saved.d; if (saved.m) $("bm").value = saved.m; if (saved.y) $("by").value = saved.y;
  const valid = (d, m, y) => { if (!d || !m || !y || y < 1900 || y > new Date().getFullYear()) return false; return new Date(y, m - 1, d).getMonth() === m - 1; };
  $("calc").onclick = () => {
    const d = +$("bd").value, m = +$("bm").value, y = +$("by").value;
    if (!valid(d, m, y)) { $("merr").textContent = "Please choose your full birth date."; return; }
    $("merr").textContent = ""; store.set("ksn_bday", { d, m, y });
    const a = red(m, true), b = red(d, true), c = red(sum(y), true), lp = red(a + b + c, true);
    const py = red(red(d) + red(m) + 2);
    const now = new Date(), pday = red(sum(m) + sum(d) + sum(now.getFullYear()) + sum(now.getMonth() + 1) + sum(now.getDate()));
    $("mine").innerHTML = '<div class="card"><div class="res"><div><b>' + lp + '</b><span>LIFE PATH</span></div><div><b>' + py + '</b><span>2027 YEAR</span></div><div><b>' + pday + '</b><span>TODAY</span></div></div>' +
      '<h3>Life Path ' + lp + ': ' + esc(LP[lp]) + '</h3><p>' + M[m - 1] + ' → ' + a + ' · Day ' + d + ' → ' + b + ' · ' + y + ' → ' + c + ' · ' + a + '+' + b + '+' + c + ' → ' + lp + '</p><a class="more" href="/life-path/' + lp + '/">What Life Path ' + lp + ' means →</a>' +
      '<h3>2027 Personal Year ' + py + '</h3><p>' + esc(PY[py]) + '.</p><a class="more" href="/numerology-2027/personal-year-' + py + '/">Your 2027, month by month →</a></div>';
  };

  initAds();
})();
