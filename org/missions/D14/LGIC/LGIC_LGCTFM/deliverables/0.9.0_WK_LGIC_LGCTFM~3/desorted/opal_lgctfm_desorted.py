#!/usr/bin/env python3
"""opal_lgctfm.py -- the LGIC legacy-transform engine (LGIC_LGCTFM).

Round 1, cell LT-e-1 (this worker: 0.9.0_WK_LGIC_LGCTFM~1) implemented `walk` -- the CURRENT half of
one run's contract (org/standards/LGCTFM_CONTRACT.schema.json, authored from infra/logic/11_LGCTFM_
CONTRACT_SCHEMA_RECORD.md). Round 1, cell LT-e-2 (same slot) adds the DESIRED half to every walk row
(DEC-4: `lib/opal_naming.py` `grade(name, node_type)`, the call verbatim, never typed) and a second
verb, `forks`, that walks a SEEDED set of storage locations and finds FORK rows -- two current rows
whose DESIRED form is one string (DEC-5) -- from the desired TWIN, never from name patterns. TENSION
rows and the PLAN are later cells (LT-e-3, LT-p-1).

THE WALK ORDER (DEC-3, PRD LGIC_LGCTFM_PRD.md DEC-2/DEC-3/DEC-14; infra/logic/06_CONFORMANCE_
LEDGER.md is read for context but the buckets themselves are the caller's --seed arguments, not
re-derived): the subject's buckets -> every AWS-plane node that names them (comp-find --corpus aws,
read-only) -> every EventBridge rule / Scheduler schedule that names them (comp-trigger, read-only,
BOTH APIs) -> the Terraform files declaring any of them -> the registries that mark them (scopes.json,
remediations.json, LEGACY_SERVED_PATHS.json) -> `lib/opal_naming.py grade()` for the desired half.
`pipescript` is never called. Every field on every row is a CELL: {value, status, evidence:
{instrument, blind_spot, ...}}. A resource no instrument here can see is planted deliberately and
returned as an UNMEASURED row, never silently dropped.

THE DESIRED HALF (LT-e-2, DEC-4): `grade(name, node_type)` is the one builder this engine calls for
every RESOURCE/PLANE row -- it is the single BUILDER_FNS member that takes just (name, type), the two
fields the walk already carries on every row, and its own grammar (R/S/L/B/K) already covers every
node_type this walk emits. It returns (verdict, canonical_form); `desired.form` is that return value,
stringified (never hand-typed, never re-typed by a seat) so a checker's own re-call of grade() with the
SAME (name, type) reproduces it byte-for-byte via `str(got) == str(form)`. A raising call is a RAISE
row: `desired.verdict = RAISE`, `desired.missing_registry_row` names the registry the raise's own text
implicates (Rule 30). This round's `walk` plants one resource whose system token resolves to no
systems.json row, so a RAISE row exists on demand (E2R1-AC4), beside LT-e-1's own plant (which stays,
unedited, still UNMEASURED on `current`).

THE FORK TEST (LT-e-2, DEC-5, `forks` verb): seeded with real storage locations (bucket + prefix) that
hold the FORK_CONTROLS.json positives -- never the pairs themselves, which this engine never reads as
data. Candidate PLANE rows (kind PLANE, node_type S3Key, one row per tier-plane prefix or per dual-write
FORMAT under one prefix) are grouped into FORK rows by THREE independent, general mechanisms, none of
them a name-pattern match on the FORK_CONTROLS members: (1) an IDENTICAL desired twin -- two rows whose
grade()-computed canonical form is the same string; (2) a `_legacy`-suffixed tier is not a valid tier
(grade() raises K3 on it, by design -- infra/logic/06_CONFORMANCE_LEDGER.md itself says so, e.g. row
"a `_legacy` suffix is not a tier") -- stripping that one suffix and re-grading is the SAME desired-twin
test, applied to the row whose own grade() call could not otherwise place it; (3) shared REGISTRY MARK
membership -- two prefixes both inside the SAME `infra/logic/registry/remediations.json` remediation
project's `surfaces` list are, by that registry's own declaration, one canonical identity split across
two current spellings, cross-bucket alias resolution folded in via `scopes.json`'s `masters` list (a
scope's registered master account ids are interchangeable in a key's identity for this purpose, and a
leading `canonical/` segment names "this bucket's own copy" rather than a distinguishing identity
segment). `canonical_member` follows DEC-5's stated order: the CONFORMANT member if exactly one is; else
the member `infra/logic/06_CONFORMANCE_LEDGER.md` itself does not dispose RETIRE, if exactly one carries
that disposition and the group has exactly two members; else `RULING-OWED`.

Standard library only, plus `lib/opal_naming.py` (same estate, same rule) and a read-only shell-out to
`.tools/aws` (routed through `.tools/msys_argv_guard.py`'s `msys_safe_run`, per CLAUDE.md: never a bare
MSYS-path-mangling-prone spawn) for the `forks` verb's live S3 listings -- `comp-find --corpus aws`'s
own S3Key band is derived from portal source references only (measured this round: it does not reach
several real, live prefixes the ledger and a direct listing both confirm), so a direct, bounded,
read-only `s3api list-objects-v2` call is this cell's own coverage-hole fix, named as such below.

ASCII only. LF endings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

# DESORTED (LGIC_LGCTFM.TO-LT-d-1-r1, negative arm): this copy lives under deliverables/<serial>/desorted/,
# not lib/, so the real engine's two-dirname REPO derivation (correct only when the file sits directly in
# lib/) would land inside deliverables/. Walk up for the real repo root (the directory carrying both
# .tools/ and lib/, the estate's own markers) instead of hardcoding a depth -- the only change here besides
# the one removed sort below.
def _find_repo_root(start):
    d = start
    for _ in range(20):
        if os.path.isdir(os.path.join(d, ".tools")) and os.path.isdir(os.path.join(d, "lib")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return start


REPO = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(REPO, ".tools")

sys.path.insert(0, os.path.join(REPO, "lib"))  # the real lib/ -- opal_naming, read-only, never copied here
import opal_naming  # noqa: E402  -- DEC-4's one builder source (grade/name/address/lookup/fence_patterns)

COMP_FIND = os.path.join(REPO, ".tools", "comp-find")
COMP_TRIGGER = os.path.join(REPO, "org", "modules", "graph", "comp_trigger.py")
AWS_SHIM = os.path.join(TOOLS_DIR, "aws")
LEDGER = os.path.join(REPO, "infra", "logic", "06_CONFORMANCE_LEDGER.md")
SCOPES_REGISTRY = os.path.join(REPO, "infra", "logic", "registry", "scopes.json")
REMEDIATIONS_REGISTRY = os.path.join(REPO, "infra", "logic", "registry", "remediations.json")
LEGACY_SERVED_PATHS = os.path.join(REPO, "org", "missions", "D14", "LGIC", "LGIC_NAMING",
                                    "deliverables", "LEGACY_SERVED_PATHS.json")
TF_ROOT = os.path.join(REPO, "infra", "aws")

CELL_STATUSES = ("MEASURED", "UNMEASURED", "INFERRED", "NOT_MEASURABLE")
# BUILDER_FNS: check_lt_r1.py's own set (11_LGCTFM_CONTRACT_SCHEMA_RECORD.md s.3.1); this engine calls
# only "grade" (see module docstring), the others stay legal for a later cell/round to use.
BUILDER_FNS = ("name", "address", "grade", "lookup", "fence_patterns")


# ============================================================================ plumbing
def ab(path):
    return path if os.path.isabs(path) else os.path.join(REPO, path)


def run(argv, cwd=None, timeout=180):
    """A read-only subprocess call. Never raises; a failure is reported, never a crash (DEC-13:
    nothing live moves -- every tool this engine shells out to is a read instrument)."""
    try:
        r = subprocess.run(argv, capture_output=True, text=True, cwd=cwd or REPO, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ds: %s" % (timeout, " ".join(argv))
    except OSError as exc:
        return 127, "did not run: %s" % exc


def log(msg):
    print("WALK: " + msg, file=sys.stderr)


def cell(value, status, instrument, blind_spot, locator=None, vintage=None, denominator=None):
    if status not in CELL_STATUSES:
        raise ValueError("bad cell status: %r" % status)
    ev = {"instrument": instrument, "blind_spot": blind_spot}
    if locator is not None:
        ev["locator"] = locator
    if vintage is not None:
        ev["vintage"] = vintage
    if denominator is not None:
        ev["denominator"] = denominator
    return {"value": value, "status": status, "evidence": ev}


def read_json(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def read_text(path):
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def git_head():
    rc, out = run(["git", "rev-parse", "HEAD"])
    return out.strip() if rc == 0 else "UNKNOWN"


# ============================================================================ instrument: lib/opal_naming.py grade() (LT-e-2, DEC-4)
def missing_registry_row_text(exc):
    """A short, honest name for the registry row Rule 30 says is missing, read from the raise's own
    text (never guessed): grade()/its grammar functions raise RaiseDefect with a step code and a
    message that already names what has no row (module docstring: 'names the registry the raise's own
    text implicates')."""
    msg = str(exc)
    low = msg.lower()
    if "vocabulary" in low or re.search(r"\bR1\.", msg) or "systems.json" in low:
        home = "systems.json"
    elif "scope" in low or "scopes.json" in low:
        home = "scopes.json"
    elif "tier" in low:
        home = "NAMING_SCHEMA.json key.tier"
    else:
        home = "the naming registry"
    return "%s: %s" % (home, msg[:180])


def desired_cells(name, node_type):
    """The DESIRED half for one row: calls opal_naming.grade(name, node_type) -- the one builder call
    this engine records (module docstring) -- and returns (desired_dict, verdict_or_None,
    canonical_or_None, raised_exc_or_None). `form` is the call's own return value, stringified, so a
    checker's independent re-call reproduces it via str(got) == str(form) (never typed as a bare
    canonical string, which a 2-tuple-returning builder cannot satisfy by direct equality)."""
    builder = {"fn": "grade", "args": [name, node_type], "kwargs": {}}
    try:
        verdict_val, canon = opal_naming.grade(name, node_type)
        raised = None
    except Exception as exc:  # noqa: BLE001 -- any raise from the builder is a RAISE row, uniformly
        verdict_val, canon, raised = None, None, exc
    if raised is not None:
        d = {
            "form": cell(None, "MEASURED", "lib/opal_naming.py grade()",
                         "a raising builder produces no canonical form to report"),
            "builder": cell(builder, "MEASURED", "the call, verbatim", "none declared"),
            "verdict": cell("RAISE", "MEASURED", "lib/opal_naming.py grade()", "none declared"),
            "missing_registry_row": cell(missing_registry_row_text(raised), "MEASURED",
                                          "the refusal text, verbatim", "none declared"),
        }
    else:
        d = {
            "form": cell(str((verdict_val, canon)), "MEASURED", "lib/opal_naming.py grade()",
                         "form is the builder call's own return value, stringified -- never hand-typed"),
            "builder": cell(builder, "MEASURED", "the call, verbatim", "none declared"),
            "verdict": cell(verdict_val, "MEASURED", "lib/opal_naming.py grade()", "none declared"),
        }
    return d, verdict_val, canon, raised


# ============================================================================ instrument: .tools/aws (read-only S3 listing, `forks` verb)
def _git_bash():
    """The engine's own docstring is 'standard library only', so this does NOT import
    .tools/git_bash_resolver.py or .tools/msys_argv_guard.py (an e1-stdlib mechanical check refuses a
    top-level import outside stdlib/lib/) -- it re-derives the SAME two facts those modules encode
    (CLAUDE.md: never bare 'bash', that resolves to the System32 WSL stub; route an MSYS-adjacent spawn
    through `bash -c` with each argv element shell-quoted) using only `os`/`shutil`/`shlex`, both stdlib."""
    import shutil
    for c in (r"C:\Program Files\Git\usr\bin\bash.exe", r"C:\Program Files\Git\bin\bash.exe",
              r"C:\Program Files (x86)\Git\usr\bin\bash.exe"):
        if os.path.isfile(c):
            return c
    git = shutil.which("git")
    if git:
        base = os.path.dirname(os.path.dirname(os.path.abspath(git)))
        for rel in ("usr/bin/bash.exe", "bin/bash.exe"):
            b = os.path.join(base, *rel.split("/"))
            if os.path.isfile(b):
                return b
    return None


def aws_json(argv, timeout=60):
    """A read-only `.tools/aws <argv>` call, routed through `bash -c` with shlex-quoted args (the same
    MSYS-path-mangling guard `.tools/msys_argv_guard.py` provides, re-derived stdlib-only -- see
    _git_bash()'s docstring). Returns (parsed_json_or_None, raw_text); a `null` or empty AWS response is
    a MEASURED-empty, not a crash; a transport failure (rc!=0, timeout, no bash) is reported in raw_text
    and returns (None, raw_text), never raises."""
    import shlex
    bash = _git_bash()
    if not bash:
        return None, "no Git Bash found (refusing to fall back to bare 'bash')"
    shell_cmd = " ".join(shlex.quote(str(c)) for c in [AWS_SHIM] + list(argv))
    try:
        r = subprocess.run([bash, "-c", shell_cmd], capture_output=True, text=True, timeout=timeout)
    except Exception as exc:  # noqa: BLE001 -- a read-only probe never crashes the walk
        return None, "did not run: %s" % exc
    if r.returncode != 0:
        return None, "aws rc=%d: %s" % (r.returncode, ((r.stdout or "") + (r.stderr or ""))[:300])
    txt = (r.stdout or "").strip()
    if not txt or txt == "null":
        return None, txt or "null"
    try:
        return json.loads(txt), txt
    except ValueError:
        return None, txt[:300]


def list_common_prefixes(bucket, prefix, timeout=60):
    """One level of S3 'directories' under bucket/prefix (delimiter='/'), read-only, bounded. [] on any
    failure or on a leaf prefix with no child prefixes (both MEASURED-empty, not distinguished further
    here -- the caller falls back to treating the seed itself as a leaf row either way)."""
    data, _raw = aws_json(["s3api", "list-objects-v2", "--bucket", bucket, "--prefix", prefix,
                            "--delimiter", "/", "--max-keys", "1000",
                            "--query", "CommonPrefixes[].Prefix"], timeout=timeout)
    return list(data) if isinstance(data, list) else []


def list_keys_sample(bucket, prefix, max_keys=200, timeout=60):
    """Up to max_keys object keys under bucket/prefix (no delimiter -- a bounded sample, not a full
    listing: this engine only needs the LEAF FILE EXTENSIONS present, never every object). [] on any
    failure or a genuinely empty prefix."""
    data, _raw = aws_json(["s3api", "list-objects-v2", "--bucket", bucket, "--prefix", prefix,
                            "--max-keys", str(max_keys), "--query", "Contents[].Key"], timeout=timeout)
    return list(data) if isinstance(data, list) else []


# ============================================================================ instrument: comp-find --corpus aws
_TYPE_RE = re.compile(r"^  \[([A-Za-z0-9_]+)\]\s*$")
_ENTRY_RE = re.compile(r"^    (.+?)  drift=(\S+) src=(\S+)\s*$")
_DENOM_RE = re.compile(r"DENOMINATOR:\s*(\d+) hit\(s\) across (\d+) aws node\(s\) scanned")
_VINTAGE_RE = re.compile(r"Built from the estate as of ([^.]+)\.")


def parse_aws_walk(text):
    """Parses comp-find --corpus aws's structured text (org/standards/... has no JSON mode for the
    aws corpus; the tool's own --help documents this exact shape). Each entry: node_type, name,
    drift, arn_or_path (the line after the header; blank for some types, e.g. S3Key)."""
    nodes = []
    cur_type = None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = _TYPE_RE.match(lines[i])
        if m:
            cur_type = m.group(1)
            i += 1
            continue
        m = _ENTRY_RE.match(lines[i])
        if m and cur_type:
            name, drift, src = m.group(1), m.group(2), m.group(3)
            arn_or_path = ""
            if i + 1 < len(lines):
                nxt = lines[i + 1]
                if not _TYPE_RE.match(nxt) and not _ENTRY_RE.match(nxt):
                    arn_or_path = nxt.strip()
            nodes.append({"node_type": cur_type, "name": name, "drift": drift, "src": src,
                          "arn_or_path": arn_or_path or name})
            i += 1
            continue
        i += 1
    denom = _DENOM_RE.search(text)
    vint = _VINTAGE_RE.search(text)
    return nodes, {
        "hits": int(denom.group(1)) if denom else None,
        "scanned": int(denom.group(2)) if denom else None,
        "vintage": vint.group(1).strip() if vint else None,
    }


def run_aws_walk(seeds, budget=90):
    pattern = r"\b(?:" + "|".join(re.escape(s) for s in seeds) + r")\b"
    argv = [sys.executable, COMP_FIND, "--corpus", "aws", pattern, "--all", "--budget", str(budget)]
    rc, out = run(argv, timeout=budget + 60)
    if rc != 0:
        log("comp-find --corpus aws rc=%d (treated as a MEASURED-zero pull, not a crash)" % rc)
        return [], {"hits": None, "scanned": None, "vintage": None, "rc": rc}
    nodes, meta = parse_aws_walk(out)
    meta["rc"] = rc
    log("comp-find --corpus aws: %d node(s) parsed, denominator hits=%s scanned=%s" %
        (len(nodes), meta.get("hits"), meta.get("scanned")))
    return nodes, meta


# ============================================================================ instrument: comp-trigger
def run_trigger_census(budget=60):
    argv = [sys.executable, COMP_TRIGGER, "--list", "--json", "--budget", str(budget)]
    rc, out = run(argv, timeout=budget + 60)
    if rc != 0:
        log("comp-trigger --list --json rc=%d" % rc)
        return None, {"rc": rc}
    i = out.find("{")
    if i < 0:
        log("comp-trigger --list --json produced no JSON body")
        return None, {"rc": rc}
    try:
        data = json.loads(out[i:])
    except ValueError as exc:
        log("comp-trigger --list --json did not parse: %s" % exc)
        return None, {"rc": rc}
    log("comp-trigger --list --json: denominator=%s, %d trigger(s) census'd" %
        (data.get("denominator"), len(data.get("triggers") or [])))
    return data, {"rc": rc}


def shortcode_for(bucket):
    """opal-data-bd -> bd, opal-data-inf -> inf, opal-data-cot -> cot: a purely mechanical strip
    of the estate's own bucket-name grammar (NAMING_SCHEMA.json bucket = opal-data-{long}), never
    read from a fixture. A bucket that does not carry this prefix yields itself, unmatched."""
    prefix = "opal-data-"
    return bucket[len(prefix):] if bucket.startswith(prefix) else bucket


def trigger_relevant(t, buckets_lower, codes):
    """True if this census entry (from comp-trigger's own JSON) names the subject: its EventPattern
    text carries a full bucket name, or its own name carries a firm shortcode as a whole token
    (word-boundary: '-bd-', 'bd-', '-bd', never a bare substring). This is the DEC-3 relevance test;
    a trigger with neither is left out of the walk's rows, which is exactly the coverage hole this
    row's blind_spot names."""
    name_l = (t.get("name") or "").lower()
    pat_l = (t.get("pattern") or "").lower()
    if any(b in pat_l for b in buckets_lower):
        return True, "pattern names the bucket"
    for c in codes:
        if re.search(r"(^|[-_])" + re.escape(c) + r"([-_]|$)", name_l):
            return True, "name carries the firm shortcode %r" % c
    return False, ""


# ============================================================================ instrument: terraform tree (declaration)
def load_tf_corpus():
    corpus = {}
    if not os.path.isdir(TF_ROOT):
        return corpus
    for root, dirs, files in os.walk(TF_ROOT):
        if ".terraform" in root.replace("\\", "/").split("/"):
            dirs[:] = []
            continue
        for f in files:
            if not f.endswith(".tf"):
                continue
            p = os.path.join(root, f)
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    corpus[os.path.relpath(p, REPO).replace("\\", "/")] = fh.read()
            except OSError:
                continue
    return corpus


def declared_in(name, tf_corpus, cap=3):
    if not name or len(name) < 3:
        return []
    hits = [p for p, text in tf_corpus.items() if name in text]
    return sorted(hits)[:cap]


# ============================================================================ instrument: the identity/served registries
def load_scopes_bucket_map():
    """bucket alias spelling -> routed(bool), from THIS ESTATE'S OWN identity registry (Rule 30's
    'one home'), never from the round's fixed-input control (which the walk must not read)."""
    doc = read_json(SCOPES_REGISTRY)
    out = {}
    for sc in (doc or {}).get("scopes", []):
        for a in sc.get("aliases", []) or []:
            if "bucket" in (a.get("planes") or []):
                out[a.get("spelling")] = bool(a.get("routed"))
    return out


def mark_for(name, scopes_bucket_map, remediations_text, served_paths_text):
    if name in scopes_bucket_map:
        return "scopes.json alias"
    if name and name in remediations_text:
        return "remediations.json surface"
    if name and name in served_paths_text:
        return "LEGACY_SERVED_PATHS.json path"
    return None


# ============================================================================ the walk
def build_row(row_id, node_type, subject_key, name, arn_or_path, current_extra, mark,
              desired=None, kind="RESOURCE"):
    current = {"name": current_extra["name"], "arn_or_path": current_extra["arn_or_path"],
               "drift_class": current_extra["drift_class"], "declaration": current_extra["declaration"],
               "live": current_extra["live"], "client_facing": current_extra["client_facing"]}
    return {"row_id": row_id, "kind": kind, "node_type": node_type, "subject": subject_key,
            "current": current, "desired": desired if desired is not None else {}, "mark": mark}


def cells_for_aws_node(node, tf_corpus, scopes_bucket_map):
    name = node["name"]
    name_c = cell(name, "MEASURED", "comp-find --corpus aws", "nodes absent from the graph build")
    arn_c = cell(node["arn_or_path"], "MEASURED", "comp-find --corpus aws",
                 "nodes absent from the graph build")
    drift_c = cell(node["drift"], "MEASURED", "comp-find --corpus aws",
                   "drift is read at the build vintage, not live at read time")
    decl = declared_in(name, tf_corpus)
    if decl:
        decl_c = cell(decl[0] if len(decl) == 1 else decl, "MEASURED", "terraform tree read (infra/aws/**/*.tf)",
                      "a resource declared outside infra/aws/terraform")
    else:
        decl_c = cell("ABSENT", "MEASURED", "terraform tree read (infra/aws/**/*.tf)",
                      "a resource declared outside infra/aws/terraform")
    if node["node_type"] == "S3_BUCKET":
        if node["drift"] == "LIVE-INCREMENTAL":
            live_c = cell(True, "MEASURED", "drift_class=LIVE-INCREMENTAL from comp-find --corpus aws",
                          "an incremental-pull touch is not a trading-day-frontier write timestamp")
        else:
            live_c = cell(None, "UNMEASURED", "drift_class from comp-find --corpus aws",
                          "this node's drift class carries no incremental-write signal; a real "
                          "LastModified sweep needs a direct S3 HeadObject pass, not run here")
        routed = scopes_bucket_map.get(name)
        if routed is not None:
            cf_c = cell(bool(routed), "MEASURED", "infra/logic/registry/scopes.json aliases[].routed",
                        "a bucket routed=false today may still be reachable through an unlisted alias")
        else:
            cf_c = cell(None, "UNMEASURED", "infra/logic/registry/scopes.json aliases[].routed",
                        "this name is not a registered bucket alias in scopes.json")
    elif node["node_type"] == "CLOUDFRONT_DISTRIBUTION":
        live_c = cell(None, "NOT_MEASURABLE", "LastModified against lib/trading_calendar.py frontier",
                      "a distribution has no write clock")
        cf_c = cell(True, "MEASURED", "structural: a CloudFront distribution IS the client-facing edge",
                    "none declared")
    else:
        live_c = cell(None, "NOT_MEASURABLE", "LastModified against lib/trading_calendar.py frontier",
                      "a %s has no write clock" % node["node_type"].lower())
        cf_c = cell(False, "MEASURED", "LEGACY_SERVED_PATHS.json + org/missions/D14/LGIC/LGIC_NAMING "
                    "paths (no reference to this name found)",
                    "a resource that indirectly feeds a served key is not traced through its "
                    "downstream writes by this pass")
    return {"name": name_c, "arn_or_path": arn_c, "drift_class": drift_c, "declaration": decl_c,
            "live": live_c, "client_facing": cf_c}


def cells_for_trigger(t, reason, tf_corpus):
    name = t["name"]
    api = "comp-trigger (list-rules)" if t["kind"] == "events-rule" else "comp-trigger (list-schedules)"
    name_c = cell(name, "MEASURED", api, "a rule in another region" if t["kind"] == "events-rule"
                  else "a schedule in another region")
    arn_c = cell(t.get("arn") or "", "MEASURED", api, "same instrument, same blind spot")
    decl = declared_in(name, tf_corpus)
    if decl:
        decl_c = cell(decl[0] if len(decl) == 1 else decl, "MEASURED", "terraform tree read (infra/aws/**/*.tf)",
                      "a resource declared outside infra/aws/terraform")
    else:
        decl_c = cell("ABSENT", "MEASURED", "terraform tree read (infra/aws/**/*.tf)",
                      "a resource declared outside infra/aws/terraform")
    drift_c = cell(None, "UNMEASURED", api,
                    "found by naming convention (%s) only; not cross-checked against comp-find "
                    "--corpus aws, so this row carries no drift_class" % reason)
    live_c = cell(None, "NOT_MEASURABLE", "LastModified against lib/trading_calendar.py frontier",
                  "a rule has no write clock" if t["kind"] == "events-rule" else "a schedule has no write clock")
    cf_c = cell(False, "MEASURED", "LEGACY_SERVED_PATHS.json + org/missions/D14/LGIC/LGIC_NAMING "
                "paths (no reference to this name found)",
                "a trigger that fires a job which writes a served key is not traced through to "
                "that key by this pass")
    return {"name": name_c, "arn_or_path": arn_c, "drift_class": drift_c, "declaration": decl_c,
            "live": live_c, "client_facing": cf_c}


def cmd_walk(args):
    seeds = args.seed
    subject_key = args.subject
    out_dir = ab(args.out)
    os.makedirs(out_dir, exist_ok=True)

    log("subject=%s seeds=%s" % (subject_key, seeds))
    ledger_text = read_text(LEDGER)
    ledger_hits = sum(ledger_text.count(s) for s in seeds)
    log("06_CONFORMANCE_LEDGER.md read: %d byte(s), %d seed-name occurrence(s) (context only; "
        "the walk's buckets come from --seed, not re-derived from the ledger)" %
        (len(ledger_text), ledger_hits))

    aws_nodes, aws_meta = run_aws_walk(seeds)
    trigger_data, trigger_meta = run_trigger_census()
    tf_corpus = load_tf_corpus()
    log("terraform tree preloaded: %d file(s) under infra/aws" % len(tf_corpus))
    scopes_bucket_map = load_scopes_bucket_map()
    remediations_text = read_text(REMEDIATIONS_REGISTRY)
    served_paths_text = read_text(LEGACY_SERVED_PATHS)

    rows = []
    seen = {}  # (node_type, name) -> row_id
    n = 0

    def add_row(node_type, name, current_cells, mark):
        nonlocal n
        key = (node_type, name)
        if key in seen:
            return
        n += 1
        row_id = "R-%04d" % n
        desired, _v, _c, _r = desired_cells(name, node_type)  # LT-e-2, DEC-4: the desired half
        rows.append(build_row(row_id, node_type, subject_key, name, name, current_cells, mark, desired))
        seen[key] = row_id

    for node in aws_nodes:
        cc = cells_for_aws_node(node, tf_corpus, scopes_bucket_map)
        mk = mark_for(node["name"], scopes_bucket_map, remediations_text, served_paths_text)
        add_row(node["node_type"], node["name"], cc, mk)

    buckets_lower = [s.lower() for s in seeds]
    codes = sorted({shortcode_for(s) for s in seeds}, key=len, reverse=True)
    triggers = (trigger_data or {}).get("triggers") or []
    list_rules_n = list_schedules_n = 0
    for t in triggers:
        ok, reason = trigger_relevant(t, buckets_lower, codes)
        if not ok:
            continue
        if t["kind"] == "events-rule":
            list_rules_n += 1
        else:
            list_schedules_n += 1
        node_type = "EVENT_RULE" if t["kind"] == "events-rule" else "SCHEDULE"
        cc = cells_for_trigger(t, reason, tf_corpus)
        mk = mark_for(t["name"], scopes_bucket_map, remediations_text, served_paths_text)
        add_row(node_type, t["name"], cc, mk)

    log("trigger relevance: list_rules=%d list_schedules=%d (both APIs, DEC-3)" %
        (list_rules_n, list_schedules_n))

    # the plant (WORKER FACE E1R1): a resource genuinely outside BOTH instruments' scope.
    # comp-trigger's own --list text says so itself: "S3 bucket notifications NOT scanned (v1
    # scope, by design)"; comp-find --corpus aws only ever surfaces a bucket notification as an
    # unlabeled property INSIDE the S3_BUCKET node's own props (event_notifications/notify_sns/
    # notify_sqs), never as a standalone node with its own name. So a bucket-notification target
    # has no row-producing instrument in this walk -- a fictional one, clearly marked planted.
    plant_name = "opal-data-bd-s3-notify-planted-test-queue"
    plant_why = ("An S3 Bucket Notification target is explicitly out of comp-trigger's scanned "
                 "scope (the tool's own --list output: 'S3 bucket notifications NOT scanned (v1 "
                 "scope, by design)') and comp-find --corpus aws only surfaces a bucket's "
                 "notification config as an unlabeled JSON field inside the S3_BUCKET node's own "
                 "props (event_notifications/notify_sns/notify_sqs per comp_trigger.py's own help "
                 "text), never as its own node with this name. Neither instrument this walk calls "
                 "can produce a row for a notification TARGET by name, so this is a planted, "
                 "fictional resource -- it is not claimed to exist in AWS.")
    plant_cells = {
        "name": cell(plant_name, "UNMEASURED", "comp-find --corpus aws + comp-trigger (neither reaches it)",
                     "an S3 bucket-notification target has no row-producing instrument in this walk"),
        "arn_or_path": cell(None, "UNMEASURED", "comp-find --corpus aws + comp-trigger (neither reaches it)",
                            "same coverage hole as current.name"),
        "drift_class": cell(None, "UNMEASURED", "comp-find --corpus aws + comp-trigger (neither reaches it)",
                            "same coverage hole as current.name"),
        "declaration": cell(None, "UNMEASURED", "terraform tree read (infra/aws/**/*.tf)",
                            "a planted name absent from Terraform by construction"),
        "live": cell(None, "UNMEASURED", "comp-find --corpus aws + comp-trigger (neither reaches it)",
                     "same coverage hole as current.name"),
        "client_facing": cell(None, "UNMEASURED", "comp-find --corpus aws + comp-trigger (neither reaches it)",
                              "same coverage hole as current.name"),
    }
    n += 1
    plant_row_id = "R-%04d" % n
    plant_desired, _v, _c, _r = desired_cells(plant_name, "SQS_QUEUE")
    rows.append(build_row(plant_row_id, "SQS_QUEUE", subject_key, plant_name, plant_name, plant_cells, None,
                           plant_desired))

    # a SECOND plant (LT-e-2, E2R1-AC4): a resource whose system token resolves to no systems.json row,
    # so grade() RAISES and this run carries a genuine RAISE row naming the missing registry row (Rule
    # 30), on demand, never left to chance on whatever real names this round's live pull happens to hit.
    # Its CURRENT half is UNMEASURED by the same construction as the LT-e-1 plant above (fictional, not
    # claimed to exist in AWS); unlike that plant, its DESIRED half is the point of planting it.
    # why: a resource name whose leading token resolves to no systems.json row (R1.f: "in no
    # vocabulary; no registry row resolves it") so this run carries a deliberate, on-demand RAISE row
    # (E2R1-AC4) rather than depending on whichever real names this round's live pull happens to raise on.
    raise_plant_name = "planted-system-without-a-row-49financial-ingest-role"
    raise_plant_cells = {
        "name": cell(raise_plant_name, "UNMEASURED", "planted (no instrument reaches a fictional name)",
                     "this resource is not claimed to exist in AWS"),
        "arn_or_path": cell(None, "UNMEASURED", "planted", "same as current.name"),
        "drift_class": cell(None, "UNMEASURED", "planted", "same as current.name"),
        "declaration": cell(None, "UNMEASURED", "terraform tree read (infra/aws/**/*.tf)",
                            "a planted name absent from Terraform by construction"),
        "live": cell(None, "UNMEASURED", "planted", "same as current.name"),
        "client_facing": cell(False, "MEASURED", "planted: an IAM_ROLE is never client-facing",
                              "none declared"),
    }
    n += 1
    raise_plant_row_id = "R-%04d" % n
    raise_plant_desired, _v, _c, raised_exc = desired_cells(raise_plant_name, "IAM_ROLE")
    if raised_exc is None:
        log("WARNING: the E2R1-AC4 plant did not raise (%r) -- grade() or the registry moved" %
            raise_plant_name)
    rows.append(build_row(raise_plant_row_id, "IAM_ROLE", subject_key, raise_plant_name, raise_plant_name,
                           raise_plant_cells, None, raise_plant_desired))

    subject_obj = {
        "kind": "scope",
        "key": subject_key,
        "vintage": {
            "repo_head": git_head(),
            "graph_built": aws_meta.get("vintage") or "UNKNOWN",
            "registry_hash": "scopes.json sha256:" + hashlib.sha256(
                read_text(SCOPES_REGISTRY).encode("utf-8")).hexdigest()[:16],
        },
    }

    contract = {
        "schema_version": "1.0",
        "subject": subject_obj,
        "trigger_denominator": {
            "list_rules": cell(list_rules_n, "MEASURED", "comp-trigger (list-rules)",
                               "a rule whose pattern names no bucket is found only through its target",
                               vintage=None, denominator="%s of %s events-rule(s) census'd" %
                               (list_rules_n, (trigger_data or {}).get("denominator", {}).get("rules"))),
            "list_schedules": cell(list_schedules_n, "MEASURED", "comp-trigger (list-schedules)",
                                   "a schedule names no bucket; its Lambda does",
                                   vintage=None, denominator="%s of %s scheduler(s) census'd" %
                                   (list_schedules_n, (trigger_data or {}).get("denominator", {}).get("schedules"))),
        },
        "ranking_rule": "order by irreversible, then client_facing, then live, then rules_colliding; "
                        "object_count as tiebreak (08_TENSION_MAP.md s.0)",
        "rows": rows,
        "edges": [],
        "tensions": [],
        "plan": [],
    }

    with open(os.path.join(out_dir, "contract.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(contract, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(out_dir, "PLANT.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"name": plant_name, "why_outside_every_instrument": plant_why}, fh, indent=1, sort_keys=True)
        fh.write("\n")

    log("wrote %d row(s) (incl. 1 planted) to %s" % (len(rows), out_dir))
    return 0


# ============================================================================ the forks run (LT-e-2, DEC-5)
def _registered_masters():
    """Every scope's registered `masters` (account/entity ids the scope's own registry row names as
    interchangeable identifiers for it -- scopes.json, read the same way load_scopes_bucket_map() already
    reads it). {master_id: scope_long}."""
    doc = read_json(SCOPES_REGISTRY)
    out = {}
    for sc in (doc or {}).get("scopes", []):
        for m in sc.get("masters") or []:
            out[str(m)] = sc.get("long")
    return out


def _remediation_surfaces():
    """[(project, bucket, prefix)] for every kind='s3-prefix' surface in remediations.json -- the SAME
    registry `mark_for` already reads, at row grain instead of membership-text grain."""
    doc = read_json(REMEDIATIONS_REGISTRY)
    out = []
    for r in (doc or {}).get("remediations") or []:
        proj = r.get("project")
        for s in r.get("surfaces") or []:
            if s.get("kind") == "s3-prefix" and s.get("bucket") and s.get("prefix"):
                out.append((proj, s["bucket"], s["prefix"]))
    return out


def mark_project_for(bucket, key, surfaces):
    """The remediation project whose s3-prefix surface covers (bucket, key) -- prefix-overlap either
    direction, since a seed's own prefix can be shallower OR deeper than the registered surface."""
    kk = key if key.endswith("/") else key + "/"
    for proj, sb, sp in surfaces:
        if sb != bucket:
            continue
        spp = sp if sp.endswith("/") else sp + "/"
        if kk.startswith(spp) or spp.startswith(kk):
            return proj
    return None


_TIER_WORDS = ("bronze", "silver", "gold", "platinum", "code")


def twin_key(key, masters):
    """A GENERAL, registry-grounded normalization for the fork test's desired-twin grouping (module
    docstring mechanism 2 and 3's cross-bucket half): drop a structural `canonical` segment (names 'this
    bucket's own copy', not a distinguishing identity component); collapse a `_legacy`-suffixed tier back
    to its base tier (06_CONFORMANCE_LEDGER.md: '_legacy is not a tier' -- the suffixed and unsuffixed
    spellings are the SAME desired identity, which is exactly why grade() raises K3 on the suffixed one
    instead of placing it somewhere else); DROP a registered master id segment entirely (scopes.json
    `masters`: two master ids of the SAME scope are interchangeable identifiers for it, and the estate's
    own `canonical/` spellings carry no master-id segment at all -- so a master id is dropped, never kept
    as a placeholder, or the two spellings would never collapse to the same key). The bucket itself is
    deliberately never part of this key -- the whole point is to fold cross-bucket duplicates together."""
    segs = [s for s in key.split("/") if s]
    out = []
    for s in segs:
        if s == "canonical":
            continue
        if s.endswith("_legacy") and s[: -len("_legacy")] in _TIER_WORDS:
            out.append(s[: -len("_legacy")])
            continue
        if s in masters:
            continue
        out.append(s)
    return "/".join(out) + "/"


_LEDGER_ROW_RE = re.compile(r"`([^`]+)`[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\*\*([A-Z][A-Z /_-]*)")


def _ledger_dispositions():
    """[(path_text, disposition_word)] parsed from infra/logic/06_CONFORMANCE_LEDGER.md's own plane
    tables: a backtick-quoted path followed, later on the same table row, by the first BOLD word (the
    ledger's own disposition column -- CONFORMANT/MIGRATE/RETIRE/...). A repo-file instrument, read the
    same way LT-e-1 already reads this file 'for context'; never FORK_CONTROLS.json."""
    text = read_text(LEDGER)
    out = []
    for ln in text.splitlines():
        m = _LEDGER_ROW_RE.search(ln)
        if m:
            out.append((m.group(1).strip(), m.group(2).strip()))
    return out


def ledger_disposition_for(bucket, key, dispositions):
    """The ledger's own disposition word for (bucket, key), or None if no ledger row's path overlaps it.
    A row filed under section 1 (the monolith) is written without its bucket in the ledger's own path
    column, so both the bare key and bucket/key are tried."""
    kk = key if key.endswith("/") else key + "/"
    candidates = (kk, "%s/%s" % (bucket, kk))
    best = None
    for path_text, word in dispositions:
        pp = path_text if path_text.endswith("/") else path_text + "/"
        pp = pp.replace("{", "").replace("}", "")  # a ledger brace-group, e.g. {bronze,silver}
        for c in candidates:
            if c == pp or c.startswith(pp) or pp.startswith(c):
                if best is None:
                    best = word
    return best


def _seed_rows(bucket, prefix, mode, add_plane_row, masters, surfaces, dispositions):
    """One seed location -> one or more PLANE rows (module docstring: 'one row per tier-plane prefix or
    per dual-write FORMAT under one prefix'). Read-only S3 listing via list_common_prefixes/
    list_keys_sample (.tools/aws); never a full recursive listing (bounded, per call). `mode`: "" ->
    enumerate one level of child prefixes (a leaf seed with none falls back to itself); "format" ->
    stay AT this exact prefix and split by leaf file extension (a dual-write twin, DEC-5's own example);
    "leaf" -> stay AT this exact prefix as ONE row, never descend -- for a seed that is ALREADY the
    tier-plane identity a fork test compares (enumerating its children would compare TABLES, not the
    plane, and a registry MARK's surface is registered at exactly this grain)."""
    if mode == "format":
        keys = list_keys_sample(bucket, prefix, max_keys=500)
        exts = set()
        for k in keys:
            base = k.rsplit("/", 1)[-1]
            if "." in base:
                exts.add(base.rsplit(".", 1)[-1].lower())
        if not exts:
            exts = {"unknown"}
        for ext in sorted(exts):
            add_plane_row(bucket, prefix, "%s%s (%s)" % (bucket, "/" + prefix, ext),
                          "%d object(s) sampled carrying a .%s leaf" % (
                              sum(1 for k in keys if k.lower().endswith("." + ext)), ext))
        return

    if mode == "leaf":
        add_plane_row(bucket, prefix, "%s/%s" % (bucket, prefix),
                      "the seed prefix itself, by request (leaf mode: this IS the tier-plane grain)")
        return

    children = list_common_prefixes(bucket, prefix)
    if children:
        for child in children:
            add_plane_row(bucket, child, "%s/%s" % (bucket, child),
                          "one child prefix under the seed %r (delimiter listing)" % prefix)
    else:
        add_plane_row(bucket, prefix, "%s/%s" % (bucket, prefix),
                      "the seed prefix itself (no child prefixes under it)")


def cmd_forks(args):
    subject_key = args.subject
    out_dir = ab(args.out)
    os.makedirs(out_dir, exist_ok=True)

    seeds = []
    for raw in args.seed_loc:
        parts = raw.split(":", 2)
        bucket, prefix = parts[0], parts[1]
        mode = parts[2] if len(parts) > 2 else ""
        seeds.append({"bucket": bucket, "prefix": prefix, "mode": mode or "enumerate"})
    with open(os.path.join(out_dir, "SEEDS.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"_about": "storage locations only -- never the FORK_CONTROLS.json pairs; the engine "
                              "discovers which locations twin each other (see module docstring)",
                   "seeds": seeds}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    log("forks: %d seed location(s)" % len(seeds))

    masters = _registered_masters()
    surfaces = _remediation_surfaces()
    dispositions = _ledger_dispositions()
    tf_corpus = load_tf_corpus()
    scopes_bucket_map = load_scopes_bucket_map()
    remediations_text = read_text(REMEDIATIONS_REGISTRY)
    served_paths_text = read_text(LEGACY_SERVED_PATHS)

    rows = []
    row_meta = {}  # row_id -> {"bucket", "key", "twin_key", "mark_project", "verdict"}
    seen_names = set()
    n = 0

    def add_plane_row(bucket, key, row_name, note):
        nonlocal n
        if row_name in seen_names:
            return
        seen_names.add(row_name)
        n += 1
        row_id = "R-%04d" % n
        arn = "s3://%s/%s" % (bucket, key)
        current = {
            "name": cell(row_name, "MEASURED", ".tools/aws s3api list-objects-v2 (read-only)", note),
            "arn_or_path": cell(arn, "MEASURED", ".tools/aws s3api list-objects-v2 (read-only)",
                                "a listing call is bounded (--max-keys/--delimiter); not a full recursive walk"),
            "drift_class": cell("LIVE-no-DECLARED", "INFERRED", "a live S3 listing implies the prefix is live",
                                "declaration is checked separately below; this cell does not cross-check it"),
            "declaration": (cell(declared_in(key, tf_corpus)[0] if declared_in(key, tf_corpus) else "ABSENT",
                                 "MEASURED", "terraform tree read (infra/aws/**/*.tf)",
                                 "a resource declared outside infra/aws/terraform")),
            "live": cell(True, "MEASURED", ".tools/aws s3api list-objects-v2 (read-only, this run)",
                        "a listing at run time is not a trading-day-frontier LastModified sweep"),
            "client_facing": cell(bucket in scopes_bucket_map or key in served_paths_text, "INFERRED",
                                  "infra/logic/registry/scopes.json + LEGACY_SERVED_PATHS.json membership",
                                  "a prefix can be served without either registry naming it by this exact string"),
        }
        mk = mark_for(row_name, scopes_bucket_map, remediations_text, served_paths_text) or \
            mark_project_for(bucket, key, surfaces)
        desired, verdict_val, _canon, _raised = desired_cells(key, "S3Key")
        rows.append(build_row(row_id, "S3Key", subject_key, row_name, arn, current, mk, desired, kind="PLANE"))
        row_meta[row_id] = {"bucket": bucket, "key": key, "twin_key": twin_key(key, masters),
                            "mark_project": mark_project_for(bucket, key, surfaces), "verdict": verdict_val}

    for s in seeds:
        mode = "" if s["mode"] == "enumerate" else s["mode"]
        _seed_rows(s["bucket"], s["prefix"], mode, add_plane_row, masters, surfaces, dispositions)

    # group candidates into FORK rows: mechanism (1)/(2) via twin_key, mechanism (3) via mark_project
    by_twin, by_mark = {}, {}
    for rid, meta in row_meta.items():
        by_twin.setdefault(meta["twin_key"], []).append(rid)
        if meta["mark_project"]:
            by_mark.setdefault(meta["mark_project"], []).append(rid)

    groups, seen_member_sets, edges = [], set(), []
    for _gk, members in list(by_twin.items()) + list(by_mark.items()):
        # DESORTED (LGIC_LGCTFM.TO-LT-d-1-r1, 0.9.0_WK_LGIC_LGCTFM~3 negative arm): the real engine's
        # `sorted(set(members))` is replaced with a bare `list(set(members))` -- the FORK row's own
        # "members" list order now depends on the process's string-hash order, which PYTHONHASHSEED
        # randomizes per process by default. This is the one deliberately removed sort under test.
        distinct = list(set(members))
        # a group is real only if it links >= 2 DIFFERENT ROWS (a dual-write format split shares one
        # (bucket, key) identity by construction, so identity distinctness is not the bar here -- row
        # identity already is, since `members` is built from a dict keyed by row_id)
        if len(distinct) < 2:
            continue
        fs = frozenset(distinct)
        if fs in seen_member_sets:
            continue
        seen_member_sets.add(fs)
        groups.append(distinct)

    fork_rows = []
    fn_ = 0
    for members in groups:
        fn_ += 1
        fork_id = "F-%04d" % fn_
        conformant = [m for m in members if row_meta[m]["verdict"] == "CONFORMANT"]
        if len(conformant) == 1:
            canon_val, canon_ev = conformant[0], "the one CONFORMANT member (grade() verdict, DEC-5 order step 1)"
        else:
            retiring = [m for m in members
                        if (ledger_disposition_for(row_meta[m]["bucket"], row_meta[m]["key"], dispositions) or "")
                        .startswith("RETIRE")]
            survivors = [m for m in members if m not in retiring]
            if len(members) == 2 and len(retiring) == 1 and len(survivors) == 1:
                canon_val = survivors[0]
                canon_ev = "the ledger's own disposition (infra/logic/06_CONFORMANCE_LEDGER.md): the " \
                           "other member is RETIRE (DEC-5 order step 2)"
            else:
                canon_val, canon_ev = "RULING-OWED", "no single CONFORMANT member and no single ledger " \
                                       "RETIRE disposition among the group (DEC-5 order step 3)"
        mechanism = "shared registry mark (infra/logic/registry/remediations.json surfaces, same project)" \
            if len({row_meta[m]["mark_project"] for m in members if row_meta[m]["mark_project"]}) == 1 and \
            any(row_meta[m]["mark_project"] for m in members) else \
            "identical desired twin (lib/opal_naming.py grade(), normalized per the module docstring)"
        fork_rows.append({
            "row_id": fork_id, "kind": "FORK", "subject": subject_key, "members": members,
            "one_job": cell("these rows are two current spellings of one desired storage identity",
                           "INFERRED", mechanism, "a false-positive group is possible if the registry "
                           "or the grammar mis-normalizes two genuinely different resources together"),
            "canonical_member": cell(canon_val, "INFERRED" if canon_val != "RULING-OWED" else "NOT_MEASURABLE",
                                     canon_ev, "none declared"),
        })
        if canon_val != "RULING-OWED":
            for m in members:
                if m != canon_val:
                    edges.append({"from": m, "to": canon_val, "type": "REPLACES"})

    log("forks: %d candidate row(s), %d FORK row(s) found" % (len(rows), len(fork_rows)))

    subject_obj = {
        "kind": "scope", "key": subject_key,
        "vintage": {
            "repo_head": git_head(),
            "graph_built": "UNKNOWN (this run reads .tools/aws s3api at call time, not the aws-graph build)",
            "registry_hash": "scopes.json sha256:" + hashlib.sha256(
                read_text(SCOPES_REGISTRY).encode("utf-8")).hexdigest()[:16],
        },
    }
    contract = {
        "schema_version": "1.0",
        "subject": subject_obj,
        "trigger_denominator": {
            "list_rules": cell(0, "NOT_MEASURABLE", "n/a -- the forks run does not walk triggers",
                               "see the walk run's own contract for the trigger denominator"),
            "list_schedules": cell(0, "NOT_MEASURABLE", "n/a -- the forks run does not walk triggers",
                                   "see the walk run's own contract for the trigger denominator"),
        },
        "ranking_rule": "order by irreversible, then client_facing, then live, then rules_colliding; "
                        "object_count as tiebreak (08_TENSION_MAP.md s.0)",
        "rows": rows + fork_rows,
        "edges": edges,
        "tensions": [],
        "plan": [],
    }
    with open(os.path.join(out_dir, "contract.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(contract, fh, indent=1, sort_keys=True)
        fh.write("\n")
    log("wrote %d candidate row(s) + %d FORK row(s) to %s" % (len(rows), len(fork_rows), out_dir))
    return 0


# ============================================================================ main
def main():
    ap = argparse.ArgumentParser(description="opal_lgctfm -- the LGIC legacy-transform engine")
    sub = ap.add_subparsers(dest="verb", required=True)

    p_walk = sub.add_parser("walk", help="walk one subject's current-state contract (LT-e-1/LT-e-2)")
    p_walk.add_argument("--subject", required=True, help="the registry key (scopes.json/systems.json)")
    p_walk.add_argument("--seed", action="append", required=True, help="a bucket/prefix to walk from")
    p_walk.add_argument("--out", required=True, help="output directory for contract.json + PLANT.json")

    p_forks = sub.add_parser("forks", help="find FORK rows from seeded storage locations (LT-e-2)")
    p_forks.add_argument("--subject", required=True, help="the registry key (scopes.json/systems.json)")
    p_forks.add_argument("--seed-loc", dest="seed_loc", action="append", required=True,
                          help="bucket:prefix[:format] -- a storage location, never a pair")
    p_forks.add_argument("--out", required=True, help="output directory for contract.json + SEEDS.json")

    args = ap.parse_args()
    if args.verb == "walk":
        return cmd_walk(args)
    if args.verb == "forks":
        return cmd_forks(args)
    ap.error("unknown verb: %s" % args.verb)
    return 2


if __name__ == "__main__":
    sys.exit(main())
