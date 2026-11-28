# Writing angel-number pages (Keep Seeing Numbers)

The order of numbers is fixed in `content/angels/_plan.txt` (top = next to write).
A number is "done" once `content/angels/<n>.json` exists.

## Per batch

1. Take the next N numbers from `_plan.txt` that have no `content/angels/<n>.json`.
2. For each, write `content/angels/_raw/<n>.json`:

```json
{"number":"9090",
 "tag":"SHORT UPPERCASE THEME (2-4 words)",
 "keyword":"One-line key message, sentence case",
 "lead":"2-3 sentences: which digits it combines and what it is read as.",
 "meaning":"2-3 sentences of numerology reading specific to THIS number's digits and pattern.",
 "single":"1-2 sentences for single readers.",
 "couple":"1-2 sentences for people in a relationship.",
 "twin":"1 sentence: how twin flame readers interpret it.",
 "career":"1-2 sentences on work and money (add 'It is not financial advice.' when money is the theme).",
 "spirit":"1 sentence starting 'Spiritually, <n> ...'.",
 "steps":["Three short imperative steps","...","..."]}
```

3. Run `python3 tools/compose_angels.py` (assigns publish dates, 10/day after the last scheduled date),
   then `python3 tools/build_angels.py` (builds only pages whose date has arrived).
4. Commit on a branch `angel-batch-<k>` and open a PR to main. The daily workflow `angels-daily` publishes them.

## Rules (quality and honesty)

- Original wording only. Never copy or paraphrase other sites.
- Use standard Pythagorean digit meanings: 0 potential, 1 beginnings, 2 partnership/balance, 3 expression,
  4 structure, 5 change, 6 love/home, 7 reflection/wisdom, 8 abundance/power, 9 completion. 11/22/33 are master numbers.
- Do not state a root number in the text unless you computed it; the composer adds the root math automatically.
- Phrase meanings as interpretation ("is read as", "numerologists see"), never as fact or prediction.
- No invented statistics, quotes, studies or historical claims. No health, legal or investment promises.
- Each number gets its own angle: what is different about its digit order, repetition or mirror shape.
  Do not reuse the same sentences across numbers.
- Plain English, short sentences, no emoji.
