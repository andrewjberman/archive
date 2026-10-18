"""AMGT_RESAPP round 115 (AMGT-bv-5 prep): the CANDIDATE pack and rich export for the eight names, from this checkout's own Lambda handler over the LIVE pool.

  PYTHONPATH=<repo root> python r115_local_candidate_capture.py <pack_outdir> <rich_outdir>

Read-only (the handler GETs the pool). Writes <pack_outdir>/<key>.txt (the PDF text, as r114_pack_capture_compare.py capture writes it) and
<rich_outdir>/<key>.md, so the issuer can run `compare` and `compare-rich` of the LIVE captures against them BEFORE the redeploy. The checkout
carries other merged rounds' members the live function does not, so only dates may be expected to differ; the compare says whether that held.
"""
import base64
import importlib.util
import os
import sys

os.environ.setdefault("AMGT_AIFILL_ROOT", "/var/empty/aifill-hold")
if os.environ.get("R117_AIFILL_LIVE") == "1":  # round 117: the live function has no AMGT_AIFILL_ROOT and reads the ai_fill object from S3; a candidate that is to show the machine-written passages must run the same way
    os.environ.pop("AMGT_AIFILL_ROOT", None)
sys.path.insert(0, ".")
import fitz  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("lam", "infra/aws/lambda/research/scoped_amgt_api/lambda_function.py")
lam = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lam)
if os.environ.get("R117_AIFILL_LIVE") == "1":
    os.environ.pop("AMGT_AIFILL_ROOT", None)
cmp_spec = importlib.util.spec_from_file_location("cmpmod", os.path.join(HERE, "r114_pack_capture_compare.py"))
cmpmod = importlib.util.module_from_spec(cmp_spec)
cmp_spec.loader.exec_module(cmpmod)


def _call(key, fmt):
    ev = {"rawPath": "/api/scoped/amgt/security/%s/print" % key, "queryStringParameters": {"format": fmt},
          "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = lam.lambda_handler(ev, None)
    return r


def main(argv):
    pack_dir, rich_dir = argv[1], argv[2]
    os.makedirs(pack_dir, exist_ok=True)
    os.makedirs(rich_dir, exist_ok=True)
    bad = 0
    for key in cmpmod.NAMES:
        for fmt, d, ext in (("pdf", pack_dir, "txt"), ("rich", rich_dir, "md")):
            r = _call(key, fmt)
            if r.get("statusCode") != 200:
                print("%s %s status %s" % (key, fmt, r.get("statusCode")))
                bad += 1
                continue
            body = r.get("body") or ""
            if fmt == "pdf":
                raw = base64.b64decode(body) if r.get("isBase64Encoded") else body.encode("latin-1")
                text = "\n".join(p.get_text() for p in fitz.open(stream=raw, filetype="pdf"))
            else:
                text = base64.b64decode(body).decode("utf-8") if r.get("isBase64Encoded") else body
            open("%s/%s.%s" % (d, key, ext), "w", encoding="utf-8", newline="\n").write(text)
        print("%s done" % key)
    print("LOCAL CANDIDATE CAPTURE: %d request(s) not 200" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
