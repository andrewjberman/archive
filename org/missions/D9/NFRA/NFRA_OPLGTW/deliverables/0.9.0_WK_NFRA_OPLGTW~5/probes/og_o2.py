"""OGO2-AC1..AC11 probes (NFRA_OPLGTW, TO-OG-o-2, worker 0.9.0_WK_NFRA_OPLGTW~5).

One function per mechanical criterion. Each prints its measurement with its denominator, then exactly
one line `VERDICT: PASS-OGO2-AC<n>` or `VERDICT: FAIL-OGO2-AC<n> <reason>`. Run:

    python og_o2.py AC<n>

AC2 and AC9 read the actual files/module at HEAD (or the worktree, for AC9's live run); AC1, AC3-AC8,
AC10-AC11 are text-shape checks against the runbook / protocol files this order wrote.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_REPO = _HERE.parents[8]                                       # .../ajb_workspace
_GW = _REPO / "infra" / "aws" / "ec2" / "opal-gateway"
_RUNBOOK = _GW / "runbooks" / "SCHWAB_PILOT_RUNBOOK.md"
_PROTOCOL = _GW / "tests" / "acceptance" / "WALKTHROUGH_PROTOCOL.md"


# --- shared helpers --------------------------------------------------------------------------------
def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, start_pat: str, end_pat: str) -> str:
    m = re.search(start_pat + r"\n(.*?)\n" + end_pat, text, re.DOTALL)
    if m is None:
        raise RuntimeError("could not isolate section %r .. %r" % (start_pat, end_pat))
    return m.group(1)


def _verdict(ac: str, ok: bool, reason: str = "") -> int:
    if ok:
        print("VERDICT: PASS-OGO2-%s" % ac)
        return 0
    print("VERDICT: FAIL-OGO2-%s %s" % (ac, reason))
    return 1


# --- AC1 -- the eight named sections ------------------------------------------------------------------
_AC1_KEYWORDS = ("onboarding", "connector add or reuse", "member connection", "troubleshooting",
                 "audit read", "grant change", "revocation", "rollback", "disclosure")


def _run_ac1() -> int:
    text = _read(_RUNBOOK)
    headings = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("#")]
    joined = " | ".join(headings).lower()
    missing = [k for k in _AC1_KEYWORDS if k not in joined]
    for h in headings:
        print(h)
    print("DENOMINATOR: %d of %d required section keyword(s) present" % (len(_AC1_KEYWORDS) - len(missing),
                                                                          len(_AC1_KEYWORDS)))
    return _verdict("AC1", not missing, "missing_keyword(s)=%r" % (missing,))


# --- AC2 -- every named command exists at HEAD ---------------------------------------------------------
_PATH_RE = re.compile(r"(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.(?:py|sh)")


def _normalize(path: str) -> str:
    if path.startswith(("infra/", "org/", ".tools/")):
        return path
    if path.startswith(("ops/", "app/")):
        return "infra/aws/ec2/opal-gateway/" + path
    return path


def _exists_at_head(path: str) -> bool:
    r = subprocess.run(["git", "-C", str(_REPO), "cat-file", "-e", "HEAD:" + path],
                       capture_output=True, timeout=30)
    return r.returncode == 0


def _run_ac2() -> int:
    text = _read(_RUNBOOK)
    commands = sorted({_normalize(p) for p in _PATH_RE.findall(text)})
    missing = []
    for c in commands:
        ok = _exists_at_head(c)
        print("%s -> %s" % (c, "OK" if ok else "MISSING-AT-HEAD"))
        if not ok:
            missing.append(c)
    print("DENOMINATOR: %d of %d named command(s) exist at HEAD" % (len(commands) - len(missing), len(commands)))
    return _verdict("AC2", not missing, "missing_at_head=%r" % (missing,))


# --- AC3 -- troubleshooting distinguishes the three classes ----------------------------------------------
def _run_ac3() -> int:
    text = _read(_RUNBOOK)
    section = _section(text, r"## 4\. Troubleshooting", r"## 5\.").lower()
    checks = {
        "authentication failure": "authentication failure" in section,
        "terminal entitlement denial": "terminal entitlement denial" in section,
        "data unavailability": "data unavailability" in section,
    }
    for k, v in checks.items():
        print("%r present: %s" % (k, v))
    missing = [k for k, v in checks.items() if not v]
    print("DENOMINATOR: %d of %d required class(es) present" % (len(checks) - len(missing), len(checks)))
    return _verdict("AC3", not missing, "missing=%r" % (missing,))


# --- AC4 -- rollback disables the integration, keeps denial + revocation shim --------------------------
def _run_ac4() -> int:
    text = _read(_RUNBOOK)
    section = _section(text, r"## 7\. Rollback", r"## 8\.").lower()
    checks = {
        "disables the integration": "disable the integration" in section or "disables the integration" in section,
        "restricted-profile denial": "restricted-profile denial" in section,
        "revocation shim": "revocation shim" in section,
    }
    for k, v in checks.items():
        print("%r present: %s" % (k, v))
    missing = [k for k, v in checks.items() if not v]
    print("DENOMINATOR: %d of %d required phrase(s) present" % (len(checks) - len(missing), len(checks)))
    return _verdict("AC4", not missing, "missing=%r" % (missing,))


# --- AC5 -- rollback forbids the email-only / legacy-refresh binary --------------------------------------
def _run_ac5() -> int:
    text = _read(_RUNBOOK)
    section = _section(text, r"## 7\. Rollback", r"## 8\.").lower()
    checks = {
        "email-only path": "email-only path" in section,
        "legacy refresh tokens": "legacy refresh tokens" in section,
        "forbidding language (do not roll back)": "do not roll back" in section,
    }
    for k, v in checks.items():
        print("%r present: %s" % (k, v))
    missing = [k for k, v in checks.items() if not v]
    print("DENOMINATOR: %d of %d required phrase(s) present" % (len(checks) - len(missing), len(checks)))
    return _verdict("AC5", not missing, "missing=%r" % (missing,))


# --- AC6 -- rollback preserves source + carries the source-bucket readbacks -----------------------------
def _run_ac6() -> int:
    text = _read(_RUNBOOK)
    section = _section(text, r"## 7\. Rollback", r"## 8\.").lower()
    checks = {
        "source ingesters": "source ingesters" in section,
        "source contents": "source contents" in section,
        "source-bucket readbacks heading": "source-bucket readbacks" in section,
        "versioning": "versioning" in section,
        "aes256": "aes256" in section,
        "blockpublicacls": "blockpublicacls" in section,
        "ignorepublicacls": "ignorepublicacls" in section,
        "blockpublicpolicy": "blockpublicpolicy" in section,
        "restrictpublicbuckets": "restrictpublicbuckets" in section,
        "non-public": "non-public" in section,
    }
    for k, v in checks.items():
        print("%r present: %s" % (k, v))
    missing = [k for k, v in checks.items() if not v]
    print("DENOMINATOR: %d of %d required element(s) present" % (len(checks) - len(missing), len(checks)))
    return _verdict("AC6", not missing, "missing=%r" % (missing,))


# --- AC7 -- the disclosure's three facts ----------------------------------------------------------------
def _run_ac7() -> int:
    text = _read(_RUNBOOK)
    section = _section(text, r"## 8\. Disclosure", r"\Z").lower()
    checks = {
        "claude chat environment": "claude chat environment" in section,
        "retention": "retention" in section,
        "commercial training defaults do not mean zero transfer":
            "commercial training defaults do not mean zero transfer" in section,
        "cannot be recalled": "cannot be recalled" in section,
    }
    for k, v in checks.items():
        print("%r present: %s" % (k, v))
    missing = [k for k, v in checks.items() if not v]
    print("DENOMINATOR: %d of %d required fact(s) present" % (len(checks) - len(missing), len(checks)))
    return _verdict("AC7", not missing, "missing=%r" % (missing,))


# --- AC8 -- named readers and their consuming moments -----------------------------------------------------
def _run_ac8() -> int:
    text = _read(_RUNBOOK)
    section = _section(text, r"## 0\. Named readers and moments", r"## 1\.").lower()
    readers = {
        "cloudops operator": "cloudops operator" in section,
        "deployment operator": "deployment operator" in section,
        "identity/data administrator": "identity/data administrator" in section,
        "3.0.0_sa_cvo": "3.0.0_sa_cvo" in section,
        "2.0.0_sa_coo": "2.0.0_sa_coo" in section,
    }
    moments = {
        "before each onboarding": "before each onboarding" in section,
        "before enablement": "before enablement" in section,
        "at every grant revision": "at every grant revision" in section,
        "at every project validation": "at every project validation" in section,
        "at l5": "at l5" in section,
    }
    checks = dict(readers)
    checks.update(moments)
    for k, v in checks.items():
        print("%r present: %s" % (k, v))
    missing = [k for k, v in checks.items() if not v]
    print("DENOMINATOR: %d of %d required reader/moment(s) present" % (len(checks) - len(missing), len(checks)))
    return _verdict("AC8", not missing, "missing=%r" % (missing,))


# --- AC9 -- the status summary against moto fixtures, no customer value ---------------------------------
def _build_moto_world():
    import boto3
    from moto import mock_aws

    sys.path.insert(0, str(_GW))
    sys.path.insert(0, str(_GW / "tests" / "acceptance"))
    sys.path.insert(0, str(_GW / "ops"))
    import make_fixtures as mf                                  # noqa: E402
    from app import access_state as acs                         # noqa: E402
    from app.integrations.schwab import aws_roles, catalog as cat  # noqa: E402
    import schwab_status as st                                  # noqa: E402

    region = "us-east-1"
    account = "313476888478"
    clock = _dt.datetime(2026, 7, 13, 14, 0, 0, tzinfo=_dt.timezone.utc).timestamp()
    contract_path = _REPO / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    contract_raw = json.loads(contract_path.read_text(encoding="utf-8"))
    role_env = {
        "SCHWAB_READER_ROLE_ARN": "arn:aws:iam::%s:role/%s" % (account, contract_raw["reader_role"]),
        "SCHWAB_READER_EXTERNAL_ID": "ogo2-probe-reader-ext",
        "SCHWAB_CATALOG_ROLE_ARN": "arn:aws:iam::%s:role/%s" % (account, contract_raw["catalog_role"]),
        "SCHWAB_CATALOG_EXTERNAL_ID": "ogo2-probe-catalog-ext",
    }

    def _fixture_objects():
        out = []
        for order, root in ((1, "s3"), (2, "s3_later_versions")):
            base = _GW / "tests" / "acceptance" / "fixtures" / root / mf.BUCKET
            if not base.exists():
                continue
            for path in sorted(base.rglob("*")):
                if not path.is_file():
                    continue
                key = path.relative_to(base).as_posix()
                if "/meta/complete/" in key:
                    continue
                out.append((key, path.read_bytes(), order))
        return out

    def _fixture_markers():
        out = []
        base = _GW / "tests" / "acceptance" / "fixtures" / "s3" / mf.BUCKET
        for path in sorted(base.rglob("date=*.json")):
            out.append(json.loads(path.read_text(encoding="utf-8")))
        return out

    def _create_table(client, name=acs.TABLE_NAME):
        client.create_table(
            TableName=name,
            KeySchema=[{"AttributeName": acs.PK, "KeyType": "HASH"},
                       {"AttributeName": acs.SK, "KeyType": "RANGE"}],
            AttributeDefinitions=[{"AttributeName": acs.PK, "AttributeType": "S"},
                                  {"AttributeName": acs.SK, "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

    cm = mock_aws()
    cm.start()
    s3 = boto3.client("s3", region_name=region)
    s3.create_bucket(Bucket=mf.BUCKET)
    s3.put_bucket_versioning(Bucket=mf.BUCKET, VersioningConfiguration={"Status": "Enabled"})
    versions = {}
    for key, body, order in _fixture_objects():
        resp = s3.put_object(Bucket=mf.BUCKET, Key=key, Body=body)
        if order == 1:
            versions[key] = resp["VersionId"]
    for marker in _fixture_markers():
        restamped = mf.restamp(marker, versions)
        s3.put_object(Bucket=mf.BUCKET, Key=mf.marker_key(restamped["master"], restamped["date"]),
                      Body=(json.dumps(restamped, indent=1, sort_keys=True) + "\n").encode("ascii"))
    audit_bucket = "opal-mcp-audit-ogo2-probe"
    s3.create_bucket(Bucket=audit_bucket)
    ddb = boto3.client("dynamodb", region_name=region)
    _create_table(ddb)
    store = acs.AccessState(client=ddb, clock=lambda: clock)
    contract = cat.load_contract(str(contract_path))
    configs = aws_roles.role_configs(contract_raw, role_env)
    roles = {kind: aws_roles.AssumedRole(configs[kind], clock=lambda: clock) for kind in aws_roles.ROLE_KINDS}
    catalog_obj = cat.Catalog(contract=contract, catalog_role=roles[aws_roles.CATALOG],
                              data_role=roles[aws_roles.READER], store=store, clock=lambda: clock)

    class FakeConfig:
        ENABLED_INTEGRATIONS = ["schwab"]
        AUDIT_S3_BUCKET = audit_bucket
        AWS_REGION = region

    report = st.build_report(contract=contract, catalog_obj=catalog_obj, roles=roles, store=store,
                             config=FakeConfig(), s3_client=s3, audit_bucket=audit_bucket, since_days=1,
                             clock=lambda: clock)
    text = st.format_report(report)
    cm.stop()
    return text, mf.SHARED_ACCOUNT


def _run_ac9() -> int:
    output, shared_account = _build_moto_world()
    print(output)
    sections = {
        "HEALTH": "=== SCHWAB STATUS: HEALTH ===" in output,
        "CLOSURE": "=== SCHWAB STATUS: CLOSURE ===" in output,
        "ERROR": "=== SCHWAB STATUS: ERROR ===" in output,
    }
    no_customer_value = {
        "no '@' (email)": "@" not in output,
        "no fixture account id (%s)" % shared_account: shared_account not in output,
    }
    checks = dict(sections)
    checks.update(no_customer_value)
    for k, v in checks.items():
        print("check %r: %s" % (k, v))
    missing = [k for k, v in checks.items() if not v]
    print("DENOMINATOR: %d of %d required section/no-value check(s) hold" % (len(checks) - len(missing), len(checks)))
    return _verdict("AC9", not missing, "failed=%r" % (missing,))


# --- AC10 -- section 4's dates are the fixed 2026-09-15, "latest" gone ------------------------------------
def _run_ac10() -> int:
    text = _read(_PROTOCOL)
    section = _section(text, r"## 4\. Real-data questions.*?", r"## 5\.")
    rows = [ln for ln in section.splitlines() if re.match(r"\|\s*RQ[1-6]\s*\|", ln)]
    print("DENOMINATOR: %d of 6 RQ row(s) found" % len(rows))
    bad = []
    for row in rows:
        rid = re.match(r"\|\s*(RQ[1-6])\s*\|", row).group(1)
        has_date = "2026-09-15" in row
        has_latest = "latest" in row.lower()
        print("%s: 2026-09-15=%s latest=%s" % (rid, has_date, has_latest))
        if not has_date or has_latest:
            bad.append(rid)
    section_has_latest = "latest" in section.lower()
    print("section-wide 'latest' occurrence: %s" % section_has_latest)
    ok = len(rows) == 6 and not bad and not section_has_latest
    return _verdict("AC10", ok, "bad_rows=%r section_has_latest=%s row_count=%d"
                    % (bad, section_has_latest, len(rows)))


# --- AC11 -- A7's per-master no-date step ---------------------------------------------------------------
def _run_ac11() -> int:
    text = _read(_PROTOCOL)
    section = _section(text, r"### A7 --.*?", r"### A10")
    masters = ("08242234", "08335338")
    present = {m: (m in section) for m in masters}
    for m, v in present.items():
        print("master %s named: %s" % (m, v))
    missing_masters = [m for m, v in present.items() if not v]
    print("DENOMINATOR: %d of 2 master(s) named" % (2 - len(missing_masters)))
    other_checks = {
        "no business date": "no business date" in section.lower(),
        "latest qualified date": "latest qualified date" in section.lower(),
        "available dates": "available dates" in section.lower(),
        "2026-09-15 in expected observation": "2026-09-15" in section,
        "utc ask time evidence": "utc ask time" in section.lower(),
    }
    for k, v in other_checks.items():
        print("%r present: %s" % (k, v))
    missing_other = [k for k, v in other_checks.items() if not v]
    ok = not missing_masters and not missing_other
    return _verdict("AC11", ok, "missing_masters=%r missing_other=%r" % (missing_masters, missing_other))


_DISPATCH = {
    "AC1": _run_ac1, "AC2": _run_ac2, "AC3": _run_ac3, "AC4": _run_ac4, "AC5": _run_ac5,
    "AC6": _run_ac6, "AC7": _run_ac7, "AC8": _run_ac8, "AC9": _run_ac9, "AC10": _run_ac10,
    "AC11": _run_ac11,
}


def main(argv) -> int:
    if len(argv) != 2 or argv[1] not in _DISPATCH:
        print("usage: og_o2.py <%s>" % "|".join(_DISPATCH))
        return 2
    return _DISPATCH[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
