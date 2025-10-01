import requests, sys, time, os

API = os.getenv("API_URL", "http://localhost:8000")

def process_file(path, target="original", store=False):
    links = [ln.strip() for ln in open(path, encoding="utf-8") if ln.strip()]
    for i, url in enumerate(links, 1):
        body = {"youtube_url": url, "target_lang": target, "max_minutes": 60, "store": store, "prefer_captions": True, "export_format": ["txt"]}
        print(f"[{i}/{len(links)}] {url}")
        try:
            r = requests.post(f"{API}/transcribe", json=body, timeout=3600)
            if r.ok:
                print("  ok:", r.json().get("title"))
            else:
                print("  fail:", r.text)
        except Exception as e:
            print("  fail:", e)
        time.sleep(1)

if __name__ == "__main__":
    process_file(sys.argv[1] if len(sys.argv)>1 else "links.txt")
