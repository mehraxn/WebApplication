# HTML `button` Tag 

## Introduction

The `button` tag in HTML is used to create a clickable button on a web page.

It is one of the most important HTML elements because it allows the user to perform an action.

A button can be used to

 submit a form
 reset a form
 trigger JavaScript
 open a menu
 confirm an action
 cancel an action
 move to another step in an application

So, the `button` tag is not just for appearance. It is a real HTML element designed for user interaction.

---

## Basic Syntax

```html
buttonClick Mebutton
```

### Explanation

 `button` = opening tag
 `Click Me` = the content shown inside the button
 `button` = closing tag

This creates a visible clickable button with the text Click Me.

---

## Why `button` Has an Opening and Closing Tag

The `button` element is a container element.

That means it can hold content between its opening and closing tags.

Example

```html
buttonSavebutton
```

It can also contain more than plain text

```html
buttonstrongBuy Nowstrongbutton
```

It can even contain icons or small inline elements.

Because of this, `button` is more flexible than some other button-like elements such as

```html
input type=button value=Click Me
```

---

## Main Forms of the `button` Tag

The most important thing about a button is its `type`.

The `type` attribute tells the browser what kind of button it is.

There are three main forms

1. normal button
2. submit button
3. reset button

---

## 1) Normal Button

```html
button type=buttonOpen Menubutton
```

### What it does

A normal button does not submit a form by itself.

It is usually used for

 JavaScript actions
 opening popups
 showing menus
 changing page content
 interactive UI features

### Example

```html
button type=button onclick=alert('Hello!')Click Mebutton
```

When the user clicks the button, JavaScript runs.

### Important point

This type is the safest choice when you want a button that should not submit a form.

---

## 2) Submit Button

```html
button type=submitSubmitbutton
```

### What it does

A submit button sends form data to the server.

It is used inside a `form` element.

### Example

```html
form
  input type=text name=username placeholder=Enter username
  button type=submitSendbutton
form
```

When the user clicks Send, the form is submitted.

### Use cases

 login forms
 signup forms
 contact forms
 search forms
 checkout forms

---

## 3) Reset Button

```html
button type=resetResetbutton
```

### What it does

A reset button returns all form fields to their original values.

### Example

```html
form
  input type=text name=name value=Ali
  button type=resetResetbutton
form
```

If the user changes the text and clicks Reset, it goes back to Ali.

### Warning

Reset buttons are less common in modern web applications because users may click them by mistake and lose their input.

---

## Default Behavior of `button`

This is very important.

If you place a `button` inside a form and do not write a `type`, many browsers treat it as

```html
button type=submit...button
```

Example

```html
form
  input type=text
  buttonSavebutton
form
```

In many cases, clicking Save will submit the form.

### Best practice

Always write the type clearly.

Examples

```html
button type=buttonOpen Panelbutton
button type=submitSavebutton
button type=resetClearbutton
```

This avoids confusion and accidental form submission.

---

# Common Attributes and Options of the `button` Tag

The `button` tag supports many attributes.

These attributes control its behavior, identity, style, and accessibility.

---

## 1) `type`

Defines the kind of button.

### Options

 `button`
 `submit`
 `reset`

### Example

```html
button type=buttonNormalbutton
button type=submitSubmitbutton
button type=resetResetbutton
```

---

## 2) `id`

Gives a unique identifier to the button.

It is useful for

 CSS styling
 JavaScript targeting
 unique identification in the page

### Example

```html
button id=loginBtnLoginbutton
```

---

## 3) `class`

Groups buttons for styling or scripting.

### Example

```html
button class=primary-btnSavebutton
button class=primary-btnUpdatebutton
```

Now both buttons can share the same CSS style.

---

## 4) `disabled`

Makes the button unclickable.

### Example

```html
button disabledNot Availablebutton
```

### Use cases

 waiting for valid form input
 blocked actions
 unavailable features

When a button is disabled

 the user cannot click it
 it usually appears faded or gray

---

## 5) `name`

Defines the name of the button when sending form data.

### Example

```html
button type=submit name=actionSavebutton
```

This is mainly useful in forms.

---

## 6) `value`

Defines the value sent with the button when the form is submitted.

### Example

```html
button type=submit name=action value=deleteDeletebutton
```

This can help the server understand which button was clicked.

---

## 7) `onclick`

Runs JavaScript when the button is clicked.

### Example

```html
button type=button onclick=alert('Welcome!')Clickbutton
```

### Note

This is useful for learning, but in larger projects JavaScript is often attached using separate JS files instead of inline `onclick`.

---

## 8) `title`

Adds extra information that often appears as a tooltip when the mouse hovers over the button.

### Example

```html
button title=Save your workSavebutton
```

---

## 9) `autofocus`

Automatically focuses the button when the page loads.

### Example

```html
button autofocusStartbutton
```

### Note

Usually only one element on a page should use `autofocus`.

---

## 10) `form`

Associates the button with a form using the form's `id`, even if the button is outside the form.

### Example

```html
form id=myForm
  input type=text name=email
form

button type=submit form=myFormSendbutton
```

This button can submit that form even though it is outside it.

---

## 11) `formaction`

Overrides the form's action URL for that specific button.

### Example

```html
form action=default-action
  input type=text name=data
  button type=submitDefault Submitbutton
  button type=submit formaction=special-actionSpecial Submitbutton
form
```

---

## 12) `formmethod`

Overrides the method used when submitting the form.

### Common options

 `get`
 `post`

### Example

```html
button type=submit formmethod=postSend with POSTbutton
```

---

## 13) `formenctype`

Defines how form data is encoded when submitted.

Commonly used when uploading files.

### Example

```html
button type=submit formenctype=multipartform-dataUploadbutton
```

---

## 14) `formtarget`

Defines where to display the response after form submission.

### Common options

 `_self`
 `_blank`
 `_parent`
 `_top`

### Example

```html
button type=submit formtarget=_blankOpen Result in New Tabbutton
```

---

## 15) `formnovalidate`

Skips form validation for that specific submit button.

### Example

```html
button type=submit formnovalidateSubmit Without Validationbutton
```

---

# Button Content Options

One big advantage of `button` is that it can contain different kinds of content.

---

## Text Only

```html
buttonSavebutton
```

---

## Formatted Text

```html
buttonstrongImportantstrongbutton
```

---

## Icon and Text

```html
button
  🔍 Search
button
```

---

## HTML Inside Button

```html
button
  spanNext Stepspan
button
```

This is why `button` is often preferred over `input type=button`.

---

# Difference Between `button` and `input type=button`

## `button`

```html
buttonClick Mebutton
```

## `input type=button`

```html
input type=button value=Click Me
```

## Main differences

### `button`

 has opening and closing tags
 can contain HTML inside it
 more flexible
 commonly preferred in modern HTML

### `input type=button`

 self-closing style element
 text is written in the `value` attribute
 cannot contain HTML inside
 less flexible

---

# Examples of Different Button Forms

## Example 1 Normal Button

```html
button type=buttonShow Messagebutton
```

## Example 2 Submit Button

```html
button type=submitSubmit Formbutton
```

## Example 3 Reset Button

```html
button type=resetReset Formbutton
```

## Example 4 Disabled Button

```html
button type=button disabledComing Soonbutton
```

## Example 5 JavaScript Button

```html
button type=button onclick=document.body.style.background='lightblue'
  Change Background
button
```

---

# Real Form Example

```html
form action=submit method=post
  label for=usernameUsernamelabel
  input type=text id=username name=username

  button type=submitSubmitbutton
  button type=resetResetbutton
  button type=button onclick=alert('Help button clicked')Helpbutton
form
```

### What happens here

 Submit sends the form
 Reset clears changes and restores defaults
 Help runs JavaScript only

---

# Styling Buttons with CSS

Buttons are created in HTML, but their appearance is usually controlled by CSS.

### HTML

```html
button class=my-btnSavebutton
```

### CSS

```css
.my-btn {
  background-color blue;
  color white;
  padding 10px 20px;
  border none;
  border-radius 8px;
  cursor pointer;
}
```

### Result

The button becomes

 colored
 larger
 rounded
 more visually attractive

So

 HTML creates the button
 CSS styles the button
 JavaScript adds behavior

---

# Accessibility of `button`

Using a real `button` is better than making a fake button with `div` or `span`.

Why

Because browsers and assistive technologies already understand what a button is.

This helps with

 keyboard navigation
 screen readers
 accessibility
 expected browser behavior

### Good practice

Use `button` when the element performs an action.

Use `a` when the element is for navigation to another page.

---

# Best Practices

## 1. Always write the `type`

```html
button type=buttonMenubutton
```

This prevents accidental submit behavior.

## 2. Use meaningful text

Bad

```html
buttonClick Herebutton
```

Better

```html
buttonDownload Reportbutton
```

## 3. Use `button` for actions, not navigation

For moving to another page, prefer links

```html
a href=about.htmlAbouta
```

## 4. Avoid reset buttons unless truly needed

Users may click them by mistake.

## 5. Disable buttons carefully

If a button is disabled, make sure the user understands why.

---

# Quick Summary Table

 Button Type    Example                                 Main Purpose                 
 -------------  --------------------------------------  ---------------------------- 
 Normal button  `button type=buttonClickbutton`  Runs actions like JavaScript 
 Submit button  `button type=submitSendbutton`   Submits form data            
 Reset button   `button type=resetResetbutton`   Restores form defaults       

---

# Final Summary

The HTML `button` tag is used to create clickable buttons for user interaction.

It is one of the most important tags in web development because it allows users to trigger actions.

## Main button forms

 `type=button` → normal button
 `type=submit` → submits a form
 `type=reset` → resets a form

## Important options and attributes

 `type`
 `id`
 `class`
 `disabled`
 `name`
 `value`
 `onclick`
 `title`
 `autofocus`
 `form`
 `formaction`
 `formmethod`
 `formenctype`
 `formtarget`
 `formnovalidate`

In simple words

 HTML gives the button structure
 CSS gives the button style
 JavaScript gives the button action

So whenever you see a button on a web page, it is usually the result of these three working together.
