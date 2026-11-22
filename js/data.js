// Keep Seeing Numbers — report content & calculations
const NAMES = {1:"The Leader",2:"The Peacemaker",3:"The Communicator",4:"The Builder",5:"The Free Spirit",6:"The Nurturer",7:"The Seeker",8:"The Powerhouse",9:"The Old Soul",11:"The Intuitive Messenger",22:"The Master Builder",33:"The Master Teacher"};
const KEYS = {1:"Independence · Courage · Beginnings",2:"Harmony · Intuition · Partnership",3:"Creativity · Expression · Joy",4:"Stability · Discipline · Foundation",5:"Freedom · Adventure · Change",6:"Love · Responsibility · Home",7:"Wisdom · Mystery · Inner truth",8:"Ambition · Abundance · Authority",9:"Compassion · Wisdom · Completion",11:"Inspiration · Insight · Awakening",22:"Vision · Legacy · Mastery",33:"Healing · Devotion · Guidance"};

const LIFE = {
1:{essence:"You came here to go first. You feel most alive when you're building something from nothing and doing it your own way. Life keeps placing you in situations where you have to stand alone for a while — not as punishment, but as training. Every time you trust your own judgment, your path gets clearer.",
 gift:"Raw willpower and originality. When you decide something, you find a way — even when nobody else believes in it yet. You see possibilities before they exist.",
 shadow:"You can confuse needing help with being weak and carry everything alone until you burn out. Impatience and pride can push away the very people who want to support you.",
 love:"You need a partner who admires your fire instead of trying to dim it. Respect matters more to you than constant reassurance. Your growth in love is learning that letting someone in doesn't cost you your independence.",
 work:"Founder, freelancer, team lead, creator of your own system. You thrive where you can call the shots and struggle anywhere you're micromanaged.",
 lesson:"Courage without isolation. Lead — but let others walk beside you.",
 aff:"I trust myself to begin."},
2:{essence:"You feel the room before anyone speaks. You came here to bring people together and to turn tension into balance. Your power is quiet, but it's real: things simply go better when you're involved.",
 gift:"Deep emotional intelligence. People open up to you without knowing why, and you notice the details everyone else misses.",
 shadow:"You can shrink your own needs to keep others comfortable — then quietly feel unseen. Indecision often comes from fear of disappointing someone.",
 love:"You love wholeheartedly and loyally. Your lesson is to ask for what you need as gently as you give.",
 work:"Counselor, mediator, designer, diplomat, the trusted right hand. You shine in true partnerships rather than solo spotlight roles.",
 lesson:"Your needs are not a burden. Balance includes you.",
 aff:"My needs matter as much as anyone's."},
3:{essence:"You came here to express — through words, art, humor or simply your presence. When you share what you truly feel, you light people up and give them permission to do the same.",
 gift:"You make life feel lighter. Your words and creativity move people more than you realize.",
 shadow:"Scattering your energy across too many things, or hiding real feelings behind jokes. Self-doubt can silence the very voice you came here to use.",
 love:"You need play, conversation and someone who laughs with you. Coldness and silence drain you faster than anything.",
 work:"Creator, writer, speaker, marketer, performer — any role where your voice is the product.",
 lesson:"Focus turns your talent into impact.",
 aff:"My voice is meant to be heard."},
4:{essence:"You're the one who turns ideas into something real. Step by step, brick by brick, you build things that last — careers, homes, families, systems.",
 gift:"Reliability. When you commit, people know it will get done, and done properly.",
 shadow:"Rigidity. Fear of change can keep you in situations long after they stopped serving you.",
 love:"You show love through loyalty and actions, not grand words. You need a partner who values security as much as you do.",
 work:"Engineering, finance, real estate, operations, craftsmanship — anything that rewards structure and patience.",
 lesson:"Stability is a foundation, not a cage.",
 aff:"I build a life that holds me."},
5:{essence:"You came here to experience life fully — new places, people, ideas. Routine feels like a cage, and change is where you come alive.",
 gift:"Adaptability. You thrive where others panic, and you make change look exciting.",
 shadow:"Restlessness. Running from commitment or starting over just as things are getting deep.",
 love:"You need a partner who is also your best friend and travel companion. Freedom inside the relationship is non-negotiable.",
 work:"Sales, travel, media, marketing, entrepreneurship — anything with variety and movement.",
 lesson:"True freedom includes the freedom to stay.",
 aff:"Freedom and commitment can live together."},
6:{essence:"You're the heart of every group. You came here to care, protect and make spaces feel like home.",
 gift:"Unconditional care. People heal and soften in your presence.",
 shadow:"Over-giving and trying to fix everyone — then feeling unappreciated or exhausted.",
 love:"Devoted and romantic. Your lesson is to love people as they are, not as who you hope they'll become.",
 work:"Teaching, healing, design, hospitality, family business — work that serves and beautifies.",
 lesson:"You can't pour from an empty cup.",
 aff:"I care for myself as I care for others."},
7:{essence:"You came here to look beneath the surface. Small talk tires you; truth, meaning and mystery fascinate you.",
 gift:"Depth. You notice what others miss and understand things on a level few people reach.",
 shadow:"Isolation and overthinking — trusting your mind but doubting your heart.",
 love:"You need intellectual and spiritual connection. Time alone is not rejection — it's how you recharge.",
 work:"Research, analysis, technology, writing, spiritual work — anything that rewards deep thought.",
 lesson:"Faith is a form of knowing too.",
 aff:"I trust what I feel, not only what I think."},
8:{essence:"You came here to master the material world — money, influence, results. You think big, and you're built to carry big things.",
 gift:"Natural authority. People follow your vision, and you know how to turn effort into reward.",
 shadow:"Tying your worth to success, or using control to feel safe.",
 love:"You need a strong partner who matches your drive. Lead with heart, not only with strength.",
 work:"Business, finance, leadership, real estate, law — positions with real power and responsibility.",
 lesson:"Power is most beautiful when it serves.",
 aff:"I am worthy beyond what I achieve."},
9:{essence:"You carry a wisdom beyond your years. You came here to give, to heal and to leave the world a little kinder.",
 gift:"Big-picture compassion. You see people's best selves and help them see it too.",
 shadow:"Holding on to the past and finding it hard to let go of people and chapters that have ended.",
 love:"You love deeply and idealistically. Your lesson is to receive love as freely as you give it.",
 work:"Humanitarian work, the arts, teaching, healing, causes bigger than yourself.",
 lesson:"Endings make room for your purpose.",
 aff:"I release what has ended and make room for what's next."},
11:{essence:"11 is a master number — the most intuitive of all. You came here to inspire and to sense what others can't yet see. Your life often feels more intense than other people's, because you're wired to receive more.",
 gift:"Powerful intuition and a presence that awakens something in people. Ideas and insights seem to arrive from nowhere.",
 shadow:"Nervous energy and self-doubt. Your sensitivity can feel like a burden until you learn to channel it.",
 love:"You need a soul-level connection. Shallow relationships leave you feeling empty.",
 work:"Teacher, creator, healer, guide, artist — roles where your vision lifts others.",
 lesson:"Your sensitivity is the instrument, not the problem.",
 aff:"My sensitivity is my strength."},
22:{essence:"22 is the most powerful master number. You came here to turn big dreams into real, lasting structures that help many people.",
 gift:"A rare mix of vision and practicality. You can build things that outlive you.",
 shadow:"Pressure. The weight of your own potential can freeze you before you start.",
 love:"You need a grounded partner who believes in your vision and keeps you human.",
 work:"Architecture, large companies, institutions, projects that change many lives.",
 lesson:"Big visions are built one ordinary day at a time.",
 aff:"I build my vision one real step at a time."},
33:{essence:"33 is the rarest master number. You came here to uplift others through love, guidance and example.",
 gift:"A healing presence. People grow simply by being around you.",
 shadow:"Self-sacrifice. You can give so much that nothing is left for you.",
 love:"Deeply devoted. Your lesson is to let love flow both ways.",
 work:"Teaching, healing, mentoring, creative work that carries a message.",
 lesson:"Love yourself as the first person you serve.",
 aff:"I lead with love — including love for myself."}
};

const EXPRESSION = {
1:"Your name carries the vibration of leadership. You're naturally driven, decisive and original. People expect you to take initiative — and you're happiest when you do. Your talents bloom when you create something that's unmistakably yours.",
2:"Your name carries the vibration of cooperation. You're tactful, perceptive and brilliant at bringing people and ideas together. Your talent works best in partnership — you make every team stronger.",
3:"Your name carries the vibration of expression. Words, design, humor, performance — you were built to communicate. Your talent grows every time you share your work instead of perfecting it in private.",
4:"Your name carries the vibration of mastery through effort. You're organized, dependable and skilled at turning chaos into systems. Your talents are practical and they compound over time.",
5:"Your name carries the vibration of versatility. You learn fast, adapt instantly and can sell an idea to anyone. Your talents shine in fields that change often and reward curiosity.",
6:"Your name carries the vibration of responsibility and beauty. You're a natural caretaker with a strong sense of style and harmony. Your talents are at their best when they make people's lives better.",
7:"Your name carries the vibration of analysis and wisdom. You're thoughtful, precise and drawn to understanding how things really work. Your talent is depth — becoming the expert others turn to.",
8:"Your name carries the vibration of achievement. You have executive energy, financial instinct and the stamina to lead big projects. Your talents are meant to be used at scale.",
9:"Your name carries the vibration of the humanitarian. You're generous, creative and moved by a bigger picture. Your talents reach their peak when they serve something beyond yourself.",
11:"Your name carries the master vibration of inspiration. You have a gift for vision, art and spiritual insight. Your work has the power to move people emotionally.",
22:"Your name carries the master vibration of the builder. You combine big-picture vision with real-world skill. Your talents are meant for projects with lasting impact.",
33:"Your name carries the master vibration of the teacher. You uplift, guide and heal through your words and example. Your talents bloom when you serve with love."
};
const SOUL = {
1:"Deep down, you want to be free to lead your own life. Independence and self-respect matter to you more than approval.",
2:"Deep down, you want love, peace and a true partner. Feeling emotionally safe with someone is your heart's greatest wish.",
3:"Deep down, you want to express yourself and be truly seen. Joy, creativity and connection feed your soul.",
4:"Deep down, you want security and a life that feels solid. Order, loyalty and a home you can rely on bring you peace.",
5:"Deep down, you want freedom and experience. Your soul craves movement, adventure and the feeling that anything is possible.",
6:"Deep down, you want to love and be needed. Family, home and harmony are what your heart secretly builds toward.",
7:"Deep down, you want truth. Quiet time, meaning and understanding the mysteries of life feed you more than anything else.",
8:"Deep down, you want to succeed and be respected. Building something powerful and abundant is your heart's ambition.",
9:"Deep down, you want to make a difference. Compassion and a sense of higher purpose are what truly fulfil you.",
11:"Deep down, you want spiritual connection and to inspire. You long to follow a calling that feels bigger than you.",
22:"Deep down, you want to leave a legacy. You dream of building something that helps many people long after you.",
33:"Deep down, you want to heal and uplift. Unconditional love is the deepest language of your soul."
};
const PERSONALITY = {
1:"People see you as confident, capable and a little bit intimidating at first. You come across as someone who knows where they're going.",
2:"People see you as gentle, approachable and kind. You come across as a safe person to talk to.",
3:"People see you as charming, witty and fun. You come across as the bright spark in the room.",
4:"People see you as solid, practical and trustworthy. You come across as someone who gets things done.",
5:"People see you as exciting, magnetic and free. You come across as someone with great stories.",
6:"People see you as warm, caring and responsible. You come across as someone others can lean on.",
7:"People see you as mysterious, intelligent and reserved. You come across as someone with hidden depths.",
8:"People see you as powerful, polished and successful. You come across as someone in charge.",
9:"People see you as wise, generous and a little dreamy. You come across as an old soul.",
11:"People see you as inspiring and a little otherworldly. You come across as someone who knows things.",
22:"People see you as capable and visionary. You come across as someone destined for something big.",
33:"People see you as nurturing and wise. You come across as a natural guide."
};
const BIRTHDAY = {
1:"Born on a 1 day, you carry a special gift for initiative. You were made to start things.",
2:"Born on a 2 day, you carry a special gift for sensitivity and cooperation.",
3:"Born on a 3 day, you carry a special gift for creativity and communication.",
4:"Born on a 4 day, you carry a special gift for discipline and building.",
5:"Born on a 5 day, you carry a special gift for adaptability and persuasion.",
6:"Born on a 6 day, you carry a special gift for care, responsibility and beauty.",
7:"Born on a 7 day, you carry a special gift for insight and research.",
8:"Born on an 8 day, you carry a special gift for business and leadership.",
9:"Born on a 9 day, you carry a special gift for compassion and vision."
};
const PYEAR = {
1:{t:"A Year of New Beginnings",d:"2027 opens a brand-new 9-year cycle for you. This is a planting year: start the project, make the move, say yes to the idea you've been holding back. What you begin now sets the tone for the next nine years."},
2:{t:"A Year of Patience & Partnership",d:"2027 slows the pace so that what you planted can take root. Relationships, collaborations and emotional healing take centre stage. Progress is quieter but deeper — trust the timing."},
3:{t:"A Year of Expression & Joy",d:"2027 is your year to be seen. Creativity, social life and self-expression expand. Share your work, reconnect with friends and let yourself enjoy the ride."},
4:{t:"A Year of Building",d:"2027 asks for focus and discipline. It's time to build the foundations — health routines, finances, skills. The work feels heavy at times, but it's what makes the next years possible."},
5:{t:"A Year of Change & Freedom",d:"2027 shakes things up. Expect movement — travel, new people, unexpected opportunities. Stay flexible: the changes that surprise you are often the ones that free you."},
6:{t:"A Year of Love & Responsibility",d:"2027 centres on home, family and the heart. Relationships deepen, commitments are made, and you may be called to care for others. Create beauty and harmony around you."},
7:{t:"A Year of Reflection",d:"2027 is an inward year. Study, rest and spiritual growth matter more than hustle. Answers come in quiet moments — protect your alone time."},
8:{t:"A Year of Power & Results",d:"2027 is a harvest year for ambition. Career, money and recognition are highlighted. Step into authority and claim what you've earned."},
9:{t:"A Year of Completion",d:"2027 closes a 9-year cycle. Let go of what is finished — people, habits, chapters. Clearing space now prepares you for the fresh start that follows."}
};
const PMONTH = {
1:"New starts — begin something",2:"Slow down — nurture connections",3:"Express yourself — be social",4:"Get organised — do the work",5:"Expect change — stay flexible",6:"Focus on home & love",7:"Rest, reflect, recharge",8:"Push for results & money",9:"Release & complete"
};
const COMPAT = {
1:{best:[3,5,6],good:[2,9],grow:[1,8]},2:{best:[4,6,8],good:[2,9],grow:[1,5]},3:{best:[1,5,9],good:[3,6],grow:[4,7]},
4:{best:[2,6,8],good:[4,7],grow:[3,5]},5:{best:[1,3,7],good:[5,9],grow:[4,6]},6:{best:[2,4,9],good:[3,6],grow:[5,7]},
7:{best:[4,5,9],good:[7,1],grow:[3,8]},8:{best:[2,4,6],good:[8,1],grow:[7,9]},9:{best:[3,6,7],good:[2,9],grow:[4,8]}
};
const ANGEL = {
1:["111","1111"],2:["222","1212"],3:["333","1313"],4:["444","1414"],5:["555","1515"],6:["666","1616"],7:["777","1717"],8:["888","1818"],9:["999","1919"],11:["1111","11:11"],22:["2222","22:22"],33:["333","3333"]
};
const ANGEL_MEAN = {
"111":"New beginnings — your thoughts are manifesting fast.","1111":"A portal moment — make a wish and align your intentions.","11:11":"A wake-up call — you're exactly where you're meant to be.",
"222":"Balance — trust the process, things are aligning.","1212":"Stay positive — your next step is already forming.","2222":"Partnership and divine timing are on your side.",
"333":"Support surrounds you — express yourself fearlessly.","1313":"Creative growth — follow what excites you.","3333":"Your purpose is expanding.",
"444":"Protection — you're building on solid ground.","1414":"Keep going — your effort is being noticed.",
"555":"Big change is coming — let it in.","1515":"Release old patterns to make room for freedom.",
"666":"Rebalance — return your focus to love and self-care.","1616":"Home and heart need your attention.",
"777":"Spiritual alignment — luck follows your intuition.","1717":"Your inner wisdom is guiding you correctly.",
"888":"Abundance is flowing toward you.","1818":"A financial chapter is shifting in your favour.",
"999":"Completion — something ends so something better can begin.","1919":"Close the chapter with gratitude.",
"22:22":"Master builder energy — build what you dream."
};

// ---------- calculations ----------
const MAP = {a:1,b:2,c:3,d:4,e:5,f:6,g:7,h:8,i:9,j:1,k:2,l:3,m:4,n:5,o:6,p:7,q:8,r:9,s:1,t:2,u:3,v:4,w:5,x:6,y:7,z:8};
const VOWELS = new Set(['a','e','i','o','u']);
const ds = n => String(n).split('').reduce((a,b)=>a + +b, 0);
function red(n, master=true){ while(n>9 && !(master && (n===11||n===22||n===33))) n = ds(n); return n; }
function clean(name){ return name.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z]/g,''); }
function nameNum(name, filter){ let s=0; for(const c of clean(name)){ if(filter(c)) s += MAP[c]; } return red(s); }
function calc(fullName, d, m, y, year=2027){
  const a=red(m), b=red(d), c=red(ds(y));
  const life = red(a+b+c);
  const expression = nameNum(fullName, ()=>true);
  const soul = nameNum(fullName, c=>VOWELS.has(c));
  const personality = nameNum(fullName, c=>!VOWELS.has(c));
  const birthday = red(d, false);
  const pyear = red(red(m,false)+red(d,false)+red(ds(year),false), false);
  const months = Array.from({length:12},(_,i)=>red(pyear + red(i+1,false), false));
  return {life, steps:{a,b,c}, expression, soul, personality, birthday, pyear, months};
}

const TRAITS = {
1:{s:["Decisive","Original","Courageous","Self-driven"],w:["Impatience","Stubbornness","Going it alone"]},
2:{s:["Empathetic","Diplomatic","Intuitive","Loyal"],w:["People-pleasing","Indecision","Over-sensitivity"]},
3:{s:["Expressive","Creative","Charming","Optimistic"],w:["Scattered focus","Hiding behind humor","Self-doubt"]},
4:{s:["Reliable","Disciplined","Practical","Honest"],w:["Rigidity","Overworking","Fear of change"]},
5:{s:["Adaptable","Curious","Persuasive","Adventurous"],w:["Restlessness","Impulsiveness","Avoiding commitment"]},
6:{s:["Caring","Responsible","Protective","Harmonious"],w:["Over-giving","Control","Perfectionism"]},
7:{s:["Insightful","Analytical","Wise","Spiritual"],w:["Isolation","Overthinking","Distrust"]},
8:{s:["Ambitious","Strategic","Confident","Resilient"],w:["Workaholism","Control","Materialism"]},
9:{s:["Compassionate","Generous","Visionary","Wise"],w:["Living in the past","Martyrdom","Scattered giving"]},
11:{s:["Intuitive","Inspiring","Visionary","Sensitive"],w:["Anxiety","Self-doubt","Nervous energy"]},
22:{s:["Visionary","Practical","Powerful","Disciplined"],w:["Pressure","Perfectionism","Overwhelm"]},
33:{s:["Nurturing","Wise","Selfless","Uplifting"],w:["Self-sacrifice","Burnout","Over-responsibility"]}
};
const PYFOCUS = {
1:{f:["Start the project you keep postponing","Set clear intentions for 9 years","Act on new ideas quickly"],a:["Waiting for permission","Dwelling on last year"]},
2:{f:["Deepen key relationships","Collaborate instead of competing","Rest and recover"],a:["Forcing fast results","Ignoring your feelings"]},
3:{f:["Share your work publicly","Socialise and network","Create something for joy"],a:["Scattering your energy","Gossip and drama"]},
4:{f:["Build routines that last","Organise money and health","Commit to a skill"],a:["Shortcuts","Burning out"]},
5:{f:["Travel or change your environment","Say yes to the unexpected","Update old habits"],a:["Reckless decisions","Running from commitments"]},
6:{f:["Invest in home and family","Heal relationships","Beautify your space"],a:["Carrying everyone's problems","Neglecting yourself"]},
7:{f:["Study and learn deeply","Spend time alone and in nature","Develop your intuition"],a:["Isolating completely","Overanalysing"]},
8:{f:["Ask for the raise or the deal","Grow income and assets","Lead with confidence"],a:["Ignoring health for work","Power struggles"]},
9:{f:["Declutter people and habits","Finish open projects","Forgive and release"],a:["Starting big new ventures","Clinging to the past"]}
};

// Paid-report-only content: deeper Life Path, workbook prompts
const DEEP = {
1:{deep:["People with Life Path 1 rarely feel at home following someone else's plan. You may remember early moments where you had to figure things out on your own — and those moments shaped a quiet self-reliance that still runs your life today.",
 "Your path is not about being alone; it's about becoming the author of your own life. The more you act from your own values instead of other people's expectations, the more your energy and luck seem to increase. When you hesitate, life tends to push you until you choose."],
 reflect:["Where in your life are you still waiting for permission?","Name one decision you made completely on your own that you're proud of. What did it teach you?","Who do you allow to help you — and who do you keep at a distance?"],
 tryit:"Pick one small thing you've been postponing because it isn't 'perfect' yet. Start it within 48 hours and give it 20 minutes."},
2:{deep:["Life Path 2 people often grow up as the emotional barometer of their family or friend group — sensing tension before anyone names it. That sensitivity is a real skill, but it can also train you to manage everyone's feelings except your own.",
 "Your path is about partnership done right: relationships where you give and receive in equal measure. Your power grows when you stop shrinking to keep the peace and start trusting that real connection can survive your honesty."],
 reflect:["When did you last say yes when you meant no? What were you afraid would happen?","Which relationship in your life feels truly balanced? What makes it work?","What do you need right now that you haven't asked for?"],
 tryit:"This week, express one honest preference — where to eat, what to watch, how to spend time — without softening it or apologising."},
3:{deep:["Life Path 3 people carry a creative current that needs an outlet. When it's flowing — writing, talking, designing, performing, even storytelling at dinner — you feel alive. When it's blocked, you can feel flat, scattered or misunderstood.",
 "Your path is about turning self-expression into something that touches other people. The challenge is commitment: finishing, publishing, showing up consistently. Your gift multiplies the moment you choose one channel and stay with it long enough for it to grow."],
 reflect:["What did you love creating as a child that you've stopped doing?","Where do you hide your real feelings behind humour or busyness?","Which one creative project deserves your focus for the next 90 days?"],
 tryit:"Share one piece of your work or one honest opinion publicly this week — a post, a story, a message — before you feel fully ready."},
4:{deep:["Life Path 4 people are the ones others quietly rely on. You may have taken on responsibility early, learning that if you don't hold things together, nobody will. That instinct has made you capable — and sometimes exhausted.",
 "Your path is about building something solid that reflects who you really are, not just what's expected. Structure is your superpower when it serves your dreams; it becomes a cage only when you forget to update it."],
 reflect:["Which routine in your life still serves you — and which one is just habit?","What would you build if you knew it would definitely last?","Where are you holding on to security at the cost of growth?"],
 tryit:"Write down your top 3 priorities for the month. Block one fixed hour per week in your calendar for the most important one."},
5:{deep:["Life Path 5 people are wired for experience. You learn by doing, moving and trying — and you probably know the restless feeling when life gets too predictable. Change isn't something that happens to you; it's how you grow.",
 "Your path is about discovering that freedom and depth can coexist. The adventures that change you most are often the ones where you stay long enough to go deep — in a relationship, a skill or a place."],
 reflect:["What are you running toward right now — and what might you be running from?","Which commitment in your life actually gives you more freedom?","What new experience have you been curious about but not tried?"],
 tryit:"Do one thing this week you've never done before — a new route, class, food or conversation — and write down how it changed your mood."},
6:{deep:["Life Path 6 people naturally take care of others. You may be the one friends call in a crisis, the one who remembers birthdays, the one who notices when someone isn't okay. Love, for you, is a verb.",
 "Your path is about learning that caring for yourself is part of caring for others. The more you allow people to be responsible for their own lives, the lighter — and more loving — you become."],
 reflect:["Who are you currently trying to 'fix'? What would happen if you stepped back?","How do you like to be cared for — and do the people close to you know?","What does your ideal home feel like, not just look like?"],
 tryit:"Schedule one hour this week that is only for you — no helping, no fixing — and protect it like an appointment."},
7:{deep:["Life Path 7 people often feel slightly different from the crowd — more inward, more questioning, more drawn to what lies beneath the surface. You need time alone the way others need company.",
 "Your path is about turning knowledge into wisdom. Your mind is brilliant, but your breakthroughs often come when you let your intuition lead and your intellect confirm — not the other way around."],
 reflect:["What question about life keeps returning to you?","When did your gut feeling turn out to be right, even though logic disagreed?","Who in your life truly understands your inner world?"],
 tryit:"Spend 15 minutes alone without your phone every day this week — walking, journaling or sitting quietly. Note one insight each day."},
8:{deep:["Life Path 8 people are built for impact in the material world. You probably have strong opinions about money, success and fairness — often shaped by early experiences of having too little or watching power used badly.",
 "Your path is about mastering power with integrity: building abundance that also lifts the people around you. Your biggest wins come when your ambition is connected to something you genuinely believe in."],
 reflect:["What does 'enough' look like for you — in money, success and recognition?","Where are you holding back from asking for what you're worth?","How do you want people to describe the way you used your power?"],
 tryit:"Write down one financial or career goal for 2027 with a specific number and date. Take one concrete step toward it this week."},
9:{deep:["Life Path 9 people carry an old-soul quality — a sense of having seen a lot, felt a lot and understood a lot. You care about fairness and meaning, and you can feel other people's pain deeply.",
 "Your path is about completion and release: letting go of what has ended so your energy can flow toward a bigger purpose. Your generosity is a gift; your growth lies in letting it include yourself."],
 reflect:["What chapter of your life are you ready to close?","Which cause or group of people moves you most deeply?","Where are you giving more than you can sustain?"],
 tryit:"Let go of one thing this week — an old item, a habit, an unfinished obligation — and write down what space it creates."},
11:{deep:["Life Path 11 is a master number, and people who carry it often describe life as intense: strong emotions, vivid intuitions, a sense that they're meant for something they can't fully name yet. Many 11s spend their early years feeling 'too much' before they learn their sensitivity is an instrument.",
 "Your path is about becoming a channel for inspiration — through creativity, teaching, healing or simply the way you show up for people. The more grounded your daily life is (sleep, routine, people who calm you), the more clearly your intuition can speak."],
 reflect:["List 3 decisions from the last 30 days where you followed a gut feeling. What happened?","When does your sensitivity feel like a burden — and when does it feel like a gift?","Who or what grounds you when your mind gets too loud?"],
 tryit:"For the next 7 days, write down every strong intuition you have in one line. At the end of the week, check which ones proved right."},
22:{deep:["Life Path 22 is the master builder number. You can see the big picture and the practical steps to get there — a rare combination. Many 22s feel a quiet pressure to do something significant with their lives.",
 "Your path is about turning large visions into real, lasting structures. The key is pacing: breaking the dream into daily, ordinary work so the weight of your potential becomes momentum instead of paralysis."],
 reflect:["What is the biggest thing you secretly believe you could build?","Which small step toward it could you finish this month?","Where does perfectionism stop you from starting?"],
 tryit:"Break your biggest goal into 5 steps. Complete the first, smallest step this week — imperfectly."},
33:{deep:["Life Path 33 is the rarest master number — the teacher and healer. People feel safe with you, and you may often find yourself guiding others through hard moments.",
 "Your path is about serving through love without losing yourself. Your influence is strongest when you lead by example and allow others to grow at their own pace."],
 reflect:["Who have you helped most in your life — and how did it change you?","Where do you sacrifice your own needs too easily?","What does 'loving yourself' look like in practical terms this month?"],
 tryit:"Do one kind thing for yourself every day this week that you would normally only do for someone else."}
};
const EXP_REFLECT = {
1:["Which of your ideas have you not acted on yet?","Do something this week where you take the lead."],2:["Where are you the glue in a team?","Offer to help connect two people who should know each other."],
3:["Which talent do people compliment you on most?","Spend 30 minutes creating something just for fun."],4:["What system could make your life easier?","Organise one area of your life you've been avoiding."],
5:["Which skill could you learn fast that would open doors?","Pitch an idea or yourself to someone new."],6:["Where does your sense of beauty show up?","Improve one space you spend time in."],
7:["What subject could you become an expert in?","Go deep: read or study one topic for an hour."],8:["Where could you take on more responsibility?","Take one step toward a leadership role."],
9:["Which cause could use your talents?","Use one of your skills to help someone for free."],11:["What vision keeps visiting you?","Write it down in detail — today."],
22:["What could you build that would help many people?","Sketch the plan on one page."],33:["Who could benefit from your guidance?","Share one lesson you've learned with someone who needs it."]
};
const SOUL_REFLECT = {
1:"Where do you feel most free to be yourself?",2:"When do you feel most loved and safe?",3:"When did you last feel pure joy?",4:"What makes you feel truly secure?",
5:"What would you do with a completely free month?",6:"What does your heart want to nurture?",7:"What truth are you searching for?",8:"What success would truly satisfy you?",
9:"What difference do you want to make?",11:"What calling do you feel but haven't followed?",22:"What legacy would make you proud?",33:"Whom do you most want to uplift?"
};
const PERS_REFLECT = {
1:"Ask a friend for 3 words that describe you. Do they match how you see yourself?",2:"Notice this week when people come to you for comfort.",3:"Notice how your mood changes the room.",
4:"Notice how often people ask you to handle things.",5:"Notice the stories people ask you to tell.",6:"Notice who relies on you this week.",
7:"Notice when people ask you for your opinion.",8:"Notice how people react when you walk into a room.",9:"Notice who seeks your advice.",
11:"Notice who seems inspired after talking to you.",22:"Notice who looks to you for direction.",33:"Notice who feels better after time with you."
};
const PYEAR_MONTH_HINT = "Use these as planning themes, not predictions. Write one intention for each month.";


window.KSN_D={calc,NAMES,KEYS,LIFE,EXPRESSION,SOUL,PERSONALITY,BIRTHDAY,PYEAR,PMONTH,COMPAT,ANGEL,ANGEL_MEAN,TRAITS,PYFOCUS};
window.KSN_W={DEEP,EXP_REFLECT,SOUL_REFLECT,PERS_REFLECT,PYEAR_MONTH_HINT};
