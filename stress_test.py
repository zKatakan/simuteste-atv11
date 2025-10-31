
import os, time, requests, json
from dotenv import load_dotenv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TARGET = BASE_URL + "/api/catalog"
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

def do_req(session):
    t0 = time.perf_counter()
    try:
        r = session.get(TARGET, timeout=10)
        ok = (200 <= r.status_code < 400)
    except Exception:
        ok = False
    dt = (time.perf_counter() - t0) * 1000.0
    return ok, dt

def run_phase(concurrency, duration_s=30):
    lat = []
    oks = 0
    total = 0
    end = time.time() + duration_s
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        with requests.Session() as s:
            while time.time() < end:
                futs = [ex.submit(do_req, s) for _ in range(concurrency)]
                for f in as_completed(futs):
                    ok, dt = f.result()
                    lat.append(dt)
                    oks += int(ok)
                    total += 1
    ok_rate = (oks/max(1,total))*100
    lat.sort()
    p95 = lat[int(len(lat)*0.95)] if lat else None
    return {"conc": concurrency, "ok_rate": ok_rate, "p95_ms": p95, "n": total}

def main():
    print(f"[stress] alvo = {TARGET}")
    phases = []
    conc_list = [100, 300, 600, 1200, 2400, 4800, 9600, 15000, 20000]
    for c in conc_list:
        res = run_phase(c, duration_s=15)
        print(res)
        phases.append(res)
        if res["ok_rate"] < 95 or (res["p95_ms"] and res["p95_ms"] > 5000):
            break
    breakpoint_users = phases[-1]["conc"]
    out = {"phases": phases, "breakpoint_users": breakpoint_users}
    (RESULTS_DIR / "stress_results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
