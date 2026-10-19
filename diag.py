import requests
from bs4 import BeautifulSoup

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ko-KR,ko;q=0.9",
}
BASE = "https://reserv.bucheon.go.kr/site/main"
TESTS = [
    ("main", f"{BASE}/main", {}),
    ("list", f"{BASE}/lending/lendingList",
     {"inst_cate": "01", "lending_inst_nm": "football"}),
    ("detail68", f"{BASE}/lending/lendingDetail",
     {"lending_info_seq": 68, "inst_cate": "01"}),
    ("detail68-nov", f"{BASE}/lending/lendingDetail",
     {"lending_info_seq": 68, "inst_cate": "01", "year": 2026, "month": 11}),
]

try:
    print("runner ip:", requests.get("https://api.ipify.org", timeout=10).text)
except Exception as e:
    print("ip error:", e)

for name, url, params in TESTS:
    for attempt in (1, 2):
        try:
            r = requests.get(url, headers=H, params=params, timeout=(10, 30))
            soup = BeautifulSoup(r.text, "html.parser")
            rows7 = [tr for tr in soup.select("table tr")
                     if len(tr.find_all("td")) == 7]
            i = r.text.find("예약현황")
            print(f"[{name}] status={r.status_code} len={len(r.text)} "
                  f"title={soup.title.string if soup.title else None!r} "
                  f"rows7={len(rows7)} 완료={'예약완료' in r.text} "
                  f"가능={'예약가능' in r.text}")
            print("  head:", repr(r.text[:300]))
            print("  cal :", repr(r.text[i:i + 300]) if i >= 0 else None)
            break
        except Exception as e:
            print(f"[{name}] attempt {attempt} error: "
                  f"{type(e).__name__} {str(e)[:150]}")
