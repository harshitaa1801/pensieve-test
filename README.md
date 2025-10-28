# pensieve-test

Small Django project used to exercise and test HTTP endpoints.

This repository provides a set of simple test endpoints in the `dive` app (500/400/404, delayed, instant, and small CPU work) and a small executable script that calls them repeatedly to generate data for testing out my `pensivium` python package.

## Quick start

Prerequisites

- Python 3.10+ (this repo was developed with Python 3.10)
- A virtualenv or other isolated environment is recommended

Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the development server (from repo root):

```bash
# default Django dev server port
python3 manage.py runserver 8003
```

If you prefer the usual 8000 port:

```bash
python3 manage.py runserver 8000
```

## Test endpoints
All endpoints are mounted under `/dive/test/`.

- `/dive/test/raise-500/` — raises an exception to produce HTTP 500 and a traceback (useful when DEBUG=True)
- `/dive/test/raise-nested/` — raises a ValueError from a nested call stack (multi-frame traceback)
- `/dive/test/raise-chain/` — raises a RuntimeError chained from a ValueError (shows __cause__)
- `/dive/test/raise-key/` — raises a KeyError inside a helper function
- `/dive/test/bad-request/` — returns HTTP 400 with a plain-text message
- `/dive/test/not-found/` — returns HTTP 404 with a plain-text message
- `/dive/test/delay/` — sleeps a random 1–3 seconds then returns how long it slept
- `/dive/test/instant/` — returns `ok` immediately
- `/dive/test/status/` — returns JSON with a UTC timestamp and status
- `/dive/test/cpu/?n=<int>` — computes Fibonacci(n) and returns it as JSON (default `n=25`, capped at 35)

Examples (assuming server at http://127.0.0.1:8003):

```bash
curl -i http://127.0.0.1:8003/dive/test/instant/
curl -i http://127.0.0.1:8003/dive/test/delay/
curl -i http://127.0.0.1:8003/dive/test/status/
curl -i "http://127.0.0.1:8003/dive/test/cpu/?n=20"
curl -i http://127.0.0.1:8003/dive/test/raise-500/   # will produce a 500 (DEBUG=True shows traceback)
curl -i http://127.0.0.1:8003/dive/test/bad-request/  # 400
curl -i http://127.0.0.1:8003/dive/test/not-found/   # 404
```

## Load / smoke script

The repository includes `scripts/hit_endpoints.py`, an executable script that schedules and performs multiple requests against the endpoints. It is intentionally simple and uses the Python standard library (urllib) so no additional packages are required.

Basic usage

```bash
# default: base url http://127.0.0.1:8003/ -- hits each endpoint 10-15 times and spreads calls across 300s
python3 scripts/hit_endpoints.py --duration 300

# dry-run (do not make network calls) for quick verification
python3 scripts/hit_endpoints.py --dry-run --duration 10

# specify a different base url (e.g., default Django port 8000)
python3 scripts/hit_endpoints.py --base-url http://127.0.0.1:8000/ --duration 300

# change per-endpoint min/max hits
python3 scripts/hit_endpoints.py --min-hits 5 --max-hits 8 --duration 120
```

Options

- `--base-url` — base server URL (default `http://127.0.0.1:8003/` in the script)
- `--min-hits` / `--max-hits` — integer range of how many times to hit each endpoint (default 10–15)
- `--duration` — target total run duration in seconds (default 300)
- `--dry-run` — simulate schedule without making HTTP requests


Generated on 2025-10-28 by the local workspace tooling.
