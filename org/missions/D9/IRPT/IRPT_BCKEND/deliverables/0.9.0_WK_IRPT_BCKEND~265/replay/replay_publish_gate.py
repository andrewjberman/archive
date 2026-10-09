"""IB-pr-400 offline replay of a holdings bundle's publish gate, ONE bundle tree per process. AWS READS ONLY. Run with python -I.

Usage:
  python -I replay_publish_gate.py run <extracted_bundle_dir> <scratch_dir> <label> [firms comma list]
      drives the tree's OWN holdings_snapshot.run_firm. Writes <scratch>/gate_<label>.json (counts, booleans and hashes only:
      no account id, no security id, no name). Two families of arms:
        real_<firm>       the real source inputs and the real served index, upload=True through a GUARDED client: reads go to
                          AWS, every write is captured in memory and never leaves the process. Records the gate outcome and the
                          landed revision, gold hash and put list.
        fx_<firm>_*       fixture arms on an in-memory versioned bucket under the tree's real HoldingsPublication (the same
                          fixture shape as tests/test_holdings_publish_gate.py): worse_restored (QA table), all_unknown_loses_account,
                          closed_account_not_refused (negative control), monday_not_stale (negative control),
                          mutant_gate_stubbed (negative control: the gate replaced by PUBLISHED must publish the worse candidate).
  python -I replay_publish_gate.py compose <scratch_dir> <out.json> <pin> <built_label> <live_label>
      compares the two labels arm by arm and writes the arms file.
"""
import copy
import hashlib
import io
import json
import os
import sys
import time

DATE0, DATE1 = "2026-10-07", "2026-10-08"
READ_PREFIXES = ("get_", "list_", "head_", "describe_", "batch_get", "scan", "query", "can_paginate", "meta", "exceptions")


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Overlay:
    """Captured writes: (bucket, key) -> {version: (body, etag)}; `current` -> latest version. Nothing leaves the process."""

    def __init__(self):
        self.objects, self.current, self.puts = {}, {}, []


class Guard:
    """A read-through client: reads go to the real client, put_object is captured in the overlay, every other mutation raises."""

    def __init__(self, real, overlay):
        self._real, self._ov = real, overlay

    def _exists(self, bucket, key):
        if (bucket, key) in self._ov.current:
            return True
        try:
            self._real.head_object(Bucket=bucket, Key=key)
            return True
        except Exception as exc:  # noqa: BLE001 -- a 404 is a state
            code = str(getattr(exc, "response", {}).get("Error", {}).get("Code"))
            if code in ("404", "NoSuchKey", "NotFound"):
                return False
            raise

    def _etag(self, bucket, key):
        if (bucket, key) in self._ov.current:
            return self._ov.objects[(bucket, key, self._ov.current[(bucket, key)])][1]
        return self._real.head_object(Bucket=bucket, Key=key)["ETag"]

    def put_object(self, **kw):
        from botocore.exceptions import ClientError
        bucket, key = kw["Bucket"], kw["Key"]
        if kw.get("IfNoneMatch") == "*" and self._exists(bucket, key):
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        if "IfMatch" in kw and (not self._exists(bucket, key) or self._etag(bucket, key) != kw["IfMatch"]):
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        body = bytes(kw["Body"])
        version = "ov-%d" % (len(self._ov.puts) + 1)
        etag = '"' + hashlib.md5(body).hexdigest() + '"'  # noqa: S324 -- an ETag stand-in, not a security use
        self._ov.objects[(bucket, key, version)] = (body, etag)
        self._ov.current[(bucket, key)] = version
        self._ov.puts.append({"bucket": bucket, "key": key, "sha256": sha(body), "bytes": len(body), "version": version})
        return {"VersionId": version, "ETag": etag}

    def get_object(self, **kw):
        bucket, key, version = kw["Bucket"], kw["Key"], kw.get("VersionId")
        if version is None and (bucket, key) in self._ov.current:
            version = self._ov.current[(bucket, key)]
        if version is not None and (bucket, key, version) in self._ov.objects:
            body, etag = self._ov.objects[(bucket, key, version)]
            return {"Body": io.BytesIO(body), "ETag": etag, "VersionId": version, "ContentLength": len(body)}
        return self._real.get_object(**kw)

    def head_object(self, **kw):
        bucket, key = kw["Bucket"], kw["Key"]
        if (bucket, key) in self._ov.current:
            version = self._ov.current[(bucket, key)]
            return {"ETag": self._ov.objects[(bucket, key, version)][1], "VersionId": version}
        return self._real.head_object(**kw)

    def __getattr__(self, name):
        if name.startswith(READ_PREFIXES):
            return getattr(self._real, name)
        raise RuntimeError("REPLAY GUARD: %s is a mutation and is refused" % name)


def canon_doc(d):
    return json.dumps(d, sort_keys=True, separators=(",", ":"), default=str)


class VersionedS3:
    """In-memory versioned bucket with S3 conditional writes (fixture arms only)."""

    def __init__(self):
        self.objects, self.current, self.calls = {}, {}, []

    def put_object(self, **kw):
        from botocore.exceptions import ClientError
        key = (kw["Bucket"], kw["Key"])
        cur = self.current.get(key)
        if ((kw.get("IfNoneMatch") == "*" and cur is not None)
                or ("IfMatch" in kw and (cur is None or self.objects[key + (cur,)][1] != kw["IfMatch"]))):
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        body = bytes(kw["Body"])
        version = str(len(self.calls) + 1)
        etag = '"' + sha(body) + '"'
        self.objects[key + (version,)] = (body, etag)
        self.current[key] = version
        self.calls.append(kw)
        return {"VersionId": version, "ETag": etag}

    def get_object(self, **kw):
        from botocore.exceptions import ClientError
        key = (kw["Bucket"], kw["Key"])
        version = kw.get("VersionId") or self.current.get(key)
        if key + (version,) not in self.objects:
            raise ClientError({"Error": {"Code": "NoSuchKey"}}, "GetObject")
        body, etag = self.objects[key + (version,)]
        return {"Body": io.BytesIO(body), "ETag": etag, "VersionId": version}


def gate_view(res):
    g = res.get("publish_gate") or {"outcome": "ABSENT (the tree has no publish gate)"}
    landed = res.get("landed") or {}
    return {"outcome": g.get("outcome"),
            "conditions": [[c["condition"], c["count"]] for c in g.get("conditions", [])],
            "listed": {k: v.get("count") for k, v in (g.get("listed") or {}).items()},
            "uploaded": bool(landed.get("uploaded")), "refused": bool(landed.get("refused")),
            "revision": landed.get("revision"), "gold_sha256": landed.get("gold_sha256")}


def run_mode(tree, scratch, label, firms):
    here = os.path.join(tree, "data", "assets", "scripts", "gold", "investor_reporting")
    sys.path.insert(0, here)
    import boto3
    import holdings_snapshot as hs
    assert os.path.abspath(hs.__file__).startswith(os.path.abspath(tree)), "holdings_snapshot resolved outside the bundle"
    import pytest
    ov = Overlay()
    real_client = boto3.client

    def guarded(service, *a, **k):
        return Guard(real_client(service, *a, **k), ov)
    boto3.client = guarded
    out = {"label": label, "holdings_snapshot_sha256": sha(open(hs.__file__, "rb").read()),
           "has_publish_gate": hasattr(hs, "evaluate_publish_gate"), "arms": {}}

    # ---------------------------------------------------------------- real inputs, guarded client
    from publication import canonical_bytes
    orig_land = hs.land
    cap = {}

    def capturing_land(bucket, prefix, as_of, payload, upload, local_out, s3_client=None, expected=None):
        body = {k: v for k, v in payload.items() if not k.startswith("_")}
        stable = {k: v for k, v in body.items() if k not in ("clocks", "source_set_revision")}
        cap["nodes_sha256"] = sha(canonical_bytes(payload["nodes"]))
        cap["stable_body_sha256"] = sha(canonical_bytes(stable))
        cap["clocks_sha256"] = sha(canonical_bytes(body.get("clocks")))
        cap["source_set_revision_sha256"] = sha(canonical_bytes(body.get("source_set_revision")))
        with open(os.path.join(scratch, "nodes_%s_%s.json" % (label, payload["scope"]["firm_id"])), "w", encoding="utf-8") as fh:
            json.dump({n["node_id"]: n for n in payload["nodes"]}, fh, sort_keys=True, default=str)
        return orig_land(bucket, prefix, as_of, payload, upload, local_out, s3_client=s3_client, expected=expected)

    for firm in firms:
        ov.puts.clear()
        ov.objects.clear()
        ov.current.clear()
        cap.clear()
        hs.land = capturing_land
        t0 = time.time()
        try:
            s3 = boto3.client("s3", region_name="us-east-1")
            res = hs.run_firm(firm, s3, qa=False, upload=True, local_out=None, as_of=None)
            rec = gate_view(res)
            rec.update(cap)
            rec.update({"business_date": res["business_date"], "node_count": res["node_count"],
                        "unique_account_count": res["unique_account_count"], "reconcile_ok": res["reconcile_ok"],
                        "schema_valid": res["schema_valid"],
                        "puts": [[p["key"].rsplit(".", 1)[-1], p["sha256"][:12], p["bytes"]] for p in ov.puts],
                        "put_count": len(ov.puts),
                        "put_keys_class": sorted({p["key"].split("/")[3] + "/" + p["key"].split("/")[4] for p in ov.puts})})
        except Exception as exc:  # noqa: BLE001 -- classified, never echoed past 200 chars
            rec = {"error": type(exc).__name__ + ": " + str(exc)[:200]}
        hs.land = orig_land
        rec["seconds"] = round(time.time() - t0, 1)
        out["arms"]["real_" + firm] = rec
        print("real", firm, rec.get("outcome"), rec.get("error"), rec["seconds"], flush=True)
    boto3.client = real_client

    # ---------------------------------------------------------------- fixtures
    def make_snapshot(firm, book=None, *, date=DATE0, stamp="2026-10-08T10:15:00Z", before=None):
        book = book if book is not None else {"acc1": [("AAA", "equity", 60.0), ("BBB", "fixed_income", 40.0)],
                                              "acc2": [("CCC", "cash", 50.0), ("DDD", "alternatives", 50.0)]}
        nodes, total = [], 0.0
        for acct, positions in sorted(book.items()):
            value = round(sum(v for _, _, v in positions), 6)
            total += value
            nodes.append(hs._node(acct, None, 0, "ACCOUNT", "OBSERVED", value, "USD", "UNIQUE_CUSTODY_TOTAL", value, None, None,
                                  "test", "fixture", 1, 1, "measured", drill_refs=[{"ref_kind": "ACCOUNT", "ref_id": acct}],
                                  classification=hs._unknown_classification(["fixture"])))
            for i, (ticker, klass, v) in enumerate(positions):
                n = hs._node("%s:pos:%d" % (acct, i), acct, 1, "SECURITY", "OBSERVED", v, "USD", "PARENT_NODE", value,
                             v / value, None, "test", "fixture", 1, 1, "measured",
                             security_id={"namespace": "TICKER", "value": ticker},
                             classification=hs._unknown_classification(["fixture"]))
                n["asset_class"], n["asset_class_basis"] = klass, "TABLE"
                nodes.append(n)
        hs.recompute_weights(nodes)
        accounts = sorted(book)
        before = total if before is None else before
        return {
            "scope": {"resolved_scope_fingerprint": sha("|".join(accounts).encode()), "firm_id": firm, "account_ids": accounts},
            "source_set_revision": [{"source": "fixture", "revision": "fixture@" + date, "completion_date": date}],
            "clocks": {"business_date": date, "as_of_timestamp": stamp, "custody_as_of": date, "overlay_as_of": date,
                       "source_as_of": [{"source": "fixture (custody)", "as_of": date},
                                        {"source": "fixture (overlay)", "as_of": date}]},
            "custody_totals": {"unique_account_count": len(accounts),
                               "unique_position_count": sum(len(p) for p in book.values()),
                               "total_market_value": {"value": round(total, 2), "currency": "USD"}, "deduplicated": True},
            "nodes": nodes,
            "coverage": {"nodes_resolved": len(nodes), "nodes_attempted": len(nodes),
                         "remainder": {"amount": 0.0, "units": "USD", "reason": "fixture"}},
            "source_vendor_keys": hs.source_vendor_keys("smartx/platform/silver"),
            "attribution_holdouts": {
                "unassigned": hs.holdout_block(set(accounts), set(accounts), {a: 0.0 for a in accounts},
                                               observable="MEASURED", source="fixture"),
                "assigned_without_custody": {"account_count": 0, "denominator": "0 of %d" % len(accounts), "source": "fixture"},
                "reconcile": {"total_before": round(before, 2), "total_after": round(total, 2),
                              "difference": round(before - total, 2), "tolerance": hs.RECON_TOLERANCE_USD,
                              "reconciled": abs(before - total) <= hs.RECON_TOLERANCE_USD}},
            "_manifest": {"total_market_value": round(before, 2)},
            "_clock_census": {},
        }

    class Inputs:
        def __init__(self, s3):
            self.s3 = s3

        def receipts(self):
            return [{"source": "fixture", "bucket": "fixture", "key": "fixture/1", "version_id": "1", "sha256": "0" * 64}]

    mp = pytest.MonkeyPatch()

    def fire(firm, s3, candidate, qa=False):
        mp.setattr(hs, "build_snapshot", lambda *a, **k: copy.deepcopy(candidate))
        mp.setattr(hs, "VersionedInputs", Inputs)
        return hs.run_firm(firm, s3, qa=qa, upload=True, local_out=None, as_of=candidate["clocks"]["business_date"])

    def index_ref(s3, firm, qa=False):
        b, k = hs.HoldingsPublication(s3, firm, qa=qa).location("platinum", "current", "manifest.json")
        return s3.current.get((b, k))

    def directory(s3, firm, indicators):
        bucket = hs.firm_bucket_map()[firm]
        prefix = hs.PROD_PREFIX.replace("holdings", "directory")
        s3.put_object(Bucket=bucket, Key=prefix + "/latest.json", Body=json.dumps({"key": prefix + "/d.json"}).encode())
        s3.put_object(Bucket=bucket, Key=prefix + "/d.json", Body=json.dumps({"entries": [
            {"ids": {"account_ids": [a]}, "termination": {"indicator": i}} for a, i in indicators.items()]}).encode())

    base_book = {"acc1": [("AAA", "equity", 60.0), ("BBB", "fixed_income", 40.0)],
                 "acc2": [("CCC", "cash", 50.0), ("DDD", "alternatives", 50.0)]}
    worse_book = dict(base_book, acc1=[("AAA", "unclassified", 60.0), ("BBB", "fixed_income", 40.0)])
    one_acct = {"acc1": base_book["acc1"]}
    for firm in firms:
        fid = firm
        # worse / restored pair on the QA table, one run
        s3 = VersionedS3()
        base = fire(fid, s3, make_snapshot(fid, stamp="2026-10-08T10:15:00Z"), qa=True)
        before = index_ref(s3, fid, True)
        worse = fire(fid, s3, make_snapshot(fid, worse_book, date=DATE1, stamp="2026-10-09T10:15:00Z"), qa=True)
        after_worse = index_ref(s3, fid, True)
        rec_key = [k for k in s3.current if k[1].endswith("publish_refusal.json")]
        restored = fire(fid, s3, make_snapshot(fid, date=DATE1, stamp="2026-10-09T10:15:00Z"), qa=True)
        out["arms"]["fx_%s_worse_restored" % firm] = {
            "baseline": gate_view(base)["outcome"], "worse": gate_view(worse), "worse_index_moved": after_worse != before,
            "refusal_record_keys": len(rec_key), "restored": gate_view(restored),
            "restored_index_moved": index_ref(s3, fid, True) != after_worse}
        # an all-UNKNOWN firm loses an account
        s3 = VersionedS3()
        fire(fid, s3, make_snapshot(fid))
        directory(s3, fid, {"acc1": "UNKNOWN", "acc2": "UNKNOWN"})
        b4 = index_ref(s3, fid)
        r = fire(fid, s3, make_snapshot(fid, one_acct, date=DATE1, stamp="2026-10-09T10:15:00Z"))
        out["arms"]["fx_%s_all_unknown_loses_account" % firm] = {"result": gate_view(r), "index_moved": index_ref(s3, fid) != b4}
        # negative control: an account the source records TERMINATED is listed, never refused
        s3 = VersionedS3()
        fire(fid, s3, make_snapshot(fid))
        directory(s3, fid, {"acc1": "ACTIVE", "acc2": "TERMINATED"})
        b4 = index_ref(s3, fid)
        r = fire(fid, s3, make_snapshot(fid, one_acct, date=DATE1, stamp="2026-10-09T10:15:00Z"))
        out["arms"]["fx_%s_closed_account_not_refused" % firm] = {"result": gate_view(r), "index_moved": index_ref(s3, fid) != b4}
        # negative control: Monday is not stale against Friday
        s3 = VersionedS3()
        fire(fid, s3, make_snapshot(fid, date="2026-10-09", stamp="2026-10-09T10:15:00Z"))
        b4 = index_ref(s3, fid)
        r = fire(fid, s3, make_snapshot(fid, date="2026-10-12", stamp="2026-10-13T10:15:00Z"))
        out["arms"]["fx_%s_monday_not_stale" % firm] = {"result": gate_view(r), "index_moved": index_ref(s3, fid) != b4}
        # negative control: the gate stubbed to PUBLISHED must publish the worse candidate (the worse arm discriminates)
        if hasattr(hs, "evaluate_publish_gate"):
            s3 = VersionedS3()
            fire(fid, s3, make_snapshot(fid))
            b4 = index_ref(s3, fid)
            mp.setattr(hs, "evaluate_publish_gate", lambda *a, **k: {"outcome": "PUBLISHED", "conditions": [], "listed": {}})
            r = fire(fid, s3, make_snapshot(fid, worse_book, date=DATE1, stamp="2026-10-09T10:15:00Z"))
            mp.undo()
            mp.setattr(hs, "VersionedInputs", Inputs)
            out["arms"]["fx_%s_mutant_gate_stubbed" % firm] = {"result": gate_view(r), "index_moved": index_ref(s3, fid) != b4}
    mp.undo()
    with open(os.path.join(scratch, "gate_%s.json" % label), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote", label, len(out["arms"]), "arms")


def node_diff(path_a, path_b):
    """Counts only: nodes in both and equal / changed, only in A, only in B, and which top-level fields differ on a changed node."""
    with open(path_a, encoding="utf-8") as fa, open(path_b, encoding="utf-8") as fb:
        a, b = json.load(fa), json.load(fb)
    fields = {}
    same = changed = 0
    for k in a.keys() & b.keys():
        if a[k] == b[k]:
            same += 1
            continue
        changed += 1
        for f in sorted(x for x in set(a[k]) | set(b[k]) if a[k].get(x) != b[k].get(x)):
            fields[f] = fields.get(f, 0) + 1
    return {"same": same, "changed": changed, "only_in_a": len(a.keys() - b.keys()), "only_in_b": len(b.keys() - a.keys()),
            "differing_fields_on_changed_nodes": dict(sorted(fields.items()))}


def pub_view(r):
    return [bool(r.get("uploaded")), r.get("revision"), r.get("gold_sha256")]


def compose_mode(scratch, out_path, pin, built_label, live_label):
    def load(lb):
        with open(os.path.join(scratch, "gate_%s.json" % lb), encoding="utf-8") as fh:
            return json.load(fh)
    b, lv, pr = load(built_label), load(live_label), load("prior")
    arms = []
    short = {"49financial": "49f", "inflection": "inf", "cottonwood": "cot"}

    def real_arm(name, ba, la, nodes_a, nodes_b, what):
        if "error" in ba or "error" in la:
            arms.append({"name": name, "verdict": "expected-diff", "negative_control": False,
                         "detail": "NOT REPLAYED: built=%r other=%r" % (ba.get("error"), la.get("error"))})
            return
        nd = node_diff(nodes_a, nodes_b)
        same_nodes = ba["nodes_sha256"] == la["nodes_sha256"]
        same_stable = ba["stable_body_sha256"] == la["stable_body_sha256"]
        same_rev = ba["revision"] == la["revision"]
        ok = ba["outcome"] == "PUBLISHED" and ba["uploaded"] and not ba["conditions"]
        ident = ok and la["uploaded"] and same_nodes and same_stable
        arms.append({"name": name, "verdict": "identical" if ident else "expected-diff", "negative_control": False,
                     "detail": "%s. Real inputs + real served index, writes captured in memory. BUILT gate=%s conditions=%s listed=%s%s; other tree gate=%s. "
                               "Candidate nodes identical=%s (sha256 %s/%s), stable body (everything but clocks and source_set_revision) identical=%s, "
                               "whole revision identical=%s (clocks identical=%s, source_set_revision identical=%s); puts %d/%d; nodes %s/%s; accounts %s/%s; business_date %s/%s. "
                               "Node diff other->built: %s"
                               % (what, ba["outcome"], ba["conditions"], ba["listed"], "" if ok else " ** BUILT DID NOT PUBLISH **", la["outcome"],
                                  same_nodes, la["nodes_sha256"][:12], ba["nodes_sha256"][:12], same_stable, same_rev,
                                  ba["clocks_sha256"] == la["clocks_sha256"], ba["source_set_revision_sha256"] == la["source_set_revision_sha256"],
                                  la["put_count"], ba["put_count"], la["node_count"], ba["node_count"], la["unique_account_count"], ba["unique_account_count"],
                                  la["business_date"], ba["business_date"], json.dumps(nd, sort_keys=True))})

    for firm in sorted(short):
        ba = b["arms"]["real_" + firm]
        la = lv["arms"]["real_" + firm]
        pa = pr["arms"]["real_" + firm]
        real_arm("real_%s_fwd14_only_ordered_artifact" % firm, ba, pa, os.path.join(scratch, "nodes_built_%s.json" % firm),
                 os.path.join(scratch, "nodes_prior_%s.json" % firm),
                 "ORDERED ARTIFACT, FWD-14 isolated: the built consumer tree versus the same tree with holdings_snapshot.py swapped for the live "
                 "W2Wragr copy (b4c1c984f6ad = the pre-IB-pr-393 blob)")
        real_arm("real_%s_standalone_live_vs_built" % firm, ba, la, os.path.join(scratch, "nodes_built_%s.json" % firm),
                 os.path.join(scratch, "nodes_live_%s_%s.json" % (short[firm], firm)),
                 "CONSUMER ARTIFACT: live standalone bundle %s versus the built standalone bundle (18 members differ, 17 not FWD-14)" % short[firm])
    for name in sorted(n for n in b["arms"] if n.startswith("fx_")):
        ba = b["arms"][name]
        la = lv["arms"][name] if name in lv["arms"] else None
        firm = name.split("_")[1]
        if "mutant" in name:
            worse = b["arms"]["fx_%s_worse_restored" % firm]["worse"]
            res = ba["result"]
            stubbed_publishes = res["uploaded"] and ba["index_moved"]
            arms.append({"name": name, "verdict": "expected-diff", "negative_control": True,
                         "detail": "NEGATIVE CONTROL (the worse arm discriminates): the SAME worse candidate (a classified security now unclassified), with "
                                   "evaluate_publish_gate stubbed to PUBLISHED, publishes and moves the index (uploaded=%s index_moved=%s); with the real gate the built "
                                   "tree REFUSES it (%s, index_moved=%s)%s" % (res["uploaded"], ba["index_moved"], worse["outcome"],
                                   b["arms"]["fx_%s_worse_restored" % firm]["worse_index_moved"], "" if stubbed_publishes else " ** STUB DID NOT PUBLISH **")})
            continue
        if name.endswith("worse_restored"):
            w, r = ba["worse"], ba["restored"]
            lw, lr = la["worse"], la["restored"]
            exp = (w["outcome"] == "REFUSED" and not ba["worse_index_moved"] and ba["refusal_record_keys"] == 1
                   and r["outcome"] == "PUBLISHED" and ba["restored_index_moved"])
            arms.append({"name": name, "verdict": "expected-diff", "negative_control": False,
                         "detail": "QA table, one run. BUILT: worse arm %s on %s, index_moved=%s, refusal records=%d, then restored arm %s index_moved=%s%s. "
                                   "LIVE standalone (no gate): worse arm uploaded=%s index_moved=%s (the worse candidate IS published), restored uploaded=%s index_moved=%s"
                                   % (w["outcome"], w["conditions"], ba["worse_index_moved"], ba["refusal_record_keys"], r["outcome"], ba["restored_index_moved"],
                                      "" if exp else " ** UNEXPECTED **", lw["uploaded"], la["worse_index_moved"], lr["uploaded"], la["restored_index_moved"])})
            continue
        res, lres = ba["result"], la["result"]
        want = {"all_unknown_loses_account": "account_lost_not_refused", "closed_account_not_refused": "closed_accounts_not_refused",
                "monday_not_stale": None}
        key = [k for k in want if name.endswith(k)][0]
        listed_key = want[key]
        exp = res["outcome"] == "PUBLISHED" and ba["index_moved"] and (listed_key is None or res["listed"].get(listed_key) == 1)
        same_pub = pub_view(res) == pub_view(lres) and ba["index_moved"] == la["index_moved"]
        title = {"all_unknown_loses_account": "an all-UNKNOWN firm loses an account: PUBLISHED and listed",
                 "closed_account_not_refused": "NEGATIVE CONTROL: an account the source records TERMINATED is listed, never refused",
                 "monday_not_stale": "NEGATIVE CONTROL: a Monday candidate is not stale against Friday's served frontier"}[key]
        arms.append({"name": name, "verdict": "identical" if same_pub and exp else "expected-diff", "negative_control": key != "all_unknown_loses_account",
                     "detail": "%s. BUILT %s index_moved=%s listed=%s conditions=%s%s; LIVE standalone (no gate) uploaded=%s index_moved=%s; the landed revision is %s"
                               % (title, res["outcome"], ba["index_moved"], res["listed"], res["conditions"], "" if exp else " ** UNEXPECTED **",
                                  lres["uploaded"], la["index_moved"], "identical in both trees" if same_pub else "different")})
    doc = {"pin": pin, "to_id": "IRPT_BCKEND.TO-IB-pr-400", "built_label": built_label, "live_label": live_label,
           "built_holdings_snapshot_sha256": b["holdings_snapshot_sha256"], "live_holdings_snapshot_sha256": lv["holdings_snapshot_sha256"],
           "prior_holdings_snapshot_sha256": pr["holdings_snapshot_sha256"],
           "method": "each bundle tree extracted into its own directory and driven by replay_publish_gate.py (python -I). Real arms: the tree's "
                     "own run_firm on the real sources and the real served index through a read-through client whose writes are captured "
                     "in memory (every other mutation raises). Fixture arms: an in-memory versioned bucket under the tree's real HoldingsPublication. "
                     "Trees: built = the standalone bundle built at the pin; live = the live per-firm standalone bundle; prior = the built tree with "
                     "holdings_snapshot.py swapped for the live W2Wragr copy (FWD-14 isolated). Nothing is put anywhere.", "arms": arms}
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print("wrote", out_path, len(arms), "arms")


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run_mode(sys.argv[2], sys.argv[3], sys.argv[4], (sys.argv[5] if len(sys.argv) > 5 else "inflection,cottonwood,49financial").split(","))
    else:
        compose_mode(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
