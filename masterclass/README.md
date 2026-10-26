# IITGN Alumni MasterClass website

Live at **https://iitgnalumni.github.io/masterclass/**

A single static page (no build step, no database) that recognises every IITGN alum who has given a MasterClass. It replaces the "Alumni MasterClass" category on the alumni portal.

## What is in this folder

| Path | What it is |
| --- | --- |
| `index.html` | The whole website: design, session data and page logic |
| `posters/` | One poster or photo per MasterClass, named `firstname-lastname.jpg` |
| `images/` | Alumni Relations logo and the campus photo behind the main heading |

## Adding a new MasterClass

1. Save the poster (or a photo from the session) as `posters/firstname-lastname.jpg`.
2. In `index.html`, find `const SESSIONS = [`.
3. Copy the first `{ ... },` entry, paste it directly below `const SESSIONS = [` (newest first) and edit the fields. The field list is in the comment just above it.
4. Commit. GitHub Pages updates the site within a minute or two.

The counts on the page (speakers, sessions, disciplines, sessions per field, "MasterClass #N") update automatically.

After an event, update the same entry: replace the invitation text in `about` with the recap, add `attended`, `quote`, a `recording` link if there is one, and extra photos in `gallery`.

## Sharing a single session

Each session opens in a pop-up and has its own link, e.g. `https://iitgnalumni.github.io/masterclass/#session-17` (numbered from the first MasterClass, Deepti Chopra, as `#session-1`).
