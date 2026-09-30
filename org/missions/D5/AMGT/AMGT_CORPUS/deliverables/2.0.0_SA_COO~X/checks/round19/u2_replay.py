"""AMGT_CORPUS round 19, CRPS-u-2 -- replay Hitachi's unit-map build at HEAD against the PRE-Hitachi map (ead621d685^1) in a
temp file, through build_unit_map's own CLI (S3 raw reads only, no vendor call), and compare with the committed map at
ead621d685 (the CTO-ruled Hitachi-only delta). Read-only on the repo; the issuer's file.

  -> 'u2 replay rc R shared_changed C shared_removed D type_changed T hitachi_reproduced H of N non6501_added X'
"""
import importlib.util
import json
import os
import subprocess
import tempfile
from pathlib import Path

REF = "ead621d685"
FM = "integrations/bloomberg/research/field_map.json"


def at(ref):
    return json.loads(subprocess.run(["git", "show", "%s:%s" % (ref, FM)], capture_output=True, text=True,
                                     encoding="utf-8").stdout)


base, ref = at(REF + "^1"), at(REF)
spec = importlib.util.spec_from_file_location("bum", "integrations/bloomberg/research/build_unit_map.py")
bum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bum)
d = tempfile.mkdtemp(prefix="u2_replay_")
tmp = Path(d) / "field_map.json"
tmp.write_text(json.dumps(base, indent=2, default=str), encoding="utf-8")
bum.FIELD_MAP_PATH = tmp
try:
    rc = bum.main(["--securities", "6501 JP Equity"])
except SystemExit as e:
    rc = e.code if isinstance(e.code, int) else 1
out = json.loads(tmp.read_text(encoding="utf-8"))
tmp.unlink()
os.rmdir(d)

H = "6501"


def key_of(e):
    if isinstance(e, dict):
        for k in ("mnemonic", "security", "security_key"):
            if k in e:
                return "%s=%s" % (k, e[k])
    return json.dumps(e, sort_keys=True)


def diff(a, b, p, acc):
    """Structural diff; LIST elements are matched by identity (mnemonic / security / value), never by position."""
    if type(a) is not type(b):
        acc["type"].append(p)
        return
    if isinstance(a, dict):
        for k in a:
            if k not in b:
                acc["removed"].append(p + "/" + k)
            else:
                diff(a[k], b[k], p + "/" + k, acc)
        for k in b:
            if k not in a:
                acc["added"].append(p + "/" + k)
    elif isinstance(a, list):
        ka = {key_of(e): e for e in a}
        kb = {key_of(e): e for e in b}
        for k in ka:
            if k not in kb:
                acc["removed"].append(p + "[" + k + "]")
            else:
                diff(ka[k], kb[k], p + "[" + k + "]", acc)
        for k in kb:
            if k not in ka:
                acc["added"].append(p + "[+" + k + "]")
    elif a != b:
        acc["changed"].append(p)


def run(x, y):
    acc = {"changed": [], "removed": [], "type": [], "added": []}
    diff(x, y, "", acc)
    return acc


got, want = run(base, out), run(base, ref)
reproduced = sum(1 for x in want["added"] if x in set(got["added"]))
non6501 = sum(1 for x in got["added"] if H not in x)
print("u2 replay rc %s shared_changed %d shared_removed %d type_changed %d hitachi_reproduced %d of %d non6501_added %d" % (
    rc, len(got["changed"]), len(got["removed"]), len(got["type"]), reproduced, len(want["added"]), non6501))
