# Vinha dos Padres website

Static site for www.vinhadospadres.com, maintained by Francesco and Claude.

| Folder | Contents |
|---|---|
| `site/` | The published website (HTML, data, images, fonts, PDFs). Cloudflare serves this folder as is. |
| `build/` | Python scripts that generate the Portuguese pages, SEO tags, legal pages, sitemap and age gate from the English pages. |

## Cloudflare settings
Deployed as a Cloudflare Worker with static assets (see `wrangler.jsonc`, which serves the `site/` folder).
- Build command: (leave empty)
- Deploy command: `npx wrangler deploy`

## Updating
1. Edit the English pages in `site/`.
2. Run `build/build.sh` to regenerate the `-pt` pages, sitemap, canonicals and footers.
3. Run `python3 build/seo_launch.py` to re-apply titles, descriptions, share image, favicons and structured data.
4. Commit and push to `main`. Cloudflare publishes automatically.

URLs: English pages are `/<name>`, Portuguese pages `/<name>-pt` (home: `/` and `/index-pt`). Wine pages use the label abbreviation, e.g. Quinta da Vinha dos Padres 2022 white 3M12M = `/qdvdp-3m12m-2022-white`.
