# Vinha dos Padres website

Static site for www.vinhadospadres.com, maintained by Francesco and Claude.

| Folder | Contents |
|---|---|
| `site/` | The published website (HTML, data, images, fonts, PDFs). Cloudflare Pages serves this folder as is. |
| `build/` | Python scripts that generate the Portuguese pages, SEO tags, legal pages, sitemap and age gate from the English pages. |

## Cloudflare Pages settings
- Framework preset: None
- Build command: (leave empty)
- Build output directory: `site`

## Updating
1. Edit the English pages in `site/`.
2. Run `build/build.sh` to regenerate the `-pt` pages, sitemap, canonicals and footers.
3. Commit and push to `main`. Cloudflare publishes automatically.

URLs: English pages are `/<name>`, Portuguese pages `/<name>-pt` (home: `/` and `/index-pt`).
