"""Buffet explainer, v3: staged like the reference clips (01–05).
- One big waist-up ANCHOR character bottom-left (cropped by the frame), staying through the beat; a second
  character can enter bottom-right. They face each other (engine auto-flips by tagged facing).
- A small stacked header top-centre: subject / date / context.
- Content builds left-to-right next to the anchor like a sentence (element, arrow, element), each with a small
  hand-lettered label above. Auto-layout spaces the row evenly in the free area, so nothing overlaps.
- Things simply appear on their word (quick settle, no big pops); hard cuts between beats; occasional zoom punch.
- Numbers are plain hand-lettered text that counts up; archive photos / plates are feathered vignettes.
Timing: cue phrases are looked up in the forced-aligned script; visuals land LEAD seconds before the word."""
import json, re
TOK = json.load(open('script_words_fa.json'))
LIB = json.load(open('editor/library.json'))
DUR = 843.86
LEAD = 0.15
N = [t['n'] for t in TOK]
cur = 0

def norm(s): return [re.sub(r"[^a-z0-9]", "", w.lower().replace('’', "'")) for w in re.findall(r"[\w$€¢'’.,%\-]+", s)]

def T(phrase, back=40):
    """scene start: next occurrence of phrase after the previous scene start"""
    global cur
    p = [w for w in norm(phrase) if w]
    for i in range(max(0, cur - back), len(N) - len(p) + 1):
        if N[i:i + len(p)] == p:
            cur = i
            return round(max(0, TOK[i]['s'] - LEAD), 2)
    raise SystemExit(f'scene phrase not found: {phrase!r}')

def TA(phrase, near, end=False):
    p = [w for w in norm(phrase) if w]
    for i in range(len(N) - len(p) + 1):
        if N[i:i + len(p)] == p and TOK[i]['s'] >= near - 1.0:
            return round(max(0, (TOK[i + len(p) - 1]['e'] if end else TOK[i]['s']) - LEAD), 2)
    raise SystemExit(f'cue not found: {phrase!r} near {near}')

RED = '#D0362C'
AH, AY = 1000, 1370          # anchor: full-body height and feet line (feet below frame -> waist-up crop)

# ---------- element specs (cue = script phrase; resolved per scene) ----------
def A(a, cue=None, lab=None, x=300, **k):  return dict(kind='anchor', a=a, cue=cue, lab=lab, x=x, **k)
def B(a, cue=None, lab=None, x=1640, **k): return dict(kind='anchor', a=a, cue=cue, lab=lab, x=x, side='R', **k)
def E(a, cue=None, lab=None, h=240, **k):  return dict(kind='e', a=a, cue=cue, lab=lab, h=h, **k)
def Nm(to, cue=None, pre='', suf='', dec=0, cap='', size=110, frm=None, color=None, **k):
    return dict(kind='n', to=to, cue=cue, pre=pre, suf=suf, dec=dec, cap=cap, size=size, frm=frm, color=color, **k)
FALLBACK = {'A-ocb': 'B03-01', 'A-running_sushi': 'B01-03', 'A-vacant_ryans': 'B03-01', 'A-souplantation': 'B04-03',
            'A-vegas_buffet': 'B01-01', 'A-stardust': 'B03-03', 'A-gc_storefront': 'B04-03', 'A-gc_buffet': 'B01-02'}
def P(a, cue=None, cap=None, w=560, gray=False, **k):
    if a not in LIB: a, gray = FALLBACK[a], False      # archive photo not downloaded yet -> matching plate
    return dict(kind='p', a=a, cue=cue, cap=cap, w=w, gray=gray, **k)
def Tx(t, cue=None, size=46, cls='hand', color=None, w=None, **k): return dict(kind='t', t=t, cue=cue, size=size, cls=cls, color=color, w=w, **k)
def X(cue): return dict(kind='x', cue=cue)            # red X over the previous element
def O(cue): return dict(kind='o', cue=cue)            # red ink circle round the previous element
def ARW(): return dict(kind='arrow')                  # arrow between neighbours (appears with the next one)
def SFX(name, cue, vol=0.5): return dict(kind='sfx', a=name, cue=cue, vol=vol)
def BUB(t, cue, x, y, w, tx, ty, h=110, size=36, out=None): return dict(kind='bub', t=t, cue=cue, x=x, y=y, w=w, tx=tx, ty=ty, h=h, size=size, out=out)
def THK(t, cue, x, y, w, tx, ty, h=150, size=34, a=None): return dict(kind='think', t=t, cue=cue, x=x, y=y, w=w, tx=tx, ty=ty, h=h, size=size, a=a)
def RAW(d, cue=None): return dict(kind='raw', d=d, cue=cue)
def REEN(): return dict(kind='raw', d=dict(k='img', a='G06-01', x=1700, y=1040, h=64, center=1, still=1), cue=None)

def width_of(sp):
    k = sp['kind']
    if k == 'e': L = LIB[sp['a']]; return sp['h'] * L['w'] / L['h']
    if k == 'n': return max(len(f"{sp['pre']}{sp['to']:,}{sp['suf']}"), len(sp['cap']) * 0.55) * sp['size'] * 0.42 + 20
    if k == 'p': return sp['w']
    if k == 't': return sp['w'] or len(sp['t']) * sp['size'] * 0.42
    return 0
def height_of(sp):
    k = sp['kind']
    if k == 'e': return sp['h']
    if k == 'n': return sp['size'] * 1.3
    if k == 'p': L = LIB[sp['a']]; return sp['w'] * L['h'] / L['w']
    if k == 't': return sp['size']
    return 0

S = []
def scene(cue, head=('', '', ''), anchors=(), rows=(), extra=(), z=None, out_prev=False):
    s = T(cue) if isinstance(cue, str) else cue
    at = lambda c: s if c is None else (c if isinstance(c, (int, float)) else TA(c, s))
    items = []
    right = any(a.get('side') == 'R' for a in anchors)
    x0, x1 = (700, 1300) if right else (700, 1870)
    for a in anchors:
        L = LIB[a['a']]; ah = min(a.get('h', AH), 640 * L['h'] / L['w'])      # wide sprites (props in hand) get scaled down
        ax = a['x'] if ah * L['w'] / L['h'] < 600 else (330 if a['x'] < 960 else 1590)
        d = dict(k='img', a=a['a'], x=ax, y=a.get('y', round(AY - AH + ah)), h=round(ah), at=at(a['cue']))
        for kk in ('noPop', 'out', 'face', 'lab'):
            if a.get(kk) is not None: d[kk] = a[kk] if kk != 'out' else at(a[kk])
        if a.get('lab'): d['ls'] = 38
        if a.get('side') == 'R' and not a.get('noPop'): d['in'] = 'right'
        items.append(d)
    # ---------- v5 collage layout: elements join into one packed group; every arrival re-packs the group and
    # earlier elements glide/shrink to make room (reference R1 F1632/F1721/F2110, R2 F464). ----------
    rows = [r for r in rows if r]
    flat = [sp for r in rows for sp in r]
    has_bub = any(sp['kind'] in ('bub', 'think') for sp in extra)
    gx0 = 640; gx1 = 1300 if right else 1880
    gy0 = 150; gy1 = 1000 if any(sp['kind'] == 'raw' and sp['d'].get('a') == 'G06-01' for sp in extra) else 1050
    if has_bub:
        bb = max(sp['y'] + sp['h'] for sp in extra if sp['kind'] in ('bub', 'think'))
        if bb < 560: gy0 = bb + 30
    els = []; marks = []; arrows = []; pending = False
    for sp in flat:
        k = sp['kind']
        if k == 'arrow': pending = True; continue
        if k in ('x', 'o'):
            if els: marks.append((len(els) - 1, k, at(sp['cue'])))
            continue
        if k == 'sfx': items.append(dict(k='sfx', a=sp['a'], at=at(sp['cue']), vol=sp['vol'])); continue
        e = dict(sp=sp, t=at(sp['cue']), out=at(sp['out']) if sp.get('out') else None)
        if k == 'e':
            L = LIB[sp['a']]; ar = L['w'] / L['h']; ih = 300
            lab = 50 if sp.get('lab') else 0
            e.update(w=max(ih * ar, len(sp.get('lab') or '') * 21), h=ih + lab, oy=lab / 2, fmax=1.55, ih=ih)
        elif k == 'n':
            sz = 110; txt = f"{sp['pre']}{sp['to']:,.{sp['dec']}f}{sp['suf']}" if not (sp['frm'] is not None and sp['frm'] == sp['to']) else f"{sp['pre']}{sp['to']}{sp['suf']}"
            capw = len(sp['cap']) * 19 if sp['cap'] else 0
            e.update(w=max(len(txt) * sz * 0.52, capw) + 20, h=sz * (1.45 if sp['cap'] else 1.05), oy=sz * (0.42 if sp['cap'] else 0.3), fmax=1.5, sz=sz)
        elif k == 'p':
            L = LIB[sp['a']]; pw = 560; ph = pw * L['h'] / L['w']; cap = 46 if sp.get('cap') else 0
            e.update(w=pw, h=ph + cap, oy=cap / 2, fmax=1.45, pw=pw)
        else:
            sz = sp['size'] * 1.1
            e.update(w=len(sp['t']) * sz * 0.56 + 16, h=sz * 1.25, oy=sz * 0.3, fmax=1.4, sz=sz)
        if pending and els: arrows.append(len(els))
        pending = False
        els.append(e)
    # composition templates read off the reference state strips (R1 F65-F443, F1157-F1263, F1839-F2241; R2 F4673-F4991, F9941-F10170):
    # the first element is the hero (big, low-left of the free area); later elements are satellites placed around and partly over it,
    # at different heights and sizes. Each arrival switches to the template for the new count, so earlier elements glide/shrink to make room.
    TPL = {1: [(.50, .54, .92)],
           2: [(.37, .58, .82), (.80, .30, .50)],
           3: [(.34, .60, .76), (.79, .27, .46), (.83, .74, .44)],
           4: [(.31, .62, .70), (.70, .22, .42), (.88, .52, .38), (.64, .84, .34)],
           5: [(.28, .62, .64), (.60, .19, .36), (.87, .27, .36), (.70, .62, .36), (.92, .84, .28)],
           6: [(.26, .62, .60), (.56, .17, .32), (.83, .17, .32), (.62, .52, .32), (.89, .55, .32), (.76, .86, .28)],
           7: [(.25, .63, .56), (.54, .16, .30), (.79, .16, .30), (.58, .48, .30), (.85, .46, .30), (.62, .82, .28), (.90, .80, .28)]}
    CHAIN = {n: [(0.10 + 0.80 * k / max(1, n - 1), (.42 if k % 2 == 0 else .62) if n > 2 else .5, min(.62, 1.7 / (n + 0.6))) for k in range(n)] for n in range(1, 8)}
    chain = len(arrows) >= 1 and len(arrows) >= (len(els) - 1) / 2
    flip = len(S) % 2 == 1          # alternate satellites above/below the hero so consecutive scenes don't repeat
    # numbers/words in a second row that line up one-to-one with pictures above them are captions of those pictures
    if len(rows) == 2:
        r1 = [i for i, e in enumerate(els) if e['sp'] in rows[0]]; r2 = [i for i, e in enumerate(els) if e['sp'] in rows[1]]
        if len(r1) == len(r2) and all(els[i]['sp']['kind'] in ('n', 't') for i in r2) and any(els[i]['sp']['kind'] in ('e', 'p') for i in r1):
            for a_, b_ in zip(r1, r2): els[b_]['att'] = a_
    def pack(idx, prev=None):
        att = [i for i in idx if 'att' in els[i] and els[i]['att'] in idx]
        idx = [i for i in idx if i not in att]
        pics = [i for i in idx if els[i]['sp']['kind'] in ('p', 'e')]
        hero = ([i for i in pics if els[i]['sp']['kind'] == 'p'] or pics or idx)[:1]
        cmp_ = any('att' in e for e in els)
        if not chain and not cmp_: idx = hero + [i for i in idx if i not in hero]
        n = min(len(idx), 7); W = gx1 - gx0; H = gy1 - gy0
        slots = [(0.12 + 0.76 * k / max(1, n - 1) if n > 1 else .5, .42, min(.62, 1.6 / (n + 0.5))) for k in range(n)] if cmp_ else (CHAIN if chain else TPL)[n]
        out = {}
        for k, i in enumerate(idx[:7]):
            x, y, s = slots[k]
            if flip and not chain and n > 1: y = 1.0 - y if k > 0 else y
            e = els[i]; TH = s * H; TW = s * H * 1.35
            f = min(TH / e['h'], TW / e['w'], e['fmax'] * (1.3 if k == 0 else 1.0))
            cx = gx0 + x * W; cy = gy0 + y * H
            hw, hh = e['w'] * f / 2, e['h'] * f / 2
            cx = min(max(cx, gx0 - 60 + hw), 1900 - hw); cy = min(max(cy, 125 + hh), 1070 - hh)
            out[i] = (cx, cy, f)
        for i in att:
            if els[i]['att'] not in out: continue
            px, py, pf = out[els[i]['att']]; pe = els[els[i]['att']]; e = els[i]
            f = min(pe['h'] * pf * 0.34 / e['h'], pe['w'] * pf * 1.3 / e['w'], e['fmax'])
            cy = py + pe['h'] * pf / 2 + e['h'] * f / 2 + 6
            if cy + e['h'] * f / 2 > 1070:      # no room below: put it above the picture
                cy = py - pe['h'] * pf / 2 - e['h'] * f / 2 - 6
            out[i] = (px, cy, f)
        return out
    times = sorted(set(e['t'] for e in els) | set(e['out'] for e in els if e['out'] is not None))
    lay = []; last = None
    for t in times:
        idx = [i for i, e in enumerate(els) if e['t'] <= t and (e['out'] is None or e['out'] > t)]
        if idx: last = pack(idx, last); lay.append((t, last))
    def anchor(i, cx, cy, f): return (cx, cy + els[i]['oy'] * f)
    mvs = {}
    for i, e in enumerate(els):
        L0 = next(L for t, L in lay if t >= e['t'] and i in L); cx, cy, f0 = L0[i]
        ax, ay = anchor(i, cx, cy, f0); sp = e['sp']; k = sp['kind']
        if k == 'e':
            d = dict(k='img', a=sp['a'], x=round(ax), y=round(ay), h=round(e['ih'] * f0), center=1, still=1, at=e['t'])
            for kk in ('lab', 'rot', 'noPop'):
                if sp.get(kk) is not None: d[kk] = sp[kk]
            if sp.get('lab'): d['ls'] = round(38 * f0)
        elif k == 'n':
            sz = round(e['sz'] * f0); d = dict(k='counter', plain=True, to=sp['to'], pre=sp['pre'], suf=sp['suf'], dec=sp['dec'], cap=sp['cap'], size=sz, x=round(ax), y=round(ay), at=e['t'], rot=0)
            if sp['frm'] is not None: d['from'] = sp['frm']
            if sp['frm'] is not None and sp['frm'] == sp['to']: d['nosep'] = True
            if sp['color']: d['color'] = sp['color']
        elif k == 'p':
            d = dict(k='photo', a=sp['a'], x=round(ax), y=round(ay), w=round(e['pw'] * f0), at=e['t'], cs=round(34 * f0))
            if sp.get('cap'): d['cap'] = sp['cap']
            if sp.get('gray'): d['gray'] = True
        else:
            d = dict(k='text', t=sp['t'], x=round(ax), y=round(ay), size=round(e['sz'] * f0), cls=sp['cls'], at=e['t'])
            if sp.get('color'): d['color'] = sp['color']
        if e['out'] is not None: d['out'] = e['out']
        mv = []
        for t, L in lay:
            if t <= e['t'] or i not in L: continue
            cx, cy, f = L[i]; nx, ny = anchor(i, cx, cy, f)
            mv.append(f"{t},{round(nx - ax)},{round(ny - ay)},{round(f / f0, 3)}")
        if mv: d['mv'] = ';'.join(mv)
        mvs[i] = (ax, ay, f0); (items.insert(len([x for x in items if x['k'] == 'img' and x.get('h', 0) >= 700]), d) if k == 'p' else items.append(d))
    # attached red X / circle: follow their element through every re-pack
    for i, kind, t0 in marks:
        e = els[i]
        Ls = [(t, L) for t, L in lay if i in L]
        cur = [L for t, L in Ls if t <= t0]; L0 = cur[-1] if cur else Ls[0][1]
        cx, cy, f = L0[i]; w, h = e['w'] * f, e['h'] * f; icy = cy + e['oy'] * f
        if kind == 'x': d = dict(k='xmark', x=round(cx), y=round(icy), s=round(max(30, min(w, h - 2 * e['oy'] * f) * 0.32)), at=t0)
        else: d = dict(k='loop', x=round(cx), y=round(icy), rx=round(w * 0.62), ry=round(h * 0.62), color=RED, sw=7, at=t0)
        mv = []
        for t, L in Ls:
            if t <= t0: continue
            nx, ny, nf = L[i]; mv.append(f"{t},{round(nx - cx)},{round(ny + e['oy'] * nf - icy)},{round(nf / f, 3)}")
        if mv: d['mv'] = ';'.join(mv)
        items.append(d)
    # arrows between neighbours: redrawn (without re-animating) after every re-pack
    for j in arrows:
        i = j - 1; first = True
        for n_, (t, L) in enumerate(lay):
            if j not in L or i not in L: continue
            ax_, ay_, fa = L[i]; bx, by, fb = L[j]
            nxt = next((tt for tt, LL in lay[n_ + 1:]), None)
            pa = (ax_, ay_ + els[i]['oy'] * fa); pb = (bx, by + els[j]['oy'] * fb)
            def edge(c, o, w, hh):
                dx, dy = o[0] - c[0], o[1] - c[1]
                if dx == 0 and dy == 0: return c
                t_ = min(abs(w / 2 / dx) if dx else 9e9, abs(hh / 2 / dy) if dy else 9e9)
                return (c[0] + dx * min(t_, 0.95), c[1] + dy * min(t_, 0.95))
            s0 = edge(pa, pb, els[i]['w'] * fa * 0.95, (els[i]['h'] - 2 * els[i]['oy']) * fa * 0.95)
            s1 = edge(pb, pa, els[j]['w'] * fb * 0.95, (els[j]['h'] - 2 * els[j]['oy']) * fb * 0.95)
            if ((s1[0] - s0[0]) ** 2 + (s1[1] - s0[1]) ** 2) ** 0.5 < 50: continue
            d = dict(k='arrow', x=round(s0[0]), y=round(s0[1]), x2=round(s1[0]), y2=round(s1[1]), bend=-15, at=t)
            if not first: d['noPop'] = True
            if nxt is not None: d['out'] = nxt
            items.append(d); first = False
    for sp in extra:
        k = sp['kind']
        if k == 'raw': d = dict(sp['d']); d['at'] = d.get('at', at(sp['cue'])); items.append(d)
        elif k == 'bub':
            d = dict(k='bubble', t=sp['t'], x=sp['x'], y=sp['y'], w=sp['w'], h=sp['h'], tx=sp['tx'], ty=sp['ty'], size=max(38, sp['size']), at=at(sp['cue']))
            if sp['out']: d['out'] = at(sp['out'])
            items.append(d)
        elif k == 'think':
            d = dict(k='think', t=sp['t'], x=sp['x'], y=sp['y'], w=sp['w'], h=sp['h'], tx=sp['tx'], ty=sp['ty'], size=sp['size'], at=at(sp['cue']))
            if sp['a']: d['a'] = sp['a']; d['t'] = ''
            items.append(d)
        elif k == 'sfx': items.append(dict(k='sfx', a=sp['a'], at=at(sp['cue']), vol=sp['vol']))
    h = dict(a=head[0], b=head[1] if len(head) > 1 else '', c=head[2] if len(head) > 2 else '')
    sc = dict(id=f's{len(S)+1:03d}', s=s, e=0, h=h, items=items, tr='cut')
    if z: sc['z'] = ';'.join(f"{at(c)},{zs},{zx},{zy}" for c, zs, zx, zy in z)
    S.append(sc)

GC = ('Golden Corral', '2026')
# ============================ 1. A $17 steak dinner with no limit ============================
scene('From a triathlete', ('Running Sushi', 'Landshut, 2018'), [A('C03-01')],
      [[E('F03-05', 'hundred plates', 'about 100 plates', h=380), ARW(), E('G03-06', 'banned for eating', h=150)]],
      [REEN(), SFX('stamp', 'banned for eating')])
scene('to forty people', ('Golden Corral', 'Bensalem, 2022'), [A('C03-11')],
      [[P('B05-02', None, w=560), Nm(40, 'forty people', pre='~', cap='people', color='red')]], [REEN(), SFX('crash', 'brawling', 0.45)])
scene('this is how all-you-can-eat', ('All you can eat', '', ''), [A('C01-12')],
      [[E('F03-07', None, 'eat 5 plates', h=300), ARW(), E('P02-09', 'make money', 'how is that profitable?', h=220)]])
scene('At a lot of Golden Corrals', GC, [A('C02-01', lab='Gary')],
      [[P('B04-03', None, cap='Golden Corral', w=560), Nm(17, 'seventeen dollars gets', pre='$', cap='dinner', size=140)]],
      [SFX('ding', 'gets you dinner', 0.35)])
scene('Not a dinner', GC, [A('C02-01', noPop=True)],
      [[Tx('not "a" dinner…', None, size=48), Tx('ALL of it', 'All of it', size=64, color=RED)],
       [E('F01-01', 'Carved sirloin', 'carved sirloin', h=170), E('F01-03', 'fried chicken', 'fried chicken', h=150), E('F01-04', 'shrimp', 'shrimp', h=150),
        E('F01-05', 'mac and cheese', 'mac & cheese', h=150), E('F02-09', 'a dessert bar', 'dessert bar', h=110)]])
scene('a hundred and fifty other', GC, [A('C02-01', noPop=True)],
      [[Nm(150, None, pre='+', cap='other things', size=120), E('E01-11', 'keep walking back', 'keep walking back', h=200)]])
scene('Nobody counts your plates', ('Golden Corral', 'trip no. 5'), [A('C02-02', lab='Gary')],
      [[E('F03-08', None, 'plates', h=200), X('Nobody taps'), E('G06-02', 'trip number five', h=150)]], [SFX('ding', 'trip number five', 0.4)])
scene('That makes the next part strange', ('The biggest buffet chain', 'for years', ''), [A('C01-02')],
      [[E('P05-01', "wasn't Golden", 'Golden Corral', h=260), X('It was Old'), E('P05-02', 'It was Old Country', 'Old Country Buffet', h=280), O('at its peak')],
       [Nm(350, 'more than 350', suf='+', cap='restaurants at its peak', size=100)]])
scene('Its parent company went bankrupt', ('Old Country Buffet', '2008 – 2016', ''), [A('C01-08')],
      [[P('A-ocb', None, w=420), Nm(2008, '2008', frm=2008, cap='bankrupt', size=90), ARW(), Nm(2012, 'again in 2012', frm=2012, cap='again', size=90), ARW(), Nm(2016, 'then again in 2016', frm=2016, cap='again', size=90)]],
      [SFX('stamp', '2008', 0.4), SFX('stamp', 'again in 2012', 0.35), SFX('stamp', 'then again in 2016', 0.35)])
scene('By 2021', ('Old Country Buffet', '2021', ''), [A('C04-09', lab='auctioneer')],
      [[Nm(0, 'a single Old Country', cap='Old Country Buffets left', size=120, color='red'), E('P03-09', 'most of the furniture', 'sold at auction', h=300)]],
      [SFX('clang', 'sold at auction', 0.3)])
scene('So the obvious answer', ('The obvious answer', '', ''), [A('C01-11')], [],
      [THK('"most people don\'t eat that much"', None, 720, 260, 760, 520, 470, h=170, size=38),
       RAW(dict(k='xmark', x=1100, y=345, s=70), "can't be the whole"), RAW(dict(k='text', t="…can't be the whole story", x=1100, y=640, size=48, cls='hand'), "can't be the whole")])
scene('Both chains had', ('Same customers, same plates', '', ''), [A('C02-03', lab='customers')],
      [[E('P05-01', None, 'Golden Corral', h=240), E('F01-06', 'mashed potatoes', 'same mashed potatoes', h=170), E('P05-02', None, 'Old Country', h=250)],
       [E('E01-08', 'One is still opening', 'still opening restaurants', h=130), Tx(' ', None, size=10), E('E01-07', 'The other one is a memory', 'a memory', h=130)]])
scene('To work out why', ('The number not on the sign', '', ''), [A('C01-12')],
      [[Tx('what does it cost', "what it actually costs", size=60), Tx('to feed YOU?', 'to feed you', size=60, color=RED)]])

# ============================ 2. What does it cost to feed you? ============================
H2 = ('What does it cost to feed you?', 'per the Wall Street Journal', '')
scene('According to the Wall Street Journal', H2, [A('C02-05', lab='Golden Corral')],
      [[E('G01-02', 'of every dollar', h=150), ARW(), Nm(38, 'goes on food', suf='¢', cap='goes on food', size=140)]])
scene('On a seventeen-dollar dinner', H2, [A('C02-05', noPop=True)],
      [[Nm(17, None, pre='$', cap='dinner', size=120), ARW(), Nm(6.5, 'six dollars and fifty', pre='≈ $', dec=2, cap='of food per person', size=140)],
       [Tx("that's the budget", "That's the budget", size=48), Tx('…try everything twice', 'try everything twice', size=44)]])
scene('Of course nobody eats an average meal', ("The Hustle's model", 'a $20 buffet', 'hypothetical'), [A('C01-12')],
      [[E('C02-04', 'Someone who mostly', 'bread & potatoes', h=300), E('C02-03', 'The average eater', 'average', h=300), E('C02-01', 'the person who walked past', 'Gary', h=300)],
       [Nm(4.7, '$4.70', pre='$', dec=2, size=90), Nm(7.4, '$7.40', pre='$', dec=2, size=90), Nm(16.9, '$16.90', pre='$', dec=2, size=90, color='red')]])
scene('In that model only about one diner', ('1 in 20 diners', 'eats like Gary', ''), [A('C02-01', lab='Gary')],
      [], [RAW(dict(k='icons', x=1290, y=440, n=20, cols=10, sz=78, gap=18, hi='19', hiAt=0)),
           RAW(dict(k='loop', x=1700, y=562, rx=62, ry=70, color=RED, sw=7), 'eats like Gary'),
           RAW(dict(k='text', t='the other 19 quietly cover him', x=1290, y=780, size=48, cls='hand'), 'the other nineteen')])
scene('But every now and then', ('Gary', '…on a diet?', ''), [A('C02-01', noPop=True), B('C03-01', 'who makes Gary')], [],
      [BUB('"…he makes ME look like I\'m on a diet"', 'look like', 560, 170, 760, 420, 380, h=120, size=32), REEN()])
H3 = ('Jaroslav Bobrowski', 'September 2018', 'triathlete, 30')
scene('In September 2018', H3, [A('C03-01')],
      [[P('B02-01', 'walked into a restaurant', cap='Running Sushi', w=560), E('P05-12', 'Landshut', 'Landshut, Bavaria', h=230)]], [REEN()])
scene('It was all-you-can-eat for', H3, [A('C03-01', noPop=True)],
      [[Nm(15.9, '€15.90', pre='€', dec=2, cap='all you can eat', size=120), Tx('≈ $18.50', 'eighteen and a half', size=46)],
       [E('P04-06', "doesn't eat for 20", 'fasts ~20 hours', h=220), ARW(), E('F03-06', "eats until he's full", 'then eats until full', h=200)]], [REEN()])
scene('That evening', ('Jaroslav Bobrowski', 'that evening', ''), [A('C01-03', lab='counting…')],
      [[E('F03-05', 'turned out to be', '', h=520), Nm(100, 'one hundred plates', pre='~', cap='plates of sushi', size=150, dur=1.6)]], [SFX('ding', 'of sushi', 0.4)])
scene("He wasn't taking one plate", ('Jaroslav Bobrowski', '5–7 plates at a time', ''), [A('C03-02'), B('C03-07', 'other customers asked')],
      [[E('G03-05', 'five or seven', h=120)], [E('P01-08', 'leaving such big gaps', 'gaps on the belt', h=220)]],
      [BUB('"skimping on fish?"', 'skimping on fish', 1190, 230, 380, 1480, 420, h=100, size=34), REEN()])
scene('So when Bobrowski went to pay', ('Jaroslav Bobrowski', 'banned', ''), [A('C03-04'), B('C03-05', 'the waiter refused', out='the owner told him'), B('C03-06', 'the owner told him', noPop=True)],
      [[E('G03-06', 'banned for good', h=150)], [Tx('"he ate for five people"', 'he ate for five', size=42)]], [SFX('stamp', 'banned for good'), REEN()])
H4 = ('Bill Wisth', "Chuck's Place, 2012", "6'6\", 350 lb")
scene("And Bobrowski isn't the only one", H4, [A('C03-08')],
      [[P('B01-04', 'fish fry at', cap="Chuck's Place", w=560), E('P05-12', 'Thiensville', 'Thiensville, Wisconsin', h=220)]], [REEN()])
scene('After twelve pieces of fish', H4, [A('C03-08', noPop=True), B('C03-10', 'cut him off')],
      [[E('F01-11', None, '', h=170), X('cut him off')], [Nm(12, 'twelve pieces', cap='pieces', size=110)]], [SFX('stamp', 'cut him off', 0.4), REEN()])
scene('So two days later', ('Bill Wisth', 'two days later', ''), [A('C03-09')],
      [[E('G06-03', 'picket sign', h=140), Tx('"false advertising"', 'false advertising', size=48, color=RED)],
       [E('P04-07', 'every Sunday', 'every Sunday', h=230), Tx('"all HE could eat"', 'all he could eat', size=44)]], [REEN()])
scene('Both stories show', ('Both stories', '', ''), [A('C01-12')],
      [[E('C03-01', None, 'Bobrowski', h=280), E('C03-08', None, 'Bill Wisth', h=280)], [Tx('one extreme eater = a real cost', 'one extreme eater', size=50)]])
scene('Notice who paid', ('Who actually paid?', '', ''), [A('C03-07')],
      [[Tx('not the sushi bill', "wasn't the sushi bill", size=46), P('B05-01', 'the other customers', cap='the other customers', w=520)]])
H5 = ("The Hustle's model", 'a $20 buffet', '')
scene('To be fair', H5, [A('C02-08', lab='manager')],
      [[E('G02-05', 'staff', h=110), E('G02-06', 'rent', h=110), E('G02-07', 'electricity', h=110)],
       [Nm(1, 'one dollar of profit', pre='≈ $', cap='profit per customer', size=110, color='green'), Nm(5, 'five percent', suf='%', cap='margin', size=110, color='green')]])
scene("So buffets can't just hope", ("Buffets don't hope", '', ''), [A('C01-06')],
      [[Tx('they make sure of it', 'They make sure', size=64, color=RED)], [E('F03-09', 'picked up a plate', 'before your first plate', h=120)]])

# ============================ 3. Why are the rolls always first? ============================
H6 = ('Why are the rolls always first?', '', '')
scene('Walk into almost any buffet', H6, [A('C02-01', lab='Gary')],
      [[P('B01-02', None, cap='the start of the line', w=560)],
       [E('F01-07', 'salad', 'salad', h=140), ARW(), E('F01-08', 'bread rolls', 'rolls', h=140), ARW(), E('F01-06', 'potatoes something', 'potatoes', h=140), ARW(), E('F01-03', 'something fried', 'fried', h=140)]])
scene('The expensive meat is usually', H6, [A('C02-01', noPop=True), B('C02-06', 'served by a person')],
      [[E('F01-01', None, 'further in…', h=230)], [Tx('a "specific idea" of a portion', 'fairly specific idea', size=40)]])
scene("That layout isn't an accident", ('Buffet line studies', 'one well-known study', ''), [A('C01-05')],
      [[E('P01-01', None, 'first tray', h=260)], [E('G02-11', 'three-quarters', h=130), E('G02-12', 'two-thirds', h=130)]])
scene('By the time you reach the steak', ('Potato vs. steak', 'per serving', ''), [A('C02-04', lab='your plate')],
      [[E('F02-02', 'by a potato', 'potato', h=200), E('F01-02', 'The steak by comparison', 'steak', h=170)],
       [Nm(30, 'thirty cents', pre='≈ ', suf='¢', size=110, color='green'), Nm(2.25, '$2.25', pre='≈ $', dec=2, size=110, color='red')]])
scene('Golden Corral goes a step further', ('Golden Corral', '"modules"', ''), [A('C02-05', lab='Golden Corral')],
      [[E('F02-10', 'The meat and seafood', 'seafood + hush puppies + fries', h=210), E('F02-11', 'The meatloaf comes', 'meatloaf + potatoes + gravy', h=210)],
       [Tx('expensive + cheap, on purpose', 'pair expensive', size=46)]])
scene("You didn't choose that side dish", ('Golden Corral', '"modules"', ''), [A('C01-05')], [],
      [THK("chosen for you… in a spreadsheet meeting", 'It was chosen', 700, 250, 800, 520, 470, h=170, size=38)])
scene('Then there are the small details', ('The small details', '', ''), [A('C02-03')],
      [[E('P01-04', 'bigger serving spoons', 'BIG potato spoon', h=220), E('P01-05', 'smaller tongs', 'small meat tongs', h=150)],
       [E('F03-09', 'The plates are smaller', 'small plates', h=100), E('P02-03', 'water glasses', 'BIG water glass', h=230)]])
scene('None of this stops you', ('The small details', '', ''), [A('C02-03', noPop=True)],
      [[E('F01-02', None, 'you can still eat steak…', h=180)], [Tx('…it just takes a little more effort', 'a little more effort', size=46)]])
scene('And when steak is the one thing', ('Steak', 'rationed by design', ''), [A('C02-06')],
      [[E('F01-01', None, 'the one rationed thing', h=280)], [Tx('people notice when it runs low', 'runs low', size=48)]])
H7 = ('Golden Corral, Bensalem PA', 'January 29, 2022', '')
scene('On January 29th', H7, [A('C03-11')],
      [[E('P05-12', 'Bensalem Pennsylvania', 'Bensalem, Pennsylvania', h=220), E('F01-01', 'the line for steak', 'the steak line', h=200)],
       [Tx('cut in line?', 'someone cut in line', size=42), Tx('running out?', 'running out', size=42), Tx('both?', 'or both', size=42)]], [REEN()])
scene('Either way', H7, [A('C03-12')],
      [[P('B05-02', 'Within minutes', cap='within minutes', w=520), Nm(40, 'around forty people', pre='~', cap='people fighting', size=130, color='red')]],
      [SFX('crash', 'fighting', 0.5), REEN()])
scene('The video which went viral', H7, [A('C03-12', noPop=True)],
      [[E('P03-03', 'chairs flying', 'chairs flying', h=170, rot=-12), E('P03-04', 'tables flipping', 'tables flipping', h=210, rot=8), E('P03-05', 'high chairs', 'HIGH chairs', h=170, rot=-6)],
       [E('E01-09', 'An employee was hit', 'an employee was hit by a table', h=150)]], [SFX('crash', 'chairs flying', 0.45), REEN()])
scene('And as things finally calmed down', H7, [A('C03-11')],
      [[Tx(' ', None, size=10)], [E('E01-08', 'no serious injuries', 'no serious injuries reported', h=170)]],
      [BUB('"All I wanted was some steak."', 'All I wanted', 620, 220, 760, 470, 400, h=120, size=38), REEN()])
scene("But it's probably the clearest proof", ('The most valuable thing', 'in a buffet', ''), [A('C01-07')],
      [[E('P02-12', "isn't on the menu", 'not on the menu', h=220), X("isn't on the menu"), E('P01-03', 'queue for the carving', 'the queue for steak', h=260)]])
scene("That's also why when beef prices", ('Golden Corral', 'the pork chop', ''), [A('C02-05')],
      [[E('F01-01', 'beef prices went up', 'beef prices ↑', h=170), ARW(), E('F01-09', 'bone-in fried pork chop', 'bone-in pork chop', h=200)],
       [Nm(40, '40 percent', pre='≈ ', suf='%', cap="of the sirloin's cost", size=110), E('E01-06', 'got a treat', 'still feels like a treat', h=130)]])
scene('You can see the result', ('Old Country Buffet', 'per The Atlantic', 'pounds served a year'), [A('C02-08')],
      [], [RAW(dict(k='bars', rows='Chicken|47|47M lb|y;Steak|6|6M lb|r', x=720, y=420, w=1050, rh=90, lw=210, title=''), '47 million'),
           RAW(dict(k='counter', plain=True, to=8, pre='~', suf=' : 1', cap='chicken to steak', size=120, x=1250, y=820, rot=0), 'nearly eight pounds')])
scene('So the food is cheap', ('So far…', '', ''), [A('C02-01', lab='Gary')],
      [[E('F01-06', None, 'cheap food', h=170), E('F01-02', 'steak is surrounded', 'steak, surrounded by potatoes', h=150)],
       [E('G06-04', 'getting through the door', h=150)]], [SFX('ching', 'getting through the door', 0.4)])

# ============================ 4. Would you like a drink with that? ============================
H8 = ('Would you like a drink with that?', '', '')
scene('At most Golden Corrals', H8, [A('C02-07', lab='server')],
      [[E('P02-01', 'A soda', 'soda', h=250), E('P02-02', 'iced tea', 'iced tea', h=220)], [E('G04-05', 'two and a half', h=130)]])
scene('And fountain soda is one of the best', ('Fountain soda', 'best deal in the restaurant', ''), [A('C02-07', noPop=True)],
      [[E('P02-04', None, 'fountain soda', h=250)],
       [Nm(12, 'twelve cents', pre='≈ ', suf='¢', cap='to fill', size=100, color='green'), ARW(), Nm(2, 'two dollars', pre='$', suf='+', cap='price', size=100), Nm(1000, 'one thousand percent', suf='%+', cap='markup', size=100, color='red', dur=1.4)]],
      [SFX('ching', 'one thousand percent', 0.45)])
scene('On a seventeen-dollar dinner that contains', ('Your $17 dinner', '', ''), [A('C01-12')],
      [[Nm(6.5, None, pre='$', dec=2, cap='food', size=110), Tx('+', 'the drink is almost', size=90), E('P02-01', 'the drink is almost', 'almost pure profit', h=240)],
       [Tx("…bought before you've seen a tray", "before you've seen", size=44)]])
scene("Then there's the kids' deal", ("The kids' deal", 'Fri – Sun', ''), [A('C02-10', lab='age 7')],
      [[E('P04-07', 'Fridays Saturdays', 'Fri · Sat · Sun', h=210), Nm(2.5, '$2.50 with each', pre='$', dec=2, cap='per kid (up to 12)', size=120)],
       [Tx('a terrible deal?', 'a terrible deal', size=46), Tx('not a threat to the sirloin', 'not a serious threat', size=42)]])
scene('And a $2.50 child never arrives alone', ("The kids' deal", '', ''), [A('C02-09')],
      [[Tx('never arrives alone', 'never arrives alone', size=48)], [Nm(17, 'at least one adult', pre='$', cap='adult, full price', size=110), E('P02-01', 'a couple of drinks', '+ drinks', h=200)]])
scene('So by now the seventeen-dollar buffet', ('The running tally', '', ''), [A('C02-12')],
      [], [RAW(dict(k='img', a='G07-01', x=1150, y=520, h=480, center=1, still=1), None),
           RAW(dict(k='img', a='G07-02', x=1150, y=520, h=480, center=1, still=1, noPop=True), 'a drink a second'),
           RAW(dict(k='img', a='G07-04', x=1150, y=520, h=480, center=1, still=1, noPop=True), 'second adult'),
           RAW(dict(k='img', a='G07-05', x=1150, y=520, h=480, center=1, still=1, noPop=True), 'a child who ate'),
           RAW(dict(k='img', a='F02-07', x=1660, y=420, h=150, center=1, still=1, lab='4 nuggets', ls=30), 'four chicken nuggets'),
           RAW(dict(k='img', a='F02-08', x=1660, y=720, h=170, center=1, still=1, lab='a pudding cup', ls=30), 'a pudding cup'),
           SFX('ching', 'a pudding cup', 0.45)])
scene('Which brings us back', ('The real question', '', ''), [A('C01-02')], [],
      [THK('…so why did the others go broke?', 'why did so many', 700, 250, 800, 520, 470, h=170, size=40)])

# ============================ 5. Why did the other buffets go bankrupt? ============================
H9 = ('Why did the other buffets go bankrupt?', '', '')
scene("Here's the part that surprises", H9, [A('C02-01', lab='Gary'), B('C03-01', "it wasn't triathletes", lab='Bobrowski')], [],
      [RAW(dict(k='xmark', x=330, y=520, s=80), "it wasn't Gary"), RAW(dict(k='xmark', x=1610, y=520, s=80), 'triathletes either'),
       RAW(dict(k='text', t='it wasn\'t the big eaters', x=960, y=420, size=50, cls='hand'), "it wasn't Gary")])
H10 = ('Old Country Buffet', '2006', '')
scene("Old Country Buffet's parent company", H10, [A('C04-12')],
      [[E('P05-02', None, 'Old Country Buffet', h=230), ARW(), E('P05-03', "bought Ryan's", "Ryan's", h=200)],
       [Nm(2006, 'in 2006', frm=2006, cap='bought', size=100), Tx('…with borrowed money', 'borrowed heavily', size=46, color=RED)]])
scene('That debt led to', ('Old Country Buffet', 'bankruptcies', ''), [A('C04-12', noPop=True)],
      [[Nm(2008, 'first bankruptcy in 2008', frm=2008, cap='bankrupt', size=100), ARW(), Nm(2012, 'again in 2012', frm=2012, cap='again', size=100), ARW(), Nm(2016, 'and again in 2016', frm=2016, cap='again', size=100)]],
      [SFX('stamp', 'first bankruptcy in 2008', 0.4), SFX('stamp', 'again in 2012', 0.35), SFX('stamp', 'and again in 2016', 0.35)])
scene('In early 2016', ('Old Country Buffet', 'early 2016', ''), [A('C04-10')],
      [[Nm(74, '74 restaurants', cap='closed at once', size=110, color='red'), Nm(92, '92 more', pre='+', cap='a month later', size=110, color='red')],
       [E('P03-11', 'without warning', 'often without warning staff', h=200)]], [SFX('stamp', 'in one go', 0.35)])
scene('That same year', ('Souplantation & Sweet Tomatoes', '2016', ''), [A('C01-08')],
      [[E('G05-06', 'Souplantation', h=100), E('G05-07', 'Sweet Tomatoes', h=100)], [Nm(175, '$175 million', pre='$', suf='M', cap='of debt', size=130, color='red')]])
scene('Debt is especially dangerous', ('Cook first, hope later', '', ''), [A('C04-05', lab='normal restaurant'), B('C04-06', 'A buffet cooks first', lab='buffet')],
      [[Tx('cooks AFTER you order', 'after you order', size=40)], [Tx('cooks FIRST, then hopes', 'hopes people turn up', size=40, color=RED)]])
scene('If the dining room is half empty', ('7 p.m.', 'half empty', ''), [A('C04-10')],
      [[P('B02-04', None, cap='7 p.m., half empty', w=560), E('P04-06', "at seven o'clock", '', h=200)],
       [E('F01-12', 'the turkey still', 'still carved', h=180), E('F03-12', 'trays still have', 'trays still full', h=130)]])
scene('Somewhere between 5 and 25', ('Waste', '', ''), [A('C04-07')],
      [[Nm(25, None, frm=5, pre='5–', suf='%', cap='of a dish can be binned', size=110, color='red'), E('P03-08', 'end up in the bin', 'the bin', h=240)],
       [E('P03-02', 'empty chairs', 'the real loss: empty chairs', h=210)]], [SFX('stamp', 'empty chairs', 0.35)])
scene('Then in 2020', ('2020', 'pandemic', ''), [A('C04-11')],
      [[E('P03-12', 'sharing serving tongs', 'shared tongs', h=200), X('least appealing')], [Tx("what was left didn't make it", "didn't make it", size=46)]])
scene('By early 2021', ('By early 2021', '', ''), [A('C04-12')],
      [[E('G05-02', 'every Old Country', h=90), E('G05-05', 'HomeTown Buffet', h=90), E('G05-04', "and Ryan's", h=90)], [E('G05-11', 'had closed', h=150)]],
      [SFX('stamp', 'had closed', 0.45)])
scene('The odd thing is', ('The odd thing', '', ''), [A('C01-11')], [],
      [THK('the most famous buffets never even TRIED to make money', 'the most famous', 680, 230, 880, 520, 470, h=190, size=38)])

# ============================ 6. Why did Las Vegas give up on buffets? ============================
H11 = ('Las Vegas', 'for decades', '')
scene('For decades the Las Vegas buffet', H11, [A('C04-01', lab='casino executive')],
      [[P('B03-02', None, cap='Las Vegas Strip', w=560), E('G08-01', 'loss leaders', h=150)]], [SFX('ding', 'loss leaders', 0.35)])
scene('Back in the 1980s', ('Las Vegas', '1980s', ''), [A('C04-01', noPop=True)],
      [[P('B03-03', None, cap='casino floor', w=520), Nm(75, 'three-quarters', pre='≈ ', suf='%', cap='of revenue: gambling', size=120)]])
scene('so a cheap all-you-can-eat dinner', ('Las Vegas', '1980s', ''), [A('C04-02', lab='diner')],
      [[E('F02-12', None, 'cheap dinner', h=180), ARW(), E('P05-10', 'through the door', 'in the door', h=200), ARW(), E('P04-05', 'back to the tables', 'back to the tables', h=170)]])
scene('That works as long as', ('Las Vegas', 'today', ''), [A('C04-03'), B('C04-02', 'a giant room losing')],
      [[Tx("don't gamble much", "don't gamble much", size=44)], [Tx('happy to pay full price for food', 'happy to pay full price', size=40)]],
      [RAW(dict(k='xmark', x=480, y=600, s=60), "don't gamble much")])
scene('Around the year 2000', ('Las Vegas Strip buffets', '', ''), [A('C01-12')], [],
      [RAW(dict(k='bars', rows='Around 2000|35|~35|y;Today|7|~7|r', x=720, y=430, w=1080, rh=100, lw=260, title=''), None),
       SFX('ding', 'about seven', 0.35)])
scene('A lot of that space became', ('Food halls', '', ''), [A('C04-04')],
      [[P('B03-04', None, cap='food hall', w=560), E('P02-07', 'every single thing', 'pay for every single thing', h=230)],
       [Tx('the exact opposite of a buffet', 'exact opposite', size=46)]])
scene('Vegas buffets were built', ('Golden Corral', 'no casino', ''), [A('C01-09')],
      [[E('P04-02', "Golden Corral doesn't", 'no casino money', h=200), X('quietly paying'), E('F01-04', 'for the shrimp', 'the shrimp', h=170)],
       [Tx('the food has to pay for itself', 'pay for itself', size=50)]])

# ============================ 7. So how does $17 make money? ============================
H12 = ('So how does $17 make money?', '', '')
scene('So how does it manage that', H12, [A('C01-12')],
      [[Tx('mostly:', 'The answer is mostly', size=50), Tx('SCALE', 'scale', size=140, cls='anton', color=RED)]], [SFX('stamp', 'scale', 0.35)])
scene('A typical Golden Corral serves', ('Golden Corral', 'scale', ''), [A('C02-08', lab='manager')],
      [[P('A-gc_storefront', None, cap='a typical Golden Corral', w=440), Nm(6500, 'six to six', pre='~', cap='customers a week', size=110)],
       [Nm(7.5, '$7.5', pre='$', suf='M', dec=1, cap='a year (best new ones)', size=100), Nm(12, '$12 million', pre='$', suf='M', cap='Puerto Rico', size=100)]],
      [SFX('ching', 'first new location', 0.4)])
scene('This is exactly what Running Sushi', ('A rounding error', '', ''), [A('C03-02')],
      [[E('P05-06', None, 'Running Sushi', h=210), E('P05-05', "Chuck's Place", "Chuck's Place", h=190)],
       [Tx('a few hundred a night', 'a few hundred', size=40), Nm(6000, 'six thousand a week', cap='a week = rounding error', size=100)]])
scene('That volume changes the kitchen too', ('The kitchen', 'customers per hour', ''), [A('C04-05'), B('C04-06', 'A buffet cook')], [],
      [RAW(dict(k='bars', rows='To order|25|~25|b;Batch|200|~200|y', x=640, y=430, w=620, rh=80, lw=150, title=''), 'might manage about'),
       RAW(dict(k='text', t='a tiny share of a VERY big batch', x=960, y=800, size=40, cls='hand'), 'a tiny share')])
scene('Golden Corral also forecasts', ('Golden Corral', 'forecasting', ''), [A('C04-08')],
      [[E('G08-09', 'fifteen-minute', h=130), E('P04-09', 'fifteen-minute', '', h=200)],
       [E('P01-07', 'under heat lamps', 'no big batches under heat lamps', h=200), X('the waste problem'), E('F01-01', 'running out of steak', 'no running out on Saturday', h=150)]])
scene('And it counts on loyalty', ('Loyalty', '', ''), [A('C02-11')],
      [[Nm(70, '70 times a year', pre='~', cap='visits a year', size=120), E('P02-11', 'more than once a week', 'more than once a week', h=170)],
       [E('P01-12', 'second kitchen', 'a second kitchen', h=220)]])
scene('To be fair none of this', ('Not a money printer', 'end of 2025', ''), [A('C04-12')],
      [[Nm(348, '348 restaurants', cap='Golden Corrals', size=110), E('G08-12', 'three fewer', h=130)],
       [Tx('CEO: "We are trying to at least tread water."', 'We are trying', size=40)]])
scene("So seventeen dollars isn't really", ("It's a bet", '', ''), [A('C01-12')],
      [[Nm(17, None, pre='$', cap="isn't the price of the food", size=120), Tx("it's a BET", "It's a bet", size=70, color=RED)],
       [E('F02-01', 'start with the rolls', 'rolls', h=120), E('F02-11', 'the meatloaf will bring', 'meatloaf + potatoes', h=110), E('P02-01', "you'll order a drink", 'a drink', h=150),
        E('C02-10', 'bring a kid', 'a kid', h=170), E('P04-07', 'come back next Thursday', 'next Thursday', h=130)]], [SFX('stamp', "It's a bet", 0.35)])
scene('Yes Gary is still allowed', ("…and that's fine", '', ''), [A('C02-01', lab='Gary'), B('C03-01', 'Bobrowski is still welcome', lab='Bobrowski')],
      [[E('F02-01', 'skip the bread', '', h=110), X('ignore the soda'), E('P02-01', 'ignore the soda', '', h=140)],
       [E('F01-06', 'the other nineteen of us', 'really, really like potatoes', h=190)]])
scene('This channel is brand new', ('Thanks for watching', '', ''), [A('C01-10')],
      [[E('G05-10', 'a subscribe', h=150)], [P('B05-04', 'Next time', cap='next: movie theaters', w=480)]], [SFX('ding', 'a subscribe', 0.35)])

# ---------- finalise ----------
S.sort(key=lambda s: s['s'])
for i in range(len(S) - 1): S[i]['e'] = S[i + 1]['s']
S[-1]['e'] = DUR
for sc in S:
    for it in sc['items']:
        it['at'] = round(min(max(it['at'], sc['s']), sc['e'] - 0.3), 2)
        if it.get('out') is not None and it['out'] <= it['at']: it['out'] = round(it['at'] + 0.5, 2)
    vis = [it for it in sc['items'] if it['k'] != 'sfx' and it.get('a') != 'G06-01']
    if vis and min(it['at'] for it in vis) - sc['s'] > 0.3:        # never open on an empty frame
        f = min(it['at'] for it in vis)
        for it in vis:
            if abs(it['at'] - f) < 0.05: it['at'] = sc['s']

# ======================= v4: reference-analysis pass (Explainer_Motion_and_Style_Guide.md) =======================
import random
random.seed(7)
# T1 chapter index -> title card: 6f hold + 14f zoom + ~1.4 s card, starting 1.0 s before the chapter's first scene
TILES = [dict(bg='B02-02', t='A $17 dinner, no limit'), dict(bg='B01-01', t='What does it cost?'), dict(bg='B01-02', t='Why rolls first?'),
         dict(bg='B02-03', t='A drink with that?'), dict(bg='B03-01', t='Why others went broke'), dict(bg='B03-02', t='Why Vegas gave up'),
         dict(bg='B04-01', t='How $17 makes money')]
CH_START = ['From a triathlete', 'According to the Wall Street Journal', 'Walk into almost any buffet', 'At most Golden Corrals',
            "Here's the part that surprises", 'For decades the Las Vegas buffet', 'So how does it manage that']
def first_word_time(ph):
    p = [w for w in norm(ph) if w]
    for i in range(len(N) - len(p) + 1):
        if N[i:i + len(p)] == p: return TOK[i]['s']
    raise SystemExit(ph)
for k, ph in enumerate(CH_START):
    t = round(max(0, first_word_time(ph) - LEAD), 2)
    sc = min(S, key=lambda s: abs(s['s'] - t))
    i0 = max(0.0, sc['s'] - (0.0 if k == 0 else 1.0)); i1 = round(i0 + 2.1, 2)
    # trim the previous scene, push this chapter's first scene start (and its early items) to i1
    for s in S:
        if s is not sc and s['s'] < i0 < s['e']: s['e'] = i0
    sc['s'] = i1
    for it in sc['items']: it['at'] = round(max(it['at'], i1), 2)
    S.append(dict(id=f'idx{k+1}', s=round(i0, 2), e=i1, h=dict(a='', b='', c=''), items=[], tr='cut', index=dict(tiles=TILES, sel=k, cols=4)))
S.sort(key=lambda s: s['s'])
for i in range(len(S) - 1): S[i]['e'] = S[i + 1]['s']
S[-1]['e'] = DUR
# pose families (replacement drawings of the same character, same footprint)
FAM = {'C01': ['C01-12', 'C01-06', 'C01-11', 'C01-05', 'C01-02', 'C01-09', 'C01-01'], 'C02-01': ['C02-01', 'C02-02'], 'C02-02': ['C02-02', 'C02-01'],
       'C03-01': ['C03-01', 'C03-04'], 'C03-02': ['C03-02', 'C03-01'], 'C03-04': ['C03-04', 'C03-01'],
       'C03-08': ['C03-08', 'C03-09'], 'C03-09': ['C03-09', 'C03-08'], 'C02-05': ['C02-05', 'C02-06'], 'C02-06': ['C02-06', 'C02-05']}
def family(a): return FAM.get(a) or (FAM['C01'] if a.startswith('C01') else None)
swaps = zooms = 0
for sc in S:
    if sc.get('index'): continue
    for _ in range(6):
        ts = sorted(set([sc['s']] + [it['at'] for it in sc['items'] if it['k'] != 'sfx'] + [sc['e']]))
        gaps = [(b - a, a, b) for a, b in zip(ts, ts[1:]) if b - a > 3.0]
        if not gaps: break
        g, a, b = max(gaps); t = round(a + g / 2, 2)
        anc = [it for it in sc['items'] if it['k'] == 'img' and it.get('h', 0) >= 700 and it['at'] <= t and (it.get('out') is None or it['out'] > t)]
        fam = family(anc[-1]['a']) if anc else None
        if anc and fam and len(fam) > 1:
            cur = anc[-1]; choices = [x for x in fam if x != cur['a']]; nxt = random.choice(choices)
            old_out = cur.get('out'); cur['out'] = t
            new = {k2: v for k2, v in cur.items() if k2 not in ('out', 'at', 'a', 'in')}; new.update(a=nxt, at=t, noPop=True)
            if old_out is not None: new['out'] = old_out
            if 'lab' in cur: new['lab'] = cur['lab']
            sc['items'].append(new); swaps += 1
        else:
            # red ink circle round the key element on screen (reference accent), only if that element no longer moves
            def last_mv(it): return max([float(m.split(',')[0]) for m in str(it.get('mv', '')).split(';') if m] or [0])
            cand = [it for it in sc['items'] if it['k'] in ('img', 'counter', 'photo') and it.get('h', 0) < 700 and it['at'] <= t
                    and (it.get('out') is None or it['out'] > t) and last_mv(it) <= t and not it.get('a', '').startswith('G06-01')]
            if not cand or any(it['k'] == 'loop' and abs(it['at'] - t) < 3 for it in sc['items']): break
            it = max(cand, key=lambda q: q['at'])
            ms = [m.split(',') for m in str(it.get('mv', '')).split(';') if m]
            dx, dy, sc_ = (float(ms[-1][1]), float(ms[-1][2]), float(ms[-1][3])) if ms else (0, 0, 1)
            if it['k'] == 'img': r_ = it['h'] * sc_ * 0.62
            elif it['k'] == 'counter': r_ = it['size'] * sc_ * 0.9
            else: r_ = it['w'] * sc_ * 0.36
            cy_ = it['y'] + dy - (it['size'] * sc_ * 0.35 if it['k'] == 'counter' else 0)
            sc['items'].append(dict(k='loop', x=round(it['x'] + dx), y=round(cy_), rx=round(r_ * 1.15), ry=round(r_), color=RED, sw=7, at=t))
# sound: references have no picture-synced SFX -> keep at most one signature hit per chapter
starts = sorted(s['s'] for s in S if s.get('index'))
kept = set()
for sc in S:
    ch = sum(1 for x in starts if x <= sc['s'])
    keep = []
    for it in sc['items']:
        if it['k'] != 'sfx': keep.append(it); continue
        if ch not in kept and it['a'] in ('ching', 'crash', 'stamp'):
            it['vol'] = 0.35; keep.append(it); kept.add(ch)
    sc['items'] = keep
print('v4: index cards', len(starts), 'pose swaps', swaps, 'zoom punches', zooms, 'sfx kept', len(kept))

board = dict(version=5, title="Why Buffets Don't Lose Money", duration=DUR, scenes=S)
json.dump(board, open('editor/storyboard.json', 'w'))
lens = [round(s['e'] - s['s'], 1) for s in S]
print(len(S), 'scenes', sum(len(s['items']) for s in S), 'items', sum(1 for s in S for i in s['items'] if i['k'] == 'sfx'), 'sfx; scene length', min(lens), '-', max(lens))
