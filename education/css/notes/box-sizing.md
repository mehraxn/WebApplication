# CSS `box-sizing` Explained

## The code

```css
 {
    box-sizing border-box;
}
```

This is a very common CSS rule.

It means

 Apply `box-sizing border-box;` to every HTML element on the page.

The `` selector is called the universal selector.

It selects all elements, for example

```html
body
header
div
p
img
button
```

So this rule tells the browser

```css
Every element should use border-box sizing.
```

---

# What is `box-sizing`

In CSS, every HTML element is treated like a box.

A box can have

1. Content
2. Padding
3. Border
4. Margin

Example

```css
.card {
    width 300px;
    padding 20px;
    border 5px solid black;
    margin 10px;
}
```

The important question is

 When we write `width 300px`, what exactly is 300px

Does it mean only the content is 300px

Or does it mean the whole box, including padding and border, is 300px

That is what `box-sizing` controls.

---

# The two main values of `box-sizing`

The two main values are

```css
box-sizing content-box;
box-sizing border-box;
```

These are the most important ones.

---

# 1. `content-box`

```css
box-sizing content-box;
```

This is the default value in CSS.

That means if you do not write `box-sizing`, the browser normally uses `content-box`.

With `content-box`, the width and height apply only to the content area.

Padding and border are added outside the width and height.

## Example

```css
.box {
    width 300px;
    padding 20px;
    border 5px solid black;
    box-sizing content-box;
}
```

Here, the content width is 300px.

But the real visible width is bigger.

Calculation

```text
content width = 300px
left padding = 20px
right padding = 20px
left border = 5px
right border = 5px
```

So the total width becomes

```text
300px + 20px + 20px + 5px + 5px = 350px
```

So even though we wrote

```css
width 300px;
```

The real box becomes

```text
350px wide
```

## Why can `content-box` be confusing

Because the final size of the element becomes bigger than the width you wrote.

For example, this can break layouts

```css
.left-box {
    width 50%;
    padding 20px;
}

.right-box {
    width 50%;
    padding 20px;
}
```

You may expect the two boxes to fit beside each other.

But with `content-box`, the padding is added after the width.

So the real size may become more than 100% total, and the layout can break.

---

# 2. `border-box`

```css
box-sizing border-box;
```

With `border-box`, the width and height include

1. Content
2. Padding
3. Border

So when you write

```css
width 300px;
```

The whole visible box will be 300px wide.

Padding and border are included inside that 300px.

## Example

```css
.box {
    width 300px;
    padding 20px;
    border 5px solid black;
    box-sizing border-box;
}
```

Now the total visible width is exactly

```text
300px
```

The browser calculates the content area automatically.

Calculation

```text
total width = 300px
left padding = 20px
right padding = 20px
left border = 5px
right border = 5px
```

So the content width becomes

```text
300px - 20px - 20px - 5px - 5px = 250px
```

So the full box stays 300px wide.

The content area becomes smaller, but the layout is easier to control.

---

# Main difference between `content-box` and `border-box`

## `content-box`

```css
width 300px;
padding 20px;
border 5px solid black;
box-sizing content-box;
```

Result

```text
Real width = 350px
```

The width only controls the content.

Padding and border are added outside.

---

## `border-box`

```css
width 300px;
padding 20px;
border 5px solid black;
box-sizing border-box;
```

Result

```text
Real width = 300px
```

The width controls the whole visible box.

Padding and border are included inside.

---

# Why do many developers use this rule

```css
 {
    box-sizing border-box;
}
```

Because it makes layouts easier.

When we write

```css
width 300px;
```

we usually expect the whole box to be 300px wide.

`border-box` makes CSS behave more like that expectation.

It helps avoid unexpected layout problems caused by padding and borders.

---

# A better common version

Many developers use this version

```css
html {
    box-sizing border-box;
}

,
before,
after {
    box-sizing inherit;
}
```

This means

```css
html {
    box-sizing border-box;
}
```

The main HTML document uses `border-box`.

Then

```css
,
before,
after {
    box-sizing inherit;
}
```

means all elements, and their pseudo-elements, inherit the same `box-sizing` value.

`before` and `after` are special CSS pseudo-elements that can create extra content before or after an element.

This version is useful because it includes normal elements and pseudo-elements too.

---

# Other possible values of `box-sizing`

The main real values are

```css
box-sizing content-box;
box-sizing border-box;
```

But CSS properties can also use global values.

These global values are not special only to `box-sizing`.

They can be used with many CSS properties.

---

# 3. `inherit`

```css
box-sizing inherit;
```

This means

 Use the same `box-sizing` value as the parent element.

Example

```css
.parent {
    box-sizing border-box;
}

.child {
    box-sizing inherit;
}
```

Here, `.child` will also use `border-box` because its parent uses `border-box`.

This is useful when you want child elements to follow the same rule as their parent.

---

# 4. `initial`

```css
box-sizing initial;
```

This means

 Reset `box-sizing` to its default CSS value.

The default value of `box-sizing` is

```css
content-box
```

So this

```css
box-sizing initial;
```

is similar to

```css
box-sizing content-box;
```

---

# 5. `unset`

```css
box-sizing unset;
```

This means

 Remove the current value and behave like the default rule for this property.

For `box-sizing`, `unset` usually behaves like `initial` because `box-sizing` is not naturally inherited.

So this usually becomes

```css
box-sizing content-box;
```

---

# 6. `revert`

```css
box-sizing revert;
```

This means

 Go back to the value that would come from the browser or previous CSS origin.

In simple words, it tries to undo your custom CSS and return closer to the browser's normal style.

For most beginner-level work, you do not need this often.

---

# 7. `revert-layer`

```css
box-sizing revert-layer;
```

This is related to CSS cascade layers.

It means

 Revert the value only inside the current CSS layer.

This is an advanced CSS feature.

You usually do not need it when learning basic CSS layouts.

---

# Old or uncommon value `padding-box`

You may see this value somewhere

```css
box-sizing padding-box;
```

This value is not commonly used today.

It was supported in some older browser situations, but it is not part of normal modern CSS usage.

With `padding-box`, the width would include the content and padding, but not the border.

Conceptually

```text
width = content + padding
border is added outside
```

But for normal modern web development, you should mainly use

```css
content-box
border-box
```

Especially

```css
border-box
```

---

# Simple visual idea

Imagine this CSS

```css
.box {
    width 300px;
    padding 20px;
    border 5px solid black;
}
```

## With `content-box`

```text
[ border [ padding [ content = 300px ] padding ] border ]

Total width = 350px
```

## With `border-box`

```text
[ border [ padding [ content ] padding ] border ] = 300px total

Total width = 300px
```

---

# Does margin count inside `box-sizing`

No.

This is very important.

`box-sizing` affects content, padding, and border.

It does not include margin.

Example

```css
.box {
    width 300px;
    padding 20px;
    border 5px solid black;
    margin 30px;
    box-sizing border-box;
}
```

The visible box width is

```text
300px
```

But the margin still creates extra space outside the box.

So margin is separate.

---

# Best practice

Most modern projects use this

```css
html {
    box-sizing border-box;
}

,
before,
after {
    box-sizing inherit;
}
```

Or the simpler version

```css
 {
    box-sizing border-box;
}
```

Both are common.

For beginner projects, this is completely okay

```css
 {
    box-sizing border-box;
}
```

---

# Final summary

`box-sizing` controls how the browser calculates the size of an element.

The default value is

```css
content-box
```

With `content-box`

```text
width = only content
padding and border are added outside
```

With `border-box`

```text
width = content + padding + border
```

That is why this rule is very useful

```css
 {
    box-sizing border-box;
}
```

It makes element sizes easier to understand and prevents many layout problems.
