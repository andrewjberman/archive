#!/usr/bin/env python3
"""battery_ib_rt_3.py -- ONE opaque-id normalizer: one definition, equal ids across the three
producers for three firms, typed refusals, the grain agreed, the projection resolving, the layer
landed. Cell IB-rt-3 (CTO ruling 4, round 2; closes rows W1-S7, W1-S9, W2-S11, W2-S2).

EVERY ARM'S SUBJECT IS THE REAL ARTIFACT. Arm (a) censuses the two real source trees and reads
the real layer zip against the COMMITTED blobs; arm (b) reads the LANDED QA directory and
holdings objects out of the three firm buckets and hands their ids to the REAL `_scope.resolve`
and the REAL performance adapter's own `check_scope`; arm (c) calls the real requirers; arm (d)
runs the real `_scope.resolve` and the real `directory/handler.resolve`; arm (e) reads RAW
upstream keys out of the tables `raw_keys.json` CITES and projects them through the real
normalizer; arm (f) reads the live layer version, the live function configurations and the
ledger entry. Nothing here wraps or re-implements the thing it grades, and every denominator is
RE-DERIVED on each run.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import ast
import base64
import hashlib
import importlib.util as _ilu
import json
import os
import re
import subprocess
import sys
import zipfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "..", "..", "..", ".."))
_LAMBDA_ROOT = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting")
_GOLD = os.path.join(_REPO, "data", "assets", "scripts", "gold", "investor_reporting")

for _p in (os.path.join(_LAMBDA_ROOT, "_ids"), os.path.join(_LAMBDA_ROOT, "_scope"),
           os.path.join(_LAMBDA_ROOT, "_keys"), _GOLD):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ids as _ids          # noqa: E402  THE one normalizer
import resolve as _scope    # noqa: E402  IB-s-2's resolver

RESULT_TOKEN = "IBRT3-ONE-ID-SPACE"

FIRM_BUCKETS = {"49financial": "opal-data-bd", "inflection": "opal-data-inf",
                "cottonwood": "opal-data-cot"}
LAYER_NAME = "irpt-common"
LAYER_CONSUMERS = ("irpt-performance-adapter", "irpt-narrative")
LEDGER_SLUG = "irpt-bckend-rt3"
LAYER_ZIP = os.path.join(_REPO, "infra", "aws", "lambda", "layers", "irpt-common",
                         "irpt-common.zip")

CENSUS_TREES = ("infra/aws/lambda/investor-reporting",
                "data/assets/scripts/gold/investor_reporting")
IDS_PACKAGE = "infra/aws/lambda/investor-reporting/_ids"


def _aws(*args):
    """The estate's aws shim via aws.cmd -- this battery runs under native Windows Python, where
    handing CreateProcess the bash script `.tools/aws` is 'not a valid Win32 application'."""
    exe = os.path.join(_REPO, ".tools", "aws.cmd")
    proc = subprocess.run([exe] + list(args), capture_output=True, text=True, timeout=180)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _load(name, path, extra_syspath=None):
    if extra_syspath and extra_syspath not in sys.path:
        sys.path.insert(0, extra_syspath)
    spec = _ilu.spec_from_file_location(name, path)
    mod = _ilu.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _s3():
    import boto3
    return boto3.client("s3", region_name="us-east-1")


def _landed(s3, firm_id, family):
    """The REAL landed QA artifact for one firm and family, reached through its own pointer."""
    bucket = FIRM_BUCKETS[firm_id]
    ptr = json.loads(s3.get_object(
        Bucket=bucket, Key="investor-reporting/qa/%s/latest.json" % family)["Body"].read())
    doc = json.loads(s3.get_object(Bucket=bucket, Key=ptr["key"])["Body"].read())
    return ptr, doc


# =================================================================== (a) ONE DEFINITION
# The grammar as a pattern over SOURCE rather than a list of files a reviewer must trust: a
# 24-hex truncation of a sha256 digest.
_GRAMMAR_RE = re.compile(r"hexdigest\(\)\s*\[\s*:\s*24\s*\]")
_ACCT_PREFIX_RE = re.compile(r":acct:")
_NS_PREFIX_RE = re.compile(r'"([A-Za-z]{2,10}[-_])"')


def _mention_lines(text, needle):
    """The lines where `needle` appears INSIDE A STRING CONSTANT'S OWN VALUE -- a docstring that
    describes the grammar, or a guard whose assertion text quotes it. Scoping this to constants
    that actually CONTAIN the needle matters: a line that merely has some other string literal on
    it (`return "REQ-" + hashlib...`) is live code and must stay gradeable."""
    covered = set()
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return covered
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and needle in node.value:
            for ln in range(node.lineno, (node.end_lineno or node.lineno) + 1):
                covered.add(ln)
    return covered


def _classify_grammar_hit(lines, line_no, in_string):
    """What KIND of id this occurrence mints. The census sweeps the grammar; the CLAIM is about
    the OPAQUE-ID normalizer, so each hit is classified and only an opaque-id mint outside
    `_ids/` is a second definition. The classification prints the namespace prefix it read, so
    a wrong call is visible rather than buried in a verdict."""
    if in_string:
        return "STRING-LITERAL", "the text appears inside a docstring or a guard's own assertion"
    window = "\n".join(lines[max(0, line_no - 3):line_no])
    m = _NS_PREFIX_RE.search(window)
    prefix = m.group(1) if m else None
    if prefix and prefix in set(_ids.KINDS.values()):
        return "OPAQUE-ID-MINT", "mints a %r id -- the normalizer's own grammar" % prefix
    if prefix:
        return "FOREIGN-NAMESPACE", ("mints a %r id, a different id space entirely (not one of "
                                     "the four opaque kinds %s)"
                                     % (prefix, sorted(_ids.KINDS.values())))
    return "OPAQUE-ID-MINT", "no namespace prefix read in the statement -- classified fail-closed"


def arm_one_definition():
    scanned = 0
    hits = []
    prefix_hits = []
    for tree in CENSUS_TREES:
        root = os.path.join(_REPO, *tree.split("/"))
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames
                           if d not in ("__pycache__", ".build", ".terraform")]
            for name in filenames:
                if not name.endswith(".py"):
                    continue
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, _REPO).replace("\\", "/")
                scanned += 1
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
                lines = text.splitlines()
                grammar_prose = _mention_lines(text, "hexdigest()[:24]")
                prefix_prose = _mention_lines(text, ":acct:")
                for m in _GRAMMAR_RE.finditer(text):
                    line_no = text[:m.start()].count("\n") + 1
                    kind, why = _classify_grammar_hit(lines, line_no,
                                                      line_no in grammar_prose)
                    hits.append({"file": rel, "line": line_no,
                                 "inside_ids": rel.startswith(IDS_PACKAGE),
                                 "classification": kind, "why": why})
                for m in _ACCT_PREFIX_RE.finditer(text):
                    line_no = text[:m.start()].count("\n") + 1
                    line = lines[line_no - 1].strip()
                    live = not line.startswith("#") and line_no not in prefix_prose
                    prefix_hits.append({"file": rel, "line": line_no, "text": line[:110],
                                        "live_code": live})

    outside = [h for h in hits
               if not h["inside_ids"] and h["classification"] == "OPAQUE-ID-MINT"]
    inside = [h for h in hits if h["inside_ids"]]
    not_the_normalizer = [h for h in hits
                          if not h["inside_ids"] and h["classification"] != "OPAQUE-ID-MINT"]
    live_prefix = [p for p in prefix_hits if p["live_code"]]

    # THE LAYER CARRIES THE SAME BYTES -- compared against the COMMITTED blob, never the
    # worktree file: on an autocrlf box the checkout is not the record.
    layer_rows = []
    if os.path.exists(LAYER_ZIP):
        z = zipfile.ZipFile(LAYER_ZIP)
        for rel, arc in (("infra/aws/lambda/investor-reporting/_ids/ids.py", "python/ids.py"),
                         ("infra/aws/lambda/investor-reporting/_ids/raw_keys.json",
                          "python/raw_keys.json")):
            blob = subprocess.run(["git", "-C", _REPO, "show", "HEAD:" + rel],
                                  capture_output=True).stdout
            member = z.read(arc) if arc in z.namelist() else b""
            layer_rows.append({"packaged_as": arc, "committed_blob_bytes": len(blob),
                               "member_bytes": len(member),
                               "byte_equal_to_committed_blob":
                                   bool(member) and member == blob})
        z.close()

    ok = (not outside) and bool(inside) and (not live_prefix) and len(layer_rows) == 2 \
        and all(r["byte_equal_to_committed_blob"] for r in layer_rows)
    return ok, {
        "python_files_scanned": scanned,
        "grammar_occurrences_total": len(hits),
        "second_opaque_id_definitions_outside_ids": "%d of %d" % (len(outside), len(hits)),
        "outside_ids_second_definitions": outside,
        "outside_ids_but_a_different_id_space": not_the_normalizer,
        "inside_ids": inside,
        "firm_prefixed_account_id_sites": "%d live code of %d textual hits"
                                          % (len(live_prefix), len(prefix_hits)),
        "live_prefix_sites": live_prefix,
        "prose_prefix_mentions": [p for p in prefix_hits if not p["live_code"]],
        "layer_members": layer_rows,
    }


# =================================================================== (b) THREE PRODUCERS
def arm_three_producers(s3):
    """Directory, holdings and the performance adapter, per firm, from the REAL landed
    artifacts. The claim is NOT that the two populations are the same SIZE -- they are built
    from different upstream tables and never were -- it is that for the SAME account the
    producers mint the SAME id, so every account both producers hold JOINS, and the third
    producer accepts those ids as its scope."""
    perf = _load("irpt_perf_handler", os.path.join(_LAMBDA_ROOT, "performance", "handler.py"),
                 os.path.join(_LAMBDA_ROOT, "performance"))
    rows = {}
    all_ok = True
    for firm_id in sorted(FIRM_BUCKETS):
        dptr, ddoc = _landed(s3, firm_id, "directory")
        hptr, hdoc = _landed(s3, firm_id, "holdings")

        dir_ids = set()
        for e in ddoc.get("entries", []):
            dir_ids.update(e["ids"]["account_ids"])
        hold_ids = set(hdoc["scope"]["account_ids"])
        joined = dir_ids & hold_ids
        prefixed = sorted(a for a in (dir_ids | hold_ids) if ":acct:" in a)
        unissued = sorted(a for a in (dir_ids | hold_ids)
                          if not _ids.is_issued("account", a))[:5]

        # THE THIRD PRODUCER. A firm-operations principal resolves to the firm population out of
        # the REAL directory, narrowed to a requested ACCOUNT scope taken from the JOINED set;
        # the resolved ids are then handed to the performance adapter's OWN check_scope. If the
        # three producers did not share one id space this resolves empty or is refused.
        firm_opaque = ddoc.get("firm_id_opaque") or _ids.opaque_firm(firm_id)
        sample = sorted(joined)[:25]
        headers = {"X-User-Email": "ops@opalinvest.dev", "X-User-Name": "N",
                   "X-User-Tier": "partner", "X-User-Role": "admin", "X-Firm-Id": firm_opaque,
                   "X-User-Type": "Advisor", "X-Advisor-Id": "", "X-Advisor-Role": "",
                   "X-Origin-Verify": "cloudfront"}
        scope = _scope.resolve(headers, ddoc,
                               requested_scope={"scope_kind": "ACCOUNT", "scope_ids": sample},
                               entitlement_revision="rt3", policy=_scope.DEFAULT_POLICY)
        scope_ids = set(scope["resolved_scope"]["scope_ids"])
        try:
            perf_firm, perf_ids = perf.check_scope({
                "verified_request_firm_id": firm_id,
                "permitted_account_set": scope["permitted_account_set"],
                "resolved_scope": scope["resolved_scope"]})
            perf_accepted = True
            perf_reason = ("the adapter's own check_scope accepted %d resolved id(s) for %s"
                           % (len(perf_ids), perf_firm))
        except Exception as exc:  # noqa: BLE001 -- the refusal text IS the evidence
            perf_accepted = False
            perf_reason = "%s: %s" % (type(exc).__name__, str(exc)[:200])

        scope_equal = bool(scope_ids) and scope_ids == set(sample) \
            and scope_ids <= dir_ids and scope_ids <= hold_ids
        firm_ok = (not prefixed) and (not unissued) and bool(joined) \
            and scope_equal and perf_accepted
        all_ok = all_ok and firm_ok
        rows[firm_id] = {
            "directory_object": dptr["key"],
            "holdings_object": hptr["key"],
            "directory_accounts": len(dir_ids),
            "holdings_accounts": len(hold_ids),
            "holdings_ids_found_in_the_directory": "%d of %d" % (len(joined), len(hold_ids)),
            "directory_ids_found_in_holdings": "%d of %d" % (len(joined), len(dir_ids)),
            "firm_prefixed_ids": len(prefixed),
            "ids_not_of_issued_shape_sample": unissued,
            "third_producer_scope_ids": "%d of %d" % (len(scope_ids), len(sample)),
            "third_producer_ids_are_directory_and_holdings_ids": scope_equal,
            "performance_adapter_accepted": perf_accepted,
            "performance_adapter_reason": perf_reason,
            "declared_raw_key": _ids.raw_key_for(firm_id, "account")["raw_key"],
            "ok": firm_ok,
        }
    return all_ok, rows


# =================================================================== (c) TYPED REFUSALS
def _bad_inputs_for(kind):
    """Four inputs, each genuinely bad FOR THAT KIND. For the firm requirer an issued firm id is
    CORRECT, so its fourth case is the other shape the order names: the REQUEST-CONTROLLED raw
    firm token, which is exactly what an unfiltered X-Firm-Id carries."""
    swapped = "inflection" if kind == "firm" else _ids.opaque_firm("inflection")
    return [("raw upstream key", "0010020692"),
            ("display name", "Whitfield Family"),
            ("e-mail address", "advisor.a@49financial.com"),
            ("cross-kind / request-controlled firm token", swapped)]


def arm_typed_refusals():
    rows = {}
    all_ok = True
    for kind in ("account", "relationship", "client", "firm"):
        requirer = _ids.REQUIRERS[kind]
        cases = _bad_inputs_for(kind)
        refused = 0
        echoed = []
        accepted = []
        for label, value in cases:
            try:
                requirer(value)
                accepted.append(label)
            except _ids.IdRefused as exc:
                refused += 1
                if value in str(exc):
                    echoed.append(label)
        # The MINT side too: an unregistered firm token and a name-shaped raw key.
        mint_refused = 0
        for firm_token, raw in (("notafirm", "A-1"), ("49financial", "Whitfield Family")):
            try:
                _ids.opaque(kind, firm_token, raw)
            except _ids.IdRefused:
                mint_refused += 1
        # ... and the POSITIVE CONTROL: a genuinely issued id of this kind is ACCEPTED, so the
        # four refusals are a discriminating instrument and not a requirer that says no to
        # everything.
        good = _ids.opaque(kind, "49financial", "POSITIVE-CONTROL-RT3")
        try:
            requirer(good)
            positive = True
        except _ids.IdRefused:
            positive = False
        ok = refused == len(cases) and not echoed and mint_refused == 2 and positive
        all_ok = all_ok and ok
        rows[kind] = {"boundary_refusals": "%d of %d" % (refused, len(cases)),
                      "accepted_that_should_not_be": accepted,
                      "echoed_the_refused_value": echoed,
                      "mint_refusals": "%d of 2" % mint_refused,
                      "positive_control_issued_id_accepted": positive, "ok": ok}
    return all_ok, rows


# =================================================================== (d) THE GRAIN
def _grain_directory():
    """Three grain cases in one small directory. Every id is MINTED by the normalizer -- not a
    hand-typed string that merely looks like one."""
    firm = "49financial"
    fo = _ids.opaque_firm(firm)

    def entry(client_raw, rel_raw, account_raws):
        ids = {"firm_id": fo, "client_id": _ids.opaque_client(firm, client_raw),
               "account_ids": [_ids.opaque_account(firm, a) for a in account_raws]}
        if rel_raw is not None:
            ids["relationship_id"] = _ids.opaque_relationship(firm, rel_raw)
        return {"ids": ids, "display_name": "Fixture " + client_raw,
                "masked_discriminator": "****0001",
                "permitted_scope": {"scope_kind": "CLIENT", "scope_ids": [ids["client_id"]]},
                "permitted_capabilities": ["DIRECTORY_READ"],
                "termination": {"indicator": "ACTIVE", "effective_date": None},
                "access": {"entitled": "UNKNOWN", "reason": "resolved at request time"},
                "revision": {"directory_revision": "irpt-dir/rt3-fixture/2026-09-11/1.0"},
                "cohort": {"authoritative": False}}

    directory = {"firm_id_opaque": fo, "as_of_business_date": "2026-09-10", "entries": [
        entry("C-ONLY", None, ["A-ONLY"]),                   # 1. account-only, NO relationship
        entry("C-MULTI", "R-1", ["A-MULTI"]),                # 2. one account under
        entry("C-MULTI", "R-2", ["A-MULTI"]),                #    TWO relationships
        entry("C-OUT", "R-OUT", ["A-MULTI", "A-OUTSIDE"]),   # 3. a relationship reaching out
    ]}
    k = {"A_ONLY": _ids.opaque_account(firm, "A-ONLY"),
         "A_MULTI": _ids.opaque_account(firm, "A-MULTI"),
         "A_OUTSIDE": _ids.opaque_account(firm, "A-OUTSIDE"),
         "R_1": _ids.opaque_relationship(firm, "R-1"),
         "R_2": _ids.opaque_relationship(firm, "R-2"),
         "R_OUT": _ids.opaque_relationship(firm, "R-OUT")}
    return firm, fo, directory, k


def arm_the_grain():
    dh = _load("irpt_dir_handler", os.path.join(_LAMBDA_ROOT, "directory", "handler.py"),
               os.path.join(_LAMBDA_ROOT, "directory"))
    firm, fo, directory, K = _grain_directory()
    headers = {"X-User-Email": "adv@49financial.com", "X-User-Name": "N",
               "X-User-Tier": "partner", "X-User-Role": "user", "X-Firm-Id": fo,
               "X-User-Type": "Advisor", "X-Advisor-Id": "ADV-A", "X-Advisor-Role": "",
               "X-Origin-Verify": "cloudfront"}
    proj = _ids.projection_for(firm)
    cases = {}

    def own(accounts, relationships):
        return {"schema_version": 1,
                "advisors": {"ADV-A": {"accounts": accounts, "relationships": relationships}}}

    # 1. ACCOUNT-ONLY. The entry carries NO relationship_id at all; the permitted set is exactly
    #    the one granted account, and the entry is reachable without a relationship.
    s1 = _scope.resolve(headers, directory, own(["A-ONLY"], []), id_projection=proj,
                        entitlement_revision="rt3", policy=_scope.DEFAULT_POLICY)
    entry1 = [e for e in directory["entries"] if K["A_ONLY"] in e["ids"]["account_ids"]][0]
    r1 = dh.resolve(directory, s1, {"account_ids": [K["A_ONLY"]]})
    cases["account_only"] = {
        "entry_carries_a_relationship_id": "relationship_id" in entry1["ids"],
        "permitted": sorted(s1["permitted_account_set"]),
        "expected": [K["A_ONLY"]],
        "handler_ok": r1["ok"], "handler_account_ids": r1["account_ids"],
        "ok": (sorted(s1["permitted_account_set"]) == [K["A_ONLY"]]
               and "relationship_id" not in entry1["ids"]
               and r1["ok"] and r1["account_ids"] == [K["A_ONLY"]]),
    }

    # 2. MULTI-RELATIONSHIP. One account listed under TWO relationships is ONE account in the
    #    permitted set, and resolving through EITHER relationship names the SAME id.
    s2 = _scope.resolve(headers, directory, own([], ["R-1", "R-2"]), id_projection=proj,
                        entitlement_revision="rt3", policy=_scope.DEFAULT_POLICY)
    rels = [e["ids"]["relationship_id"] for e in directory["entries"]
            if K["A_MULTI"] in e["ids"]["account_ids"] and "relationship_id" in e["ids"]]
    via1 = dh.resolve(directory, s2, {"relationship_id": K["R_1"]})
    via2 = dh.resolve(directory, s2, {"relationship_id": K["R_2"]})
    cases["multi_relationship"] = {
        "relationships_listing_the_account": len(rels),
        "relationships_granted": 2,
        "permitted": sorted(s2["permitted_account_set"]),
        "expected": [K["A_MULTI"]],
        "via_R_1": via1["account_ids"], "via_R_2": via2["account_ids"],
        "ok": (sorted(s2["permitted_account_set"]) == [K["A_MULTI"]] and len(rels) >= 2
               and K["R_1"] in rels and K["R_2"] in rels
               and via1["ok"] and via2["ok"]
               and via1["account_ids"] == via2["account_ids"] == [K["A_MULTI"]]),
    }

    # 3. A RELATIONSHIP CARRYING AN ACCOUNT OUTSIDE THE VIEWER'S POPULATION. Requesting it must
    #    never widen the permitted set, and the handler must answer UNSUPPORTED with the
    #    shortfall COUNTED rather than a silently narrowed set dressed as a whole one.
    s3 = _scope.resolve(headers, directory, own(["A-MULTI"], []), id_projection=proj,
                        requested_scope={"scope_kind": "RELATIONSHIP",
                                         "scope_ids": [K["R_OUT"]]},
                        entitlement_revision="rt3", policy=_scope.DEFAULT_POLICY)
    r3 = dh.resolve(directory, s3, {"relationship_id": K["R_OUT"]})
    cases["relationship_reaching_outside"] = {
        "permitted": sorted(s3["permitted_account_set"]),
        "outside_account_in_the_permitted_set": K["A_OUTSIDE"] in s3["permitted_account_set"],
        "resolver_partial_reason": (s3.get("partial_reason") or "")[:140],
        "handler_ok": r3["ok"], "handler_scope_kind": r3["resolved_scope"]["scope_kind"],
        "handler_permitted_of_requested": "%s of %s" % (r3.get("permitted_account_count"),
                                                        r3.get("requested_account_count")),
        "ok": (K["A_OUTSIDE"] not in s3["permitted_account_set"]
               and sorted(s3["permitted_account_set"]) == [K["A_MULTI"]]
               and bool(s3.get("partial_reason"))
               and r3["ok"] is False
               and r3["resolved_scope"]["scope_kind"] == "UNSUPPORTED"
               and K["A_OUTSIDE"] not in (r3["account_ids"] or [])),
    }

    passed = sum(1 for c in cases.values() if c["ok"])
    return passed == 3, {"denominator": "%d of 3" % passed, "cases": cases}


# =================================================================== (e) THE PROJECTION
def _raw_key_sample(s3, firm_id, limit=25):
    """RAW upstream keys for one firm, read from the table `raw_keys.json` CITES -- so this arm
    is exercised on the real custodian key space, not on a convenient invention."""
    hs = sys.modules.get("holdings_snapshot") or _load(
        "holdings_snapshot", os.path.join(_GOLD, "holdings_snapshot.py"), _GOLD)
    if firm_id == "inflection":
        b, pre, dp, col = ("opal-data-inf", "silver/api_dims/accounts_v2/",
                           "snapshot_date=", "account_id")
    elif firm_id == "cottonwood":
        b, pre, dp, col = ("opal-data-assets",
                           "blackdiamond/cottonwood/silver/fact_allocations/", "date=",
                           "AccountID")
    else:
        b, pre, dp, col = ("opal-data-assets",
                           "smartx/platform/silver/fact_allocation_account_map/", "date=",
                           "account_number")
    date = hs._latest_date_partition(s3, b, pre, date_prefix=dp)
    df = hs._read_parquet(s3, b, "%s%s%s/data.parquet" % (pre, dp, date))
    vals = [str(v) for v in df[col].dropna().astype(str).drop_duplicates().head(limit)]
    if firm_id == "49financial":
        vals = [hs._pad10(v) for v in vals]
    return vals, "s3://%s/%s%s%s/data.parquet [%s]" % (b, pre, dp, date, col)


def arm_the_projection(s3):
    """The ownership map is keyed by the UPSTREAM key, the directory by the ISSUED id. With
    `_ids.projection_for(firm)` as `id_projection`, every granted key must resolve into the
    directory's id space with 0 UNPROJECTED-ID (row W2-S7) -- and the NEGATIVE CONTROL (the same
    keys with NO projection) must fail, or the arm proves nothing."""
    rows = {}
    all_ok = True
    for firm_id in sorted(FIRM_BUCKETS):
        _p, ddoc = _landed(s3, firm_id, "directory")
        firm_opaque = ddoc.get("firm_id_opaque")
        dir_ids = set()
        for e in ddoc.get("entries", []):
            dir_ids.update(e["ids"]["account_ids"])

        raw, source = _raw_key_sample(s3, firm_id)
        ownership = {"schema_version": 1,
                     "advisors": {"ADV-RT3": {"accounts": raw, "relationships": []}}}

        granted, _r, census = _scope.advisor_grant(ownership, "ADV-RT3",
                                                   _ids.projection_for(firm_id))
        gaps = _scope.unmatched_reasons(granted, ddoc, firm_opaque)
        unprojected = [g for g in gaps if g["reason"].startswith("UNPROJECTED-ID")]
        resolved = [g for g in granted if g in dir_ids]

        # NEGATIVE CONTROL: the SAME raw keys with NO projection cannot resolve, and every gap
        # is NAMED UNPROJECTED-ID rather than left as a silently smaller set.
        n_granted, _nr, _nc = _scope.advisor_grant(ownership, "ADV-RT3", None)
        n_gaps = _scope.unmatched_reasons(n_granted, ddoc, firm_opaque)
        n_unprojected = [g for g in n_gaps if g["reason"].startswith("UNPROJECTED-ID")]
        n_resolved = [g for g in n_granted if g in dir_ids]

        # THE GAPS ARE CLASSIFIED, NOT SWALLOWED. A key the directory does not hold is a
        # POPULATION fact (this firm's holdings feed carries accounts the directory build does
        # not, measured 5856 of 5873 for 49F) and NOT a projection failure. What this arm
        # refuses is an UNPROJECTED-ID -- the seam it exists to close -- and a CROSS-FIRM gap.
        by_reason = {}
        for g in gaps:
            by_reason[g["reason"].split(":")[0]] = by_reason.get(
                g["reason"].split(":")[0], 0) + 1
        cross_firm = by_reason.get("CROSS-FIRM", 0)

        ok = (bool(raw) and not unprojected and not cross_firm
              and len(resolved) + len(gaps) == len(granted)
              and not n_resolved and len(n_unprojected) == len(n_granted))
        all_ok = all_ok and ok
        rows[firm_id] = {
            "raw_key_source_read": source,
            "granted_raw_keys": len(raw),
            "projected_by_the_normalizer": "%d of %d" % (census["projected"], len(raw)),
            "unprojected_id_gaps": "%d of %d" % (len(unprojected), len(granted)),
            "resolved_in_the_directory": "%d of %d" % (len(resolved), len(granted)),
            "gaps_by_reason": by_reason,
            "negative_control_resolved_without_projection":
                "%d of %d" % (len(n_resolved), len(n_granted)),
            "negative_control_unprojected_gaps":
                "%d of %d" % (len(n_unprojected), len(n_granted)),
            "ok": ok,
        }
    return all_ok, rows


# =================================================================== (f) THE LAYER LANDED
def arm_the_layer():
    # NO `&` IN THE JMESPATH. `.tools/aws.cmd` runs through cmd.exe, which eats an unquoted
    # ampersand as a command separator: `max_by(LayerVersions,&Version).Version` returned an
    # EMPTY string with rc=0 on the first run of this battery -- a false ABSENT, not an error.
    # list-layer-versions already returns newest-first, so element 0 is the max.
    _rc, version, _e = _aws("lambda", "list-layer-versions", "--layer-name", LAYER_NAME,
                            "--region", "us-east-1", "--query",
                            "LayerVersions[0].Version", "--output", "text")
    version = version.strip()
    _rc2, live_sha, _e2 = _aws("lambda", "get-layer-version", "--layer-name", LAYER_NAME,
                               "--version-number", version, "--region", "us-east-1",
                               "--query", "Content.CodeSha256", "--output", "text")
    live_sha = live_sha.strip()
    built_sha = None
    if os.path.exists(LAYER_ZIP):
        built_sha = base64.b64encode(
            hashlib.sha256(open(LAYER_ZIP, "rb").read()).digest()).decode()

    consumers = {}
    for fn in LAYER_CONSUMERS:
        _rc3, arn, _e3 = _aws("lambda", "get-function-configuration", "--function-name", fn,
                              "--region", "us-east-1", "--query", "Layers[].Arn",
                              "--output", "text")
        arn = arn.strip()
        consumers[fn] = {"arn": arn,
                         "on_the_new_version": bool(version) and arn.endswith(":" + version)}

    sentinel_rel = "org/critical_paths/.open_deploys/%s.json" % LEDGER_SLUG
    sentinel_abs = os.path.join(_REPO, *sentinel_rel.split("/"))
    sentinel_commits = subprocess.run(
        ["git", "-C", _REPO, "log", "--format=%h", "--full-history", "--", sentinel_rel],
        capture_output=True, text=True).stdout.split()

    cm_dir = os.path.join(_REPO, "org", "critical_paths", "change_management")
    entry = None
    for name in sorted(os.listdir(cm_dir)):
        if LEDGER_SLUG in name:
            entry = os.path.join(cm_dir, name)
    text = open(entry, encoding="utf-8", errors="replace").read() if entry else ""
    closed = "CLOSED" in text
    open_legs = text.count("| OPEN")

    plans = {}
    tf = os.path.join(_REPO, ".tools", "terraform.exe")
    for root in ("performance", "narrative"):
        p = subprocess.run([tf, "-chdir=infra/aws/terraform/investor-reporting/%s" % root,
                            "plan", "-no-color", "-input=false", "-lock=false"],
                           cwd=_REPO, capture_output=True, text=True, timeout=600)
        plans[root] = "No changes. Your infrastructure matches the configuration." in p.stdout

    ok = (bool(version) and bool(built_sha) and live_sha == built_sha
          and all(c["on_the_new_version"] for c in consumers.values())
          and closed and open_legs == 0 and bool(sentinel_commits)
          and not os.path.exists(sentinel_abs) and all(plans.values()))
    return ok, {
        "layer_version": version,
        "live_code_sha256": live_sha,
        "built_zip_sha256": built_sha,
        "sha_match_by_content_not_filename": live_sha == built_sha,
        "consumers_on_the_new_version": "%d of %d" % (
            sum(1 for c in consumers.values() if c["on_the_new_version"]), len(consumers)),
        "consumers": consumers,
        "ledger_entry": os.path.basename(entry) if entry else None,
        "ledger_closed": closed, "legs_still_open": open_legs,
        "sentinel_commits_before_the_act": sentinel_commits,
        "sentinel_removed_by_the_close": not os.path.exists(sentinel_abs),
        "zero_diff_plans": plans,
    }


# =================================================================== driver
def main():
    report = {"battery": "IB-rt-3", "token_printed_only_when_every_arm_holds": RESULT_TOKEN,
              "arms": {}}
    s3 = _s3()
    all_pass = True
    for key, fn in (("a_one_definition", lambda: arm_one_definition()),
                    ("b_three_producers_three_firms", lambda: arm_three_producers(s3)),
                    ("c_typed_refusals", lambda: arm_typed_refusals()),
                    ("d_the_grain_three_fixtures", lambda: arm_the_grain()),
                    ("e_the_projection_resolves", lambda: arm_the_projection(s3)),
                    ("f_the_layer_landed", lambda: arm_the_layer())):
        ok, detail = fn()
        report["arms"][key] = {"ok": ok, "detail": detail}
        all_pass = all_pass and ok

    report["overall_pass"] = all_pass
    print(json.dumps(report, default=str, indent=1))
    if all_pass:
        print(RESULT_TOKEN)
        return 0
    print("BLOCKED: one or more IB-rt-3 arms did not hold; see the per-arm detail above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
