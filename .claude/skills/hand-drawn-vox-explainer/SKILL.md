---
name: hand-drawn-vox-explainer
description: Turn a voiceover, a script and a hand-drawn asset pack into a long-form (10–20 min) cartoon-history explainer in the user's reference style. The style has a flat pale-blue background, one big waist-up main character on the left, a small stacked header at the top, and content that builds left to right like a sentence, with hand-lettered labels, red arrows and Xs, feathered archive photos and counting numbers. Builds a live, editable browser storyboard (save, version history, autosave) and renders it to 540p preview / 1080p / 4K MP4. Use whenever the user sends a script + voiceover + asset zip and asks for a video, preview or sample, says "same style as the clips", "same style as Perseus" or "vox style", or asks for a re-render after edits.
---

# Hand-drawn explainer (reference-clip style)

The user writes the script, records the voiceover and supplies a hand-drawn asset pack (characters, props, effects, backgrounds, often ready-made number cards). You turn it into a finished video in the style of their five reference clips and give them a live editor to tweak it.

`SKILL_DIR` is this folder. `references/sheet1–5.jpg` show the five reference clips at two frames per second. **Look at them before storyboarding.** `engine/index.html` is both the editor and the renderer, so the preview is exactly what gets rendered.

## The look (read straight off the reference clips)

**Background**
- Flat pale sky blue `#BFE6F5`, nothing else.
- No paper texture, no grid paper, no torn cards, no yellow paint blocks, no dark backgrounds.

**Main character (the anchor)**
- One **big, waist-up** character stands bottom-left, cropped by the bottom edge and sometimes by the left edge.
- Use full-body art about 1000 px tall with the feet below the frame, so only the head down to the hips shows.
- They stay on screen through the whole beat. To change their reaction, swap to another pose of the same character in the same spot rather than moving them.
- Wide sprites (a character holding a door, a counter or a big prop) are scaled down so they don't spill into the content area.

**Second character**
- Comes in bottom-right at the same size, facing the anchor, for a conversation, an exchange (handshake, tip, order) or a reaction.
- **Characters always face each other.** The engine flips sprites using the facing tags in `library.json`.

**Header**
- A small stack at top-centre in the hand-lettered font: subject, then date or place, then context.
- Update it in place as the story moves ("1944" → "April 27, 1945").

**Content (the sentence)**
- Builds **left to right next to the anchor like a sentence**: element, red or black arrow, element, element.
- Each element gets a **small plain black hand-lettered label above it**.
- Two rows at most. Spacing is automatic, so nothing ever overlaps.

**Supporting visuals**
- **Archive photos and places** are soft **feathered vignettes**, with black and white for real archive photos.
- **Maps:** a pale map with a red X and a place label, red arrows for movement.
- **Numbers** are plain hand-lettered text that counts up, with a small caption above.
- Red means bad (losses, debt, "banned") and green means good. That is the only colour coding.
- **Callouts:** a red X crosses out what's wrong, and a red ink circle rings what matters. White speech bubbles and cloud thought bubbles (sometimes with an icon inside) carry quotes and thoughts.

**Motion (keep it simple, like the clips)**
- Things **appear on their word** with a tiny settle. No big pops, no slides.
- **Hard cuts** between beats, usually every 5–12 s.
- Use an occasional **zoom punch** (`z`) to reframe on a face or detail.
- A second character can slide in from the right.
- Counters count up, and bars grow.
- The line boil and drawing on twos (15 fps, encoded at 30 fps) keep it hand-made.

**Vox touches (keep them light)**
- Red ink arrows and circles, a counting number, an occasional bar chart for a comparison, the pack's own number cards.
- No yellow stickers, no paper notes, no paint wipes. The user moved away from those after seeing them.

## Pacing rules (from the user's feedback)
1. **Sync:** time every element to its word with forced alignment (step 3), and have it land **0.15 s before** the word.
2. **No empty frames:** every beat opens with the anchor (and usually the first element) already on screen.
3. **Busy, not crowded:** something new every 1–2 s, with no more than about 3.5 s without a change. Each element has its own space, and the auto-layout guarantees it.
4. **Sound effects only on key hits:** stamp, ching (money), crash, ding, clang. About 2–3 per minute at most.
5. **Archive images where real places, things or people appear:** Wikimedia Commons public-domain or CC images, credited in the caption, with `meta.json` kept. If downloads fail, use the closest illustrated plate and swap in the photo later.
6. **Reenactments:** add the pack's "illustrated reenactment" tag bottom-right on scenes depicting real people.

## Workflow

### 1. Unpack and look
- Unzip into its own folder and read `Asset_Index.csv`, any scene guide and the notes.
- Run `scripts/contact_sheets.py` and **look at every sheet**.
- Tag each character's facing (`FACE` in `scripts/build_library.py`: L, R or F).
- Run the library build. It produces `editor/assets/*.webp` and `editor/library.json` with `k: char | prop | fx | bg | gfx | archive`.

### 2. Transcribe
- Hugging Face, OpenAI and Vosk model downloads are blocked here. Use PocketSphinx: its English model ships inside the pip package.
- Make a 16 kHz mono WAV and run `scripts/transcribe_chunk.py` as 4 parallel workers.

### 3. Align to the script (this is what fixes "voice not in sync")
1. Run `scripts/rough_align.py`. It tokenises the narration, skipping `[cues]` and chapter headings because they aren't spoken, and marks sentence ends.
2. Run `scripts/force_align.py`. It does PocketSphinx forced alignment one sentence at a time with a sliding window, and writes `script_words_fa.json`.
   - First fill in the **spoken form of every number** (`SP`), taken from how the narrator actually read it. For example, "$7.40" was read "seven dollars and forty cents".
   - Add phones for unknown names (`PH`).
   - Target: 0 failed sentences.

### 4. Storyboard
Write it in the DSL of `examples/buffet_build_board_v3_clip_style.py`:

```python
scene('script phrase that starts the beat', ('Subject', 'date / place', 'context'),
      [A('C02-01', lab='Gary'), B('C03-01', 'cue phrase')],                 # anchor (+ optional second character)
      [[E('F03-05', 'cue', 'label above', h=300), ARW(), Nm(100, 'cue', pre='~', cap='plates')],   # row 1
       [P('B05-02', 'cue', cap='feathered plate'), X('cue'), Tx('plain words', 'cue')]],            # row 2
      [BUB('"quote"', 'cue', x, y, w, tx, ty), THK('thought', 'cue', ...), SFX('stamp', 'cue')])
```

**Elements and markers**

| Helper | What it places |
|---|---|
| `E` | a prop, food, effect or number card |
| `Nm` | a plain counting number with a caption |
| `P` | a feathered photo or plate |
| `Tx` | hand-lettered words |
| `ARW()` | an arrow joining the neighbouring elements |
| `X` / `O` | a red X or a red circle on the previous element |
| `RAW` | any explicit element, such as bars, an icon grid or receipts |
| `REEN()` | the reenactment tag |

**Rules**
- Cue phrases are exact script words, and the beat's start phrase is resolved first.
- **Anchors:**
  - Pick the anchor for each beat: the person the narration is about, the mascot for explanations, a diner for customer-side points.
  - Use `noPop=True` when the same anchor carries on into the next beat (continuity across a cut).
- **Header:** set it for each beat and keep it consistent within a story arc.
- **Rows:**
  - Up to 3 elements per row, or 5 for a montage.
  - With a second character present, the free area is the centre column, so use 1–2 elements.
- **Zoom punch:** `z=[('cue', 1.25, x, y)]`.

### 5. Check before rendering
- Render the last frame of every scene with `scripts/capture.js <dir> t1,t2,…`, tile them with `scripts/check_sheet.py`, and **look at every tile**.
- Check for:
  - overlaps;
  - text off the frame;
  - circles or Xs that miss;
  - wide sprites intruding into the content area;
  - wrong facing.
- Expect 2 passes. Also render a few mid-animation frames (counters, entrances) to check the motion.

### 6. Live editor
- Copy `engine/index.html` to `editor/index.html`, then update the title, the placeholder text and the SFX list.
- Publish as an Artifact with `capabilities: {db: {}, downloads: true}`. Use two publishes if there are more than 255 files.
- Editor features:
  - preview with audio, a scene timeline and a transcript strip;
  - drag elements and edit any field;
  - add any element type;
  - **Save**: every save is a version, with an optional note;
  - **History**: open, download, CSV edit log, all versions;
  - 2-minute **autosave**;
  - **Download JSON**.
- Before republishing a new storyboard, check `ArtifactData list versions`. If the user has saved edits, build from **their** version (`board/meta` → `versions/{v}/chunks/c*`), not from the builder.

### 7. Render
1. Run `scripts/mix.py` to get the voiceover plus the sound-effect cues as `mix_full.wav`.
2. Capture frames:
   - **Preview:** `deviceScaleFactor 0.5` gives 960×540.
   - **Final:** scale 1 gives 1080p, and scale 2 gives 4K.
   - Use 4 parallel workers on time ranges, at about 4–5 fps per worker at 540p.
3. Encode: `ffmpeg -framerate 15 -i frames/%06d.jpg -i mix_full.wav -vf "fps=30,format=yuv420p" -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4`
   - Make the 1080p by downscaling the 4K with lanczos.
4. Render gotchas:
   - The capture server must send `text/html; charset=utf-8`, or characters such as ≈, €, · and … come out garbled.
   - In render mode the stage must have no body margin, or the frame comes out 1904 wide instead of 1920.
   - Before restarting a render, stop the old wait-then-encode job, or it encodes a half-finished frame set.
   - Uploads to the user are capped at about 400 MB, so split a long 4K with `-c copy` into parts.

### 8. Deliver and save
- Send the low-quality preview first. Do the final 4K + 1080p only after the user approves.
- Commit the project to the repo: editor, sources, pipeline and a process log. Never commit MP4s or frames.
- Tell the user the editor link, what changed, and anything still pending.

## Good judgment calls
- The pack is the cast. Never restyle or invent characters. If a figure is missing, use the mascot or a prop.
- Real copy only. Every number on screen is in the script, and labels may simplify but never add a statistic.
- Don't put a real person's words in a generic character's speech bubble. A CEO quote goes in as on-screen text, not from a stand-in.
- Brands and real people: storefronts stay blank and the pack's name cards label them. Real people are illustrated reenactments.
- When the user says "elements take too long" or "not in sync", check alignment, empty openers and long gaps, in that order.
- When the user points at the reference clips, re-read `references/` and match the staging (anchor + sentence row + header) before adding any new effects.

## Files
- **`engine/index.html`: element kinds**
  - figures and images: img (`lab` puts a label above), photo (feathered), archive, card;
  - words and labels: text, sticker, stamp, bubble, think;
  - ink marks: arrow, loop, hl, xmark;
  - numbers and charts: counter (`plain`, `nosep`), bars, icons;
  - structure and sound: chapter, sfx.

  Every kind also takes `in`, `mv` and `out`. Scenes take `tr` (cut/slide/up/wipe), `z` (zoom punches) and `cam` (push).
- **`scripts/`:** library build, transcription, rough and forced alignment, capture, check sheet, mix, SFX synthesis.
- **`examples/`**
  - `buffet_build_board_v3_clip_style.py`: **the current reference**;
  - the older Perseus and Buffet v2 (Vox-heavy) builders;
  - the original vox skill.
- **`references/`:** two-frames-per-second contact sheets of the user's five reference clips.
- **`sfx/`:** stamp, ching, crash, ding, pop, swish, whoosh, clang, crack, splash, rewind.
