# The Footprints Times: Achievement poster maker

Live at **https://iitgnalumni.github.io/footprints-times/** (internal team tool).

**Keep it separate from the public alumni site:** do not add it to `alumni-nav.js` or link it from any other page, and do not add the shared top bar (`<script src="/alumni-nav.js">`) to this page. It is hidden from search engines, but anyone with the link can open it, so share the link only within the team.

Makes the approved "The Footprints Times · Achievement Edition" Instagram/LinkedIn poster (1080 × 1350 px) in the browser. Nothing is uploaded anywhere: the photo and text stay on the computer of whoever uses the page.

## How the team uses it

1. Open the link, fill in the edition (post no., month, year), headline, name, batch, story and closing line.
2. Upload the alumnus photo: JPG, PNG or HEIC (iPhone). Any size or shape works: it is cropped to the square and keeps its colours, with an adjustable **Vintage tone** (30% to start) to match the paper. Frame the face with **Zoom**, **Move left ↔ right** and **Move up ↕ down** (or drag the photo in the preview). **Reset photo position** starts over.
3. Fix anything the **Checks** panel marks in red. The download stays locked until all red items are fixed.
4. Click **Download PNG** (sharpest) or **Download JPG** (smaller file).

## What the page enforces

| Item | Rule |
| --- | --- |
| Headline | Must fit on one line (about 28 characters). The page says how many characters to remove. |
| Photo | Always a square: starts at 640 × 640, adjustable from 460 × 460 up to 664 × 664 with **Photo size** (shrinks from the right; the story column widens). Warning (not blocking) if the photo is smaller than the square. |
| Name | At most two lines in the story column. |
| Batch | One line inside the box, e.g. `BTECH · ME · 2018`. |
| Caption | One line under the photo. |
| Story | Justified, with automatic hyphenation. The column must start level with the top of the photo and end level with its bottom. Too long or too short gives "remove/add about N words". |

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The whole tool: form, checks and the poster drawing code |
| `assets/alumni-relations-logo.webp` | Alumni Relations logo (top-left of the poster) |
| `assets/paper-texture.jpg` | The aged-paper texture laid over the poster |
| `vendor/heic2any.min.js` | Converts iPhone HEIC photos in the browser (MIT licence; loaded only when a HEIC file is uploaded) |
| `vendor/hyphenate.js` | English hyphenation for the justified story (Hypher, BSD licence + TeX en-US patterns) |
| `fonts/` | Playfair Display, Old Standard TT and Oswald (SIL Open Font License), served locally so the poster looks the same on every computer |

## Changing the design

All fixed positions and sizes are in the `FIXED DESIGN` block at the top of the script in `index.html`. The fixed wording (masthead, "Where IITGN shines", "Congratulations from the IITGN family", `#IITGNAlumni`) is in the `RENDER` section.
