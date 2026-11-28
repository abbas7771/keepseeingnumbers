import json, datetime, hashlib, os, re
import glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "content/angels")
RAW = os.path.join(OUT, "_raw")
PER_DAY = 10
FIELDS = ["tag","keyword","lead","meaning","single","couple","twin","career","spirit","steps"]

LEGACY = ["000","111","222","333","444","555","666","777","888","999","1111","1212","1010","1234","2222"]
B1 = ["0000","3333","4444","5555","6666","7777","8888","9999","11","22"]
pub = {n: "2026-11-28" for n in LEGACY}
for f in glob.glob(os.path.join(OUT, "*.json")):
    p = json.load(open(f)); pub[p["number"]] = p["published"]
plan = open(os.path.join(OUT, "_plan.txt")).read().split()
D = {}
for f in glob.glob(os.path.join(RAW, "*.json")):
    j = json.load(open(f)); n = j["number"]
    if n not in pub:
        missing = [k for k in FIELDS if not j.get(k)]
        if missing: sys.exit(f"{n}: missing {missing}")
        D[n] = tuple(j[k] for k in FIELDS)
nums = [n for n in plan if n in D]
extra = set(D) - set(nums)
if extra: sys.exit(f"not in plan: {sorted(extra)}")
last = max(pub.values())
start = max(datetime.date.fromisoformat(last) + datetime.timedelta(days=1),
            (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)).date() + datetime.timedelta(days=1))
for i, n in enumerate(nums):
    pub[n] = (start + datetime.timedelta(days=i // PER_DAY)).isoformat()

def live_at(n, date):
    return n in pub and pub[n] <= date

RM = {"1": "new beginnings and independence", "2": "balance and partnership", "3": "creativity and expression",
      "4": "structure and steady work", "5": "change and freedom", "6": "love, home and responsibility",
      "7": "reflection and inner wisdom", "8": "abundance and personal power", "9": "completion and compassion",
      "11": "intuition (master number 11)", "22": "the master builder (master number 22)", "33": "the master teacher (master number 33)", "0": "pure potential"}
Y27 = {
 "1": "Its root of 1 is about starting. In 2027, an 11/2 year (2+0+2+7 = 11, then 2) that favours partnership, the best new starts are the ones you make with good people around you.",
 "2": "Its root of 2 matches the year itself: 2027 adds up to 11 and then 2 (2+0+2+7 = 11, 1+1 = 2). That makes this number especially relevant for 2027's themes of partnership, patience and intuition.",
 "3": "Its root of 3 is about expression. In 2027, an 11/2 year (2+0+2+7 = 11, then 2), sharing ideas with others and creating together fits the year's partnership energy.",
 "4": "Its root of 4 is about structure. 2027 is an 11/2 year (2+0+2+7 = 11, then 2), full of intuition and ideas, and a 4-root number helps give those ideas something solid to stand on.",
 "5": "Its root of 5 is about change. 2027 is an 11/2 year (2+0+2+7 = 11, then 2), so changes go best when they are talked through and shared rather than made alone.",
 "6": "Its root of 6 is about love and home. 2027 is an 11/2 year (2+0+2+7 = 11, then 2), a partnership year, which makes care for your closest relationships a strong focus.",
 "7": "Its root of 7 is about inner wisdom, and 2027 adds up to 11 (2+0+2+7), the master number of intuition. Trusting your own read on situations matters a lot in the year ahead.",
 "8": "Its root of 8 is about results. In 2027, an 11/2 year (2+0+2+7 = 11, then 2), success is more likely to come through cooperation than through going it alone.",
 "9": "Its root of 9 is about completion. Seen in late 2026, it is read as a cue to finish the year cleanly before 2027, an 11/2 year of new partnerships and intuition (2+0+2+7 = 11, then 2).",
 "11": "Its root is 11, and 2027 also adds up to 11 (2+0+2+7). That makes this number one of the most directly connected to the year ahead: a year of intuition, sensitivity and partnership.",
 "22": "Its root is the master builder 22. 2027 adds up to 11 (2+0+2+7), the visionary number, and 22 is read as the builder who turns that vision into something real.",
 "33": "Its root is 33, the master teacher. In 2027, an 11/2 year (2+0+2+7 = 11, then 2), sharing what you know with the people around you fits the year's partnership energy.",
 "0": "2027 adds up to 11 and then 2 (2+0+2+7 = 11, then 2): a year of intuition and partnership. 0 is read as the open space before that cycle starts.",
}

def root(n):
    if n in ("11", "22", "33"): return n
    c = n
    while len(c) > 1:
        c = str(sum(map(int, c)))
        if c in ("11", "22"): return c
    return c

def root_math(n):
    if n == "0": return "0 has no root: it is pure potential."
    parts, c = [], n
    while len(c) > 1:
        s = str(sum(map(int, c))); parts.append(f"{'+'.join(c)} = {s}"); c = s
        if c in ("11", "22"): break
    return ", ".join(parts)

def clock(n):
    if len(n) == 4:
        h, m = int(n[:2]), int(n[2:])
        if h < 24 and m < 60:
            t = f"{n[:2]}:{n[2:]}"
            if h <= 12 and h > 0:
                return f"{t} on any clock", True
            return f"{t} on a 24-hour clock", True
    if len(n) == 3 and n[0] != "0":
        h, m = int(n[0]), int(n[1:])
        if m < 60:
            return f"{n[0]}:{n[1:]} on a 12-hour clock", True
    if len(n) == 2:
        return f"{n}:{n} on a clock, dates and page numbers" if int(n) < 24 else "receipts, prices and page numbers", int(n) < 24
    return "receipts, prices, addresses and phone numbers", False

WHY = [
 "Psychologists call this the frequency illusion: once a pattern means something to you, you start noticing it more. In numerology, the useful question is not whether the number is 'sent', but what you were thinking about when you saw it.",
 "Part of the reason is simple attention: once a number catches your eye, your brain flags it every time. Numerologists use that moment as a prompt. Notice your thought when the number appears.",
 "Repeated sightings often come from a mix of habit and attention, which psychologists call the frequency illusion. Numerology treats each sighting as a moment to check in with yourself.",
]

def comparisons(n, date):
    out = []
    rev = n[::-1]
    if rev != n and live_at(rev, date):
        out.append(f'<a href="/angel-numbers/{rev}/">{rev}</a> uses the same digits in reverse order, so it is read with the same ingredients but a different emphasis: it starts from {rev[0]} ({RM[rev[0]]}) instead of {n[0]} ({RM[n[0]]}).')
    seen = []
    for d in n:
        if d in seen: continue
        seen.append(d)
        for x in (d * 4, d * 3):
            if x != n and live_at(x, date):
                out.append(f'<a href="/angel-numbers/{x}/">{x}</a> is the pure form of the digit {d} in this number, so reading it helps you understand the {RM[d]} side of {n}.')
                break
    r = root(n)
    for x in ((r * 3) if len(r) == 1 else r,):
        if x != n and live_at(x, date) and x not in "".join(out):
            out.append(f'<a href="/angel-numbers/{x}/">{x}</a> carries the energy of this number\'s root, {r}, on its own.')
    return out

def related(n, date):
    cands = [n[::-1]] + [d * 4 for d in n] + [d * 3 for d in n]
    r = root(n); cands += [r * 3 if len(r) == 1 else r]
    if len(n) == 4 and n[:2] == n[2:]:
        cands += [n[2:] + n[:2]]
    seen, out = set(), []
    for x in cands:
        if x != n and x not in seen and live_at(x, date):
            seen.add(x); out.append(x)
    for x in B1 + LEGACY:
        if len(out) >= 4: break
        if x != n and x not in seen: seen.add(x); out.append(x)
    return out[:4]

def title_case(s):
    return " ".join(w.capitalize() if w not in ("and", "of", "to", "in", "a") else w for w in s.lower().split())

for i, n in enumerate(nums):
    tag, kw, lead, meaning, single, couple, twin, career, spirit, steps = D[n]
    date = pub[n]
    r = root(n)
    where, isclock = clock(n)
    rm = root_math(n)
    meaning_html = f"<p>{meaning}</p>"
    if "root" not in lead + meaning and n != "0":
        meaning_html += f"<p>Its digits add up like this: {rm}. So its root number is {r}, read as {RM[r]}. In numerology the root is the overall theme that sits under the visible digits.</p>"
    h = int(hashlib.md5(n.encode()).hexdigest(), 16)
    why = (f"<p>{n} can show up as {where}, so it is easy to meet more than once in a day.</p>" if isclock
           else f"<p>{n} is not a clock time, so people usually notice it on {where}.</p>")
    why += f"<p>{WHY[h % 3]}</p>"
    secs = [
        (f"What does {n} mean in numerology?", meaning_html),
        (f"Why do I keep seeing {n}?", why),
        (f"What does {n} mean in love?", f"<p><b>If you are single:</b> {single}</p><p><b>If you are in a relationship:</b> {couple}</p>"),
        (f"Is {n} a twin flame number?", f"<p>{twin} Treat it as a prompt for reflection, not a promise about how a connection will turn out.</p>"),
        (f"What does {n} mean for money and career?", f"<p>{career}</p>"),
        (f"What does {n} mean spiritually?", f"<p>{spirit}</p>"),
    ]
    comp = comparisons(n, date)
    if comp:
        secs.append((f"How is {n} related to other angel numbers?", "<ul style=\"margin:0 0 14px 20px\">" + "".join(f"<li style=\"margin-bottom:8px;color:#ddd5c6\">{c}</li>" for c in comp) + "</ul>"))
    T = title_case(tag)
    p = dict(
        number=n, tag=tag, keyword=kw,
        title=f"{n} Angel Number Meaning: {T}, Love & Twin Flame",
        desc=f"What does {n} mean? In numerology, {n} is read as: {kw.lower()}. Meaning for love, career, twin flames and what to do when you see it."[:158],
        h1=f"What Does <em>{n}</em> Mean? {T}",
        lead=lead, clock=where[0].upper() + where[1:], sections=secs, steps=steps,
        y2027=f"<p>{Y27[r]}</p>",
        faq=[
            (f"What does {n} mean?", f"In numerology, {n} is read as: {kw.lower()}. {lead.split('. ')[0].rstrip('.')}."),
            (f"What does {n} mean in love?", f"{single} {couple}"),
            (f"What is the root number of {n}?", (f"{rm}. The root is {r}, read as {RM[r]}." if n != "0" else rm)),
            (f"What should I do when I see {n}?", " ".join(s.rstrip(".") + "." for s in steps)),
        ],
        related=related(n, date), published=date, modified=date,
    )
    json.dump(p, open(f"{OUT}/{n}.json", "w"), indent=1, ensure_ascii=False)
print("composed", len(nums), (pub[nums[0]], pub[nums[-1]]) if nums else "")
