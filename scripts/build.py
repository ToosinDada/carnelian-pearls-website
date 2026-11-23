#!/usr/bin/env python3
"""Build the site into ./_site, generating the Insights section from posts/*.md.

Run from the repository root:   python scripts/build.py

What it does
  1. Copies the static site into _site/ (leaving out posts/, scripts/, .git etc. and
     the old insights/ folder, which is always regenerated).
  2. Reads every posts/YYYY-MM-DD-slug.md, skipping drafts and future-dated posts.
  3. Writes /insights/ (index) and /insights/<slug>/ (articles) using the page shell
     of consulting/index.html, so they always match the site's current design.
  4. Rewrites sitemap.xml so it lists the published posts.

If anything is wrong (a missing field, a broken link in a post, a duplicate slug) the
build FAILS with a plain message and nothing is deployed, so the live site is never
replaced with a broken one.
"""
import html
import json
import math
import re
import shutil
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
SITE = "https://carnelianandpearls.com"
AUTHOR = "Tosin Dada"
LINKEDIN = "https://www.linkedin.com/in/tosindada/"

# Never copied into the published site.
SKIP_TOP_LEVEL = {".git", ".github", ".gitignore", ".pages.yml", ".DS_Store", "_site", "posts", "scripts",
                  "insights", "README.md", "WRITING-POSTS.md"}
FILENAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")


def fail(msg):
    print(f"\nBUILD FAILED: {msg}\n", file=sys.stderr)
    sys.exit(1)


# ---- read posts ----------------------------------------------------------
def load_posts():
    today = datetime.now(timezone.utc).date()
    posts, scheduled, seen = [], [], {}
    for path in sorted((ROOT / "posts").glob("*.md")):
        m = FILENAME.match(path.name)
        if not m:
            fail(f"posts/{path.name}: file names must look like 2026-12-01-my-post-title.md")
        text = path.read_text(encoding="utf-8")
        fm = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
        if not fm:
            fail(f"posts/{path.name}: the file must start with a header between two lines of ---")
        if re.search(r"(?mi)^draft:\s*true\s*$", fm.group(1)):
            print(f"  skipped (draft):      {path.name}")
            continue          # drafts may be unfinished; they never block a build
        try:
            meta = yaml.safe_load(fm.group(1)) or {}
        except yaml.YAMLError as e:
            fail(f"posts/{path.name}: the header could not be read ({e}). "
                 "If a title or summary contains a colon, put it in quotes.")
        for field in ("title", "summary"):
            if not str(meta.get(field, "")).strip():
                fail(f"posts/{path.name}: the header is missing '{field}'")
        raw_date = meta.get("date", m.group(1))
        post_date = raw_date if isinstance(raw_date, date) else None
        if post_date is None:
            try:
                post_date = date.fromisoformat(str(raw_date))
            except ValueError:
                fail(f"posts/{path.name}: date must look like 2026-12-01")
        if isinstance(post_date, datetime):
            post_date = post_date.date()

        if meta.get("draft") is True:          # e.g. "draft: yes"/"True" written differently
            print(f"  skipped (draft):      {path.name}")
            continue

        slug = m.group(2)
        if slug in seen:
            fail(f"posts/{path.name} and posts/{seen[slug]} use the same address '{slug}'")
        seen[slug] = path.name

        body_md = fm.group(2)
        body = markdown.markdown(body_md, extensions=["sane_lists", "tables"])
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S)      # editing notes never reach the page
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        minutes = int(meta.get("minutes") or max(1, round(words / 220)))
        post = {"slug": slug, "title": str(meta["title"]).strip(), "summary": str(meta["summary"]).strip(),
                "date": post_date, "minutes": minutes, "body": body, "file": path.name}
        if post_date > today:
            print(f"  scheduled (checked):  {path.name}  goes live on {post_date}")
            scheduled.append(post)
            continue
        posts.append(post)
        print(f"  published:            {path.name}")
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts, scheduled


def human(d):
    return f"{d.day} {d.strftime('%B %Y')}"


# ---- page shell ----------------------------------------------------------
def load_shell():
    s = (ROOT / "consulting" / "index.html").read_text(encoding="utf-8")
    s = re.sub(r'(?s)\s*<script type="application/ld\+json">.*?</script>', "", s)
    return s.replace(' aria-current="page"', "")


def make_page(shell, depth, title, desc, url, og_type, ld, main):
    s = shell
    if depth == 2:  # the shell's links are written for one level deep ("../")
        s = re.sub(r'(href|src)="\.\./', r'\1="../../', s)
    seo = (f'<title>{html.escape(title)} | CarnelianPearls Tech</title>\n'
           f'  <meta name="description" content="{html.escape(desc, quote=True)}">\n'
           f'  <link rel="canonical" href="{url}">\n'
           f'  <meta name="robots" content="index, follow">\n\n'
           f'  <meta property="og:type" content="{og_type}">\n'
           f'  <meta property="og:site_name" content="CarnelianPearls Tech">\n'
           f'  <meta property="og:title" content="{html.escape(title, quote=True)}">\n'
           f'  <meta property="og:description" content="{html.escape(desc, quote=True)}">\n'
           f'  <meta property="og:url" content="{url}">\n'
           f'  <meta property="og:image" content="{SITE}/assets/img/og-image.png">\n'
           f'  <meta name="twitter:card" content="summary_large_image">')
    s, n = re.subn(r'(?s)<title>.*?<meta name="twitter:card"[^>]*>', lambda m: seo, s, count=1)
    if n != 1:
        fail("could not find the page head in consulting/index.html (its layout has changed)")
    s = s.replace("</head>", f'  <script type="application/ld+json">\n{json.dumps(ld, indent=2)}\n  </script>\n</head>', 1)
    s, n = re.subn(r'(?s)<main id="main">.*?</main>', lambda m: f'<main id="main">\n{main}\n  </main>', s, count=1)
    if n != 1:
        fail("could not find <main> in consulting/index.html (its layout has changed)")
    prefix = "../" * depth
    s = s.replace(f'href="{prefix}insights/">Insights</a>', f'href="{prefix}insights/" aria-current="page">Insights</a>')
    return s


def check_links(post, out_dir):
    """Fail if a post links to a page or image on this site that does not exist."""
    for target in re.findall(r'(?:href|src)="(/[^"#?]*)"', post["body"]):
        t = target.lstrip("/")
        candidates = [out_dir / t, out_dir / t / "index.html"] if t else [out_dir / "index.html"]
        if not any(c.is_file() for c in candidates):
            fail(f"posts/{post['file']} links to {target}, which does not exist on the site")


# ---- main ------------------------------------------------------------------
def main():
    print("Reading posts:")
    posts, scheduled = load_posts()

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for item in ROOT.iterdir():
        if item.name in SKIP_TOP_LEVEL:
            continue
        if item.is_dir():
            shutil.copytree(item, OUT / item.name, ignore=shutil.ignore_patterns(".DS_Store"))
        else:
            shutil.copy2(item, OUT / item.name)

    for p in scheduled:          # catch mistakes in scheduled posts now, not on the day they go live
        check_links(p, OUT)

    shell = load_shell()
    author_ld = {"@type": "Person", "name": AUTHOR, "url": f"{SITE}/consulting/", "sameAs": [LINKEDIN]}

    for i, p in enumerate(posts):
        check_links(p, OUT)
        nxt = posts[(i + 1) % len(posts)] if len(posts) > 1 else None
        next_html = (f'''
          <nav class="post-end__next" aria-label="Next article">
            <a href="../{nxt['slug']}/"><span class="post-end__label">Next article</span><span class="post-end__title">{html.escape(nxt['title'])}</span></a>
          </nav>''' if nxt else "")
        url = f"{SITE}/insights/{p['slug']}/"
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"],
              "description": p["summary"], "datePublished": p["date"].isoformat(), "author": author_ld,
              "image": f"{SITE}/assets/img/og-image.png",
              "publisher": {"@type": "Organization", "name": "CarnelianPearls Technologies Limited", "url": SITE + "/"},
              "mainEntityOfPage": url}
        main_html = f'''    <article class="section post">
      <div class="container">
        <div class="prose">
          <p class="eyebrow"><a href="../">Insights</a></p>
          <h1>{html.escape(p["title"])}</h1>
          <div class="post-meta">
            <img class="post-meta__photo" src="../../assets/img/tosin-dada.jpg" alt="" width="720" height="720">
            <span><a href="../../consulting/">{AUTHOR}</a><br><time datetime="{p["date"].isoformat()}">{human(p["date"])}</time> &middot; {p["minutes"]} min read</span>
          </div>
          <p class="lead">{html.escape(p["summary"])}</p>
{p["body"]}
          <aside class="post-cta">
            <p><strong>Working through something similar?</strong> I take on ServiceNow engagements directly or corp-to-corp.</p>
            <div class="btn-row">
              <a class="btn btn--primary" href="../../consulting/">Work with Tosin</a>
              <a class="btn btn--secondary" href="../">More insights</a>
            </div>
          </aside>{next_html}
        </div>
      </div>
    </article>'''
        d = OUT / "insights" / p["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(
            make_page(shell, 2, p["title"], p["summary"], url, "article", ld, main_html), encoding="utf-8")

    if posts:
        items = "\n".join(f'''          <li class="post-list__item">
            <a href="{p["slug"]}/">
              <span class="post-list__meta"><time datetime="{p["date"].isoformat()}">{human(p["date"])}</time> &middot; {p["minutes"]} min read</span>
              <span class="post-list__title">{html.escape(p["title"])}</span>
              <span class="post-list__summary">{html.escape(p["summary"])}</span>
            </a>
          </li>''' for p in posts)
        listing = f'        <ol class="post-list">\n{items}\n        </ol>'
    else:
        listing = '        <p>The first posts are on their way.</p>'
    index_main = f'''    <section class="section">
      <div class="container">
        <div class="prose">
          <p class="eyebrow">Insights</p>
          <h1>Insights</h1>
          <p class="lead">Practical notes on ServiceNow delivery from <a href="../consulting/">{AUTHOR}</a>: platform design decisions, process and requirements, and using AI in delivery without lowering standards.</p>
        </div>
{listing}
      </div>
    </section>'''
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Insights | CarnelianPearls Tech",
          "url": f"{SITE}/insights/", "author": author_ld,
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/insights/{p['slug']}/",
                        "datePublished": p["date"].isoformat()} for p in posts]}
    (OUT / "insights").mkdir(exist_ok=True)
    (OUT / "insights" / "index.html").write_text(
        make_page(shell, 1, "Insights", "Practical notes on ServiceNow delivery from Tosin Dada, two-time ServiceNow MVP.",
                  f"{SITE}/insights/", "website", ld, index_main), encoding="utf-8")

    # sitemap: drop any insights entries, then add the published ones
    sm = (OUT / "sitemap.xml").read_text(encoding="utf-8")
    sm = re.sub(r"  <url>\n    <loc>[^<]*/insights/[^<]*</loc>.*?</url>\n", "", sm, flags=re.S)
    newest = (posts[0]["date"] if posts else date.today()).isoformat()
    add = f"  <url>\n    <loc>{SITE}/insights/</loc>\n    <lastmod>{newest}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    for p in posts:
        add += f"  <url>\n    <loc>{SITE}/insights/{p['slug']}/</loc>\n    <lastmod>{p['date'].isoformat()}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.7</priority>\n  </url>\n"
    (OUT / "sitemap.xml").write_text(sm.replace("</urlset>", add + "</urlset>"), encoding="utf-8")

    print(f"\nBuilt {len(posts)} post(s) into {OUT.name}/")


if __name__ == "__main__":
    main()
