# Animated Login Page

## Project Overview
A styled, centered login page with smooth CSS transitions and a subtle fade-in animation.
It focuses on polished input styling and clear focus/hover states — the details that make
a form feel professional.

## Features
- Login form (email, password, remember me, forgot password)
- Clean input styling
- Hover and focus states on inputs, links, and the button
- Transition effects (focus glow, button hover, active press)
- Fade-in animation on page load
- Responsive, centered layout

## Technologies Used
- HTML5
- CSS3 (Flexbox centering, `@keyframes`, transitions, CSS variables — no Bootstrap)

## Folder Structure
```
animated-login-page/
├── index.html    # the login page
├── style.css     # styling
├── README.md     # this file
└── screenshots/  # add screenshots here
```

## How to Run or Open
Open `index.html` directly in any web browser — no server needed.

## What I Learned
- Centering a card both axes with Flexbox on the `body`.
- A `@keyframes` fade-in animation and `:focus` glow with `box-shadow`.
- Tasteful `transition` timing for hover/active states.

## Resume Value
Forms and authentication screens appear in almost every app. This shows I can style inputs,
handle interactive states accessibly, and add tasteful motion.

## Future Improvements
- Add client-side validation feedback (JavaScript)
- Add a show/hide password toggle
- Wire it to a real Flask login route
