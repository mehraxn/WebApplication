# Bootstrap CSS Link — Complete README

## Overview

When you want to use Bootstrap in your web page, the most common way is to import Bootstrap from a CDN inside the `head` section of your HTML file.

The Bootstrap CSS link usually looks like this

```html
link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css rel=stylesheet
```

A fuller version may look like this

```html
link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css
      rel=stylesheet
      integrity=sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH
      crossorigin=anonymous
```

This README explains

 what the Bootstrap CSS link is
 where it should be placed
 which parts are necessary
 what `integrity` means
 what `crossorigin` means
 how Bootstrap is imported correctly
 what is optional and what is recommended

---

## 1) What is the Bootstrap CSS link

The Bootstrap CSS link is an HTML `link` tag used to load the Bootstrap stylesheet into your web page.

Example

```html
link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css rel=stylesheet
```

After the browser loads this file, you can use Bootstrap classes such as

```html
container
row
col
btn
text-center
bg-dark
mt-3
```

So this link is what makes Bootstrap styling available in your HTML.

---

## 2) Where should we place the Bootstrap CSS link

It should be placed inside the `head` section of the HTML document.

Example

```html
!DOCTYPE html
html lang=en
head
  meta charset=UTF-8
  meta name=viewport content=width=device-width, initial-scale=1.0
  titleMy Bootstrap Pagetitle

  link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css rel=stylesheet
head
body

  h1 class=text-primaryHello Bootstraph1

body
html
```

It is placed in `head` because CSS should be loaded before the page content is shown, so the browser can style the page correctly.

---

## 3) What are the necessary parts of the Bootstrap CSS link

The minimum working Bootstrap CSS link is

```html
link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css rel=stylesheet
```

### Necessary parts

#### `href`

```html
href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css
```

This tells the browser where the Bootstrap CSS file is located.

In this case, the file is being loaded from a CDN called jsDelivr.

#### `rel=stylesheet`

```html
rel=stylesheet
```

This tells the browser that the linked file is a CSS stylesheet.

Without this, the browser would not treat the file as CSS properly.

### Final conclusion for the necessary parts

For basic importing of Bootstrap CSS, the truly necessary parts are

 `href`
 `rel=stylesheet`

---

## 4) What is a CDN

A CDN stands for Content Delivery Network.

It is a service that stores files such as CSS, JavaScript, images, and other assets, then delivers them quickly to users.

In the Bootstrap link

```html
httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css
```

this URL points to the Bootstrap CSS file on the jsDelivr CDN.

This means you do not need to download Bootstrap manually into your project. The browser fetches it directly from the internet.

---

## 5) How do we import Bootstrap correctly

### Minimum import

```html
head
  link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css rel=stylesheet
head
```

This is enough to use Bootstrap CSS classes.

### Recommended basic HTML structure

```html
!DOCTYPE html
html lang=en
head
  meta charset=UTF-8
  meta name=viewport content=width=device-width, initial-scale=1.0
  titleBootstrap Exampletitle

  link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css rel=stylesheet
head
body

  div class=container mt-4
    h1 class=text-primaryHello Bootstraph1
    button class=btn btn-successClick mebutton
  div

body
html
```

### More complete version with security attributes

```html
!DOCTYPE html
html lang=en
head
  meta charset=UTF-8
  meta name=viewport content=width=device-width, initial-scale=1.0
  titleBootstrap Exampletitle

  link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css
        rel=stylesheet
        integrity=sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH
        crossorigin=anonymous
head
body

  div class=container mt-4
    h1 class=text-primaryHello Bootstraph1
    button class=btn btn-successClick mebutton
  div

body
html
```

---

## 6) What is `integrity`

`integrity` is a security feature.

It is used to verify that the external file downloaded by the browser is exactly the file you expect.

Example

```html
integrity=sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH
```

### What does it check

It checks the file being imported from the URL in `href`.

In the Bootstrap example, it checks

```html
bootstrap.min.css
```

The browser does this process

1. It downloads the Bootstrap CSS file from the CDN.
2. It calculates a hash value from that downloaded file.
3. It compares that hash to the hash written in the `integrity` attribute.
4. If they match, the browser uses the file.
5. If they do not match, the browser blocks the file.

### Why is this useful

It helps protect against cases where the file was

 changed
 corrupted
 tampered with
 replaced by a malicious version

### Is `integrity` necessary

No.

It is not necessary for basic Bootstrap importing.

Bootstrap will still load without it if the link is otherwise correct.

But it is a strong extra safety feature and is often included in official examples.

### Very important clarification

`integrity` does not check your whole website.

It checks only the external file being loaded by that specific tag.

So in this case, it checks the imported Bootstrap CSS file, not

 your HTML file
 your local CSS file
 your whole project

---

## 7) What does `sha384` mean in `integrity`

The `sha384` part tells the browser which hashing algorithm was used to create the file fingerprint.

So

```html
integrity=sha384-...
```

means

 this is a hash-based fingerprint
 it was created using the SHA-384 algorithm

You can think of it as a very specific digital fingerprint for the file.

If the downloaded file changes even a little, the hash will no longer match.

---

## 8) What is `crossorigin`

`crossorigin` is about loading a file from another origin.

### What is an origin

An origin is defined by the combination of

 protocol, such as `http` or `https`
 domain, such as `example.com`
 port, such as `80`, `443`, or `5000`

If your page is on one origin and the Bootstrap file is on another, the request is cross-origin.

Example

 your site `httpsmywebsite.com`
 Bootstrap CDN `httpscdn.jsdelivr.net`

These are different origins.

### What does `crossorigin=anonymous` mean

```html
crossorigin=anonymous
```

This tells the browser

 load the file from another origin
 do not send credentials such as cookies or authentication information

So the file is requested as a public resource.

### Why is it often used with `integrity`

When a resource comes from another origin and you want to verify it using `integrity`, the browser may need the request to be handled as a CORS-enabled request. The `crossorigin` attribute helps define how that request is made.

That is why `integrity` and `crossorigin=anonymous` often appear together in CDN examples.

### Is `crossorigin` necessary

No, not for basic importing.

Bootstrap CSS can still be imported with only

```html
link href=... rel=stylesheet
```

But `crossorigin` is commonly included for better correctness and compatibility when using external resources together with `integrity`.

---

## 9) What values can `crossorigin` have

There are two important values

### `anonymous`

```html
crossorigin=anonymous
```

Meaning

 make the cross-origin request
 do not send credentials

This is the common value for public CDN files like Bootstrap.

### `use-credentials`

```html
crossorigin=use-credentials
```

Meaning

 make the cross-origin request
 do send credentials such as cookies or authentication information

This is not commonly used for public Bootstrap imports.

### If the attribute is omitted

If `crossorigin` is not written at all, the browser simply does not use an explicitly declared crossorigin mode from this attribute.

For learning purposes, that means

 the file may still load normally
 but you are not explicitly telling the browser how to handle the cross-origin fetch through this attribute

---

## 10) Is the viewport meta tag necessary

A Bootstrap page commonly includes this line

```html
meta name=viewport content=width=device-width, initial-scale=1.0
```

### What does it do

It helps the page display properly on phones and tablets.

It tells the browser to match the page width to the device width and use a normal initial zoom level.

### Is it necessary for importing Bootstrap

No.

It does not import Bootstrap.

But it is strongly recommended because Bootstrap is built for responsive design, and this meta tag helps responsive layouts behave properly on mobile devices.

---

## 11) Is Bootstrap JavaScript necessary

Bootstrap CSS and Bootstrap JavaScript are not the same thing.

### Bootstrap CSS

Used for

 layout
 colors
 spacing
 typography
 buttons
 grid system
 responsive classes

### Bootstrap JavaScript

Used for interactive components such as

 navbar toggle
 modal
 dropdown
 carousel
 collapse
 tooltip
 offcanvas

### Is JS necessary for importing Bootstrap CSS

No.

If you only want Bootstrap styling, the CSS link is enough.

### When should we include Bootstrap JS

If you want interactive Bootstrap features, include this before `body`

```html
script src=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distjsbootstrap.bundle.min.jsscript
```

So the final rule is

 for Bootstrap styling only, CSS is enough
 for interactive Bootstrap components, add Bootstrap JS too

---

## 12) What if we also have our own CSS file

You can still use your own CSS file together with Bootstrap.

Example

```html
head
  meta charset=UTF-8
  meta name=viewport content=width=device-width, initial-scale=1.0
  titleMy Pagetitle

  link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css rel=stylesheet
  link rel=stylesheet href=style.css
head
```

### Why put `style.css` after Bootstrap

Because when your CSS file comes after Bootstrap, your custom CSS can override Bootstrap styles more easily.

So

 first load Bootstrap
 then load your own CSS

---

## 13) Necessary vs recommended vs optional

### Necessary for importing Bootstrap CSS

```html
link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css rel=stylesheet
```

### Recommended

```html
meta name=viewport content=width=device-width, initial-scale=1.0
```

This helps responsive design work properly.

### Optional but useful

```html
integrity=...
crossorigin=anonymous
```

These improve security and define cross-origin loading behavior.

### Optional depending on your needs

```html
script src=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distjsbootstrap.bundle.min.jsscript
```

This is needed only for interactive Bootstrap components.

---

## 14) Full final example

```html
!DOCTYPE html
html lang=en
head
  meta charset=UTF-8
  meta name=viewport content=width=device-width, initial-scale=1.0
  titleBootstrap Complete Exampletitle

  link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css
        rel=stylesheet
        integrity=sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH
        crossorigin=anonymous

  link rel=stylesheet href=style.css
head
body

  div class=container mt-5
    h1 class=text-primaryHello Bootstraph1
    p class=leadThis page uses Bootstrap CSS.p
    button class=btn btn-successExample Buttonbutton
  div

  script src=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distjsbootstrap.bundle.min.jsscript
body
html
```

---

## 15) Final summary

To import Bootstrap correctly

1. Place the Bootstrap CSS `link` inside the `head` section.
2. The truly necessary parts are `href` and `rel=stylesheet`.
3. `integrity` is a security feature that checks the downloaded Bootstrap file matches the expected fingerprint.
4. `crossorigin` tells the browser how to request a file from another origin.
5. `crossorigin=anonymous` means fetch it without sending credentials.
6. The viewport meta tag is strongly recommended for responsive design.
7. Bootstrap JavaScript is only needed for interactive components such as modals, dropdowns, carousels, and navbar toggles.
8. If you have your own CSS file, load it after Bootstrap.

The minimum working Bootstrap import is

```html
link href=httpscdn.jsdelivr.netnpmbootstrap@5.3.3distcssbootstrap.min.css rel=stylesheet
```

That is the essential starting point for using Bootstrap in an HTML page.
