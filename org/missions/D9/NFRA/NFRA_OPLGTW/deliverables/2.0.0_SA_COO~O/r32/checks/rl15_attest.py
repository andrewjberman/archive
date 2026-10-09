"""OPLGTW round 32 -- the attestation instrument for release r29 (OG-rl-15) host reads.

  python rl15_attest.py <record.json> <DIGEST_MARKER> <deployed_commit>

A record is {"body": {...}, "ssm_command_id", "instance_id"}. The host printed `<DIGEST_MARKER> <sha256>` in that SSM
invocation's own output, where the digest is sha256(json.dumps(body, sort_keys=True)); the record is then the host's
answer, not a transcription. The marker picks the field rule:
  RL15_DIGEST  -- the served release, through the INSTALLED code (AC2);
  RL15G_DIGEST -- the 13-month grant write's read-back (AC3).
Prints one line `fields=<yes|no> ssm=<Status> digest=<yes|no>`; exit 0 only on yes/Success/yes.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def _served_ok(b: dict, deployed: str) -> bool:
    # R54: opal_asker_query is SAFE (OG-sf-1). R50: the refresh/code send gate is in the installed oauth_as (OG-rf-1).
    # PRD v2.0 item 4: calendar_months 1..13 and contract 1.4 (OG-cm-1). PRD v1.9 C7: the domain table holds exactly the
    # entries the halves signed (OG-md-1). Z-S67's disarm read: 0 revoked families for the concierge since the deploy.
    return (b.get("served_release") == deployed and b.get("installed_code") is True
            and b.get("asker_query_class") == "SAFE" and b.get("asker_query_write_class") is None
            and b.get("unclassified_registered_tools") == 0
            and b.get("send_gate_in_oauth_as") is True
            and b.get("calendar_months_max") == 13 and b.get("contract_version") == "1.4"
            and isinstance(b.get("mail_domain_entries"), int)
            and b.get("mail_domain_entries") == b.get("mail_domain_entries_signed")
            and b.get("concierge_families_revoked_since_deploy") == 0
            and b.get("bloomberg_tools_allowed") == 5
            and b.get("grants_written") == 0)


def _grants_ok(b: dict, deployed: str) -> bool:
    # The CTO ruling msg 32087: exactly two principals' grants, the reach field only, set to 13 calendar months; no other
    # field or principal; the prior reach recorded per key for rollback.
    return (b.get("served_release") == deployed
            and b.get("principals_changed") == 2
            and b.get("fields_changed") == ["calendar_months"]
            and b.get("calendar_months_after") == [13, 13]
            and b.get("other_principals_changed") == 0
            and isinstance(b.get("prior_reach_recorded"), int) and b.get("prior_reach_recorded") == 2
            and b.get("thirteen_month_read_available_dates_min", 0) >= 1)


RULES = {"RL15_DIGEST": _served_ok, "RL15G_DIGEST": _grants_ok}


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
    if len(argv) != 4 or argv[2] not in RULES:
        print(__doc__)
        return 2
    try:
        d = json.load(open(argv[1], encoding="utf-8"))
    except Exception as exc:
        print("fields=no ssm=NONE digest=no (record unreadable: %s)" % type(exc).__name__)
        return 1
    b = d.get("body") or {}
    fields = RULES[argv[2]](b, argv[3])
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
