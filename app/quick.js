// Quick readings for any number (0-999999) built from standard Pythagorean digit meanings.
// Used by the app when a number has no full guide yet. Every line is derived from the digits.
(function (g) {
  const DIG = {
    "0": { n: "potential", t: "open potential and new cycles", love: "Zero clears space: it favours a fresh start or an honest reset rather than repeating old patterns.", work: "Zero suits planning and exploring options before you commit to one path.", step: "Write down three options you have not considered yet." },
    "1": { n: "beginnings", t: "new beginnings, independence and initiative", love: "1 asks you to stay yourself in love: say what you want clearly instead of waiting to be asked.", work: "1 favours starting things: a project, a pitch or a role where you lead.", step: "Take the first visible step on something you have been postponing." },
    "2": { n: "partnership", t: "balance, partnership and patience", love: "2 is the most relationship-focused digit: listen closely and look for fair give-and-take.", work: "2 favours teamwork, agreements and quiet diplomacy over solo pushing.", step: "Follow up once with someone you are waiting on, then give it time." },
    "3": { n: "expression", t: "creativity, communication and joy", love: "3 favours open, playful communication: say the kind thing you usually keep to yourself.", work: "3 favours work where your voice or ideas are the product: writing, teaching, design, sales.", step: "Share one idea or piece of work you have been holding back." },
    "4": { n: "structure", t: "structure, discipline and steady work", love: "4 values reliability: trust is built through kept promises and routines.", work: "4 favours systems, planning and long projects that reward patience.", step: "Turn one goal into a small daily habit and do it today." },
    "5": { n: "change", t: "change, freedom and movement", love: "5 brings fresh energy: a new setting, a new experience or more space for each person.", work: "5 favours flexibility, travel, new skills and saying yes to a change you have planned for.", step: "Do one thing differently from your usual routine today." },
    "6": { n: "care", t: "love, home and responsibility", love: "6 is the nurturer: care for others, but check that you are cared for too.", work: "6 favours helping roles: teaching, care, hospitality and anything that supports a household.", step: "Ask for help with one task you usually carry alone." },
    "7": { n: "wisdom", t: "reflection, study and inner wisdom", love: "7 favours depth: real conversations matter more than quick chemistry.", work: "7 favours research, expertise and decisions you have thought through.", step: "Spend 10 quiet minutes with the question on your mind and write what comes." },
    "8": { n: "abundance", t: "abundance, power and results", love: "8 favours confidence and fair exchange: know your worth and expect respect.", work: "8 is the results digit: money, recognition and leadership. It is not financial advice.", step: "Make one practical money or career decision you have been delaying." },
    "9": { n: "completion", t: "completion, compassion and letting go", love: "9 favours closure: let an old story end so something new has room.", work: "9 favours finishing what is open and work with a purpose beyond money.", step: "Finish or let go of one thing that is clearly done." }
  };
  const ROOT = {
    "1": { t: "a new beginning", love: "Overall, this number points to a fresh start in how you approach relationships.", work: "Overall, it favours starting something under your own name.", y: "In 2027, an 11/2 year (2+0+2+7 = 11, then 2), new starts go best with good partners beside you." },
    "2": { t: "balance and partnership", love: "Overall, this number puts the focus on cooperation and patience with the people close to you.", work: "Overall, it favours teamwork and agreements over going it alone.", y: "Its root of 2 matches 2027 itself (2+0+2+7 = 11, then 2), so its themes of partnership and patience are especially relevant next year." },
    "3": { t: "expression and joy", love: "Overall, this number favours honest, light-hearted communication.", work: "Overall, it favours sharing your ideas and creative work.", y: "In 2027, an 11/2 year, sharing ideas with others fits the year's partnership energy." },
    "4": { t: "structure and steady progress", love: "Overall, this number favours building trust slowly and reliably.", work: "Overall, it favours plans, systems and consistent effort.", y: "2027 is an 11/2 year full of ideas; a 4 root helps give those ideas a solid base." },
    "5": { t: "change and freedom", love: "Overall, this number points to change in your love life or routine.", work: "Overall, it favours a planned change of direction.", y: "In 2027, an 11/2 year, changes go best when you talk them through with the people they affect." },
    "6": { t: "love and responsibility", love: "Overall, this number is about care, home and fair sharing of responsibility.", work: "Overall, it favours work that helps or supports people.", y: "2027 is a partnership year (11/2), which makes care for close relationships a strong focus." },
    "7": { t: "reflection and inner wisdom", love: "Overall, this number favours depth and honesty over speed.", work: "Overall, it favours study, expertise and careful decisions.", y: "2027 adds up to 11 (2+0+2+7), the master number of intuition, which fits a 7 root closely." },
    "8": { t: "results and abundance", love: "Overall, this number favours confidence and balanced effort in relationships.", work: "Overall, it favours progress in money and career. It is not financial advice.", y: "In 2027, an 11/2 year, results are more likely to come through cooperation." },
    "9": { t: "completion", love: "Overall, this number points to closing an old chapter in love.", work: "Overall, it favours finishing projects and moving toward meaningful work.", y: "Seen near the end of a year, a 9 root is a cue to finish cleanly before 2027 begins." },
    "11": { t: "intuition (master number 11)", love: "Overall, this number favours trusting your instincts about people.", work: "Overall, it favours ideas, vision and inspiring others.", y: "2027 also adds up to 11 (2+0+2+7), so this number is closely tied to the year ahead." },
    "22": { t: "building something lasting (master number 22)", love: "Overall, this number favours a partnership built around shared long-term goals.", work: "Overall, it favours big plans made real through practical steps.", y: "2027 adds up to 11, the visionary number; a 22 root is read as the builder who makes that vision real." },
    "33": { t: "teaching and compassion (master number 33)", love: "Overall, this number favours kindness and supporting each other's growth.", work: "Overall, it favours teaching, guiding and sharing what you know.", y: "In 2027, an 11/2 year, sharing knowledge with others fits the year well." },
    "0": { t: "pure potential", love: "Overall, this number points to a clean slate.", work: "Overall, it favours exploring before committing.", y: "2027 is an 11/2 year; 0 is read as the open space before that cycle starts." }
  };
  const sum = s => String(s).split("").reduce((a, b) => a + +b, 0);
  function root(n) {
    if (/^0+$/.test(n)) return { r: "0", math: "0 has no root: it is pure potential" };
    if (/^(11|22|33)$/.test(n)) return { r: n, math: n.split("").join("+") + " = " + sum(n) + ", kept as master number " + n };
    const parts = []; let c = n;
    while (c.length > 1) {
      const s = String(sum(c)); parts.push(c.split("").join("+") + " = " + s); c = s;
      if (c === "11" || c === "22") { parts.push("kept as master number " + c); break; }
    }
    return { r: c, math: parts.join(", ") || "a single digit is its own root" };
  }
  function shape(n) {
    const L = n.length, set = new Set(n), d = n.split("").map(Number);
    if (L === 1) return ["single", "As a single digit, " + n + " is read in its purest form: " + DIG[n].t + "."];
    if (L >= 2 && set.size === 1) return ["repeating", "Every digit is the same, so the meaning of " + n[0] + " is amplified with nothing to dilute it."];
    if (L === 4 && n.slice(0, 2) === n.slice(2)) return ["pair", "It repeats the pair " + n.slice(0, 2) + ", which numerologists read as a rhythm: " + DIG[n[0]].n + " and " + DIG[n[1]].n + " taking turns."];
    if (L === 4 && n[0] === n[1] && n[2] === n[3]) return ["double", "It moves from " + n[0] + n[0] + " to " + n[2] + n[2] + ", read as a shift from " + DIG[n[0]].n + " to " + DIG[n[2]].n + "."];
    if (L >= 3 && n === n.split("").reverse().join("")) return ["mirror", "It is a mirror number (it reads the same both ways), which is read as reflection: what you see around you reflects something in you."];
    if (L >= 3 && d.every((x, i) => i === 0 || x - d[i - 1] === 1)) return ["ascending", "Its digits climb in order, read as step-by-step progress."];
    if (L >= 3 && d.every((x, i) => i === 0 || d[i - 1] - x === 1)) return ["descending", "Its digits step down in order, read as winding something down or simplifying."];
    if (L >= 4 && set.size === 2) { const [a, b] = [...set]; const big = n.split(a).length - 1 >= 3 ? a : (n.split(b).length - 1 >= 3 ? b : null);
      if (big) { const other = big === a ? b : a; return ["triple", "Three of its digits are " + big + ", so " + DIG[big].n + " dominates, with one " + other + " adding " + DIG[other].n + "."]; } }
    if (n.includes("0") && set.size > 1) return ["zero", "It contains 0, which numerologists read as amplifying the digits around it."];
    return ["mixed", "It mixes " + set.size + " different digits, so it is read as a blend, led by the digit that appears most or comes first."];
  }
  function clock(n) {
    if (n.length === 4) { const h = +n.slice(0, 2), m = +n.slice(2); if (h < 24 && m < 60) return n.slice(0, 2) + ":" + n.slice(2) + (h > 0 && h <= 12 ? " on any clock" : " on a 24-hour clock"); }
    if (n.length === 3 && n[0] !== "0") { const m = +n.slice(1); if (m < 60) return n[0] + ":" + n.slice(1) + " on a 12-hour clock"; }
    return "receipts, prices, addresses and phone numbers";
  }
  function quick(n) {
    n = String(n).replace(/\D/g, "").slice(0, 6);
    if (!n) return null;
    const cnt = {}; n.split("").forEach(x => cnt[x] = (cnt[x] || 0) + 1);
    const uniq = [...new Set(n)];
    const dom = uniq.filter(x => x !== "0" || uniq.length === 1).sort((a, b) => cnt[b] - cnt[a] || n.indexOf(a) - n.indexOf(b))[0];
    const R = root(n), RR = ROOT[R.r], sh = shape(n);
    const list = uniq.map(x => x + " (" + DIG[x].n + ")");
    const listTxt = list.length > 1 ? list.slice(0, -1).join(", ") + " and " + list[list.length - 1] : list[0];
    const lead = (uniq.length === 1 ? n + " is made only of " + listTxt : n + " combines " + listTxt) + ". In numerology it is read as a number about " + RR.t + ", led by the " + DIG[dom].t + " of " + dom + ".";
    const meaning = sh[1] + " The leading digit is " + dom + ", which stands for " + DIG[dom].t + ". Its root number is " + R.r + " (" + R.math + "), read as " + RR.t + ".";
    const second = (/^[1-9]$/.test(R.r) && R.r !== dom) ? R.r : (uniq.find(x => x !== dom && x !== "0") || dom);
    const steps = [DIG[dom].step, DIG[second].step, "Notice what you were thinking when " + n + " appeared and write it down; after a week, read the list back."];
    return {
      number: n, tag: "QUICK READING", keyword: (RR.t[0].toUpperCase() + RR.t.slice(1)),
      lead, meaning, root: R.math, seen: clock(n), shape: sh[0],
      love: DIG[dom].love + " " + RR.love, career: DIG[dom].work + " " + RR.work,
      y2027: RR.y, steps: [...new Set(steps)].slice(0, 3)
    };
  }
  g.ksnQuick = quick;
})(typeof window !== "undefined" ? window : globalThis);
