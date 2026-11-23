#!/usr/bin/env python3
"""Publish due Instagram reels from ig-queue.json (media branch). Runs in GitHub Actions."""
import datetime, json, os, sys, time, urllib.parse, urllib.request

TOKEN = os.environ["IG_TOKEN"]; UID = os.environ["IG_USER_ID"]
QUEUE = sys.argv[1] if len(sys.argv) > 1 else "ig-queue.json"
MEDIA_BASE = os.environ.get("MEDIA_BASE", "https://media.keepseeingnumbers-site.pages.dev/")
API = "https://graph.facebook.com/v21.0/"

def call(method, path, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = API + path
    req = urllib.request.Request(url + ("?" + data.decode() if method == "GET" else ""), data=None if method == "GET" else data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode()[:400].replace(TOKEN, "***"))

q = json.load(open(QUEUE)); now = datetime.datetime.now(datetime.timezone.utc); changed = False
for p in q["posts"]:
    if p.get("status") != "approved": continue
    if datetime.datetime.fromisoformat(p["publish_at"].replace("Z", "+00:00")) > now: continue
    try:
        if p.get("type") == "carousel":
            kids = [call("POST", f"{UID}/media", image_url=MEDIA_BASE + f, is_carousel_item="true")["id"] for f in p["files"]]
            for k in kids:
                for _ in range(20):
                    if call("GET", k, fields="status_code").get("status_code") == "FINISHED": break
                    time.sleep(3)
            c = call("POST", f"{UID}/media", media_type="CAROUSEL", children=",".join(kids), caption=p["caption"])
        else:
            c = call("POST", f"{UID}/media", media_type="REELS", video_url=MEDIA_BASE + p["file"], caption=p["caption"], share_to_feed="true")
        cid = c["id"]
        for _ in range(40):
            st = call("GET", cid, fields="status_code,status")
            if st.get("status_code") == "FINISHED": break
            if st.get("status_code") == "ERROR": raise RuntimeError("processing error: " + json.dumps(st))
            time.sleep(15)
        else: raise RuntimeError("timeout waiting for video processing")
        pub = call("POST", f"{UID}/media_publish", creation_id=cid)
        info = call("GET", pub["id"], fields="permalink")
        p.update(status="published", media_id=pub["id"], permalink=info.get("permalink"), published_at=now.isoformat())
        print("published", p["id"], info.get("permalink"))
    except Exception as e:
        p.update(status="failed", error=str(e)[:400], failed_at=now.isoformat()); print("FAILED", p["id"], e)
    changed = True
json.dump(q, open(QUEUE, "w"), ensure_ascii=False, indent=1)
print("changed" if changed else "nothing due")
