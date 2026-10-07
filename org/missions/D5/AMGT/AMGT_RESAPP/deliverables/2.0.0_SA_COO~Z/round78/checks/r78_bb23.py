"""AMGT_RESAPP round 78 -- AMGT-bb-23, pyarrow and rpds-py are taken from the deployed package, never fetched.

  python r78_bb23.py --crit AC1|AC2|AC3
  python r78_bb23.py --compare-zip <new.zip>     (not a criterion: the bb-18 read of a BUILT zip)

The ruling (CTO msg 31206): the build script takes the two folders only from a zip whose sha256 equals the live
function's CodeSha256 read at build time, and stops if it does not; it never falls back to a download. The check is
that the two folders equal the deployed zip's byte for byte, with a negative control (one changed byte fails).

The deployed package on this box is DEPLOYED_ZIP (override: env R78_BB23_DEPLOYED_ZIP). The four folders are FOLDERS.
The helper under test is HELPER; the build script is SCRIPT. Nothing here runs the build, pip or any AWS write. One
AWS read: lambda get_function_configuration (CodeSha256) for AC1 and AC2. Temp files go under tempfile and are removed.

AC1 (build) the helper, handed the deployed zip and the live CodeSha256, fills an empty folder with exactly the zip's
     entries under the four folders, byte for byte.
  C1 the zip's sha256 (base64) equals the live CodeSha256 (bound: PASS at the base);
  C2 the helper exists and exits 0;
  C3 every zip entry under the four folders is in the filled folder with equal bytes, and nothing else is there;
  C4 the per-folder counts are the ones measured on 2026-10-07 (132 + 6 and 4 + 5, 147 in all).
AC2 (build) the negative controls.
  P0 the helper exits 0 on the right sha (without this a non-zero exit below proves nothing);
  N1 a wrong expected sha: non-zero exit, a line naming sha256, 0 files copied;
  N2 a copy of the zip with ONE byte changed inside a pyarrow member, the live sha expected: non-zero exit, 0 files;
  N3 the comparer of C3 reports exactly 1 mismatch when one extracted byte is flipped (bound: PASS at the base);
  N4 a small zip whose pyarrow dist-info folder is another version, its own true sha expected: non-zero exit, 0 files.
AC3 (build, with two bound clauses) read from the script TEXT.
  C1 VENDOR_PINS expands to exactly the five pure pins;
  C2 no pip download command that names --platform names pyarrow or rpds;
  C3 the script requires AMGT_DEPLOYED_ZIP, reads CodeSha256 by get-function-configuration and calls the helper
     with --expect-sha256= under MSYS2_ARG_CONV_EXCL, all before the first pip download;
  C4 no other fetch route: none of the fetch tokens in the script, and the helper imports no network module;
  C5 (bound) the script's VENDOR_PRUNE, applied to the deployed zip's entries under the four folders, removes 0;
  C6 (bound) bash -n on the script exits 0;
  C7 the packaging step (python - "$ROOT" "$ZIP" "$WHEELS" ...) is handed "$FROM_DEPLOYED" and the refusal text
     "expected exactly 2 admitted native wheels" is gone (printed before C6).
Verdict: R78 BB23 <crit> SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

DEPLOYED_ZIP = os.environ.get("R78_BB23_DEPLOYED_ZIP", "C:/tmp/ba20-r77-14a36147bd.zip")
FUNCTION = "opal-amgt-scoped-api"
REGION = "us-east-1"
SCRIPT = "infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh"
HELPER = "infra/aws/terraform/harvest/vendor_from_deployed.py"
FOLDERS = ("pyarrow/", "pyarrow-16.1.0.dist-info/", "rpds/", "rpds_py-2026.6.3.dist-info/")
MEASURED = {"pyarrow/": 132, "pyarrow-16.1.0.dist-info/": 6, "rpds/": 4, "rpds_py-2026.6.3.dist-info/": 5}
PURE_PINS = {"jsonschema==4.26.0", "attrs==26.1.0", "jsonschema-specifications==2025.9.1", "referencing==0.37.0",
             "typing_extensions==4.16.0"}
TWO = ("pyarrow", "rpds")
FETCH_TOKENS = ("curl ", "wget ", "Code.Location", "get-object", "s3 cp", "s3 sync", "urlopen", "urlretrieve")
NETWORK_MODULES = {"urllib", "http", "socket", "ssl", "ftplib", "subprocess", "boto3", "botocore", "requests", "pip"}


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _line(ok, label, detail):
    print("%s %s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def _verdict(crit, results):
    ok = all(results)
    print("R78 BB23 %s SERVED: %s" % (crit, "YES" if ok else "NO"))
    return 0 if ok else 1


def b64_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return base64.b64encode(h.digest()).decode("ascii")


def live_sha():
    """(CodeSha256, None) from one read-only get_function_configuration, or (None, why)."""
    try:
        import boto3

        cfg = boto3.client("lambda", region_name=REGION).get_function_configuration(FunctionName=FUNCTION)
        return cfg["CodeSha256"], None
    except Exception as exc:  # noqa: BLE001 -- a failed read is printed as a failed read, never as a mismatch
        return None, "%s: %s" % (type(exc).__name__, str(exc)[:160])


def zip_entries(zip_path):
    """{entry name: bytes} of every file entry under the four folders."""
    out = {}
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if not info.is_dir() and info.filename.startswith(FOLDERS):
                out[info.filename] = zf.read(info.filename)
    return out


def tree_files(dest):
    """{forward-slash relative path: absolute path} of every file under dest."""
    out = {}
    if not os.path.isdir(dest):
        return out
    for base, _dirs, names in os.walk(dest):
        for n in names:
            ap = os.path.join(base, n)
            out[os.path.relpath(ap, dest).replace(os.sep, "/")] = ap
    return out


def compare(want, dest):
    """want {name: bytes} against the files under dest: (equal, mismatched, missing, extra)."""
    have = tree_files(dest)
    equal, mismatched, missing = 0, [], []
    for name in sorted(want):
        if name not in have:
            missing.append(name)
            continue
        with open(have[name], "rb") as fh:
            same = fh.read() == want[name]
        if same:
            equal += 1
        else:
            mismatched.append(name)
    extra = sorted(n for n in have if n not in want)
    return equal, mismatched, missing, extra


def counts(names):
    return {pre: sum(1 for n in names if n.startswith(pre)) for pre in FOLDERS}


def run_helper(root, zip_path, sha, dest):
    """(rc, output) of the helper; (None, why) when it cannot be run."""
    helper = os.path.join(root, HELPER.replace("/", os.sep))
    if not os.path.isfile(helper):
        return None, "the helper %s does not exist" % HELPER
    p = subprocess.run([sys.executable, helper, "--zip", zip_path, "--expect-sha256=" + sha, "--dest", dest],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout + p.stderr)


def _tail(text):
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    return (lines[-1] if lines else "")[:200]


def ac1(root):
    results = []
    want = zip_entries(DEPLOYED_ZIP)
    zc = counts(want)
    zsha = b64_sha256(DEPLOYED_ZIP)
    print("   deployed zip %s: %d bytes, sha256 %s; entries under the four folders %d %s"
          % (DEPLOYED_ZIP, os.path.getsize(DEPLOYED_ZIP), zsha, len(want), [zc[p] for p in FOLDERS]))
    live, why = live_sha()
    results.append(_line(live is not None and live == zsha, "C1 the zip's sha256 equals the live CodeSha256",
                         "zip %s live %s%s" % (zsha, live, "" if why is None else " (live read failed: %s)" % why)))
    tmp = tempfile.mkdtemp(prefix="r78bb23_")
    try:
        dest = os.path.join(tmp, "dest")
        rc, out = run_helper(root, DEPLOYED_ZIP, live or zsha, dest)
        results.append(_line(rc == 0, "C2 the helper exists and exits 0", "rc=%s %s" % (rc, _tail(out))))
        equal, mismatched, missing, extra = compare(want, dest)
        results.append(_line(equal == len(want) and not mismatched and not missing and not extra and rc == 0,
                             "C3 the filled folder equals the zip's entries byte for byte",
                             "%d of %d equal; mismatched %d, missing %d, extra %d %s"
                             % (equal, len(want), len(mismatched), len(missing), len(extra),
                                (mismatched + missing + extra)[:3])))
        dc = counts(tree_files(dest))
        results.append(_line(dc == MEASURED and zc == MEASURED, "C4 the per-folder counts are the measured ones",
                             "filled %s zip %s measured %s; pyarrow %d of 138, rpds %d of 9"
                             % ([dc[p] for p in FOLDERS], [zc[p] for p in FOLDERS], [MEASURED[p] for p in FOLDERS],
                                dc[FOLDERS[0]] + dc[FOLDERS[1]], dc[FOLDERS[2]] + dc[FOLDERS[3]])))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return _verdict("AC1", results)


def one_byte_copy(src, dst):
    """Copy src to dst and flip ONE byte inside the stored bytes of a pyarrow member. Returns (member, offset)."""
    with zipfile.ZipFile(src) as zf:
        info = zf.getinfo("pyarrow/__init__.py")
    shutil.copyfile(src, dst)
    with open(dst, "r+b") as fh:
        fh.seek(info.header_offset + 26)
        name_len, extra_len = struct.unpack("<HH", fh.read(4))
        at = info.header_offset + 30 + name_len + extra_len + info.compress_size // 2
        fh.seek(at)
        byte = fh.read(1)
        fh.seek(at)
        fh.write(bytes([byte[0] ^ 0x01]))
    return info.filename, at


def other_version_zip(path):
    """A small zip holding the four folders, except that the pyarrow dist-info folder is version 17.0.0."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("pyarrow/__init__.py", "x = 1\n")
        zf.writestr("pyarrow-17.0.0.dist-info/METADATA", "Name: pyarrow\nVersion: 17.0.0\n")
        zf.writestr("rpds/__init__.py", "y = 1\n")
        zf.writestr("rpds_py-2026.6.3.dist-info/METADATA", "Name: rpds-py\nVersion: 2026.6.3\n")


def ac2(root):
    results = []
    live, why = live_sha()
    zsha = b64_sha256(DEPLOYED_ZIP)
    print("   deployed zip sha256 %s; live CodeSha256 %s%s" % (zsha, live, "" if why is None else " (%s)" % why))
    right = live or zsha
    tmp = tempfile.mkdtemp(prefix="r78bb23_")
    try:
        d0 = os.path.join(tmp, "p0")
        rc0, out0 = run_helper(root, DEPLOYED_ZIP, right, d0)
        results.append(_line(rc0 == 0 and len(tree_files(d0)) == sum(MEASURED.values()),
                             "P0 the helper exits 0 on the right sha and copies the files",
                             "rc=%s files %d %s" % (rc0, len(tree_files(d0)), _tail(out0))))
        helper_ok = rc0 == 0

        wrong = base64.b64encode(hashlib.sha256(b"r78 bb23 wrong").digest()).decode("ascii")
        d1 = os.path.join(tmp, "n1")
        rc1, out1 = run_helper(root, DEPLOYED_ZIP, wrong, d1)
        results.append(_line(helper_ok and rc1 not in (None, 0) and len(tree_files(d1)) == 0 and "sha256" in out1.lower(),
                             "N1 a wrong expected sha stops the helper and nothing is copied",
                             "rc=%s files %d %s" % (rc1, len(tree_files(d1)), _tail(out1))))

        bad = os.path.join(tmp, "one-byte.zip")
        member, at = one_byte_copy(DEPLOYED_ZIP, bad)
        bad_sha = b64_sha256(bad)
        d2 = os.path.join(tmp, "n2")
        rc2, out2 = run_helper(root, bad, right, d2)
        results.append(_line(helper_ok and bad_sha != zsha and rc2 not in (None, 0) and len(tree_files(d2)) == 0,
                             "N2 one changed byte inside a pyarrow member fails the sha gate",
                             "byte %d of the copy, inside %s; copy sha256 %s; rc=%s files %d %s"
                             % (at, member, bad_sha, rc2, len(tree_files(d2)), _tail(out2))))

        want = zip_entries(DEPLOYED_ZIP)
        d3 = os.path.join(tmp, "n3")
        for name, payload in want.items():
            ap = os.path.join(d3, name.replace("/", os.sep))
            os.makedirs(os.path.dirname(ap), exist_ok=True)
            with open(ap, "wb") as fh:
                fh.write(payload)
        eq_a, mis_a, miss_a, extra_a = compare(want, d3)
        victim = "pyarrow/libarrow.so.1601"
        vp = os.path.join(d3, victim.replace("/", os.sep))
        with open(vp, "r+b") as fh:
            fh.seek(os.path.getsize(vp) // 2)
            byte = fh.read(1)
            fh.seek(os.path.getsize(vp) // 2)
            fh.write(bytes([byte[0] ^ 0x01]))
        eq_b, mis_b, miss_b, extra_b = compare(want, d3)
        results.append(_line(eq_a == len(want) and not mis_a and mis_b == [victim] and eq_b == len(want) - 1,
                             "N3 the comparer reports the one flipped byte",
                             "before the flip %d of %d equal, mismatched %d; after it %d of %d equal, mismatched %s"
                             % (eq_a, len(want), len(mis_a), eq_b, len(want), mis_b)))

        small = os.path.join(tmp, "other-version.zip")
        other_version_zip(small)
        d4 = os.path.join(tmp, "n4")
        rc4, out4 = run_helper(root, small, b64_sha256(small), d4)
        results.append(_line(helper_ok and rc4 not in (None, 0) and len(tree_files(d4)) == 0,
                             "N4 a zip whose pyarrow dist-info is another version is refused, its sha being right",
                             "rc=%s files %d %s" % (rc4, len(tree_files(d4)), _tail(out4))))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return _verdict("AC2", results)


def logical_lines(text):
    """[(first line number, joined text)] with backslash continuations joined; comment lines dropped."""
    out, buf, start = [], "", 0
    for i, raw in enumerate(text.splitlines(), 1):
        if not buf:
            start = i
        if raw.rstrip().endswith("\\"):
            buf += raw.rstrip()[:-1] + " "
            continue
        buf += raw
        if not buf.lstrip().startswith("#"):
            out.append((start, buf))
        buf = ""
    return out


def shell_vars(text):
    """{NAME: value} of every column-0 NAME="value" or NAME=value assignment, later ones winning."""
    found = {}
    for m in re.finditer(r'^([A-Z_][A-Z0-9_]*)=(?:"([^"\n]*)"|([^\s"\n]*))$', text, re.M):
        found[m.group(1)] = m.group(2) if m.group(2) is not None else m.group(3)
    return found


def expand(value, env, depth=0):
    if depth > 8:
        return value
    out = re.sub(r"\$\{?([A-Z_][A-Z0-9_]*)\}?", lambda m: env.get(m.group(1), m.group(0)), value)
    return out if out == value else expand(out, env, depth + 1)


PIP_DOWNLOAD = re.compile(r"(?:^|[\s;&|!])python[\w.]*\s+-m\s+pip\s+download\b|(?:^|[\s;&|!])pip[\d.]*\s+download\b")


def helper_imports(path):
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.add((node.module or "").split(".")[0])
    return names


def ac3(root):
    results = []
    script = os.path.join(root, SCRIPT.replace("/", os.sep))
    with open(script, encoding="utf-8") as fh:
        text = fh.read()
    env = shell_vars(text)
    lines = logical_lines(text)

    pins = set(expand(env.get("VENDOR_PINS", ""), env).split())
    results.append(_line(pins == PURE_PINS, "C1 VENDOR_PINS expands to exactly the five pure pins",
                         "%d pin(s) %s; beyond the five %s; of the five absent %s"
                         % (len(pins), sorted(pins), sorted(pins - PURE_PINS), sorted(PURE_PINS - pins))))

    downloads = [(n, expand(ln, env)) for n, ln in lines
                 if PIP_DOWNLOAD.search(ln) and not ln.lstrip().startswith("echo")]
    platform = [(n, ln) for n, ln in downloads if "--platform" in ln]
    dirty = [n for n, ln in platform if any(t in ln.lower() for t in TWO)]
    results.append(_line(len(platform) >= 1 and not dirty,
                         "C2 no pip download that names --platform names pyarrow or rpds",
                         "pip download commands %d at lines %s; with --platform %d; of those naming one of the two %s"
                         % (len(downloads), [n for n, _ in downloads], len(platform), dirty)))

    def first(pattern):
        hits = [n for n, ln in lines if re.search(pattern, ln)]
        return hits[0] if hits else None

    need_zip = first(r"\$\{AMGT_DEPLOYED_ZIP:\?")
    read_sha = first(r"get-function-configuration.*CodeSha256")
    call = [(n, ln) for n, ln in lines if "vendor_from_deployed.py" in ln and "--expect-sha256=" in ln]
    call_at = call[0][0] if call else None
    excl = bool(call) and "MSYS2_ARG_CONV_EXCL=" in call[0][1]
    first_dl = downloads[0][0] if downloads else None
    order = None not in (need_zip, read_sha, call_at, first_dl) and read_sha < call_at < first_dl
    results.append(_line(bool(order and excl),
                         "C3 the script requires the zip, reads the live CodeSha256 and calls the helper before any pip download",
                         "AMGT_DEPLOYED_ZIP required at line %s; CodeSha256 read at line %s; helper called at line %s "
                         "(MSYS2_ARG_CONV_EXCL on the call: %s); first pip download at line %s"
                         % (need_zip, read_sha, call_at, excl, first_dl)))

    tokens = [(t.strip(), n) for n, ln in lines for t in FETCH_TOKENS if t in ln]
    helper = os.path.join(root, HELPER.replace("/", os.sep))
    if os.path.isfile(helper):
        imports = helper_imports(helper)
        net = sorted(imports & NETWORK_MODULES)
        helper_detail = "helper imports %s, network modules among them %s" % (sorted(imports), net)
        helper_clean = not net
    else:
        helper_detail = "the helper %s does not exist" % HELPER
        helper_clean = False
    results.append(_line(not tokens and helper_clean, "C4 no other fetch route in the script or the helper",
                         "fetch tokens in the script %s; %s" % (tokens, helper_detail)))

    m = re.search(r"^VENDOR_PRUNE\s*=\s*(\([^)]*\))", text, re.M)
    prune = ast.literal_eval(m.group(1)) if m else None
    names = sorted(zip_entries(DEPLOYED_ZIP))
    removed = [n for n in names if prune and any(x in ("/" + n) for x in prune)]
    results.append(_line(prune is not None and not removed,
                         "C5 the script's prune list removes nothing from the deployed four folders",
                         "VENDOR_PRUNE %s; removed %d of %d %s" % (prune, len(removed), len(names), removed[:3])))

    pack = [(n, ln) for n, ln in lines if re.search(r'python\s+-\s+"\$ROOT"\s+"\$ZIP"\s+"\$WHEELS"', ln)]
    handed = bool(pack) and '"$FROM_DEPLOYED"' in pack[0][1]
    old_count = "expected exactly 2 admitted native wheels" in text
    results.append(_line(handed and not old_count,
                         "C7 the packaging step is handed the filled folder and no longer demands two native wheels",
                         "packaging step at line %s, handed $FROM_DEPLOYED: %s; the two-native-wheels refusal still in the text: %s"
                         % (pack[0][0] if pack else None, handed, old_count)))

    sys.path.insert(0, os.path.join(root, ".tools"))
    from git_bash_resolver import git_bash

    bash = git_bash()
    if bash:
        p = subprocess.run([bash, "-n", SCRIPT], cwd=root, capture_output=True, text=True)
        results.append(_line(p.returncode == 0, "C6 bash -n on the script exits 0",
                             "rc=%d %s" % (p.returncode, _tail(p.stderr))))
    else:
        results.append(_line(False, "C6 bash -n on the script exits 0", "no Git Bash found"))
    return _verdict("AC3", results)


def compare_zip(new_zip):
    """Not a criterion. The four folders of a BUILT zip against the deployed zip's, entry by entry."""
    want = zip_entries(DEPLOYED_ZIP)
    have = zip_entries(new_zip)
    equal = sum(1 for n in want if have.get(n) == want[n])
    mismatched = sorted(n for n in want if n in have and have[n] != want[n])
    missing = sorted(n for n in want if n not in have)
    extra = sorted(n for n in have if n not in want)
    ok = equal == len(want) and not mismatched and not missing and not extra
    print("%s Z1 the four folders of %s equal the deployed zip's byte for byte %d of %d equal; mismatched %d, "
          "missing %d, extra %d %s" % ("PASS" if ok else "FAIL", new_zip, equal, len(want), len(mismatched),
                                       len(missing), len(extra), (mismatched + missing + extra)[:3]))
    print("R78 BB23 COMPARE-ZIP EQUAL: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"))
    ap.add_argument("--compare-zip", default=None)
    a = ap.parse_args()
    if a.compare_zip:
        return compare_zip(a.compare_zip)
    if not a.crit:
        ap.error("one of --crit or --compare-zip is required")
    root = _root()
    return {"AC1": ac1, "AC2": ac2, "AC3": ac3}[a.crit](root)


if __name__ == "__main__":
    sys.exit(main())
