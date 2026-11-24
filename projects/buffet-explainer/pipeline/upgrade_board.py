p='build_board.py';h=open(p).read()
def rep(a,b):
    global h
    assert h.count(a)==1,(h.count(a),a[:80]);h=h.replace(a,b)
rep("TOK = json.load(open('script_words.json'))","TOK = json.load(open('script_words_fa.json'))   # forced-aligned word times\nLEAD = 0.15   # visuals land just before the word")
rep("            return round(TOK[i + len(p) - 1]['e'] if end else TOK[i]['s'], 2)","            return round(max(0, (TOK[i + len(p) - 1]['e'] if end else TOK[i]['s']) - LEAD), 2)")
rep("def ch(a, x, at, h=560, y=1010, out=None, **k):","def ch(a, x, at, h=600, y=1030, out=None, **k):")
rep("def fx(name, at, vol=0.6): return dict(k='sfx', a=name, at=at, vol=vol)","""def fx(name, at, vol=0.6): return dict(k='sfx', a=name, at=at, vol=vol)
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
    return dict(k='chapter', n=n, t=title, x=960, y=520, at=at, out=round(at + 2.2, 2))""")
# ---------- chapter 1
rep("""scene(s, 'Golden Corral', 'dinner, tonight', [
    card('B02-02', 160, 210, 1000, 560, s, rot=-1.5),
    g('G01-01', 1520, 420, T('seventeen dollars gets'), h=190), fx('ding', T('seventeen dollars gets'), 0.4),""","""scene(s, 'Golden Corral', 'dinner, tonight', [
    chap(1, 'A $17 steak dinner with no limit', s),
    card('B02-02', 160, 210, 1000, 560, s + 2.0, rot=-1.5, mv=f"{T('seventeen dollars gets')},-60,0,0.9"),
    cnt(17, 1500, 470, T('seventeen dollars gets'), pre='$', cap='all-you-can-eat dinner', size=150), fx('ding', T('dinner'), 0.4),""")
rep("""scene(s, 'The biggest buffet chain', 'was not Golden Corral', [
    ch('P05-01', 520""","""scene(s, 'The biggest buffet chain', '', [
    paper(460, 230, 1000, 200, s, rot=-1, mv=f"{T('Golden Corral', back=5)},0,-40,0.75"),
    lab('For years, the biggest name in buffets…', 960, 350, s, size=48, cls='serif', italic=True, typeOn=True, mv=f"{T('Golden Corral', back=5)},0,-40,0.75"),
    ch('P05-01', 520""")
rep("ch('P05-01', 520, T('Golden Corral', back=5), h=330, y=860), g('G05-01', 520, 380, T('Golden Corral', back=5), h=130),",
    "ch('P05-01', 520, T('Golden Corral', back=5), h=330, y=880, **{'in': 'left'}), g('G05-01', 520, 470, T('Golden Corral', back=5), h=110), xm(700, 470, T('Corral It was'), s=40),")
rep("ch('P05-02', 1400, T('It was Old Country'), h=340, y=860), g('G05-02', 1400, 380, T('It was Old Country'), h=130),",
    "ch('P05-02', 1400, T('It was Old Country'), h=340, y=880, **{'in': 'right'}), g('G05-02', 1400, 470, T('It was Old Country'), h=110),")
rep("stk('350+ restaurants at its peak', 1400, 950, T('more than 350'), rot=2), loop(1400, 690, 260, 210, T('at its peak')),",
    "cnt(350, 1400, 990, T('more than 350'), suf='+', size=70, cap='', rot=2), loop(1400, 720, 260, 200, T('at its peak')),")
# ---------- chapter 2
rep("""scene(s, 'What does it cost to feed you?', '', [
    lab('per the Wall Street Journal', 960, 210, s, size=30, cls='type'),
    g('G01-02', 520, 480, T('of every dollar'), h=200),
    arrow(860, 480, 1060, 480, T('Golden Corral takes in')),
    g('G01-03', 1400, 480, T('goes on food'), h=200),""","""scene(s, '', '', [
    chap(2, 'What does it cost to feed you?', s),
    lab('per the Wall Street Journal', 960, 210, s + 2.0, size=30, cls='type'),
    g('G01-02', 520, 480, T('of every dollar'), h=200),
    arrow(860, 480, 1060, 480, T('Golden Corral takes in')),
    cnt(38, 1400, 500, T('goes on food'), suf='¢', cap='of every $1 goes on food', size=150),""")
rep("g('G01-04', 960, 600, T('six dollars and fifty'), h=230), fx('ding', T('six dollars and fifty'), 0.4),",
    "cnt(6.5, 960, 640, T('six dollars and fifty'), pre='≈ $', dec=2, cap='of food per $17 dinner', size=150), fx('ding', T('per person'), 0.4),")
rep("""scene(s, '1 in 20 diners eats like Gary', '', [
    g('G02-01', 960, 470, s, h=470),
    loop(1430, 535, 60, 66, T('eats like Gary')),""","""scene(s, '1 in 20 diners eats like Gary', '', [
    icons(960, 380, s, n=20, cols=10, hi='19', hiAt=T('eats like Gary') - s, sz=90),
    loop(1414, 506, 70, 76, T('eats like Gary') + 0.4),""")
rep("g('G03-03', 1400, 330, T('€15.90'), h=190),","cnt(15.9, 1400, 360, T('€15.90'), pre='€', dec=2, cap='all you can eat', size=130),")
rep("g('G03-04', 1500, 380, T('one hundred plates'), h=190), fx('ding', T('one hundred plates'), 0.5),",
    "cnt(100, 1500, 400, T('one hundred plates'), pre='~', suf=' plates', cap='Jaroslav Bobrowski, 2018', size=120, dur=1.6), fx('ding', T('of sushi'), 0.5),")
rep("prop('F01-11', 960, 520, 220, s), g('G03-08', 960, 760, T('twelve pieces'), h=160),",
    "prop('F01-11', 960, 520, 220, s), cnt(12, 960, 800, T('twelve pieces'), suf=' pieces', cap='then: cut off', size=110),")
rep("g('G01-10', 640, 790, T('one dollar of profit'), h=180), g('G01-11', 1280, 790, T('five percent'), h=180),",
    "cnt(1, 640, 800, T('one dollar of profit'), pre='≈ $', cap='profit per customer', size=120, color='green'), cnt(5, 1280, 800, T('five percent'), suf='%', cap='profit margin', size=120, color='green'),")
# ---------- chapter 3
rep("""scene(s, 'Why are the rolls always first?', '', [
    card('B01-02', 160, 200, 860, 484, s, rot=-1.5, yellow=False),""","""scene(s, '', '', [
    chap(3, 'Why are the rolls always first?', s),
    card('B01-02', 160, 200, 860, 484, s + 2.0, rot=-1.5, yellow=False),""")
rep("prop('F02-02', 360, 560, 220, T('by a potato')), g('G02-09', 360, 800, T('thirty cents'), h=150),",
    "prop('F02-02', 360, 560, 220, T('by a potato')), cnt(30, 360, 820, T('thirty cents'), pre='≈ ', suf='¢', cap='potatoes / serving', size=110, color='green'),")
rep("prop('F01-02', 1560, 560, 190, T('The steak by comparison')), g('G02-10', 1560, 800, T('$2.25'), h=150),",
    "prop('F01-02', 1560, 560, 190, T('The steak by comparison')), cnt(2.25, 1560, 820, T('$2.25'), pre='≈ $', dec=2, cap='steak / serving', size=110, color='red'),")
rep("g('G03-11', 1500, 330, T('around forty people'), h=180), fx('crash', T('fighting'), 0.55),",
    "cnt(40, 1500, 360, T('around forty people'), pre='~', cap='people fighting', size=140, color='red'), fx('crash', T('fighting'), 0.55),")
rep("g('G03-12', 960, 850, T('40 percent'), h=170),","cnt(40, 960, 860, T('40 percent'), pre='≈ ', suf='%', cap='of what the sirloin costs', size=120),")
rep("g('G04-01', 960, 480, T('47 million'), h=380),",
    "bars('Chicken|47|47M lb|y;Steak|6|6M lb|r', 400, 380, T('47 million'), title='Pounds served per year', w=1150, rh=90, lw=260, stag=T('6 million') - T('47 million')),")
rep("g('G04-02', 960, 840, T('nearly eight pounds'), h=170), fx('ding', T('nearly eight pounds'), 0.4),",
    "cnt(8, 960, 860, T('nearly eight pounds'), pre='~', suf=' : 1', cap='chicken to steak', size=120), fx('ding', T('every pound of steak'), 0.4),")
# ---------- chapter 4
rep("""scene(s, 'Would you like a drink with that?', '', [
    card('B02-03', 160, 220, 820, 460, s, rot=-1.5, yellow=False),""","""scene(s, '', '', [
    chap(4, 'Would you like a drink with that?', s),
    card('B02-03', 160, 220, 820, 460, s + 2.0, rot=-1.5, yellow=False),""")
rep("g('G04-03', 400, 470, T('twelve cents'), h=170),","cnt(12, 400, 470, T('twelve cents'), pre='≈ ', suf='¢', cap='cost to fill', size=120, color='green'),")
rep("g('G04-04', 1520, 470, T('two dollars'), h=170),","cnt(2, 1520, 470, T('two dollars'), pre='$', suf='+', cap='price', size=120),")
rep("stp('1,000%+ MARKUP', 960, 900, T('one thousand percent'), rot=-4, size=58), fx('ching', T('one thousand percent'), 0.5),",
    "cnt(1000, 960, 910, T('one thousand percent'), suf='%+', cap='markup', size=110, color='red', dur=1.4), fx('ching', T('one thousand percent') + 1.2, 0.5),")
rep("g('G04-06', 1000, 420, T('$2.50 with each'), h=190), fx('ding', T('$2.50 with each'), 0.4),",
    "cnt(2.5, 1000, 440, T('$2.50 with each'), pre='$', dec=2, cap='per kid, with each adult', size=130), fx('ding', T('adult buffet'), 0.4),")
# ---------- chapter 5
rep("""scene(s, 'Why did the other buffets go bankrupt?', '', [""","""scene(s, '', '', [
    chap(5, 'Why did the other buffets go bankrupt?', s),""")
rep("g('G04-08', 1350, 330, T('74 restaurants'), h=170), fx('stamp', T('74 restaurants'), 0.45),",
    "cnt(74, 1350, 360, T('74 restaurants'), suf=' closed', cap='early 2016', size=110, color='red'), fx('stamp', T('in one go'), 0.45),")
rep("g('G04-09', 1350, 560, T('92 more'), h=170), fx('stamp', T('92 more'), 0.45),",
    "cnt(92, 1350, 600, T('92 more'), pre='+', suf=' more', cap='a month later', size=110, color='red'), fx('stamp', T('about a month later'), 0.45),")
rep("g('G04-10', 1450, 330, T('$175 million'), h=180),","cnt(175, 1450, 330, T('$175 million'), pre='$', suf='M', cap='debt', size=130, color='red'),")
# ---------- chapter 6
rep("""scene(s, 'Why did Las Vegas give up on buffets?', '', [
    card('B03-02', 160, 220, 900, 506, s, rot=-1.5),""","""scene(s, '', '', [
    chap(6, 'Why did Las Vegas give up on buffets?', s),
    card('B03-02', 160, 220, 900, 506, s + 2.0, rot=-1.5),""")
rep("g('G08-02', 1380, 330, T('three-quarters'), h=180),","cnt(75, 1380, 340, T('three-quarters'), pre='≈ ', suf='%', cap='of casino revenue: gambling', size=120),")
rep("""    g('G08-03', 960, 440, s, h=420),
    stk('~35 → ~7', 960, 800, T('about seven'), rot=-2, size=50), fx('ding', T('about seven'), 0.4),""","""    bars('Around 2000|35|~35|y;Today|7|~7|r', 420, 420, s, title='Buffets on the Las Vegas Strip', w=1150, rh=100, lw=280, stag=T('about seven') - s),
    fx('ding', T('about seven'), 0.4),""")
# ---------- chapter 7
rep("""scene(s, 'So how does $17 make money?', '', [
    paper(560, 380, 800, 260, s, rot=-1),
    lab('mostly:', 960, 470, T('The answer is mostly'), size=48, cls='serif', italic=True),""","""scene(s, '', '', [
    chap(7, 'So how does $17 make money?', s),
    paper(560, 380, 800, 260, T('The answer is mostly'), rot=-1),
    lab('mostly:', 960, 470, T('The answer is mostly'), size=48, cls='serif', italic=True),""")
rep("g('G08-05', 1360, 300, T('six to six'), h=160),","cnt(6500, 1360, 320, T('six to six'), pre='~', cap='customers / week / restaurant', size=110, frm=0),")
rep("g('G08-06', 1360, 520, T('$7.5'), h=160),","cnt(7.5, 1360, 560, T('$7.5'), pre='$', suf='M', dec=1, cap='a year, best newer locations', size=110),")
rep("g('G05-09', 1360, 720, T('Puerto Rico'), h=110), g('G08-07', 1360, 890, T('$12 million'), h=160), fx('ching', T('$12 million'), 0.45),",
    "cnt(12, 1360, 800, T('$12 million'), pre='$', suf='M', cap='Puerto Rico location', size=110), fx('ching', T('$12 million') + 1.0, 0.45),")
rep("g('G08-08', 960, 360, T('A cook at a normal'), h=380),",
    "bars('Cook to order|25|~25|b;Buffet batch|200|~200|y', 420, 330, T('A cook at a normal'), title='Customers served per hour', w=1100, rh=80, lw=280, stag=T('A buffet cook') - T('A cook at a normal')),")
rep("L('C04-05', T('A cook at a normal'), x=300, h=420), R('C04-06', T('A buffet cook'), x=1620, h=420),",
    "L('C04-05', T('A cook at a normal'), x=260, h=380), R('C04-06', T('A buffet cook'), x=1660, h=380),")
rep("g('G08-10', 1250, 330, T('70 times a year'), h=180),","cnt(70, 1250, 350, T('70 times a year'), pre='~', suf=' visits', cap='a year, most loyal guests', size=120),")
rep("g('G08-11', 600, 340, T('348 restaurants'), h=180),","cnt(348, 600, 360, T('348 restaurants'), cap='Golden Corrals, end of 2025', size=120),")
# ---------- post-processing: first visual at scene start, transitions, chapters
rep("board = dict(version=1, title=\"Why Buffets Don't Lose Money\", duration=DUR, scenes=S)","""for k, sc in enumerate(S):
    vis = [it for it in sc['items'] if it['k'] != 'sfx']
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
board = dict(version=2, title="Why Buffets Don't Lose Money", duration=DUR, scenes=S, chapters=CHAPTERS)""")
open(p,'w').write(h);print('ok')
