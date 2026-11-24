"""Builds editor/storyboard.json for the whole Perseus voiceover.
Layout rules: main character LEFT (x330), second character RIGHT (x1590, auto-turned to face left),
props/third figure CENTRE, notes in the top band; labels sit above figures, never on them."""
import json
W = json.load(open('words_raw.json'))
DUR = 1075.96

def c(word, after, within=25):
    """start time of the first spoken word beginning with `word` at/after `after`"""
    word = word.lower()
    for w in W:
        if w['s'] >= after - 0.3 and w['w'].lower().startswith(word):
            if w['s'] - after > within: break
            return round(w['s'], 2)
    return round(after, 2)

RED = '#D0362C'; WHITE = '#fff'
def ch(a, x, at, h=600, y=1010, out=None, **k):
    d = dict(k='img', a=a, x=x, y=y, h=h, at=at, **k)
    if out is not None: d['out'] = out
    return d
def L(a, at, x=330, **k): return ch(a, x, at, **k)
def Rt(a, at, x=1590, **k): return ch(a, x, at, **k)
def C(a, at, h=480, x=960, **k): return ch(a, x, at, h=h, **k)
def prop(a, x, y, h, at, out=None, **k):
    return ch(a, x, at, h=h, y=y, out=out, center=1, still=1, **k)
def lab(t, x, y, at, out=None, size=42, **k):
    d = dict(k='text', t=t, x=x, y=y, size=size, at=at, **k)
    if out is not None: d['out'] = out
    return d
def stk(t, x, y, at, out=None, rot=-3, size=40):
    d = dict(k='sticker', t=t, x=x, y=y, at=at, rot=rot, size=size)
    if out is not None: d['out'] = out
    return d
def stp(t, x, y, at, out=None, rot=-6, size=54):
    d = dict(k='stamp', t=t, x=x, y=y, at=at, rot=rot, size=size)
    if out is not None: d['out'] = out
    return d
def arc(a, x, y, w, at, out=None, cap=None, rot=2):
    d = dict(k='archive', a=a, x=x, y=y, w=w, at=at, rot=rot)
    if cap: d['cap'] = cap
    if out is not None: d['out'] = out
    return d
def card(bg, x, y, w, h, at, out=None, rot=-1.5, yellow=True, **k):
    d = dict(k='card', bg=bg, x=x, y=y, w=w, h=h, at=at, rot=rot, yellow=yellow, **k)
    if out is not None: d['out'] = out
    return d
def paper(x, y, w, h, at, out=None, rot=-1):
    d = dict(k='card', x=x, y=y, w=w, h=h, at=at, rot=rot)
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
def hl(x, y, w, at, h=32, out=None):
    d = dict(k='hl', x=x, y=y, w=w, h=h, at=at)
    if out is not None: d['out'] = out
    return d
def bub(t, x, y, w, tx, ty, at, out=None, h=110, size=40):
    d = dict(k='bubble', t=t, x=x, y=y, w=w, h=h, tx=tx, ty=ty, at=at, size=size)
    if out is not None: d['out'] = out
    return d
def xm(x, y, at, s=50): return dict(k='xmark', x=x, y=y, s=s, at=at)
def fx(name, at, vol=0.6): return dict(k='sfx', a=name, at=at, vol=vol)
def cracks(x, y, h, at): return prop('E05-04', x, y, h, at)
def stone(a, x, at, h=480, **k): return ch(a, x, at, h=h, **k)

S = []
def scene(s, e, a, b='', items=()):
    S.append(dict(id=f's{len(S)+1:03d}', s=round(s, 2), e=round(e, 2), h=dict(a=a, b=b), items=list(items)))

# Medusa sleeping sprite (363x157): her face sits ~27% across, ~38% up from the feet line
def medusa_face(x, h): w = h * 363 / 157; return (round(x - w / 2 + 0.27 * w), round(1000 - 0.38 * h))

# ---------------- 0:00 cold open (approved sample, tidied) ----------------
scene(0, 10.9, "The Gorgons' cave", '', [
    ch('P02-07', 330, 0.0, h=580),
    ch('P06-05', 1080, 0.3, h=240, y=960, still=1),
    lab('Medusa', 1080, 680, 1.62),
    arc('A-medusa_caravaggio', 1480, 170, 340, 2.85, out=6.1),
    stp('ONE LOOK = STONE', 1640, 640, 4.84, out=6.1, size=46, rot=-5), fx('stamp', 4.84),
    ch('P06-07', 800, 6.79, h=170, y=560), lab('Stheno', 800, 350, 6.9),
    ch('P06-10', 1480, 7.0, h=170, y=560), lab('Euryale', 1480, 350, 7.1),
    stp('IMMORTAL', 800, 250, 8.42, size=46, rot=-4), stp('IMMORTAL', 1480, 250, 8.6, size=46, rot=4), fx('stamp', 8.42),
    stk('mortal', 1250, 670, 9.3, size=36),
])
scene(10.9, 17.8, 'On the way in', '', [
    stone('P11-08', 330, 12.34, h=460, y=1000), stone('P11-06', 780, 12.77, h=350, y=1000), stone('P11-04', 1200, 13.2, h=470, y=1000),
    cracks(330, 740, 260, 14.07), cracks(790, 830, 220, 14.2), cracks(1200, 740, 260, 14.35), fx('crack', 14.07),
    stk('turned to stone', 770, 300, 13.47, size=46),
    ch('P10-11', 1640, 15.4, h=360, y=1000, stone=True), cracks(1640, 820, 200, 16.1), fx('crack', 16.1, 0.4),
    stk('even the animals', 1640, 520, 15.6, rot=3),
])
fx_ = medusa_face(1150, 260)
scene(17.8, 23.3, "The Gorgons' cave", '', [
    L('P01-07', 17.83, x=430),
    prop('E05-08', 250, 430, 200, 19.11, out=20.2), fx('swish', 19.11),
    ch('P06-05', 1150, 17.83, h=260, y=1000, still=1),
    arc('A-pelike_met', 1490, 150, 330, 19.47),
    stk('eyes on the shield', 520, 300, 20.17),
    loop(fx_[0], fx_[1], 95, 80, 21.37),
    stp("DON'T LOOK", 1010, 620, 22.29, size=56), fx('stamp', 22.29),
])
scene(23.3, 25.05, '', '', [
    stk('rewind', 960, 380, 23.36, size=44, rot=-4), fx('rewind', 23.3),
    lab("And the reason he's here?", 960, 590, 23.36, size=120, cls='serif', italic=True, typeOn=True),
    hl(1330, 615, 330, 24.15, h=36),
])
scene(25.05, 33.2, 'The island of Seriphos', '', [
    Rt('P04-09', 25.09, x=1560), lab('King Polydectes', 1560, 370, 25.21),
    ch('E06-03', 960, 26.66, h=180, y=1000, still=1), stk('wedding gift', 960, 770, 27.14, rot=3),
    L('P01-02', 27.94),
    bub("I'll bring you Medusa's head!", 400, 170, 600, 390, 410, 28.87, out=30.7),
    stp('KING #2', 1120, 330, 31.09, size=60), fx('stamp', 31.09),
    lab('tried to get him killed', 1120, 440, 31.82, size=40, typeOn=True),
])
scene(33.2, 38.8, 'Argos', '', [
    L('P04-01', 33.27, out=37.41), L('P04-04', 37.41, x=350, noPop=True),
    stp('KING #1', 330, 280, 33.82, size=60), fx('stamp', 33.82),
    stk('his grandfather', 800, 420, 34.11, out=37.41),
    prop('P03-09', 1200, 820, 190, 36.35, out=37.41), lab('baby Perseus', 1200, 680, 36.35, out=37.41),
    arrow(620, 640, 1080, 800, 37.45, bend=-25), fx('whoosh', 37.35),
    ch('E01-03', 1250, 37.41, h=280, y=960, still=1), ch('E03-05', 1640, 37.98, h=400, still=1), fx('splash', 37.98),
])
scene(38.8, 42.45, 'Argos', '', [
    L('P04-01', 38.8, noPop=True),
    paper(640, 330, 560, 330, 38.99, rot=-2),
    lab('Acrisius', 920, 500, 39.81, size=120, cls='serif', typeOn=True),
    hl(740, 555, 360, 40.76, h=38), lab('King of Argos', 920, 600, 40.76, size=52),
    arc('A-cast_out_met', 1300, 190, 540, 41.0),
])
scene(42.45, 59.9, 'The oracle', 'Argos', [
    L('P04-01', 42.45, noPop=True, out=53.67), L('P04-02', 53.67, x=370, noPop=True),
    Rt('P09-01', 43.03, x=1610, h=540), lab('the oracle', 1610, 430, 43.2),
    card('B01-02', 860, 230, 480, 340, 42.84, out=45.2, rot=1.5),
    bub('I want a son.', 400, 200, 380, 380, 420, 43.8, out=45.2),
    stk('the prophecy', 1000, 220, 45.6, size=44, rot=-2),
    ch('P03-05', 860, 48.47, h=380, y=1000), lab('his daughter Danaë', 860, 580, 48.6, out=57.97),
    arrow(960, 820, 1180, 870, 50.32, bend=-20),
    prop('P03-09', 1270, 900, 130, 50.68), lab('a boy', 1270, 790, 50.68, out=55.27),
    arrow(1300, 760, 620, 440, 52.84, bend=45, color=RED),
    stp('WILL KILL HIM', 1000, 330, 53.67, rot=-5), fx('stamp', 53.67),
    xm(1270, 900, 55.27, s=55),
    stk('not born yet', 1270, 790, 55.46, rot=4, size=38),
    stk('not even pregnant', 860, 575, 57.97, rot=-2, size=38),
])
scene(59.9, 74.2, 'The bronze chamber', 'under the palace', [
    lab('the sensible response:', 960, 260, 59.91, size=84, cls='serif', italic=True, typeOn=True, out=63.2),
    hl(900, 280, 290, 61.83, out=63.2),
    L('P04-03', 59.91, out=70.43), L('P04-05', 70.43, noPop=True, face='L'),
    ch('E01-05', 1000, 63.32, h=200, y=960, out=65.4, still=1),
    card('B01-03', 700, 200, 700, 450, 63.78),
    lab('underground, bronze', 1050, 710, 64.54, size=44, out=67.7),
    ch('P03-05', 1050, 65.3, h=330, y=610),
    prop('E05-09', 1050, 450, 340, 66.5, out=67.3),
    ch('E01-04', 1050, 66.6, h=370, y=625, still=1), fx('clang', 66.6),
    arc('A-tower_brass', 1560, 170, 250, 64.0),
    stk('his death', 330, 300, 69.73, rot=-4),
    arrow(470, 320, 740, 420, 71.29, bend=-20),
    stk('her problem', 1050, 715, 71.64, rot=3),
    paper(650, 820, 1190, 190, 72.11),
    lab("someone else's", 710, 950, 72.11, size=64, cls='serif', italic=True, anchor='start'),
    hl(1190, 940, 610, 72.4, h=46),
    lab('HOUSING PROBLEM', 1210, 955, 72.4, size=80, cls='anton', anchor='start'),
])

# ---------------- 1:14 Zeus, the chest, Seriphos ----------------
t = 74.2
scene(t, 83.5, 'The bronze chamber', 'Argos', [
    card('B01-03', 620, 200, 620, 420, t, noPop=True),
    stk('kept men out', 930, 690, t, rot=2),
    Rt('P05-08', c('zeus', 74)), lab('Zeus', 1590, 370, c('zeus', 74)),
    prop('E01-06', 930, 330, 220, c('shower', 75)), prop('E01-07', 930, 470, 380, c('gold', 76)),
    L('P03-05', c('donny', 78), out=c('gave', 80)), lab('Danaë', 330, 360, c('donny', 78)),
    L('P03-06', c('gave', 80), noPop=True), stk('baby Perseus', 330, 290, c('perseus', 81)),
])
scene(83.5, 100.45, 'Argos', '', [
    L('P04-01', 83.5, out=c('pass', 87)), L('P04-04', c('pass', 87), noPop=True),
    stk("didn't believe her", 330, 330, c('refuse', 84)),
    Rt('P03-06', 83.5, out=c('chest', 86.5)),
    ch('P12-01', 1200, c('chest', 86.5), h=300, y=980, still=1), fx('whoosh', c('pass', 87)),
    ch('E03-05', 1660, c('sea', 88), h=380, still=1), fx('splash', c('sea', 88)),
    stk('plan A: bronze room', 900, 250, c('bronze', 91), rot=-2), xm(1110, 250, c('failed', 92), s=36),
    stk('plan B: wooden box + water', 900, 350, c('wooden', 96), rot=2),
])
scene(100.45, 117.44, 'The island of Seriphos', '', [
    card('B02-01', 640, 170, 640, 400, 100.45),
    ch('P12-01', 960, 100.6, h=280, y=1000, still=1, out=c('growing', 111.5)),
    L('P12-02', c('dick', 103)), lab('Dictys, a fisherman', 330, 380, c('dick', 103)),
    ch('P04-01', 1660, c('king', 108), h=380), stk('lost track', 1660, 560, c('lost', 108), rot=3),
    ch('P03-11', 960, c('growing', 111.5), h=360, y=1000), stk('safe', 960, 610, c('reason', 113), rot=-2),
])
scene(117.44, 139.6, 'Seriphos', 'years later', [
    L('P08-08', 117.44, out=c('adulthood', 131)), lab('Dictys', 330, 360, 117.6, out=c('adulthood', 131)),
    C('P03-01', 118.0, h=500), lab('Danaë', 960, 450, 118.2),
    Rt('P04-07', c('brother', 124)), lab('Polydectes', 1590, 360, c('name', 127.7)),
    stk("Dictys's brother", 1590, 290, c('brother', 124), rot=3),
    stp('KING OF THE ISLAND', 1590, 200, c('king', 129), size=40), fx('stamp', c('king', 129)),
    L('P01-01', c('adulthood', 131), noPop=False),
    arrow(1400, 640, 1090, 700, c('interested', 133), bend=20, color=RED),
    stk('interested in Danaë', 1250, 820, c('interested', 133), rot=-2),
    stp('IN THE WAY', 330, 330, c('stood', 137.5), size=50), fx('stamp', c('stood', 137.5)),
])
scene(139.6, 157.4, "Polydectes' palace", 'Seriphos', [
    Rt('P04-09', 139.6), lab('Polydectes', 1590, 370, 139.8),
    stk('impressive when announced', 820, 300, c('impressive', 143), out=147.1),
    stk('fatal when attempted', 820, 400, c('fatal', 145), out=147.1, rot=2),
    L('P11-01', c('gathered', 147)), ch('P11-02', 760, c('friends', 147.5), h=520, out=c('hip', 152.5)),
    ch('E06-03', 1180, c('wedding', 149), h=170, y=1000, still=1), stk('wedding gift', 1180, 780, c('wedding', 149)),
    ch('P09-09', 760, c('hip', 152.5), h=520), lab('Hippodamia', 760, 450, c('hip', 152.5)),
    stk('so he claimed', 760, 380, c('claimed', 153), rot=3),
])
scene(157.4, 184.34, "Polydectes' palace", 'Seriphos', [
    L('P01-02', 157.4), Rt('P04-09', 157.4, noPop=True),
    bub("I'll bring back a Gorgon's head!", 380, 160, 620, 380, 400, c('declared', 160.5), out=170.7),
    stk('dangerous enthusiasm', 960, 560, c('dangerous', 164), out=170.7),
    ch('P10-11', 960, c('horses', 171), h=330, y=1000, out=c('head', 176)), stk('everyone else: horses', 960, 600, c('horses', 171), out=175.9),
    dict(xm(960, 860, c('no', 174), s=60), out=c('head', 176)), fx('stamp', c('no', 174), 0.4),
    prop('P06-04', 960, 640, 230, c('head', 176)),
    stk('his own idea', 330, 330, c('idea', 178)),
    stp('ASSIGNMENT', 960, 380, c('assignment', 182), size=60), fx('stamp', c('assignment', 182)),
])

# ---------------- 3:04 Medusa and the Gorgons ----------------
scene(184.34, 210.7, 'Medusa', '', [
    Rt('P06-01', 184.34), lab('Medusa', 1590, 360, c('medusa', 184.5)),
    stone('P11-04', 960, c('anyone', 186.5), h=460, out=190.1), dict(cracks(960, 760, 240, c('stone', 188)), out=190.1), fx('crack', c('stone', 188)),
    stp('LOOK = STONE', 960, 300, c('stone', 188), out=190.1),
    L('P02-04', 190.15),
    prop('E02-06', 960, 640, 240, c('weapon', 192), out=194.8),
    stk('step 1: find it with your eyes', 960, 330, c('ordinary', 195), out=204),
    prop('E02-10', 960, 640, 150, c('eyes', 197), out=204), xm(960, 640, c('last', 201), s=70),
    ch('P06-09', 860, c('sisters', 205), h=470), lab('Stheno', 860, 500, c('steen', 206)),
    ch('P06-12', 1250, c('sisters', 205.4), h=470), lab('Euryale', 1250, 500, c('you', 207)),
    stp('3 GORGONS', 1060, 250, c('three', 208.5), size=56), fx('stamp', c('three', 208.5)),
])
scene(210.7, 237.7, 'The Gorgons', 'as described by Apollodorus', [
    C('P06-02', 210.78, h=560),
    stk('snakes for hair', 560, 330, c('heads', 212)), arrow(690, 360, 880, 470, c('heads', 212.2), bend=-25),
    stk('tusks', 1380, 420, c('tasks', 214), rot=3), arrow(1300, 450, 1010, 560, c('tasks', 214.2), bend=25),
    stk('bronze hands', 560, 760, c('bronze', 215.5), rot=2), arrow(690, 760, 860, 800, c('bronze', 215.7), bend=20),
    stk('golden wings', 1380, 700, c('golden', 217), rot=-2),
    prop('E05-06', 1380, 560, 200, c('fly', 220)),
    stk('they could fly', 960, 230, c('fly', 220)),
])
scene(220.9, 237.7, 'The Gorgons', '', [
    ch('P06-09', 420, c('three', 221), h=500), ch('P06-02', 960, c('three', 221), h=500, noPop=True), ch('P06-12', 1500, c('three', 221), h=500),
    stk('faces that kill', 960, 300, c('faces', 222.5), out=230.2),
    stk('nowhere to hide from fliers', 960, 300, c('running', 225.6), out=230.2, rot=2),
    stp('IMMORTAL', 420, 380, c('immortal', 231), size=46), stp('IMMORTAL', 1500, 380, c('immortal', 231.3), size=46, rot=5), fx('stamp', c('immortal', 231)),
    stk('mortal', 960, 330, c('die', 234), rot=-3),
    loop(960, 770, 190, 260, c('king', 236)),
])
fm = medusa_face(960, 240)
scene(237.7, 266.5, 'Which sister?', '', [
    ch('P06-07', 600, 237.76, h=170, y=640), ch('P06-10', 1320, 237.76, h=170, y=640),
    ch('P06-05', 960, 237.76, h=240, y=1000, still=1),
    stk('?', 600, 440, c('pick', 240.5), size=44), stk('?', 1320, 440, c('pick', 240.7), size=44, rot=4), stk('?', 960, 720, c('pick', 241), size=44),
    loop(fm[0], fm[1], 95, 80, c('right', 241.5)),
    stk('eyes off their faces', 960, 250, c('eyes', 243)),
])
scene(246.2, 266.5, 'Two versions', '', [
    paper(160, 200, 700, 300, 246.24, rot=-1.5),
    lab('Hesiod', 510, 300, 246.4, size=72, cls='serif'),
    lab('a family of sea monsters', 510, 400, c('family', 247.5), size=40),
    ch('P10-08', 510, c('monstrous', 248.5), h=170, y=700),
    paper(1060, 200, 700, 300, c('roman', 251), rot=1.5),
    lab('Ovid', 1410, 300, c('roman', 251.2), size=72, cls='serif'),
    lab('a different past', 1410, 400, c('constructive', 252.5), size=40),
    stk('told by Perseus, at a wedding', 1410, 600, c('wedding', 256), rot=2),
    stk('why the snakes?', 1410, 700, c('snakes', 259), rot=-2),
    stp('HARDER TO CHEER FOR', 960, 900, c('cheer', 263), size=50), fx('stamp', c('cheer', 263)),
])

# ---------------- 4:26 divine help, Gray Sisters, nymphs ----------------
scene(266.5, 287.2, 'Divine help', '', [
    L('P01-03', 266.54, out=275.7),
    C('P05-01', c('athena', 269), h=540, out=275.7), lab('Athena', 960, 430, c('athena', 269), out=275.7),
    Rt('P05-04', c('hermes', 270), out=275.7), lab('Hermes', 1590, 370, c('hermes', 270), out=275.7),
    stk('step 1: directions', 960, 250, c('first', 273.3), out=281.4),
    L('P01-01', 275.7, noPop=True),
    ch('P12-04', 1300, c('sisters', 276), h=480, out=287.2), lab('the Gray Sisters', 1300, 470, c('sisters', 276)),
    stk('born already old', 1300, 400, c('old', 280), rot=2),
    prop('E02-10', 820, 560, 110, c('single', 282)), lab('one eye', 820, 470, c('single', 282)),
    prop('E02-11', 820, 760, 110, c('tooth', 283.5)), lab('one tooth', 820, 680, c('tooth', 283.5)),
])
scene(287.2, 304.5, 'The Gray Sisters', '', [
    L('P01-01', 287.2, noPop=True),
    prop('E02-10', 560, 600, 100, c('possession', 287.5)), prop('E02-11', 600, 690, 90, c('possession', 287.8)),
    ch('P07-01', 1050, 287.6, h=470), ch('P07-03', 1600, 288.0, h=470),
    bub('Give them back!', 1080, 180, 420, 1320, 520, c('demanded', 290), out=294.6),
    stk('directions to the nymphs first', 900, 300, c('directions', 292), out=304.4),
    stp('HOSTAGE: 1 EYE, 1 TOOTH', 960, 420, c('dental', 301), size=46), fx('stamp', c('dental', 301)),
])
scene(304.5, 330.9, 'The nymphs', 'their spring grove', [
    L('P01-01', 304.5, noPop=True),
    ch('P07-07', 820, c('wing', 312), h=480), lab('winged sandals', 820, 470, c('wing', 312)),
    ch('P07-08', 1220, c('cap', 313.3), h=480), lab('cap of Hades', 1220, 470, c('cap', 313.3)),
    ch('P07-09', 1620, c('pouch', 316.8), h=480), lab('the kibisis (bag)', 1620, 470, c('pouch', 316.8)),
    stk('three gifts', 1220, 250, c('three', 309), out=320.9),
    stk('to get there', 820, 380, c('samples', 321), rot=-2),
    stk('to get away', 1220, 380, c('cap', 323), rot=2),
    stk('never look inside', 1620, 380, c('bag', 325), rot=-2),
])
scene(330.9, 345.6, 'The last piece', '', [
    L('P01-01', 330.9, noPop=True),
    Rt('P05-05', 330.91, out=339.5), lab('Hermes', 1590, 370, 331.0, out=339.5),
    stk('a curved blade of adamant', 1590, 290, c('curved', 332), out=339.5),
    stk('see her without looking at her', 960, 250, c('last', 334.5), rot=2),
    prop('E02-07', 960, 640, 360, c('ordinary', 342.5)),
    stp('A SHIELD', 960, 900, c('battle', 344.5), size=56), fx('stamp', c('battle', 344.5)),
])

# ---------------- 5:45 back in the cave ----------------
scene(345.6, 357.8, "The Gorgons' cave", 'back where we started', [
    stk('back where we started', 960, 250, 345.67, rot=-2),
    stone('P11-08', 330, c('frozen', 349.5), h=440, y=1000), stone('P11-06', 780, c('frozen', 349.8), h=340, y=1000),
    stone('P11-04', 1200, c('frozen', 350.1), h=450, y=1000), ch('P10-11', 1640, c('animals', 349), h=340, y=1000, stone=True),
    cracks(330, 760, 240, c('line', 351.5)), cracks(1200, 760, 240, c('line', 351.7)), cracks(1640, 830, 190, c('line', 351.9)), fx('crack', c('line', 351.5)),
    stk('frozen in the pose they were in', 960, 360, c('post', 355)),
])
fm2 = medusa_face(1080, 240)
scene(357.8, 367.8, "The Gorgons' cave", '', [
    L('P02-07', 357.85, h=580),
    ch('P06-07', 760, c('sleeping', 359.5), h=170, y=640), ch('P06-10', 1480, c('sleeping', 359.7), h=170, y=640),
    ch('P06-05', 1080, c('sleeping', 359.9), h=240, y=1000, still=1),
    stk('all three asleep', 1120, 400, c('all', 361.6)),
    stp('THE ONLY SAFE MOMENT', 1120, 250, c('moment', 365), size=46), fx('stamp', c('moment', 365)),
])
fm3 = medusa_face(1460, 260)
scene(367.8, 395.1, "The Gorgons' cave", '', [
    L('P12-03', 367.81),
    ch('P06-05', 1460, 367.9, h=260, y=1000, still=1),
    prop('E02-09', 960, 400, 320, c('reflection', 371.5)), stk('her reflection', 960, 200, c('reflection', 371.5)),
    stk('face turned away', 330, 330, c('face', 376)),
    stk('watch her in the bronze', 960, 650, c('watch', 381), rot=2),
    loop(fm3[0], fm3[1], 95, 80, c('directly', 385)),
    stp("DON'T LOOK", 1460, 640, c('directly', 385.2), size=56), fx('stamp', c('directly', 385.2)),
])
scene(395.1, 422.2, 'The strike', '', [
    L('P01-07', 395.16, x=430),
    C('P05-02', 395.3, h=480, out=400.4), lab('Athena guides his hand', 960, 470, 395.5, out=400.4),
    prop('E05-08', 250, 430, 200, c('came', 397), out=399), fx('swish', c('came', 397)),
    arc('A-pelike_met', 1480, 160, 330, c('head', 398.5), out=405),
    prop('E05-02', 960, 640, 420, c('winged', 400.5), out=403.4),
    C('P10-02', c('winged', 400.6), h=460), lab('Pegasus', 960, 470, c('pegasus', 403.4)),
    Rt('P10-05', c('second', 405.2)), lab('Chrysaor', 1590, 370, c('chris', 406)),
    stk("Medusa's children, by Poseidon", 960, 250, c('both', 408.6)),
    prop('E06-09', 1590, 290, 150, c('golden', 413), rot=-20), stk('"golden sword"', 1590, 200, c('golden', 413), rot=3),
    stk('later: a problem for Heracles', 960, 340, c('problem', 419), rot=2),
])
scene(422.2, 438.4, 'Escape', '', [
    L('P02-02', 422.21), Rt('P10-01', 422.3),
    stk('finally, a horse', 1590, 360, c('finally', 425.5)),
    stk('Pegasus belongs to a later hero', 960, 250, c('pegasus', 430.7), out=433.4),
    prop('E02-01', 960, 640, 180, c('sandals', 434.5)),
    stp('TWO GORGONS WAKING UP', 960, 360, c('wake', 436.5), size=46), fx('stamp', c('wake', 436.5)),
])
scene(438.4, 474.3, 'Escape', '', [
    L('P14-02', 438.41, out=c('cap', 446.3)),
    ch('P06-08', 1100, c('pursued', 440.5), h=460, out=451.3), ch('P06-11', 1600, c('pursued', 440.8), h=460, out=451.3), fx('whoosh', c('pursued', 440.5)),
    stk('furious sisters', 1350, 330, c('sister', 442.4), out=451.3),
    L('P12-06', c('cap', 446.3), noPop=True), stk('invisible', 330, 330, c('cap', 446.5)),
    stk('chasing nobody they can see', 1350, 420, c('seeing', 448), out=451.3, rot=2),
    C('P05-11', 451.4, h=520), lab('Athena', 960, 450, 451.6),
    stk("the sisters' grief", 960, 260, c('grief', 452.5), rot=-2),
    stk('becomes a song for the aulos', 960, 360, c('musical', 459), rot=2),
    stp('GRIEF YOU CAN PERFORM', 1560, 640, c('perform', 471), size=42), fx('stamp', c('perform', 471), 0.4),
])

# ---------------- 7:54 Andromeda ----------------
scene(474.3, 498.2, 'The flight home', '', [
    ch('P01-05', 420, 474.37, h=420, y=760),
    prop('P14-11', 960, 700, 220, c('bag', 477.5), out=489), stk('does it still work?', 960, 470, c('still', 478), out=489),
    card('B03-02', 760, 180, 720, 440, c('perseus', 489), rot=1.5),
    ch('P08-05', 1250, c('woman', 490), h=480, y=1010), lab('Andromeda', 1250, 470, c('andromeda', 492.5)),
    ch('P10-08', 1680, c('monster', 495), h=170, y=900), stk('already on its way', 1680, 760, c('already', 496), rot=3),
])
scene(498.2, 515.6, 'Why she was chained', '', [
    L('P12-12', 498.21), lab('Queen Cassiopeia', 330, 360, 498.4),
    stk('more beautiful than the sea nymphs', 960, 250, c('beauty', 502)),
    Rt('P07-12', c('nymphs', 506.4), out=508.3),
    Rt('P05-10', c('side', 508.3)), lab('Poseidon', 1590, 370, c('side', 508.3)),
    prop('E05-12', 960, 520, 260, c('flood', 509.5)),
    ch('P10-09', 1000, c('monster', 510.5), h=300, y=1000),
    stp('OVERREACTION', 960, 360, c('destructive', 512.5), size=52), fx('stamp', c('destructive', 512.5)),
])
scene(515.6, 531.3, 'Why she was chained', '', [
    card('B03-03', 620, 180, 640, 400, 515.67),
    Rt('P09-02', c('oracle', 520)), lab('an oracle', 1590, 370, c('oracle', 520)),
    stk('give Andromeda to the creature', 940, 660, c('andromeda', 522.5), rot=2),
    L('P09-05', c('father', 527.5)), lab('King Cepheus', 330, 360, c('father', 527.5)),
    stp('UNDER PRESSURE', 330, 280, c('pressure', 526.5), size=44), fx('stamp', c('pressure', 526.5), 0.4),
])
scene(531.3, 554.2, 'Two boasts', '', [
    L('P01-02', 531.35, out=537.5), prop('P06-04', 720, 720, 170, 532.0, out=537.5),
    stk("Perseus's boast", 520, 300, 531.6, out=537.5), arrow(480, 640, 640, 700, 532.2, bend=-20, out=537.5),
    Rt('P12-12', c('casio', 534.5), out=537.5), ch('P10-08', 1200, c('daughter', 536), h=150, y=760, out=537.5),
    stk("Cassiopeia's boast", 1400, 300, c('casio', 534.5), out=537.5), arrow(1440, 640, 1320, 700, c('daughter', 536), bend=20, out=537.5),
    L('P12-07', 537.6, noPop=True), C('P08-01', 537.7, h=500), lab('Andromeda', 960, 470, 537.8),
    Rt('P12-11', c('bargain', 546)), lab('Cepheus', 1590, 370, c('bargain', 546)),
    stk('he fell in love', 330, 330, c('love', 543), rot=-3, out=548.9),
    bub('I kill the monster, I marry her.', 260, 150, 640, 360, 400, c('kill', 549), out=554.2),
])
scene(554.2, 602.2, 'The fight at sea', '', [
    stp('DEAL', 960, 250, 554.3, size=70, out=557), fx('stamp', 554.3),
    ch('P01-05', 520, c('takes', 559), h=420, y=620, out=567.5),
    stk('his shadow on the water', 520, 760, c('shadow', 560), out=567.5),
    Rt('P10-07', c('creature', 562.8), x=1500, h=560),
    stk('it attacks the shadow', 1100, 300, c('attacks', 564), out=575.7),
    ch('P13-01', 920, c('drops', 567.6), h=360, y=640, out=588.1), prop('E05-08', 1140, 520, 220, c('strikes', 569.5), out=572), fx('swish', c('strikes', 569.5)),
    prop('E05-10', 1300, 640, 300, c('thrash', 576), out=588), fx('splash', c('thrash', 576)),
    prop('E05-11', 760, 420, 200, c('spray', 578.4), out=588),
    stk('wet wings get heavy', 960, 250, c('heavier', 586.2)),
    ch('E03-01', 560, c('rock', 588.3), h=300, y=1010, still=1),
    ch('P13-02', 560, c('hand', 590.5), h=420, y=800),
    stk('finishing it from a rock', 960, 360, c('clinging', 596), rot=2),
])

# ---------------- 10:02 after the rescue ----------------
scene(602.2, 612.5, 'The rescue', '', [
    L('P01-10', 602.27, x=520), lab('Andromeda, free', 520, 380, 602.5),
    Rt('P10-10', 602.3, h=300, x=1600), stk('defeated', 1600, 640, 603, rot=3),
    prop('E03-03', 640, 960, 140, 602.6),
    stk('on his way home, supposedly', 960, 250, c('trip', 610), rot=-2),
])
scene(612.5, 632.4, 'The origin of coral', 'according to Ovid', [
    L('P02-09', 612.55),
    prop('P06-04', 960, 620, 200, c('lays', 617)),
    ch('E03-11', 960, c('plants', 618), h=180, y=900, still=1),
    ch('E03-11', 1400, c('hard', 621), h=180, y=900, still=1, stone=True), arrow(1080, 880, 1290, 880, c('hard', 621), bend=-20),
    stk('coral', 1400, 700, c('coral', 626), rot=3), fx('crack', c('hard', 621), 0.35),
    stk('still changing things', 960, 260, c('changing', 628.5)),
])
scene(632.4, 651.4, 'The wedding feast', '', [
    L('P02-01', 632.49), prop('E01-09', 960, 900, 200, 633, out=638.3), stk('offerings to the gods', 960, 680, 633.2, out=638.3),
    ch('E07-04', 960, c('feast', 638.6), h=230, y=1010, still=1),
    Rt('P11-02', c('guests', 639)), lab('wedding guests', 1590, 380, c('guests', 639)),
    stk('how did you do it?', 1590, 300, c('how', 640), out=645, rot=3),
    bub('Why did she have snakes for hair?', 1000, 150, 640, 1450, 420, c('why', 645), out=651.4),
])
scene(651.4, 687.8, "Medusa's story", "Ovid's version", [
    stk('once admired for her beauty', 960, 250, c('medusa', 651.6), out=661.6),
    stk('especially her hair', 960, 340, c('hair', 655.5), out=661.6),
    prop('E03-12', 960, 760, 460, 652, out=661.6), lab("Athena's temple", 960, 480, c('temple', 659), out=661.6),
    Rt('P05-09', c('poseidon', 657.6), out=661.6), lab('Poseidon', 1590, 370, c('poseidon', 657.6), out=661.6),
    stk('he assaulted her there', 1590, 300, c('assaulted', 658.5), out=661.6, rot=2),
    Rt('P05-11', c('athena', 661.8), face='R'), stk('looked away', 1590, 330, c('turned', 662), rot=3),
    C('P06-02', c('snakes', 664), h=500), stk('she was the one punished', 960, 330, c('punishment', 669), rot=-2, out=679.4),
    L('P02-11', c('celebrating', 672.5)), stk('celebrating her killer', 330, 330, c('killer', 673)),
    stk('the same goddess who guided his hand', 960, 230, c('same', 681.5), rot=2),
    prop('P14-11', 640, 900, 160, c('head', 685)),
])
scene(687.8, 729.9, 'The wedding', 'interrupted', [
    L('P02-01', 687.81),
    C('P08-02', 688.5, h=500, out=705), lab('Andromeda', 960, 470, 688.6, out=705),
    Rt('P09-06', c('door', 689.5)), lab('Phineus', 1590, 370, c('name', 696.7)),
    stk('a spear and a claim', 1590, 290, c('speedier', 691), out=696.6),
    stk('her fiancé, and her uncle', 1590, 290, c('brother', 699), rot=2),
    ch('P11-07', 1180, c('armed', 707), h=440), stk('armed friends', 1180, 520, c('supporters', 708)),
    stk('"he stole my bride"', 960, 230, c('bride', 711), out=712.8),
    C('P09-04', c('points', 713), h=500, x=760), lab('Cepheus', 760, 470, c('points', 713)),
    stk('where were you for the monster?', 760, 380, c('monster', 717), rot=-2),
    stp('WANTS TO COLLECT', 1590, 200, c('collect', 728.5), size=44), fx('stamp', c('collect', 728.5)),
])
scene(729.9, 766.6, 'The wedding brawl', '', [
    L('P13-02', 729.96), Rt('P09-07', 730),
    prop('E05-07', 960, 560, 200, c('spear', 731), out=737), fx('swish', c('spear', 731)),
    stk('sent back', 960, 400, c('back', 735.2), out=737),
    ch('E01-09', 1250, c('altar', 738.5), h=180, y=1010, still=1),
    stp('BRAWL', 960, 260, c('fighting', 741), size=70), fx('stamp', c('fighting', 741)),
    stk('even the musician', 960, 380, c('musician', 752.5), rot=2),
    ch('E03-12', 620, c('pillar', 755), h=520, y=1010, still=1), stk('back to a pillar', 620, 420, c('pillar', 755)),
    stk('strength running out', 330, 330, c('strength', 761)),
    prop('P14-11', 960, 720, 200, c('thing', 763.5)), loop(960, 720, 140, 120, c('thing', 764)),
])
scene(766.6, 813.5, 'The wedding brawl', '', [
    L('P14-04', 771.5),
    bub('Turn your faces away!', 380, 150, 540, 380, 400, c('warns', 771.6), out=776.4),
    Rt('P11-07', c('attacker', 777), out=c('freezes', 780)), Rt('P11-08', c('freezes', 780), noPop=True),
    cracks(1590, 760, 240, c('freezes', 780)), fx('crack', c('freezes', 780)),
    stk('even his own side', 960, 250, c('supporters', 786), rot=-2),
    stone('P11-04', 1000, c('hardens', 788.5), h=460), cracks(1000, 760, 220, c('hardens', 789)), fx('crack', c('hardens', 789), 0.4),
    prop('E05-08', 1250, 520, 200, c('swing', 791.5), out=796), fx('clang', c('rings', 794.5), 0.4),
    stk('*clang*', 1250, 400, c('rings', 794.5), out=800, rot=4),
    stp('NO SIDES', 960, 360, c('side', 806.5), size=60), fx('stamp', c('side', 806.5)),
    stk('only Perseus chooses when', 960, 460, c('choose', 808.5), rot=2),
])
scene(813.5, 845.0, 'The wedding hall', '', [
    stk('200 attackers', 960, 250, c('hundred', 814.5), out=823.8),
    stone('P11-04', 420, c('hundred', 815), h=440, out=823.8), ch('P14-07', 960, c('remaining', 815.5), h=420, out=823.8), stone('P11-08', 1500, c('stone', 817), h=440, out=823.8),
    fx('crack', c('stone', 817)),
    stk('a room of fixed bodies', 960, 360, c('collection', 820), out=823.8),
    stone('P11-08', 860, 823.9, h=420), stone('P11-06', 1200, 824.0, h=330),
    Rt('P09-06', c('phineas', 824), out=c('joins', 839)), lab('Phineus', 1590, 370, c('phineas', 824), out=c('joins', 839)),
    stk('hard and silent', 1030, 380, c('silent', 831)),
    stk('now he surrenders', 1590, 300, c('surrender', 834.5), out=c('joins', 839)),
    L('P14-04', c('turns', 838)),
    Rt('P09-08', c('joins', 839), noPop=True), cracks(1590, 760, 240, c('joins', 839.2)), fx('crack', c('joins', 839.2)),
    stk('frozen asking for mercy', 1590, 300, c('mercy', 842), rot=3),
])

# ---------------- 14:05 home to Seriphos ----------------
scene(845.0, 857.0, 'Leaving the wedding', '', [
    C('P13-12', 845.0, h=520, x=700),
    stk('Gorgons ✓', 1450, 300, c('borg', 853)), stk('a sea monster ✓', 1450, 400, c('busey', 854.5), rot=2), stk('his own wedding ✓', 1450, 500, c('wedding', 855.5), rot=-2),
])
scene(857.0, 881.9, 'Seriphos', 'meanwhile', [
    Rt('P04-08', 857.04), lab('Polydectes', 1590, 370, 857.2),
    L('P03-02', 858.0, out=c('refuge', 868.5)), lab('Danaë', 330, 360, 858.1, out=c('refuge', 868.5)),
    stk('alone, without her son', 330, 290, c('without', 862), out=c('refuge', 868.5)),
    card('B03-04', 640, 190, 640, 340, c('refuge', 868.5)),
    ch('P03-08', 820, c('refuge', 868.8), h=330, y=1010), ch('P08-10', 1150, c('refuge', 869.1), h=330, y=1010),
    stk('sheltering from his own brother', 960, 610, c('sheltering', 875), rot=2),
    ch('P13-06', 330, c('finds', 880.2), h=600, noPop=False),
])
scene(881.9, 912.8, "Polydectes' palace", '', [
    Rt('P04-09', 881.9, out=c('reveals', 893)), lab('Polydectes', 1590, 370, 882, out=c('reveals', 893)),
    C('P11-03', 882.3, h=480, out=c('reveals', 893)),
    stk('asked in public', 960, 250, c('company', 887), out=888.4), stk('delivered in public', 960, 250, c('company', 889.5), rot=2, out=891),
    L('P14-01', c('turning', 891.2)),
    Rt('P04-12', c('reveals', 893), noPop=True), ch('P14-07', 960, c('reveals', 893), h=420, noPop=True),
    cracks(1590, 760, 240, c('stone', 896)), fx('crack', c('stone', 896)),
    stp('WEDDING GIFT: DELIVERED', 960, 280, c('gift', 901.5), size=48), fx('stamp', c('gift', 901.5)),
])
scene(904.1, 912.8, 'Seriphos', 'a new king', [
    C('P13-11', 904.19, h=520), lab('King Dictys', 1060, 450, c('dick', 905)),
    stk('the man who took them in', 960, 260, c('took', 907)),
])
scene(912.8, 945.1, 'Returning the gifts', '', [
    C('P14-05', 912.89, h=500),
    prop('E02-01', 640, 280, 120, c('sandals', 913.5)), prop('E02-03', 960, 280, 120, c('cap', 914)), prop('E02-04', 1280, 280, 120, c('pouch', 914.5)),
    stk('back to the nymphs', 960, 420, c('nymphs', 916), out=918.6),
])
scene(918.6, 945.1, "Athena's shield", '', [
    L('P05-03', c('athena', 919)), lab('Athena', 330, 360, c('athena', 919)),
    prop('E02-09', 960, 520, 340, c('shield', 921)), stk('facing outward at her enemies', 960, 250, c('outward', 925)),
    arc('A-medusa_caravaggio', 1450, 220, 360, c('objects', 931), cap='Caravaggio painted Medusa on a parade shield, 1597'),
    stk('a face that protects', 960, 800, c('protection', 937), rot=2),
])

# ---------------- 15:45 Argos, Larissa, the discus ----------------
scene(945.1, 973.7, 'To Argos', '', [
    L('P13-06', 947.0), ch('P03-04', 640, 948.0, h=520), ch('P08-07', 900, 948.5, h=520),
    card('B01-01', 1160, 200, 640, 400, c('argos', 952.5), rot=1.5, out=c('someone', 958.5)), lab('Argos', 1480, 680, c('argos', 952.5), out=c('someone', 958.5)),
    stk('a harmless visit', 960, 250, c('harmless', 948)),
    Rt('P13-08', c('someone', 958.5), out=973.7),
    stk('remembers the prophecy', 1590, 520, c('oracle', 961), rot=3),
    stk('alive, grown, monster-killer', 960, 360, c('alive', 966.5), rot=-2),
])
scene(973.7, 988.3, 'Argos', '', [
    Rt('P04-05', 973.79, face='R'), lab('Acrisius', 1590, 370, 974),
    stk('plan A: stop the birth', 860, 300, c('once', 977.5), rot=-2), xm(1120, 300, c('born', 980), s=34),
    stk('plan B: the sea', 860, 400, c('disposable', 983), rot=2), xm(1060, 400, c('disposable', 983.5), s=34),
    stk('plan C: leave town', 860, 500, c('leaving', 985)),
])
scene(988.3, 1016.9, 'Larissa', 'funeral games', [
    Rt('P13-09', 988.34, out=c('christie', 1000.6)), lab('King of Larissa', 1590, 370, 988.5, out=c('christie', 1000.6)),
    prop('E07-10', 960, 700, 380, 989),
    L('P01-11', c('pentathlon', 995), out=c('throw', 1010)), stk('the pentathlon', 330, 330, c('pentathlon', 995)),
    prop('E04-01', 960, 900, 120, c('discus', 999)),
    Rt('P13-08', c('christie', 1000.6), noPop=False, out=c('strikes', 1013)), lab('Acrisius', 1590, 370, c('christie', 1000.6), out=c('strikes', 1013)),
    stk('within range', 1590, 300, c('range', 1006)),
    L('P01-12', c('throw', 1010), noPop=True),
    prop('E04-02', 1180, 560, 120, c('throw', 1010.5), out=c('strikes', 1013)), fx('whoosh', c('throw', 1010.5)),
    Rt('P14-08', c('strikes', 1013), noPop=True), fx('stamp', c('strikes', 1013.4), 0.5),
])
scene(1016.9, 1036.9, 'Larissa', '', [
    stp('PROPHECY FULFILLED', 960, 300, 1016.94, size=56), fx('stamp', 1016.94),
    L('P02-10', c('perseus', 1020.8), out=c('buries', 1029)), stk('by accident', 330, 330, c('accident', 1024), out=c('buries', 1029)),
    L('P13-07', c('buries', 1029), noPop=True),
    stk('outside the city', 760, 420, c('outside', 1030)),
    stk('ashamed to take Argos', 1500, 450, c('ashamed', 1032), rot=3),
])
scene(1036.9, 1046.2, 'A trade', '', [
    L('P01-01', 1036.9), Rt('P09-11', c('exchange', 1037.5)), lab('Megapenthes', 1590, 370, c('mega', 1040)),
    stk('gets Argos', 1590, 290, c('mega', 1042)),
    card('B04-04', 660, 220, 600, 360, c('turin', 1044.3)), stk('Perseus takes Tiryns', 960, 700, c('turin', 1044.5), rot=2),
])
scene(1046.2, DUR, 'What came after', '', [
    C('P13-12', 1046.24, h=520, x=700, out=1068.3),
    stk('their granddaughter: Alcmene', 1420, 300, c('granddaughters', 1052.5)),
    arrow(1420, 340, 1420, 440, c('mother', 1054)),
    stk('her son: Heracles', 1420, 490, c('cleese', 1055), rot=2),
    prop('E01-01', 1420, 760, 180, c('chest', 1058)), stk('the baby in the chest', 1420, 640, c('chest', 1058.2), rot=-2),
    stk('the most famous strongman', 960, 230, c('famous', 1064)),
    paper(420, 840, 1080, 170, 1068.4),
    lab('died within', 470, 950, c('dies', 1071), size=60, cls='serif', italic=True, anchor='start'),
    hl(830, 930, 640, c('throwing', 1072), h=46),
    lab('THROWING DISTANCE', 850, 955, c('throwing', 1072), size=76, cls='anton', anchor='start'),
])

# make scenes contiguous and validate times
S.sort(key=lambda s: s['s'])
for i in range(len(S) - 1):
    S[i]['e'] = S[i + 1]['s']
S[-1]['e'] = DUR
for sc in S:
    for it in sc['items']:
        it['at'] = max(it['at'], sc['s'])
board = dict(version=1, title='Perseus and Medusa', duration=DUR, scenes=S)
json.dump(board, open('editor/storyboard.json', 'w'))
print(len(S), 'scenes', sum(len(s['items']) for s in S), 'items')
