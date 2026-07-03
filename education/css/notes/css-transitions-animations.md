# CSS Transitions & Animations

Motion makes a page feel polished. CSS gives you two tools: **transitions** (smooth change between two states) and **animations** (multi-step sequences with keyframes).

## `transition`
A transition smoothly animates a property when its value changes (e.g. on hover) instead of snapping instantly.

```css
.button {
  background: blue;
  transition: background 0.3s ease;  /* animate background over 0.3s */
}
.button:hover {
  background: darkblue;   /* the change fades smoothly */
}
```

The shorthand is: `transition: property duration timing-function delay;`
```css
transition: all 0.3s ease-in-out;   /* animate every changing property */
transition: transform 0.2s linear;
```
Tip: naming a specific property (`transform`) performs better than `all`.

## `transform`
`transform` changes an element's shape/position **without affecting the layout** around it — great for hover effects because nothing else shifts.
```css
transform: scale(1.1);         /* 10% bigger */
transform: rotate(15deg);      /* rotate */
transform: translateY(-5px);   /* move up 5px */
transform: translateX(20px);   /* move right 20px */
```

## Hover effects (transition + transform together)
The classic "lift on hover" card:
```css
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-5px);           /* lifts up */
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
```
A button that grows slightly:
```css
.btn { transition: transform 0.15s ease; }
.btn:hover { transform: scale(1.05); }
```

## Simple keyframes animation
For motion that runs on its own (not just on hover), use `@keyframes` to define the steps, then attach it with `animation`.

```css
/* 1. define the steps */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* 2. apply it */
.box {
  animation: fadeIn 0.5s ease-in;
}
```

You can use percentages for more steps:
```css
@keyframes pulse {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.1); }
  100% { transform: scale(1); }
}
.heart {
  animation: pulse 1s infinite;   /* repeat forever */
}
```

The `animation` shorthand: `animation: name duration timing-function delay iteration-count;`
```css
animation: pulse 1s ease-in-out 0s infinite;
```

### Common mistakes
- **Putting `transition` on the `:hover` rule** — it belongs on the **base** element so it works going both in *and* out.
- **Animating `width`/`height`/`top`/`left`**, which is janky. Prefer `transform` and `opacity` (much smoother).
- **Forgetting units** (`0.3s`, not `0.3`) — the transition silently won't run.
- **Too much motion** — subtle is better; overdone animations feel unprofessional and can hurt accessibility.

---

### Quick review
- `transition` on the **base** element smooths changes (like on `:hover`).
- `transform` (scale/rotate/translate) is the smooth, layout-safe way to move things.
- `@keyframes` + `animation` create self-running, multi-step motion.
- Animate `transform`/`opacity`, not layout properties.
