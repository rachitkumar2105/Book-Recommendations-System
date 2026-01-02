import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server():
    for _ in range(10):
        try:
            response = requests.get(f"{BASE_URL}/api/trending")
            if response.status_code == 200:
                print("Server is up!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
        print("Waiting for server...")
    return False

def test_endpoints():
    if not wait_for_server():
        print("Server failed to start.")
        sys.exit(1)

    print("\nTesting /api/trending...")
    res = requests.get(f"{BASE_URL}/api/trending")
    if res.status_code == 200 and len(res.json()) > 0:
        print("SUCCESS: Trending books fetched.")
    else:
        print("FAILURE: Trending books.")

    print("\nTesting /api/books...")
    res = requests.get(f"{BASE_URL}/api/books")
    if res.status_code == 200 and len(res.json()) > 0:
        print("SUCCESS: Book titles fetched.")
    else:
        print("FAILURE: Book titles.")

    print("\nTesting /api/recommend...")
    # Use a known title from the trending list or just hardcode one that exists
    test_title = "The Kitchen God's Wife"
    res = requests.post(f"{BASE_URL}/api/recommend", json={"title": test_title})
    if res.status_code == 200 and len(res.json()) > 0:
        print(f"SUCCESS: Recommendations for '{test_title}' fetched.")
    else:
        print(f"FAILURE: Recommendations for '{test_title}' failed. Status: {res.status_code}")

if __name__ == "__main__":
    test_endpoints()
