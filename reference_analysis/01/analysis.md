# Reference 01: "Every Historical Glitch We Can't Explain"

This file was analysed as the substitute for reference 01, at the user's instruction. It is 24:50.6 long, 1280×720, 30 fps, with 44,715 decoded frames. The first video frame has PTS 0.033333 s and the audio starts at 0.000 s.

Detailed data:
- `frames.csv`: one row per frame.
- `events.csv`: 1,451 events.
- `audio_cues.csv`.
- `chapters.json`.
- `transition_measurements.md`.
- `annot/*.tsv`: the visual notes for each event.
- `evidence/`: review sheets.

## Coverage

| Status | Frames | Share |
|---|---:|---:|
| identical_hold_verified (md5 identical to the previous decoded frame) | 18,186 | 40.7 % |
| near_identical_hold_measured (≤ 0.04 % of pixels changed by more than 24 levels; codec noise) | 24,423 | 54.6 % |
| visual_verified (event boundary frames, or frames inside per-frame strips, looked at) | 1,557 | 3.5 % |
| event_interior_measured (inside a multi-frame event; measured, not individually viewed) | 489 | 1.1 % |
| measured_codec_refresh (I-frame refresh with no content change; rule verified on a sample) | 60 | 0.1 % |
| **Total** | **44,715** | 100 % |

**How events were reviewed:**
- Every one of the 1,451 change events was looked at.
- C01–C04 were reviewed with before / first / last / after crops, plus per-frame strips and tight-diff crops.
- C05–C22 were reviewed from before/after crops of each event's changed region.

**Audio:**
- Measured only: waveform, spectral analysis and PocketSphinx word timing (4,213 words).
- Nothing was heard, because there is no playback in this environment.

## Format at a glance

**Canvas**
- Flat light blue, sampled near #BDE7FB, everywhere.
- Never textured, never a full background plate.
- Exceptions:
  - occasional ground strips or vignettes (brown earth, grass, water, a night-sky patch);
  - one tinted "inside the cloud" frame (C05).

**Chapter index**
- 24 tiles in a 6 × 4 grid. Each tile is a feathered archive image with a 1–2 line title.
- There are 23 chapters (the Titanic chapter was found during review), and every one is entered through the grid.
- Transition:
  1. Hard cut to the grid; it holds 6 frames.
  2. It zooms into the chosen tile in 14–15 frames, using an exponential scale ×1 → ×3.8–4.1 that eases out.
  3. The title card holds 40–45 frames.
  4. Hard cut to the chapter canvas.
- Measurements are in `transition_measurements.md`.

**Chapter opening**
1. The tile image is reused, small, at the left, either as a feathered vignette or as a cut-out.
2. A 2-line header sits at top centre, in small black hand lettering: chapter name, then date.
3. The date often fills in 0.5–1 s after the header ("July 29" → "July 29, 1900"), as a two-step text update.

**Content order**
After the opening, facts arrive left → right:
1. a flag (country);
2. an occupation icon;
3. a map with a red X and a place label, often with a curved arrow;
4. a number label with a small arrow ("29 years old").

**Characters**
- Big, waist-up torsos cropped by the bottom edge, holding their place across many events.
- They change by **swapping the whole drawing**: pose swap 89×, expression swap 38×.
- They almost never move.
- A second character enters from the opposite side; dialogue happens through speech bubbles.
- A recurring narrator or "professor" figure (white blob head, glasses, book) explains near the end of each chapter.

## Measured pacing (all 23 chapters)

| Measure | Value |
|---|---|
| Narration rate | about 170 words per minute (4,213 words) |
| Composition length (reset to reset) | median 9.0 s (IQR 4.7–13.3 s, n = 159) |
| Gap between beat events (appear, label, enter, swap, replace) | median 1.33 s (IQR 0.69–2.30 s, p90 3.5 s) |
| Beat events per composition | median 5, p75 7.5, max 16 |
| Longest stretch with no visual change | 5.3 s; only 2 % of runtime sits in still stretches over 4 s |
| Event duration | 1 frame for 79 %; 2–8 frames for 16 %; longer for 5 % (zooms, fades, slides) |

## Motion vocabulary (counts from events.csv)

**Placement and text**
- **appear** (559): placed whole in a single frame. No fade, no scale-pop.
- **label** (104) and **text_update** (23): appear whole.

**Characters**
- **pose_swap** (89) and **expression_swap** (38): replacement drawings at the same anchor.

**Scene changes**
- **layout_reset** (98), **hard_cut** (44) and **partial_reset** (18): the composition is cleared down to 1–2 kept elements, which may be resized.
- **enter** (42): a character slides in from off-frame over 3–6 frames with ease-out (C01 F885–F888; C02 F3633–F3640, taken in 3 held steps), or is simply placed.

**Movement**
- **reposition**, **scale_up** / **scale_down**, **motion_step** and **position_jumps**: moves are stepped.
  - Objects hold for 3–9 frames, then jump.
  - Example: the C02 sun zig-zag holds 9 → 4 frames per position (measured centre track in `annot/C02.tsv`).
  - "Travel" along a map is 3–5 discrete hops of a face or marker icon (C11 F22129–F22140; C14 F29809–F29856).

**Looping effects (cycles)**
- **cycle_swap**, **boil_cycle**, **flash_cycle** and **dance_cycle**: 2–3 drawings alternate every 3–6 frames.
- Uses: spinning sun, twinkling sparkles, the Vela double flash, the dance plague, cloud interiors.

**Camera**
- **camera_zoom** and **camera_zoom_out** are used only for:
  - the index;
  - map zoom-ins and zoom-outs (C06 F11340–F11358, Mexico → world, with holds; C09 Lake Superior);
  - the C21 dancer zoom-out.

**Fades and dissolves**
- **fade_step** (C21 F40746–F40841): stepped opacity, 6–7 levels about 7 frames apart.
- A cross-dissolve is used once (C21b F41590–F41601, book cover → ship illustration, 12 frames).

**Accents**
- Red X: drawn over an item about 0.3–0.4 s after it appears, used to rule things out (C03, C09, C10, C17, C20).
- Red circles round places on maps.
- Red "!" marks.
- Yellow lightning marks for stress.
- Stamps: "MISSING", "CLASSIFIED".

## Recurring scene recipes

1. **Ruled-out list.** One icon appears, then a red X lands on it, then the next icon, then its X. The pattern is C03 F5595–F5650, C09 F18542–F18576, C10 F19677–F19687 and F20402, and C20 F38868–F38988.
2. **Comparison table.** Two characters face each other with an "=" between them. The "=" shrinks, then matching icon pairs build down in rows, one row every 1.2–2.5 s. Seen in C04 F6772–F7019 (king and chef), C07 (Lincoln–Kennedy), C15 (Jim twins).
3. **Map story.** A small map appears beside the anchor, with a red X and a place name.
   - Movement is shown by a curved arrow.
   - Distance is shown by a dimension line with a label ("1.9 miles", "600 miles off course", "9,000 miles away").
   - A zoom-out to a world map reveals scale (C06).
4. **Symptom or consequence ring.** A central symbol is surrounded by pictograms placed one at a time around it, about 1 per second (C03 F5236–F5400; C21 F39875–F39941).
5. **Explainer close.** The narrator or professor torso enters, says one bubble line, and props icons line up next to him. It ends on a dry one-liner bubble ("This Doppelgänger was just a myth", "Anyway, it's still a good story!").
6. **Event reenactment.** The hard cut usually changes scale: the full-body figure is smaller, and gets a ground strip or vignette only when needed. Sensitive moments are shown as cartoon X-eyes, small red marks, an x-ray skeleton gag or a crosshair, never graphic (C04, C07, C11, C20).

## Audio
- **Narration:** a single narrator, continuous. 606 pauses of at least 0.25 s (median 0.33 s, longest 6.0 s).
- **Music bed:** continuous and tonal, about 25–28 dB under the voice, at a steady level, fading out over the final second.
- **Sound effects:** the 678 broadband transients found inside voice pauses are **not aligned to the picture**. They fall within ±2 frames of a visual event at the same rate as random times (13.4 % vs 12.8 %).
- **Conclusion:** there is no systematic sound effect on pops, cuts, entrances or Xs. The picture is driven by the narration and the bed alone.

## What remains unverified
- **Audio:** cue identities are unverified (no playback).
- **Event interiors:** the 489 frames inside multi-frame events in C05–C22 were not viewed one by one, but their endpoints were.
- **Exact word alignment:** whether elements land on exact words cannot be shown statistically, because narration words are too dense (chance of being within 150 ms of a word onset is about 70 %). By inspection, elements arrive on the noun or number they illustrate, but that is not measured.
