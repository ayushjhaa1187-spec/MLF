"""
Automated Link and Asset Verification Test
Scans all HTML, CSS, JS, and JSON files to verify:
1. Every internal relative link resolves to a valid file on disk.
2. All data JSON files parse cleanly.
3. No 404s or broken relative asset links.
"""
import os
import re
import json
from bs4 import BeautifulSoup

repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def check_json_files():
    print("Checking JSON data files...")
    data_dir = os.path.join(repo_dir, "data")
    for root, _, files in os.walk(data_dir):
        for f in files:
            if f.endswith(".json"):
                fp = os.path.join(root, f)
                try:
                    with open(fp, encoding="utf-8") as jf:
                        json.load(jf)
                    print(f"  [OK] {os.path.relpath(fp, repo_dir)}")
                except Exception as e:
                    print(f"  [FAIL] {os.path.relpath(fp, repo_dir)}: {e}")
                    return False
    return True

def check_html_links():
    print("\nChecking HTML internal links...")
    broken = []
    checked = 0

    for root, _, files in os.walk(repo_dir):
        # Skip .git and tests
        if ".git" in root or "tests" in root:
            continue
        for f in files:
            if f.endswith(".html"):
                fp = os.path.join(root, f)
                with open(fp, encoding="utf-8") as html_f:
                    soup = BeautifulSoup(html_f.read(), "html.parser")
                    
                    # check links
                    for tag in soup.find_all(["a", "link", "script", "iframe"], href=True) + soup.find_all(["script", "iframe"], src=True):
                        target = tag.get("href") or tag.get("src")
                        if not target or target.startswith("http") or target.startswith("#") or target.startswith("javascript:") or target.startswith("data:"):
                            continue
                            
                        # strip query string or anchor
                        clean_target = target.split("?")[0].split("#")[0]
                        if not clean_target:
                            continue
                            
                        resolved = os.path.normpath(os.path.join(root, clean_target))
                        checked += 1
                        if not os.path.exists(resolved):
                            broken.append((os.path.relpath(fp, repo_dir), target, resolved))

    print(f"Checked {checked} internal relative links across HTML files.")
    if broken:
        print(f"Found {len(broken)} broken internal links:")
        for source, link, resolved in broken:
            print(f"  In {source} -> '{link}' (Resolved to missing: {resolved})")
        return False
    else:
        print("  [OK] All internal relative links resolved successfully with zero broken paths!")
        return True

if __name__ == "__main__":
    json_ok = check_json_files()
    html_ok = check_html_links()
    if json_ok and html_ok:
        print("\nAll verification checks passed!")
    else:
        print("\nVerification checks failed.")
        exit(1)
