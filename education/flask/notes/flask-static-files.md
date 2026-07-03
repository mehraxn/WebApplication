# Flask Static Files

**Static files** are files that don't change on the server: CSS stylesheets, JavaScript,
images, fonts. Flask serves them from a special folder so your pages can load them.

## The `static` folder
Create a folder named exactly `static` next to `app.py`. Flask automatically serves
anything inside it at the `/static/` URL.
```
myapp/
├── app.py
├── templates/
│   └── index.html
└── static/
    ├── style.css
    ├── script.js
    └── logo.png
```
You can add subfolders too (e.g. `static/css/`, `static/images/`).

## `url_for('static', filename='...')`
Always build the path to a static file with `url_for` instead of hard-coding `/static/`.
It returns the correct URL and won't break if things move.
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
```
For a file in a subfolder, include the subfolder in `filename`:
```html
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" />
```

## Linking CSS
Put the link in your template's `<head>`:
```html
<head>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
</head>
```

## Linking JavaScript
Put the script tag near the end of `<body>`:
```html
<body>
  <!-- page content -->
  <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
```

## Linking images
Use `url_for` in the `src`:
```html
<img src="{{ url_for('static', filename='logo.png') }}" alt="Company logo" />
```

## Why `url_for` instead of a plain path?
```html
<!-- fragile: breaks if the app is hosted under a subpath -->
<link rel="stylesheet" href="/static/style.css" />

<!-- robust: Flask builds the right URL -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
```
`url_for` is the recommended, portable way.

### Common mistakes
- **Wrong folder name** — it must be `static` (and `templates` for HTML). A typo means
  Flask can't find the files.
- **Hard-coding `/static/...`** instead of using `url_for`.
- **Forgetting the subfolder** in `filename` (e.g. `images/logo.png`).
- Editing CSS but not seeing changes — do a hard refresh; the browser may cache static
  files.

---

### Quick review
- Static files (CSS/JS/images) go in the `static/` folder.
- Link them with `url_for('static', filename='...')`, including any subfolder.
- CSS in `<head>`, JS before `</body>`.
- Don't hard-code `/static/` paths.
