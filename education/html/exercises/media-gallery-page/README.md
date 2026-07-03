# Exercise: Media Gallery Page

## Goal
Build an HTML-only page that displays images with captions, plus audio and video
using placeholder media files.

## Concepts practiced
- `<img>` with descriptive `alt` text and `width`
- `<figure>` and `<figcaption>` to pair an image with its caption
- `<audio>` with `controls` and a `<source>`
- `<video>` with `controls`, `poster`, and a `<source>`
- Fallback text inside audio/video for unsupported browsers
- Organizing media into `<section>`s with headings

## Files included
- `index.html` — the media gallery page
- `README.md` — this file

> Note: the `images/` and `media/` paths are placeholders. The page structure is
> correct; add real files with those names to see them load.

## What I learned
- Every meaningful image needs `alt` text for screen readers and broken-image cases.
- `<figure>` + `<figcaption>` semantically connect an image and its caption, which is
  better than a plain paragraph underneath.
- `controls` is what shows the play/pause bar on audio and video.
- `<source>` lets me specify the file and its type, with fallback text inside.
- `poster` sets the thumbnail shown before a video plays.
