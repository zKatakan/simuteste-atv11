
import os, time, statistics, requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
ENDPOINTS = [
    "/api/catalog",
    "/api/cart/add",
    "/api/checkout"
]

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

def timed_get(url):
    t0 = time.perf_counter()
    r = requests.get(url, timeout=10)
    dt = (time.perf_counter() - t0) * 1000.0
    return r.status_code, dt

def pctl(values, p):
    if not values: return None
    k = (len(values)-1) * (p/100.0)
    f, c = int(k), min(int(k)+1, len(values)-1)
    if f == c: return sorted(values)[f]
    d0 = sorted(values)[f] * (c-k)
    d1 = sorted(values)[c] * (k-f)
    return d0 + d1

def main():
    print(f"[perf] BASE_URL = {BASE_URL}")
    latencies = []
    codes = []
    for ep in ENDPOINTS:
        url = BASE_URL + ep
        for _ in range(50):
            try:
                code, ms = timed_get(url)
                latencies.append(ms)
                codes.append(code)
            except requests.RequestException as e:
                print(f"[perf] erro: {e}")

    ok_rate = sum(1 for c in codes if 200 <= c < 400) / max(1,len(codes)) * 100
    avg = statistics.mean(latencies) if latencies else None
    p95 = pctl(latencies, 95) if latencies else None
    p99 = pctl(latencies, 99) if latencies else None

    out = {
        "ok_rate_percent": ok_rate,
        "avg_ms": avg,
        "p95_ms": p95,
        "p99_ms": p99,
        "n_samples": len(latencies)
    }
    print("[perf] resultados:", out)

    (RESULTS_DIR / "perf_results.json").write_text(__import__("json").dumps(out, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
