
import os, requests, json
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "changeme_admin_token")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

def rate_limit_test():
    url = BASE_URL + "/api/catalog"
    codes = []
    for _ in range(130):
        try:
            r = requests.get(url, timeout=5)
            codes.append(r.status_code)
        except Exception:
            codes.append(0)
    too_many = sum(1 for c in codes if c == 429)
    return {"sent": len(codes), "status_429": too_many}

def auth_rbac_tests():
    results = {}
    r = requests.post(BASE_URL + "/auth/login", json={"user":"admin","pass":"wrong"})
    results["login_invalido"] = r.status_code
    r = requests.get(BASE_URL + "/admin")
    results["admin_sem_token"] = r.status_code
    r = requests.get(BASE_URL + "/admin", headers={"Authorization": f"Bearer {ADMIN_TOKEN}"})
    results["admin_com_token"] = r.status_code
    return results

def main():
    rl = rate_limit_test()
    auth = auth_rbac_tests()
    out = {"rate_limit": rl, "auth_rbac": auth}
    (RESULTS_DIR / "security_results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(out)

if __name__ == "__main__":
    main()
