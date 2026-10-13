"""check_fa6_store_run.py -- acceptance arms for AMGT-fa-6 (the store address/IO and the run command).

  PYTHONPATH=<repo root> python check_fa6_store_run.py
Offline: a fake S3 client, no AWS. Needs the whole package of cells fa-1, fa-2, fa-3, fa-4, fa-5 merged (the base this cell is cut from).
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402


class FakeS3:
    def __init__(self, objects=None):
        self.objects = dict(objects or {})
        self.puts = []

    def put_object(self, **kw):
        self.puts.append(kw)
        self.objects[(kw["Bucket"], kw["Key"])] = kw["Body"]
        return {"ETag": "x"}

    def get_object(self, Bucket, Key):
        if (Bucket, Key) not in self.objects:
            err = type("NoSuchKey", (Exception,), {})("not found")
            raise err
        return {"Body": io.BytesIO(self.objects[(Bucket, Key)])}


def main():
    from lib.research.aifill import contract, orchestrate, run, store
    from lib.research.harvest import store as hstore

    arms = L.Arms("FA-6")
    KEY = "ASML_NA_Equity"

    def expected_uri(key):
        return hstore.address_of("amgt", "gold", "ai_fill", hstore.entity_partition("security_key", key), object_name="ai_fill.json")

    def address_ok():
        uri = store.address_for(KEY)
        bucket, _, key = uri[len("s3://"):].partition("/")
        return uri == expected_uri(KEY) and uri.startswith("s3://opal-data-harvest/amgt/harvest/gold/ai_fill/") and key.endswith("/ai_fill.json"), uri
    arms.run("address_for equals the naming builder's output (gold/ai_fill)", address_ok)

    def address_slash():
        return store.address_for("BP/_LN_Equity") == expected_uri("BP/_LN_Equity") and "BP/_LN" not in store.address_for("BP/_LN_Equity").split("ai_fill/")[1], store.address_for("BP/_LN_Equity")
    arms.run("a slash in the security key is encoded by the builder, never split", address_slash)

    def no_typed_address():
        src = open(store.__file__, "r", encoding="utf-8").read()
        return "harvest/gold" not in src and "ai_fill/" not in src.replace("ai_fill.json", ""), "typed address literal"
    arms.run("store.py types no address literal (rule 30)", no_typed_address)

    def good_doc():
        return orchestrate.build_document(KEY, {"overlay": None, "thesis": None, "errors": {}}, lambda *a, **k: None, now=L.NOW,
                                          builders={i: (lambda c, i=i: contract.make_block(i, "OPAL_SOURCE", "Text.", [{"source_kind": "opal", "ref": "Company officer list", "url": None, "title": None, "quote": None}])) for i in L.BLOCK_IDS})

    def write_ok():
        s3 = FakeS3()
        receipt = store.write_document(good_doc(), client=s3)
        put = s3.puts[0]
        body = put["Body"]
        text = body.decode("utf-8") if isinstance(body, bytes) else body
        uri = expected_uri(KEY)
        return (len(s3.puts) == 1 and "s3://%s/%s" % (put["Bucket"], put["Key"]) == uri and put["ContentType"] == "application/json"
                and text.isascii() and json.loads(text)["security_key"] == KEY and isinstance(receipt, dict) and receipt.get("uri") == uri), (put["Bucket"], put["Key"])
    arms.run("write_document puts ASCII JSON at the builder address and returns a receipt", write_ok)

    def write_refuses_invalid():
        s3 = FakeS3()
        doc = good_doc()
        doc["schema"] = "wrong"
        try:
            store.write_document(doc, client=s3)
        except contract.ContractError:
            return not s3.puts, "put happened"
        return False, "no refusal"
    arms.run("write_document refuses an invalid document before any put", write_refuses_invalid)

    def read_ok():
        s3 = FakeS3()
        doc = good_doc()
        store.write_document(doc, client=s3)
        back = store.read_document(KEY, client=s3)
        return back == doc, "round trip differs"
    arms.run("read_document round-trips what was written", read_ok)

    def read_absent():
        return store.read_document(KEY, client=FakeS3()) is None, "absent should be None"
    arms.run("read_document of a missing object is None (not an error)", read_absent)

    def read_other_error():
        class Boom(FakeS3):
            def get_object(self, Bucket, Key):
                raise RuntimeError("access denied")
        try:
            store.read_document(KEY, client=Boom())
        except RuntimeError:
            return True
        return False, "swallowed"
    arms.run("read_document does not swallow a non-missing error", read_other_error)

    # ------------------------------------------------------------------ run
    def run_cli(args, extra_env=None):
        env = dict(os.environ)
        env.pop("ANTHROPIC_API_KEY", None)
        env.update(extra_env or {})
        return subprocess.run([sys.executable, "-m", "lib.research.aifill.run"] + args, capture_output=True, text=True, env=env, timeout=120)

    served = os.path.join(L.FIXTURES, "served_inputs_ASML_NA_Equity.json")

    def cli_no_model():
        with tempfile.TemporaryDirectory() as out:
            p = run_cli(["--key", KEY, "--inputs-file", served, "--no-model", "--out", out])
            path = os.path.join(out, "%s.json" % KEY)
            doc = json.load(open(path, "r", encoding="utf-8")) if os.path.exists(path) else None
            lines = p.stdout.strip().splitlines()
            summary = [ln for ln in lines if ln.startswith("AIFILL RUN:")]
            blocks = [ln for ln in lines if ln.startswith("BLOCK ")]
            return (p.returncode == 0 and doc is not None and contract.validate_document(doc) == [] and len(blocks) == 5 and len(summary) == 1
                    and "document=VALID" in summary[0] and "blocks=5" in summary[0] and open(path, "rb").read().isascii()), (p.returncode, p.stderr[-200:], summary)
    arms.run("run --no-model --inputs-file --out writes a valid ASCII document", cli_no_model)

    def cli_census_line():
        with tempfile.TemporaryDirectory() as out:
            p = run_cli(["--key", KEY, "--inputs-file", served, "--no-model", "--out", out])
            summary = [ln for ln in p.stdout.splitlines() if ln.startswith("AIFILL RUN:")][0]
            import re
            m = re.search(r"\(OPAL (\d+) WEB (\d+) NONE (\d+)\)", summary)
            return bool(m) and sum(int(g) for g in m.groups()) == 5, summary
    arms.run("the summary line prints OPAL/WEB/NONE counts summing to 5", cli_census_line)

    def cli_no_model_means_no_call():
        with tempfile.TemporaryDirectory() as out:
            p = run_cli(["--key", KEY, "--inputs-file", served, "--no-model", "--out", out], {"ANTHROPIC_API_KEY": "must-not-be-used"})
            doc = json.load(open(os.path.join(out, "%s.json" % KEY), "r", encoding="utf-8"))
            web_blocks = [b for b in doc["blocks"].values() if b["source_class"] == "WEB_SEARCH"]
            return p.returncode == 0 and not web_blocks, [b["block_id"] for b in web_blocks]
    arms.run("--no-model makes no model call even with a key in the environment", cli_no_model_means_no_call)

    def cli_needs_key():
        with tempfile.TemporaryDirectory() as out:
            p = run_cli(["--key", KEY, "--inputs-file", served, "--out", out])
            return p.returncode != 0 and "ANTHROPIC_API_KEY" in (p.stdout + p.stderr), (p.returncode, (p.stdout + p.stderr)[-160:])
    arms.run("run without --no-model and without a key stops naming ANTHROPIC_API_KEY", cli_needs_key)

    def cli_slash_key_file():
        with tempfile.TemporaryDirectory() as out:
            p = run_cli(["--key", "BP/_LN_Equity", "--inputs-file", served, "--no-model", "--out", out])
            names = os.listdir(out)
            return p.returncode == 0 and len(names) == 1 and "/" not in names[0] and names[0].endswith(".json"), names
    arms.run("a slash key writes one slash-safe file name", cli_slash_key_file)

    def main_dry_run():
        s3 = FakeS3()
        buf = io.StringIO()
        real = sys.stdout
        sys.stdout = buf
        try:
            with tempfile.TemporaryDirectory() as out:
                rc = run.main(["--key", KEY, "--inputs-file", served, "--no-model", "--out", out, "--to-s3"], client=s3)
        finally:
            sys.stdout = real
        text = buf.getvalue()
        return rc == 0 and not s3.puts and "DRY-RUN" in text and expected_uri(KEY) in text, text[-200:]
    arms.run("--to-s3 alone is a DRY-RUN: prints the address, writes nothing", main_dry_run)

    def main_confirmed():
        s3 = FakeS3()
        buf = io.StringIO()
        real = sys.stdout
        sys.stdout = buf
        try:
            with tempfile.TemporaryDirectory() as out:
                rc = run.main(["--key", KEY, "--inputs-file", served, "--no-model", "--out", out, "--to-s3", "--confirm-write"], client=s3)
        finally:
            sys.stdout = real
        return rc == 0 and len(s3.puts) == 1 and "s3://%s/%s" % (s3.puts[0]["Bucket"], s3.puts[0]["Key"]) == expected_uri(KEY), buf.getvalue()[-200:]
    arms.run("--to-s3 --confirm-write puts exactly one object at the builder address", main_confirmed)

    def invalid_never_written():
        s3 = FakeS3()
        real_validate = contract.validate_document
        contract.validate_document = lambda doc: ["forced problem"]
        buf = io.StringIO()
        real = sys.stdout
        sys.stdout = buf
        try:
            with tempfile.TemporaryDirectory() as out:
                rc = run.main(["--key", KEY, "--inputs-file", served, "--no-model", "--out", out, "--to-s3", "--confirm-write"], client=s3)
        finally:
            sys.stdout = real
            contract.validate_document = real_validate
        return rc != 0 and not s3.puts, (rc, buf.getvalue()[-160:])
    arms.run("an invalid document is never written to S3 (exit non-zero)", invalid_never_written)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
