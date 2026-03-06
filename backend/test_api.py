import requests
import json

def test_api():
    url = "http://localhost:5000/analyze"
    test_payload = {
        "code": """
def has_duplicate(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False
""",
        "language": "python",
        "user_id": "test_user_1"
    }

    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=test_payload)
        
        if response.status_code == 200:
            print("✅ Success! Received 200 OK")
            print("Response JSON:")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the Flask server running? (Run 'python app.py' first)")

if __name__ == "__main__":
    test_api()
