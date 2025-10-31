from locust import HttpUser, task, between, events
import os, time, json
from pathlib import Path

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

class EcomUser(HttpUser):
    wait_time = between(2, 5)
    host = os.getenv("BASE_URL", None)

    @task(7)
    def view_catalog(self):
        self.client.get("/api/catalog", name="/api/catalog")

    @task(2)
    def add_to_cart(self):
        payload = {"sku": "BLACK-FRIDAY-123", "qty": 1}
        self.client.post("/api/cart/add", json=payload, name="/api/cart/add")

    @task(1)
    def checkout(self):
        payload = {"payment": "pix", "address": "rua a, 123"}
        self.client.post("/api/checkout", json=payload, name="/api/checkout")

window_counts = []
window_size = 5.0
last = time.time()
counter = 0

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, exception, **kwargs):
    global counter, last
    counter += 1
    now = time.time()
    if now - last >= window_size:
        rps = counter / (now - last)
        window_counts.append(rps)
        counter = 0
        last = now

@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    if window_counts:
        out = {
            "avg_rps": sum(window_counts) / len(window_counts),
            "max_rps": max(window_counts),
            "samples": window_counts
        }
        (RESULTS_DIR / "load_results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
