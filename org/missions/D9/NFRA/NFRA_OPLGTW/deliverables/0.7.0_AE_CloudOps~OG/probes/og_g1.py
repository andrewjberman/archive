"""NFRA_OPLGTW TO-OG-g-1 (cell OG-g-1) -- the six mechanical criteria of gate G-C's evidence.

Usage: python <this file> AC1|AC2|AC3|AC4|AC5|AC6

Each run prints its measurement WITH the denominator it was taken against, then exactly one line
`VERDICT: PASS-GCG1-AC<n>` or `VERDICT: FAIL-GCG1-AC<n> <reason>`. Every instrument failure is a FAIL
with its cause named -- never a silent pass, because an absent reader and a true negative read alike.

Run from the worktree root. Each criterion finishes inside 110 s.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[8]
_SEAT = _REPO / "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~OG"
_EVIDENCE = _SEAT / "G-C_CONTROLLED_IDENTITY_AND_GRANT_EVIDENCE.md"
_CANDIDATE = _SEAT / "grant_candidate_scope.json"
_RESULT = _SEAT / "controlled-identity-and-grant.result.md"
_SEAL = _REPO / "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~10/SEALED_EXPECTED_V2.json"
_CONTRACT = _REPO / "org/standards/NFRA_OPLGTW_CONTRACT.json"
_GATEWAY = _REPO / "infra/aws/ec2/opal-gateway"
_INSTANCE = "i-07dccb1615503ac99"
_TABLE = "gateway-access-state-table"
# A2: the candidate's account ids live ONLY here, outside the repository, alongside the route
# WALKTHROUGH_PROTOCOL.md section 2 already uses for real-data answers.
_OFFREPO = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "opal" / "og-salt" / "og_g1_candidate.json"

_GUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
_PLACEHOLDER = re.compile(r"<|>|REDACT|PLACEHOLDER|TODO|TBD|FIXME|XXXX|ABSENT|NONE|N/A", re.I)
_ZERO_GUID = "00000000-0000-0000-0000-000000000000"


def _out(name, ok, reason=""):
    print("VERDICT: %s-GCG1-%s%s" % ("PASS" if ok else "FAIL", name, ("" if ok else " " + reason)))
    return 0 if ok else 1


def _aws(args):
    """The repo's aws shim. Returns (rc, stdout, stderr) -- never raises, so a broken instrument is
    reported as a FAIL rather than a traceback.

    `.tools/aws` is a bash script: native Windows Python cannot exec it ('%1 is not a valid Win32
    application'), so the `.cmd` forwarder is resolved first on win32. Every argument stays on ONE line --
    aws.cmd truncates a multi-line argv value at the first newline and still returns rc=0.
    """
    cands = []
    if sys.platform == "win32":
        cands.append(_REPO / ".tools" / "aws.cmd")
    cands.append(_REPO / ".tools" / "aws")
    shim = next((c for c in cands if c.exists()), None)
    if shim is None:
        return 255, "", "no aws shim found at %s" % ", ".join(str(c) for c in cands)
    for a in args:
        if "\n" in a:
            return 255, "", "refusing a multi-line argv value (aws.cmd truncates it silently)"
    try:
        p = subprocess.run([str(shim)] + args, capture_output=True, text=True, timeout=95,
                           cwd=str(_REPO), shell=False)
        return p.returncode, p.stdout, p.stderr
    except Exception as exc:  # noqa: BLE001 -- the cause is printed and graded as a FAIL
        return 255, "", "shim invocation failed: %r" % (exc,)


def _identity_from_evidence():
    """(tid, oid, instrument, quoted_output_present) as the evidence file records them. Any field the
    file does not carry comes back None, which every caller grades as a FAIL rather than skipping."""
    if not _EVIDENCE.exists():
        return None, None, None, False
    text = _EVIDENCE.read_text(encoding="utf-8")
    def field(label):
        # capture the whole value: an instrument name legitimately carries backticks of its own, so a
        # backtick-excluding class truncates it to nothing and reads as ABSENT.
        m = re.search(r"^\s*-\s*\*\*%s:\*\*[ \t]*(.+?)[ \t]*$" % re.escape(label), text, re.M)
        if not m:
            return None
        return m.group(1).strip().strip("`").strip() or None
    tid = field("controlled_tid")
    oid = field("controlled_oid")
    instrument = field("instrument")
    quoted = "```" in text and re.search(r"INSTRUMENT OUTPUT, VERBATIM", text) is not None
    return tid, oid, instrument, quoted


def _evidence_field(label):
    """One `- **<label>:** <value>` line from the evidence file, or None."""
    if not _EVIDENCE.exists():
        return None
    m = re.search(r"^\s*-\s*\*\*%s:\*\*[ 	]*(.+?)[ 	]*$" % re.escape(label),
                  _EVIDENCE.read_text(encoding="utf-8"), re.M)
    return (m.group(1).strip().strip("`").strip() or None) if m else None


# --- AC1: the identity is recorded, as canonical GUIDs, with its instrument and that instrument's output
def ac1():
    required = ["controlled_tid", "controlled_oid", "instrument", "verbatim instrument output"]
    tid, oid, instrument, quoted = _identity_from_evidence()
    found = {"controlled_tid": tid, "controlled_oid": oid, "instrument": instrument,
             "verbatim instrument output": "present" if quoted else None}
    have = [k for k, v in found.items() if v]
    print("evidence file: %s (%s)" % (_EVIDENCE.relative_to(_REPO), "present" if _EVIDENCE.exists() else "ABSENT"))
    print("required identity fields: %d" % len(required))
    for k in required:
        v = found.get(k)
        print("  %-26s %s" % (k, v if v else "<<ABSENT>>"))
    print("fields found: %d of %d" % (len(have), len(required)))
    missing = [k for k in required if not found.get(k)]
    if missing:
        return _out("AC1", False, "%d of %d required field(s) absent: %s" % (len(missing), len(required), ",".join(missing)))
    for label, val in (("controlled_tid", tid), ("controlled_oid", oid)):
        if _PLACEHOLDER.search(val):
            return _out("AC1", False, "%s is a placeholder (%r)" % (label, val))
        if not _GUID.match(val):
            return _out("AC1", False, "%s is not a canonical GUID (%r)" % (label, val))
        if val == _ZERO_GUID:
            return _out("AC1", False, "%s is the all-zero GUID" % label)
    return _out("AC1", True)


# --- AC2: the identity is NOT privileged on the LIVE gateway
def ac2():
    keys = ["MASTER_ADMIN_EMAILS", "WRITE_CAPABLE_EMAILS", "MASTER_ADMIN_PRINCIPALS", "WRITE_CAPABLE_PRINCIPALS"]
    cmds = ['ENV=/opt/opal-gateway/.env', 'if [ ! -f "$ENV" ]; then echo RESULT=NO-ENV; exit 0; fi']
    cmds.append('for k in %s; do v=$(sed -n "s/^$k=//p" "$ENV"); if [ -n "$v" ]; then echo "$k=$v"; '
                'else echo "$k=<<ABSENT>>"; fi; done' % " ".join(keys))
    cmds.append('echo CONTROL_AWS_REGION=$(sed -n "s/^AWS_REGION=//p" "$ENV")')
    payload = {"InstanceIds": [_INSTANCE], "DocumentName": "AWS-RunShellScript", "Parameters": {"commands": cmds}}
    tmp = _SEAT / "probes" / ".ac2_ssm.json"
    tmp.write_text(json.dumps(payload), encoding="utf-8")
    try:
        rc, so, se = _aws(["ssm", "send-command", "--cli-input-json", "file://" + str(tmp).replace("\\", "/"),
                           "--query", "Command.CommandId", "--output", "text"])
        if rc != 0 or not so.strip():
            return _out("AC2", False, "deployed-roster read could not be issued (rc=%d): %s" % (rc, (se or so).strip()[:200]))
        cid = so.strip()
        import time
        text = ""
        for _ in range(18):
            time.sleep(4)
            rc2, so2, se2 = _aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", _INSTANCE,
                                  "--query", "{s:Status,o:StandardOutputContent}", "--output", "json"])
            if rc2 != 0:
                continue
            try:
                got = json.loads(so2)
            except ValueError:
                continue
            if got.get("s") in ("Success", "Failed", "TimedOut", "Cancelled"):
                text = got.get("o") or ""
                if got.get("s") != "Success":
                    return _out("AC2", False, "deployed-roster read ended %s" % got.get("s"))
                break
        else:
            return _out("AC2", False, "deployed-roster read did not reach a terminal state inside the probe budget")
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass
    if "CONTROL_AWS_REGION=us-east-1" not in text:
        return _out("AC2", False, "positive control absent from the deployed read -- the instrument, not the world")
    rosters = {}
    for line in text.splitlines():
        for k in keys:
            if line.startswith(k + "="):
                v = line[len(k) + 1:].strip()
                rosters[k] = [] if v == "<<ABSENT>>" else [e.strip().lower() for e in v.split(",") if e.strip()]
    entries = sum(len(v) for v in rosters.values())
    print("deployed rosters read from the live host (positive control returned):")
    for k in keys:
        v = rosters.get(k)
        print("  %-26s %s" % (k, "<<ABSENT FROM DEPLOYED ENV>>" if not v else ",".join(v)))
    print("roster entries checked (denominator): %d across %d roster(s) present" % (entries, len([1 for v in rosters.values() if v])))
    tid, oid, _i, _q = _identity_from_evidence()
    email = None
    if _EVIDENCE.exists():
        m = re.search(r"^\s*-\s*\*\*controlled_upn:\*\*\s*`?([^`\n]+?)`?\s*$", _EVIDENCE.read_text(encoding="utf-8"), re.M)
        email = m.group(1).strip().lower() if m else None
    print("identity under test: upn=%s oid=%s" % (email or "<<ABSENT>>", oid or "<<ABSENT>>"))
    if not email or not oid or _PLACEHOLDER.search(email) or _PLACEHOLDER.search(oid or ""):
        return _out("AC2", False, "no controlled identity recorded, so the comparison cannot be made "
                                  "(an absent identity is not a non-privileged one)")
    hits = []
    for k, v in rosters.items():
        if email in v:
            hits.append("%s names the upn" % k)
        if oid.lower() in v or ("%s#%s" % ((tid or "").lower(), oid.lower())) in v:
            hits.append("%s names the principal" % k)
    if hits:
        return _out("AC2", False, "identity IS privileged: " + "; ".join(hits))
    print("matches against %d roster entries: 0" % entries)
    return _out("AC2", True)


# --- AC3: the OFF-REPO candidate passes the operator command's own validation, and the committed
#     redacted diff is provably the same diff as the unredacted one (AMENDMENT A2, ruling @8bf2bf37c6)
def ac3():
    """A2 replaced AC3's original form. The CLI has no `prepare` subcommand (row NFRA_OPLGTW-Z-S9), so the
    probe imports the module and calls `validate_candidate` -- the function `activate` itself runs first.
    AC6 wins over a verbatim diff (row NFRA_OPLGTW-Z-S10): the evidence file carries the diff with every
    account identifier REDACTED plus the SHA-256 of the UNREDACTED diff, and this probe recomputes the
    unredacted diff from the off-repo candidate and compares that SHA-256. No write of any kind."""
    if not _CANDIDATE.exists():
        return _out("AC3", False, "no grant candidate recorded at %s" % _CANDIDATE.relative_to(_REPO))
    print("validator: ops/schwab_entitlement_admin.py validate_candidate (the function `activate` runs first)")
    print("note: the CLI exposes activate|revoke|deny-backfill -- there is NO `prepare` subcommand (row NFRA_OPLGTW-Z-S9)")
    print("off-repo candidate (A2: the ids never enter the repo): %s" % _OFFREPO)
    if not _OFFREPO.exists():
        print("  state: ABSENT")
        print("  denominator: 1 off-repo candidate required, 0 present")
        return _out("AC3", False, "the off-repo candidate does not exist -- it is keyed by the controlled "
                                  "identity's tid/oid, which does not exist yet (see AC1); nothing to validate")
    recorded_sha = _evidence_field("unredacted_diff_sha256")
    if not recorded_sha or _PLACEHOLDER.search(recorded_sha):
        return _out("AC3", False, "the evidence file records no unredacted_diff_sha256 to compare against")
    sys.path.insert(0, str(_GATEWAY))
    try:
        from ops import schwab_entitlement_admin as adm
    except Exception as exc:  # noqa: BLE001
        return _out("AC3", False, "the operator command is not importable: %r" % (exc,))
    contract = json.loads(_CONTRACT.read_text(encoding="utf-8"))
    cand = json.loads(_OFFREPO.read_text(encoding="utf-8"))
    try:
        _principal, scope = adm.validate_candidate(cand, contract)
    except Exception as exc:  # noqa: BLE001
        print("  validate_candidate: REJECTED -- %r" % (exc,))
        return _out("AC3", False, "the off-repo candidate is refused by the command's own validation")
    counts = {m: len(v) for m, v in sorted(scope.accounts.items())}
    print("  validate_candidate: ACCEPTED -- masters=%d datasets=%d dates=%s(%d) operations=%d"
          % (len(scope.masters), len(scope.datasets), scope.date_mode, len(scope.dates), len(scope.operations)))
    print("  account COUNT per master (never an identifier): %s" % counts)
    # the UNREDACTED diff, recomputed here and never printed
    diff = adm.scope_diff(None, scope)
    unredacted = adm.format_diff(diff)
    got = hashlib.sha256(unredacted.encode("utf-8")).hexdigest()
    print("  unredacted diff: %d bytes, sha256 recomputed (the text itself is never printed)" % len(unredacted))
    print("  recorded sha256: %s" % recorded_sha)
    print("  recomputed      : %s" % got)
    if got.lower() != recorded_sha.strip().lower():
        return _out("AC3", False, "the recomputed unredacted-diff sha256 does not match the one recorded -- "
                                  "the committed redacted diff is not a redaction of THIS candidate")
    # and the committed diff must actually be redacted
    ev = _EVIDENCE.read_text(encoding="utf-8")
    leaked = [m for m, ids in scope.accounts.items() for i in list(ids)[:200] if i in ev]
    print("  committed evidence scanned for any account identifier of the candidate: %d leak(s)" % len(leaked))
    if leaked:
        return _out("AC3", False, "%d account identifier(s) from the candidate appear in the committed "
                                  "evidence file" % len(leaked))
    return _out("AC3", True)


# --- AC4: the grant is ACTIVE in the live table, by a STRONG read of POLICY#<tid>#<oid>
def ac4():
    tid, oid, _i, _q = _identity_from_evidence()
    if not tid or not oid or _PLACEHOLDER.search(tid) or _PLACEHOLDER.search(oid):
        print("principal key: POLICY#<tid>#<oid> -- NOT CONSTRUCTIBLE (identity absent)")
        return _out("AC4", False, "no identity recorded, so no principal key exists to read back "
                                  "(and this order performed no live write)")
    pk = "POLICY#%s#%s" % (tid, oid)
    rc, so, se = _aws(["dynamodb", "query", "--table-name", _TABLE,
                       "--key-condition-expression", "pk = :p",
                       "--expression-attribute-values", json.dumps({":p": {"S": pk}}),
                       "--consistent-read", "--output", "json"])
    if rc != 0:
        return _out("AC4", False, "strong read failed (rc=%d): %s" % (rc, (se or so).strip()[:200]))
    items = json.loads(so).get("Items", [])
    print("strong consistent read of %s: %d item(s)" % (pk, len(items)))
    prof = next((i for i in items if i.get("sk", {}).get("S") == "principal_profile"), None)
    if prof is None:
        return _out("AC4", False, "no principal_profile at %s (denominator %d items read)" % (pk, len(items)))
    status = prof.get("status", {}).get("S")
    grev = prof.get("grant_revision", {}).get("N")
    print("  profile status=%s grant_revision=%s" % (status, grev))
    if status != "active":
        return _out("AC4", False, "profile status is %r, not 'active'" % status)
    grant = next((i for i in items if i.get("sk", {}).get("S") == "data_entitlement#%010d" % int(grev)), None)
    if grant is None:
        return _out("AC4", False, "grant_revision %s names a data_entitlement record that does not exist" % grev)
    recorded = json.loads(_CANDIDATE.read_text(encoding="utf-8"))["scope"]
    live = _ddb_plain(grant.get("scope", {}))
    dims = ["masters", "datasets", "dates", "columns", "operations", "accounts"]
    diffs = []
    for d in dims:
        a, b = _norm(recorded.get(d)), _norm(live.get(d))
        same = a == b
        print("  %-11s recorded==live: %s" % (d, same))
        if not same:
            diffs.append(d)
    print("scope dimensions compared (denominator): %d; equal: %d" % (len(dims), len(dims) - len(diffs)))
    if diffs:
        return _out("AC4", False, "%d of %d scope dimension(s) differ: %s" % (len(diffs), len(dims), ",".join(diffs)))
    return _out("AC4", True)


def _ddb_plain(v):
    if not isinstance(v, dict):
        return v
    if len(v) == 1:
        (t, val), = v.items()
        if t == "S":
            return val
        if t == "N":
            return val
        if t == "L":
            return [_ddb_plain(x) for x in val]
        if t == "M":
            return {k: _ddb_plain(x) for k, x in val.items()}
        if t == "BOOL":
            return val
        if t == "NULL":
            return None
    return {k: _ddb_plain(x) for k, x in v.items()}


def _norm(v):
    if isinstance(v, list):
        return sorted(_norm(x) for x in v)
    if isinstance(v, dict):
        return {k: _norm(x) for k, x in sorted(v.items())}
    return v


# --- AC5: the scope covers what the walkthrough asks
def ac5():
    if not _CANDIDATE.exists():
        return _out("AC5", False, "no grant candidate recorded")
    scope = json.loads(_CANDIDATE.read_text(encoding="utf-8"))["scope"]
    seal = json.loads(_SEAL.read_text(encoding="utf-8"))
    qs = seal["questions"]
    masters, datasets = set(scope["masters"]), set(scope["datasets"])
    gdates = set(scope["dates"].get("dates", []))
    mode = scope["dates"]["mode"]
    ops = set(scope["operations"])
    print("seal read at HEAD: %s" % _SEAL.relative_to(_REPO))
    print("sealed questions (denominator): %d" % len(qs))
    gaps = []
    for q in qs:
        qm, qd, qdates = set(q["masters"]), q["dataset"], set(q["dates"])
        miss = []
        if not qm <= masters:
            miss.append("master(s) %s" % sorted(qm - masters))
        if qd not in datasets:
            miss.append("dataset %s" % qd)
        if mode == "fixed_dates" and not qdates <= gdates:
            miss.append("date(s) %s" % sorted(qdates - gdates))
        print("  %-7s masters=%-22s dataset=%-12s dates=%-24s %s"
              % (q["id"], ",".join(sorted(qm)), qd, ",".join(sorted(qdates)), "INSIDE" if not miss else "GAP: " + "; ".join(miss)))
        if miss:
            gaps.append("%s(%s)" % (q["id"], "; ".join(miss)))
    print("questions inside the grant: %d of %d" % (len(qs) - len(gaps), len(qs)))
    # A7 step 4: one no-date request per master. check_scope skips the date dimension when `dates` is
    # omitted ("an omitted optional dimension means 'the granted set'"), so the ask needs master+operation only.
    nodate_ops = {"list", "query"}
    nodate_gaps = [m for m in ("08242234", "08335338") if m not in masters]
    if not nodate_ops & ops:
        nodate_gaps.append("neither 'list' nor 'query' granted for a no-date ask")
    print("A7 step 4 no-date asks inside the grant: %d of 2 (%s)"
          % (2 - len([g for g in nodate_gaps if g in ("08242234", "08335338")]), "operations " + ",".join(sorted(nodate_ops & ops)) or "NONE"))
    # A7 step 3: one download_filtered for one master and date
    dl_gap = [] if "download_filtered" in ops else ["download_filtered not granted"]
    if mode == "fixed_dates" and not gdates:
        dl_gap.append("no granted date")
    if not masters:
        dl_gap.append("no granted master")
    print("A7 step 3 download_filtered inside the grant: %d of 1" % (0 if dl_gap else 1))
    allg = gaps + nodate_gaps + dl_gap
    if allg:
        return _out("AC5", False, "%d uncovered request(s): %s" % (len(allg), "; ".join(allg)))
    return _out("AC5", True)


# --- AC6: no secret and no customer value in any artifact this order commits
def ac6():
    files = [p for p in [_EVIDENCE, _CANDIDATE, _RESULT, Path(__file__)] if p.exists()]
    masters_ok = {"08242234", "08335338"}
    pats = [
        ("bearer/authorization token", re.compile(r"\b(Bearer|Authorization:)\s+\S{8,}", re.I)),
        ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.")),
        ("cookie", re.compile(r"\b(Set-)?Cookie\s*[:=]\s*\S+", re.I)),
        ("client secret / key assignment", re.compile(r"\b(CLIENT_SECRET|FERNET_KEY|OTP_BEARER|MS_INGEST_BEARER|GRAPH_READ_BEARER|SECRET_ACCESS_KEY|PRIVATE_KEY)\s*=\s*\S+")),
        ("complete URL with a query string", re.compile(r"https?://\S+\?\S*=\S+")),
        ("currency amount", re.compile(r"[$]\s?\d[\d,]*\.\d{2}\b")),
    ]
    print("files scanned (denominator): %d" % len(files))
    findings = []
    for p in files:
        text = p.read_text(encoding="utf-8", errors="replace")
        hits = []
        for label, rx in pats:
            for m in rx.finditer(text):
                if label == "client secret / key assignment" and re.search(r"<<|REDACT|ABSENT", m.group(0), re.I):
                    continue
                hits.append(label)
                break
        # a raw account identifier: an 8+ digit run that is not one of the two contract MASTER ids and
        # not part of a date. Master ids are named openly by the contract, the order and the protocol.
        # GUIDs are blanked first: a tid/oid is recordable by this order, and its all-digit hex groups
        # would otherwise read as account numbers (the zero GUID sentinel is the exemplar).
        scan = re.sub(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", "<guid>", text)
        # The boundary is WORD-class, not digit-class. A digit run glued to a hex letter is part of a
        # commit-ish (a hash beginning with a hex letter carries a 9-digit tail), not an account number; a real
        # account identifier stands alone as its own token. A digit-only lookaround misses that and
        # fires on every commit hash the record cites -- measured on this file.
        for m in re.finditer(r"(?<![0-9A-Za-z])\d{8,}(?![0-9A-Za-z])", scan):
            tok = m.group(0)
            if tok in masters_ok:
                continue
            if re.match(r"^20\d{6}$", tok):
                continue
            hits.append("raw account identifier candidate %s" % tok)
        print("  %-58s %s" % (p.relative_to(_REPO), "clean" if not hits else "; ".join(sorted(set(hits)))))
        if hits:
            findings.append("%s: %s" % (p.name, "; ".join(sorted(set(hits)))))
    print("files with a finding: %d of %d" % (len(findings), len(files)))
    if findings:
        return _out("AC6", False, "%d file(s) carry a forbidden value: %s" % (len(findings), " | ".join(findings)))
    return _out("AC6", True)


_DISPATCH = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in _DISPATCH:
        print("usage: og_g1.py %s" % "|".join(sorted(_DISPATCH)))
        raise SystemExit(2)
    raise SystemExit(_DISPATCH[sys.argv[1]]())
