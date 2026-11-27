# 14 reference clips: what they add

The clips came from Claude_Animation_Reference_Clips.zip.
- **Clips 01–07:** from "History's Strangest War Tactics Explained", a video we hadn't seen before.
- **Clips 08–14:** from "How Every Feared Waffen-SS General Died", already analysed in `../02`.

**Method:** every distinct frame was extracted with `mpdecimate` (81, 20, 20, 68, 71, 22, 21, 142, 30, 132, 108, 127, 67 and 46 frames). They were laid out as timestamped sheets with `sheet2.py`; samples are in this folder.

## Clips 08–14 (source B)
These confirm the v6 scene grammar already in `../clips_deep`:
- one waist-up character at the left;
- touching clusters;
- small labels;
- two-character staging;
- the courtroom, bars and armchair escalation;
- the roster zoom.

## New from clips 01–07 (source A): chapter framing, built into v7

### 1. Chapter index
- The grid is made of **isolated illustrated objects**, with a bold label under each. There are no photo frames.
- Hold the grid about 6 frames, then push into the chosen tile over about 14 frames, then hard-cut to the chapter (clip 01 #1–55).

### 2. Chapter title
- A bold, all-caps, comic-style title sits at the top centre for the whole chapter, about 80 px tall at 1080p (clip 01 #55 onward; `title_crop.png`).
- A small copy of the chapter's object sits in the **top-right corner**, about 130×77 px at 1080p.

### 3. Date cards
- Before a dated story, a big centred date appears alone on the canvas for about 1.3 s ("In 266 BC" at clip 01 #74, "In 1942" at clip 05 #71).
- The scene then builds, and the date stays as a small sub-header.

### 4. Make room by compacting
- When a new sub-topic starts, the earlier group shrinks into the top-left corner and the new content fills the free area (clip 01 #58, #64, #72).
- Our shrink-to-fit re-pack does this.

### 5. Scenes without a character
- Source A often runs a whole beat with no anchor character, just icons, maps and archive images in labelled clusters.
- A character enters when the narration is about a person (clip 02 #1–10, clip 07).

### 6. Labels sit under items in source A
- In source A, labels sit **under** the item ("Chremonidean War", "Athens"). In source B they sit above.
- We kept them above, as in source B, because the anchor-character scenes come from B.

## Not copied
The real tactics and subjects in these clips are not used; only the visual grammar is.
