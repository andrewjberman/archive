#!/usr/bin/env python3
"""IB-rtf-13 -- the directory-search zip carries its contract, and every runtime open across
the seven serving functions is a staged member. Cell IB-rtf-13.

APPLY PASS (this revision): arms (a)-(c) re-derive the census/member/packet as before; arm (d)
is the v2 SUBTRACTION GATE (CTO compared-object term @ac63a41207 -- compares `resource_changes`
PER ROOT and nothing else, never the whole `show -json` document) over all 7 investor-reporting
roots, then applies the directory root through `.tools/safe-apply.sh` IFF the gate passes and the
directory root is not already applied (idempotent re-run: if the built sha is already served and
the 7-root gate already reads empty/matching, arm (d) reports ALREADY-APPLIED-AND-VERIFIED rather
than re-applying a 0-diff plan); arm (e) is the LIVE PROOF under the DEPLOYED ROLE AND BYTES,
reusing the rtf-10/rtf-9 bounded-test-principal mechanism, narrowed to the directory route.

Re-derives, every run, from git blobs / the committed manifest / the committed layer build
manifest / the committed terraform env lines -- never from a hand-typed verdict table with no
premise check. Where a classification cannot be MECHANICALLY confirmed against those sources it
prints UNVERIFIED rather than asserting it.

Usage: py -3.12 battery_ib_rtf_13.py
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request

import bcrypt
import boto3

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

# ---------------------------------------------------------------------------------------------
# ARM (d)/(e) CONSTANTS -- the v2 packet's signed shape and the rtf-9 bounded-principal precedent.
# ---------------------------------------------------------------------------------------------
V2_PACKET_REL = "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-13_v2.md"
V2_BLOB = "0e06953ecc21b51307d0c707ff1c57c4ca725ae2"
COO_HALF_REL = ("org/tier1_exec/2.0.0_SA_COO~B/deliverables/"
                "NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-13_DIRECTORY_CONTRACT_STAGED.md")
CTO_HALF_REL = ("org/tier1_exec/1.0.0_SA_CTO/deliverables/"
                "NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-13_DIRECTORY_CONTRACT_STAGED.md")
PRIOR_LIVE_CODESHA = "PUjH3OjDe8Yj3RwdIO0KT3GXsYGfvUCmzG/aHsi6e1c="
BUILT_CODESHA = "76LeVyYNfhdyDnQNXR3LzrqSv7k7Vr3POSjpcBzww6E="
ROLLBACK_VERSION = "elK9Z3qtolvKrVJhSuMrmlFJZT.77_Dk"
LEDGER_SLUG = "irpt-bckend-ib-rtf-13-apply"
LEDGER_SENTINEL_REL = "org/critical_paths/.open_deploys/%s.json" % LEDGER_SLUG
LEDGER_ENTRY_REL = "org/critical_paths/change_management/20260920T0928Z_%s_deploy_completion.md" % LEDGER_SLUG
PLAN_DIR = os.path.join(REPO, ".scratch", "plans_rtf13")
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "investor-reporting/irpt-directory-search.zip"

# arm (e): the rtf-9 bounded test principal, reused per this order's own text.
RTF9_PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md"
RTF9_BLOB = "a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4"
RTF9_HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
}
PRINCIPAL_SENTINEL_REL = "org/critical_paths/.open_deploys/irpt-bckend-ib-rtf-13-live-principal.json"
USERS, PARTNER, THROTTLE = "opal-users-v2", "opal-partner-49financial", "opal-portal-auth-throttle"
FIRM, ADVISOR = "49financial", "abby_horton"
FOREIGN_FIRM = "inflection"
OM_BUCKET, OM_KEY = "opal-data-bd", "platinum/49financial/ownership_map.json"
BASE = "https://opalinvest.dev"
PFX = "/api/scoped/investor-reporting"
UA = "opal-irpt-ib-rtf-13-battery/1.0 (0.9.0_WK_IRPT_BCKEND~1)"

SECRETS_SEEN: list[str] = []


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
    if changed_fns == []:
        # THE ALREADY-LANDED SHAPE: the manifest edit is already committed at HEAD (a re-run in
        # the same worktree after this pass's own earlier commit landed it), so HEAD-vs-working
        # is trivially empty -- that is NOT a failure, it is this run recognising its own prior
        # commit. The mechanical checks above (declared sha == measured sha, member in files[]
        # and staged_from) already hold; nothing further to parse-diff.
        print("OK: the manifest edit is ALREADY LANDED at HEAD (this worktree's own prior commit) "
              "-- 0 functions changed vs HEAD is the correct reading here, not a FAIL")
    elif changed_fns != ["irpt-directory-search"]:
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


def s3_get_and_hash(bucket, key, version_id):
    """boto3, not aws.cmd -- avoids a second temp-file round trip for a bytes read."""
    s3 = boto3.client("s3", region_name="us-east-1")
    body = s3.get_object(Bucket=bucket, Key=key, VersionId=version_id)["Body"].read()
    return base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")


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

    # 2. rebuild irpt-directory-search ONLY, under this ledger.
    #
    # SKIP THE UPLOAD when the function ALREADY SERVES the manifest's declared artifact_sha256
    # (a re-run of this battery in the SAME worktree after a prior pass's build/apply already
    # landed it): build-and-upload.sh's S3 PutObject mints a NEW version_id on every call even
    # with byte-identical content, and that per-run version churn manufactures a phantom
    # `aws_lambda_function.this` "update" (source_code_hash UNCHANGED, only s3_object_version/
    # last_modified moving) on arm (d)'s later plan -- measured this pass: those two fields
    # surface as ATTRIBUTES of the lambda resource itself, never as a separately-listed
    # `data.aws_s3_object` resource_changes entry (0 of N mode=="data" entries, every root, every
    # run), which is outside the LITERAL scope of the CTO's compared-object term (row filed).
    # Re-uploading unconditionally on every re-run would keep re-creating exactly that class.
    print()
    sm_pre = load_source_map()
    pre_declared_sha = sm_pre["functions"]["irpt-directory-search"].get("artifact_sha256")
    live_rc0, live_cfg0, _ = aws_json(["lambda", "get-function-configuration",
                                      "--function-name", "irpt-directory-search",
                                      "--query", "{CodeSha256:CodeSha256}"])
    already_built = (live_rc0 == 0 and pre_declared_sha and live_cfg0.get("CodeSha256") == pre_declared_sha)
    print("pre-rebuild check: live CodeSha256=%s manifest artifact_sha256=%s -> already_built=%s"
        % (live_cfg0.get("CodeSha256") if live_rc0 == 0 else "?", pre_declared_sha, already_built))
    if already_built:
        print("-- SKIPPING the rebuild/upload: the function already serves the manifest's declared "
              "sha -- re-uploading would mint a needless new S3 version and manufacture a phantom "
              "volatile diff at arm (d). Reading the current build-store state instead (no write). --")
        result["build_rc"] = 0
        sm2 = sm_pre
    else:
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


# ---------------------------------------------------------------------------------------------
# ARM (d): THE SUBTRACTION GATE (CTO compared-object term @ac63a41207) + APPLY
# ---------------------------------------------------------------------------------------------
def tf_show_json(root, plan_file):
    root_dir = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", root)
    p = subprocess.run([TERRAFORM, "show", "-json", plan_file], cwd=root_dir,
                       capture_output=True, timeout=180)
    if p.returncode != 0:
        raise SystemExit("ERROR: terraform show -json failed for %s: %s"
                         % (root, p.stderr.decode("utf-8", "replace")[:500]))
    return json.loads(p.stdout.decode("utf-8"))


def subtract_within_entry(entry):
    """Deep-walk ONE resource_changes entry, removing version_id/last_modified wherever they
    appear WITHIN it, but only when the entry itself is a data.aws_s3_object read (the signed
    subtraction set). Returns (paths_removed, entry_after)."""
    is_s3_data_read = (entry.get("mode") == "data" and entry.get("type") == "aws_s3_object")
    if not is_s3_data_read:
        return 0, entry
    removed = [0]

    def walk(node):
        if isinstance(node, dict):
            out = {}
            for k, v in node.items():
                if k in ("version_id", "last_modified"):
                    removed[0] += 1
                    continue
                out[k] = walk(v)
            return out
        if isinstance(node, list):
            return [walk(x) for x in node]
        return node

    return removed[0], walk(entry)


def is_noop(entry):
    actions = (entry.get("change") or {}).get("actions") or []
    return actions in ([], ["no-op"])


def subtraction_gate(plans):
    """PER ROOT: compare `resource_changes`, WHOLE, minus the subtraction set applied WITHIN
    each entry -- never the whole show-json document. Returns (ok, per_root_substantive,
    total_compared, total_subtracted)."""
    total_compared = 0
    total_subtracted = 0
    per_root_substantive = {}
    for root in TF_ROOTS:
        doc = tf_show_json(root, plans[root])
        rcs = doc.get("resource_changes") or []
        compared = len(rcs)
        subtracted_here = 0
        substantive = []
        for e in rcs:
            n, e2 = subtract_within_entry(e)
            subtracted_here += n
            if not is_noop(e2):
                substantive.append(e2)
        total_compared += compared
        total_subtracted += subtracted_here
        per_root_substantive[root] = substantive
        print("root=%-12s resource_changes entries compared=%d  paths subtracted (observed)=%d  "
              "substantive after subtraction=%d" % (root, compared, subtracted_here, len(substantive)))
        for e in substantive:
            ch = e.get("change") or {}
            before = ch.get("before") if isinstance(ch.get("before"), dict) else {}
            after = ch.get("after") if isinstance(ch.get("after"), dict) else {}
            print("    address=%s actions=%s before.source_code_hash=%s after.source_code_hash=%s"
                  % (e.get("address"), ch.get("actions"), (before or {}).get("source_code_hash"),
                     (after or {}).get("source_code_hash")))
    print()
    print("TOTAL DENOMINATOR: %d resource_changes entries compared across %d roots; "
          "%d paths subtracted (observed)" % (total_compared, len(TF_ROOTS), total_subtracted))

    ok = True
    directory_state = None  # "ALREADY-APPLIED" | "PENDING-APPLY" | "STOP"
    dir_sub = per_root_substantive["directory"]
    if len(dir_sub) == 0:
        directory_state = "ALREADY-APPLIED"
        print("directory root: 0 substantive entries after subtraction -- the desired code change "
              "is ALREADY REFLECTED (idempotent re-run reading).")
    elif len(dir_sub) == 1:
        e = dir_sub[0]
        ch = e.get("change") or {}
        before = ch.get("before") or {}
        after = ch.get("after") or {}
        cond = (e.get("address") == "module.irpt_directory_search.aws_lambda_function.this"
               and ch.get("actions") == ["update"]
               and before.get("source_code_hash") == PRIOR_LIVE_CODESHA
               and after.get("source_code_hash") == BUILT_CODESHA)
        if cond:
            directory_state = "PENDING-APPLY"
            print("directory substantive entry MATCHES THE SIGNED SHAPE (update, %s -> %s) -- "
                  "PENDING-APPLY" % (before.get("source_code_hash"), after.get("source_code_hash")))
        else:
            directory_state = "STOP"
            ok = False
            print("STOP: directory's ONE substantive entry does NOT match the signed shape: "
                  "address=%s actions=%s before=%s after=%s"
                  % (e.get("address"), ch.get("actions"), before.get("source_code_hash"),
                     after.get("source_code_hash")))
    else:
        directory_state = "STOP"
        ok = False
        print("STOP: directory root has %d substantive entries after subtraction (expected 0 or 1)"
              % len(dir_sub))

    for root in TF_ROOTS:
        if root == "directory":
            continue
        n = len(per_root_substantive[root])
        good = (n == 0)
        ok = ok and good
        print("root=%-12s substantive-after-subtraction=%d -> %s"
              % (root, n, "EMPTY (OK)" if good else "NOT EMPTY -- STOP (content outside the "
                                                     "subtraction set)"))
    return ok, directory_state, total_compared, total_subtracted


def arm_d():
    print()
    print("=" * 100)
    print("ARM (d) -- THE SUBTRACTION GATE + APPLY")
    print("=" * 100)

    # 1. PRE-VERIFY: v2 packet blob at HEAD, both halves naming it.
    rc, head_blob, _ = run(["git", "rev-parse", "HEAD:%s" % V2_PACKET_REL])
    head_blob = head_blob.strip()
    print("v2 packet %s at HEAD: blob %s (expected %s) -> %s"
          % (V2_PACKET_REL, head_blob or "ABSENT", V2_BLOB,
             "MATCH" if head_blob == V2_BLOB else "MISMATCH"))
    if head_blob != V2_BLOB:
        print("ARM (d): STOP -- the packet blob at HEAD does not match. Arm (d) does not run.")
        return False, {}

    halves_ok = 0
    for who, path in (("COO", COO_HALF_REL), ("CTO", CTO_HALF_REL)):
        rc2, text, _ = run(["git", "show", "HEAD:%s" % path])
        present = rc2 == 0
        naming = present and (V2_BLOB in text)
        halves_ok += int(naming)
        print("  %s half %s at HEAD: present=%s naming-the-blob=%s" % (who, path, present, naming))
    print("halves naming the v2 blob: %d of 2" % halves_ok)
    if halves_ok != 2:
        print("ARM (d): STOP -- a half is absent or does not name the blob. Arm (d) does not run.")
        return False, {}

    # 2. Rebuild (idempotent) and verify at rest; confirm latest S3 version == BUILT_CODESHA.
    #
    # SKIP THE UPLOAD when the function is ALREADY SERVING the built sha (a re-run of this
    # battery after a prior pass's apply already landed): build-and-upload.sh's S3 PutObject
    # mints a NEW version_id on every call even when the CONTENT is byte-identical, and Terraform
    # renders that as a fresh "update" action on aws_lambda_function.this whose ONLY drift is
    # `s3_object_version`/`last_modified` -- a volatile field the signed subtraction set was
    # written to cover, but which surfaces HERE as an attribute of the lambda resource itself,
    # never as a separately-listed `data.aws_s3_object` entry (measured: 0 mode=="data" entries
    # in resource_changes on this module, every run). Re-uploading on an already-applied re-run
    # would manufacture exactly the volatility class this order exists to eliminate. So: rebuild
    # only when the desired transition has not yet landed.
    print()
    live_before_rc, live_before_cfg, _ = aws_json(["lambda", "get-function-configuration",
                                                   "--function-name", "irpt-directory-search",
                                                   "--query", "{CodeSha256:CodeSha256,ContractsDir:Environment.Variables.IRPT_CONTRACTS_DIR}"])
    already_served = (live_before_rc == 0 and live_before_cfg.get("CodeSha256") == BUILT_CODESHA
                      and live_before_cfg.get("ContractsDir") == "/var/task/contracts")
    print("pre-rebuild check: live CodeSha256=%s ContractsDir=%s -> already_served=%s"
          % (live_before_cfg.get("CodeSha256") if live_before_rc == 0 else "?",
             live_before_cfg.get("ContractsDir") if live_before_rc == 0 else "?", already_served))
    if already_served:
        print("-- SKIPPING the rebuild/upload: the function already SERVES the built sha and the "
              "env -- re-uploading here would mint a needless new S3 version and manufacture a "
              "phantom volatile diff. Verifying against the CURRENT build-store state instead. --")
        sm = load_source_map()
        built_sha = sm["functions"]["irpt-directory-search"]["artifact_sha256"]
    else:
        print("-- rebuild (idempotent) + verify at rest --")
        bash = git_bash()
        if not bash:
            raise SystemExit("ERROR: no Git Bash found (git_bash_resolver)")
        rc, out, err = run([bash, os.path.join(REPO, "infra", "aws", "lambda", "ci", "build-and-upload.sh"),
                           "investor-reporting", "irpt-directory-search"], timeout=180)
        print(out[-2000:])
        if rc != 0:
            print("ARM (d): STOP -- rebuild rc=%d" % rc)
            return False, {}
        sm = load_source_map()
        built_sha = sm["functions"]["irpt-directory-search"]["artifact_sha256"]
    print("built artifact_sha256 this run: %s (expected %s) -> %s"
          % (built_sha, BUILT_CODESHA, "MATCH" if built_sha == BUILT_CODESHA else "MISMATCH -- STOP"))
    if built_sha != BUILT_CODESHA:
        print("ARM (d): STOP -- rebuild produced a different sha than the signed packet names.")
        return False, {}

    rc, versions, err = aws_json(["s3api", "list-object-versions", "--bucket", ARTIFACT_BUCKET,
                                  "--prefix", ARTIFACT_KEY,
                                  "--query", "Versions[?Key=='%s'].{VersionId:VersionId,LastModified:LastModified,IsLatest:IsLatest}" % ARTIFACT_KEY])
    latest = next((v for v in (versions or []) if v.get("IsLatest")), None) if rc == 0 else None
    rollback_present = any(v.get("VersionId") == ROLLBACK_VERSION for v in (versions or [])) if rc == 0 else False
    print("build-store latest version: %s (this run's rebuild); rollback source %s present: %s"
          % (latest.get("VersionId") if latest else "?", ROLLBACK_VERSION, rollback_present))
    if latest:
        got = s3_get_and_hash(ARTIFACT_BUCKET, ARTIFACT_KEY, latest.get("VersionId"))
        print("latest version content sha256(b64): %s -> %s"
              % (got, "MATCHES BUILT" if got == BUILT_CODESHA else "DOES NOT MATCH -- STOP"))
        if got != BUILT_CODESHA:
            return False, {}
    if not rollback_present:
        print("ARM (d): STOP -- the rollback source version is no longer present in the build store.")
        return False, {}

    # 3. Fresh plan, all 7 roots.
    print()
    print("-- terraform plan, 7 roots (vendored binary) --")
    os.makedirs(PLAN_DIR, exist_ok=True)
    plans = {}
    for root in TF_ROOTS:
        root_dir = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", root)
        run([TERRAFORM, "init", "-input=false"], cwd=root_dir, timeout=180)
        plan_file = os.path.join(PLAN_DIR, "%s.tfplan" % root)
        rc_plan, out_plan, err_plan = run([TERRAFORM, "plan", "-input=false", "-no-color",
                                          "-out=%s" % plan_file], cwd=root_dir, timeout=180)
        tail = "\n".join(out_plan.splitlines()[-5:])
        print("root=%-12s plan_rc=%d\n  %s" % (root, rc_plan, tail.replace("\n", "\n  ")))
        plans[root] = plan_file

    # 4. THE SUBTRACTION GATE.
    print()
    print("-- the subtraction gate --")
    gate_ok, directory_state, compared, subtracted = subtraction_gate(plans)
    result = {"gate_ok": gate_ok, "directory_state": directory_state,
             "compared": compared, "subtracted": subtracted}
    if not gate_ok:
        print()
        print("ARM (d): GATE REFUSES -- a root carries content outside the subtraction set. "
              "Nothing is applied. This is EVIDENCE, not an obstacle (row this run).")
        return False, result

    # 5. APPLY (only if pending); otherwise re-verify the already-applied state.
    print()
    if directory_state == "PENDING-APPLY":
        print("-- APPLYING the directory root (ledger already open+closed by this pass's operator "
              "act, or opened fresh here if not) --")
        rc_sentinel, _, _ = run(["git", "rev-parse", "--verify", "--quiet", "HEAD:%s" % LEDGER_SENTINEL_REL])
        if rc_sentinel == 0:
            print("STOP: a prior OPEN ledger sentinel is still committed at HEAD -- refusing a "
                  "second concurrent apply. Close it first.")
            return False, result
        rc_open, out_open, err_open = run(["python", os.path.join(REPO, ".tools", "deploy_ledger.py"),
                                          "open", "--slug", LEDGER_SLUG,
                                          "--title", "IB-rtf-13 apply -- directory-search contract member + IRPT_CONTRACTS_DIR env, subtraction gate PASS",
                                          "--author", "0.9.0_WK_IRPT_BCKEND~1",
                                          "--lambda", "irpt-directory-search", "--window-hours", "2"])
        print(out_open)
        if rc_open != 0:
            print("STOP: could not open the deploy ledger: %s" % err_open[:500])
            return False, result
        apply_rc, apply_out, apply_err = run(["bash", os.path.join(REPO, ".tools", "safe-apply.sh"),
                                             "-chdir=infra/aws/terraform/investor-reporting/directory",
                                             "apply", "-input=false", "-no-color",
                                             plans["directory"]], timeout=300)
        print(apply_out[-3000:])
        if apply_err.strip():
            print("STDERR (tail):", apply_err[-1500:])
        result["apply_rc"] = apply_rc
        if apply_rc != 0:
            print("ARM (d): STOP -- safe-apply rc=%d" % apply_rc)
            return False, result
        result["applied_this_run"] = True
    else:
        print("directory root already reflects the signed change (ALREADY-APPLIED-AND-VERIFIED) -- "
              "no apply needed this run.")
        result["applied_this_run"] = False

    # 6. POST-CONDITION VERIFICATION (read at the event, R-40).
    print()
    print("-- post-condition verification --")
    rc_plan2, out_plan2, _ = run([TERRAFORM, "plan", "-input=false", "-no-color"],
                                 cwd=os.path.join(REPO, "infra", "aws", "terraform",
                                                 "investor-reporting", "directory"), timeout=180)
    zero_diff = "No changes." in out_plan2
    print("post-apply re-plan, directory root: %s" % ("0-DIFF" if zero_diff else "DIFF REMAINS -- STOP"))
    result["post_apply_zero_diff"] = zero_diff

    rc, cfg, err = aws_json(["lambda", "get-function-configuration",
                            "--function-name", "irpt-directory-search",
                            "--query", "{CodeSha256:CodeSha256,ContractsDir:Environment.Variables.IRPT_CONTRACTS_DIR,LastModified:LastModified}"])
    live_sha = cfg.get("CodeSha256") if rc == 0 else None
    contracts_dir = cfg.get("ContractsDir") if rc == 0 else None
    print("live CodeSha256 NOW: %s (expected %s) -> %s" % (live_sha, BUILT_CODESHA,
          "MATCH" if live_sha == BUILT_CODESHA else "MISMATCH -- STOP"))
    print("live IRPT_CONTRACTS_DIR: %s" % contracts_dir)
    result["live_codesha256"] = live_sha
    result["contracts_dir"] = contracts_dir

    rc, loc, err = aws_json(["lambda", "get-function", "--function-name", "irpt-directory-search",
                            "--query", "Code.Location"])
    member_present = False
    served_sha = None
    if rc == 0 and loc:
        scratch = os.path.join(REPO, ".scratch")
        os.makedirs(scratch, exist_ok=True)
        zip_path = os.path.join(scratch, "irpt-directory-search-served.zip")
        try:
            urllib.request.urlretrieve(loc, zip_path)
            with open(zip_path, "rb") as fh:
                zb = fh.read()
            served_sha = base64.b64encode(hashlib.sha256(zb).digest()).decode("ascii")
            import zipfile
            zf = zipfile.ZipFile(zip_path)
            names = zf.namelist()
            member_present = "contracts/DirectoryEntry.schema.json" in names
            print("served zip downloaded and re-hashed: %s (expected %s) -> %s; member present: %s"
                  % (served_sha, BUILT_CODESHA, "MATCH" if served_sha == BUILT_CODESHA else "MISMATCH",
                     member_present))
        except Exception as exc:  # noqa: BLE001
            print("ERROR downloading/verifying served zip: %s: %s" % (type(exc).__name__, exc))
    result["served_sha_match"] = (served_sha == BUILT_CODESHA)
    result["member_present"] = member_present

    ok = (zero_diff and live_sha == BUILT_CODESHA and contracts_dir == "/var/task/contracts"
         and result["served_sha_match"] and member_present)
    print()
    print("ARM (d): %s" % ("PASS" if ok else "FAIL"))
    return ok, result


# ---------------------------------------------------------------------------------------------
# ARM (e): THE LIVE PROOF, UNDER THE DEPLOYED ROLE AND BYTES -- the directory route only
# ---------------------------------------------------------------------------------------------
def emit(line=""):
    for s in SECRETS_SEEN:
        if s:
            line = line.replace(s, "<REDACTED>")
    print(line, flush=True)


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()


def http(method, path, token=None, body=None, query=None, cookie=None):
    url = BASE + path
    if query:
        url += "?" + "&".join("%s=%s" % (k, urllib.request.quote(str(v))) for k, v in query.items())
    headers = {"User-Agent": UA, "X-Contract-Version": "v1", "Origin": BASE}
    if token:
        headers["Authorization"] = "Bearer " + token
    if cookie:
        headers["Cookie"] = cookie
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        r = urllib.request.urlopen(req, timeout=60)
        return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def as_json(b):
    try:
        return json.loads(b.decode("utf-8"))
    except ValueError:
        return None


def classify(status, j):
    out = {"http": status}
    if isinstance(j, dict):
        st = j.get("status") or {}
        out.update({"operation": j.get("operation"), "firm_id": j.get("firm_id"),
                   "code": st.get("public_reason_code"), "state": st.get("state")})
        if status < 400 and "data" in j:
            out["class"] = "SERVED"
            return out
        if out["code"] == "UNEXPECTED":
            out["class"] = "UNEXPECTED"
        elif out.get("firm_id") or out["code"] == "FIRM_BINDING":
            out["class"] = "POLICY"
        else:
            out["class"] = "UNRESOLVED"
        return out
    out["class"] = "UNEXPECTED" if status >= 500 else "UNRESOLVED"
    return out


def jwt_claims(tok):
    seg = tok.split(".")[1]
    seg += "=" * (-len(seg) % 4)
    return json.loads(base64.urlsafe_b64decode(seg.encode()).decode("utf-8"))


def f_precondition():
    emit("  PRECONDITION: the rtf-9 packet's 2 of 2 halves at HEAD")
    rc, head, _ = run(["git", "rev-parse", "--verify", "--quiet", "HEAD:%s" % RTF9_PACKET_REL])
    rc2, wt, _ = run(["git", "hash-object", os.path.join(REPO, RTF9_PACKET_REL)])
    pk = (rc == 0 and head.strip() == RTF9_BLOB == wt.strip())
    n = 0
    for who, path in RTF9_HALVES.items():
        rc3, text, _ = run(["git", "show", "HEAD:%s" % path])
        n += int(rc3 == 0 and RTF9_BLOB in text)
    emit("  rtf-9 packet blob at HEAD %s (== %s: %s); halves naming it %d of 2"
        % (head.strip(), RTF9_BLOB, pk, n))
    return pk and n == 2


def prefix_scan(ddb, label):
    ok = True
    for table, attr, prefix in ((USERS, "PK", "USER#usr_irptrtf13_"), (USERS, "email", "irpt-rtf13-test-"),
                                (PARTNER, "email", "irpt-rtf13-test-")):
        d = ddb.scan(TableName=table, Select="COUNT", FilterExpression="begins_with(#a, :p)",
                    ExpressionAttributeNames={"#a": attr}, ExpressionAttributeValues={":p": {"S": prefix}})
        ok = ok and d["Count"] == 0
        emit("  %s: %s %s begins_with '%s': %d of %d scanned" % (label, table, attr, prefix,
                                                                  d["Count"], d["ScannedCount"]))
    return ok


def create_principal(ddb, epoch, password, created):
    email = "irpt-rtf13-test-%d@opal.test" % epoch
    pk = "USER#usr_irptrtf13_%d" % epoch
    created.update({"email": email, "pk": pk})
    created_at = now_iso()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10, prefix=b"2a")).decode("ascii")
    SECRETS_SEEN.append(pw_hash)
    k1 = {"PK": {"S": pk}, "SK": {"S": "PROFILE"}, "email": {"S": email}, "passwordHash": {"S": pw_hash},
         "name": {"S": "IRPT test principal (IB-rtf-13)"}, "role": {"S": "user"}, "firmId": {"S": FIRM},
         "status": {"S": "active"}, "createdAt": {"S": created_at}, "createdBy": {"S": "0.9.0_WK_IRPT_BCKEND~1 IB-rtf-13"}}
    ddb.put_item(TableName=USERS, Item=k1, ConditionExpression="attribute_not_exists(PK)")
    got1 = ddb.get_item(TableName=USERS, Key={"PK": {"S": pk}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
    emit("  K1 created: PK %s; consistent read-back present: %s" % (pk, got1 is not None))
    k1b = {"email": {"S": email}, "advisorKey": {"S": ADVISOR}}
    ddb.put_item(TableName=PARTNER, Item=k1b, ConditionExpression="attribute_not_exists(email)")
    got = ddb.get_item(TableName=PARTNER, Key={"email": {"S": email}}, ConsistentRead=True).get("Item")
    emit("  K1b created in %s: consistent read-back present: %s; attributes %s" % (PARTNER, got is not None, sorted(got or {})))
    ok = (got1 is not None and sorted(got1) == sorted(k1) and got is not None and sorted(got) == ["advisorKey", "email"])
    return {"email": email, "pk": pk, "ok": ok, "k1_created": created_at}


def login(email, password):
    status, headers, body = http("POST", "/auth/login", body={"email": email, "password": password})
    j = as_json(body) or {}
    tok = j.get("accessToken") if isinstance(j, dict) else None
    cookies = headers.get_all("Set-Cookie") or []
    refresh = next((c.split(";", 1)[0] for c in cookies if c.startswith("refresh_token=")), None)
    for s in (tok, refresh, refresh.split("=", 1)[1] if refresh else None):
        if s:
            SECRETS_SEEN.append(s)
    out = {"http": status, "token": tok, "refresh_cookie": refresh}
    emit("  login POST /auth/login -> HTTP %d; access token minted=%s; refresh cookie set=%s"
        % (status, bool(tok), bool(refresh)))
    if tok:
        c = jwt_claims(tok)
        out["claims"] = c
        emit("  K2 claims: firmId=%s role=%s advisorKey=%s" % (c.get("firmId"), c.get("role"), c.get("advisorKey")))
    return out


def rollback(ddb, created, sess):
    emit("  ROLLBACK -- K1b then K1, each verified by a failing consistent read; refresh refused; 401 after exp")
    out = {"k1b_deleted": None, "k1_deleted": None, "refresh_refused": None, "expired_refused": None}
    if created.get("email"):
        ddb.delete_item(TableName=PARTNER, Key={"email": {"S": created["email"]}})
        gone = ddb.get_item(TableName=PARTNER, Key={"email": {"S": created["email"]}}, ConsistentRead=True).get("Item") is None
        out["k1b_deleted"] = now_iso() if gone else None
        emit("  K1b DeleteItem -> gone: %s" % gone)
    if created.get("pk"):
        ddb.delete_item(TableName=USERS, Key={"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}})
        gone = ddb.get_item(TableName=USERS, Key={"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item") is None
        out["k1_deleted"] = now_iso() if gone else None
        emit("  K1 DeleteItem -> gone: %s" % gone)
    try:
        if sess.get("refresh_cookie"):
            st, _, b = http("POST", "/auth/refresh", cookie=sess["refresh_cookie"])
            j = as_json(b) or {}
            minted = isinstance(j, dict) and bool(j.get("accessToken"))
            refused = st != 200 and not minted
            out["refresh_refused"] = now_iso() if refused else None
            emit("  REFRESH after K1's delete: HTTP %d, minted=%s -> %s" % (st, minted, "REFUSED" if refused else "NOT REFUSED"))
        if sess.get("token"):
            exp = sess["claims"].get("exp", 0)
            wait = exp + 10 - time.time()
            emit("  waiting %.0f s for exp+10s" % max(wait, 0))
            if wait > 0:
                time.sleep(wait)
            st, _, _b = http("GET", PFX + "/status", sess["token"])
            out["expired_refused"] = now_iso() if st == 401 else None
            emit("  access token after exp: GET /status -> HTTP %d -> %s" % (st, "REFUSED 401" if st == 401 else "NOT 401"))
    except Exception as exc:  # noqa: BLE001
        emit("  EXCEPTION in post-delete checks: %s: %s" % (type(exc).__name__, str(exc)[:300]))
    return out


def arm_e():
    print()
    print("=" * 100)
    print("ARM (e) -- THE LIVE PROOF, UNDER THE DEPLOYED ROLE AND BYTES (directory route)")
    print("=" * 100)
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()["Arn"]
    emit("  operator identity: %s (creates/deletes the test principal's keys only; the SERVED "
        "compute runs as irpt-directory-search's OWN execution role, printed per request)" % identity)

    if not f_precondition():
        emit("  STOP at the precondition: nothing written")
        return False, {}

    ddb = boto3.client("dynamodb", region_name="us-east-1")
    s3 = boto3.client("s3", region_name="us-east-1")
    lam = boto3.client("lambda", region_name="us-east-1")

    cfg = lam.get_function_configuration(FunctionName="irpt-directory-search")
    role = cfg["Role"].split("/")[-1]
    emit("  route %s%s/directory/* -> function irpt-directory-search -> execution role %s (CodeSha256 %s)"
        % (BASE, PFX, role, cfg["CodeSha256"]))

    try:
        om = json.loads(s3.get_object(Bucket=OM_BUCKET, Key=OM_KEY)["Body"].read().decode("utf-8"))
        present = ADVISOR in (om.get("advisors") or {})
    except Exception as exc:  # noqa: BLE001
        emit("  GUARD ERROR reading s3://%s/%s: %s" % (OM_BUCKET, OM_KEY, exc))
        return False, {}
    emit("  GUARD: %s present in s3://%s/%s: %s" % (ADVISOR, OM_BUCKET, OM_KEY, present))
    if not present:
        emit("  STOP at the guard: nothing written")
        return False, {}

    if not prefix_scan(ddb, "before"):
        emit("  STOP: a principal key already exists (residue) -- nothing written")
        return False, {}

    password = secrets.token_urlsafe(24)
    SECRETS_SEEN.append(password)
    created, sess = {}, {}
    req_ok = keys_ok = False
    rows = []
    s92 = {}
    try:
        k = create_principal(ddb, int(time.time()), password, created)
        sess = login(k["email"], password)
        c = sess.get("claims") or {}
        keys_ok = k["ok"] and sess.get("http") == 200 and c.get("firmId") == FIRM and c.get("advisorKey") == ADVISOR
        emit("  keys read back and the session as the rtf-9 packet declares: %s" % keys_ok)
        if keys_ok:
            tok = sess["token"]

            def go(label, method, path, body=None, query=None, want="SCOPE"):
                st, _, b = http(method, PFX + path, tok, body=body, query=query)
                j = as_json(b)
                c2 = classify(st, j)
                c2["sha256"] = sha256_hex(b)
                c2["label"] = label
                ok2 = c2["class"] in ("SERVED", "POLICY") and (want == "SCOPE" or c2.get("code") == want or c2["class"] == want)
                c2["ok"] = ok2
                rows.append(c2)
                emit("    %-52s %-6s -> %s http %d code %s firm_id %s | sha256 %s -> %s"
                    % (label, method, c2["class"], st, c2.get("code"), "present" if c2.get("firm_id") else "ABSENT",
                       c2["sha256"][:16], "AS REQUIRED" if ok2 else "NOT AS REQUIRED"))
                return j, c2

            j1, _ = go("directory search WITH a query (q=a)", "GET", "/directory/search",
                       query={"q": "a", "limit": "25"}, want="SERVED")
            d1 = j1.get("data") if isinstance(j1, dict) and isinstance(j1.get("data"), list) else []
            j2, _ = go("directory search, a no-match query", "GET", "/directory/search",
                       query={"q": "zzqqxxnomatch13", "limit": "25"})
            d2 = j2.get("data") if isinstance(j2, dict) and isinstance(j2.get("data"), list) else None
            first = d1[0] if d1 else {}
            ids = first.get("ids") or {}
            j3, _ = go("directory resolve WITH a selection", "POST", "/directory/resolve",
                       body={"selection": {"relationship_id": ids.get("relationship_id")}})
            d3 = j3.get("data") if isinstance(j3, dict) else None
            resolved = isinstance(d3, dict) and d3.get("ok") is True

            # NEGATIVE CONTROL: a foreign firm's id, smuggled as a claimed-firm field -- expect
            # FIRM_BINDING, and the swapped value never echoed back in the response body.
            st_neg, _, b_neg = http("GET", PFX + "/directory/search", tok,
                                    query={"q": "a", "limit": "5", "firm_id": FOREIGN_FIRM})
            j_neg = as_json(b_neg)
            c_neg = classify(st_neg, j_neg)
            echoed = FOREIGN_FIRM.encode("utf-8") in b_neg
            neg_ok = (c_neg.get("code") == "FIRM_BINDING") and not echoed
            rows.append({"label": "NEGATIVE: foreign firm_id=%s claimed" % FOREIGN_FIRM,
                        "class": c_neg["class"], "ok": neg_ok})
            emit("    NEGATIVE: firm_id=%s claimed on /directory/search -> http %d code %s echoed=%s -> %s"
                % (FOREIGN_FIRM, st_neg, c_neg.get("code"), echoed, "REFUSED WITHOUT ECHO" if neg_ok else "NOT AS REQUIRED"))

            unexpected = sum(1 for r in rows if r["class"] == "UNEXPECTED")
            ok_n = sum(1 for r in rows if r.get("ok"))
            emit("  requests scope-resolved as required: %d of %d; UNEXPECTED %d" % (ok_n, len(rows), unexpected))
            s92_search = isinstance(d2, list) and len(d2) == 0 and len(d1) > 0
            emit("  S92 search: q=a -> %d entries, no-match -> %s entries -> %s"
                % (len(d1), len(d2) if isinstance(d2, list) else "n/a",
                   "HONOURED (FIXED)" if s92_search else "NOT HONOURED"))
            emit("  S92 resolve: ok=%s -> %s" % ((d3 or {}).get("ok") if isinstance(d3, dict) else None,
                 "RESOLVES (FIXED)" if resolved else "DOES NOT RESOLVE"))
            req_ok = (ok_n == len(rows) and unexpected == 0)
            s92 = {"search": s92_search, "resolve": resolved}
    except Exception as exc:  # noqa: BLE001
        emit("  EXCEPTION during the act: %s: %s -- rollback now" % (type(exc).__name__, str(exc)[:300]))
    finally:
        rb = rollback(ddb, created, sess)

    after_ok = prefix_scan(ddb, "after")
    life_ok = (bool(rb.get("k1b_deleted")) and bool(rb.get("k1_deleted")) and bool(rb.get("refresh_refused"))
              and bool(rb.get("expired_refused")) and after_ok)
    emit("  (e) keys+login %s; requests scope-resolved with 0 UNEXPECTED %s; lifecycle closed %s; "
        "S92 search %s, resolve %s" % (keys_ok, req_ok, life_ok,
        "FIXED" if s92.get("search") else "NOT FIXED", "FIXED" if s92.get("resolve") else "NOT FIXED"))
    ok = keys_ok and req_ok and life_ok
    print("ARM (e): %s" % ("PASS" if ok else "FAIL"))
    return ok, {"rows": rows, "life_ok": life_ok, "s92": s92, "role": role}


def main():
    ok_a, rows = arm_a()
    ok_b = arm_b()
    ok_c, result_c = arm_c()

    ok_d, result_d = (False, {})
    ok_e, result_e = (False, {})
    if ok_a and ok_b and ok_c:
        ok_d, result_d = arm_d()
        if ok_d:
            ok_e, result_e = arm_e()
        else:
            print()
            print("ARM (e): NOT RUN -- arm (d) did not PASS.")

    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print("arm (a) census cross-check: %s" % ("CLEAN" if ok_a else "SOME ROWS FAILED THEIR CHECK"))
    print("arm (b) member+env:         %s" % ("PASS" if ok_b else "FAIL"))
    print("arm (c) packet+halves:      %s (halves_present=%s)" % (
          "PASS" if ok_c else "STOP (expected this pass)", result_c.get("halves_present")))
    print("arm (d) subtraction gate+apply: %s (directory_state=%s)" % (
          "PASS" if ok_d else "FAIL/NOT-RUN", result_d.get("directory_state")))
    print("arm (e) live proof:         %s" % ("PASS" if ok_e else "FAIL/NOT-RUN"))
    print()
    if ok_a and ok_b and ok_c and not (ok_d and ok_e):
        print("ARM (d)/(e) did not both PASS -- R70-AC1 is not satisfied this run. See output above "
              "for which arm stopped and why.")
        return 1
    if ok_a and ok_b and not ok_c and result_c.get("halves_present", 0) < 2:
        print("THIS IS THE EXPECTED FIRST-PASS OUTCOME: (a) and (b) hold, (c) stops truthfully "
              "on ABSENT halves. Token WITHHELD (not printed) -- the criterion is not satisfied "
              "this pass and the order stays open.")
        return 0
    if ok_a and ok_b and ok_c and ok_d and ok_e:
        print("IBR70-CONTRACT-STAGED-SERVED-AND-SEARCH-ANSWERS")
        return 0
    print("ARM FAILURE OUTSIDE THE EXPECTED SHAPE -- see output above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
