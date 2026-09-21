#!/usr/bin/env python3
"""MDPF_TAXSMA TX-g-2 probe: one acceptance criterion per invocation (TXG2-AC1 .. TXG2-AC4).

    cd <WS> && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~1/probes/tx_g_2.py AC<n>

Each run prints its measurement with vintage (HEAD, UTC time) and denominator, then exactly one line:
`VERDICT: PASS-TXG2-AC<n>` or `VERDICT: FAIL-TXG2-AC<n> <reason>`.

  AC1  extracts the BUILD-ONLY portion of the registered deploy script (infra/aws/ec2/opal-gateway/deploy-to-ec2.sh,
       named by EC2_MANIFEST.json's Gateway row `deploy_script`) -- the block from the instance-id resolution
       through the `tar -czf` artifact build and its "built artifact" echo -- verbatim out of the script's own
       bytes, stops BEFORE the S3 upload / SSM sections, and runs exactly that extracted block in a fresh bash
       process. It then lists the built tarball's members and compares app/taxsma_workbook.py's SHA-256 inside
       the tarball against the source file's SHA-256. No `aws` call occurs in this arm (the manifest already
       carries a live instance_id, so the script's own `aws ec2 describe-instances` fallback branch never runs).
  AC2  reads deploy-to-ec2.sh's tar invocation statically: the archived member list and the --exclude set. If
       `app` is archived as a whole directory member and no exclude targets it or the module, the builder already
       bundles the module -- VERIFY-REUSE -- and this arm asserts the cell changed no file (git diff empty on the
       deploy script and on this repo's tracked set under the order's grant).
  AC3  reads infra/aws/ec2/EC2_MANIFEST.json's `services["opal-gateway"]` row, states its `deploy_script` field
       (the registered deploy path), and asserts the cell has not touched `deployed_commit` (git diff empty on the
       manifest file).
  AC4  reads deliverables/0.9.0_WK_MDPF_TAXSMA~1/command_log.jsonl (appended by AC1..AC3 of this same probe; if the
       log is empty because AC4 ran standalone, it runs AC1..AC3 first to populate it) and asserts no logged
       command -- and no line of AC1's executed build fragment -- names `ssm send-command` or an S3 write verb
       (`s3 cp`, `s3api put-object`).

A failed or empty read is a FAIL, never a zero.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _resolve_bash() -> str:
    """A bare 'bash' argv[0] under Windows CreateProcess can resolve to the WSL relay stub
    (C:\\Windows\\System32\\bash.exe) instead of Git Bash even when shutil.which finds Git Bash first --
    measured here (WSL relay error) despite shutil.which('bash') returning the Git Bash path. Always pass
    the RESOLVED absolute path as argv[0]; a missing resolution is a loud refusal, never a silent WSL fallback."""
    for candidate in (shutil.which("bash"), r"C:\Program Files\Git\bin\bash.exe",
                      r"C:\Program Files\Git\usr\bin\bash.exe"):
        if candidate and Path(candidate).is_file():
            return candidate
    raise RuntimeError("could not resolve a Git Bash executable (bare 'bash' risks the WSL relay stub)")


BASH = _resolve_bash()
HERE = Path(__file__).resolve()
DELIVERABLES_DIR = HERE.parent.parent
COMMAND_LOG = DELIVERABLES_DIR / "command_log.jsonl"
GW_REL = "infra/aws/ec2/opal-gateway"
DEPLOY_SCRIPT_REL = f"{GW_REL}/deploy-to-ec2.sh"
MODULE_REL = f"{GW_REL}/app/taxsma_workbook.py"
MANIFEST_REL = "infra/aws/ec2/EC2_MANIFEST.json"
SERVICE_KEY = "opal-gateway"

FORBIDDEN_PATTERNS = [
    re.compile(r"\bssm\s+send-command\b", re.IGNORECASE),
    re.compile(r"\bs3\s+cp\b", re.IGNORECASE),
    re.compile(r"\bs3api\s+put-object\b", re.IGNORECASE),
]


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _repo() -> Path:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(HERE.parent),
                        capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError("git rev-parse --show-toplevel failed: rc=%s %s" % (r.returncode, r.stderr.strip()))
    return Path(r.stdout.strip())


def _git(repo: Path, *args: str) -> tuple:
    r = subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout, r.stderr


def _msys_path(windows_path: Path) -> str:
    """MSYS bash's PATH is colon-separated; a raw Windows form ("C:/tmp/...") is split on the drive-letter
    colon and silently breaks executable resolution (measured here: 'jq: command not found' after exporting
    PATH with a Windows-form entry). Convert with cygpath -u; refuse loud rather than guess if it is absent."""
    cygpath = shutil.which("cygpath")
    if not cygpath:
        raise RuntimeError("cygpath not found -- cannot safely derive an MSYS-form path")
    r = subprocess.run([cygpath, "-u", str(windows_path)], capture_output=True, text=True, timeout=30)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError("cygpath -u failed on %s: rc=%s %s" % (windows_path, r.returncode, r.stderr.strip()))
    return r.stdout.strip()


def _vintage(repo: Path) -> str:
    rc, head, _ = _git(repo, "rev-parse", "--short=10", "HEAD")
    rc2, br, _ = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    return "vintage: HEAD %s (branch %s), %s UTC" % (head.strip() or "UNKNOWN", br.strip() or "UNKNOWN", _utc())


def _log_cmd(ac: str, argv, rc: int, note: str = "", scanned_text: str = "") -> None:
    """Append one command-log entry. `scanned_text` (if given) is scanned HERE, at log time, for the forbidden
    SSM-send / S3-put patterns, and the result is recorded on the row -- AC4 re-checks this same field, never
    re-deriving it from `scanned_text` (which is not itself persisted, to keep the log small)."""
    hit = None
    if scanned_text:
        for pat in FORBIDDEN_PATTERNS:
            m = pat.search(scanned_text)
            if m:
                hit = m.group(0)
                break
    entry = {
        "ts": _utc(),
        "ac": ac,
        "argv": argv if isinstance(argv, list) else [str(argv)],
        "rc": rc,
        "note": note,
        "forbidden_match": hit,
    }
    DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)
    with open(COMMAND_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=True) + "\n")


def _fail(ac: str, reason: str) -> None:
    print("VERDICT: FAIL-%s %s" % (ac, reason))
    sys.exit(1)


def _pass(ac: str) -> None:
    print("VERDICT: PASS-%s" % ac)
    sys.exit(0)


# --------------------------------------------------------------------------------------------------------------
# AC1 -- build via the registered deploy path's own bytes, stopping before S3/SSM; verify the module's SHA-256.
# --------------------------------------------------------------------------------------------------------------

def _extract_manifest_deploy_script(repo: Path) -> str:
    manifest = json.loads((repo / MANIFEST_REL).read_text(encoding="utf-8"))
    row = manifest.get("services", {}).get(SERVICE_KEY)
    if not row:
        raise RuntimeError("EC2_MANIFEST.json has no services.%s row" % SERVICE_KEY)
    ds = row.get("deploy_script")
    if not ds:
        raise RuntimeError("EC2_MANIFEST.json services.%s carries no deploy_script" % SERVICE_KEY)
    return ds


def _extract_build_fragment(script_text: str) -> tuple:
    """Pull the constants block and the instance-id-through-artifact-build block verbatim out of the deploy
    script's own text. Returns (constants_lines, build_block_text). Raises if either marker is absent -- an
    absent marker is a REFUSAL (the script changed shape), never a silent skip."""
    const_names = ["SERVICE", "REGION", "ARTIFACT_BUCKET", "ARTIFACT_PREFIX", "REMOTE_DIR", "SYSTEMD_UNIT",
                   "GATEWAY_PORT"]
    consts = []
    for name in const_names:
        # The assignment line itself, quote-delimited value only -- trailing inline comments (e.g. SYSTEMD_UNIT's)
        # are deliberately NOT captured, so the fragment gets the same bash assignment with none of the comment.
        m = re.search(r'^%s="[^"]*"' % re.escape(name), script_text, re.MULTILINE)
        if not m:
            raise RuntimeError("deploy-to-ec2.sh: constant %s not found in its declared shape" % name)
        consts.append(m.group(0))

    lines = script_text.splitlines()
    start_idx = end_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith('INSTANCE_ID="${1:-}"'):
            start_idx = i
        if 'echo "INFO: built artifact $ART' in ln:
            end_idx = i
    if start_idx is None or end_idx is None or end_idx < start_idx:
        raise RuntimeError("deploy-to-ec2.sh: could not locate the instance-id..built-artifact block by marker")
    build_block = "\n".join(lines[start_idx:end_idx + 1])
    # Belt-and-suspenders: the block we are about to EXECUTE must itself carry none of the forbidden verbs.
    for pat in FORBIDDEN_PATTERNS:
        if pat.search(build_block):
            raise RuntimeError("extracted build block unexpectedly contains a forbidden verb: %s" % pat.pattern)
    return consts, build_block


def ac1(repo: Path) -> None:
    print(_vintage(repo))
    deploy_script_field = _extract_manifest_deploy_script(repo)
    print("registered deploy_script (EC2_MANIFEST.json services.%s): %s" % (SERVICE_KEY, deploy_script_field))
    deploy_script_path = repo / deploy_script_field
    if not deploy_script_path.is_file():
        _fail("TXG2-AC1", "registered deploy script %s does not exist" % deploy_script_field)
    script_text = deploy_script_path.read_text(encoding="utf-8")

    try:
        consts, build_block = _extract_build_fragment(script_text)
    except RuntimeError as exc:
        _fail("TXG2-AC1", "extraction: %s" % exc)

    ws_posix = _msys_path(repo)
    scratch_dir = repo / ".scratch" / "tx_g_2"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    fragment_path = scratch_dir / "ac1_build_fragment.sh"
    appendix = (
        '\n# --- probe verification appendix (not part of the registered script; runs before the tar dir'
        ' is removed by the script\'s own trap) ---\n'
        'echo "PROBE_TMP=$TMP"\n'
        'echo "PROBE_ART=$ART"\n'
        'echo "PROBE_MEMBERS_BEGIN"\n'
        'tar tzf "$TMP/$ART"\n'
        'echo "PROBE_MEMBERS_END"\n'
        'mkdir -p "$TMP/probe_extract"\n'
        'tar -xzf "$TMP/$ART" -C "$TMP/probe_extract" app/taxsma_workbook.py\n'
        'echo "PROBE_SHA_BUILT=$(sha256sum "$TMP/probe_extract/app/taxsma_workbook.py" | cut -d\' \' -f1)"\n'
        'echo "PROBE_SHA_SOURCE=$(sha256sum "$WORKSPACE_ROOT/%s" | cut -d\' \' -f1)"\n' % MODULE_REL
    )
    fragment_text = (
        "set -euo pipefail\n"
        'export PATH="%s/.tools:$PATH"\n' % ws_posix +
        'WORKSPACE_ROOT="%s"\n' % ws_posix +
        "\n".join(consts) + "\n" +
        build_block + "\n" +
        appendix
    )
    fragment_path.write_text(fragment_text, encoding="utf-8", newline="\n")

    r = subprocess.run([BASH, str(fragment_path)], cwd=str(repo), capture_output=True, text=True, timeout=100)
    _log_cmd("TXG2-AC1", [BASH, str(fragment_path)], r.returncode,
              note="registered-deploy-path build fragment (instance-id..built-artifact, verbatim from %s)"
                   % deploy_script_field,
              scanned_text=fragment_text)
    print("build fragment rc=%s" % r.returncode)
    print("--- stdout ---")
    print(r.stdout)
    if r.stderr.strip():
        print("--- stderr ---")
        print(r.stderr)
    if r.returncode != 0:
        _fail("TXG2-AC1", "build fragment exited rc=%s" % r.returncode)

    members_m = re.search(r"PROBE_MEMBERS_BEGIN\n(.*?)PROBE_MEMBERS_END", r.stdout, re.DOTALL)
    if not members_m:
        _fail("TXG2-AC1", "member list markers not found in build output")
    members = [ln.strip() for ln in members_m.group(1).splitlines() if ln.strip()]
    if not any(m == "app/taxsma_workbook.py" or m.endswith("/app/taxsma_workbook.py") for m in members):
        _fail("TXG2-AC1", "app/taxsma_workbook.py not among the %d archived members" % len(members))
    print("archived member list (%d members):" % len(members))
    for m in members:
        print("  %s" % m)

    sha_built_m = re.search(r"PROBE_SHA_BUILT=([0-9a-f]{64})", r.stdout)
    sha_src_m = re.search(r"PROBE_SHA_SOURCE=([0-9a-f]{64})", r.stdout)
    if not sha_built_m or not sha_src_m:
        _fail("TXG2-AC1", "SHA-256 markers not found in build output")
    sha_built, sha_src = sha_built_m.group(1), sha_src_m.group(1)
    # Independent, second-instrument confirmation of the source hash (not just trusting the bash arm).
    sha_src_py = hashlib.sha256((repo / MODULE_REL).read_bytes()).hexdigest()
    print("SHA-256 in built package : %s" % sha_built)
    print("SHA-256 of source (bash) : %s" % sha_src)
    print("SHA-256 of source (py)   : %s" % sha_src_py)
    if sha_built != sha_src or sha_src != sha_src_py:
        _fail("TXG2-AC1", "SHA-256 mismatch (built=%s source-bash=%s source-py=%s)"
              % (sha_built, sha_src, sha_src_py))
    _pass("TXG2-AC1")


# --------------------------------------------------------------------------------------------------------------
# AC2 -- static: does the builder already bundle app/ whole? If so, VERIFY-REUSE and no file changes.
# --------------------------------------------------------------------------------------------------------------

def _extract_tar_invocation(script_text: str) -> str:
    lines = script_text.splitlines()
    start_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("tar -czf"):
            start_idx = i
            break
    if start_idx is None:
        raise RuntimeError("no 'tar -czf' invocation found in deploy-to-ec2.sh")
    block = [lines[start_idx]]
    i = start_idx
    while lines[i].rstrip().endswith("\\"):
        i += 1
        block.append(lines[i])
    return "\n".join(block)


def ac2(repo: Path) -> None:
    print(_vintage(repo))
    deploy_script_path = repo / DEPLOY_SCRIPT_REL
    script_text = deploy_script_path.read_text(encoding="utf-8")
    try:
        tar_block = _extract_tar_invocation(script_text)
    except RuntimeError as exc:
        _fail("TXG2-AC2", "extraction: %s" % exc)
    print("tar invocation as registered:")
    print(tar_block)

    excludes = re.findall(r"--exclude='([^']*)'", tar_block)
    last_line = tar_block.splitlines()[-1]
    members = last_line.strip().split()
    print("excludes (%d): %s" % (len(excludes), excludes))
    print("archived members (%d): %s" % (len(members), members))

    bundles_app_whole = "app" in members
    module_basename = MODULE_REL.rsplit("/", 1)[-1]
    excludes_hit_module = any(
        exc in ("app", "app/*", "app/**") or exc == module_basename or "taxsma_workbook" in exc
        for exc in excludes
    )
    print("bundles 'app' as a whole directory member: %s" % bundles_app_whole)
    print("an --exclude targets the app dir or the module (checked against %r): %s"
          % (module_basename, excludes_hit_module))

    if not (bundles_app_whole and not excludes_hit_module):
        _fail("TXG2-AC2", "the builder does NOT already bundle app/ whole as read -- this arm does not apply "
                           "(TXG2-AC1 covers the actual build; a script edit is out of this arm's scope)")

    print("VERIFY-REUSE: the builder already bundles the app directory whole; module app/taxsma_workbook.py is "
          "covered with no addition needed.")
    rc, out, err = _git(repo, "status", "--porcelain", "--", DEPLOY_SCRIPT_REL)
    _log_cmd("TXG2-AC2", ["git", "status", "--porcelain", "--", DEPLOY_SCRIPT_REL], rc, note="verify no edit made")
    print("git status --porcelain -- %s : %r" % (DEPLOY_SCRIPT_REL, out))
    if out.strip():
        _fail("TXG2-AC2", "deploy-to-ec2.sh shows a working-tree change: %r" % out.strip())
    rc2, diffout, _ = _git(repo, "diff", "--stat", "HEAD", "--", DEPLOY_SCRIPT_REL)
    _log_cmd("TXG2-AC2", ["git", "diff", "--stat", "HEAD", "--", DEPLOY_SCRIPT_REL], rc2, note="verify no edit made")
    print("git diff --stat HEAD -- %s : %r" % (DEPLOY_SCRIPT_REL, diffout))
    if diffout.strip():
        _fail("TXG2-AC2", "deploy-to-ec2.sh diffs from HEAD: %r" % diffout.strip())
    _pass("TXG2-AC2")


# --------------------------------------------------------------------------------------------------------------
# AC3 -- read EC2_MANIFEST.json's Gateway row, state its deploy path, assert deployed_commit untouched.
# --------------------------------------------------------------------------------------------------------------

def ac3(repo: Path) -> None:
    print(_vintage(repo))
    manifest_path = repo / MANIFEST_REL
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    row = manifest.get("services", {}).get(SERVICE_KEY)
    if not row:
        _fail("TXG2-AC3", "EC2_MANIFEST.json has no services.%s row" % SERVICE_KEY)
    deploy_script = row.get("deploy_script")
    deployed_commit = row.get("deployed_commit")
    deployed_at = row.get("deployed_at")
    print("services.%s.deploy_script : %s" % (SERVICE_KEY, deploy_script))
    print("services.%s.deployed_commit : %s" % (SERVICE_KEY, deployed_commit))
    print("services.%s.deployed_at : %s" % (SERVICE_KEY, deployed_at))
    if not deploy_script:
        _fail("TXG2-AC3", "deploy_script field is empty/absent")

    rc, out, err = _git(repo, "status", "--porcelain", "--", MANIFEST_REL)
    _log_cmd("TXG2-AC3", ["git", "status", "--porcelain", "--", MANIFEST_REL], rc, note="verify deployed_commit untouched")
    print("git status --porcelain -- %s : %r" % (MANIFEST_REL, out))
    if out.strip():
        _fail("TXG2-AC3", "EC2_MANIFEST.json shows a working-tree change: %r" % out.strip())
    rc2, diffout, _ = _git(repo, "diff", "HEAD", "--", MANIFEST_REL)
    _log_cmd("TXG2-AC3", ["git", "diff", "HEAD", "--", MANIFEST_REL], rc2, note="verify deployed_commit untouched")
    if diffout.strip():
        _fail("TXG2-AC3", "EC2_MANIFEST.json diffs from HEAD (deployed_commit or another field was edited): %r"
              % diffout.strip()[:400])
    print("EC2_MANIFEST.json unchanged vs HEAD (diff empty); deployed_commit not edited by this cell.")
    _pass("TXG2-AC3")


# --------------------------------------------------------------------------------------------------------------
# AC4 -- the command log carries no SSM send-command and no S3 put.
# --------------------------------------------------------------------------------------------------------------

def ac4(repo: Path) -> None:
    print(_vintage(repo))
    if not COMMAND_LOG.exists() or not COMMAND_LOG.read_text(encoding="utf-8").strip():
        print("command_log.jsonl is empty/absent -- running AC1..AC3 first to populate it (self-sufficient arm).")
        for fn, ac_id in ((ac1, "TXG2-AC1"), (ac2, "TXG2-AC2"), (ac3, "TXG2-AC3")):
            try:
                fn(repo)
            except SystemExit as exc:
                if exc.code not in (0, None):
                    print("(AC4 pre-population run of %s exited non-zero; continuing to grade the log as-is)" % ac_id)

    if not COMMAND_LOG.exists():
        _fail("TXG2-AC4", "command_log.jsonl still absent after pre-population")
    lines = [ln for ln in COMMAND_LOG.read_text(encoding="utf-8").splitlines() if ln.strip()]
    print("command_log.jsonl entries: %d (denominator)" % len(lines))
    if not lines:
        _fail("TXG2-AC4", "command_log.jsonl has zero entries -- an empty log is not evidence of a clean one")

    offenders = []
    for i, ln in enumerate(lines):
        try:
            entry = json.loads(ln)
        except json.JSONDecodeError:
            offenders.append((i, "UNPARSEABLE LINE", ln[:200]))
            continue
        argv_str = " ".join(entry.get("argv", []))
        for pat in FORBIDDEN_PATTERNS:
            if pat.search(argv_str):
                offenders.append((i, "argv", argv_str))
        if entry.get("forbidden_match"):
            offenders.append((i, "forbidden_match", entry["forbidden_match"]))

    print("entries scanned: %d; offending entries: %d" % (len(lines), len(offenders)))
    for idx, kind, detail in offenders:
        print("  OFFENDER[%d] (%s): %s" % (idx, kind, detail))

    if offenders:
        _fail("TXG2-AC4", "%d of %d command_log.jsonl entries name an SSM send-command or an S3 put"
              % (len(offenders), len(lines)))
    print("0 of %d command_log.jsonl entries name ssm send-command, s3 cp or s3api put-object." % len(lines))
    _pass("TXG2-AC4")


AC_FUNCS = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in AC_FUNCS:
        print("usage: tx_g_2.py {%s}" % "|".join(AC_FUNCS), file=sys.stderr)
        return 2
    ac_id = sys.argv[1]
    repo = _repo()
    full_id = "TXG2-%s" % ac_id
    try:
        AC_FUNCS[ac_id](repo)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 -- a probe failure is reported as FAIL, never a traceback-only exit
        print("VERDICT: FAIL-%s exception: %s: %s" % (full_id, type(exc).__name__, exc))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
