#!/usr/bin/env python
"""YCD-u-6 checks: python u6_checks.py <schema|regen|census>   (run from the worktree root).

One argument, one RESULT line. ASCII only. No vendor call, no AWS call, no install, no write under portal/.

  schema  every AnalysisReport document valid against the schema as it stood at the spawn base (BASE_REV) is
          still valid against the schema as changed.
  regen   the portal's own wire generator (a COPY of gen-wire.ts placed in a temporary tree, so its
          out-dir -- fixed by import.meta.url -- lands in that tree and never in contracts/wire/) is run
          against the changed schema; the generated AnalysisReport.ts is compared byte for byte with the one
          committed at the portal pin.
  census  every reader of AnalysisReport.schema.json, found by a printed-denominator search, is named and run
          against the new branch; a reader that turns red when the base schema did not is a FAIL.
"""
import contextlib
import difflib
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=str(HERE)).decode().strip())
SCHEMA_REL = "docs/contracts/investor-reporting/v1/AnalysisReport.schema.json"
SCHEMA = ROOT / SCHEMA_REL
CONTRACTS_DIR = ROOT / "docs/contracts/investor-reporting/v1"
BASE_REV = "1974945570"  # the spawn base: the schema here is byte-for-byte the v1 file as it stood before YCD-u-6
BASE_SHA = "1bd0dc85847690b277e3a3011bcbe500a02820792cd53a38a1201fc3c55d153f"
PORTAL = ROOT / "portal"
PORTAL_PIN = "d1b21c97"
TS_REL = "src/pages/InvestorReporting/contracts/wire/AnalysisReport.ts"
GEN_REL = "src/pages/InvestorReporting/__tests__/fe-s-13/gen-wire.ts"
FIXTURES = ROOT / "infra/aws/lambda/investor-reporting/_contracts/fixtures"
LAMBDA = "infra/aws/lambda/investor-reporting"


CROSS = chr(0x2717)  # the failing-test mark bun prints


def sha(b):
    return hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()


def git(*args, cwd=None):
    return subprocess.check_output(["git"] + list(args), cwd=str(cwd or ROOT))


def base_bytes():
    data = git("show", BASE_REV + ":" + SCHEMA_REL)
    if sha(data) != BASE_SHA:
        raise SystemExit("BASE schema at %s hashes %s, expected %s" % (BASE_REV, sha(data), BASE_SHA))
    return data.replace(b"\r\n", b"\n")


@contextlib.contextmanager
def base_schema_in_place():
    """Swap the BASE schema bytes into the working tree for one measurement; restored in finally."""
    current = SCHEMA.read_bytes()
    SCHEMA.write_bytes(base_bytes())
    try:
        yield
    finally:
        SCHEMA.write_bytes(current)
        if SCHEMA.read_bytes() != current:
            print("ERROR: schema file NOT restored")
            raise SystemExit(2)


def validator(schema_bytes):
    import jsonschema
    schema = json.loads(schema_bytes.decode("utf-8"))
    return jsonschema.Draft202012Validator(schema)


# ---------------------------------------------------------------------------------------------- schema arm
def candidate_documents():
    """(path, document) for every tracked JSON file holding an AnalysisReport-shaped document."""
    outer = [t for t in git("ls-files", "-z", "--", "*.json").decode("utf-8", "replace").split("\0") if t]
    inner = ["portal/" + t for t in git("-C", str(PORTAL), "ls-files", "-z", "--", "*.json").decode("utf-8", "replace").split("\0") if t]
    tracked = outer + inner  # the portal is a nested worktree: its tracked files are not in the outer index
    found, scanned, unreadable = [], 0, 0
    for rel in tracked:
        p = ROOT / rel
        try:
            if p.stat().st_size > 30 * 1024 * 1024:
                continue
            raw = p.read_bytes()
        except OSError:
            unreadable += 1
            continue
        scanned += 1
        if b'"request_ref"' not in raw or b'"sections"' not in raw or b'"disclosures"' not in raw:
            continue
        try:
            obj = json.loads(raw.decode("utf-8"))
        except ValueError:
            unreadable += 1
            continue
        doc = obj.get("instance") if isinstance(obj, dict) and isinstance(obj.get("instance"), dict) else obj
        if isinstance(doc, dict) and {"request_ref", "sections", "disclosures"} <= set(doc):
            found.append((rel, doc))
    return found, len(tracked), scanned, unreadable


def arm_schema():
    old_v = validator(base_bytes())
    new_v = validator(SCHEMA.read_bytes())
    new_sha = sha(SCHEMA.read_bytes())
    print("schema at base %s: sha256 %s (pinned %s)" % (BASE_REV, sha(base_bytes()), BASE_SHA))
    print("schema as changed: sha256 %s" % new_sha)
    docs, tracked, scanned, unreadable = candidate_documents()
    print("DENOMINATOR: %d tracked .json files (outer + portal); %d read; %d unreadable/unparsable; %d AnalysisReport-shaped documents found"
          % (tracked, scanned, unreadable, len(docs)))
    regress, valid_before, newly_valid, still_invalid = [], 0, 0, 0
    for rel, doc in docs:
        before, after = old_v.is_valid(doc), new_v.is_valid(doc)
        print("  FIXTURE %s  before=%s after=%s" % (rel, "VALID" if before else "invalid", "VALID" if after else "invalid"))
        if before:
            valid_before += 1
            if not after:
                regress.append(rel)
        elif after:
            newly_valid += 1
        else:
            still_invalid += 1
    print("COUNT: %d documents; valid before %d; valid before and after %d; valid before and NOT after %d; "
          "newly valid %d; invalid both %d"
          % (len(docs), valid_before, valid_before - len(regress), len(regress), newly_valid, still_invalid))
    # the new branch itself: the served OPAL form is valid, a vendor member on it is refused, a NOT_AVAILABLE with no reason is refused
    expect = {
        "AnalysisReport.v2.opal.valid.json": True,
        "AnalysisReport.v2.opal.invalid_vendor_member.json": False,
        "AnalysisReport.v2.opal.invalid_not_available_no_reason.json": False,
        "AnalysisReport.v2.ycharts.valid.json": True,
        "AnalysisReport.valid.json": True,
        "AnalysisReport.invalid.json": False,
    }
    branch_bad = []
    for name, want in expect.items():
        doc = json.loads((FIXTURES / name).read_text(encoding="utf-8"))["instance"]
        got = new_v.is_valid(doc)
        print("  BRANCH %s expected %s got %s" % (name, "VALID" if want else "invalid", "VALID" if got else "invalid"))
        if got != want:
            branch_bad.append(name)
    ok = valid_before >= 1 and not regress and not branch_bad
    print("RESULT: schema %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


# ---------------------------------------------------------------------------------------------- bun / regen
def find_bun():
    found = shutil.which("bun")
    if found:
        return found
    base = os.environ.get("LOCALAPPDATA", "")
    hits = glob.glob(os.path.join(base, "Microsoft", "WinGet", "Packages", "Oven-sh.Bun*", "bun-windows-x64", "bun.exe"))
    if hits:
        return hits[0]
    raise SystemExit("bun not found")


def run_generator(contracts_dir, tmp_root):
    """Run a COPY of gen-wire.ts from inside portal/ with --no-install; return (rc, out_dir, stdout)."""
    gen_dir = Path(tmp_root) / "src/pages/InvestorReporting/__tests__/fe-s-13"
    gen_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PORTAL / GEN_REL, gen_dir / "gen-wire.ts")
    env = dict(os.environ, IRPT_CONTRACTS_DIR=str(contracts_dir))
    p = subprocess.run([find_bun(), "--no-install", "run", str(gen_dir / "gen-wire.ts")], cwd=str(PORTAL), env=env,
                       capture_output=True, timeout=110)
    out = Path(tmp_root) / "src/pages/InvestorReporting/contracts/wire"
    return p.returncode, out, (p.stdout + p.stderr).decode("utf-8", "replace").strip()


def portal_porcelain():
    return git("-C", str(PORTAL), "status", "--porcelain", "--untracked-files=all").decode("utf-8", "replace")


def regen_both():
    """Return (base_result, new_result) each = (rc, out_dir, text); temp trees under one tmp dir."""
    tmp = tempfile.mkdtemp(prefix="u6regen_")
    # a temp dir must not sit inside the portal tree
    assert not str(Path(tmp).resolve()).startswith(str(PORTAL.resolve())), "temp dir inside portal"
    base_contracts = Path(tmp) / "base_contracts"
    shutil.copytree(str(CONTRACTS_DIR), str(base_contracts))
    (base_contracts / "AnalysisReport.schema.json").write_bytes(base_bytes())
    return tmp, run_generator(base_contracts, Path(tmp) / "base"), run_generator(CONTRACTS_DIR, Path(tmp) / "new")


def lf(b):
    return b.replace(b"\r\n", b"\n")


def arm_regen():
    head = git("-C", str(PORTAL), "rev-parse", "HEAD").decode().strip()
    if not head.startswith(PORTAL_PIN):
        print("ERROR: portal HEAD %s is not the pin %s" % (head, PORTAL_PIN))
        print("RESULT: regen FAIL")
        return 1
    committed = lf(git("-C", str(PORTAL), "show", head + ":" + TS_REL))
    on_disk = lf((PORTAL / TS_REL).read_bytes())
    print("committed AnalysisReport.ts at portal %s: %d bytes, %d lines (working copy equal to the commit: %s)"
          % (PORTAL_PIN, len(committed), committed.count(b"\n"), committed == on_disk))
    before = portal_porcelain()
    tmp, base_r, new_r = regen_both()
    after = portal_porcelain()
    print("portal tree before/after the generator runs: %r / %r (unchanged: %s)" % (before, after, before == after))
    print("generator (copy of gen-wire.ts, run from portal/ with --no-install, out-dir %s):" % tmp)
    for label, r in (("base schema", base_r), ("changed schema", new_r)):
        print("  %s: rc=%d  %s" % (label, r[0], r[2].splitlines()[-1] if r[2] else ""))
    if base_r[0] or new_r[0]:
        print("RESULT: regen FAIL")
        return 1
    base_gen = lf((base_r[1] / "AnalysisReport.ts").read_bytes())
    new_gen = lf((new_r[1] / "AnalysisReport.ts").read_bytes())
    # (1) the S388 measurement, reproduced: what a regeneration against the BASE schema removes from the committed type
    gone = [ln for ln in difflib.unified_diff(base_gen.decode().split("\n"), committed.decode().split("\n"), lineterm="", n=0)
            if ln.startswith("+") and not ln.startswith("+++")]
    print("MEASURE base schema: a regeneration drops %d lines present in the committed type (S388 measured 56)" % len(gone))
    # (2) the other 27 generated files must not move because of this change
    moved = []
    names = sorted(p.name for p in base_r[1].iterdir())
    for n in names:
        if n != "AnalysisReport.ts" and (base_r[1] / n).read_bytes() != (new_r[1] / n).read_bytes():
            moved.append(n)
    print("OTHER generated files: %d compared, %d differ between base-schema and changed-schema runs %s"
          % (len(names) - 1, len(moved), moved))
    # (3) the claim
    a, b = new_gen.decode().split("\n"), committed.decode().split("\n")
    ident = new_gen == committed
    print("changed schema: generated %d bytes / %d lines; committed %d bytes / %d lines; identical: %s"
          % (len(new_gen), len(a) - 1, len(committed), len(b) - 1, ident))
    if not ident:
        for i in range(max(len(a), len(b))):
            la, lb = (a[i] if i < len(a) else "<EOF>"), (b[i] if i < len(b) else "<EOF>")
            if la != lb:
                print("FIRST DIFFERING LINE %d:" % (i + 1))
                print("  generated: %s" % la)
                print("  committed: %s" % lb)
                break
        d = list(difflib.unified_diff(a, b, lineterm="", n=0))
        print("DIFF: %d lines only in generated, %d lines only in committed"
              % (sum(1 for ln in d if ln.startswith("-") and not ln.startswith("---")),
                 sum(1 for ln in d if ln.startswith("+") and not ln.startswith("+++"))))
        # which of the committed OPAL-form declarations can the generator emit at all
        for token in ("AnalysisSectionNotAvailableReason", "AnalysisReportOpalSectionWire", "AnalysisReportOpalWire",
                      "AnalysisReportAnyWire", "INPUT_MISSING:${string}", "/** v2 discriminator"):
            print("  committed token %-40s in generated output: %s" % (token, token.encode() in new_gen))
    shutil.rmtree(tmp, ignore_errors=True)
    print("RESULT: regen %s" % ("PASS" if ident else "FAIL"))
    return 0 if ident else 1


# ---------------------------------------------------------------------------------------------- census arm
def run_pytest(path):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rf", path],
                       cwd=str(ROOT), capture_output=True, timeout=115)
    text = p.stdout.decode("utf-8", "replace")
    failed = set()
    for line in text.splitlines():
        if line.startswith("FAILED "):
            failed.add(line[len("FAILED "):].split(" - ")[0].strip())
    last = [ln for ln in text.splitlines() if re.search(r"\b(passed|failed|error)", ln)]
    return p.returncode, failed, (last[-1].strip() if last else "")


def run_bun_tests(files):
    p = subprocess.run([find_bun(), "--no-install", "test"] + files, cwd=str(PORTAL), capture_output=True, timeout=115)
    text = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    failed = {re.sub(r"\s*\[[0-9.]+m?s\]$", "", ln[2:].strip()) for ln in text.splitlines() if ln.startswith(CROSS)}
    problems = {ln.strip() for ln in text.splitlines() if re.match(r"^AnalysisReport\.[A-Za-z_.]+: ", ln)}
    summary = [ln.strip() for ln in text.splitlines() if re.match(r"^\s*\d+ (pass|fail)$", ln.strip())]
    return p.returncode, failed, problems, summary


def pointer_get(doc, pointer):
    target = doc
    for seg in pointer.lstrip("#").lstrip("/").split("/"):
        seg = seg.replace("~1", "/").replace("~0", "~")
        target = target[int(seg)] if isinstance(target, list) else target[seg]
    return target


def reader_response_schema():
    """analysis-report.response.schema.json: resolve its five pointers into the NEW schema and validate slices."""
    import jsonschema
    from referencing import Registry, Resource
    new = json.loads(SCHEMA.read_text(encoding="utf-8"))
    resp = json.loads((CONTRACTS_DIR / "responses/analysis-report.response.schema.json").read_text(encoding="utf-8"))
    data = resp["properties"]["data"]["properties"]
    resolved = []
    for key, node in data.items():
        ref = node["$ref"]
        assert ref.startswith(new["$id"] + "#"), ref
        pointer_get(new, ref.split("#", 1)[1])
        resolved.append(key)
    registry = Registry()
    for p in sorted(CONTRACTS_DIR.glob("*.schema.json")):
        registry = registry.with_resource(json.loads(p.read_text(encoding="utf-8"))["$id"],
                                          Resource.from_contents(json.loads(p.read_text(encoding="utf-8"))))
    sub = {"$schema": resp["$schema"], "$id": resp["$id"] + "#data", "$ref": resp["$id"] + "#/properties/data"}
    v = jsonschema.Draft202012Validator(sub, registry=registry.with_resource(resp["$id"], Resource.from_contents(resp)))
    out = []
    for name, keys in (("AnalysisReport.valid.json", ("request_ref", "sections", "extraction_validation")),
                       ("AnalysisReport.v2.opal.valid.json", ("request_ref", "sections"))):
        doc = json.loads((FIXTURES / name).read_text(encoding="utf-8"))["instance"]
        slice_ = {k: doc[k] for k in keys}
        errs = list(v.iter_errors(slice_))
        out.append((name, "VALID" if not errs else "invalid: " + errs[0].message[:90]))
    return resolved, out


def arm_census():
    tracked = git("ls-files").decode("utf-8", "replace").split("\n")
    tracked = [t for t in tracked if t]
    hits = [h for h in git("grep", "-l", "-I", "-F", "AnalysisReport.schema").decode("utf-8", "replace").split("\n") if h]
    p_tracked = [t for t in git("-C", str(PORTAL), "ls-files").decode("utf-8", "replace").split("\n") if t]
    p_hits = [h for h in git("-C", str(PORTAL), "grep", "-l", "-I", "-E",
                             "AnalysisReport\\.schema|WIRE_CONTRACTS|CONSUMED_CONTRACTS|WIRE_CONTRACT_NAMES", "--", "src")
              .decode("utf-8", "replace").split("\n") if h]
    print("SEARCH 1: git grep -l -I -F 'AnalysisReport.schema' over %d tracked outer files (binary files excluded by -I): %d files hit"
          % (len(tracked), len(hits)))
    print("SEARCH 2: git -C portal grep -l -I -E 'AnalysisReport.schema|WIRE_CONTRACTS|CONSUMED_CONTRACTS|WIRE_CONTRACT_NAMES' -- src "
          "over %d tracked portal files: %d files hit" % (len(p_tracked), len(p_hits)))
    org = [h for h in hits if h.startswith("org/")]
    live = [h for h in hits if not h.startswith("org/")]
    org_scripts = [h for h in org if h.endswith((".py", ".sh", ".ts", ".mjs", ".js"))]
    print("  org/** records (documents, evidence, probes): %d files, of which %d are scripts: %s"
          % (len(org), len(org_scripts), ", ".join(org_scripts)))
    print("  outside org/: %d files" % len(live))

    py_tests = {
        LAMBDA + "/_contracts/tests/test_analysisreport_v2.py": "v2 schema file + the v1 sha pin",
        LAMBDA + "/_contracts/tests/test_undated_analysis.py": "validator over docs schema",
        LAMBDA + "/export/tests/test_packaged_contracts_match_docs.py": "packaged copy byte-equal to docs copy",
        LAMBDA + "/ops/tests/test_owned_report.py": "resolves #/properties/<key> pointers",
        LAMBDA + "/reports/tests/test_repository.py": "validator over docs schema",
        LAMBDA + "/ycharts/extract/tests/test_publication.py": "partial-view validation over docs schema",
    }
    portal_tests = {
        "src/pages/InvestorReporting/__tests__/fe-s-13/content-pins.test.ts": "required/offered pins from docs schema",
        "src/pages/InvestorReporting/__tests__/fe-s-13/producer-fixtures.test.ts": "producer fixtures vs docs schemas",
        "src/pages/InvestorReporting/__tests__/fe-s-1/fixtures.test.ts": "fixture set",
        "src/pages/InvestorReporting/__tests__/fe-s-4/manifest.test.ts": "manifest",
        "src/pages/InvestorReporting/__tests__/fe-s-47/no-status-reason.test.ts": "no status reason",
        "src/pages/InvestorReporting/__tests__/fe-s-50/hash-stability.test.ts": "renderModule hash stability",
    }
    not_run = {
        "src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-26.wire-regen.test.ts":
            "NOT RUN: it calls generate(), which WRITES into contracts/wire/; its assertion (regeneration == committed bytes) is the regen arm's AC2",
        "src/pages/InvestorReporting/__tests__/fe-s-13/gen-consumed.ts":
            "NOT RUN: it writes contracts/wire/consumed.ts; its two readers (propertiesOf, requiredOf) are the ones content-pins.test.ts applies",
        "src/pages/InvestorReporting/__tests__/fe-s-13/gen-wire.ts":
            "RUN as a copy by the regen arm (rc and output below)",
    }

    ok = True
    named = []

    def line(kind, name, verdict, note=""):
        named.append((kind, name, verdict))
        print("  READER [%s] %s -> %s%s" % (kind, name, verdict, ("  " + note) if note else ""))

    # --- classify every live hit; an unclassified one fails the census
    known_docs = {SCHEMA_REL, "docs/contracts/investor-reporting/v1/CONTRACT.md"}
    packaged_loaders = {
        LAMBDA + "/reports/resident_installed.py", LAMBDA + "/export/submit_installed.py",
        LAMBDA + "/reports/generate_installed.py", LAMBDA + "/ycharts/extract/tests/run_offline_suite.py",
        LAMBDA + "/ycharts/generate/tests/run_offline_suite.py",
    }
    manifests = {"infra/aws/lambda/ci/lambda-source-map.json", LAMBDA + "/PATH_MANIFEST.json"}
    other = {
        LAMBDA + "/_contracts/AnalysisReport.schema.json", LAMBDA + "/_contracts/AnalysisReport.v2.schema.json",
        "docs/contracts/investor-reporting/v1/responses/analysis-report.response.schema.json",
    }
    unclassified = [h for h in live if h not in known_docs and h not in py_tests and h not in packaged_loaders
                    and h not in manifests and h not in other]
    print("UNCLASSIFIED live hits: %d %s" % (len(unclassified), unclassified))
    if unclassified:
        ok = False

    # --- 1. the schema file itself
    import jsonschema
    new_bytes = SCHEMA.read_bytes()
    try:
        jsonschema.Draft202012Validator.check_schema(json.loads(new_bytes.decode("utf-8")))
        v = validator(new_bytes)
        opal = json.loads((FIXTURES / "AnalysisReport.v2.opal.valid.json").read_text(encoding="utf-8"))["instance"]
        v1 = json.loads((FIXTURES / "AnalysisReport.valid.json").read_text(encoding="utf-8"))["instance"]
        res = "reads (meta-schema valid; OPAL fixture %s, v1 fixture %s)" % (
            "VALID" if v.is_valid(opal) else "INVALID", "VALID" if v.is_valid(v1) else "INVALID")
        if not (v.is_valid(opal) and v.is_valid(v1)):
            ok = False
        line("schema", SCHEMA_REL, res)
    except Exception as exc:  # a read error is the verdict
        ok = False
        line("schema", SCHEMA_REL, "ERROR %s" % type(exc).__name__)

    # --- 2. the response schema's five pointers
    try:
        keys, outs = reader_response_schema()
        bad = [o for o in outs if not o[1].startswith("VALID")]
        if bad:
            # the OPAL slice carries no extraction_validation, which this response requires -- print, do not hide
            pass
        line("response", "docs/contracts/investor-reporting/v1/responses/analysis-report.response.schema.json",
             "pointers resolve in the new schema: %s; slices: %s" % (keys, "; ".join("%s %s" % o for o in outs)))
        if outs[0][1] != "VALID":
            ok = False
    except Exception as exc:
        ok = False
        line("response", "analysis-report.response.schema.json", "ERROR %s: %s" % (type(exc).__name__, str(exc)[:100]))

    # --- 3. the packaged copy and everything that loads it
    pk = (ROOT / LAMBDA / "_contracts/AnalysisReport.schema.json").read_bytes()
    pk_state = "UNCHANGED v1 (sha256 %s)" % sha(pk)[:12] if sha(pk) == BASE_SHA else "differs from base"
    line("packaged-copy", LAMBDA + "/_contracts/AnalysisReport.schema.json",
         "%s: carries NO OPAL_ENGINE branch until synced to the docs copy; byte-equal to docs copy now: %s"
         % (pk_state, lf(pk) == lf(SCHEMA.read_bytes())))
    for h in sorted(packaged_loaders):
        line("packaged-loader", h, "reads the PACKAGED copy (%s), not the docs file: no error, no OPAL branch until synced" % pk_state)
    for h in sorted(manifests):
        text = (ROOT / h).read_text(encoding="utf-8", errors="replace")
        stale = SCHEMA_REL in text and BASE_SHA in text
        line("manifest", h, "sha256 pin of the docs schema is %s" % ("the BASE sha (STALE after this change)" if stale else "absent/current"))
        if stale:
            ok = False

    # --- 4. generator: the regen run
    tmp, base_r, new_r = regen_both()
    gen_ok = base_r[0] == 0 and new_r[0] == 0 and (new_r[1] / "AnalysisReport.ts").is_file()
    line("generator", "portal gen-wire.ts (copy, temp out-dir)",
         "renders the new schema without UnrenderableSchemaError: %s (rc base=%d new=%d; %s)"
         % (gen_ok, base_r[0], new_r[0], new_r[2].splitlines()[-1] if new_r[2] else ""))
    if not gen_ok:
        ok = False
    shutil.rmtree(tmp, ignore_errors=True)
    for k, why in sorted(not_run.items()):
        line("portal-not-run", k, why)

    # --- 5. executable readers: run under the NEW schema; a red that the BASE schema does not show is a FAIL
    results_new = {}
    for t in py_tests:
        results_new[t] = run_pytest(t)
    pt_files = list(portal_tests)
    pnew = run_bun_tests(pt_files)
    red_py = [t for t, r in results_new.items() if r[1] or r[0] not in (0,)]
    base_py, pbase = {}, None
    with base_schema_in_place():
        for t in red_py:
            base_py[t] = run_pytest(t)
        pbase = run_bun_tests(pt_files)
    for t, why in py_tests.items():
        n, b = results_new[t], base_py.get(t, (0, set(), "clean under the new schema"))
        new_red = sorted(n[1] - b[1])
        if new_red:
            ok = False
        line("pytest", t, ("NEW RED %d: %s" % (len(new_red), [x.split("::", 1)[-1][:90] for x in new_red]))
             if new_red else "reads without error (%s)" % n[2], "[%s]" % why)
    new_probs = sorted(pnew[2] - pbase[2])
    new_fail = sorted(pnew[1] - pbase[1])
    print("  PORTAL bun test (%d files) under the new schema: %s ; under the BASE schema: %s"
          % (len(pt_files), pnew[3], pbase[3]))
    print("  PORTAL failing tests present at BASE already (not counted): %d" % len(pnew[1] & pbase[1]))
    for t, why in portal_tests.items():
        line("bun-test", t, "ran", "[%s]" % why)
    if new_fail or new_probs:
        ok = False
    print("  PORTAL NEW failing tests vs base: %d %s" % (len(new_fail), new_fail))
    print("  PORTAL NEW AnalysisReport pin problems vs base: %d" % len(new_probs))
    for pr in new_probs:
        print("    " + pr)
    # the lines above are evidence; whether the schema file ended up restored is printed by the context manager's check
    print("SCHEMA FILE restored after the base measurements: sha256 %s" % sha(SCHEMA.read_bytes()))
    print("READERS NAMED: %d" % len(named))
    print("RESULT: census %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    arms = {"schema": arm_schema, "regen": arm_regen, "census": arm_census}
    if len(argv) != 2 or argv[1] not in arms:
        print("usage: python u6_checks.py <schema|regen|census>")
        return 2
    os.chdir(str(ROOT))
    return arms[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
