import requests
import json
import sys

BASE_URL = "http://localhost:5001/api/search"

def test_randomization():
    print("Testing Randomization...")
    payload = {
        "language": "python",
        "num_repos": 5
    }

    # First request
    response1 = requests.post(BASE_URL, json=payload)
    if response1.status_code != 200:
        print(f"Request 1 failed: {response1.text}")
        return False
    data1 = response1.json()
    seed1 = data1.get('seed')
    repos1 = [r['full_name'] for r in data1['repositories']]

    print(f"Request 1 Seed: {seed1}")
    print(f"Request 1 Repos: {repos1}")

    # Second request (should generate new seed)
    response2 = requests.post(BASE_URL, json=payload)
    if response2.status_code != 200:
        print(f"Request 2 failed: {response2.text}")
        return False
    data2 = response2.json()
    seed2 = data2.get('seed')
    repos2 = [r['full_name'] for r in data2['repositories']]

    print(f"Request 2 Seed: {seed2}")
    print(f"Request 2 Repos: {repos2}")

    if seed1 == seed2:
        print("FAIL: Seeds are identical!")
        return False

    if repos1 == repos2:
        print("FAIL: Repositories are identical!")
        return False

    print("PASS: Randomization works.")
    return True

def test_pagination():
    print("\nTesting Pagination...")

    # Initial request to get a seed
    payload1 = {
        "language": "javascript",
        "num_repos": 5
    }
    response1 = requests.post(BASE_URL, json=payload1)
    if response1.status_code != 200:
        print(f"Page 1 request failed: {response1.text}")
        return False

    data1 = response1.json()
    if not data1.get('success'):
        print(f"Page 1 API error: {data1.get('error')}")
        return False

    seed = data1.get('seed')
    repos1 = [r['full_name'] for r in data1['repositories']]

    print(f"Page 1 Seed: {seed}")
    print(f"Page 1 Repos: {repos1}")

    # Second page request with same seed
    payload2 = {
        "language": "javascript",
        "num_repos": 5,
        "page": 2,
        "seed": seed
    }
    response2 = requests.post(BASE_URL, json=payload2)
    if response2.status_code != 200:
        print(f"Page 2 request failed: {response2.text}")
        return False

    data2 = response2.json()
    if not data2.get('success'):
        print(f"Page 2 API error: {data2.get('error')}")
        return False

    repos2 = [r['full_name'] for r in data2['repositories']]

    print(f"Page 2 Repos: {repos2}")

    if repos1 == repos2:
        print("FAIL: Page 1 and Page 2 results are identical!")
        return False

    # Check for overlap (should be none ideally, but with small result sets it's possible,
    # but with "javascript" there should be plenty)
    overlap = set(repos1).intersection(set(repos2))
    if overlap:
        print(f"WARNING: Overlap found: {overlap}")

    print("PASS: Pagination works.")
    return True

if __name__ == "__main__":
    try:
        if test_randomization() and test_pagination():
            print("\nALL TESTS PASSED")
            sys.exit(0)
        else:
            print("\nTESTS FAILED")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
