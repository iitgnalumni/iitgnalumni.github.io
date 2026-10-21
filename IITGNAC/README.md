# IITGN Alumni Collective website

A one-page static website for the IIT Gandhinagar Alumni Collective (IITGN-AC), made for GitHub Pages. No build step, database or plugins.

## Files
- `index.html` – the whole website
- `images/iitgn-campus.jpg` – campus photo beside "About"
- `photos/` – Executive Committee photos
- `.nojekyll` – tells GitHub Pages to serve the files as they are

## Publish on GitHub Pages
1. Create a public repository under the iitgnalumni account (for example `IITGNAC`).
2. Upload everything in this folder so `index.html` sits at the top level.
3. Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)` → Save.
4. After a minute the site is live at `https://iitgnalumni.github.io/IITGNAC`.

## Editing
Open `index.html` (pencil icon on GitHub) and search for **EDIT HERE**.
- `LINKS` – Constitution, Participating Members sheet, membership payment link, the emails shown in "Get in touch" (`contact`), social media.
- `COMMITTEE` – name, degree, role, biography, `linkedin` and `email` of each person. A person's email is shown as text only when filled in; until a LinkedIn link is filled in, its icon shows faded. Everyone is listed as an Office Bearer, one below the other, in the order they appear in COMMITTEE.

## Photos
Each person's photo is `photos/<slug>.jpg` (square, about 600 × 600 px), named exactly:

    abhishek-kandoi.jpg   eepsit-tiwari.jpg      sujay-kadam.jpg
    shashwat-jain.jpg     samarpita-mallick.jpg  ihsan-k.jpg
    jainam-shah.jpg       hyma-balakrishnan.jpg

To change a photo, upload a new file with the same name. If a photo is missing, the person's initials are shown.

Contact: alumnirelations@iitgn.ac.in
