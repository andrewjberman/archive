#!/usr/bin/env python3
"""check_bucket_of_round11 -- LGIC_BLANKFIX round 11, cell BF-z-1 (0.9.0_WK_LGIC_BLANKFIX~1).

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~1/check_bucket_of_round11.py

  1. reads the four lines of HOLES_OWNED_round10.md that begin `OWNED ` and name owner 1.0.0_SA_CTO (the key, and the real
     lambda source file each cites);
  2. finds each key's line in its real file and runs bucket_of on it twice: BEFORE (lib/opal_naming_keyfill.py as it stood at the
     base of the round, read from git by the pin below) and AFTER (the module in this worktree);
  3. copies infra/logic/registry/ to a temporary folder, merges the drafted rows of REGISTRY_ROWS_round10.json (`_cite`
     stripped) for those keys into the copy's key_rulings.json, and asks the root check's own match rule
     (opal_naming_rootcheck._ruling_of) which row answers each key, with the BEFORE reader and with the AFTER reader;
  4. runs the negative arm: a file that shows several bucket candidates and whose use picks none still reads None, the
     candidates listed.

One line per key (bucket before -> after, the row matched before and after), then the last line:
  BUCKET-OF ok=<bool> keys=4 right=N rows_kept=N negative_held=<bool>
right = keys whose AFTER bucket is the bucket the code uses (the bucket of the row drafted or held for it); rows_kept = keys whose
row matches after and did not before. Nothing in the repository is written. Python 3.9; ASCII only.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.check_output(["git", "-C", HERE, "rev-parse", "--show-toplevel"]).decode("ascii").strip()
os.chdir(REPO)
sys.path.insert(0, os.path.join(REPO, "lib"))

import opal_naming  # noqa: E402
import opal_naming_keyfill as after_kf  # noqa: E402
import opal_naming_rootcheck as rc  # noqa: E402

BASE_PIN = "32c925520c"  # the round-11 base: lib/opal_naming_keyfill.py as the five reads of round 10 saw it
OWNED = os.path.join(HERE, "..", "0.9.0_WK_LGIC_BLANKFIX~2", "HOLES_OWNED_round10.md")
ROWS = os.path.join(HERE, "..", "0.9.0_WK_LGIC_BLANKFIX~2", "REGISTRY_ROWS_round10.json")


def load_before(tmp):
    src = subprocess.check_output(["git", "show", "%s:lib/opal_naming_keyfill.py" % BASE_PIN]).decode("utf-8")
    path = os.path.join(tmp, "opal_naming_keyfill_before.py")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("opal_naming_keyfill_before", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def owned_keys():
    out = []
    with open(OWNED, encoding="utf-8") as fh:
        for ln in fh:
            if not ln.startswith("OWNED ") or "|| 1.0.0_SA_CTO ||" not in ln:
                continue
            m = re.match(r"OWNED (\S+) \|\| S3Key (\S+) \|\|", ln)
            f = re.search(r"(infra/aws/lambda/\S+?\.py):(\d+)", ln)
            if not m or not f:
                raise SystemExit("BUCKET-OF ok=False reason=unreadable OWNED line: %s" % ln[:80])
            out.append((m.group(1), m.group(2), f.group(1), int(f.group(2))))
    return out


def key_line(path, key, cited):
    with open(os.path.join(REPO, *path.split("/")), encoding="utf-8") as fh:
        for n, ln in enumerate(fh, 1):
            if key in ln and not ln.lstrip().startswith("#"):
                return n
    return cited


def main():
    problems = []
    keys = owned_keys()
    tmp = tempfile.mkdtemp(prefix="bucket_of_r11_")
    try:
        before = load_before(tmp)
        reg = os.path.join(tmp, "registry")
        shutil.copytree(opal_naming.REGISTRY_DIR, reg)
        kr_path = os.path.join(reg, "key_rulings.json")
        with open(kr_path, "rb") as fh:
            kr = json.loads(fh.read().decode("utf-8"))
        with open(ROWS, "rb") as fh:
            drafted = json.loads(fh.read().decode("utf-8"))["key_rulings.json"]
        wanted = set(k for _r, k, _p, _n in keys)
        have = set((r.get("bucket"), r.get("key")) for r in kr["key_rulings"])
        merged = 0
        for r in drafted:
            if r["key"] in wanted and (r["bucket"], r["key"]) not in have:
                kr["key_rulings"].append(dict((k, v) for k, v in r.items() if k != "_cite"))
                merged += 1
        with open(kr_path, "wb") as fh:
            fh.write((json.dumps(kr, indent=1) + "\n").encode("utf-8"))
        refusals, _warn = opal_naming.validate(reg)
        if refusals:
            problems.append("registry copy refused: %s" % (refusals[:2],))
        rulings = rc.load_key_rulings(kr_path)
        right = kept = 0
        for root, key, path, cited in keys:
            ln = key_line(path, key, cited)
            item = {"plane": "repo", "type": "S3Key", "current": key, "where": "%s:%d" % (path, ln)}
            b0, _w0 = before.bucket_of(item)
            b1, w1 = after_kf.bucket_of(item)
            rows_for = [r for (_b, k), r in rulings.items() if k == key]
            code_bucket = rows_for[0].get("bucket") if len(rows_for) == 1 else None
            r0 = rc._ruling_of(item, rulings, bucket_reader=before.bucket_of)[0]
            r1 = rc._ruling_of(item, rulings, bucket_reader=after_kf.bucket_of)[0]
            is_right = code_bucket is not None and b1 == code_bucket and b0 != code_bucket
            is_kept = r1 is not None and r0 is None
            right += 1 if is_right else 0
            kept += 1 if is_kept else 0
            print("KEY %s %s (%s:%d): %s -> %s | row before=%s after=%s" % (
                root, key, path.rsplit("/", 2)[-2], ln, b0, b1,
                "matched" if r0 else "none", "matched" if r1 else "none"))
            if not is_right:
                problems.append("%s: bucket %s -> %s, the row's bucket is %s" % (key, b0, b1, code_bucket))
            if not is_kept:
                problems.append("%s: the row does not newly match" % key)
        # the negative arm: several candidates, the key's use picks none -> None, the candidates listed
        neg = ("import boto3\n"
               "A_BUCKET = 'opal-data-astn'\n"
               "B_BUCKET = 'plain-artifacts-bucket-9'\n"
               "K = 'state/head.json'\n"
               "boto3.client('s3').get_object(Bucket=pick(), Key=K)\n"
               "boto3.client('s3').get_object(Bucket=B_BUCKET, Key='other')\n")
        nb, nwhy = after_kf.bucket_of({"current": "state/head.json", "where": "infra/aws/lambda/x/lambda_function.py:4"}, neg)
        negative_held = nb is None and "opal-data-astn" in nwhy and "plain-artifacts-bucket-9" in nwhy
        print("NEGATIVE: bucket=%s | %s" % (nb, nwhy))
        ok = (len(keys) == 4 and right == 4 and kept == 4 and negative_held and not problems)
        for p in problems:
            print("PROBLEM: " + p)
        print("BUCKET-OF ok=%s keys=%d right=%d rows_kept=%d negative_held=%s" % (ok, len(keys), right, kept, negative_held))
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
