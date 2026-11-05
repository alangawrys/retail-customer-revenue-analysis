from pathlib import Path
import io
import zipfile

import requests

URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"
EXPECTED_FILE = RAW_DIR / "Online Retail.xlsx"

def main():
    if EXPECTED_FILE.exists():
        print(f"Already downloaded: {EXPECTED_FILE}. Skipping.")
        return

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {URL}...")
    response = requests.get(URL, timeout=128)
    response.raise_for_status()

    if not response.content.startswith(b"PK"):
        raise ValueError(f"Download from {URL} is not a zip file. Check the URL.")

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        print("Zip contains:", zf.namelist())
        zf.extractall(RAW_DIR)

    size_mb = EXPECTED_FILE.stat().st_size / 1_000_000
    print(f"Saved {EXPECTED_FILE.name} ({size_mb:.1f} MB) to {RAW_DIR}")

if __name__ == "__main__":
    main()
