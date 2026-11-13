# Calculus course: production rules

This repository holds an automated video course covering Calculus 1, 2 and 3 for US students.
It follows the topic order of the OpenStax Calculus volumes. All explanations, examples, problems
and figures are original. Never copy text, examples, exercises or figures from OpenStax or any
other textbook: the OpenStax licence is non-commercial.

## Layout
- `CURRICULUM.csv`: every section, with a status per level (`todo`, `done`). Section titles were
  written from memory; check each against the book's table of contents before building it.
- `engine/render.py`: shared drawing helpers (`Cues`, `T`, `fade`, `ease`, colours) plus the first
  lesson (Volume 1, 3.1, Level 1).
- `lessons/`: one animation file and one narration file per lesson, named `v<volume>_<section>_L<level>`.
- `vo/`: narration audio and character-level timings from the voice model.
- `videos/`: finished lessons.

## The three levels
1. The idea (2-4 min): the picture and the intuition, almost no algebra. One or two quick checks.
2. The course (10-12 min): definition, rules, worked examples, common mistakes. Three to five practice problems.
3. The deep dive (10-15 min): proofs, harder problems, links to other topics. Three to five practice problems.

## Every lesson
- Order: why it matters, the picture, the definition, worked examples, common mistakes, practice.
- Practice format: show the problem, the narrator says to pause and try it, then work the full solution step by step.
- Narration is split into segments. Each on-screen element appears at the moment its words are spoken,
  using the character timings in `vo/*.json` (see `Cues`). Never time animation by guesswork.
- 1920x1080, 24 fps, one encoded file per segment, joined with the concat demuxer and `-c copy`.

## Accuracy (there is no human reviewer)
- Recompute every number, derivative, integral and limit shown or spoken with sympy before rendering.
  If a check fails, fix the script; do not render.
- Draw two still frames per segment and look at them before the full render. Fix overlaps and cut-off text.
- Narration text and on-screen text must state the same values.

## Secrets
This repository is public. Never commit API keys. The voice model key is supplied outside the repository.
