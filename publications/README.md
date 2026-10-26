# Newsletters & Annual Reports website

Live at **https://iitgnalumni.github.io/publications/**

The website reads everything from one Google Drive folder:
**Alumni Website – Newsletters & Annual Reports**
(https://drive.google.com/drive/folders/1bxMzPifuOyF-yhqr3wLpUoR1-L-QlZ7q)

## Adding a new issue or report

1. Upload the PDF into the right folder in Drive:
   - **Footprints in Palaj** – the current quarterly newsletter
   - **Annual Reports**
   - **Footprints Archive (before Oct 2025)** – old Footprints issues
2. Name the file the way it should appear on the website, with the period in it, for example
   `Footprints in Palaj – April-June 2026.pdf` or `Alumni Annual Report 2025-26.pdf`.
   The newest is shown first, worked out from the months and years in the name.
3. Within about an hour it appears on the website as a flip-book with a Download button.

That's all. No code and no GitHub needed.

- **Change a title:** rename the file in Drive.
- **Remove something:** delete it from the folder (or move it out). It disappears from the website at the next update.
- **Replace a PDF:** delete the old file and upload the new one.
- Files with **"draft"** in their name are ignored, so drafts can stay in the folder safely.
- Google Docs and Google Slides placed in the folders work too; they are shown as PDFs.
- A **new folder** inside the main folder becomes a new section on the website, named after the folder.

### PDFs that live elsewhere

The Google Sheet **"Website links – PDFs kept outside Drive"** in the main folder lists PDFs that are hosted on alumni.iitgn.ac.in instead of Drive (older Footprints issues and the first two Footprints in Palaj issues).
Columns: `Shelf | Title | PDF link | Date (YYYY-MM)`. Add a row to add one more; delete a row to remove it.

### Keep the folder shared

The main folder must stay shared as **Anyone with the link → Viewer**. If it is made private, the website keeps showing what it already has but cannot add anything new.

## Seeing it sooner than an hour

On GitHub: **Actions** tab → **Sync publications from Drive** → **Run workflow**. It takes a few minutes, longer when many new PDFs were added.

## How it works (for whoever maintains it)

- `.github/workflows/sync-publications.yml` runs every hour.
- `.github/scripts/sync_publications.py` lists the Drive folder, turns each new or changed PDF into page images (`library/<drive-id>/p-001.webp …` and `cover.webp`) and writes `library.json`, which `index.html` reads.
- The flip-book uses `assets/page-flip.js` (StPageFlip, MIT licence).
- Texts on the page (intros, email) are in the **EDIT HERE** block near the top of `index.html`.
- Optional: a Drive API key saved as the repository secret `DRIVE_API_KEY` is used to list the folder if Google ever changes its public folder view.
