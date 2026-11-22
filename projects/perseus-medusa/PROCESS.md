# Production log: Perseus & Medusa

This is a record of how the video was made, from the reference study to the final 4K render, with the decision behind each step. The files mentioned are in this folder.

## 1. Style research
- **Studied two kinds of reference:**
  - five cartoon-history clips: character reactions, scene builds, courtroom cuts, maps and archives, battle layers;
  - two Vox-style editorial references.
- **Target style:** a hybrid of the two.
  - The sky-blue background and hand-drawn figures come from the cartoon clips.
  - Vox-style graphic devices sit on top: torn paper cards, yellow highlighter, ink circles and arrows, red stamps, archive photo cards and typewriter captions.
- **Style frames:** `process/style_frames/`, made on 2026-11-20.

## 2. Assets
- **Source:** the original Perseus & Medusa asset pack in `source/asset_pack/`. It has 166 character images, plus props, effects and backgrounds.
- **Facing direction:** every character image was tagged with the way it faces (left, right or front), in `data/facing.json`. The editor uses this to turn characters toward each other automatically.
- **Archive images:** public-domain museum images went into `source/archive_images/`, with their sources listed in `meta.json`. They include Caravaggio's *Medusa* (1597) and Greek vase paintings.
- **Check sheets:** contact sheets of all the assets, in `process/check_sheets/chars_*.jpg` and `sheet_assets.jpg`.

## 3. Voiceover timing
- The 18-minute voiceover was transcribed to word level with timestamps, in `data/words_raw.json`. The scripts are in `pipeline/transcription/`.
- Every element on screen is timed to the spoken word it illustrates.

## 4. First sample (1 minute) and feedback
- **Sample 1** was rendered from the prototype renderer in `pipeline/sample_renderer/`.
- **Feedback on sample 1, applied in sample 2:**
  - removed the white checkered paper;
  - gave every element its own space, with no crowding;
  - added sound effects only on key hits;
  - added archive images.
- **Feedback on sample 2:**
  - moved the red circle onto Medusa's full face;
  - made characters always face each other.

## 5. Full storyboard
- **`pipeline/build_board.py`** builds the full storyboard: 55 scenes, 579 elements and 52 sound-effect cues.
- **Layout rules:**
  - the main character stands on the left;
  - the second character stands on the right;
  - props go in the centre;
  - notes go in the top band;
  - labels sit above figures.
- **Overlap checks:** check sheets were rendered at many timestamps to look for overlaps (`process/check_sheets/chk3_*`), and every overlap found was fixed.

## 6. Live editor
- **`editor/index.html`** is a browser editor with live preview and a timeline with scene markers. In it you can:
  - click the transcript to jump to a moment;
  - drag elements on the stage;
  - edit any property;
  - add or delete elements and scenes.
- **Version history** was added on 2026-11-22:
  - every save is kept, with an optional note;
  - there is a 2-minute autosave;
  - the edit log can be downloaded as CSV, and all versions as JSON.
- **Previous version:** the editor before version history is kept in `process/editor_v1_before_history.html`.

## 7. Final render
- **Mixing:** `pipeline/mix_full.py` mixes the voiceover with every sound-effect cue in the storyboard.
- **Frames:**
  - Frames are rendered by the editor's own engine in headless Chromium.
  - They are drawn at 15 fps ("on twos", for the hand-made feel), with a frame-by-frame line "boil".
  - That makes 16,140 frames in total.
- **Encoding:** the frames were encoded at 30 fps to H.264.
- **Outputs (2026-11-20):**
  - `Perseus_full_4K.mp4`: 3840×2160, 17:56;
  - `Perseus_full_1080p.mp4`: 1920×1080, downscaled from the 4K.

## Your edits
Add your own entries below as you edit. Download the edit log from the editor's History panel, and save the storyboard versions into `storyboard_versions/`.

| Date | What changed | Version file |
|---|---|---|
| 2026-11-20 | Claude's first full draft | `storyboard_versions/v1_claude_draft_2026-11-20.json` |
