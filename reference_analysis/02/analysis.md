# Reference 02: "How Every Feared Waffen-SS General Died"

This file matches the manifest: container 1253.516 s, 37,602 decoded frames, first video PTS 0.033333 s, audio starting at 0.000 s, 1280×720 at 30 fps.

Detailed data:
- `frames.csv`: one row per frame.
- `events.csv`: 1,155 events.
- `audio_cues.csv`.
- `chapters.json`: 27 profile chapters.
- `annot/*.tsv`.
- `evidence/`.

The war subject is studied only for its visual grammar. Every death and atrocity in the source is shown symbolically (skull icons, X-eyes, a figure lying down, red marks, pictograms) and never graphically. Our recipes keep that rule.

## Coverage

| Status | Frames |
|---|---:|
| identical_hold_verified | 13,165 |
| near_identical_hold_measured | 22,742 |
| visual_verified | 1,198 |
| event_interior_measured | 442 |
| measured_codec_refresh | 55 |
| **Total** | **37,602** (every frame present, no gaps) |

- All 1,155 events were reviewed from before/after crops of each event's changed region.
- Audio was measured only, never heard.

## Format at a glance (and how it differs from reference 01)

**Roster instead of index**
- A grid of soft-edged grayscale portraits (about 9 × 4), each with a name under it.
- Each profile opens the same way:
  1. Hard cut to the roster; it holds 5–6 frames.
  2. It zooms into the chosen portrait in 14 frames: ×1 → ×3.3, exponential, easing out over the last 3 frames.
  3. The enlarged portrait strip holds about 45 frames, with neighbouring portraits visible on both sides.
  4. Hard cut to the profile canvas.
- Measured at C15 (F20519–F20533). The scale per frame was 1.097, 1.206, 1.328, 1.464, 1.618, 1.787, 1.974, 2.175, 2.389, 2.606, 2.821, 3.019, 3.184, then 3.304 (settled). The centre drifts from x .515 to .621, with y steady at about .49.
- The end card has a presenter on the left with the bubble "Watch These", leaving space on the right for end screens.

**Profile header**
- Small black text at top centre: the subject's name, then a date under it once the story is dated.
- The date updates in place as time advances, for example "April, 1945" → "April 28, 1945" (C03, C04, C09, C24…).

**Opening composition (always the same)**
1. The feathered grayscale portrait is reused at the left.
2. Then come units or symbols:
   - division shields with a 2–3 line label above each;
   - rank stars with green up arrows for promotions;
   - a "commander pointing at troops" pictogram;
   - medal photos.
3. Then a Europe map with the relevant region shaded and place names marked with an X.

**Torso puppet**
- After the first hard cut, the subject becomes a cartoon torso at bottom left: black uniform, cap with eagle, cropped at mid-chest.
- He stays on screen for most of the chapter.
- He changes only by pose swaps (point, open palm, hands up, handcuffed, wounded, hand on chin) and expression swaps.

**Escalation ladder.** Almost every chapter ends with the same sequence of hard cuts, which lets the viewer predict the structure:
1. Hands up, as a US, British or Soviet soldier enters from the right.
2. Handcuffed.
3. Courtroom: an empty chair at the left and a judge at the bench on the right.
4. Behind bars, with the bars sliding away in 3–6 stepped frames.
5. A civilian-jacket puppet.
6. An old man in an armchair who slumps with X-eyes.
7. Date of death, then "aged NN" with a curved arrow, sometimes followed by a funeral-crowd plate with a count.

**Maps**
- Light cream land over the blue canvas.
- Regions are shaded light red, sometimes with a swastika marker as a historical identifier, or circled with a hand-drawn red ellipse.
- Places get a black or red X and a hand-lettered name.
- Movement is shown by red or black curved arrows, or by a helmet or face head-marker that hops across the map in 3–5 steps.
- Maps are often a small inset next to the puppet, enlarging in 2–3 steps when they become the subject.

**Bubbles and insets**
- Speech bubbles for direct dialogue.
- Cloud thought bubbles containing icons.
- Circular insets (a face, a gulag icon).

## Measured pacing

| Measure | Reference 02 | Reference 01 |
|---|---|---|
| Narration rate | about 194 wpm (4,045 words) | about 170 wpm |
| Composition length (reset to reset) | median **5.2 s** (IQR 2.8–7.6 s) | median 9.0 s |
| Gap between beat events | median 1.4 s (IQR 0.7–2.5 s) | median 1.33 s |
| Beat events per composition | median **3**, p75 5, max 10 | median 5 |
| Longest still stretch | 4.1 s (0.3 % of runtime above 4 s) | 5.3 s (2 %) |

**Comparison with reference 01:**
- Reference 02 resets far more often: 156 layout resets and 53 hard cuts, against 98 and 44 in a longer video.
- Its compositions are smaller (about 3 beats each).
- The sense of continuity comes from the persistent puppet and header, not from building one dense canvas.

## Motion vocabulary specific to reference 02
- **Stepped bars slide-away (release):** the bars move left in 3–6 discrete steps (C10 F14922, C16 F22261–22265, C26 F36150).
- **Stepped climb:** the escape over a wall in C22 F29968–F30010 uses 6 climb poses about 7 frames apart.
- **Group compaction:** when a new emblem or map arrives, the previous emblems shift and shrink in 3–5 frames (C01 F464, C11 F16074).
- **Second character entry:** the opposing actor (captor, judge, leader) is placed at the right edge facing left in 1 frame, or enters over 3–5 frames. The puppet then reacts with a pose swap within about 0.3–1.5 s.

## Audio (measured, not heard)
- **Narration:** a single narrator at about 194 wpm, with 543 pauses of at least 0.25 s.
- **Music bed:** continuous, with 10 ms RMS p10 at about −44 dBFS against voice p90 at about −17.6 dBFS, so roughly 26 dB under the voice. It fades out over the final second.
- **Sound effects:** the 587 transients found in voice pauses fall within ±2 frames of a visual event 15.5 % of the time. Random pause times score exactly the same, 15.5 %.
- **Conclusion:** there are no picture-synced one-shot sound effects, exactly as in reference 01.

## What remains unverified
- **Event interiors:** the 442 frames inside multi-frame events were not viewed one by one.
- **Audio:** cue identities are unverified (no playback).
- **Manifest checkpoints:** the face-inset and callout pairs listed in the manifest were reviewed through the C04 events. For example, the "Find Fegelein!" bubble is at F5771, 1 frame after the manifest's F005770 hand-to-head pose and before F005774. Other checkpoints were not re-measured beyond their containing events.
