# Palette Mood Analyzer Microservice

Accepts an array of hex color codes and returns mood/genre tags describing the emotional tone of the palette.

---

## Setup

1. Install dependencies:
```
pip install flask
```

2. Start the microservice:
```
python app.py
```

The service runs on **http://localhost:5300**

---

## Communication Contract

### Endpoint: `POST /analyze`

**Request format:**

Send a POST request to `http://localhost:5300/analyze` with a JSON body containing a `colors` key with an array of 1–10 hex color codes.

```json
{
  "colors": ["#1A1A2E", "#E94560", "#0F3460", "#533483"]
}
```

**Example request (Python):**

```python
import requests

response = requests.post(
    "http://localhost:5300/analyze",
    json={"colors": ["#1A1A2E", "#E94560", "#0F3460", "#533483"]}
)
data = response.json()
print(data["moods"])  # e.g. ["gothic", "mysterious"]
```

**Success response (HTTP 200):**

```json
{
  "moods": ["gothic", "mysterious"]
}
```

**Error responses:**

| Scenario | Status | Response |
|---|---|---|
| Missing `colors` key | 400 | `{"error": "Request body must include a 'colors' key..."}` |
| Invalid hex code | 400 | `{"error": "Invalid hex code: '#ZZZZZZ'..."}` |
| Array length < 1 or > 10 | 400 | `{"error": "colors must be an array of 1 to 10 hex codes"}` |

---

### Endpoint: `GET /health`

Returns `{"status": "ok"}` with HTTP 200 to confirm the service is running.

---

## Mood Tags

The microservice may return any of the following mood tags:

`gothic` `whimsical` `romantic` `noir` `fantasy` `serene` `earthy` `energetic` `mysterious` `natural` `neutral`

---

## Notes

- Hex codes must be in `#RRGGBB` format (6 digits, case-insensitive)
- The microservice runs in its own process and is called via HTTP — no direct function imports
- The `moods` array will always contain at least one tag