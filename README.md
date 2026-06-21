# CarnelianPearls Tech website

A small, fast, static marketing site. Plain HTML, CSS, and a little vanilla
JavaScript. No framework, no build step, no backend. Contact runs through the
visitor's own email client (mailto), so there is nothing to deploy but files.

---

## Contents

```
site/
├── index.html                Home
├── partnerships/index.html
├── venture-studio/index.html
├── opportunities/index.html
├── about/index.html
├── contact/index.html
├── privacy/index.html        Legal stub (placeholder copy)
├── terms/index.html          Legal stub (placeholder copy)
├── 404.html                  Not-found page (uses absolute paths, see note)
├── assets/
│   ├── css/styles.css        One shared stylesheet
│   ├── js/main.js            Menu toggle + contact mailto composer
│   └── img/favicon.svg       Site icon (add og-image.png here, see below)
├── sitemap.xml
├── robots.txt
└── README.md                 This file
```

---

## How to preview locally

**Quickest:** double-click `index.html` (or any page's `index.html`) to open it
in a browser. Each page renders on its own with no server.

**Full navigation:** because the site uses clean, extensionless folder URLs
(`/partnerships/` rather than `/partnerships/index.html`), browsers opening files
straight from disk will not always follow links between pages, and `404.html`
will not be styled. To preview exactly as it will deploy, run any static server
from inside the `site/` folder:

```bash
# Python 3 (built in on macOS)
python3 -m http.server 8000

# or Node, if you have it
npx serve .
```

Then open <http://localhost:8000>.

---

## How to publish

The output is a plain folder. Pick one:

- **Netlify Drop:** drag the `site/` folder onto <https://app.netlify.com/drop>.
- **Cloudflare Pages:** create a project and upload the `site/` folder, or
  connect a Git repo with the build output set to this folder.
- **GitHub Pages:** push the contents of `site/` to a repo and enable Pages.
- **Any web host:** upload the contents of `site/` to the public directory
  (often `public_html`).

Then point the `carnelianandpearls.com` domain at the host. No account-specific
service, database, or serverless function is required.

> **404 note:** `404.html` uses root-absolute paths (`/assets/...`) on purpose,
> so it stays styled when a host serves it for a missing URL at any depth. All
> hosts listed above serve `404.html` automatically.

---

## Placeholders to fill before launch

Everything below is wrapped in an obvious token so you can find it with a
search. Search the whole `site/` folder for the token in brackets.

| Token | What it is | Where it appears |
|---|---|---|
| `[TASKA_URL]` | The live Taska link | Home (In focus button), Venture Studio (2 buttons), every footer "Taska" link, Home JSON-LD `sameAs` |
| `[TASKA_DESCRIPTION]` | One or two sentences on what Taska is, who it helps, what it does | Home (In focus blurb), Venture Studio (Taska block) |
| `[LINKEDIN_URL]` | LinkedIn company page | Every footer "LinkedIn" link, Home JSON-LD `sameAs` |
| `[RC_NUMBER]` | Company registration (RC) number | Every footer legal line, Privacy, Terms |
| `[REGISTERED_ADDRESS]` | Registered address | Every footer legal line, Privacy, Terms |
| `[OG_IMAGE]` | Social share image | See "Social share image" below |
| `[DATE]` | Last-updated date on legal pages | Privacy, Terms |
| `[PLACEHOLDER]` | Draft legal copy that must be reviewed | Privacy, Terms |

### Contact email

The contact email defaults to **info@carnelianandpearls.com** and is already wired
up and working (mailto links, the contact form, footers). To use a different
address, search the `site/` folder for `info@carnelianandpearls.com` and replace
all occurrences, including the `data-email` attribute on the contact form in
`contact/index.html`.

### Social share image

The pages reference `assets/img/og-image.png` for Open Graph / Twitter cards, but
that file is not included. Add a `1200x630` PNG at `assets/img/og-image.png`. The
`<meta property="og:image">` and `twitter:image` tags already point to it (as
absolute URLs on `https://carnelianandpearls.com`). Update those URLs if the live
domain differs.

### Live domain

`https://carnelianandpearls.com` is used in the `canonical`, Open Graph, JSON-LD,
`sitemap.xml`, and `robots.txt` entries. If the live domain differs, update it in
those places (search for `carnelianandpearls.com`).

### Adding a real logo

Each page has a clearly commented `LOGO SLOT` in the header (and a matching mark
in the footer). Replace the inline `<svg class="brand__mark">` plus the
`<span class="brand__name">` with your SVG logo when ready. The markup is
identical across pages, so a find-and-replace updates them all.

---

## How it is built

- **One stylesheet** (`assets/css/styles.css`) and **one script**
  (`assets/js/main.js`) shared by every page. Styles are never duplicated per
  page; the header, footer, and closing call-to-action band are hand-copied
  partials kept byte-identical so edits are easy to find and replace.
- **Design tokens** (colours, spacing) live as CSS custom properties on `:root`.
  The accent is carnelian (`#B7410E`), used sparingly.
- **Mobile-first and responsive**, breakpoints around 560/640/768/880/900px.
  The navigation collapses to an accessible hamburger menu below 880px.
- **Accessibility:** semantic landmarks, a skip link, visible focus states,
  `aria-expanded` on the menu toggle, labelled form fields, and respect for
  `prefers-reduced-motion`.
- **No people, no stock photos.** The only imagery is small inline SVG motifs.
- **British English** throughout, and no em dashes in any copy.

The contact form is progressive enhancement: with JavaScript it composes a
prefilled `mailto:`; without JavaScript the visible email address and the four
prefilled intent links still work. No visitor data is ever sent to a server.
