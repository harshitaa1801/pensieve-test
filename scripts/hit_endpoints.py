#!/usr/bin/env python3
"""Hit test endpoints randomly.

Usage:
  ./scripts/hit_endpoints.py [--base-url URL] [--min-hits MIN] [--max-hits MAX] [--duration SECONDS] [--dry-run]

By default this targets http://127.0.0.1:8000 and runs for ~300s (5 minutes), hitting each endpoint 10-15 times.
The script uses only the Python standard library so no extra deps are required.
"""
import argparse
import random
import time
import urllib.request
import urllib.error
from urllib.parse import urljoin


ENDPOINTS = [
    "dive/test/raise-500/",
    "dive/test/delay/",
    "dive/test/instant/",
    "dive/test/status/",
    "dive/test/cpu/",
    "dive/test/raise-nested/",
    "dive/test/raise-chain/",
    "dive/test/raise-key/",
    "dive/test/bad-request/",
    "dive/test/not-found/",
]


def make_calls_list(base_path, min_hits, max_hits):
    calls = []
    for ep in ENDPOINTS:
        n = random.randint(min_hits, max_hits)
        for _ in range(n):
            calls.append(ep)
    random.shuffle(calls)
    return calls


def perform_request(full_url, timeout=30):
    req = urllib.request.Request(full_url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read(200)
            return status, body[:200]
    except urllib.error.HTTPError as e:
        return e.code, getattr(e, 'read', lambda: b'')()
    except Exception as e:
        return None, str(e).encode('utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8003/", help="Base URL of the server")
    parser.add_argument("--min-hits", type=int, default=10, help="Minimum hits per endpoint")
    parser.add_argument("--max-hits", type=int, default=15, help="Maximum hits per endpoint")
    parser.add_argument("--duration", type=float, default=300.0, help="Target total duration in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Do not perform HTTP requests; only simulate schedule")
    args = parser.parse_args()

    calls = make_calls_list(args.base_url, args.min_hits, args.max_hits)
    total_calls = len(calls)
    print(f"Planned total calls: {total_calls}; target duration: {args.duration:.1f}s")

    if total_calls == 0:
        print("No calls scheduled. Exiting.")
        return

    start = time.time()
    for i, ep in enumerate(calls, start=1):
        elapsed = time.time() - start
        remaining_calls = total_calls - i + 1
        remaining_time = max(0.0, args.duration - elapsed)

        # build URL; for cpu endpoint, append a random n param
        if ep.startswith("dive/test/cpu"):
            n = random.randint(10, 30)
            ep_full = f"{ep}?n={n}"
        else:
            ep_full = ep

        full_url = urljoin(args.base_url, ep_full)

        print(f"[{i}/{total_calls}] -> {full_url} (elapsed {elapsed:.1f}s, rem_time {remaining_time:.1f}s)")

        if args.dry_run:
            status, body = ("DRY-RUN", b"")
        else:
            status, body = perform_request(full_url)

        print(f"    result: status={status} body_preview={body!r}")

        # Recompute elapsed and remaining
        elapsed = time.time() - start
        remaining_calls = total_calls - i
        if remaining_calls <= 0:
            break

        # ideal sleep to spread remaining calls across remaining_time
        remaining_time = max(0.0, args.duration - elapsed)
        if remaining_time <= 0:
            sleep = 0.0
        else:
            ideal = remaining_time / remaining_calls
            # add a bit of jitter
            sleep = ideal * random.uniform(0.8, 1.2)

        # cap the sleep to not be excessive
        sleep = max(0.0, min(sleep, args.duration))
        print(f"    sleeping for {sleep:.2f}s before next call")
        time.sleep(sleep)

    total_elapsed = time.time() - start
    print(f"Finished {total_calls} calls in {total_elapsed:.1f}s")


if __name__ == "__main__":
    main()
