# Writing and publishing Insights posts

Each post is one text file in the `posts` folder. When you save it, GitHub rebuilds the site
and publishes it, usually within two to three minutes. No terminal and no software needed.

## Publish a post (GitHub website)

1. Open the repository on github.com and go into the **`posts`** folder.
2. Click **Add file → Create new file**.
3. Name the file with the date first, then the title in lowercase with hyphens:
   `2026-12-01-how-i-run-discovery-workshops.md`
   The part after the date becomes the web address: `/insights/how-i-run-discovery-workshops/`.
4. Paste in the template below and write your post.
5. Click **Commit changes**, keep "Commit directly to the main branch", and confirm.
6. Open the **Actions** tab. A green tick next to your commit means it is live.

## The template

```
---
title: "A clear headline for the post"
date: 2026-12-01
summary: "One or two sentences. Shown on the Insights page and in link previews."
draft: false
---

Your opening paragraph.

## A section heading

More text, with **bold** and *italic*.

- A bullet point
- Another bullet point
```

Only `title`, `date` and `summary` are required. Reading time is worked out for you.

**Put the title and summary in quotes.** A colon inside an unquoted line (like `Taska: what we learned`)
breaks the header.

## Formatting cheat sheet

| You type | You get |
|---|---|
| `## Heading` | A section heading |
| `**bold**` and `*italic*` | **bold** and *italic* |
| `- item` | A bullet point |
| `1. item` | A numbered list |
| `[link text](https://example.com)` | A link |
| `[my consulting page](/consulting/)` | A link to a page on this site |
| `> a quote` | A quotation |
| `![Describe the image](/assets/img/my-photo.jpg)` | An image |

## Images

Upload the image first: in the repository open **`assets/img`**, then **Add file → Upload files**.
Make it about 1200 pixels wide and under 300 KB, and always describe it in the square brackets
(screen readers and search engines read that). Then use `/assets/img/the-file-name.jpg` in your post.

## Drafts and scheduling

- **Draft:** set `draft: true`. The post is not published. Drafts can be unfinished and never stop the site building.
- **Schedule:** give the post a future `date`. It is checked now and goes live on that date
  (the site rebuilds every morning at about 06:00 Lagos time).
- **Unpublish:** set `draft: true` (or delete the file). It disappears at the next rebuild.

> **Important: this repository is public.** Anyone can read files in `posts`, including drafts,
> on github.com. Do not keep anything sensitive there (unconfirmed client details, anything
> your employer might object to) until you are ready to publish it. Write those posts somewhere
> private and add them when they are final.

## If something goes wrong

If a post has a mistake, the build **stops and the live site stays exactly as it was**. Nothing broken
goes live. In the **Actions** tab, click the run with the red cross, then the **build** step, and read the
line that starts `BUILD FAILED`. Fix that file and save again.

| Message says | Fix |
|---|---|
| file names must look like 2026-12-01-my-post-title.md | Rename the file: date first, then words joined with hyphens |
| the header is missing 'summary' (or 'title') | Add the line to the header |
| the header could not be read | Put the title and summary in quotes |
| links to /something/, which does not exist | Fix the link or upload the missing image |
| use the same address | Two posts have the same words after the date; change one |

## Things to know

- Renaming a published post changes its web address; the old address stops working.
- Changing a post's `date` moves it in the Insights list (newest first).
- Posts always appear under your name, with your photo, and end with the "Work with Tosin" box.
- The Insights pages are generated, so edit posts in `posts/` and not the `insights/` folder.
