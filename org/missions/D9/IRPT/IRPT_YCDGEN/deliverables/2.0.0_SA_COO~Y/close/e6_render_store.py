"""IRPT_YCDGEN E6 (issuer close act): render one live run's Opal Overview from its kept answers, store it beside them, and
print a short-lived signed link. Laptop, issuer only. OS temp only; every temp file is deleted.

    python e6_render_store.py <REQ-id> [--firm cottonwood] [--expires 3600]

1. Reads the run record and every kept answer it names from the firm's store (read-only), into a temp dir.
2. Copies the held risk-free object (layout_overview.RISK_FREE_SOURCE) into the temp dir.
3. Runs layout_overview.main: the Opal-held rows are read live, read-only, by its loader; the PDF and the finished run
   record are written to the temp dir.
4. Puts the PDF at the run record's report key (opal_naming builder output, layout_overview._report_key) and the
   finished run record at the run's own key; reads both back and compares sha256.
5. Prints the report's key, sha256, pages, the run's clocks, and ONE presigned GET link (C-DELIVERY: printed to the
   issuer's terminal only, never written to a file).
No figure value, ticker or amount is printed. ASCII only.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 8))
RESEARCH = os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting", "ycharts", "research")
AWS = os.path.join(ROOT, ".tools", "aws.cmd")
for p in (RESEARCH, os.path.join(RESEARCH, "..", "session"), os.path.join(RESEARCH, "..", "generate"),
          os.path.join(ROOT, "lib")):
    sys.path.insert(0, p)
import runner  # noqa: E402
import layout_overview  # noqa: E402


def aws(*args):
    out = subprocess.run([AWS, *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit("ERROR: aws %s rc=%d %s" % (" ".join(args[:2]), out.returncode, out.stderr.strip()[-300:]))
    return out.stdout


def s3_get(bucket, key, path):
    aws("s3", "cp", "s3://%s/%s" % (bucket, key), path, "--only-show-errors", "--region", "us-east-1")


def s3_put(path, bucket, key, content_type):
    aws("s3", "cp", path, "s3://%s/%s" % (bucket, key), "--only-show-errors", "--region", "us-east-1",
        "--content-type", content_type)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("request")
    ap.add_argument("--firm", default="cottonwood")
    ap.add_argument("--expires", type=int, default=3600)
    a = ap.parse_args(argv)
    bucket, run_key = runner.run_location(a.firm, a.request)
    tmp = tempfile.mkdtemp(prefix="irpt_e6_")
    try:
        run_path = os.path.join(tmp, "run.json")
        s3_get(bucket, run_key, run_path)
        run_doc = json.load(open(run_path, encoding="utf-8"))
        kept_dir = os.path.join(tmp, "kept")
        os.makedirs(kept_dir)
        for c in run_doc["calls"]:
            s3_get(bucket, c["key"], os.path.join(kept_dir, "%02d.json" % c["step"]))
        rf_bucket, rf_rest = layout_overview.RISK_FREE_SOURCE.split("/", 1)
        rf_key = rf_rest.split("#", 1)[0]
        rf_path = os.path.join(tmp, "risk_free.json")
        s3_get(rf_bucket, rf_key, rf_path)
        map_path = os.path.join(ROOT, "org", "missions", "D9", "IRPT", "IRPT_YCDGEN", "deliverables", "maps",
                                "overview_map.json")
        pdf_path, run_out = os.path.join(tmp, "overview.pdf"), os.path.join(tmp, "run_final.json")
        rc = layout_overview.main(["--run", run_path, "--kept", kept_dir, "--map", map_path, "--out", pdf_path,
                                   "--run-out", run_out, "--risk-free", rf_path])
        if rc != 0:
            raise SystemExit("ERROR: layout_overview rc=%s" % rc)
        final = json.load(open(run_out, encoding="utf-8"))
        report_key = final["report"]["key"]
        s3_put(pdf_path, bucket, report_key, "application/pdf")
        s3_put(run_out, bucket, run_key, "application/json")
        back_pdf, back_run = os.path.join(tmp, "back.pdf"), os.path.join(tmp, "back_run.json")
        s3_get(bucket, report_key, back_pdf)
        s3_get(bucket, run_key, back_run)
        ok = sha(back_pdf) == final["report"]["sha256"] and sha(back_run) == sha(run_out)
        states = {}
        for e in final.get("elements", []):
            st = (e.get("computed") or {}).get("status")
            if st:
                states[st] = states.get(st, 0) + 1
        print("REPORT key=%s sha256=%s pages=%s read_back_equal=%s" % (report_key, final["report"]["sha256"],
                                                                      final["report"]["pages"], ok))
        print("CLOCKS %s" % json.dumps(final.get("clocks"), sort_keys=True))
        print("COMPUTED element states %s" % json.dumps(states, sort_keys=True))
        url = aws("s3", "presign", "s3://%s/%s" % (bucket, report_key), "--expires-in", str(a.expires),
                  "--region", "us-east-1").strip()
        print("LINK (expires in %d s; terminal only): %s" % (a.expires, url))
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        print("temp removed: %s" % (not os.path.exists(tmp)))


if __name__ == "__main__":
    sys.exit(main())
