#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-3 battery -- the bounded test principal: precondition, premise gate, and the
STOP it reaches.

Arm (a) PRECONDITION, as the face states it: 2 of 2 never-widen halves at HEAD naming the packet's blob,
the packet re-hashed equal, and both halves naming the same keys (K1, K2).

Arm (a) PREMISE GATE, added because the halves sign a SESSION SHAPE ("a token minted against K1 carries
exactly abby_horton's already-live entitlement"), and whether K1 + K2 can produce that shape is a
property of the DEPLOYED mint path, not of the packet:
  1. the deployed auth-handler's bytes (downloaded; sha256 must equal the live CodeSha256) source the
     token's advisor claim from `opal-partner-<firm>` by `GetItem Key {email}`;
  2. the repo's getUser() mapping at HEAD carries no advisor field from the opal-users-v2 row;
  3. the live partner table's key is `email`, and the number of its rows binding any login to
     advisorKey = abby_horton is counted.
If no partner row binds abby_horton, K1 (a new e-mail) + K2 mint a 49financial session with NO advisor
claim, which is not the entitlement either half signed, and reaching the signed shape needs a
partner-table write the packet does not name. The CTO half's own rule (s.1): a key the act discovers it
needs is "a STOP and a new packet, not a widening of this one". The battery then STOPs: NOTHING is
created, arms (b)-(e) are NOT RUN, and the principal's interval is EMPTY.

Read-only on every live plane. Prints no URL, no e-mail, no token, no secret. Re-derives every value
each run and never reads its own earlier output.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
AWS = os.path.join(WS, ".tools", "aws.cmd")
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-3_R60-AC1_battery_output.txt")
TOKEN = "IBR60-FOUR-OUTCOMES-EXERCISED-AND-PRINCIPAL-DELETED"

PACKET = ("org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/"
          "NEVER_WIDEN_SIGNOFF_PACKET_IB-rte-1.md")
PACKET_BLOB = "3d9f57335b9893753973132ba5c4958b2622e24f"
HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rte-2_TEST_PRINCIPAL.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rte-2_TEST_PRINCIPAL.md",
}
AUTH_FN = "opalinvest-auth-handler"
DB_TS = "infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts"
FIRM = "49financial"
PARTNER_TABLE = "opal-partner-" + FIRM
ADVISOR = "abby_horton"
OM_BUCKET, OM_KEY = "opal-data-bd", "platinum/49financial/ownership_map.json"
CALL_TIMEOUT_S = 180

LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=WS, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=60)
    return out.returncode, out.stdout


def aws(*args: str) -> tuple[int, str, str]:
    try:
        out = subprocess.run([AWS, *args], capture_output=True, text=True, encoding="utf-8",
                             errors="replace", timeout=CALL_TIMEOUT_S)
        return out.returncode, out.stdout, out.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ss" % CALL_TIMEOUT_S


def arm_a_precondition() -> bool:
    emit("(a) PRECONDITION -- halves at HEAD naming the packet blob; packet re-hashed; same keys")
    _, head = git("rev-parse", "HEAD:" + PACKET)
    _, wt = git("hash-object", PACKET)
    packet_ok = head.strip() == PACKET_BLOB and wt.strip() == PACKET_BLOB
    emit("  packet blob at HEAD %s, worktree %s, expected %s -> %s"
         % (head.strip(), wt.strip(), PACKET_BLOB, "EQUAL" if packet_ok else "DIFFERS"))
    n_ok = 0
    for who, path in HALVES.items():
        rc, text = git("show", "HEAD:" + path)
        names_blob = rc == 0 and PACKET_BLOB in text
        keys = [k for k in ("K1", "K2") if re.search(r"\b%s\b" % k, text)] if rc == 0 else []
        ok = names_blob and keys == ["K1", "K2"]
        n_ok += ok
        emit("  %s half at HEAD: present=%s names_packet_blob=%s keys_named=%s -> %s"
             % (who, rc == 0, names_blob, ",".join(keys) or "none", "OK" if ok else "FAIL"))
    emit("  halves: %d of %d at HEAD naming the packet blob and K1+K2" % (n_ok, len(HALVES)))
    return packet_ok and n_ok == len(HALVES)


def arm_a_premise() -> dict:
    emit("(a) PREMISE GATE -- can K1 + K2 mint the SESSION SHAPE the halves sign?")
    res: dict = {}
    rc, so, se = aws("lambda", "get-function-configuration", "--function-name", AUTH_FN,
                     "--query", "CodeSha256", "--output", "text")
    live_sha = so.strip() if rc == 0 else ""
    emit("  1. %s live CodeSha256 = %s (rc %s)" % (AUTH_FN, live_sha or "<unread>", rc))
    rc, so, se = aws("lambda", "get-function", "--function-name", AUTH_FN,
                     "--query", "Code.Location", "--output", "text")
    bundle_ok = partner_lookup = False
    if rc == 0 and so.strip():
        blob = urllib.request.urlopen(so.strip(), timeout=CALL_TIMEOUT_S).read()  # URL never printed
        got = base64.b64encode(hashlib.sha256(blob).digest()).decode()
        bundle_ok = bool(live_sha) and got == live_sha
        emit("     downloaded deployed zip: %d bytes, sha256(b64) %s -> %s live CodeSha256"
             % (len(blob), got, "EQUALS" if bundle_ok else "DIFFERS FROM"))
        zf = zipfile.ZipFile(io.BytesIO(blob))
        js = [n for n in zf.namelist() if n.endswith((".js", ".mjs")) and "node_modules" not in n]
        for n in js:
            text = zf.read(n).decode("utf-8", errors="replace")
            has_table = "`opal-partner-${" in text
            has_email_key = bool(re.search(r"Key:\s*\{\s*email\s*:", text))
            if has_table and has_email_key:
                partner_lookup = True
            emit("     %s: partner-table name builder present=%s, GetItem Key {email:..} present=%s"
                 % (n, has_table, has_email_key))
        emit("     deployed advisor-claim source = opal-partner-<firm> GetItem by e-mail: %s"
             % ("YES" if partner_lookup else "NOT FOUND"))
    else:
        emit("     get-function rc %s: %s" % (rc, se[-200:]))
    res["served_bytes_identified"] = bundle_ok
    res["partner_lookup_by_email"] = partner_lookup

    _, head = git("rev-parse", "--short=10", "HEAD")
    rc, src = git("show", "HEAD:" + DB_TS)
    m = re.search(r"export async function getUser\(email: string\).*?\n  return \{(.*?)\n  \} as User;", src, re.S)
    mapped = m.group(1) if m else ""
    start = src[: m.start(1)].count("\n") + 1 if m else 0
    end = start + mapped.count("\n") if m else 0
    no_advisor = bool(m) and "advisor" not in mapped.lower()
    emit("  2. %s:%d-%d @%s getUser() return mapping: %s"
         % (DB_TS, start, end, head.strip(),
            "carries NO advisor field" if no_advisor else ("carries an advisor field" if m else "NOT FOUND")))
    res["user_row_carries_no_advisor"] = no_advisor

    rc, so, se = aws("dynamodb", "describe-table", "--table-name", PARTNER_TABLE,
                     "--query", "Table.KeySchema", "--output", "json")
    keyschema = json.loads(so) if rc == 0 else []
    email_key = keyschema == [{"AttributeName": "email", "KeyType": "HASH"}]
    emit("  3. %s key schema %s -> hash key is e-mail: %s"
         % (PARTNER_TABLE, json.dumps(keyschema), email_key))
    rc, so, se = aws("dynamodb", "scan", "--table-name", PARTNER_TABLE, "--select", "COUNT",
                     "--filter-expression", "advisorKey = :a",
                     "--expression-attribute-values", json.dumps({":a": {"S": ADVISOR}}),
                     "--output", "json")
    cnt = json.loads(so) if rc == 0 else {}
    bound = cnt.get("Count")
    scanned = cnt.get("ScannedCount")
    emit("     rows binding a login to advisorKey=%s: %s of %s scanned (rc %s)" % (ADVISOR, bound, scanned, rc))
    res["partner_rows_for_advisor"] = bound
    res["partner_rows_scanned"] = scanned
    res["premise_holds"] = not (partner_lookup and email_key and no_advisor and bound == 0)
    emit("  PREMISE: K1 (a new e-mail in opal-users-v2) + K2 mint a %s session carrying %s"
         % (FIRM, "an advisor claim" if res["premise_holds"] else "NO advisor claim"))
    return res


def informational_ownership_map() -> None:
    emit("(info) the live ownership map, read for the re-cut packet's magnitude -- NOT the guard "
         "(no K1 is created)")
    rc, so, se = aws("s3api", "head-object", "--bucket", OM_BUCKET, "--key", OM_KEY,
                     "--query", "{V:VersionId,E:ETag,M:LastModified}", "--output", "json")
    if rc != 0:
        emit("  head-object rc %s: %s" % (rc, se[-200:]))
        return
    head = json.loads(so)
    fd, tmp = tempfile.mkstemp(suffix=".json", dir=os.path.join(WS, ".scratch"))
    os.close(fd)
    try:
        rc, _, se = aws("s3api", "get-object", "--bucket", OM_BUCKET, "--key", OM_KEY,
                        "--version-id", head["V"], tmp)
        with open(tmp, encoding="utf-8") as fh:
            om = json.load(fh)
    finally:
        os.remove(tmp)
    adv = om.get("advisors", {}).get(ADVISOR)
    emit("  s3://%s/%s VersionId %s ETag %s LastModified %s"
         % (OM_BUCKET, OM_KEY, head["V"], head["E"], head["M"]))
    emit("  %s present: %s; accounts %s, relationships %s (packet's run: 43 / 18); advisors in map %d"
         % (ADVISOR, adv is not None, len(adv.get("accounts", [])) if adv else 0,
            len(adv.get("relationships", [])) if adv else 0, len(om.get("advisors", {}))))


def main() -> int:
    _, head = git("rev-parse", "HEAD")
    emit("IB-rtf-3 R60-AC1 battery -- run at %s -- worktree HEAD %s" % (now(), head.strip()))
    emit("")
    pre_ok = arm_a_precondition()
    emit("")
    prem = arm_a_premise()
    emit("")
    informational_ownership_map()
    emit("")
    stop = not pre_ok or not prem["premise_holds"]
    if stop:
        emit("STOP at arm (a): %s" % ("precondition failed" if not pre_ok else
             "the signed keys K1 + K2 cannot produce the session shape both halves sign; reaching it "
             "needs a partner-table row (e-mail -> advisorKey=%s) the packet does not name -- the CTO "
             "half s.1: a STOP and a new packet, not a widening" % ADVISOR))
        emit("(b) CREATE: NOT RUN -- 0 of 2 keys applied; nothing written to opal-users-v2")
        emit("(c) EXERCISE: NOT RUN -- 0 of 4 outcome arms; no session minted, vendor calls 0")
        emit("(d) NEGATIVE CONTROLS: NOT RUN -- no principal to present them")
        emit("(e) DELETE: NOTHING TO DELETE -- the principal's interval is EMPTY (never created)")
        emit("")
        emit("RESULT: R60-AC1 FAIL -- STOP at arm (a); 0 of 4 outcomes exercised; principal never created")
        rc = 1
    else:
        emit("RESULT: R60-AC1 NOT COMPLETE -- the premise holds; arms (b)-(e) are not implemented in this "
             "battery revision and must be run under a ledger entry")
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
