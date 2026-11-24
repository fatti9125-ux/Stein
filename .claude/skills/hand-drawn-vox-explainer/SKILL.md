---
name: hand-drawn-vox-explainer
description: Turn a voiceover, a script and a hand-drawn asset pack into a long-form (10–20 min) animated explainer that mixes cartoon-history characters on a sky-blue background with Vox/editorial motion graphics (torn paper cards, yellow paint blocks, ink circles and arrows, stickers, red stamps, rolling counters, growing bar charts, archive photo cards). Builds a live, editable browser storyboard (with save, version history and autosave) and renders it to 1080p/4K MP4. Use whenever the user sends a script + voiceover + asset zip and asks for a video, a preview, a sample, "vox style", "same style as Perseus", or a re-render after edits.
---

# Hand-drawn Vox explainer

The user writes the script, records the voiceover and supplies a hand-drawn asset pack (characters, props, effects, backgrounds, often ready-made number cards). You turn that into a finished video in their house style and give them a live editor so they can tweak it themselves. Two finished projects define the style: **Perseus & Medusa** (story, characters) and **Why Buffets Don't Lose Money** (money, numbers). Their storyboard builders are in `examples/`.

`SKILL_DIR` is this folder. `ENGINE` is `engine/index.html`: one HTML file that is both the editor and the renderer, so what the user sees in the preview is exactly what gets rendered.

## The look (why it works)

- **Ground:** flat sky blue `#BFE6F5` with a faint animated grain. Never grid or checkered paper (the user rejected it), and never a dark background.
- **Figures:** the pack's hand-drawn characters, big (about 600 px tall on a 1080 frame), standing on the bottom edge.
  - The main figure goes left (x≈330) and the second figure goes right (x≈1590).
  - **Characters always face each other.** The engine flips a sprite when its tagged facing (`f: L/R/F` in `library.json`) points away from the centre. Tag every character when you build the library.
- **Vox layer on top:** torn paper notes with serif italic, a yellow highlighter swipe under the key words, Anton headlines, yellow stickers with the hand-lettered font, red rubber stamps, ink circles and arrows that draw on, speech bubbles, and archive photos on torn cards with a typewriter caption.
- **Numbers move:** money and statistics are rolling **counters** on a paint block, comparisons are **bars** that grow, and "1 in N" ideas are an **icon grid** that fills in.
- **Motion:**
  - Everything moves on twos (15 fps, then encoded at 30) with a line "boil", so it feels handmade.
  - Every scene has a slow camera push-in.
  - Scenes change with a slide, an upward push, or a yellow paint wipe (the wipe is used at chapter starts).
  - Elements pop in, slide in from a side, glide aside to **make room** for new ones, and shrink out when they leave.
- **One idea per element, each with its own space.** Nothing may overlap or crowd. When a new idea needs room, move the old one with `mv`; don't stack on top of it.

## Pacing rules (from the user's feedback)

1. **Sync:** every element is timed to the word it illustrates and lands about **0.15 s before** that word. Use forced alignment (step 3), never guessed times.
2. **No empty openers:** every scene shows something on its first frame. The builder pulls a scene's earliest element(s) to the scene start.
3. **Keep it busy:** something new arrives roughly every 1.5–2.5 s. Aim for **no gap longer than about 3.5 s** without a new element or a running animation (counter, bars, type-on). After building, list the gaps along with the words spoken in each, and add an element that fits what's being said, placed in free space.
4. **Sound effects only on key hits:** stamps, money reveals ("ching"), crashes, the odd bell. About 3 per minute at most. No ambient or transition sounds.
5. **Archive images:** the user wants real archive photos where the story has real places or things. Use Wikimedia Commons public-domain or CC images, with the licence and author in the caption, and keep `meta.json`. If a download fails, fall back to the closest illustrated background and swap the photo in later.
6. **Circles and arrows land on the right spot.** For example, the Medusa circle goes around her whole face. Compute positions from the sprite's size; don't guess.
7. **Reenactments:** put the pack's "illustrated reenactment" tag in the corner of any scene that shows real people as illustrations.

## Workflow

### 1. Unpack and look
- Unzip the pack into its own folder and read `Asset_Index.csv`, any scene guide and the notes.
- Run `scripts/contact_sheets.py` and **look at every sheet** (characters, props, graphics, backgrounds).
- Tag the facing of each character (L/R/F) in `FACE` in `scripts/build_library.py`.
- Run `build_library.py`. It converts everything to WebP in `editor/assets/` and writes `editor/library.json` (`k: char | prop | fx | bg | gfx | archive`).

### 2. Transcribe
- Hugging Face, OpenAI and Vosk model downloads are blocked in this environment. Use PocketSphinx: its English model ships inside the pip package.
- Convert the voiceover to 16 kHz mono WAV.
- Run `scripts/transcribe_chunk.py <startMin> <endMin>` as 4 parallel workers.
- Merge the results into `words_raw.json`.

### 3. Align to the script (this fixes "voice not in sync")
1. Run `scripts/rough_align.py`. It tokenises the script's narration (skipping `[cues]` and chapter headings, which aren't spoken), matches it to the recognised words, and marks sentence ends.
2. Run `scripts/force_align.py`. It does PocketSphinx **forced alignment** one sentence at a time with a sliding window, giving exact word times in `script_words_fa.json`.
   - Before running it, fill in the spoken form of every number and symbol (`SP`). Read how the narrator actually said each one from the free transcript, e.g. "$7.40" was read "seven dollars and forty cents".
   - Add phones for out-of-vocabulary names (`PH`).
   - Target: 0 failed sentences.

### 4. Storyboard
Write `build_board.py`, modelled on `examples/buffet_build_board.py` (numbers-heavy) or `examples/perseus_build_board.py` (character story). Rules:

**Timing and order**
- `T('exact script phrase')` returns that phrase's time minus the lead. Write scenes in script order.
- One scene per idea, usually 5–15 s.

**Structure**
- A `chap(n, title, at)` card opens each chapter, with a yellow wipe.
- A small chapter tag sits bottom-left after the card.
- A short header (`h.a`) names the place or topic.

**Characters and layout**
- Characters: `L()` / `R()` at 600 px tall, with a name label above the head and stickers above that.
- Props and number elements go in the centre.
- Use only the 1920×1080 safe area (40 px margins).

**Numbers**
- Use `cnt()` for every number the narrator says: prefix, suffix, decimals and a short caption.
- Use `bars()` for comparisons and `icons()` for "1 in N".
- Use the pack's ready-made graphic cards where a counter doesn't fit (timelines, receipts, labels).

**Motion and transitions**
- `mv="t,dx,dy,scale"` glides an element aside to make room.
- `**{'in':'left'}` slides an element in from a side.
- Use `out=` to retire elements when the narration moves on.

**Gap fill**
- `fill_gaps.py`-style additions use `TA(phrase, nearTime)`.
- Re-list the gaps until the pacing rules hold.

### 5. Check before rendering
- Render a still of the last frame of every scene with `scripts/capture.js <dir> t1,t2,…`.
- Tile them with `scripts/check_sheet.py`.
- **Look at every tile:** overlaps, text off the frame, circles that miss, stickers hidden behind figures, wrong facing.
- Fix and repeat. Expect two passes.

### 6. Live editor (the user always wants this)
- Copy `engine/index.html` to `editor/index.html`. Change the title and placeholder text, and set the SFX list to the files in `editor/sfx/`.
- Publish it as an Artifact with `capabilities: {db: {}, downloads: true}`.
- It has more than 255 files, so publish in two parts to the same file path: part 1 is the page, JSON, audio, sfx and the first 200 assets; part 2 is the rest.
- What the editor does:
  - live preview with audio and a scene timeline;
  - drag elements and edit any field;
  - add any element type;
  - **Save**: every save is kept as a version, with an optional note;
  - **History**: open, download, CSV edit log, all versions;
  - **Autosave** every 2 minutes, plus a warning before closing with unsaved edits;
  - **Download JSON**.
- After publishing, run `ArtifactData list` on `versions`. It should be empty.

### 7. Render
1. Mix: `scripts/mix.py` puts the voiceover together with every `sfx` element, giving `mix_full.wav`.
2. Choose the scale:
   - **Preview:** `capture.js` with `deviceScaleFactor: 0.5` gives 960×540.
   - **Final:** scale 1 gives 1080p, and `deviceScaleFactor: 2` gives 4K.
3. Run 4 workers in parallel on time ranges (`node capture.js frames 15 <start> <end>`), at about 15–17 fps per machine at 540p and about 8 fps at 4K.
4. Encode: `ffmpeg -framerate 15 -i frames/%06d.jpg -i mix_full.wav -vf "fps=30,format=yuv420p" -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4`
   - For 4K add `-level 5.1`.
   - Make the 1080p by downscaling the 4K with lanczos.
5. The capture server **must send `text/html; charset=utf-8`**, or non-ASCII characters (·, ≈, €) come out garbled.
6. Make sure the stage is exactly 1920×1080 in render mode (`body.render` has no margin and `max-width:none`). An 8 px body margin once produced 1904×1080.
7. Uploads to the user are capped at about 400 MB per file. Send a long 4K as parts cut with `-c copy` on keyframes.

### 8. Deliver and save
- Send the preview first (low quality). Do the final 4K + 1080p only once the user approves.
- Commit the project to the repo (editor, sources, scripts, `PROCESS.md` log). Never commit MP4s or frames.
- Tell the user the editor link, what changed, and anything still pending (for example, archive photos that are still downloading).

## Good judgment calls
- The user's assets are the cast. Never invent characters or restyle them. If a figure is missing, use the mascot or a prop.
- Real copy only. Every number on screen comes from the script. A label may simplify, but it never adds a statistic.
- Real people and brands: storefronts stay blank with the pack's name cards, and real people are "illustrated reenactments".
- When the user says "elements take too long" or "not in sync", check alignment, scene openers and gaps, in that order. The cause last time was empty scene openers, not word timing.
- When the user edits in the editor, read their saved version from the artifact db (`board/meta` → `versions/{v}/chunks/c*`), rebuild `storyboard.json` from it, and render from that. Don't overwrite their edits with the builder.

## Files
- `engine/index.html`: the editor and renderer. Element kinds:
  - figures and images: img, archive, card;
  - text and labels: text, sticker, stamp, bubble;
  - ink marks: arrow, loop, hl, xmark;
  - animated numbers and charts: counter, bars, icons;
  - structure and sound: chapter, sfx.

  Every element can also take `in`, `mv` and `out`.
- `scripts/`: library build, transcription, alignment, capture, check sheets, mix and SFX synthesis.
- `sfx/`: synthesised effects (stamp, ching, crash, ding, pop, swish, whoosh, clang, crack, splash, rewind).
- `examples/`: the Perseus and Buffet storyboard builders, plus the original vox skill for reference.
