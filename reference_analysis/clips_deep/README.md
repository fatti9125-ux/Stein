# Clips 01–05: what our video was getting wrong

This is an analysis of the five reference clips: Photos & Icons, Character Reactions, Courtroom, Maps & Archives, and Battle Layers.
- **Frames:** every distinct frame was extracted with `mpdecimate`: 139, 47, 124, 47 and 58 frames.
- **Sheets:** the frames were laid out as timestamped contact sheets (`c0X_sheetN.jpg`, built with `sheet.py`).
- **Comparison:** the sheets were compared with 16 frames from our v5 render.
- **Metric:** `occ.py` measures how much of the frame is used and how far apart the separate groups of elements are.

## Measurements

| Metric | Refs: 01 | 02 | 03 | 04 | 05 | Our v5 |
|---|---|---|---|---|---|---|
| Separate element groups on screen (median) | 2 | 2 | 3 | 2 | 3 | **6** |
| Distance needed to merge the groups (px at 1080p, median) | 24 | 18 | 27 | 36 | 81 | **90** |
| Frame used, below the header (median) | 0.22 | 0.33 | 0.16 | 0.45 | 0.30 | 0.23 |

**What the numbers mean:**
- The reference scenes are **one or two touching clusters**.
- Our v5 scattered about six islands with roughly 90 px of empty blue between them.
- The amount of frame used was similar, so the problem was **arrangement, not quantity**.

## Text size (measured in clip 05)

| Text | Size at 720p | Size at 1080p |
|---|---|---|
| Header ("Gustav Krukenberg") | ≈ 24 px | ≈ 36 px |
| Labels ("~54 tanks / by french SS", "Out of 108 / destroyed tanks") | ≈ 26 px, two lines | ≈ 39 px |

**Numbers never appear as giant type.** They are labels the same size as all the other labels, sitting directly above their picture.

## Rules (built into `build_board_v6.py`)

### 1. The anchor is a person from the story
- The anchor is the person the story is about, as a big waist-up figure at the left, cropped by the bottom of the frame.
- There is no mascot or narrator animal. **Inspector Crumb (the mouse) was removed** at the user's request.
- In scenes that only explain, the anchor is the most relevant human: the manager, chef, director, cashier, a diner or Gary.

### 2. Elements form a cluster that touches the anchor
- The first element sits right beside the anchor's head and shoulder, near the top.
- Each next element takes the first free spot reading left to right, then the next row down, **touching** its neighbours (gap of about 14 px).
- Feathered photos may be overlapped at their edges.
- Evidence: clip 01 #21–33 (portrait → symbols → photo → medal → shield → map), clip 04 #2–10, and clip 05 #1–16 and #21–32.

### 3. Element sizes
| Element | Size at 1080p |
|---|---|
| Icons and props | about 230–470 px tall |
| Photos and maps | about 0.35–0.4 of the frame width |
| Second characters | the same scale as the anchor |

### 4. Labels go directly above their picture
- Labels are one or two lines, about 39 px.
- A number that belongs to a picture becomes that picture's label, appearing when it is spoken ("Held soviets / for 48 hours" over a clock).

### 5. Earlier elements hold still
They move only when the newcomer doesn't fit. Then the whole group shrinks and re-packs in about 8 frames. Evidence: clip 05 #24, where the clock shrinks and drops when the tank arrives; and clip 01 #53–56, where the SS logo leaves and the shield moves up.

### 6. The second character stands near the anchor and faces them
- Content can sit in the gap between the two characters or above their heads (clip 05 #36–44, the medal between two men).

### 7. Only labels, maps and bubbles carry text
- Text is black hand lettering.
- Red is kept for X marks, circles and arrows.

## What we can't match with this asset pack
- **Archive photos:** the references use real grayscale photos. Wikimedia still returns HTTP 429, so the archive photo spots use the pack's illustrated backgrounds.
- **Character reactions:** the references swap between many poses of the same character. The pack has only 1–4 poses for each person, so swaps are rarer.
- **Physical interaction:** the references show hand-holding, pinning a medal and carrying a suitcase. We can only place drawings next to each other.
