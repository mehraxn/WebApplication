# `object-fit` in CSS

## What `object-fit` is

`object-fit` is a CSS property that controls how the content of a replaced element is resized inside its box.

The most common element is the HTML `img` tag, but `object-fit` can also be used with other replaced elements such as

 `img`
 `video`
 `canvas` in some rendering contexts
 other replaced content

In everyday web development, you will mostly use it with images.

---

## The main idea

An image has

 its own natural size and ratio
 the box size you give it in CSS

These two sizes are often different.

Example

 image natural size `800 × 400`
 CSS box size `300 × 300`

Now a question appears

How should the image fit inside that `300 × 300` box

That is exactly what `object-fit` controls.

---

## Why `object-fit` is needed

Without `object-fit`, when you force both width and height on an image, the browser may stretch or squeeze the image.

Example

```css
img {
  width 300px;
  height 300px;
}
```

If the original image is not square, it can look distorted.

With `object-fit`, you can control that behavior more intelligently.

---

## Important requirement

`object-fit` becomes meaningful when the element has a box to fit into, usually through `width` and `height`.

Example

```css
img {
  width 300px;
  height 200px;
  object-fit cover;
}
```

If no size is constrained, you may not notice much effect.

---

## Syntax

```css
object-fit fill;
object-fit contain;
object-fit cover;
object-fit none;
object-fit scale-down;
```

---

# All `object-fit` values

## 1. `object-fit fill`

This is the default value.

```css
img {
  object-fit fill;
}
```

### What it does

 The content is resized to fill the entire box.
 It does not preserve the original aspect ratio.
 The image may look stretched or squeezed.

### Result

 whole box is covered
 no cropping
 distortion can happen

### Example

If the image is wide but the box is square, the image will be forced into that square shape.

### When to use it

Usually not preferred for photographs, because it can distort them.

It can sometimes be acceptable when distortion does not matter much.

---

## 2. `object-fit contain`

```css
img {
  object-fit contain;
}
```

### What it does

 The entire image is made visible inside the box.
 The original aspect ratio is preserved.
 The image is scaled up or down as needed.
 Empty space may remain in the box.

### Result

 whole image is visible
 no cropping
 no distortion
 empty space may appear

### Example

Suppose

 image `400 × 200`
 box `200 × 200`

With `contain`, the image becomes `200 × 100`.

So

 the whole image is visible
 the box is not fully covered
 there will be empty space above and below

### When to use it

Use `contain` when showing the entire image is more important than filling the box.

Common examples

 product previews
 logos
 image galleries where cropping is not acceptable
 screenshots

---

## 3. `object-fit cover`

```css
img {
  object-fit cover;
}
```

### What it does

 The image keeps its original aspect ratio.
 The image is resized so the entire box is covered.
 If necessary, some part of the image is cropped.

### Result

 whole box is covered
 no distortion
 cropping may happen

### Example

Suppose

 image `400 × 200`
 box `200 × 200`

If we resized the image to `200 × 100`, the whole image would be visible, but the box would not be fully covered.

So `cover` does not choose that.

Instead, it scales the image so that the box is fully covered. Then any extra part is cropped.

### Key rule

`cover` cares about the box being fully covered, not about the entire image staying visible.

### When to use it

Use `cover` when filling the box matters more than preserving the full image.

Common examples

 profile photos
 card thumbnails
 hero banners
 post previews
 image sections with fixed dimensions

---

## 4. `object-fit none`

```css
img {
  object-fit none;
}
```

### What it does

 The content is not resized to fit the box.
 The image keeps its natural size.
 If the image is larger than the box, it overflows or gets clipped depending on overflow behavior.

### Result

 no scaling
 no ratio change
 image may overflow or be cropped by the box

### Example

Suppose

 image `500 × 300`
 box `200 × 200`

With `none`, the image still behaves like `500 × 300` content inside the `200 × 200` box.

So only part of it may be visible.

### When to use it

Use `none` when you do not want the browser to resize the image content automatically.

This is less common in normal responsive layouts.

---

## 5. `object-fit scale-down`

```css
img {
  object-fit scale-down;
}
```

### What it does

This value compares two possibilities

 `none`
 `contain`

Then it uses whichever gives a smaller rendered object.

### Simpler meaning

 if the image is already small enough, it may stay at its natural size
 if it is too large, it scales down like `contain`

### Result

 no distortion
 no cropping
 may keep natural size or scale down

### Example 1

If the image is small and already fits inside the box, it may remain unchanged.

### Example 2

If the image is too large for the box, it will shrink like `contain`.

### When to use it

Use `scale-down` when you want

 the image not to become larger unnecessarily
 the image to shrink only when needed

---

# Summary table

 Value         Keeps ratio  Covers whole box  Shows whole image             Crops  Distorts 
 ------------  ------------  ----------------  -----------------  ----------------  -------- 
 `fill`        No                          Yes                 Yes                 No        Yes 
 `contain`     Yes                  Not always                 Yes                 No         No 
 `cover`       Yes                         Yes          Not always                Yes         No 
 `none`        Yes             Not necessarily     Not necessarily  Possible clipping         No 
 `scale-down`  Yes                  Not always       Yes if fitted                 No         No 

---

# Difference between `contain` and `cover`

This is the most important comparison.

## `contain`

Says

Show the whole image, even if empty space remains.

## `cover`

Says

Fill the whole box, even if part of the image is cropped.

### Easy memory trick

 `contain` → protect the whole image
 `cover` → protect the whole box

---

# How scaling and cropping happen in `cover`

A common question is

When does the browser scale down, and when does it crop

Answer

With `cover`, the browser first resizes the image so the box becomes fully covered while preserving the image ratio.

After resizing

 if extra content remains outside the box, that extra part is cropped

So the process is

1. preserve aspect ratio
2. resize until the box is fully covered
3. crop overflow

### Scale up

Happens when the image is too small for the box.

### Scale down

Happens when the image is too large for the box.

### Crop

Happens when, after resizing to cover the box, one side becomes larger than the box.

---

# `object-fit` vs `object-position`

These two properties are often used together.

## `object-fit`

Controls

How the image is resized inside the box

## `object-position`

Controls

Which part of the image stays visible inside the box

Example

```css
img {
  width 300px;
  height 200px;
  object-fit cover;
  object-position right;
}
```

Meaning

 fill the box
 keep ratio
 crop overflow if needed
 keep more of the right side visible

---

# Full examples

## Example 1 Distorted image

```css
img {
  width 300px;
  height 300px;
  object-fit fill;
}
```

The image fills the square, but distortion may happen.

## Example 2 Entire image visible

```css
img {
  width 300px;
  height 300px;
  object-fit contain;
}
```

The full image is visible, but empty space may appear.

## Example 3 Best for thumbnails

```css
img {
  width 300px;
  height 300px;
  object-fit cover;
}
```

The image fills the square and keeps its ratio, but some part may be cropped.

## Example 4 Natural size only

```css
img {
  width 300px;
  height 300px;
  object-fit none;
}
```

The image content is not resized to fit that box.

## Example 5 Shrink only if needed

```css
img {
  width 300px;
  height 300px;
  object-fit scale-down;
}
```

The image stays natural if it already fits, otherwise it shrinks.

---

# Practical use cases

## Use `cover` for

 avatar images
 YouTube thumbnails
 blog post cards
 hero image sections
 portfolio cards

## Use `contain` for

 logos
 screenshots
 product photos where every part matters
 diagrams

## Use `fill` for

 rare cases where exact box fill matters more than distortion

## Use `none` for

 advanced layouts where you want the natural image size

## Use `scale-down` for

 interfaces where images should not enlarge unnecessarily

---

# Common mistake

A common mistake is thinking `object-fit` works like this

 on any element
 without giving the element a meaningful box size

But usually, `object-fit` is useful only when the element has a clear box, especially fixed or constrained dimensions.

---

# Very important final idea

`object-fit` answers this question

When the image and the box have different shapes or sizes, what should the browser prioritize

Different values give different priorities

 `fill` → fill the box, even with distortion
 `contain` → show the whole image
 `cover` → cover the whole box
 `none` → do not resize the content
 `scale-down` → shrink only when necessary

---

# Short final summary

`object-fit` controls how image content fits inside its CSS box.

The most important values are

 `contain` → whole image visible
 `cover` → whole box covered
 `fill` → default, may distort
 `none` → no resizing
 `scale-down` → shrink only if needed

For most real web layouts

 use `cover` for thumbnails and cards
 use `contain` when cropping is not acceptable
