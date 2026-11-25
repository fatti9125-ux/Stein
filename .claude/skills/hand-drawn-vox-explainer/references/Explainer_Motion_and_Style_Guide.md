# Explainer motion and style guide

This guide is built from two frame-by-frame analyses:
- **Reference 01**, "Every Historical Glitch We Can't Explain": 44,715 frames, 1,451 events, 23 chapters.
- **Reference 02**, "How Every Feared Waffen-SS General Died": 37,602 frames, 1,155 events, 27 profiles.

Frame references below are source frame IDs: `R1 F…` or `R2 F…`. Values come from `01/events.csv`, `02/events.csv` and the two `analysis.md` files.

## 0. The ten rules that matter most
1. **Canvas:** flat light blue (#BDE7FB / #BCE7FB) for the whole video. Nothing else is full-frame, except brief title cards or index tiles and small ground, water or room vignettes.
2. **Things appear, they don't animate in.** 79 % of all events (R1) last a single frame: whole drawings placed or swapped. Never use fades, scale-pops or slides for ordinary icons.
3. **Characters change by swapping drawings,** never by tweening limbs. The anchor holds its footprint while its pose or expression swaps. React within 0.3–1.5 s of the line that motivates it.
4. **One new beat every ~1.3–1.4 s** (median gap; IQR 0.7–2.4 s).
   - Reset the composition every ~5 s (R2 profile pace) to ~9 s (R1 story pace).
   - Build up to 5 beats (R1) or 3 beats (R2) per composition.
   - Never leave the frame unchanged for more than ~4 s.
5. **Reset by hard cut,** keeping one carry-over (the anchor character, a key symbol, or the header).
6. **The header is the spine.** Small black hand lettering at top centre: subject or chapter, then date. The date fills in or updates in place ("July 29" → "July 29, 1900").
7. **Real places and things** go on a cream map with red or black X marks and hand-lettered names, or in a feathered grayscale or sepia archive vignette.
8. **Red is the only accent for annotation.**
   - A red X rules something out, landing about 0.3 s after it appears.
   - Red circles and ellipses mark places.
   - Red curved arrows show movement.
   - Red "!" marks shock.
   - Green check and green up-arrows mean success or promotion.
9. **Movement is stepped, not tweened.**
   - Objects hop between held positions every 3–9 frames: the sun zig-zag, map markers, bars sliding, climbing.
   - Only camera zooms and make-room compactions are smooth, eased over 3–15 frames.
10. **No picture-synced sound effects.** In both references, voice-pause transients line up with visual events at chance level. Use narration plus a quiet music bed about 26 dB down, and put sound effects only on a few signature moments, if any.

## 1. Canvas and colour
- **Background:** #BFE6F5 in our engine. The references decode to #BDE7FB; keep ours.
- **Ink:** black outlines for all line art, with slight hand irregularity.
- **Accents:**
  - red #D0362C for X marks, circles, arrows and stamps;
  - yellow for sun, light and sparkle;
  - green for checks and up-arrows;
  - pale red for region fills on maps.
- **Archive images:** grayscale or sepia, with a feathered (blurred-edge) oval or rectangle vignette. They are never hard-framed, except a handful of newspaper clippings (R1 C18 F35748).

## 2. Templates

Each template gives its source evidence, layer stack (top → bottom), parameters, timing, and when to use it.

### T1. Chapter index → title card → canvas (R1, 23×; R2 roster, 27×)
- **Evidence:** R1 F7–F65, F2300–F2364 (`transition_measurements.md`); R2 F20519–F20533 (`roster_zoom_C15.txt`).
- **Layers:**
  - **Grid:** a grid of tiles (R1: feathered image plus 1–2 line title; R2: feathered portrait plus name).
- **Timing:**
  1. Hard cut to the grid; hold 6 frames.
  2. Zoom 14 frames, with scale ×1 → ×3.3–4.1, constant log-velocity, eased over the last 3–4 frames, and the target tile centred.
  3. Hold the title card 40–45 frames.
  4. Hard cut to the canvas.
- **Params:** target tile index, final scale, hold lengths.
- **Use:** every chapter or list item in a "N things" or "every X" format.

### T2. Profile or chapter opener (archive + header + facts row)
- **Evidence:**
  - R1 C04 F6354–F6525 (portrait, date fill F6386, name label, flag, map, arrow);
  - R2 C01 F65–F245, C17 F22654–F22781.
- **Layers:**
  - header (2 lines);
  - feathered archive image at left (x .00–.30);
  - facts row building left → right;
  - map at right (x .55–.97).
- **Timing:**
  1. Header appears with the cut.
  2. The date completes 0.5–1.1 s later.
  3. Facts arrive every 0.8–1.5 s.
  4. The map comes last, with its X 0.3 s after it.
- **Use:** the first 5–8 s of every chapter.

### T3. Anchor torso + evolving facts (the main explainer template)
- **Evidence:**
  - R2 every profile: torso at bottom-left, cropped mid-chest, about 0.30 of frame width;
  - R1 C04 F6589+ (king and chef), C07 (Lincoln/JFK), C15 (twins).
- **Layers:**
  - anchor torso (bottom-left, cropped);
  - 1–3 element row or map in the free area (x .35–.95);
  - header.
- **Acting:**
  - neutral at the start of a beat;
  - point (toward the element) when the element arrives;
  - hand on chin when doubt is narrated;
  - hands up or handcuffed for a plot turn.
- **Timing:** each element on its noun or number; a pose swap at most every 2–3 s.

### T4. Two-actor dialogue
- **Evidence:** R1 C04 F6589–F6765, C06 F11489–F11669; R2 C04 F5714–F5771, C16 F22036–F22116.
- **Layers:**
  - actor A bottom-left facing right;
  - actor B bottom-right facing left (opposing three-quarter views);
  - speech bubble over the speaker, tail to the mouth;
  - an optional map or backdrop between them.
- **Timing:**
  - B enters in 1 frame or in 3–5 frames.
  - The bubble appears 2–3 frames after the speaker's pose swap (R1 F1338 → F1340).
  - The listener reacts with an expression swap 0.3–1 s later.
  - The bubble holds until the next line, then is replaced.
- **Use:** quotes, accusations, orders.

### T5. Ruled-out list (icon + red X, repeated)
- **Evidence:** R1 C03 F5595–F5650, C09 F18542–F18576, C10 F19677–F19687 and F20402, C20 F38868–F38988.
- **Timing:**
  - Each icon appears, then its red brush X appears 0.25–0.4 s (8–12 frames) later.
  - The next icon follows 0.3–1 s after that.
  - Three items per row.
- **Use:** "it wasn't X, it wasn't Y, it wasn't Z".

### T6. Comparison table (A = B, rows building)
- **Evidence:** R1 C04 F6772–F7019 (5 rows), C07 F12986–F13353, C15 F30500–F30651.
- **Layers:**
  - two figures facing each other;
  - a big "=" that shrinks after about 1.5 s;
  - matching icon pairs added row by row underneath.
- **Timing:** one row every 1.2–2.5 s, each row on its spoken item.

### T7. Map story
- **Evidence:**
  - R1 C06 F11298–F11358 (zoom-out to world, "9,000 miles away");
  - R1 C11 F22129–F22140 (face marker hops in 4 steps);
  - R2 C11 F16186–F16204 (marker crosses Albania in 4 steps), C24 F31834–F31964.
- **Layers:**
  - cream map;
  - region fill (pale red) or ellipse (red);
  - X marks + labels;
  - curved arrow, or a head or icon marker;
  - an optional dimension line with a label.
- **Timing:**
  - Map, then X 0.3–0.5 s later, then label with the X or 0.3 s after it.
  - Movement: a marker hop every 3–7 frames.
  - Zoom in or out: 3–4 stepped scale changes, or a smooth zoom of 15–130 frames with holds.

### T8. Symptom or consequence ring
- **Evidence:** R1 C03 F5236–F5400 (6 pictograms round a central face), C21 F39875–F39941.
- **Timing:** a central symbol, then pictograms placed around it about every 0.8–1.1 s, filling the canvas.

### T9. Escalation ladder (biography end)
- **Evidence:** R2 almost every profile (e.g. C10 F14748–F15397, C14 F19623–F20354).
- **Steps:** each step is a hard cut with one plate:
  1. hands up + captor;
  2. handcuffed;
  3. courtroom (chair + judge);
  4. bars (slide away in 3–6 steps);
  5. civilian;
  6. armchair;
  7. slump;
  8. date of death + "aged NN".
- **Use (generalised):** any "what happened next" consequence chain.

### T10. Stepped motion effects
| Effect | Evidence | Mechanism |
|---|---|---|
| Spin or twinkle | R1 F2916–F3014 | 2 drawings alternate every 4–6 frames |
| Zig-zag or erratic path | R1 F3208–F3264 | held positions; holds shorten 9 → 4 frames (acceleration) |
| Dance cycle | R1 F39588–F39780 | 2–3 poses, a swap every 3–10 frames |
| Flash pulse | R1 F33551–F33765 | size swaps every 3–5 frames, in 2 pulses |
| Fade out | R1 F40746–F40841 | 6–7 opacity steps about 7 frames apart |
| Bars release | R2 F14922, F22261 | bars translate in 3–6 steps |

### T11. Make-room and compaction
- **Evidence:** R1 C01 F1632–F1634 (group slides 0.05 width in 3 frames), F2110–F2117 (cluster shrinks to ~0.7× and moves to a corner); R2 C01 F464–F468.
- **Mechanism:** smooth, eased-out translate and scale over 3–8 frames. This is the only routinely tweened motion besides zooms.

### T12. Explainer close (professor + one-liner)
- **Evidence:** R1 C04 F7750–F7813, C20 F38613–F39086, C22 F44448.
- **Timing:** the narrator or professor torso enters; supporting icons appear one by one; it ends on a dry bubble line.

### T13. End card
- **Evidence:** R1 F44554–F44714, R2 F37412–F37601.
- **Layout:** the presenter at the left (x .05–.35) pointing right, with a bubble "Watch these!". The right 60 % stays empty for end-screen elements, for about the last 5 s.

## 3. Typography
- One hand-lettered sans-serif family everywhere (rounded, slightly irregular).
- Black, sentence case.
- **Sizes (relative to 720 p):**
  - header ~18–22 px;
  - labels ~16–26 px;
  - numbers and dates as standalone labels ~40–60 px;
  - title-card titles ~30 px.
- **Labels** sit directly above their object, or connect to it with a thin curved arrow ("aged 51 ↘", "29 years old ↗").
- **Quotes** go in white bubbles with a black outline. Thoughts go in cloud bubbles with trailing circles.
- **Our engine:** "Patrick Hand" for labels and headers, which is the closest open match.

## 4. Sound
- One narrator, with no music swells on cuts.
- A music bed throughout, about 26 dB under the voice, steady, fading out at the very end.
- No sound effect per element (both references, measured).
- For our videos: voice plus bed. Sound effects are optional and only for 1–3 signature moments per chapter, and they stay editable.

## 5. Content safety
- Show real violence symbolically: skull icons, X-eyes, a figure lying down, small red marks, pictograms.
- Present maps of historical regimes as historical context only.
- Use symbols only as identifiers.
