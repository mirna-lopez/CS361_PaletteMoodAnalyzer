import requests

BASE_URL = "http://localhost:5300"

def run_test(name, method, endpoint, payload=None, expected_status=None):
    print(f"\n--- {name} ---")
    try:
        if method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        else:
            response = requests.get(f"{BASE_URL}{endpoint}")

        print(f"Status:   {response.status_code}")
        print(f"Response: {response.json()}")

        if expected_status and response.status_code == expected_status:
            print("PASS")
        elif expected_status:
            print(f"FAIL (expected {expected_status})")
    except Exception as e:
        print(f"ERROR: {e}")


# Test 1: Valid palette with multiple colors
run_test(
    name="Test 1: Valid palette (multiple colors)",
    method="POST",
    endpoint="/analyze",
    payload={"colors": ["#1A1A2E", "#E94560", "#0F3460", "#533483"]},
    expected_status=200
)

# Test 2: Valid single hex code
run_test(
    name="Test 2: Single hex code",
    method="POST",
    endpoint="/analyze",
    payload={"colors": ["#FF6B6B"]},
    expected_status=200
)

# Test 3: Malformed hex code
run_test(
    name="Test 3: Malformed hex code (#ZZZZZZ)",
    method="POST",
    endpoint="/analyze",
    payload={"colors": ["#ZZZZZZ"]},
    expected_status=400
)

# Test 4: Missing 'colors' key
run_test(
    name="Test 4: Missing 'colors' key",
    method="POST",
    endpoint="/analyze",
    payload={"palette": ["#FF0000"]},
    expected_status=400
)

# Test 5: More than 10 colors
run_test(
    name="Test 5: More than 10 colors (batch limit exceeded)",
    method="POST",
    endpoint="/analyze",
    payload={"colors": [f"#{'AB' * 3}" for _ in range(11)]},
    expected_status=400
)

# Test 6: Health check
run_test(
    name="Test 6: Health check",
    method="GET",
    endpoint="/health",
    expected_status=200
)
