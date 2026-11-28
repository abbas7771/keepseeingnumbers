// Angel number search: go to the guide if it exists, otherwise give a digit reading.
(function () {
  var D = {"0":"potential and new cycles","1":"new beginnings and independence","2":"balance and partnership",
    "3":"creativity and expression","4":"structure and steady work","5":"change and freedom",
    "6":"home, care and responsibility","7":"reflection and inner wisdom","8":"abundance and personal power",
    "9":"completion and compassion"};
  var list = null;
  function load() {
    if (list) return Promise.resolve(list);
    return fetch("/angel-numbers/numbers.json").then(function (r) { return r.json(); })
      .then(function (j) { list = j; return j; }).catch(function () { list = {}; return list; });
  }
  function rootLine(n) {
    if (n === "11" || n === "22" || n === "33") return n.split("").join("+") + " = " + (2 * +n[0]) + " (master number " + n + ")";
    if (/^0+$/.test(n)) return "0 (pure potential)";
    var parts = [], cur = n;
    while (cur.length > 1) {
      var s = String(cur.split("").reduce(function (a, d) { return a + +d; }, 0));
      parts.push(cur.split("").join("+") + " = " + s); cur = s;
    }
    return parts.join(", ") || n;
  }
  function rootOf(n) {
    if (/^(11|22|33)$/.test(n)) return n;
    var cur = n;
    while (cur.length > 1) cur = String(cur.split("").reduce(function (a, d) { return a + +d; }, 0));
    return cur;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]; }); }
  function show(n, j) {
    var out = document.getElementById("aout");
    if (!n) { out.innerHTML = "Type a number with 1 to 6 digits, like 1717 or 11:11."; return; }
    if (j[n] !== undefined) { location.href = "/angel-numbers/" + n + "/"; return; }
    var seen = [], rows = "";
    n.split("").forEach(function (d) { if (seen.indexOf(d) < 0) { seen.push(d); rows += "<li><b>" + d + "</b>: " + D[d] + "</li>"; } });
    var links = [];
    seen.forEach(function (d) { [d + d + d + d, d + d + d].forEach(function (x) { if (j[x] !== undefined && links.indexOf(x) < 0) links.push(x); }); });
    var r = rootOf(n);
    [r, r + r + r].forEach(function (x) { if (j[x] !== undefined && links.indexOf(x) < 0) links.push(x); });
    out.innerHTML = '<div class="card"><p><b>' + esc(n) + "</b>: our full guide to this number is not written yet. Here is a quick reading from its digits.</p>" +
      "<ul style=\"margin:0 0 10px 18px\">" + rows + "</ul><p>Root number: " + esc(rootLine(n)) + ". The root is read as the overall theme.</p>" +
      (links.length ? "<p>Read more: " + links.map(function (x) { return '<a href="/angel-numbers/' + x + '/">' + x + "</a>"; }).join(" · ") + "</p>" : "") +
      "</div>";
  }
  window.ksnSearch = function (e) {
    if (e) e.preventDefault();
    var raw = document.getElementById("aq").value || "";
    var n = raw.replace(/\D/g, "").slice(0, 6);
    load().then(function (j) { show(n, j); });
    return false;
  };
  document.addEventListener("DOMContentLoaded", function () {
    var q = new URLSearchParams(location.search).get("q");
    if (q && document.getElementById("aq")) { document.getElementById("aq").value = q; window.ksnSearch(); }
  });
})();
