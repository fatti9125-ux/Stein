# Ref 01 — index-grid → chapter transition (measured)

Method: ORB features + RANSAC similarity transform, chained frame to frame from the last held grid frame; scale = grid magnification; centre = grid point (normalised) shown at frame centre. Evidence: evidence/transitions/trans01_*.jpg, evidence/C03/strips_c03.jpg.

All 22 chapter entries use the same structure (exact frames in chapters.json):
1. Hard cut from the last chapter state to the full 24-tile index grid (6 x 4 tiles, each a feathered archive image + 1–2 line title). Grid holds 6 frames (0.2 s).
2. Zoom into the selected tile over 14 frames (0.47 s): pure uniform scale + translation (no rotation), grid moves as one rigid group. Scale grows exponentially (≈ ×1.10–1.12 per frame) and eases out over the last 4 frames.
3. Enlarged tile = title card (image + big title, neighbour tiles' edges still visible at the frame edges) holds ≈ 40–45 frames (≈ 1.4 s).
4. Hard cut to the chapter canvas: the same image re-used small at left, title removed, header (chapter name + date) appears.

| frame offset | C03 scale | C03 centre (x,y) | C13 scale | C13 centre (x,y) |
|---|---|---|---|---|
| +0 | 1.106 | .496,.454 | 1.102 | .469,.516 |
| +1 | 1.226 | .491,.411 | 1.219 | .440,.530 |
| +2 | 1.364 | .488,.371 | 1.352 | .414,.543 |
| +3 | 1.522 | .484,.334 | 1.352 (repeated frame) | .414,.543 |
| +4 | 1.704 | .481,.301 | 1.504 | .389,.556 |
| +5 | 1.909 | .478,.270 | 1.675 | .366,.567 |
| +6 | 2.144 | .475,.242 | 1.868 | .346,.577 |
| +7 | 2.407 | .473,.218 | 2.084 | .327,.586 |
| +8 | 2.693 | .471,.196 | 2.324 | .311,.595 |
| +9 | 2.999 | .469,.178 | 2.584 | .297,.602 |
| +10 | 3.312 | .468,.163 | 2.855 | .284,.608 |
| +11 | 3.613 | .467,.150 | 3.132 | .274,.613 |
| +12 | 3.876 | .466,.141 | 3.390 | .266,.617 |
| +13 | 4.065 (settle) | .465,.139 | 3.614 | .260,.620 |
| +14 | — | — | 3.779 (settle) | .256,.625 |

Implementation recipe: keyframe scale 1 → ~3.8–4.1 with an exponential ease (constant log-scale velocity, last ~30 % eased out), keyframe position so the target tile's centre ends at frame centre; duration 14 frames @30 fps. C13 contains one duplicated frame inside the move (+2/+3), i.e. a render hiccup in the source, not a style choice.
