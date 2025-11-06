import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sys
from urllib.parse import urljoin
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


BASE_URL = "https://www.ibps.in/"

def fetch_recruitments_page(session=None):
    s = session or requests.Session()
    # Disable SSL verification for ibps.in (public site)
    resp = s.get(BASE_URL, timeout=15, verify=False)
    resp.raise_for_status()
    return resp.text


def parse_job_rows(html):
    soup = BeautifulSoup(html, "lxml")

    # Strategy: IBPS often posts recruitment as links on the homepage or a "Recruitment" page.
    # We'll try to find anchor tags under sections that look like "latest" or "career" or list of posts.
    items = []

    # first, try to find links that look like jobs: anchor tags with "Recruitment" or "Recruit" or "Notification"
    anchors = soup.find_all("a", href=True)
    candidate_anchors = []
    keywords = ("recruit", "recruitment", "notification", "career", "vacancy", "advertisement", "apply")
    for a in anchors:
        txt = (a.get_text(separator=" ", strip=True) or "").lower()
        href = a["href"]
        if any(k in txt for k in keywords) or any(k in href.lower() for k in keywords):
            candidate_anchors.append(a)

    # Deduplicate by href
    seen = set()
    for a in candidate_anchors:
        href = a["href"]
        if href in seen:
            continue
        seen.add(href)
        title = a.get_text(strip=True) or "IBPS Notification"
        link = urljoin(BASE_URL, href)
        # try to fetch the linked page to extract date and location if available
        post_date, location = None, None
        try:
            resp = requests.get(link, timeout=12)
            if resp.status_code == 200:
                sub_soup = BeautifulSoup(resp.text, "lxml")
                # try to find date-like strings
                # common patterns: "Published on 01 Jan 2025", or meta tags
                # check meta tags
                if sub_soup.find("meta", {"name": "date"}):
                    post_date = sub_soup.find("meta", {"name": "date"}).get("content")
                if not post_date:
                    # search for text nodes with date-like patterns (YYYY or dd Mon yyyy)
                    import re
                    text = sub_soup.get_text(" ", strip=True)
                    # look for patterns like 01 January 2025 or 01-01-2025 or 2025
                    m = re.search(r"\b(?:\d{1,2}[ \-\/](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[ \-\/]\d{4}|\d{2}[ \-\/]\d{2}[ \-\/]\d{4}|\d{4})\b", text, re.IGNORECASE)
                    if m:
                        post_date = m.group(0)
                # try find location words near headings
                # naive search for "location" label
                loc_label = sub_soup.find(text=lambda t: t and "Location" in t)
                if loc_label:
                    # if it's like "Location: Mumbai"
                    import re
                    m = re.search(r"Location[:\-\s]*([A-Za-z ,\-]+)", loc_label)
                    if m:
                        location = m.group(1).strip()
                # fallback: try to pick the first occurrence of city names? skip for simplicity
            else:
                pass
        except Exception:
            pass

        items.append({
            "job_title": title,
            "location": location,
            "post_date": post_date,
            "link": link,
            "scraped_at": datetime.datetime.now(datetime.UTC).isoformat()

        })

    # If candidate_anchors empty, fallback: try to look for "news-list" style items
    if not items:
        # attempt another heuristic: find lists with 'news' or 'latest' in class
        sections = soup.find_all(lambda tag: tag.name in ("div", "section", "ul") and ("news" in " ".join(tag.get("class", [])).lower() or "latest" in " ".join(tag.get("class", [])).lower()))
        for sec in sections:
            for li in sec.find_all("a", href=True):
                href = li["href"]
                title = li.get_text(strip=True) or "IBPS Notification"
                if href in seen:
                    continue
                seen.add(href)
                items.append({
                    "job_title": title,
                    "location": "",
                    "post_date": "",
                    "link": urljoin(BASE_URL, href),
                    "scraped_at": datetime.datetime.utcnow().isoformat() + "Z"
                })

    return items

def save_to_csv(items, filename="ibps_jobs.csv"):
    df = pd.DataFrame(items)
    # ensure column order
    cols = ["job_title", "location", "post_date", "link", "scraped_at"]
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    df = df[cols]
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} rows to {filename}")

def main():
    try:
        html = fetch_recruitments_page()
        items = parse_job_rows(html)
        if not items:
            print("No job links found with the heuristics. You may need to update scraping heuristics.")
        save_to_csv(items)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()