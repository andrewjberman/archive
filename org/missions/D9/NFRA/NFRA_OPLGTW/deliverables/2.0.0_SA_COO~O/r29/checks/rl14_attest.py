"""OPLGTW round 29 -- the attestation instrument for rl14.AC2's host-read record.

  python rl14_attest.py <record.json> <DIGEST_MARKER> <deployed_commit>

A record is {"body": {...}, "ssm_command_id", "instance_id"}. The host printed `<DIGEST_MARKER> <sha256>` in that SSM
invocation's own output, where the digest is sha256(json.dumps(body, sort_keys=True)). The record is then the host's
answer and not a transcription. Prints one line `fields=<yes|no> ssm=<Status> digest=<yes|no>`; exit 0 only on yes/Success/yes.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

FULL_SCOPES = 17
TERMINAL = ("SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED")
IDENTITY_KEYS = {"OG_TAXSMA_WORKBOOK_IDENTITY", "MS_INGEST_IDENTITY", "OTP_MAILBOX"}


def _send_ok(b: dict, deployed: str) -> bool:
    w = b.get("max_inline_wait_s")
    return (b.get("served_release") == deployed and b.get("installed_code") is True
            and b.get("tools_before") == 65 and b.get("tools_after") == 66
            and b.get("status_tool") == "OK" and b.get("status_value") in TERMINAL
            and isinstance(w, (int, float)) and w <= 60
            and b.get("confirm_true_run") is False and b.get("grants_written") == 0)


def _scopes_ok(b: dict, deployed: str) -> bool:
    k = b.get("identity_keys_scoped") or {}
    n = b.get("probes_run")
    return (b.get("served_release") == deployed and b.get("installed_code") is True
            and b.get("unscoped_scope_count") == FULL_SCOPES
            and b.get("scoped_scope_count") in (8, 9) and b.get("scoped_subset_of_full") is True
            and b.get("scoped_silent_acquire") == "OK"
            and isinstance(n, int) and n >= 3 and b.get("probes_ok") == n
            and b.get("sharepoint_site_resolve") == 200
            and set(k) == IDENTITY_KEYS and all(isinstance(v, bool) for v in k.values())
            and b.get("grants_written") == 0)


def _allow_ok(b: dict, deployed: str) -> bool:
    return (b.get("served_release") == deployed and b.get("installed_code") is True
            and b.get("status_tool_allowed_for_scoped") is True and b.get("unnamed_tool_allowed_for_scoped") is False
            and b.get("scoped_scope_count") == 9 and b.get("tools") == 66
            and isinstance(b.get("overlay_rows_before"), int) and b.get("overlay_rows_after") == b["overlay_rows_before"] + 1
            and b.get("grants_written") == 0)


def _read_ok(b: dict, deployed: str) -> bool:
    d = b.get("displayed_date")
    n = b.get("audit_bytes_page")
    return (b.get("served_release") == deployed and b.get("installed_code") is True
            and b.get("tools") == 66 and b.get("scoped_scope_count") == 9
            and b.get("wrapper_status_tool") == "OK"
            and isinstance(d, str) and bool(d.strip()) and d == b.get("manifest_generated_at")
            and b.get("audit_keys_page") == ["day", "route"]
            and b.get("audit_keys_chart_404") == ["day", "fund", "route"]
            and isinstance(n, int) and n > 0 and n == b.get("page_bytes_served")
            and b.get("audit_other_args_kept") == 0
            and b.get("grants_written") == 0)


def _lake_ok(b: dict, deployed: str) -> bool:
    return (b.get("served_release") == deployed and b.get("installed_code") is True
            and b.get("tools") == 66 and b.get("scoped_scope_count") == 9
            and b.get("lake_key_no_ts_time_part_empty") is False
            and b.get("lake_key_no_ts_day_matches_time") is True
            and b.get("lake_key_with_ts_shape_unchanged") is True
            and b.get("records_changed_by_key_builder") == 0
            and b.get("lake_objects_written") == 0
            and b.get("grants_written") == 0)


def _aws(args: list) -> tuple:
    root = Path(__file__).resolve()
    while root != root.parent and not (root / ".tools").is_dir():
        root = root.parent
    shim = root / ".tools" / ("aws.cmd" if sys.platform == "win32" else "aws")
    try:
        p = subprocess.run([str(shim)] + args, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=110)
        return p.returncode, p.stdout or ""
    except Exception as exc:  # an absent reader is a FAIL, never a pass
        return 255, "%s: %s" % (type(exc).__name__, exc)


def main(argv: list) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    try:
        d = json.load(open(argv[1], encoding="utf-8"))
    except Exception as exc:
        print("fields=no ssm=NONE digest=no (record unreadable: %s)" % exc)
        return 1
    b = d.get("body") or {}
    fields = _lake_ok(b, argv[3])
    dig = hashlib.sha256(json.dumps(b, sort_keys=True).encode("utf-8")).hexdigest()
    rc, out = _aws(["ssm", "get-command-invocation", "--command-id", str(d.get("ssm_command_id", "NONE")),
                    "--instance-id", str(d.get("instance_id", "NONE")), "--region", "us-east-1",
                    "--query", "[Status,StandardOutputContent]", "--output", "json"])
    status, found = "NONE", False
    if rc == 0:
        try:
            st, body = json.loads(out)
            status, found = str(st), ("%s %s" % (argv[2], dig)) in (body or "")
        except Exception:
            pass
    print("fields=%s ssm=%s digest=%s" % ("yes" if fields else "no", status, "yes" if found else "no"))
    return 0 if (fields and status == "Success" and found) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
