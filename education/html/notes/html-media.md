# HTML Media

How to put images, audio, video, and embedded content on a page.

## `<img>` — images
Shows a picture. It's a self-closing tag with two key attributes: `src` (the file) and `alt` (text description).

```html
<img src="cat.jpg" alt="A sleeping orange cat" />
```
- `src` — path or URL to the image.
- `alt` — see below, it's important.
- You can add `width` / `height` too.

## `alt` text
The `alt` attribute is a short text description of the image. It matters because:
1. **Screen readers** read it aloud for blind users.
2. It shows if the image **fails to load**.
3. It helps **SEO** (search engines read it).

```html
<img src="logo.png" alt="Company logo" />
```
If an image is purely decorative, use an empty alt so screen readers skip it:
```html
<img src="divider.png" alt="" />
```

## `<audio>`
Plays sound files. Add `controls` so the user gets a play/pause bar.
```html
<audio controls>
  <source src="song.mp3" type="audio/mpeg" />
  Your browser does not support audio.
</audio>
```
The text inside shows only if audio isn't supported.

## `<video>`
Plays video. Similar to audio — add `controls`, and you can set `width`.
```html
<video controls width="480">
  <source src="clip.mp4" type="video/mp4" />
  Your browser does not support video.
</video>
```
Useful extras: `autoplay`, `muted`, `loop`, `poster="thumbnail.jpg"`.

## `<iframe>`
Embeds another web page inside yours — commonly a YouTube video or a Google Map.
```html
<iframe
  src="https://www.youtube.com/embed/VIDEO_ID"
  width="560"
  height="315"
  title="YouTube video"
></iframe>
```
Always add a `title` for accessibility. Be careful embedding sites you don't trust.

## `<figure>` and `<figcaption>`
`<figure>` wraps a piece of media (usually an image) that has a caption. `<figcaption>` is the caption text. Together they connect the image and its description semantically.

```html
<figure>
  <img src="chart.png" alt="Sales rising from 2020 to 2026" />
  <figcaption>Sales grew steadily over six years.</figcaption>
</figure>
```
Use this instead of just putting a `<p>` under an image — it tells browsers and screen readers "this caption belongs to this image."

---

### Quick review
- `<img>` needs `src` **and** `alt`. Empty `alt=""` for decorative images.
- `<audio>` and `<video>` need `controls` for a play bar; use `<source>` inside.
- `<iframe>` embeds another page (YouTube, maps) — give it a `title`.
- `<figure>` + `<figcaption>` = media with a proper caption.
