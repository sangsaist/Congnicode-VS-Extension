
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

    try:
        response = requests.post(url, json=test_payload)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
