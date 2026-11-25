# Ref 01 audio pass — notes (measured; identities UNVERIFIED: no playback available in this environment)
Source: AAC 44.1 kHz stereo, audio starts at container 0.000 s; first video PTS 0.033333 s (subtract for video-relative time).
- VO/dialogue lane: single narrator; speech-band activity from ~0.03 s to ~1489.5 s. 606 pauses ≥ 0.25 s detected (median 0.33 s, longest 6.03 s).
- Music/ambience lane: a continuous low bed is present everywhere, including pauses: 10 ms RMS p10 ≈ −41…−48 dBFS per 10 s window vs VO p90 ≈ −17…−18 dBFS (bed sits ≈ 25–28 dB under VO). Pause spectra are tonal (spectral flatness median 0.004; stable narrow peaks e.g. 215 Hz, 1.36 kHz, 2.6 kHz) → probable soft music bed, not room tone. Level steady across chapters (no obvious ducking); fades out over the final ~1 s (−52 → −71 dBFS).
- One-shot SFX lane: 968 spectral-flux onset candidates logged (afeat01.json); most coincide with VO consonants. Candidates inside VO pauses are listed in audio_cues.csv with verification=unverified.

## One-shot SFX lane — result (measured, 2026-11-25)
- 678 broadband transients were found inside VO pauses (flux z ≥ 6 above a 2 s running median). These are logged in audio_cues.csv.
- **They are not synchronised to the picture**: 13.4 % fall within ±2 frames of a visual event, against 12.8 % for random times drawn from the same pauses. That is chance level.
- Conclusion: the reference uses **no systematic one-shot sound effects on pops, cuts or icon entrances**. The soundtrack is narrator + soft music bed; visual hits are carried by the VO rhythm alone. The transients are most likely breaths, mouth clicks or music-bed attacks (identity unverified without playback).
- Implication for our videos: keep SFX extremely sparse (a few signature moments per video at most), never one per element.
