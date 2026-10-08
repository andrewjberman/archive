"""Print the wire status-key sets of served.py's success and refusal envelopes, run from a given package dir.

Usage: python -I envelope_keys.py <package_dir> <label>
Offline only: no route, no network, no AWS call. Imports served.py from <package_dir>.
"""
import json
import sys

pkg, label = sys.argv[1], sys.argv[2]
sys.path.insert(0, pkg)
import served  # noqa: E402

st = served.status_envelope("analysis.submit", "NOT_READY", "corr-probe-0001", state="QUEUED", operation_kind="submit")
ok = served.response_envelope("analysis.submit", "invented-firm", served.NO_DATA, st)
ref = served.refuse("analysis.submit", None, "NOT_AUTHORIZED", "corr-probe-0002")


def status_keys(env):
    body = env
    if isinstance(env, dict) and "body" in env and isinstance(env["body"], str):
        body = json.loads(env["body"])
    status = body.get("status") if isinstance(body, dict) else None
    return sorted(status) if isinstance(status, dict) else repr(type(status))


print(label, "success status keys:", status_keys(ok))
print(label, "refusal status keys:", status_keys(ref))
print(label, "internal_correlation_id on success wire:", "internal_correlation_id" in json.dumps(ok))
print(label, "internal_correlation_id on refusal wire:", "internal_correlation_id" in json.dumps(ref))
