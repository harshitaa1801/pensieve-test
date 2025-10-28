from django.http import HttpResponse, JsonResponse
import time
import random
from datetime import datetime


def raise_500(request):
	"""Endpoint that always raises a server error (500)."""
	raise Exception("Intentional test 500 error")


def delay_random(request):
	"""Endpoint that sleeps for a random 1-3 seconds before responding."""
	secs = random.uniform(1, 3)
	# round to 2 decimals for clarity
	time.sleep(secs)
	return HttpResponse(f"Slept for {secs:.2f} seconds", content_type="text/plain")


def instant(request):
	"""Instant endpoint that returns a simple OK response."""
	return HttpResponse("ok", content_type="text/plain")


def status_json(request):
	"""Returns a small JSON payload with server time and status."""
	payload = {
		"status": "ok",
		"timestamp": datetime.utcnow().isoformat() + "Z",
	}
	return JsonResponse(payload)


def cpu_work(request):
	"""Performs a small CPU-bound task (Fibonacci) to simulate work, then returns result.

	This uses an iterative approach and a small n to keep response time reasonable.
	"""
	n = int(request.GET.get("n", 25))
	# limit n to avoid very long runs
	if n < 0:
		n = 0
	if n > 35:
		n = 35

	a, b = 0, 1
	for _ in range(n):
		a, b = b, a + b

	return JsonResponse({"n": n, "fib": a})


def nested_error(request):
	"""Raise an exception from nested helper calls to produce a multi-frame traceback."""
	def level_one(x):
		return level_two(x)

	def level_two(x):
		return level_three(x)

	def level_three(x):
		# This will raise inside a deeply nested call stack
		raise ValueError(f"Nested error: bad value for x={x}")

	return level_one(42)


def chained_error(request):
	"""Raise an exception that chains another to show __cause__ in traceback."""
	try:
		int("not-an-int")
	except ValueError as exc:
		# wrap and chain the original exception
		raise RuntimeError("Higher level failure while parsing integer") from exc


def key_error_in_helper(request):
	"""Raise a KeyError inside a helper function to generate a clear stack trace."""
	def helper():
		d = {"a": 1}
		return d["missing"]  # KeyError

	return helper()


def bad_request(request):
	"""Return a 400 Bad Request with a helpful message."""
	return HttpResponse("Bad request: this endpoint returns HTTP 400 for testing", status=400, content_type="text/plain")


def not_found(request):
	"""Return a 404 Not Found response."""
	return HttpResponse("Not found: this endpoint returns HTTP 404 for testing", status=404, content_type="text/plain")
