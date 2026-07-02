# 📐 Bootstrap Grid System — Complete Guide

 A clear, structured reference for understanding and using the Bootstrap grid layout system.

---

## 📋 Table of Contents

1. [What is the Bootstrap Grid System](#1-what-is-the-bootstrap-grid-system)
2. [The 12-Column System](#2-the-12-column-system)
3. [Container](#3-container)
4. [Row](#4-row)
5. [Column](#5-column)
6. [Column Classes Explained](#6-column-classes-explained)
7. [Breakpoints](#7-breakpoints)
8. [Column Examples](#8-column-examples)
9. [Responsive Columns](#9-responsive-columns)
10. [Overflow Beyond 12 Columns](#10-overflow-beyond-12-columns)
11. [Auto-Layout Columns](#11-auto-layout-columns)
12. [Gutters & Spacing](#12-gutters--spacing)
13. [Nesting Rows & Columns](#13-nesting-rows--columns)
14. [Bootstrap Grid & Flexbox](#14-bootstrap-grid--flexbox)
15. [Best Practice Structure](#15-best-practice-structure)
16. [Common Mistakes](#16-common-mistakes)
17. [Summary](#17-summary)

---

## 1. What is the Bootstrap Grid System

The Bootstrap grid system is a layout system built on containers, rows, and columns. It helps divide a page into clean, organized sections and makes layouts automatically responsive across different screen sizes.

```
container → row → columns
```

 Part         Role                                      
--------------------------------------------------------
 `container`  Wraps and centers the overall content     
 `row`        Creates a horizontal grouping             
 `col-`      Divides the row into sized sections       

---

## 2. The 12-Column System

Every Bootstrap row is divided into 12 equal parts. Column widths are defined by how many of those 12 parts the element should occupy.

 Class     Width         
-------------------------
 `col-12`  Full width    
 `col-6`   Half width    
 `col-4`   One-third     
 `col-3`   One-quarter   

Common combinations that add up to 12

```
12          → full width
6  + 6      → two equal columns
4  + 4  + 4 → three equal columns
3  + 3  + 3 + 3 → four equal columns
8  + 4      → main content + sidebar
```

---

## 3. Container

A container is the outer wrapper of the grid. It centers the layout and provides proper spacing.

```html
!-- Fixed max-width, centered --
div class=container
  ...
div

!-- Full viewport width --
div class=container-fluid
  ...
div
```

 Class               Behavior                              
-----------------------------------------------------------
 `container`         Centered with a max-width             
 `container-fluid`   Full-width across the entire screen   

---

## 4. Row

A row holds columns and creates a single horizontal group.

```html
div class=row
  ...
div
```

- Groups columns into one horizontal line
- Tells Bootstrap the children are part of the grid
- Handles alignment and wrapping automatically
- Should always be placed inside a container

---

## 5. Column

A column is the building block that occupies width inside a row.

```html
div class=col-4Columndiv
```

This element takes 4 out of 12 available column slots.

---

## 6. Column Classes Explained

Bootstrap column classes follow this naming pattern

```
col - {breakpoint} - {size}
 │         │           │
 │         │           └── Number from 1 to 12
 │         └────────────── Screen size (sm, md, lg, xl, xxl)
 └──────────────────────── Column keyword
```

Example

```html
div class=col-md-4Contentdiv
```

 Occupy 4 of 12 columns on medium screens and larger.

---

## 7. Breakpoints

Bootstrap uses breakpoints to define how columns behave at different screen widths. Each breakpoint applies to that size and above.

 Class        Screen Size               Starts At 
-------------------------------------------------
 `col-sm-`   Small and larger          576px     
 `col-md-`   Medium and larger         768px     
 `col-lg-`   Large and larger          992px     
 `col-xl-`   Extra large and larger    1200px    
 `col-xxl-`  Extra extra large         1400px    

Example — combining breakpoints

```html
div class=col-md-6 col-lg-4Contentdiv
```

```
Medium screens  → 612 width  (2 columns per row)
Large screens   → 412 width  (3 columns per row)
```

---

## 8. Column Examples

### One Full-Width Column
```html
div class=row
  div class=col-12Full widthdiv
div
```
```
[ Full width ]
```

---

### Two Equal Columns
```html
div class=row
  div class=col-6Leftdiv
  div class=col-6Rightdiv
div
```
```
[ Left ] [ Right ]
```

---

### Three Equal Columns
```html
div class=row
  div class=col-4Onediv
  div class=col-4Twodiv
  div class=col-4Threediv
div
```
```
[ One ] [ Two ] [ Three ]
```

---

### Four Equal Columns
```html
div class=row
  div class=col-3Onediv
  div class=col-3Twodiv
  div class=col-3Threediv
  div class=col-3Fourdiv
div
```
```
[ One ] [ Two ] [ Three ] [ Four ]
```

---

### Unequal Columns (Main + Sidebar)
```html
div class=row
  div class=col-8Main contentdiv
  div class=col-4Sidebardiv
div
```
```
[ Main content      ] [ Sidebar ]
```

---

## 9. Responsive Columns

Columns can change size based on screen width by combining multiple breakpoint classes.

```html
div class=col-12 col-md-6 col-lg-4Contentdiv
```

 Screen   Behavior            
------------------------------
 Mobile   Full width (1212)  
 Tablet   Half width (612)   
 Desktop  One-third (412)    

Full responsive example

```html
div class=row
  div class=col-12 col-md-6 col-lg-4Card 1div
  div class=col-12 col-md-6 col-lg-4Card 2div
  div class=col-12 col-md-6 col-lg-4Card 3div
div
```

```
Mobile   [ Card 1 ]
          [ Card 2 ]
          [ Card 3 ]

Tablet   [ Card 1 ] [ Card 2 ]
          [ Card 3 ]

Desktop  [ Card 1 ] [ Card 2 ] [ Card 3 ]
```

---

## 10. Overflow Beyond 12 Columns

If column widths in a row add up to more than 12, the extra columns wrap to the next line automatically.

```html
div class=row
  div class=col-6Adiv
  div class=col-6Bdiv
  div class=col-6Cdiv  !-- Wraps! 6+6+6 = 18 --
div
```

```
[ A ] [ B ]
[ C ]
```

---

## 11. Auto-Layout Columns

Use `col` without a number to let Bootstrap divide the row equally.

```html
div class=row
  div class=colOnediv
  div class=colTwodiv
  div class=colThreediv
div
```

Each column gets the same width automatically. Useful when exact widths are not needed.

---

## 12. Gutters & Spacing

Gutters add spacing between columns. Use the `g-` classes on the row.

```html
div class=row g-3
  ...
div
```

 Class   Gap Size        
-------------------------
 `g-0`   No gap          
 `g-1`   Very small      
 `g-2`   Small           
 `g-3`   Medium          
 `g-4`   Large           
 `g-5`   Very large      

Separate horizontal and vertical gaps

```html
div class=row gx-3 gy-4
  ...
div
```

 Class    Controls          
----------------------------
 `gx-`   Horizontal gap    
 `gy-`   Vertical gap      

---

## 13. Nesting Rows & Columns

You can place a row inside a column to create more complex layouts.

```html
div class=container
  div class=row
    div class=col-8
      Main content
      div class=row
        div class=col-6Nested 1div
        div class=col-6Nested 2div
      div
    div
    div class=col-4Sidebardiv
  div
div
```

---

## 14. Bootstrap Grid & Flexbox

Bootstrap rows use Flexbox internally. When you write

```html
div class=row
```

Bootstrap applies `display flex` behind the scenes. This is why columns align and respond so reliably without writing any custom layout CSS.

---

## 15. Best Practice Structure

A clean, well-separated Bootstrap grid looks like this

```html
section class=container
  div class=row g-3
    div class=col-md-4
      div class=card
        Content
      div
    div
  div
section
```

 Element     Responsibility                  
---------------------------------------------
 `container` Centering and page margins      
 `row`       Horizontal grouping             
 `col-md-4`  Width and layout control        
 `card`      Visual appearance only          

 ✅ Keep layout (columns) and design (cards) separate.

---

## 16. Common Mistakes

### ❌ Placing Columns Outside a Row

```html
!-- Wrong --
div class=container
  div class=col-6Columndiv
div

!-- Correct --
div class=container
  div class=row
    div class=col-6Columndiv
  div
div
```

### ❌ Forgetting the Container

Without a container the layout will not be centered or properly padded.

### ❌ Overly Complex Column Combinations

Stick to simple, readable combinations

```
✅  6 + 6
✅  4 + 4 + 4
✅  3 + 3 + 3 + 3
✅  8 + 4
```

---

## 17. Summary

 Concept        Key Point                                          
-------------------------------------------------------------------
 Grid structure  `container → row → columns`                      
 Column system   Every row has 12 columns                      
 Column class    `col-{breakpoint}-{size}` (e.g. `col-md-4`)      
 Responsive      Combine breakpoints on one element                
 Auto columns    `col` without a number for equal widths           
 Gutters         `g-`, `gx-`, `gy-` for spacing                
 Under the hood  Bootstrap grid is built on Flexbox            

---

 💡 The golden rule Every row has 12 columns. Column classes define how many of those 12 parts each element takes at each screen size.