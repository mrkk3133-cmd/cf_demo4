import json
import requests
import os

# Local Cloud Function endpoint
FUNCTION_URL = "http://localhost:8080"

# Path to JSON payload file (relative to this testCF directory)
REQUEST_FILE = os.path.join(os.path.dirname(__file__), "df_weatherstack_requestbody.json")

def main():
    if not os.path.exists(REQUEST_FILE):
        print(f"❌ Request file not found: {REQUEST_FILE}")
        return

    with open(REQUEST_FILE, "r") as f:
        payload = json.load(f)

    print(f"📤 Sending request to: {FUNCTION_URL}")
    print(f"📦 Using payload file: {REQUEST_FILE}\n")

    try:
        response = requests.post(FUNCTION_URL, json=payload)
        print("✅ Response status:", response.status_code)
        print("🪄 Response body:\n")
        print(json.dumps(response.json(), indent=2))

    except Exception as e:
        print("❌ Request failed:", str(e))

if __name__ == "__main__":
    main()
