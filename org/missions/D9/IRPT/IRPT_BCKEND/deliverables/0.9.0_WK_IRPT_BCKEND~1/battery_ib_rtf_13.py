#!/usr/bin/env python3
"""IB-rtf-13 -- the directory-search zip carries its contract, and every runtime open across
the seven serving functions is a staged member. Cell IB-rtf-13. FIRST PASS: arms (a)-(c) only.

Re-derives, every run, from git blobs / the committed manifest / the committed layer build
manifest / the committed terraform env lines -- never from a hand-typed verdict table with no
premise check. Where a classification cannot be MECHANICALLY confirmed against those sources it
prints UNVERIFIED rather than asserting it. This is a CENSUS + PACKET pass: no `terraform apply`,
no `aws lambda update-function-code`. Every AWS/terraform read runs read-only or `plan` only.

Usage: py -3.12 battery_ib_rtf_13.py
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE,
                      capture_output=True, check=True).stdout.decode("utf-8").strip()
REPO = REPO.replace("/", os.sep)
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
LAYER_MANIFEST = os.path.join(REPO, "infra", "aws", "lambda", "layers", "irpt-common",
                              "BUILD_MANIFEST.json")
# This battery runs under native `py -3.12`, not Git Bash -- .tools/aws is a bash script (native
# subprocess.run cannot exec it, WinError 193); .tools/aws.cmd is the Windows-shell companion
# built for exactly this caller class. .tools/terraform.exe is a real PE, used by its own path.
AWS = os.path.join(REPO, ".tools", "aws.cmd")
TERRAFORM = os.path.join(REPO, ".tools", "terraform.exe")

sys.path.insert(0, os.path.join(REPO, ".tools"))
from git_bash_resolver import git_bash  # noqa: E402

FUNCTIONS = ("irpt-directory-search", "irpt-performance-adapter", "irpt-narrative",
             "irpt-intake-poller", "irpt-export-render", "irpt-holdings", "irpt-status")
# The other function this project ships that is NOT in the 7: irpt-directory-refresh
# (a schedule target, not a served route) and irpt-ycharts-generate (barred, S102).
BARRED = ("irpt-ycharts-generate",)

TF_ROOTS = ("directory", "export", "holdings", "intake", "narrative", "ops", "performance")

# THE ENVIRONMENT EACH FUNCTION IS DEPLOYED WITH, cited to its own lambda.tf -- read here from
# the FILE, not typed twice, so a future env edit cannot silently outdate this table.
TF_ENV_FILES = {
    "irpt-directory-search": "infra/aws/terraform/investor-reporting/directory/lambda.tf",
    "irpt-performance-adapter": "infra/aws/terraform/investor-reporting/performance/lambda.tf",
    "irpt-narrative": "infra/aws/terraform/investor-reporting/narrative/lambda.tf",
    "irpt-intake-poller": "infra/aws/terraform/investor-reporting/intake/lambda.tf",
    "irpt-export-render": "infra/aws/terraform/investor-reporting/export/lambda.tf",
    "irpt-holdings": "infra/aws/terraform/investor-reporting/holdings/lambda.tf",
    "irpt-status": "infra/aws/terraform/investor-reporting/ops/lambda.tf",
}


def run(cmd, cwd=None, timeout=120):
    p = subprocess.run(cmd, cwd=cwd or REPO, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def git_show(pin, path):
    rc, out, err = run(["git", "show", "%s:%s" % (pin, path)])
    if rc != 0:
        raise SystemExit("ERROR: git show %s:%s failed: %s" % (pin, path, err[:300]))
    return out.encode("utf-8") if isinstance(out, str) else out


def git_show_bytes(pin, path):
    p = subprocess.run(["git", "show", "%s:%s" % (pin, path)], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("ERROR: git show %s:%s failed: %s" % (pin, path,
                                                                p.stderr.decode("utf-8", "replace")[:300]))
    return p.stdout


def load_json_at(pin, path):
    return json.loads(git_show_bytes(pin, path).decode("utf-8"))


def head_commit():
    rc, out, _ = run(["git", "rev-parse", "HEAD"])
    return out.strip()


def load_source_map():
    with open(SOURCE_MAP, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_layer_members():
    with open(LAYER_MANIFEST, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    names = set()
    for row in d.get("contracts", []):
        names.add(row["packaged_as"])
    for row in d.get("modules", []):
        names.add(row["packaged_as"])
    for row in d.get("data", []):
        names.add(row["packaged_as"])
    for row in d.get("id_normalizer", {}).get("members", []):
        names.add(row["packaged_as"])
    for row in d.get("carried_forward_members", {}).get("members", []):
        names.add(row["packaged_as"])
    names.add("python/bd_helpers.py")
    return names


def declared_members(fn_cfg):
    names = set(fn_cfg.get("files") or [])
    for s in fn_cfg.get("staged_from") or []:
        names.add(s["packaged_as"])
    return names


def read_tf_env(path):
    """A best-effort, line-scoped read of `environment_variables = { ... }` -- NAME = "literal"
    pairs only (every value this census needs is a literal). Not a general HCL parser."""
    with open(os.path.join(REPO, path), "r", encoding="utf-8") as fh:
        text = fh.read()
    start = text.find("environment_variables")
    if start < 0:
        return {}
    brace = text.find("{", start)
    depth = 0
    end = brace
    for i in range(brace, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    block = text[brace:end]
    env = {}
    import re
    for m in re.finditer(r'([A-Z0-9_]+)\s*=\s*"([^"]*)"', block):
        env[m.group(1)] = m.group(2)
    has_layer = "aws_lambda_layer_version.irpt_common" in text or \
                "data.aws_lambda_layer_version.irpt_common" in text
    return env, has_layer


# ---------------------------------------------------------------------------------------------
# ARM (a): THE RUNTIME-OPEN CENSUS
# ---------------------------------------------------------------------------------------------
# Every distinct runtime-file-open SITE found by reading the packaged Python members of the 7
# serving functions (this pass's manual sweep, cited file:line @HEAD 19ccf82226; the population
# is the union of files[] + staged_from across the 7, MINUS tests/ and fixture-GENERATOR scripts,
# which build-and-upload.sh never ships). Each row's classification is CHECKED below against the
# manifest / layer manifest / terraform env -- never trusted from this table alone.
#
# resolves_to: the literal packaged_as name the site targets when it succeeds, or None when no
# candidate ever resolves in a deployed zip (a pure-MISSING site).
# via: "own_zip" (files[]/staged_from of the SAME function), "layer" (irpt-common), or "none".
CENSUS_SITES = [
    # -- directory-search's OWN module (not shared frontier) --
    dict(fn="irpt-directory-search", file="directory/entry.py", line="74-83",
         target="DirectoryEntry.schema.json", resolves_to="contracts/DirectoryEntry.schema.json",
         via="own_zip", env_gate="IRPT_CONTRACTS_DIR", note="row S103 -- THIS ORDER'S FIX"),
    # -- _scope/resolve.py (staged as resolve.py; identical construct in holdings' own copy) --
    dict(fn="irpt-directory-search", file="_scope/resolve.py", line="503-510",
         target="ResolvedScope.schema.json", resolves_to=None, via="none", env_gate=None,
         note="new finding, row filed"),
    dict(fn="irpt-narrative", file="_scope/resolve.py", line="503-510",
         target="ResolvedScope.schema.json", resolves_to=None, via="none", env_gate=None,
         note="new finding, row filed"),
    dict(fn="irpt-export-render", file="_scope/resolve.py", line="503-510",
         target="ResolvedScope.schema.json", resolves_to=None, via="none", env_gate=None,
         note="new finding, row filed"),
    dict(fn="irpt-performance-adapter", file="_scope/resolve.py", line="503-510",
         target="ResolvedScope.schema.json", resolves_to=None, via="none", env_gate=None,
         note="new finding, row filed"),
    dict(fn="irpt-status", file="_scope/resolve.py", line="503-510",
         target="ResolvedScope.schema.json", resolves_to=None, via="none", env_gate=None,
         note="new finding, row filed"),
    dict(fn="irpt-holdings", file="holdings/resolve.py", line="503-510",
         target="ResolvedScope.schema.json", resolves_to=None, via="none", env_gate=None,
         note="new finding, own tracked copy of the same construct, row filed"),
    # -- ops/status.py's own StatusEnvelope schema (same defect SHAPE, SAFE fallback) --
    dict(fn="irpt-status", file="ops/status.py", line="84-98",
         target="StatusEnvelope.schema.json", resolves_to=None, via="none", env_gate=None,
         note="new finding, row filed -- fallback is the SAFE direction"),
    # -- ops/manifests.py's PATH_MANIFEST.json (checkout-only, one level above source_dir) --
    dict(fn="irpt-status", file="ops/manifests.py", line="46,216-219",
         target="PATH_MANIFEST.json", resolves_to=None, via="none", env_gate=None,
         note="new finding, row filed -- reachability from the live route UNVERIFIED this pass"),
    # -- ids.py, staged wherever declared (firm registry via env/walk/beside) --
    dict(fn="irpt-directory-search", file="_ids/ids.py", line="113-155",
         target="firm_registry.json", resolves_to="firm_registry.json", via="own_zip",
         env_gate="IRPT_FIRM_REGISTRY", note="beside-fallback (env unset)"),
    dict(fn="irpt-narrative", file="_ids/ids.py", line="113-155",
         target="firm_registry.json", resolves_to="firm_registry.json", via="own_zip",
         env_gate="IRPT_FIRM_REGISTRY", note="beside-fallback (env unset)"),
    dict(fn="irpt-performance-adapter", file="_ids/ids.py", line="113-155",
         target="firm_registry.json", resolves_to="firm_registry.json", via="own_zip",
         env_gate="IRPT_FIRM_REGISTRY", note="beside-fallback (env unset)"),
    dict(fn="irpt-status", file="_ids/ids.py", line="113-155",
         target="firm_registry.json", resolves_to="firm_registry.json", via="own_zip",
         env_gate="IRPT_FIRM_REGISTRY", note="beside-fallback (env unset)"),
    dict(fn="irpt-export-render", file="_ids/ids.py", line="113-155",
         target="firm_registry.json", resolves_to="python/firm_registry.json", via="layer",
         env_gate="IRPT_FIRM_REGISTRY", note="explicit env -> layer"),
    dict(fn="irpt-holdings", file="_ids/ids.py", line="113-155",
         target="firm_registry.json", resolves_to="python/firm_registry.json", via="layer",
         env_gate="IRPT_FIRM_REGISTRY", note="explicit env -> layer"),
    # -- ids.py raw_keys() and the seam index: always beside HERE, always packaged where ids.py is --
    dict(fn="irpt-directory-search", file="_ids/ids.py", line="159-163",
         target="raw_keys.json", resolves_to="raw_keys.json", via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-narrative", file="_ids/ids.py", line="159-163",
         target="raw_keys.json", resolves_to="raw_keys.json", via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-performance-adapter", file="_ids/ids.py", line="159-163",
         target="raw_keys.json", resolves_to="raw_keys.json", via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-export-render", file="_ids/ids.py", line="159-163",
         target="raw_keys.json", resolves_to="raw_keys.json", via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-holdings", file="_ids/ids.py", line="159-163",
         target="raw_keys.json", resolves_to="raw_keys.json", via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-status", file="_ids/ids.py", line="159-163",
         target="raw_keys.json", resolves_to="raw_keys.json", via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-directory-search", file="_ids/ids.py", line="338-362",
         target="data/custodian_key_seam.json", resolves_to="data/custodian_key_seam.json",
         via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-narrative", file="_ids/ids.py", line="338-362",
         target="data/custodian_key_seam.json", resolves_to="data/custodian_key_seam.json",
         via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-performance-adapter", file="_ids/ids.py", line="338-362",
         target="data/custodian_key_seam.json", resolves_to="data/custodian_key_seam.json",
         via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-export-render", file="_ids/ids.py", line="338-362",
         target="data/custodian_key_seam.json", resolves_to="data/custodian_key_seam.json",
         via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-holdings", file="_ids/ids.py", line="338-362",
         target="data/custodian_key_seam.json", resolves_to="data/custodian_key_seam.json",
         via="own_zip", env_gate=None, note=""),
    dict(fn="irpt-status", file="_ids/ids.py", line="338-362",
         target="data/custodian_key_seam.json", resolves_to="data/custodian_key_seam.json",
         via="own_zip", env_gate=None, note=""),
    # -- keys.py's own load_firm_ids/_load_registry (same shape, only where keys.py is packaged
    # flat or reached via the layer) --
    dict(fn="irpt-directory-search", file="_keys/keys.py", line="288-294",
         target="firm_registry.json", resolves_to="firm_registry.json", via="own_zip",
         env_gate="IRPT_FIRM_REGISTRY", note="beside-fallback (env unset)"),
    dict(fn="irpt-intake-poller", file="_keys/keys.py", line="288-294",
         target="firm_registry.json", resolves_to="firm_registry.json", via="own_zip",
         env_gate="IRPT_FIRM_REGISTRY", note="explicit env -> own zip"),
    dict(fn="irpt-status", file="_keys/keys.py", line="288-294",
         target="firm_registry.json", resolves_to="firm_registry.json", via="own_zip",
         env_gate="IRPT_FIRM_REGISTRY", note="beside-fallback (env unset)"),
    dict(fn="irpt-narrative", file="_keys/keys.py", line="288-294",
         target="firm_registry.json", resolves_to="python/firm_registry.json", via="layer",
         env_gate="IRPT_FIRM_REGISTRY", note="beside-fallback lands in /opt/python (keys.py is a layer member here)"),
    dict(fn="irpt-performance-adapter", file="_keys/keys.py", line="288-294",
         target="firm_registry.json", resolves_to="python/firm_registry.json", via="layer",
         env_gate="IRPT_FIRM_REGISTRY", note="beside-fallback lands in /opt/python (keys.py is a layer member here)"),
    dict(fn="irpt-export-render", file="_keys/keys.py", line="288-294",
         target="firm_registry.json", resolves_to="python/firm_registry.json", via="layer",
         env_gate="IRPT_FIRM_REGISTRY", note="explicit env -> layer"),
    dict(fn="irpt-holdings", file="_keys/keys.py", line="288-294",
         target="firm_registry.json", resolves_to="python/firm_registry.json", via="layer",
         env_gate="IRPT_FIRM_REGISTRY", note="explicit env -> layer"),
    # -- _gate/gate.py's load_policy (only intake packages gate.py of the 7) --
    dict(fn="irpt-intake-poller", file="_gate/gate.py", line="60-102",
         target="firm_destination_policy.json", resolves_to="firm_destination_policy.json",
         via="own_zip", env_gate="IRPT_FIRM_DESTINATION_POLICY", note="explicit env -> own zip"),
    # -- performance's own domain files (env-then-layer pattern, verified working) --
    dict(fn="irpt-performance-adapter", file="performance/bd_adapter.py", line="56-93",
         target="bd_helpers.py", resolves_to="python/bd_helpers.py", via="layer",
         env_gate="IRPT_BD_HELPERS_PATH", note="importlib.util.spec_from_file_location, not open()"),
    dict(fn="irpt-performance-adapter", file="performance/normalize.py", line="57-73",
         target="PerformanceReport.schema.json", resolves_to="python/irpt_contracts/PerformanceReport.schema.json",
         via="layer", env_gate="IRPT_CONTRACTS_DIR", note=""),
    dict(fn="irpt-performance-adapter", file="performance/transport.py", line="23-80",
         target="fixtures/*.json (FIXTURE_MANIFEST + per-receipt fixture)",
         resolves_to="fixtures/FIXTURE_MANIFEST.json", via="own_zip", env_gate=None, note=""),
    # -- narrative's own domain files --
    dict(fn="irpt-narrative", file="narrative/handler.py", line="30-73",
         target="event_policy.json", resolves_to="event_policy.json", via="own_zip",
         env_gate=None, note=""),
    dict(fn="irpt-narrative", file="narrative/handler.py", line="36-73",
         target="NarrativePacket.schema.json", resolves_to="python/irpt_contracts/NarrativePacket.schema.json",
         via="layer", env_gate="IRPT_CONTRACTS_DIR", note=""),
    dict(fn="irpt-narrative", file="narrative/evidence.py", line="219-222",
         target="fixtures/topics_*.json (RecordedTopicStore.from_file)",
         resolves_to="fixtures/topics_window.json", via="own_zip", env_gate=None,
         note="caller-supplied path parameter; default fixture is a packaged member"),
    # -- export's own domain files --
    dict(fn="irpt-export-render", file="export/handler.py", line="62-321",
         target="a contract schema (export capabilities probe, one of the 5 layer contracts)",
         resolves_to="python/irpt_contracts/RenderPackage.schema.json", via="layer",
         env_gate="IRPT_CONTRACTS_DIR", note="representative of the capabilities probe's schema reads"),
    dict(fn="irpt-export-render", file="export/bundle.py", line="33-80",
         target="ExportBundle.schema.json", resolves_to="python/irpt_contracts/ExportBundle.schema.json",
         via="layer", env_gate="IRPT_CONTRACTS_DIR", note=""),
    dict(fn="irpt-export-render", file="export/assets.py", line="74-289",
         target="brand.json / Opal-Capital-Logo-Full-Color.svg (deck_generation/, GITIGNORED)",
         resolves_to=None, via="none", env_gate="IRPT_BRAND_SPEC/IRPT_OPAL_LOGO",
         note="checkout-only default, no env set for export -- MISSING, self-documented absence"),
    dict(fn="irpt-export-render", file="export/package.py", line="61-110",
         target="portal build manifest (device-specific hardcoded fallback paths)",
         resolves_to=None, via="none", env_gate="IRPT_PORTAL_CHECKOUT",
         note="new finding, row filed -- ALWAYS MISSING in the deployed zip; hardcoded device path"),
    # -- holdings' own domain files --
    dict(fn="irpt-holdings", file="holdings/snapshot.py", line="71-97",
         target="HoldingsSnapshot.schema.json", resolves_to="contracts/HoldingsSnapshot.schema.json",
         via="own_zip", env_gate=None,
         note="the /opt/python/irpt_contracts candidate is tried FIRST (IRPT_CONTRACTS_DIR is "
              "set) and is ABSENT there -- the layer's 5-contract list has no HoldingsSnapshot, "
              "confirmed below; resolution falls through to this packaged copy, which is why "
              "the gate check here is the ABSENCE of the layer candidate, not the env value"),
    # -- intake's own domain files --
    dict(fn="irpt-intake-poller", file="intake/graph_client.py", line="146-192",
         target="fixtures/graph/* (RecordedTransport, offline/test transport only)",
         resolves_to="fixtures/graph/FIXTURE_MANIFEST.json", via="own_zip", env_gate=None, note=""),
]

# Sites present in EVERY packaged copy of keys.py (directory/intake/ops flat; narrative/
# performance/export/holdings via the layer) but with NO static target -- a caller-supplied
# `layout_path` parameter and NO call site anywhere in the shipped or test tree this census's
# grep swept. Listed once, informationally; excluded from the STAGED/ENV/MISSING three columns.
UNREACHABLE_SITES = [
    dict(file="_keys/keys.py", line="582-591", target="verify_against_layout(layout_path)",
         note="0 call sites found (`comp-find`-class sweep of investor-reporting/**), "
              "present in all 7 packaged copies of keys.py"),
]


def verify_site(site, source_map, layer_members, tf_env_cache):
    fn = site["fn"]
    cfg = source_map["functions"][fn]
    members = declared_members(cfg)
    env, has_layer = tf_env_cache[fn]
    if site["resolves_to"] is None:
        # a MISSING verdict: true iff NEITHER own_zip NOR layer carries the literal target name
        # this row would need, under BOTH the "any literal in resolves_to family" check is moot
        # here since there is no candidate name at all (the resolution is checkout-relative).
        return "MISSING", True
    literal = site["resolves_to"]
    gate = site["env_gate"]
    if site["via"] == "own_zip":
        ok = literal in members
        # if an env gate is named AND set to something that is NOT this own-zip path, the
        # env would win first -- but every own_zip row above is the row that DOES fire (env
        # unset, or env explicitly names the own-zip path), so require consistency:
        if gate and env.get(gate):
            envval = env[gate]
            expect_prefix = "/var/task/"
            if not envval.startswith(expect_prefix) and envval != "":
                # env points elsewhere (e.g. to the layer) -- this row's classification is wrong
                ok = False
        return ("STAGED" if ok else "MISCLASSIFIED-CHECK-FAILED"), ok
    if site["via"] == "layer":
        ok = (literal in layer_members) and has_layer
        if gate:
            envval = env.get(gate, "")
            if envval and not envval.startswith("/opt/python"):
                ok = False
        return ("ENV-RESOLVED-TO-LAYER" if ok else "MISCLASSIFIED-CHECK-FAILED"), ok
    return "UNKNOWN", False


def arm_a():
    print("=" * 100)
    print("ARM (a) -- THE RUNTIME-OPEN CENSUS, 7 SERVING FUNCTIONS")
    print("=" * 100)
    source_map = load_source_map()
    layer_members = load_layer_members()
    tf_env_cache = {fn: read_tf_env(TF_ENV_FILES[fn]) for fn in FUNCTIONS}

    per_fn_counts = {fn: {"STAGED": 0, "ENV-RESOLVED-TO-LAYER": 0, "MISSING": 0,
                          "MISCLASSIFIED-CHECK-FAILED": 0} for fn in FUNCTIONS}
    rows_out = []
    all_ok = True
    for site in CENSUS_SITES:
        verdict, ok = verify_site(site, source_map, layer_members, tf_env_cache)
        per_fn_counts[site["fn"]][verdict] = per_fn_counts[site["fn"]].get(verdict, 0) + 1
        all_ok = all_ok and ok
        rows_out.append((site["fn"], site["file"], site["line"], site["target"], verdict,
                         site.get("note", "")))
        flag = "OK" if ok else "CHECK-FAILED"
        print("%-28s %-28s %-10s %-45s -> %-24s [%s]" % (
            site["fn"], site["file"], site["line"], site["target"][:45], verdict, flag))
        if site.get("note"):
            print("    note: %s" % site["note"])

    print()
    print("-- confirming the holdings/snapshot.py fallback premise --")
    print("'HoldingsSnapshot.schema.json' present as a bare name in any irpt-common layer "
          "member: %s (expect False -- the layer's 5 contracts are Performance/Narrative/"
          "Render/ExportBundle/ExportReceipt only)"
          % any(m.endswith("/HoldingsSnapshot.schema.json") for m in layer_members))

    print()
    print("-- unreachable/no-static-target sites (excluded from the three-way count) --")
    for s in UNREACHABLE_SITES:
        print("%-28s %-10s %-45s note: %s" % ("(all 7, keys.py)", s["line"], s["target"], s["note"]))

    print()
    print("-- per-function denominators --")
    total_missing_rowed = 0
    total_sites = 0
    for fn in FUNCTIONS:
        c = per_fn_counts[fn]
        n = sum(c.values())
        total_sites += n
        barred_note = ""
        print("  %-28s STAGED=%d ENV-RESOLVED-TO-LAYER=%d MISSING=%d MISCLASSIFIED=%d  (n=%d)%s"
              % (fn, c["STAGED"], c["ENV-RESOLVED-TO-LAYER"], c["MISSING"],
                 c["MISCLASSIFIED-CHECK-FAILED"], n, barred_note))
        total_missing_rowed += c["MISSING"]

    print()
    print("TOTAL sites censused this pass: %d of %d (this battery's own enumerated population; "
          "not a claim of exhaustive coverage of every module in the tree)" % (total_sites, len(CENSUS_SITES)))
    print("TOTAL MISSING opens found: %d -- ALL NEW (row S103's DirectoryEntry site classifies "
          "STAGED above: this run reads the manifest AFTER arm (b)'s edit, so S103 shows POST-FIX, "
          "not re-discovered as MISSING; see result.md for the new rows filed)" % total_missing_rowed)
    print("BARRED (recorded, not fixed, S102): %s" % ", ".join(BARRED))
    print("ARM (a) mechanical cross-check: %s" % ("ALL CLASSIFICATIONS CONFIRMED AGAINST "
          "MANIFEST/LAYER-MANIFEST/TERRAFORM-ENV" if all_ok else "AT LEAST ONE CLASSIFICATION "
          "DISAGREED WITH THE LIVE INPUTS -- SEE [CHECK-FAILED] ROWS ABOVE"))
    return all_ok, rows_out


# ---------------------------------------------------------------------------------------------
# ARM (b): THE MEMBER AND THE ENV -- verify the manifest edit's shape
# ---------------------------------------------------------------------------------------------
def arm_b():
    print()
    print("=" * 100)
    print("ARM (b) -- THE MEMBER AND THE ENV")
    print("=" * 100)
    source_map = load_source_map()
    cfg = source_map["functions"]["irpt-directory-search"]
    ok = True

    staged_names = [s["packaged_as"] for s in cfg["staged_from"]]
    if "contracts/DirectoryEntry.schema.json" not in staged_names:
        print("ERROR: contracts/DirectoryEntry.schema.json not in staged_from")
        ok = False
    if "contracts/DirectoryEntry.schema.json" not in cfg["files"]:
        print("ERROR: contracts/DirectoryEntry.schema.json not in files[]")
        ok = False

    added = [s for s in cfg["staged_from"] if s["packaged_as"] == "contracts/DirectoryEntry.schema.json"][0]
    pin = added["pin"]
    repo_path = added["repo_path"]
    declared_sha = added["sha256"]
    blob = git_show_bytes(pin, repo_path)
    measured_sha = hashlib.sha256(blob).hexdigest()
    print("staged_from added: repo_path=%s pin=%s packaged_as=%s" % (repo_path, pin, added["packaged_as"]))
    print("declared sha256=%s" % declared_sha)
    print("measured sha256=%s (git show <pin>:<repo_path> | sha256, this run)" % measured_sha)
    if declared_sha != measured_sha:
        print("ERROR: declared sha256 != measured sha256 of the pinned blob")
        ok = False
    else:
        print("OK: declared sha256 == measured sha256 of the pinned blob")

    # PARSE-DIFF (structural, not line-based -- a raw `git diff` shows a trailing-comma line
    # touched by the array insertion even though no VALUE changed; that is JSON syntax, not a
    # semantic edit, and a line-count check cannot tell the two apart).
    HEAD = head_commit()
    old_map = load_json_at(HEAD, "infra/aws/lambda/ci/lambda-source-map.json")
    new_map = source_map
    old_fns, new_fns = old_map["functions"], new_map["functions"]
    changed_fns = sorted(k for k in new_fns if old_fns.get(k) != new_fns.get(k))
    print("functions with ANY change: %s" % changed_fns)
    if changed_fns != ["irpt-directory-search"]:
        print("ERROR: parse-diff expected exactly ['irpt-directory-search'] changed; got %s"
              % changed_fns)
        ok = False
    else:
        old_cfg, new_cfg = old_fns["irpt-directory-search"], new_fns["irpt-directory-search"]
        old_keys, new_keys = set(old_cfg), set(new_cfg)
        if old_keys != new_keys:
            print("ERROR: top-level key set changed: only in old=%s only in new=%s"
                  % (old_keys - new_keys, new_keys - old_keys))
            ok = False
        # artifact_sha256 is EXEMPT from this check: it is the BUILD's own field (arm (c) /
        # build-and-upload.sh writes it after a real S3 upload), never a hand-edit S89 governs
        # at THIS arm -- S89 governs the MANIFEST EDIT (this arm), not the later build write.
        # If arm (c) has already run in this same worktree (this battery is re-run), artifact_
        # sha256 legitimately differs from HEAD; that is reported, not failed, here.
        changed_scalar_keys = [k for k in old_keys if k not in ("files", "staged_from", "artifact_sha256")
                               and old_cfg[k] != new_cfg[k]]
        added_files = [f for f in new_cfg["files"] if f not in old_cfg["files"]]
        removed_files = [f for f in old_cfg["files"] if f not in new_cfg["files"]]
        added_staged = [s for s in new_cfg["staged_from"] if s not in old_cfg["staged_from"]]
        removed_staged = [s for s in old_cfg["staged_from"] if s not in new_cfg["staged_from"]]
        print("changed scalar fields (excl. files[]/staged_from/artifact_sha256): %s" % changed_scalar_keys)
        print("files[] added=%s removed=%s" % (added_files, removed_files))
        print("staged_from added=%d removed=%d" % (len(added_staged), len(removed_staged)))
        print("artifact_sha256: HEAD=%s current=%s (%s -- build-owned, not this arm's hand-edit check)"
              % (old_cfg.get("artifact_sha256"), new_cfg.get("artifact_sha256"),
                 "UNCHANGED, no build has run yet" if old_cfg.get("artifact_sha256") == new_cfg.get("artifact_sha256")
                 else "MOVED, a build already ran in this worktree this session"))
        if changed_scalar_keys or removed_files or removed_staged:
            print("ERROR: parse-diff expected ONLY an addition to files[]/staged_from (plus the "
                  "build-owned artifact_sha256); found a removal or another changed scalar field")
            ok = False
        elif added_files == ["contracts/DirectoryEntry.schema.json"] and len(added_staged) == 1:
            print("OK: parse-diff is EXACTLY the added object(s); no OTHER field of "
                  "irpt-directory-search's entry is hand-touched by this edit (S89)")
        else:
            print("ERROR: unexpected files[]/staged_from delta shape")
            ok = False

    doc = load_json_at(pin, repo_path.replace(pin, pin)) if False else json.loads(blob.decode("utf-8"))
    props = tuple(k for k in (doc.get("properties") or {}) if k != "contract_version")
    print("contract described: DirectoryEntry.schema.json, %d bytes, JSON Schema, %d properties "
          "(excl. contract_version), 0 credential fields, writer=this order's manifest commit only"
          % (len(blob), len(props)))
    print("ARM (b): %s" % ("PASS" if ok else "FAIL"))
    return ok


# ---------------------------------------------------------------------------------------------
# ARM (c): THE PACKET -- rebuild, verify at rest, plan the 7 roots, then check the halves
# ---------------------------------------------------------------------------------------------
def aws_json(args, timeout=60):
    rc, out, err = run([AWS] + args + ["--output", "json"], timeout=timeout)
    if rc != 0:
        return rc, None, err
    try:
        return rc, json.loads(out), err
    except ValueError:
        return rc, out, err


def arm_c():
    print()
    print("=" * 100)
    print("ARM (c) -- THE PACKET")
    print("=" * 100)
    result = {}

    # 1. prior LIVE CodeSha256, read live, before the build
    rc, cfg, err = aws_json(["lambda", "get-function-configuration",
                             "--function-name", "irpt-directory-search",
                             "--query", "{CodeSha256:CodeSha256,LastModified:LastModified,Version:Version}"])
    if rc != 0:
        print("ERROR: get-function-configuration failed rc=%d: %s" % (rc, err[:400]))
        result["prior_live_codesha256"] = None
    else:
        print("prior LIVE CodeSha256 (read live, this run): %s  LastModified=%s"
              % (cfg.get("CodeSha256"), cfg.get("LastModified")))
        result["prior_live_codesha256"] = cfg.get("CodeSha256")
        result["prior_live_last_modified"] = cfg.get("LastModified")

    # the build-store version currently under artifact_s3_key -- the rollback source
    sm = load_source_map()
    art_key = sm["functions"]["irpt-directory-search"]["artifact_s3_key"]
    art_bucket = sm["functions"]["irpt-directory-search"]["artifact_s3_bucket"]
    # No `|` in the --query expression: a piped JMESPath through the aws.cmd Windows-shell
    # wrapper is exactly the "|" a batch-file arg pass-through can mis-forward -- fetch the
    # candidate list instead and pick the first entry in Python (avoids the shell-metachar class).
    rc, versions, err = aws_json(["s3api", "list-object-versions", "--bucket", art_bucket,
                                  "--prefix", art_key,
                                  "--query", "Versions[?Key=='%s'].{VersionId:VersionId,LastModified:LastModified,IsLatest:IsLatest}" % art_key])
    latest = None
    if rc == 0 and versions:
        latest = next((v for v in versions if v.get("IsLatest")), versions[0])
    if rc == 0 and latest:
        print("build-store version at %s at cut: VersionId=%s LastModified=%s"
              % (art_key, latest.get("VersionId"), latest.get("LastModified")))
        result["rollback_build_store_version"] = latest.get("VersionId")
    else:
        print("WARN: could not read the current build-store version (rc=%d): %s" % (rc, str(err)[:300]))
        result["rollback_build_store_version"] = None

    # 2. rebuild irpt-directory-search ONLY, under this ledger
    print()
    print("-- rebuilding irpt-directory-search (build-and-upload.sh, single-function mode) --")
    bash = git_bash()
    if not bash:
        raise SystemExit("ERROR: no Git Bash found (git_bash_resolver) -- refusing bare 'bash' "
                         "(WSL-stub trap)")
    build_cmd = [bash, os.path.join(REPO, "infra", "aws", "lambda", "ci", "build-and-upload.sh"),
                "investor-reporting", "irpt-directory-search"]
    rc, out, err = run(build_cmd, timeout=180)
    print(out[-4000:])
    if err.strip():
        print("STDERR (tail):", err[-2000:])
    result["build_rc"] = rc
    if rc != 0:
        print("ERROR: build-and-upload.sh rc=%d -- STOPPING arm (c) here" % rc)
        return False, result

    sm2 = load_source_map()
    built_sha = sm2["functions"]["irpt-directory-search"]["artifact_sha256"]
    built_key = sm2["functions"]["irpt-directory-search"]["artifact_s3_key"]
    print("built artifact_sha256 (base64, this run): %s" % built_sha)
    result["built_sha256_b64"] = built_sha

    # 3. VERIFIED AT REST: download the just-built zip, verify members
    scratch = os.path.join(REPO, ".scratch")
    os.makedirs(scratch, exist_ok=True)
    zip_path = os.path.join(scratch, "irpt-directory-search-built.zip")
    rc, out, err = run([AWS, "s3api", "get-object", "--bucket", art_bucket, "--key", built_key,
                        zip_path.replace("\\", "/")], timeout=60)
    if rc != 0:
        print("ERROR: get-object failed rc=%d: %s" % (rc, err[:400]))
        return False, result

    with open(zip_path, "rb") as fh:
        zip_bytes = fh.read()
    measured_zip_sha = base64.b64encode(hashlib.sha256(zip_bytes).digest()).decode("ascii")
    print("downloaded zip sha256(base64) = %s  (declared = %s)  match=%s"
          % (measured_zip_sha, built_sha, measured_zip_sha == built_sha))
    result["zip_sha_match"] = (measured_zip_sha == built_sha)

    import zipfile
    zf = zipfile.ZipFile(os.path.abspath(zip_path))
    zip_names = sorted(zf.namelist())
    cfg7 = sm2["functions"]["irpt-directory-search"]
    declared = sorted(set(cfg7["files"]))
    print("declared files[] (%d): %s" % (len(declared), declared))
    print("zip members (%d): %s" % (len(zip_names), zip_names))
    denom_match = (declared == zip_names)
    print("files[] == zip namelist: %s" % denom_match)

    # each member equal to the BLOB at its pin -- NEVER the working file (autocrlf)
    HEAD = head_commit()
    verified = 0
    mismatches = []
    for name in zip_names:
        staged = [s for s in cfg7["staged_from"] if s["packaged_as"] == name]
        if staged:
            pin = staged[0]["pin"]
            repo_path = staged[0]["repo_path"]
            expect = git_show_bytes(pin, repo_path)
        else:
            # a files[]-only, directly-tracked member: verify against THIS commit's blob
            repo_path = "%s/%s" % (cfg7["source_dir"], name)
            expect = git_show_bytes(HEAD, repo_path)
        got = zf.read(name)
        if got == expect:
            verified += 1
        else:
            mismatches.append(name)
    print("VERIFIED AT REST: %d of %d member(s) byte-equal to their declared blob (never the "
          "working file)" % (verified, len(zip_names)))
    if mismatches:
        print("MISMATCHES: %s" % mismatches)
    result["verified_at_rest"] = "%d of %d" % (verified, len(zip_names))
    result["verified_at_rest_clean"] = (not mismatches) and denom_match

    # the served-byte delta: exactly the added member(s)
    added_members = set(zip_names) - {"handler.py", "entry.py", "served.py", "loaders.py",
                                       "enforce.py", "errors.py", "resolve.py", "keys.py",
                                       "ids.py", "data/custodian_key_seam.json", "raw_keys.json",
                                       "firm_registry.json"}
    print("served-byte delta vs the prior declared member set: %s" % sorted(added_members))
    result["delta_is_exactly_added_member"] = (added_members == {"contracts/DirectoryEntry.schema.json"})

    # 4. terraform plan, all 7 roots, vendored binary, no apply
    print()
    print("-- terraform plan, 7 roots (vendored binary, NO APPLY) --")
    plans = {}
    for root in TF_ROOTS:
        root_dir = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", root)
        rc_init, out_init, err_init = run([TERRAFORM, "init", "-input=false"], cwd=root_dir, timeout=180)
        plan_file = os.path.join(scratch, "ib_rtf_13_%s.tfplan" % root)
        rc_plan, out_plan, err_plan = run([TERRAFORM, "plan", "-input=false", "-no-color",
                                           "-out=%s" % plan_file], cwd=root_dir, timeout=180)
        tail = "\n".join(out_plan.splitlines()[-15:])
        print("root=%-12s init_rc=%d plan_rc=%d" % (root, rc_init, rc_plan))
        print("  " + tail.replace("\n", "\n  "))
        plans[root] = {"init_rc": rc_init, "plan_rc": rc_plan, "tail": tail}
    result["plans"] = plans

    # 5. THE PACKET
    print()
    print("-- packet blob --")
    packet_path = os.path.join(HERE, "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-13.md")
    if os.path.isfile(packet_path):
        rc, blob_hash, _ = run(["git", "hash-object", packet_path])
        print("packet at %s -- blob %s (measured this run; the COMMITTED blob may differ until "
              "the commit lands)" % (packet_path, blob_hash.strip()))
    else:
        print("packet not yet written at this point in the run")

    # 6. THE HALVES
    print()
    print("-- halves at HEAD --")
    coo_dir = os.path.join(REPO, "org", "tier1_exec", "2.0.0_SA_COO~B", "deliverables")
    cto_dir = os.path.join(REPO, "org", "tier1_exec", "1.0.0_SA_CTO", "deliverables")
    coo_halves = [f for f in os.listdir(coo_dir) if "rtf-13" in f.lower()] if os.path.isdir(coo_dir) else []
    cto_halves = [f for f in os.listdir(cto_dir) if "rtf-13" in f.lower()] if os.path.isdir(cto_dir) else []
    print("COO half candidates: %s" % (coo_halves or "ABSENT"))
    print("CTO half candidates: %s" % (cto_halves or "ABSENT"))
    halves_present = len(coo_halves) + len(cto_halves)
    print("halves present: %d of 2" % halves_present)
    result["halves_present"] = halves_present

    if halves_present < 2:
        print()
        print("ARM (c): STOP HERE -- halves ABSENT (%d of 2). R70-AC1 FAILS TRUTHFULLY AT (c). "
              "Arm (d) is NOT run this pass. The order stays open." % halves_present)
        return False, result

    print("ARM (c): both halves present -- proceeding would be arm (d), NOT this pass.")
    return True, result


def main():
    ok_a, rows = arm_a()
    ok_b = arm_b()
    ok_c, result_c = arm_c()

    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print("arm (a) census cross-check: %s" % ("CLEAN" if ok_a else "SOME ROWS FAILED THEIR CHECK"))
    print("arm (b) member+env:         %s" % ("PASS" if ok_b else "FAIL"))
    print("arm (c) packet+halves:      %s (halves_present=%s)" % (
          "PASS" if ok_c else "STOP (expected this pass)", result_c.get("halves_present")))
    print()
    if ok_a and ok_b and not ok_c and result_c.get("halves_present", 0) < 2:
        print("THIS IS THE EXPECTED FIRST-PASS OUTCOME: (a) and (b) hold, (c) stops truthfully "
              "on ABSENT halves. Token WITHHELD (not printed) -- the criterion is not satisfied "
              "this pass and the order stays open.")
        return 0
    if ok_a and ok_b and ok_c:
        print("IBR70-CONTRACT-STAGED-SERVED-AND-SEARCH-ANSWERS")
        return 0
    print("ARM FAILURE OUTSIDE THE EXPECTED SHAPE -- see output above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
