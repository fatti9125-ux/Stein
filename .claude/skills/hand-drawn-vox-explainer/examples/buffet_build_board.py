"""Builds editor/storyboard.json for 'Why Buffets Don't Lose Money When You Eat 5 Plates'.
Every element is timed by T('script phrase'), which finds that phrase in the aligned script.
Layout rules (same as Perseus): main figure LEFT x330, second figure RIGHT x1590 (auto-turned to face
inward), props/graphics CENTRE, notes in the top band; one idea per element, nothing overlapping."""
import json, re
TOK = json.load(open('script_words_fa.json'))   # forced-aligned word times
LEAD = 0.15   # visuals land just before the word
DUR = 843.86
N = [t['n'] for t in TOK]
cur = 0

def norm(s): return [re.sub(r"[^a-z0-9]", "", w.lower().replace('’', "'")) for w in re.findall(r"[\w$€¢'’.,%\-]+", s)]

def T(phrase, back=40, end=False):
    """start time of `phrase` in the script, searching forward from the last phrase found"""
    global cur
    p = [w for w in norm(phrase) if w]
    for i in range(max(0, cur - back), len(N) - len(p) + 1):
        if N[i:i + len(p)] == p:
            if i - cur > 400: break
            cur = i
            return round(max(0, (TOK[i + len(p) - 1]['e'] if end else TOK[i]['s']) - LEAD), 2)
    raise SystemExit(f'phrase not found after word {cur}: {phrase!r}')

RED = '#D0362C'
def ch(a, x, at, h=600, y=1030, out=None, **k):
    d = dict(k='img', a=a, x=x, y=y, h=h, at=at, **k)
    if out is not None: d['out'] = out
    return d
def L(a, at, x=330, **k): return ch(a, x, at, **k)
def R(a, at, x=1590, **k): return ch(a, x, at, **k)
def prop(a, x, y, h, at, out=None, **k): return ch(a, x, at, h=h, y=y, out=out, center=1, still=1, **k)
def g(a, x, y, at, h=170, out=None, **k): return prop(a, x, y, h, at, out=out, **k)          # number card
def lab(t, x, y, at, out=None, size=40, **k):
    d = dict(k='text', t=t, x=x, y=y, size=size, at=at, **k)
    if out is not None: d['out'] = out
    return d
def stk(t, x, y, at, out=None, rot=-3, size=40, **k):
    d = dict(k='sticker', t=t, x=x, y=y, at=at, rot=rot, size=size, **k)
    if out is not None: d['out'] = out
    return d
def stp(t, x, y, at, out=None, rot=-6, size=54):
    d = dict(k='stamp', t=t, x=x, y=y, at=at, rot=rot, size=size)
    if out is not None: d['out'] = out
    return d
import os
LIBJ = json.load(open('editor/library.json'))
FALLBACK = {'A-ocb': 'B03-01', 'A-running_sushi': 'B01-03', 'A-vacant_ryans': 'B03-01', 'A-souplantation': 'B04-03',
            'A-vegas_buffet': 'B01-01', 'A-stardust': 'B03-03', 'A-gc_storefront': 'B04-03', 'A-gc_buffet': 'B01-02'}
def arc(a, x, y, w, at, out=None, rot=2):
    if a not in LIBJ:   # photo not downloaded yet: use the matching illustrated plate
        return card(FALLBACK[a], x, y, w, round(w * 9 / 16), at, out=out, rot=rot)
    d = dict(k='archive', a=a, x=x, y=y, w=w, at=at, rot=rot)
    if out is not None: d['out'] = out
    return d
def card(bg, x, y, w, h, at, out=None, rot=-1.5, yellow=True, **k):
    d = dict(k='card', bg=bg, x=x, y=y, w=w, h=h, at=at, rot=rot, yellow=yellow, **k)
    if out is not None: d['out'] = out
    return d
def paper(x, y, w, h, at, out=None, rot=-1, **k):
    d = dict(k='card', x=x, y=y, w=w, h=h, at=at, rot=rot, **k)
    if out is not None: d['out'] = out
    return d
def loop(x, y, rx, ry, at, out=None, color=RED, sw=7):
    d = dict(k='loop', x=x, y=y, rx=rx, ry=ry, at=at, color=color, sw=sw)
    if out is not None: d['out'] = out
    return d
def arrow(x, y, x2, y2, at, out=None, bend=30, color=None):
    d = dict(k='arrow', x=x, y=y, x2=x2, y2=y2, bend=bend, at=at)
    if color: d['color'] = color
    if out is not None: d['out'] = out
    return d
def hl(x, y, w, at, h=34, out=None):
    d = dict(k='hl', x=x, y=y, w=w, h=h, at=at)
    if out is not None: d['out'] = out
    return d
def bub(t, x, y, w, tx, ty, at, out=None, h=110, size=40):
    d = dict(k='bubble', t=t, x=x, y=y, w=w, h=h, tx=tx, ty=ty, at=at, size=size)
    if out is not None: d['out'] = out
    return d
def xm(x, y, at, s=50, out=None):
    d = dict(k='xmark', x=x, y=y, s=s, at=at)
    if out is not None: d['out'] = out
    return d
def fx(name, at, vol=0.6): return dict(k='sfx', a=name, at=at, vol=vol)
def cnt(to, x, y, at, pre='', suf='', dec=0, cap='', size=130, out=None, color=None, frm=0, rot=-2, **k):
    d = dict(k='counter', to=to, x=x, y=y, at=at, pre=pre, suf=suf, dec=dec, cap=cap, size=size, rot=rot, **k)
    if frm: d['from'] = frm
    if color: d['color'] = color
    if out is not None: d['out'] = out
    return d
def bars(rows, x, y, at, title='', w=1100, rh=80, lw=300, out=None, **k):
    d = dict(k='bars', rows=rows, x=x, y=y, at=at, title=title, w=w, rh=rh, lw=lw, **k)
    if out is not None: d['out'] = out
    return d
def icons(x, y, at, n=20, cols=10, hi='19', hiAt=1.4, sz=84, **k): return dict(k='icons', x=x, y=y, at=at, n=n, cols=cols, hi=hi, hiAt=hiAt, sz=sz, **k)
CHAPTERS = []
def chap(n, title, at):
    CHAPTERS.append(dict(s=at, n=n, t=title, d=2.3))
    return dict(k='chapter', n=n, t=title, x=960, y=520, at=at, out=round(at + 2.2, 2))
def reen(at): return g('G06-01', 1690, 1040, at, h=70)          # "illustrated reenactment" tag, bottom-right

S = []
def scene(s, a='', b='', items=()):
    S.append(dict(id=f's{len(S)+1:03d}', s=round(s, 2), e=0, h=dict(a=a, b=b), items=list(items)))

# ======================= Chapter 1: A $17 steak dinner with no limit =======================
t0 = T('From a triathlete')
scene(0, '', '', [
    prop('F03-05', 330, 600, 520, t0), stk('~100 plates of sushi', 330, 250, T('banned'), rot=-4), stp('BANNED', 560, 930, T('banned', end=True), size=60), fx('stamp', T('banned', end=True)),
    card('B05-02', 760, 300, 560, 315, T('forty people'), rot=1.5), stk('40 people, one steak line', 1040, 700, T('brawling'), rot=2), fx('crash', T('brawling'), 0.5),
    R('C03-09', T('golden corral over steak'), x=1660, h=520, out=None), reen(t0),
])
s = T('this is how all-you-can-eat')
scene(s, '', '', [
    paper(360, 330, 1200, 330, s, rot=-1),
    lab('How do buffets make money', 960, 470, s, size=74, cls='serif', italic=True),
    hl(560, 520, 800, T('when people eat'), h=46),
    lab('when people eat like THIS?', 960, 575, T('when people eat'), size=64, cls='anton'),
])
s = T('At a lot of Golden Corrals')
scene(s, 'Golden Corral', 'dinner, tonight', [
    chap(1, 'A $17 steak dinner with no limit', s),
    card('B02-02', 160, 210, 1000, 560, s + 2.0, rot=-1.5, mv=f"{T('seventeen dollars gets')},-60,0,0.9"),
    cnt(17, 1500, 470, T('seventeen dollars gets'), pre='$', cap='all-you-can-eat dinner', size=150), fx('ding', T('dinner'), 0.4),
    stk('not A dinner.', 1520, 640, T('Not a dinner'), rot=3), stk('ALL of it.', 1520, 740, T('All of it'), rot=-2, size=46),
])
s = T('Carved sirloin')
scene(s, '', '', [
    prop('F01-01', 300, 420, 260, T('Carved sirloin')), lab('carved sirloin', 300, 600, T('Carved sirloin'), size=36),
    prop('F01-03', 960, 420, 230, T('fried chicken')), lab('fried chicken', 960, 600, T('fried chicken'), size=36),
    prop('F01-04', 1620, 420, 230, T('shrimp')), lab('shrimp', 1620, 600, T('shrimp'), size=36),
    prop('F01-05', 620, 800, 210, T('mac and cheese')), lab('mac & cheese', 620, 960, T('mac and cheese'), size=36),
    prop('F02-09', 1300, 800, 170, T('a dessert bar')), lab('dessert bar', 1300, 960, T('a dessert bar'), size=36),
    stk('+ ~150 other things', 960, 220, T('a hundred and fifty'), rot=-2, size=46),
])
s = T('Nobody counts your plates')
scene(s, '', '', [
    L('C02-02', s, x=400), lab('Gary', 400, 400, s),
    prop('F03-08', 1450, 760, 260, T('Nobody counts')), xm(1450, 760, T('Nobody taps'), s=70),
    g('G06-02', 1450, 330, T('trip number five'), h=180), fx('ding', T('trip number five'), 0.5),
])
s = T('That makes the next part strange')
scene(s, 'The biggest buffet chain', '', [
    paper(460, 230, 1000, 200, s, rot=-1, mv=f"{T('Golden Corral', back=5)},0,-40,0.75"),
    lab('For years, the biggest name in buffets…', 960, 350, s, size=48, cls='serif', italic=True, typeOn=True, mv=f"{T('Golden Corral', back=5)},0,-40,0.75"),
    ch('P05-01', 520, T('Golden Corral', back=5), h=330, y=880, **{'in': 'left'}), g('G05-01', 520, 470, T('Golden Corral', back=5), h=110), xm(700, 470, T('Corral It was'), s=40),
    ch('P05-02', 1400, T('It was Old Country'), h=340, y=880, **{'in': 'right'}), g('G05-02', 1400, 470, T('It was Old Country'), h=110),
    cnt(350, 1400, 990, T('more than 350'), suf='+', size=70, cap='', rot=2), loop(1400, 720, 260, 200, T('at its peak')),
])
s = T('Its parent company went bankrupt')
scene(s, 'Old Country Buffet', '', [
    arc('A-ocb', 140, 230, 640, s, rot=-2),
    g('G03-01', 1360, 330, T('went bankrupt in 2008'), h=200),
    stp('BANKRUPT', 1360, 540, T('2008'), rot=-5), stp('AGAIN', 1230, 650, T('again in 2012'), rot=4, size=44), stp('AND AGAIN', 1500, 740, T('then again in 2016'), rot=-3, size=44),
    fx('stamp', T('2008')), fx('stamp', T('again in 2012'), 0.4), fx('stamp', T('then again in 2016'), 0.4),
])
s = T('By 2021')
scene(s, 'By 2021', '', [
    g('G05-12', 960, 260, s, h=180),
    ch('P03-09', 640, T('most of the furniture'), h=380, y=960),
    R('C04-09', T('sold at auction'), x=1400, h=500), fx('clang', T('sold at auction'), 0.35),
])
s = T('So the obvious answer')
scene(s, 'The obvious answer', '', [
    L('C01-02', s),
    paper(690, 300, 960, 200, s, rot=1),
    lab('"most people don\'t eat that much"', 1170, 420, s, size=46, cls='serif', italic=True),
    xm(1560, 340, T("can't be the whole"), s=48),
    stk("can't be the whole story", 1170, 640, T("can't be the whole"), rot=-2),
])
s = T('Both chains had')
scene(s, 'Same customers. Same plates.', '', [
    ch('P05-01', 450, s, h=300, y=760), ch('P05-02', 1470, s, h=310, y=760),
    prop('F01-06', 960, 760, 190, T('mashed potatoes')), stk('same mashed potatoes', 960, 920, T('mashed potatoes'), rot=2),
    prop('E01-08', 450, 380, 170, T('One is still opening')), lab('still opening restaurants', 450, 870, T('One is still opening'), size=34),
    prop('E01-07', 1470, 380, 170, T('The other one is a memory')), lab('a memory', 1470, 880, T('The other one is a memory'), size=34),
])
s = T('To work out why')
scene(s, '', '', [
    L('C01-11', s),
    paper(700, 340, 920, 360, s, rot=-1),
    lab('the number buffets', 1160, 470, s, size=48, cls='serif', italic=True),
    lab("don't put on the sign:", 1160, 535, T("don't put on"), size=48, cls='serif', italic=True),
    hl(800, 600, 720, T('what it actually costs'), h=48),
    lab('WHAT IT COSTS TO FEED YOU', 1160, 640, T('what it actually costs'), size=56, cls='anton'),
])

# ======================= Chapter 2: What does it cost to feed you? =======================
s = T('According to the Wall Street Journal')
scene(s, '', '', [
    chap(2, 'What does it cost to feed you?', s),
    lab('per the Wall Street Journal', 960, 210, s + 2.0, size=30, cls='type'),
    g('G01-02', 520, 480, T('of every dollar'), h=200),
    arrow(860, 480, 1060, 480, T('Golden Corral takes in')),
    cnt(38, 1400, 500, T('goes on food'), suf='¢', cap='of every $1 goes on food', size=150),
    prop('P02-09', 520, 800, 220, T('of every dollar')),
])
s = T('On a seventeen-dollar dinner')
scene(s, 'What does it cost to feed you?', '', [
    g('G01-05', 960, 300, s, h=180),
    cnt(6.5, 960, 640, T('six dollars and fifty'), pre='≈ $', dec=2, cap='of food per $17 dinner', size=150), fx('ding', T('per person'), 0.4),
    stk("that's the budget", 1450, 790, T("That's the budget"), rot=3),
    L('C01-12', T('for a meal where'), x=300, h=520),
    stk('…try everything twice', 960, 900, T('try everything twice'), rot=-2),
])
s = T('Of course nobody eats an average meal')
scene(s, 'Three kinds of diner', '', [
    g('G01-09', 960, 210, T('When The Hustle'), h=140),
    ch('C02-03', 960, T('The average eater'), h=470), g('G01-07', 960, 420, T('$7.40'), h=140),
    ch('C02-04', 330, T('Someone who mostly'), h=470), g('G01-06', 330, 420, T('$4.70'), h=140),
    ch('C02-01', 1590, T('the person who walked past'), h=480), g('G01-08', 1590, 420, T('$16.90'), h=140),
    lab("let's call him Gary", 1590, 300, T("let's call him Gary"), size=36), fx('ding', T('$16.90'), 0.4),
])
s = T('In that model only about one diner')
scene(s, '1 in 20 diners eats like Gary', '', [
    icons(960, 380, s, n=20, cols=10, hi='19', hiAt=T('eats like Gary') - s, sz=90),
    loop(1414, 506, 70, 76, T('eats like Gary') + 0.4),
    stk('the other 19 quietly cover him', 960, 860, T('the other nineteen'), rot=-2, size=44),
])
s = T('But every now and then')
scene(s, '', '', [
    L('C02-01', s, x=420, h=520), lab('Gary', 420, 420, s),
    stk("…on a diet?", 420, 300, T("on a diet"), rot=3),
    R('C03-01', T('who makes Gary look'), x=1500, h=560), reen(T('who makes Gary look')),
])
s = T('In September 2018')
scene(s, 'Landshut, Bavaria', 'September 2018', [
    L('C03-01', s), lab('Jaroslav Bobrowski', 330, 400, T('Jaroslav'), size=36), stk('30, triathlete', 330, 320, T('30-year-old'), rot=-3, size=34),
    card('B02-01', 760, 230, 900, 506, T('walked into a restaurant'), rot=1.5),
    g('G03-02', 1210, 880, T('Running Sushi'), h=150), reen(s),
])
s = T('It was all-you-can-eat for')
scene(s, 'Running Sushi', '', [
    arc('A-running_sushi', 130, 220, 680, s, rot=-2),
    cnt(15.9, 1400, 360, T('€15.90'), pre='€', dec=2, cap='all you can eat', size=130),
    prop('P04-06', 1400, 700, 260, T("doesn't eat for 20")), stk('fasts ~20 hours', 1400, 920, T("doesn't eat for 20"), rot=2),
])
s = T('That evening')
scene(s, '"Full"', '', [
    prop('F03-05', 960, 610, 600, T('turned out to be')),
    cnt(100, 1500, 400, T('one hundred plates'), pre='~', suf=' plates', cap='Jaroslav Bobrowski, 2018', size=120, dur=1.6), fx('ding', T('of sushi'), 0.5),
    L('C01-03', T('one hundred plates', end=True), x=380, h=520),
])
s = T("He wasn't taking one plate")
scene(s, '', '', [
    L('C03-02', s), g('G03-05', 330, 300, T('five or seven'), h=150),
    prop('P01-08', 960, 760, 300, T('leaving such big gaps')), stk('big gaps on the belt', 960, 560, T('big gaps'), rot=-2),
    R('C03-07', T('other customers asked')), stk('skimping on fish?', 1590, 330, T('skimping on fish'), rot=3),
    reen(s),
])
s = T('So when Bobrowski went to pay')
scene(s, '', '', [
    L('C03-04', T('tried to leave a tip')),
    R('C03-05', T('the waiter refused'), out=T('the owner told him')),
    R('C03-06', T('the owner told him'), noPop=True),
    g('G03-06', 960, 330, T('banned for good'), h=180), fx('stamp', T('banned for good')),
    stk('"he ate for five people"', 960, 560, T('he ate for five'), rot=-2), reen(s),
])
s = T("And Bobrowski isn't the only one")
scene(s, 'Thiensville, Wisconsin', '2012', [
    L('C03-08', T('a 6-foot-6')), lab('Bill Wisth', 330, 380, T('named Bill Wisth'), size=36),
    stk("6'6\", 350 lb", 330, 300, T('350-pound'), rot=-3, size=34),
    card('B01-04', 760, 230, 900, 506, T('fish fry at'), rot=-1.5),
    g('G05-03', 1210, 880, T("Chuck's Place"), h=140), reen(s),
])
s = T('After twelve pieces of fish')
scene(s, 'Chuck’s Place', '', [
    L('C03-08', s, noPop=True),
    prop('F01-11', 960, 520, 220, s), cnt(12, 960, 800, T('twelve pieces'), suf=' pieces', cap='then: cut off', size=110),
    R('C03-10', T('cut him off')), stp('CUT OFF', 1590, 330, T('cut him off'), rot=5, size=50), fx('stamp', T('cut him off'), 0.5),
])
s = T('So two days later')
scene(s, 'Two days later', '', [
    card('B05-03', 160, 210, 960, 540, s, rot=-1.5),
    g('G06-03', 1520, 360, T('picket sign'), h=150),
    stp('FALSE ADVERTISING', 1520, 560, T('false advertising'), rot=-4, size=46), fx('stamp', T('false advertising'), 0.5),
    prop('P04-07', 1520, 840, 220, T('every Sunday')), stk('every Sunday', 1520, 990, T('every Sunday'), rot=2, size=34),
])
s = T('Both stories show')
scene(s, 'For a small restaurant…', '', [
    paper(180, 300, 1160, 220, s, rot=1),
    lab('one extreme eater = a real cost', 760, 430, T('one extreme eater'), size=60, cls='serif', italic=True),
    card('B05-01', 560, 600, 800, 450, T('Notice who paid'), rot=-1.5, yellow=False),
    stk('who actually paid?', 1620, 330, T('Notice who paid'), rot=3),
    R('C03-07', T('the other customers'), x=1620, h=460),
])
s = T('To be fair')
scene(s, 'To be fair…', 'the $20 buffet model', [
    g('G01-09', 960, 230, s, h=130),
    g('G02-05', 420, 470, T('staff'), h=120), g('G02-06', 960, 470, T('rent'), h=120), g('G02-07', 1500, 470, T('electricity'), h=120),
    cnt(1, 640, 800, T('one dollar of profit'), pre='≈ $', cap='profit per customer', size=120, color='green'), cnt(5, 1280, 800, T('five percent'), suf='%', cap='profit margin', size=120, color='green'),
    fx('ding', T('five percent'), 0.4),
])
s = T("So buffets can't just")
scene(s, '', '', [
    L('C01-06', s, x=380),
    paper(700, 380, 920, 300, s, rot=-1),
    lab("buffets don't hope", 1160, 500, s, size=56, cls='serif', italic=True),
    hl(820, 560, 680, T('They make sure'), h=48),
    lab('THEY MAKE SURE', 1160, 600, T('They make sure'), size=70, cls='anton'),
])

# ======================= Chapter 3: Why are the rolls always first? =======================
s = T('Walk into almost any buffet')
scene(s, '', '', [
    chap(3, 'Why are the rolls always first?', s),
    card('B01-02', 160, 200, 860, 484, s + 2.0, rot=-1.5, yellow=False),
    g('G02-08', 1450, 300, T("what's at the start"), h=150),
    prop('F01-07', 1180, 600, 170, T('salad')), prop('F01-08', 1530, 600, 170, T('bread rolls')),
    prop('F01-06', 1180, 830, 170, T('potatoes something')), prop('F01-03', 1530, 830, 170, T('something fried')),
])
s = T('The expensive meat is usually')
scene(s, '', '', [
    arrow(200, 900, 900, 900, s, bend=-10),
    lab('further in…', 560, 840, s, size=40),
    prop('F01-01', 1200, 700, 260, s),
    R('C02-06', T('served by a person'), x=1600, h=480),
    stk('a "specific idea" of a portion', 1200, 330, T('fairly specific idea'), rot=-2),
])
s = T("That layout isn't an accident")
scene(s, "That layout isn't an accident", '', [
    lab('one well-known study of buffet lines', 960, 220, T('In one well-known study'), size=32, cls='type'),
    prop('P01-01', 960, 620, 340, s),
    g('G02-11', 430, 430, T('three-quarters'), h=170),
    g('G02-12', 1490, 430, T('two-thirds'), h=170),
    arrow(430, 540, 780, 620, T('first tray'), bend=-20),
])
s = T('By the time you reach the steak')
scene(s, 'Potato vs. steak', '', [
    prop('F03-07', 960, 560, 360, s), stk('plate: already full', 960, 790, T('already taken'), rot=-2),
    prop('F02-02', 360, 560, 220, T('by a potato')), cnt(30, 360, 820, T('thirty cents'), pre='≈ ', suf='¢', cap='potatoes / serving', size=110, color='green'),
    prop('F01-02', 1560, 560, 190, T('The steak by comparison')), cnt(2.25, 1560, 820, T('$2.25'), pre='≈ $', dec=2, cap='steak / serving', size=110, color='red'),
    fx('ding', T('$2.25'), 0.35),
])
s = T('Golden Corral goes a step further')
scene(s, 'Modules', '', [
    g('G03-09', 960, 330, T('modules'), h=300),
    prop('F02-10', 520, 760, 240, T('The meat and seafood')), lab('seafood + hush puppies + fries', 520, 920, T('hush puppies'), size=32),
    prop('F02-11', 1400, 760, 240, T('The meatloaf comes')), lab('meatloaf + potatoes + gravy + beans', 1400, 920, T('potatoes gravy'), size=32),
])
s = T("You didn't choose that side dish")
scene(s, '', '', [
    paper(160, 330, 1060, 300, s, rot=-1),
    lab("You didn't choose that side.", 690, 460, s, size=54, cls='serif', italic=True),
    lab('It was chosen for you.', 690, 540, T('It was chosen for you'), size=54, cls='serif', italic=True),
    R('C01-05', T('in a meeting with a spreadsheet'), x=1580),
    stk('…in a spreadsheet meeting', 1580, 330, T('a spreadsheet'), rot=3),
])
s = T('Then there are the small details')
scene(s, 'The small details', '', [
    prop('P01-04', 300, 500, 300, T('bigger serving spoons')), stk('BIG potato spoon', 300, 750, T('bigger serving spoons'), rot=-3, size=34),
    prop('P01-05', 760, 520, 200, T('smaller tongs')), stk('small meat tongs', 760, 750, T('smaller tongs'), rot=2, size=34),
    prop('F03-09', 1180, 540, 120, T('The plates are smaller')), stk('small plates', 1180, 750, T('The plates are smaller'), rot=-2, size=34),
    prop('P02-03', 1600, 500, 330, T('water glasses')), stk('BIG water glass', 1600, 750, T('water glasses'), rot=3, size=34),
    prop('P02-05', 1600, 900, 0.01, T('refilled')),
    lab('steak just takes a little more effort', 960, 960, T('It just makes steak'), size=40, cls='serif', italic=True),
])
s = T('And when steak is the one thing')
scene(s, 'Rationed by design', '', [
    prop('F01-01', 960, 560, 330, s), stk('the one rationed thing', 960, 320, T('rationed by design'), rot=-2),
    stk('people notice when it runs low', 960, 820, T('runs low'), rot=2),
])
s = T('On January 29th')
scene(s, 'Bensalem, Pennsylvania', 'January 29, 2022', [
    g('G03-10', 960, 250, s, h=160),
    L('C03-11', T('an argument broke out'), x=380), stk('an argument in the steak line', 380, 330, T('an argument broke out'), rot=-3, size=34),
    prop('F01-01', 1000, 720, 240, T('the line for steak')),
    stk('cut in line?', 1550, 520, T('someone cut in line'), rot=3, size=36),
    stk('running out?', 1550, 640, T('the steak was running out'), rot=-2, size=36),
    stk('both?', 1550, 760, T('or both'), rot=2, size=36), reen(s),
])
s = T('Either way')
scene(s, 'Within minutes', '', [
    card('B05-02', 160, 210, 960, 540, T('Within minutes'), rot=1.5),
    cnt(40, 1500, 360, T('around forty people'), pre='~', cap='people fighting', size=140, color='red'), fx('crash', T('fighting'), 0.55),
    stk('"even worse"', 1500, 560, T('it got even worse'), rot=-3),
    reen(s),
])
s = T('The video which went viral')
scene(s, 'Chairs. Tables. High chairs.', '', [
    prop('P03-03', 380, 520, 230, T('chairs flying'), rot=-12), fx('crash', T('chairs flying'), 0.45),
    prop('P03-04', 960, 520, 300, T('tables flipping'), rot=8),
    prop('P03-05', 1540, 520, 240, T('high chairs'), rot=-6), stk('HIGH chairs', 1540, 760, T('high chairs'), rot=3),
    prop('E01-09', 960, 830, 200, T('An employee was hit')), stk('an employee was hit by a table', 960, 980, T('An employee was hit'), rot=-2, size=36),
])
s = T('And as things finally calmed down')
scene(s, '', '', [
    L('C03-11', s, x=420),
    bub('"All I wanted was some steak."', 700, 260, 760, 500, 520, T('All I wanted'), size=42, h=130),
    prop('E01-08', 1500, 700, 220, T('no serious injuries')), lab('no serious injuries reported', 1500, 880, T('no serious injuries'), size=34),
    reen(s),
])
s = T("But it's probably the clearest proof")
scene(s, 'The most valuable thing in a buffet', '', [
    prop('P01-03', 960, 640, 380, s),
    stk("isn't on the menu", 560, 330, T("isn't on the menu"), rot=-3),
    stk("it's the queue for the carving station", 900, 900, T('queue for the carving'), rot=2),
    R('C01-07', T('carving station', end=True), x=1640, h=500),
])
s = T("That's also why when beef prices")
scene(s, 'The pork chop', '', [
    stk('beef prices ↑', 400, 300, T('beef prices went up'), rot=-3),
    prop('F01-09', 960, 560, 330, T('bone-in fried pork chop')),
    cnt(40, 960, 860, T('40 percent'), pre='≈ ', suf='%', cap='of what the sirloin costs', size=120),
    prop('E01-06', 1290, 430, 150, T('feels like they got a treat')), stk('still feels like a treat', 1500, 330, T('got a treat'), rot=3),
])
s = T('You can see the result')
scene(s, 'The shopping list', '', [
    lab('per The Atlantic', 960, 210, T('According to The Atlantic'), size=30, cls='type'),
    bars('Chicken|47|47M lb|y;Steak|6|6M lb|r', 400, 380, T('47 million'), title='Pounds served per year', w=1150, rh=90, lw=260, stag=T('6 million') - T('47 million')),
    cnt(8, 960, 860, T('nearly eight pounds'), pre='~', suf=' : 1', cap='chicken to steak', size=120), fx('ding', T('every pound of steak'), 0.4),
])
s = T('So the food is cheap')
scene(s, 'So far…', '', [
    prop('F01-06', 420, 600, 220, s), prop('F01-02', 420, 600, 0.01, s),
    lab('cheap food, steak surrounded by potatoes', 420, 820, T('surrounded by potatoes'), size=32),
    g('G06-04', 1300, 540, T('getting through the door'), h=210), fx('ching', T('getting through the door'), 0.45),
    stk("the only thing you've paid for", 1300, 330, T('the only thing'), rot=-2),
])

# ======================= Chapter 4: Would you like a drink with that? =======================
s = T('At most Golden Corrals')
scene(s, '', '', [
    chap(4, 'Would you like a drink with that?', s),
    card('B02-03', 160, 220, 820, 460, s + 2.0, rot=-1.5, yellow=False),
    prop('P02-01', 1250, 560, 300, T('A soda')), prop('P02-02', 1600, 560, 260, T('iced tea')),
    g('G04-05', 1420, 860, T('two and a half'), h=170),
    stk("the drink isn't included", 570, 820, T("the drink isn't included"), rot=2),
])
s = T('And fountain soda is one of the best')
scene(s, 'Best deal in the building', '…for the restaurant', [
    prop('P02-04', 960, 600, 380, s),
    cnt(12, 400, 470, T('twelve cents'), pre='≈ ', suf='¢', cap='cost to fill', size=120, color='green'),
    arrow(640, 420, 1300, 420, T('Sell that for'), bend=-40),
    cnt(2, 1520, 470, T('two dollars'), pre='$', suf='+', cap='price', size=120),
    cnt(1000, 960, 910, T('one thousand percent'), suf='%+', cap='markup', size=110, color='red', dur=1.4), fx('ching', T('one thousand percent') + 1.2, 0.5),
])
s = T('On a seventeen-dollar dinner that contains')
scene(s, '', '', [
    g('G01-04', 640, 500, s, h=200),
    lab('+', 960, 520, T('the drink is almost'), size=110, cls='anton'),
    prop('P02-01', 1260, 520, 300, T('the drink is almost')),
    stk('almost pure profit', 1260, 780, T('pure profit'), rot=3),
    stk("…bought before you've seen a tray", 960, 920, T("before you've seen"), rot=-2),
])
s = T("Then there's the kids' deal")
scene(s, "The kids' deal", '', [
    prop('P04-07', 400, 520, 280, T('Fridays Saturdays')), stk('Fri · Sat · Sun', 400, 740, T('Fridays Saturdays'), rot=-2, size=36),
    cnt(2.5, 1000, 440, T('$2.50 with each'), pre='$', dec=2, cap='per kid, with each adult', size=130), fx('ding', T('adult buffet'), 0.4),
    stk('a terrible deal?', 1000, 650, T('a terrible deal'), rot=2),
    R('C02-10', T('a seven-year-old')), stk('not a threat to the sirloin', 1590, 330, T('not a serious threat'), rot=3, size=34),
])
s = T('And a $2.50 child never arrives alone')
scene(s, '', '', [
    ch('C02-09', 700, s, h=560),
    stk('never arrives alone', 700, 330, T('never arrives alone'), rot=-3),
    g('G01-01', 1450, 450, T('at least one adult'), h=160), lab('paying full price', 1450, 600, T('full price'), size=36),
    prop('P02-01', 1360, 800, 200, T('a couple of drinks')), prop('P02-02', 1560, 800, 180, T('a couple of drinks')),
])
s = T('So by now the seventeen-dollar buffet')
scene(s, 'The running tally', '', [
    L('C02-12', s, x=360),
    g('G07-01', 1060, 560, T('seventeen dollars a drink'), h=470, out=T('a drink', back=3)),
    g('G07-02', 1060, 560, T('a drink', back=3), h=470, noPop=True, out=T('second adult')),
    g('G07-04', 1060, 560, T('second adult'), h=470, noPop=True, out=T('a child who ate')),
    g('G07-05', 1060, 560, T('a child who ate'), h=470, noPop=True),
    prop('F02-07', 1600, 380, 170, T('four chicken nuggets')), prop('F02-08', 1600, 680, 190, T('a pudding cup')),
    fx('ching', T('a pudding cup'), 0.5),
])
s = T('Which brings us back')
scene(s, '', '', [
    paper(360, 360, 1200, 300, s, rot=-1),
    lab('If it works this well…', 960, 480, T('If the model works'), size=58, cls='serif', italic=True),
    hl(520, 540, 880, T('why did so many'), h=48),
    lab('WHY DID THE OTHERS GO BROKE?', 960, 580, T('why did so many'), size=64, cls='anton'),
])

# ======================= Chapter 5: Why did the other buffets go bankrupt? =======================
s = T("Here's the part that surprises")
scene(s, '', '', [
    chap(5, 'Why did the other buffets go bankrupt?', s),
    L('C02-01', T("it wasn't Gary"), x=480), xm(480, 640, T("it wasn't Gary", end=True), s=80),
    R('C03-02', T("it wasn't triathletes"), x=1440), xm(1440, 640, T('triathletes either'), s=80),
])
s = T("Old Country Buffet's parent company")
scene(s, 'Debt', '', [
    g('G04-07', 960, 260, T('in 2006'), h=170),
    ch('P05-02', 520, s, h=320, y=800), ch('P05-03', 1400, T("bought Ryan's"), h=270, y=800), g('G05-04', 1400, 880, T("bought Ryan's"), h=110),
    arrow(720, 640, 1200, 640, T("bought Ryan's"), bend=-25),
    stk('…borrowed heavily', 960, 960, T('borrowed heavily'), rot=-2),
])
s = T('That debt led to')
scene(s, '', '', [
    g('G03-01', 960, 300, s, h=200),
    stp('2008', 560, 640, T('first bankruptcy in 2008'), rot=-6, size=60), stp('2012', 960, 640, T('again in 2012'), rot=4, size=60), stp('2016', 1360, 640, T('and again in 2016', back=5), rot=-3, size=60),
    fx('stamp', T('first bankruptcy in 2008')), fx('stamp', T('again in 2012'), 0.45), fx('stamp', T('in 2016', back=5), 0.45),
])
s = T('In early 2016')
scene(s, '2016', '', [
    arc('A-vacant_ryans', 130, 250, 620, s, rot=-2),
    cnt(74, 1350, 360, T('74 restaurants'), suf=' closed', cap='early 2016', size=110, color='red'), fx('stamp', T('in one go'), 0.45),
    cnt(92, 1350, 600, T('92 more'), pre='+', suf=' more', cap='a month later', size=110, color='red'), fx('stamp', T('about a month later'), 0.45),
    stk('often without warning staff', 1350, 790, T('without warning'), rot=2),
])
s = T('That same year')
scene(s, '', '', [
    g('G05-06', 600, 280, T('Souplantation'), h=120), g('G05-07', 600, 440, T('Sweet Tomatoes'), h=120),
    arc('A-souplantation', 230, 560, 520, T('another big buffet chain'), rot=-1),
    cnt(175, 1450, 330, T('$175 million'), pre='$', suf='M', cap='debt', size=130, color='red'),
    R('C01-08', T('in debt'), x=1450, h=480),
])
s = T('Debt is especially dangerous')
scene(s, 'Cook first, hope later', '', [
    L('C04-05', T('A normal restaurant cooks'), x=380), stk('cooks AFTER you order', 380, 330, T('after you order'), rot=-3),
    R('C04-06', T('A buffet cooks first'), x=1540), stk('cooks FIRST, hopes later', 1540, 330, T('hopes people turn up'), rot=3),
])
s = T('If the dining room is half empty')
scene(s, '7 p.m., half empty', '', [
    card('B02-04', 160, 230, 900, 506, s, rot=-1.5),
    prop('P04-06', 1450, 380, 220, T("at seven o'clock")),
    prop('F01-12', 1450, 720, 230, T('the turkey still')), stk('…and still carved', 1450, 900, T('still has to be carved'), rot=2),
])
s = T('Somewhere between 5 and 25')
scene(s, 'Waste', '', [
    g('G04-11', 640, 380, s, h=190),
    ch('P03-08', 640, T('end up in the bin'), h=340, y=950),
    stk('big eaters? not the problem', 1380, 340, T("doesn't really lose money on big"), rot=-2),
    ch('P03-02', 1380, T('empty chairs'), h=330, y=900), stp('EMPTY CHAIRS', 1380, 560, T('empty chairs'), rot=4, size=50), fx('stamp', T('empty chairs'), 0.45),
])
s = T('Then in 2020')
scene(s, '2020', '', [
    g('G04-12', 960, 260, s, h=170),
    L('C04-11', T('a pandemic'), x=400),
    prop('P03-12', 1400, 640, 260, T('sharing serving tongs')), stk('shared tongs: no thanks', 1400, 840, T('least appealing'), rot=2),
])
s = T('By early 2021')
scene(s, 'By early 2021', '', [
    g('G05-02', 520, 330, T('every Old Country'), h=120), g('G05-05', 520, 500, T('HomeTown Buffet'), h=120), g('G05-04', 520, 670, T("and Ryan's"), h=120),
    g('G05-11', 1360, 500, T('had closed'), h=200), fx('stamp', T('had closed')),
    stk('…all of them', 1360, 700, T('had closed', end=True), rot=2),
])
s = T('The odd thing is')
scene(s, '', '', [
    paper(360, 340, 1200, 330, s, rot=1),
    lab('the most famous buffets in the world', 960, 460, T('the most famous'), size=50, cls='serif', italic=True),
    hl(530, 520, 860, T('never even tried'), h=48),
    lab('never even tried to make money', 960, 560, T('never even tried'), size=60, cls='anton'),
])

# ======================= Chapter 6: Why did Las Vegas give up on buffets? =======================
s = T('For decades the Las Vegas buffet')
scene(s, '', '', [
    chap(6, 'Why did Las Vegas give up on buffets?', s),
    card('B03-02', 160, 220, 900, 506, s + 2.0, rot=-1.5),
    arc('A-vegas_buffet', 1180, 240, 560, T('designed to lose money'), rot=2),
    g('G08-01', 1460, 820, T('loss leaders'), h=170), fx('ding', T('loss leaders'), 0.4),
])
s = T('Back in the 1980s')
scene(s, 'The 1980s', '', [
    arc('A-stardust', 120, 240, 600, s, rot=-2),
    cnt(75, 1380, 340, T('three-quarters'), pre='≈ ', suf='%', cap='of casino revenue: gambling', size=120),
    R('C04-01', T('a cheap all-you-can-eat'), x=1380, h=430),
    stk('fill up → back to the tables', 960, 980, T('send you back to the tables'), rot=-2),
])
s = T('That works as long as')
scene(s, 'But…', '', [
    L('C04-03', T('more and more'), x=400), xm(560, 560, T("don't gamble much"), s=60),
    R('C04-02', T('a giant room losing'), x=1520), prop('F02-12', 1100, 760, 0.01, s),
    stk('losing money on crab legs', 1520, 330, T('losing money on crab legs'), rot=3),
])
s = T('Around the year 2000')
scene(s, 'Las Vegas Strip buffets', '', [
    bars('Around 2000|35|~35|y;Today|7|~7|r', 420, 420, s, title='Buffets on the Las Vegas Strip', w=1150, rh=100, lw=280, stag=T('about seven') - s),
    fx('ding', T('about seven'), 0.4),
])
s = T('A lot of that space became')
scene(s, 'Food halls', '', [
    card('B03-04', 160, 220, 880, 495, s, rot=-1.5),
    g('G08-04', 1440, 330, T('food halls'), h=170),
    R('C04-04', T('charge you separately'), x=1440, h=440),
    stk('the exact opposite of a buffet', 600, 880, T('exact opposite'), rot=2),
])
s = T('Vegas buffets were built')
scene(s, '', '', [
    L('C01-09', s, x=380),
    prop('P04-02', 1000, 560, 280, T("Golden Corral doesn't")), xm(1000, 560, T('quietly paying'), s=70),
    prop('F01-04', 1500, 560, 220, T('for the shrimp')),
    stk('the food has to pay for itself', 1250, 860, T('pay for itself'), rot=-2),
])

# ======================= Chapter 7: So how does $17 make money? =======================
s = T('So how does it manage that')
scene(s, '', '', [
    chap(7, 'So how does $17 make money?', s),
    paper(560, 380, 800, 260, T('The answer is mostly'), rot=-1),
    lab('mostly:', 960, 470, T('The answer is mostly'), size=48, cls='serif', italic=True),
    lab('SCALE', 960, 590, T('scale'), size=120, cls='anton'), fx('stamp', T('scale'), 0.4),
])
s = T('A typical Golden Corral serves')
scene(s, 'Scale', '', [
    arc('A-gc_storefront', 110, 230, 640, s, rot=-2),
    cnt(6500, 1360, 320, T('six to six'), pre='~', cap='customers / week / restaurant', size=110, frm=0),
    cnt(7.5, 1360, 560, T('$7.5'), pre='$', suf='M', dec=1, cap='a year, best newer locations', size=110),
    cnt(12, 1360, 800, T('$12 million'), pre='$', suf='M', cap='Puerto Rico location', size=110), fx('ching', T('$12 million') + 1.0, 0.45),
])
s = T('This is exactly what Running Sushi')
scene(s, 'A rounding error', '', [
    ch('P05-06', 420, s, h=300, y=640), ch('P05-05', 420, T("Chuck's Place in Wisconsin"), h=260, y=960),
    lab('a few hundred a night', 420, 260, T('a few hundred'), size=34),
    R('C03-02', T('one Bobrowski empties'), x=1080, h=440), stk('empties the belt', 1080, 400, T('empties the conveyor'), rot=-2),
    g('G08-05', 1600, 360, T('six thousand a week'), h=130), stk('= rounding error', 1600, 560, T('rounding error'), rot=3, size=44),
])
s = T('That volume changes the kitchen')
scene(s, 'The kitchen', '', [
    bars('Cook to order|25|~25|b;Buffet batch|200|~200|y', 420, 330, T('A cook at a normal'), title='Customers served per hour', w=1100, rh=80, lw=280, stag=T('A buffet cook') - T('A cook at a normal')),
    L('C04-05', T('A cook at a normal'), x=260, h=380), R('C04-06', T('A buffet cook'), x=1660, h=380),
    stk("you pay a tiny share of a VERY big batch", 960, 860, T('a tiny share'), rot=-2),
])
s = T('Golden Corral also forecasts')
scene(s, 'Forecasting', '', [
    L('C04-08', s, x=380), g('G08-09', 1000, 320, T('fifteen-minute'), h=170),
    prop('P01-07', 1100, 700, 300, T('under heat lamps')), prop('F03-12', 1460, 760, 180, T('under heat lamps')), xm(1460, 760, T('the waste problem'), s=60),
    stk('no running out on a Saturday in Pennsylvania', 1180, 990, T('Saturday night in Pennsylvania'), rot=-1, size=34),
])
s = T('And it counts on loyalty')
scene(s, 'Loyalty', '', [
    L('C02-11', s, x=420),
    cnt(70, 1250, 350, T('70 times a year'), pre='~', suf=' visits', cap='a year, most loyal guests', size=120),
    prop('P02-11', 1250, 580, 200, T('more than once a week')),
    prop('P01-12', 1250, 840, 230, T('chocolate pudding')), stk('a second kitchen', 1560, 760, T('second kitchen'), rot=3, size=38),
])
s = T('To be fair none of this')
scene(s, 'Not a money printer', '', [
    cnt(348, 600, 360, T('348 restaurants'), cap='Golden Corrals, end of 2025', size=120), g('G08-12', 600, 580, T('three fewer'), h=170),
    paper(1040, 280, 720, 420, T('its CEO recently said'), rot=1.5),
    lab('Golden Corral CEO, 2026:', 1400, 380, T('its CEO recently said'), size=30, cls='type'),
    lab('"We are trying to', 1400, 480, T('We are trying'), size=50, cls='serif', italic=True),
    lab('at least tread water."', 1400, 560, T('tread water'), size=50, cls='serif', italic=True),
    lab('beef is expensive · margins were thin', 600, 820, T('Beef is expensive'), size=34),
])
s = T("So seventeen dollars isn't really")
scene(s, "It's a bet", '', [
    g('G01-01', 960, 300, s, h=170), stp("IT'S A BET", 960, 470, T("It's a bet"), rot=-5, size=64), fx('stamp', T("It's a bet")),
    prop('F02-01', 260, 780, 170, T('start with the rolls')),
    prop('F02-11', 640, 780, 160, T('the meatloaf will bring')),
    prop('P02-01', 1000, 780, 220, T("you'll order a drink")),
    prop('C02-10', 1340, 780, 260, T('bring a kid')),
    prop('P04-07', 1680, 780, 200, T('come back next Thursday')),
    stk('…and most of us do all of it', 960, 990, T('most of us do'), rot=-1, size=36),
])
s = T('Yes Gary is still allowed')
scene(s, '', '', [
    L('C02-01', s), stk('4 plates of sirloin: allowed', 330, 330, T('four plates of sirloin'), rot=-3, size=34),
    R('C03-01', T('Bobrowski is still welcome')), stk('…just not in Landshut', 1590, 330, T('just not in Landshut'), rot=3, size=34),
    prop('F01-06', 960, 640, 230, T('the other nineteen of us')), stk('really, really like potatoes', 960, 860, T('really really like potatoes'), rot=-2),
])
s = T('This channel is brand new')
scene(s, '', '', [
    L('C01-10', s, x=420),
    g('G05-10', 1250, 360, T('a subscribe'), h=190), fx('ding', T('a subscribe'), 0.4),
    card('B05-04', 900, 560, 700, 394, T('Next time'), rot=1.5),
    lab('Next: why movie theaters barely make money on movies', 1250, 1010, T('why movie theaters'), size=30, cls='type'),
])

exec(open('fill_gaps.py').read())
# drop zero-size placeholders, make scenes contiguous, clamp starts
for sc in S:
    sc['items'] = [it for it in sc['items'] if not (it.get('k') == 'img' and it.get('h', 1) < 1)]
S.sort(key=lambda s: s['s'])
for i in range(len(S) - 1): S[i]['e'] = S[i + 1]['s']
S[-1]['e'] = DUR
for sc in S:
    for it in sc['items']:
        it['at'] = round(max(it['at'], sc['s']), 2)
        if 'out' in it and it['out'] is not None and it['out'] <= it['at']: it['out'] = round(it['at'] + 0.5, 2)
for k, sc in enumerate(S):
    vis = [it for it in sc['items'] if it['k'] != 'sfx' and it.get('a') != 'G06-01']
    if vis:   # no empty openers: the earliest element(s) land on the scene's first frame
        first = min(it['at'] for it in vis)
        if first - sc['s'] > 0.4:
            for it in vis:
                if abs(it['at'] - first) < 0.05: it['at'] = sc['s']
    chap_here = any(it['k'] == 'chapter' for it in sc['items'])
    sc['tr'] = 'wipe' if chap_here else ('up' if k % 4 == 3 else 'slide')
    if chap_here:   # everything else waits for the chapter card to clear
        for it in sc['items']:
            if it['k'] not in ('chapter', 'sfx'): it['at'] = max(it['at'], sc['s'] + 2.0)
board = dict(version=2, title="Why Buffets Don't Lose Money", duration=DUR, scenes=S, chapters=CHAPTERS)
json.dump(board, open('editor/storyboard.json', 'w'))
lens = [round(s['e'] - s['s'], 1) for s in S]
print(len(S), 'scenes', sum(len(s['items']) for s in S), 'items', sum(1 for s in S for i in s['items'] if i['k'] == 'sfx'), 'sfx; shortest', min(lens), 'longest', max(lens))
