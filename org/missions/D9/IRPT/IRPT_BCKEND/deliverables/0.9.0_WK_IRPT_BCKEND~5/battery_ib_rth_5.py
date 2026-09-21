#!/usr/bin/env python3
"""
battery_ib_rth_5.py -- cell IB-rth-5 (IRPT_BCKEND.TO-IB-rth-5), criterion R80-AC1.

PROVES: the storageState load branch added to `render_export.cjs` (a) EXISTS, (b) is WIRED into
the browser-context creation path -- not merely printed about -- and (c) correctly falls through
to the SAME `SESSION_ABSENT` refusal on a synthetic/invalid session that today's fresh-context
path already produces, never a false claim of success. It also proves the edit is ADDITIVE ONLY:
every other function in the file is byte-identical to the pre-cell HEAD.

WHAT IT DOES NOT PROVE, AND MUST NOT CLAIM: that a REAL session was ever established. Every
"session" this battery constructs is a well-formed-but-synthetic JSON file; the fake `playwright`
stub this battery injects ALWAYS reports a sign-in screen, regardless of what storageState it was
handed, precisely so this battery cannot accidentally report false success.

MECHANISM. `render_export.cjs` needs a real Chromium (via `playwright`) and the AWS CLI on a real
host to run end-to-end -- neither is available or appropriate in this worktree (no npm install,
no vendor/network reach, per this project's standing bars). So this battery runs the REAL,
UNMODIFIED `render_export.cjs` source under Node with:
  - a FAKE `playwright` module, resolved via NODE_PATH, that records every call it receives
    (chromium.launch / browser.newContext / context.newPage) and always reports "signed out"; and
  - a monkeypatched `child_process.execFileSync` (via `node --require`, module-cache injection
    BEFORE render_export.cjs's own require runs) that fakes only the two exact AWS CLI shapes the
    script calls, and throws loud on anything else.
This proves the ACTUAL shipped code path, not a reimplementation of it.

DISCRIMINATION (Rule 22): a NEGATIVE CONTROL run repeats the "valid synthetic session" scenario
against a deliberately UNWIRED copy of the file (the storageState call stripped back out) and
asserts the harness correctly fails to see the "session loaded" signal on that copy -- proving
this battery can tell a wired implementation from an unwired one, not just parse a hoped-for
string.

Denominators are printed. The success token prints ONLY if every scenario AND the negative
control hold.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[7]  # .../org/missions/D9/IRPT/IRPT_BCKEND/deliverables/<serial>/battery... -> repo root
HARNESS_DIR = Path(__file__).resolve().parent / "harness"
FAKE_MODULES_DIR = HARNESS_DIR / "fake_modules"
PRELOAD_PATH = HARNESS_DIR / "preload.cjs"
SCRIPT_PATH = REPO_ROOT / "infra" / "aws" / "ec2" / "investor-reporting-export" / "render_export.cjs"

SUCCESS_TOKEN = "IBR80-STORAGESTATE-LOAD-PATH-WIRED-AND-DISCRIMINATING"

# Anchors: byte-identical substrings from the file's pre-cell-IB-rth-5 HEAD (captured by direct
# Read of the committed file before this cell's edit, this session). If ANY is missing from the
# post-edit source, the edit touched something outside its declared additive scope.
ANCHOR_VENDOR_HOSTS = """const VENDOR_HOSTS = [
  'ycharts.com', 'api.ycharts.com', 'bd3.bdreporting.com', 'api.cloud.orionadvisor.com',
];"""

ANCHOR_ASSERT_NO_VENDOR_HOST = """function assertNoVendorHost(url) {
  const host = new URL(url).hostname.toLowerCase();
  for (const vendor of VENDOR_HOSTS) {
    if (host === vendor || host.endsWith(`.${vendor}`)) {
      throw new Error(`BLOCKED: VENDOR_ORIGIN -- ${host} is a vendor host; a render never calls one`);
    }
  }
  return host;
}"""

ANCHOR_NEED = """function need(name) {
  const value = process.env[name];
  if (!value) throw new Error(`BLOCKED: ${name} is required and was not supplied`);
  return value;
}"""

ANCHOR_AWSJSON = """function awsJson(args) {
  return execFileSync('aws', args, { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
}"""

ANCHOR_GUARD_OBJECT = "const GUARD = { requests: 0, byOrigin: {}, foreign: [], vendor: 0, allowedHost: null };"

ANCHOR_GUARD_SUMMARY = """function guardSummary(extra) {
  return Object.assign({
    requests_total: GUARD.requests,
    requests_by_origin: GUARD.byOrigin,
    foreign_origin_requests: GUARD.foreign.length,
    foreign_origins: GUARD.foreign.slice(0, 20),
    vendor_requests: GUARD.vendor,
    allowed_origin: GUARD.allowedHost,
    denominator: `${GUARD.foreign.length} foreign of ${GUARD.requests} request(s); vendor hosts checked: ${VENDOR_HOSTS.join(',')}`,
  }, extra || {});
}"""

ANCHOR_CATCH_HANDLER = """main().catch((err) => {
  const message = err && err.message ? err.message : String(err);
  process.stderr.write(message + "\\n");"""

ALL_ANCHORS = {
    "VENDOR_HOSTS": ANCHOR_VENDOR_HOSTS,
    "assertNoVendorHost": ANCHOR_ASSERT_NO_VENDOR_HOST,
    "need": ANCHOR_NEED,
    "awsJson": ANCHOR_AWSJSON,
    "GUARD object": ANCHOR_GUARD_OBJECT,
    "guardSummary": ANCHOR_GUARD_SUMMARY,
    "top-level catch handler": ANCHOR_CATCH_HANDLER,
}


def find_node():
    import shutil
    node = shutil.which("node")
    if not node:
        print("BLOCKED: no `node` on PATH -- cannot run this battery")
        sys.exit(1)
    return node


def run_render_script(node, source_path: Path, env_overrides: dict, call_log_path: Path, timeout_s=60):
    env = dict(os.environ)
    env["NODE_PATH"] = str(FAKE_MODULES_DIR)
    env["IB_RTH5_CALL_LOG"] = str(call_log_path)
    env.update(env_overrides)
    if call_log_path.exists():
        call_log_path.unlink()
    proc = subprocess.run(
        [node, "--require", str(PRELOAD_PATH), str(source_path)],
        cwd=str(source_path.parent),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_s,
    )
    call_log = []
    if call_log_path.exists():
        call_log = json.loads(call_log_path.read_text(encoding="utf-8"))
    return proc.returncode, proc.stdout, proc.stderr, call_log


def base_env(session_state_path: str) -> dict:
    return {
        "IRPT_BUCKET": "test-bucket",
        "IRPT_BUNDLE_KEY": "firms/testfirm/generations/EXP-test/attempts/1/exports/test/bundle.json",
        "IRPT_OUTPUT_KEY": "firms/testfirm/generations/EXP-test/attempts/1/exports/test/report.pdf",
        "IRPT_EXPORT_ID": "EXP-test",
        "IRPT_ATTEMPT_ID": "ATT-test",
        "IRPT_PRINT_ROUTE": "/investor-reporting/print",
        "IRPT_PORTAL_ORIGIN": "https://portal.test.internal",
        "AWS_REGION": "us-east-1",
        "IRPT_SESSION_STATE_PATH": session_state_path,
    }


def find_new_context_call(call_log):
    for entry in call_log:
        if entry.get("call") == "browser.newContext":
            return entry
    return None


def assert_true(condition, message, failures):
    if not condition:
        failures.append(message)


def main():
    node = find_node()
    if not SCRIPT_PATH.exists():
        print(f"BLOCKED: render_export.cjs not found at {SCRIPT_PATH}")
        sys.exit(1)

    source_text = SCRIPT_PATH.read_text(encoding="utf-8")

    failures = []

    # --- Static fidelity: every OTHER function is byte-identical to pre-cell HEAD -----------
    print("--- static fidelity: unrelated functions unchanged ---")
    for name, anchor in ALL_ANCHORS.items():
        present = anchor in source_text
        print(f"  {'OK' if present else 'FAIL'}: {name} anchor present-unchanged: {present}")
        assert_true(present, f"anchor for {name} not found byte-identical in render_export.cjs", failures)
    print(f"  denominator: {len(ALL_ANCHORS)} of {len(ALL_ANCHORS)} anchors checked")

    with tempfile.TemporaryDirectory(prefix="ib_rth5_battery_") as tmp:
        tmp_path = Path(tmp)
        call_log_path = tmp_path / "call_log.json"

        # --- Scenario A: no session state file (today's behavior must be UNCHANGED) --------
        print("\n--- scenario A: no storageState file present ---")
        absent_state_path = tmp_path / "does-not-exist" / "storageState.json"
        rc, out, err, calls = run_render_script(
            node, SCRIPT_PATH, base_env(str(absent_state_path)), call_log_path
        )
        print(f"  rc={rc}")
        assert_true(rc == 1, f"scenario A: expected rc=1 (SESSION_ABSENT), got {rc}", failures)
        assert_true(
            "OK: no session state file at" in out,
            "scenario A: missing the absent-file log line", failures,
        )
        assert_true(
            "BLOCKED: SESSION_ABSENT" in err,
            "scenario A: did not fall through to SESSION_ABSENT refusal", failures,
        )
        ctx_call = find_new_context_call(calls)
        assert_true(ctx_call is not None, "scenario A: browser.newContext was never called", failures)
        if ctx_call is not None:
            assert_true(
                not ctx_call.get("contextOptions") or "storageState" not in (ctx_call.get("contextOptions") or {}),
                f"scenario A: newContext called WITH storageState when no file exists: {ctx_call}",
                failures,
            )
        print(f"  newContext call: {ctx_call}")

        # --- Scenario B: a well-formed, clearly-SYNTHETIC session file ---------------------
        print("\n--- scenario B: well-formed SYNTHETIC storageState present ---")
        valid_state_path = tmp_path / "session_b" / "storageState.json"
        valid_state_path.parent.mkdir(parents=True, exist_ok=True)
        synthetic_state = {
            "cookies": [{
                "name": "synthetic-fake-session-never-real",
                "value": "0000000000000000000000000000000000",
                "domain": "portal.test.internal",
                "path": "/",
            }],
            "origins": [],
        }
        valid_state_path.write_text(json.dumps(synthetic_state), encoding="utf-8")
        rc, out, err, calls = run_render_script(
            node, SCRIPT_PATH, base_env(str(valid_state_path)), call_log_path
        )
        print(f"  rc={rc}")
        assert_true(rc == 1, f"scenario B: expected rc=1 (still refuses -- fake session), got {rc}", failures)
        assert_true(
            "OK: session state loaded from" in out and "attempting session reuse" in out,
            "scenario B: missing the session-loaded log line -- the NEW branch did not visibly fire",
            failures,
        )
        assert_true(
            "OK: no session state file at" not in out,
            "scenario B: printed the ABSENT-file line even though a file was present -- wrong branch",
            failures,
        )
        assert_true(
            "BLOCKED: SESSION_ABSENT" in err,
            "scenario B: did not correctly refuse on a synthetic session -- this would be a FALSE SUCCESS defect",
            failures,
        )
        assert_true(
            "OK: rendered" not in out,
            "scenario B: claimed a successful render off a synthetic session -- FALSE SUCCESS",
            failures,
        )
        ctx_call = find_new_context_call(calls)
        assert_true(ctx_call is not None, "scenario B: browser.newContext was never called", failures)
        got_storage_state = (ctx_call or {}).get("contextOptions", {}).get("storageState") if ctx_call else None
        assert_true(
            got_storage_state == str(valid_state_path),
            f"scenario B: newContext was NOT called with the synthetic storageState path "
            f"(got {got_storage_state!r}, expected {str(valid_state_path)!r}) -- the load branch "
            f"printed a message but did not actually WIRE into the context call",
            failures,
        )
        print(f"  newContext call: {ctx_call}")

        # --- Scenario C: corrupt (invalid JSON) session file -- must fall through cleanly --
        print("\n--- scenario C: corrupt (invalid JSON) storageState file ---")
        corrupt_state_path = tmp_path / "session_c" / "storageState.json"
        corrupt_state_path.parent.mkdir(parents=True, exist_ok=True)
        corrupt_state_path.write_text("{not valid json,,,", encoding="utf-8")
        rc, out, err, calls = run_render_script(
            node, SCRIPT_PATH, base_env(str(corrupt_state_path)), call_log_path
        )
        print(f"  rc={rc}")
        assert_true(rc == 1, f"scenario C: expected rc=1, got {rc}", failures)
        assert_true(
            "not valid JSON" in err,
            "scenario C: no WARN about invalid JSON -- silent/different failure mode", failures,
        )
        assert_true(
            "BLOCKED: SESSION_ABSENT" in err,
            "scenario C: did not fall through to the normal SESSION_ABSENT refusal", failures,
        )
        ctx_call = find_new_context_call(calls)
        got_storage_state = (ctx_call or {}).get("contextOptions", {}).get("storageState") if ctx_call else "MISSING-CALL"
        assert_true(
            got_storage_state is None,
            f"scenario C: newContext still received a storageState path from a corrupt file: {got_storage_state!r}",
            failures,
        )
        print(f"  newContext call: {ctx_call}")

        # --- Scenario D: well-formed JSON but wrong shape (no cookies[]/origins[]) ---------
        print("\n--- scenario D: well-formed JSON, wrong shape (not storageState-shaped) ---")
        wrong_shape_path = tmp_path / "session_d" / "storageState.json"
        wrong_shape_path.parent.mkdir(parents=True, exist_ok=True)
        wrong_shape_path.write_text(json.dumps({"hello": "world"}), encoding="utf-8")
        rc, out, err, calls = run_render_script(
            node, SCRIPT_PATH, base_env(str(wrong_shape_path)), call_log_path
        )
        print(f"  rc={rc}")
        assert_true(rc == 1, f"scenario D: expected rc=1, got {rc}", failures)
        assert_true(
            "not a well-formed storageState" in err,
            "scenario D: no WARN about the wrong shape", failures,
        )
        ctx_call = find_new_context_call(calls)
        got_storage_state = (ctx_call or {}).get("contextOptions", {}).get("storageState") if ctx_call else "MISSING-CALL"
        assert_true(
            got_storage_state is None,
            f"scenario D: newContext still received a storageState path from a wrong-shape file: {got_storage_state!r}",
            failures,
        )
        print(f"  newContext call: {ctx_call}")

        print("\n  denominator: 4 of 4 scenarios run (A absent, B synthetic-valid, C corrupt-json, D wrong-shape)")

        # --- Negative control: an UNWIRED copy must NOT show the session-loaded signal -----
        print("\n--- negative control: deliberately UNWIRED copy of render_export.cjs ---")
        wired_snippet = (
            "const contextOptions = loadSessionContextOptions(SESSION_STATE_PATH);\n"
            "    const context = await browser.newContext(contextOptions);\n"
            "    const page = await context.newPage();"
        )
        assert_true(
            wired_snippet in source_text,
            "negative control setup: could not find the exact wired snippet to strip out of the real file -- "
            "cannot construct the negative control, treat as a battery defect",
            failures,
        )
        unwired_source = source_text.replace(
            wired_snippet,
            "const page = await browser.newPage();",
        )
        assert_true(
            unwired_source != source_text,
            "negative control: the unwiring edit made no change to the source -- snippet did not match",
            failures,
        )
        unwired_path = tmp_path / "render_export.UNWIRED.cjs"
        unwired_path.write_text(unwired_source, encoding="utf-8")
        rc, out, err, calls = run_render_script(
            node, unwired_path, base_env(str(valid_state_path)), call_log_path
        )
        print(f"  rc={rc}")
        # The unwired copy must NOT show the session-loaded signal, and newContext must never be
        # called (it calls the legacy browser.newPage() path instead) -- if it DID show the
        # signal, this battery's checks above could not be trusted to discriminate wired code
        # from a no-op, and the success token below must not print.
        control_holds = (
            "OK: session state loaded from" not in out
            and find_new_context_call(calls) is None
        )
        print(f"  control holds (correctly shows NO session-loaded signal on unwired code): {control_holds}")
        assert_true(
            control_holds,
            "NEGATIVE CONTROL FAILED: the unwired copy still showed session-loaded / newContext-with-storageState "
            "signals -- this battery cannot discriminate a wired implementation from an unwired one, "
            "so its PASS on scenario B is not trustworthy",
            failures,
        )

    print("\n--- summary ---")
    if failures:
        print(f"FAIL: {len(failures)} of {len(ALL_ANCHORS) + 5} checks failed:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    print(f"PASS: {len(ALL_ANCHORS)} of {len(ALL_ANCHORS)} static anchors unchanged; "
          f"4 of 4 scenarios (A/B/C/D) correct; 1 of 1 negative control correctly discriminating.")
    print(SUCCESS_TOKEN)


if __name__ == "__main__":
    main()
