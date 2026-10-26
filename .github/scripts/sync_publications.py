#!/usr/bin/env python3
"""
Sync the newsletters and annual reports from Google Drive into the website.

How it works
  * The Drive folder (DRIVE_FOLDER below) must be shared as
    "Anyone with the link can view".
  * Each folder inside it becomes a shelf on the website:
      name contains "palaj"                 -> "Footprints in Palaj" (current newsletter)
      name contains "archive"/"newsletter"  -> "Footprints Archive" (before Oct 2025)
      name contains "report"                -> "Annual Reports"
    any other folder becomes a shelf with the folder's own name. Folders
    inside those (for example one per year) are read too.
  * A Google Sheet in the main folder whose name contains "link" adds PDFs
    that live elsewhere (for example on alumni.iitgn.ac.in). Columns:
    Shelf | Title | PDF link | Date (YYYY-MM).
  * Every PDF (or Google Doc / Slides file) is turned into page images
    for the flip-book, plus a cover picture. Files with "draft" in their
    name are skipped.
  * Files removed from Drive are removed from the website.

Output (inside publications/):
  library.json                 the list the website reads
  library/<drive-id>/cover.webp, p-001.webp, p-002.webp ...

Runs from .github/workflows/sync-publications.yml every hour, or on demand.
If the env var DRIVE_API_KEY is set, the folder is listed through the
Drive API instead of the public folder view (optional fallback).
"""
import datetime as dt
import html
import io
import json
import os
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request

# ---------------- EDIT HERE ----------------
DRIVE_FOLDER = "1bxMzPifuOyF-yhqr3wLpUoR1-L-QlZ7q"  # "Alumni Website – Newsletters & Annual Reports"
PAGE_WIDTH = 1100        # px width of each flip-book page image
PAGE_QUALITY = 70        # WebP quality for pages
COVER_WIDTH = 520        # px width of the cover picture on the shelf
MAX_PAGES = 200          # safety limit per document
# -------------------------------------------

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "publications")
ROOT = os.path.normpath(ROOT)
LIB = os.path.join(ROOT, "library")
INDEX = os.path.join(ROOT, "library.json")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

SHELF_ORDER = ["footprints-in-palaj", "annual-reports", "footprints-archive"]
DEFAULT_SHELVES = [("footprints-in-palaj", "Footprints in Palaj"), ("annual-reports", "Annual Reports"), ("footprints-archive", "Footprints Archive")]
MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def log(*a):
    print(*a, flush=True)


def get(url, binary=False, tries=3):
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
                return data if binary else data.decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 + 3 * k)
    raise last


# ---------------------------------------------------------------- listing
def kind_from_href(href):
    if "/drive/folders/" in href or "/folderview" in href:
        return "folder"
    if "docs.google.com/document/" in href:
        return "gdoc"
    if "docs.google.com/presentation/" in href:
        return "gslides"
    if "docs.google.com/spreadsheets/" in href:
        return "gsheet"
    return "file"


def list_public(folder_id):
    """List a public folder through Drive's embedded folder view (no key needed)."""
    page = get("https://drive.google.com/embeddedfolderview?id=" + folder_id + "#list")
    if "flip-entry" not in page:
        if "accounts.google.com" in page or "storage_access" in page or "ServiceLogin" in page:
            raise PermissionError("folder is not shared as 'Anyone with the link'")
        if "flip-entries" in page:      # shared but empty
            return []
        raise RuntimeError("unexpected folder view page")
    out = []
    for chunk in page.split('class="flip-entry"')[1:]:
        m_id = re.search(r'id="entry-([\w-]+)"', chunk) or re.search(r'/d/([\w-]{20,})', chunk) \
            or re.search(r'folders/([\w-]{20,})', chunk)
        m_href = re.search(r'<a [^>]*href="([^"]+)"', chunk)
        m_title = re.search(r'class="flip-entry-title"[^>]*>(.*?)</div>', chunk, re.S)
        m_mod = re.search(r'class="flip-entry-last-modified"[^>]*>\s*<div>(.*?)</div>', chunk, re.S)
        if not (m_id and m_title):
            continue
        href = html.unescape(m_href.group(1)) if m_href else ""
        out.append({
            "id": m_id.group(1),
            "name": html.unescape(re.sub(r"<[^>]+>", "", m_title.group(1))).strip(),
            "kind": kind_from_href(href),
            "modified": html.unescape(re.sub(r"<[^>]+>", "", m_mod.group(1))).strip() if m_mod else "",
        })
    return out


def list_api(folder_id, key):
    """Optional: list through the Drive API with an API key."""
    out, token = [], ""
    while True:
        q = urllib.parse.urlencode({
            "q": "'%s' in parents and trashed = false" % folder_id,
            "fields": "nextPageToken,files(id,name,mimeType,modifiedTime,size)",
            "pageSize": 1000, "key": key, "pageToken": token,
            "supportsAllDrives": "true", "includeItemsFromAllDrives": "true"})
        data = json.loads(get("https://www.googleapis.com/drive/v3/files?" + q))
        for f in data.get("files", []):
            mt = f["mimeType"]
            kind = {"application/vnd.google-apps.folder": "folder",
                    "application/vnd.google-apps.document": "gdoc",
                    "application/vnd.google-apps.presentation": "gslides",
                    "application/vnd.google-apps.spreadsheet": "gsheet"}.get(mt, "file")
            out.append({"id": f["id"], "name": f["name"], "kind": kind,
                        "modified": f.get("modifiedTime", "") + "|" + f.get("size", "")})
        token = data.get("nextPageToken")
        if not token:
            return out


def list_folder(folder_id):
    key = os.environ.get("DRIVE_API_KEY", "").strip()
    if key:
        try:
            return list_api(folder_id, key)
        except Exception as e:  # noqa: BLE001
            log("  Drive API listing failed, trying the public view:", e)
    return list_public(folder_id)


def shelf_for(folder_name):
    n = folder_name.lower()
    if "palaj" in n:
        return "footprints-in-palaj", "Footprints in Palaj"
    if "archive" in n or "newsletter" in n or "footprint" in n:
        return "footprints-archive", "Footprints Archive"
    if "report" in n:
        return "annual-reports", "Annual Reports"
    slug = re.sub(r"[^a-z0-9]+", "-", n).strip("-") or "other"
    return slug, folder_name.strip()


def walk(folder_id, shelf, depth=0, seen=None):
    seen = seen if seen is not None else set()
    if folder_id in seen or depth > 4:
        return []
    seen.add(folder_id)
    docs = []
    for e in list_folder(folder_id):
        if e["kind"] == "gsheet":
            if depth == 0 and re.search(r"link", e["name"], re.I):
                docs += read_link_sheet(e["id"])
            continue
        if e["kind"] == "folder":
            sub_shelf = shelf if shelf else shelf_for(e["name"])
            docs += walk(e["id"], sub_shelf, depth + 1, seen)
            continue
        if depth == 0:
            continue                      # loose files in the main folder (e.g. the READ ME) are not shown
        if re.search(r"draft|read ?me", e["name"], re.I):
            log("  skip (draft):", e["name"])
            continue
        is_pdf = e["name"].lower().endswith(".pdf") or e["kind"] in ("gdoc", "gslides")
        if not is_pdf:
            log("  skip (not a PDF):", e["name"])
            continue
        e["shelf"] = shelf or ("other", "More")
        docs.append(e)
    return docs


def read_link_sheet(sheet_id):
    """Rows of the 'Website links' sheet: Shelf | Title | PDF link | Date (YYYY-MM)."""
    import csv
    import hashlib
    try:
        text = get("https://docs.google.com/spreadsheets/d/%s/export?format=csv" % sheet_id)
    except Exception as ex:  # noqa: BLE001
        log("  could not read the links sheet:", ex)
        return []
    rows = list(csv.reader(io.StringIO(text)))
    out = []
    for r in rows[1:]:
        r = [c.strip() for c in r] + ["", "", "", ""]
        shelf, title, url, date = r[0], r[1], r[2], r[3]
        if not (title and url.startswith("http")):
            continue
        m = re.search(r"/file/d/([\w-]{20,})", url) or re.search(r"[?&]id=([\w-]{20,})", url)
        if m and "drive.google.com" in url:       # a Drive link pasted in the sheet
            e = {"id": m.group(1), "name": title, "kind": "file", "modified": "sheet|" + date}
        else:
            e = {"id": "w" + hashlib.sha1(url.encode()).hexdigest()[:16], "name": title,
                 "kind": "url", "url": url, "modified": url}
        e["date"] = date
        e["shelf"] = shelf_for(shelf or "More")
        out.append(e)
    log("  links sheet: %d rows" % len(out))
    return out


# ---------------------------------------------------------------- download + render
def download_pdf(e):
    fid = e["id"]
    if e["kind"] == "url":
        urls = [e["url"]]
    elif e["kind"] == "gdoc":
        urls = ["https://docs.google.com/document/d/%s/export?format=pdf" % fid]
    elif e["kind"] == "gslides":
        urls = ["https://docs.google.com/presentation/d/%s/export/pdf" % fid]
    else:
        urls = ["https://drive.usercontent.google.com/download?id=%s&export=download&confirm=t" % fid,
                "https://drive.google.com/uc?export=download&confirm=t&id=%s" % fid]
    for u in urls:
        try:
            data = get(u, binary=True)
        except Exception as ex:  # noqa: BLE001
            log("   download failed:", ex)
            continue
        if data[:5] == b"%PDF-":
            return data
        # big files: Drive shows a "can't scan for viruses" page with a form
        txt = data[:200000].decode("utf-8", "replace")
        m = re.search(r'action="(https://drive\.usercontent\.google\.com/download)"', txt)
        if m:
            params = dict(re.findall(r'name="(\w+)" value="([^"]*)"', txt))
            data = get(m.group(1) + "?" + urllib.parse.urlencode(params), binary=True)
            if data[:5] == b"%PDF-":
                return data
    raise RuntimeError("could not download a PDF (is it shared?)")


def render(e, pdf_bytes):
    import pypdfium2 as pdfium
    from PIL import Image  # noqa: F401  (pypdfium2 returns PIL images)

    out = os.path.join(LIB, e["id"])
    tmp = out + ".tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    pdf = pdfium.PdfDocument(io.BytesIO(pdf_bytes))
    n = min(len(pdf), MAX_PAGES)
    ratios = []
    for i in range(n):
        pg = pdf[i]
        w, h = pg.get_size()
        ratios.append(h / w)
        scale = PAGE_WIDTH / w
        img = pg.render(scale=scale).to_pil().convert("RGB")
        img.save(os.path.join(tmp, "p-%03d.webp" % (i + 1)), quality=PAGE_QUALITY, method=6)
        if i == 0:
            c = img.copy()
            c.thumbnail((COVER_WIDTH, int(COVER_WIDTH * 2)))
            c.save(os.path.join(tmp, "cover.webp"), quality=78, method=6)
        pg.close()
    pdf.close()
    shutil.rmtree(out, ignore_errors=True)
    os.rename(tmp, out)
    # most common ratio = the page shape used by the flip-book
    ratios_r = [round(r, 3) for r in ratios]
    ratio = max(set(ratios_r), key=ratios_r.count)
    return {"pages": n, "ratio": ratio, "bytes": len(pdf_bytes)}


# ---------------------------------------------------------------- metadata
def download_link(e):
    if e["kind"] == "url":
        return e["url"]
    if e["kind"] == "gdoc":
        return "https://docs.google.com/document/d/%s/export?format=pdf" % e["id"]
    if e["kind"] == "gslides":
        return "https://docs.google.com/presentation/d/%s/export/pdf" % e["id"]
    return "https://drive.usercontent.google.com/download?id=%s&export=download" % e["id"]


def date_key(e, title):
    m = re.match(r"^(\d{4})-(\d{1,2})", e.get("date") or "")
    if m:
        return int(m.group(1)) * 100 + int(m.group(2))
    return sort_key(title)


def nice_title(name):
    t = re.sub(r"\.pdf$", "", name, flags=re.I)
    t = t.replace("_", " ")
    t = re.sub(r"\s+", " ", t).strip(" -–")
    t = re.sub(r"\b(final|v\d+)\b", "", t, flags=re.I)
    return re.sub(r"\s+", " ", t).strip(" -–()") or name


def sort_key(title):
    """Newest first: use the latest year in the title, then the latest month."""
    t = title.lower()
    years = [int(y) for y in re.findall(r"(?<!\d)(20\d\d)(?!\d)", t)]
    # "2024-25" style -> 2025
    for a, b in re.findall(r"(?<!\d)(20\d\d)\s*[-–/]\s*(\d\d)(?!\d)", t):
        years.append(int(a[:2] + b))
    year = max(years) if years else 0
    months = [MONTHS[m[:3]] for m in re.findall(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*", t)]
    month = max(months) if months else 0
    return year * 100 + month


def label_year(title):
    t = title
    m = re.search(r"(?<!\d)(20\d\d)\s*[-–/]\s*(20)?(\d\d)(?!\d)", t)
    if m:
        return "%s–%s" % (m.group(1), m.group(3))
    years = re.findall(r"(?<!\d)(20\d\d)(?!\d)", t)
    return max(years) if years else ""


# ---------------------------------------------------------------- main
def main():
    os.makedirs(LIB, exist_ok=True)
    old = {}
    old_meta = {}
    if os.path.exists(INDEX):
        with open(INDEX, encoding="utf-8") as f:
            old_meta = json.load(f)
        old = {d["id"]: d for d in old_meta.get("items", [])}

    log("Listing Drive folder", DRIVE_FOLDER)
    try:
        found = walk(DRIVE_FOLDER, None)
    except PermissionError as e:
        log("STOP:", e)
        write_status("not-shared", old_meta)
        return 0
    log("Found %d documents" % len(found))

    items, changed = [], False
    for e in found:
        prev = old.get(e["id"])
        have_pages = prev and os.path.exists(os.path.join(LIB, e["id"], "p-001.webp"))
        same = prev and prev.get("modified") == e["modified"] and prev.get("name") == e["name"]
        if have_pages and same:
            upd = dict(prev, sort=date_key(e, prev["title"]), download=download_link(e))
            if upd != prev:
                changed = True
            items.append(upd)
            continue
        if have_pages and prev.get("modified") == e["modified"] and prev.get("name") != e["name"]:
            # only renamed: keep the pages, update the title
            prev = dict(prev, name=e["name"], title=nice_title(e["name"]))
            prev["sort"] = date_key(e, prev["title"])
            prev["year"] = label_year(prev["title"])
            items.append(prev)
            changed = True
            continue
        log("- rendering:", e["name"])
        try:
            pdf = download_pdf(e)
            info = render(e, pdf)
        except Exception as ex:  # noqa: BLE001
            log("   failed:", ex)
            if prev and have_pages:
                items.append(prev)          # keep the old copy
            continue
        title = nice_title(e["name"])
        item = {
            "id": e["id"], "name": e["name"], "title": title,
            "shelf": e["shelf"][0], "shelfLabel": e["shelf"][1],
            "kind": e["kind"], "modified": e["modified"],
            "pages": info["pages"], "ratio": info["ratio"], "bytes": info["bytes"],
            "year": label_year(title), "sort": date_key(e, title),
            "download": download_link(e),
            "added": (prev or {}).get("added") or dt.date.today().isoformat(),
        }
        items.append(item)
        changed = True
        log("   %d pages" % info["pages"])

    # shelf/section updates for unchanged files moved between folders
    by_id = {e["id"]: e for e in found}
    for it in items:
        s = by_id[it["id"]]["shelf"]
        if (it.get("shelf"), it.get("shelfLabel")) != s:
            it["shelf"], it["shelfLabel"] = s
            changed = True

    keep = {it["id"] for it in items}
    for d in os.listdir(LIB):
        if d.endswith(".tmp") or (d not in keep and os.path.isdir(os.path.join(LIB, d))):
            log("- removing:", d, old.get(d, {}).get("name", ""))
            shutil.rmtree(os.path.join(LIB, d), ignore_errors=True)
            changed = True
    if set(old) - keep:
        changed = True

    items.sort(key=lambda it: (-(it.get("sort") or 0), it["title"].lower()))
    shelves = []
    for it in items:
        if (it["shelf"], it["shelfLabel"]) not in shelves:
            shelves.append((it["shelf"], it["shelfLabel"]))
    for k, lbl in DEFAULT_SHELVES:
        if k not in [s[0] for s in shelves]:
            shelves.append((k, lbl))
    shelves.sort(key=lambda s: (SHELF_ORDER.index(s[0]) if s[0] in SHELF_ORDER else 99, s[1].lower()))

    meta = {
        "status": "ok",
        "folder": DRIVE_FOLDER,
        "shelves": [{"key": k, "label": lbl} for k, lbl in shelves],
        "items": items,
    }
    # keep the scheduled job alive: GitHub pauses hourly jobs after 60 days
    # without commits, so refresh "checked" once a month even if nothing changed
    last = old_meta.get("checked", "")
    today = dt.date.today().isoformat()
    stale = not last or (dt.date.today() - dt.date.fromisoformat(last)).days >= 30
    if changed or stale or old_meta.get("status") != "ok":
        meta["checked"] = today
        with open(INDEX, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=1)
        log("library.json updated (%d items)" % len(items))
    else:
        log("No changes")
    return 0


def write_status(status, old_meta):
    meta = dict(old_meta) if old_meta else {"shelves": [
        {"key": k, "label": lbl} for k, lbl in DEFAULT_SHELVES], "items": []}
    if meta.get("status") == status:
        return
    meta["status"] = status
    meta["folder"] = DRIVE_FOLDER
    meta["checked"] = dt.date.today().isoformat()
    with open(INDEX, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.exit(main())
