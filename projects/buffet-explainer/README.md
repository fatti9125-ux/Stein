# Why Buffets Don't Lose Money When You Eat 5 Plates (14:04)

**Live editor:** https://claude.ai/artifact/4qauAwpcCygiUV71EvwTFy (private to the owner). It has Save, History, autosave and Download, the same as Perseus.

This project follows the workflow in `.claude/skills/hand-drawn-vox-explainer/SKILL.md`.

## Folders

| Folder | What's in it |
|---|---|
| `editor/` | The live editor and renderer, the storyboard, the asset library, the voiceover and the sound effects. |
| `source/` | The original asset pack, the script and the full-quality sound effects. |
| `data/` | The recognised words, plus the script aligned to the voiceover. `script_words_fa.json` has the forced-aligned word times. |
| `pipeline/` | The storyboard builder (`build_board.py` + `fill_gaps.py`), the aligners, and the capture and mix scripts. |

## Rebuild and re-render

Run these from `pipeline/`, with the data files and `editor/` alongside:

1. `python3 build_board_v3.py`
2. `python3 mix_full.py`
3. `node capture_lo.js frames 15 0 844` (preview) or `node editor_capture.js frames 15 0 844` (1080p)
4. Encode with ffmpeg, as described in the skill file.

The finished MP4s are not in git. Keep your downloaded copies.
