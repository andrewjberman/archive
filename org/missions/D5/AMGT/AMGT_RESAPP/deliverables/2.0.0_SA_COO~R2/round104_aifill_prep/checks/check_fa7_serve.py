"""check_fa7_serve.py -- acceptance arms for AMGT-fa-7 (the serve: scoped_amgt.read_ai_fill and the /thesis bundle's `ai_fill`).

  PYTHONPATH=<repo root> python check_fa7_serve.py
Offline: AMGT_AIFILL_ROOT (a local directory) and a fake S3 client; no AWS, no network.
Writes its own fill documents by hand (it does not import lib.research.aifill, which this cell's base does not carry).
"""
from __future__ import annotations

import copy
import inspect
import io
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

KEY = "ASML_NA_Equity"
IDS = L.BLOCK_IDS


def block(block_id, source_class="OPAL_SOURCE"):
    if source_class == "NONE":
        return {"block_id": block_id, "source_class": "NONE", "machine_written": True, "text": None, "reason": "Nothing to fill.",
                "citations": [], "opal_inputs": [], "model_call": None}
    web = source_class == "WEB_SEARCH"
    cite = ({"source_kind": "web", "url": "https://a.example/x", "title": "T", "quote": "q", "ref": None} if web
            else {"source_kind": "opal", "url": None, "title": None, "quote": None, "ref": "Company officer list"})
    return {"block_id": block_id, "source_class": source_class, "machine_written": True, "text": "Plain text.", "reason": None,
            "citations": [cite], "opal_inputs": ["x"], "model_call": ({"model": "m", "web_search_requests": 1, "input_tokens": 1, "output_tokens": 1} if web else None)}


def document(key=KEY):
    blocks = {i: block(i) for i in IDS}
    blocks["mgmt_bio"] = block("mgmt_bio", "WEB_SEARCH")
    blocks["mgmt_team_view"] = block("mgmt_team_view", "NONE")
    return {"schema": "aifill/v1", "security_key": key, "as_of": "2026-10-13", "generated_at": "2026-10-13T12:00:00Z",
            "producer": {"version": "opal-aifill/1.0.0", "model": "claude-opus-5"}, "blocks": blocks}


class FakeS3:
    def __init__(self, body=None, error=None):
        self.body, self.error, self.calls = body, error, []

    def get_object(self, Bucket, Key):
        self.calls.append((Bucket, Key))
        if self.error:
            raise self.error
        return {"Body": io.BytesIO(self.body)}


def main():
    from lib.research.api import scoped_amgt as S
    from lib.research.harvest import store as hstore

    arms = L.Arms("FA-7")
    saved_root = os.environ.pop("AMGT_AIFILL_ROOT", None)

    def with_root(fn):
        with tempfile.TemporaryDirectory() as root:
            os.environ["AMGT_AIFILL_ROOT"] = root
            try:
                return fn(root)
            finally:
                os.environ.pop("AMGT_AIFILL_ROOT", None)

    def put(root, doc, key=KEY):
        from lib.research.identity import crosswalk
        with open(os.path.join(root, "%s.json" % crosswalk.slash_safe_key(key)), "w", encoding="utf-8") as handle:
            json.dump(doc, handle)

    def served_local():
        def go(root):
            doc = document()
            put(root, doc)
            r = S.read_ai_fill(KEY)
            return (r["status"] == "SERVED" and r["source"] == "local" and r["read_completed"] is True and r["reason"] is None
                    and r["as_of"] == "2026-10-13" and r["generated_at"] == "2026-10-13T12:00:00Z" and r["blocks"] == doc["blocks"]
                    and r["producer"] == doc["producer"] and set(r) >= {"status", "reason", "source", "read_completed", "as_of", "generated_at", "producer", "blocks"}), sorted(r)
        return with_root(go)
    arms.run("a valid local document is SERVED whole (blocks unchanged)", served_local)

    def absent_local():
        def go(root):
            r = S.read_ai_fill(KEY)
            return r["status"] == "ABSENT" and r["read_completed"] is True and r["blocks"] == {} and r["source"] == "none" and r["reason"] and r["as_of"] is None, r
        return with_root(go)
    arms.run("no document -> ABSENT, read completed, blocks {}", absent_local)

    def unreadable_local():
        def go(root):
            from lib.research.identity import crosswalk
            with open(os.path.join(root, "%s.json" % crosswalk.slash_safe_key(KEY)), "w", encoding="utf-8") as handle:
                handle.write("{not json")
            r = S.read_ai_fill(KEY)
            return r["status"] == "ABSENT" and r["read_completed"] is False and r["blocks"] == {} and "parse" in r["reason"].lower(), r["reason"]
        return with_root(go)
    arms.run("an unparseable document -> ABSENT with read_completed False (not 'nobody has filled it')", unreadable_local)

    def invalid_cases():
        def mutate(label, fn):
            def go(root):
                doc = document()
                fn(doc)
                put(root, doc)
                r = S.read_ai_fill(KEY)
                return label, r["status"] == "INVALID" and r["blocks"] == {} and r["reason"] and r["read_completed"] is True
            return with_root(go)
        cases = [
            ("schema", lambda d: d.update({"schema": "aifill/v0"})),
            ("missing block", lambda d: d["blocks"].pop("thesis_pillars")),
            ("web block without citations", lambda d: d["blocks"]["mgmt_bio"].update({"citations": []})),
            ("web block without a url", lambda d: d["blocks"]["mgmt_bio"]["citations"][0].update({"url": None})),
            ("text without machine_written", lambda d: d["blocks"]["mgmt_recent"].update({"machine_written": False})),
            ("NONE block carrying text", lambda d: d["blocks"]["mgmt_team_view"].update({"text": "x"})),
            ("unknown source class", lambda d: d["blocks"]["mgmt_recent"].update({"source_class": "GUESS"})),
            ("key of another security", lambda d: d.update({"security_key": "OTHER_US_Equity"})),
        ]
        bad = [label for label, ok in (mutate(name, fn) for name, fn in cases) if not ok]
        return not bad, bad
    arms.run("each broken document -> INVALID, blocks {} (nothing half-served)", invalid_cases)

    def unresolved():
        r = S.read_ai_fill(None)
        return r["status"] == "ABSENT" and "UNRESOLVED" in r["reason"] and r["blocks"] == {} and r["read_completed"] is True, r
    arms.run("identity UNRESOLVED (key None) -> ABSENT naming it, no read", unresolved)

    def pool_read():
        fake = FakeS3(body=json.dumps(document()).encode("utf-8"))
        real = S._s3_client
        S._s3_client = lambda: fake
        try:
            r = S.read_ai_fill(KEY)
        finally:
            S._s3_client = real
        uri = hstore.address_of("amgt", "gold", "ai_fill", hstore.entity_partition("security_key", KEY), object_name="ai_fill.json")
        bucket, _, key = uri[len("s3://"):].partition("/")
        return r["status"] == "SERVED" and r["source"] == "pool" and fake.calls == [(bucket, key)], (fake.calls, uri)
    arms.run("pool read: one get_object at exactly the naming builder's address", pool_read)

    def pool_slash_key():
        fake = FakeS3(body=json.dumps(document("BP/_LN_Equity")).encode("utf-8"))
        real = S._s3_client
        S._s3_client = lambda: fake
        try:
            S.read_ai_fill("BP/_LN_Equity")
        finally:
            S._s3_client = real
        uri = hstore.address_of("amgt", "gold", "ai_fill", hstore.entity_partition("security_key", "BP/_LN_Equity"), object_name="ai_fill.json")
        return fake.calls == [tuple(uri[len("s3://"):].split("/", 1))], fake.calls
    arms.run("pool read: a slash key uses the builder's encoded partition", pool_slash_key)

    def pool_missing():
        class NoSuchKey(Exception):
            pass
        fake = FakeS3(error=NoSuchKey("The specified key does not exist."))
        real = S._s3_client
        S._s3_client = lambda: fake
        try:
            r = S.read_ai_fill(KEY)
        finally:
            S._s3_client = real
        return r["status"] == "ABSENT" and r["read_completed"] is True and r["source"] == "none", r
    arms.run("pool NoSuchKey -> ABSENT, read completed", pool_missing)

    def pool_failure():
        fake = FakeS3(error=RuntimeError("AccessDenied"))
        real = S._s3_client
        S._s3_client = lambda: fake
        try:
            r = S.read_ai_fill(KEY)
        finally:
            S._s3_client = real
        return r["status"] == "ABSENT" and r["read_completed"] is False and "AccessDenied" in r["reason"], r
    arms.run("pool failure -> ABSENT, read_completed False, reason names it", pool_failure)

    def pool_one_read_only():
        fake = FakeS3(body=json.dumps(document()).encode("utf-8"))
        real = S._s3_client
        S._s3_client = lambda: fake
        try:
            S.read_ai_fill(KEY)
        finally:
            S._s3_client = real
        return len(fake.calls) == 1 and not hasattr(fake, "list_objects_v2"), len(fake.calls)
    arms.run("one object GET per name, no LIST (the cold-start budget)", pool_one_read_only)

    def wired_in_thesis():
        src = inspect.getsource(S.read_thesis_bundle)
        return "read_ai_fill(" in src and ("ai_fill" in src), "not wired"
    arms.run("read_thesis_bundle serves the result under the key 'ai_fill'", wired_in_thesis)

    def overlay_untouched():
        users = []
        for name, fn in inspect.getmembers(S, inspect.isfunction):
            if "overlay" in name.lower() and "read_ai_fill(" in inspect.getsource(fn):
                users.append(name)
        return not users, users
    arms.run("no overlay function calls read_ai_fill (the overlay's handler time is not touched)", overlay_untouched)

    def no_typed_address():
        import ast
        tree = ast.parse(open(S.__file__, "r", encoding="utf-8").read())
        typed = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and ("gold/ai_fill" in n.value or "harvest/gold" in n.value)]
        return not typed, typed
    arms.run("scoped_amgt.py types no ai_fill address literal (rule 30)", no_typed_address)

    def prefix_constant():
        from lib.research.api import _harvest_prefixes as hp
        return getattr(hp, "AI_FILL_GOLD_PREFIX", None) == hstore.table_prefix("amgt", "gold", "ai_fill"), getattr(hp, "AI_FILL_GOLD_PREFIX", None)
    arms.run("_harvest_prefixes.AI_FILL_GOLD_PREFIX equals the builder's table prefix", prefix_constant)

    def generated_module_imports_nothing():
        import ast
        from lib.research.api import _harvest_prefixes as hp
        tree = ast.parse(open(hp.__file__, "r", encoding="utf-8").read())
        return not [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))], "the generated module must hold constants only"
    arms.run("the generated prefixes module still imports nothing", generated_module_imports_nothing)

    def serve_does_not_import_naming_or_store():
        import ast
        tree = ast.parse(open(S.__file__, "r", encoding="utf-8").read())
        bad = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                bad += [a.name for a in node.names if a.name.startswith(("lib.opal_naming", "lib.research.harvest.store"))]
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if mod.startswith(("lib.opal_naming", "lib.research.harvest.store")) or (mod == "lib" and any(a.name == "opal_naming" for a in node.names)) \
                        or (mod == "lib.research.harvest" and any(a.name == "store" for a in node.names)):
                    bad.append(mod)
        return not bad, bad
    arms.run("scoped_amgt.py imports neither lib.opal_naming nor harvest.store (Lambda-safe)", serve_does_not_import_naming_or_store)

    def env_name():
        return hasattr(S, "ENV_AIFILL_ROOT") and S.ENV_AIFILL_ROOT == "AMGT_AIFILL_ROOT", getattr(S, "ENV_AIFILL_ROOT", None)
    arms.run("ENV_AIFILL_ROOT == 'AMGT_AIFILL_ROOT'", env_name)

    def not_mutating():
        def go(root):
            doc = document()
            before = copy.deepcopy(doc)
            put(root, doc)
            S.read_ai_fill(KEY)
            return doc == before
        return with_root(go)
    arms.run("serving does not alter the stored document", not_mutating)

    if saved_root is not None:
        os.environ["AMGT_AIFILL_ROOT"] = saved_root
    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
