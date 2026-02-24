import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000/api"

def make_request(url, method="GET", data=None):
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header('Content-Type', 'application/json')
        if data:
            req.data = json.dumps(data).encode('utf-8')
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            body = response.read().decode('utf-8')
            return status_code, json.loads(body) if body else {}
    except Exception as e:
        return 0, str(e)

def test_delete_all(resource):
    print(f"Testing deleteAll for {resource}...")
    url = f"{BASE_URL}/{resource}/deleteAll/"
    status, body = make_request(url, method="DELETE")
    if status == 204:
        print(f"[PASS] {resource} deleteAll returned 204")
    else:
        print(f"[FAIL] {resource} deleteAll returned {status}")
        print(body)

if __name__ == "__main__":
    resources = ["stores", "products", "users", "orders", "reviews"]
    for res in resources:
        test_delete_all(res)
