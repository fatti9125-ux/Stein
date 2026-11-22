# Perseus & Medusa: animated explainer (17:56)

This is the full project for the Perseus & Medusa video. It holds the editable storyboard, all art and audio sources, the render pipeline, and a record of how the video was made. For a dated log of each step, see [PROCESS.md](PROCESS.md).

## Live editor

**Online editor:** https://claude.ai/artifact/EJmbPKVrAXmvpdnxguNdZg (private to the owner)

- **Save changes** stores your edits and keeps every save as a separate version.
- Type a note in "What did you change?" before saving. The note appears in History and in the edit log.
- While there are unsaved edits, the editor **autosaves every 2 minutes**. It also warns you before you close the tab with unsaved work.
- **History** lists every saved version. From there you can:
  - **Open** any version to go back to it;
  - **Download** a version as JSON;
  - **Download edit log (CSV)**: one row per save, with time, note and items added, removed or edited;
  - **Download all versions (JSON)**: every version in one file.
- **Download JSON** saves the current storyboard to your computer.

The same editor code also renders the final video, so what you see in the preview is what gets rendered.

## Folders

| Folder | What's in it |
|---|---|
| `editor/` | The live editor (`index.html`), the storyboard (`storyboard.json`), the asset library (`library.json`), the transcript, the voiceover (`vo.mp3`), sound effects and 272 web-optimised assets. Open `index.html` through any local web server to edit offline. |
| `storyboard_versions/` | Snapshots of the storyboard. Put downloaded versions here. |
| `source/asset_pack/` | The original Perseus & Medusa asset pack (characters, props, effects, backgrounds, plus CSV indexes). |
| `source/archive_images/` | Public-domain archive images (Caravaggio's *Medusa* and others). `meta.json` lists their sources and licences. |
| `source/sfx_wav/` | Full-quality sound effects, synthesised by `pipeline/sfx.py`. |
| `data/` | Word-level transcript (`words_raw.json`), timed lines, and the facing direction of each character. |
| `pipeline/` | Scripts that build, render and mix the video. |
| `process/` | Style frames, check sheets and screenshots from each stage of production. |

## Re-render the video

Run every command from this folder (`projects/perseus-medusa`). The scripts need Node with Playwright and Chromium, Python 3 with numpy and scipy, and ffmpeg.

1. Optional: use an edited storyboard. Download it from the editor and copy it over `editor/storyboard.json`.

2. Mix the voiceover with the sound effects (writes `mix_full.wav`):

   ```bash
   python3 pipeline/mix_full.py
   ```

3. Render the frames:
   - 1080p: `node pipeline/editor_capture.js frames 15`
   - 4K: `node pipeline/editor_capture4k.js frames4k 15`

   To split the work across several processes, add a start and end time in seconds: `... frames4k 15 0 270`.

4. Encode the frames into an MP4:

   ```bash
   ffmpeg -framerate 15 -i frames4k/%06d.jpg -i mix_full.wav -vf "fps=30,format=yuv420p" -c:v libx264 -preset faster -crf 18 -profile:v high -level 5.1 -c:a aac -b:a 192k -shortest -movflags +faststart Perseus_full_4K.mp4
   ```

The finished MP4s are too large for git, so they are not in this repo. Keep your downloaded copies.
