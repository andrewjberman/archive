"""IB-pr-389 offline replay of a runner bundle on the real inputs, ONE bundle per process. AWS READS ONLY. Run with python -I.

Usage:
  python -I replay_runner_drop.py run <extracted_bundle_dir> <scratch_dir> <label> <fire date YYYY-MM-DD> [firms comma list]
      drives the bundle's OWN directory_runner.run_firm per firm, three arms, and writes <scratch>/runner_<label>.json (counts, booleans and
      hashes only: no id, no name):
        real    -- the real source snapshot, previous = the SERVED directory, upload=False (nothing is put): the landing's canonical hash
                   (payload without generated_at).
        drop    -- the same, but the BUILD loses one entry the source still holds (the builder wrapped to omit it), upload=True through the
                   runner's real land() with boto3 swapped for a put-counting fake only for that call. Records refused / puts.
        removal -- negative control: the same entry is gone from the build AND from the source keys (a vendor removal). Must land, carried
                   TERMINATED, in every bundle.
  python -I replay_runner_drop.py compose <scratch_dir> <out.json> <pin> <built_label> <live_label>[,<live_label>...]
      compares each live label against the built label per firm and writes the arms file.
"""
import datetime as dt
import hashlib
import json
import os
import sys
import types


def canon(payload):
    p = {k: v for k, v in payload.items() if k != "generated_at"}
    return hashlib.sha256(json.dumps(p, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()


def run_mode(tree, scratch, label, now, firms):
    sys.path.insert(0, os.path.join(tree, "data", "assets", "scripts", "gold", "investor_reporting"))
    import boto3  # noqa: E402
    import directory_runner as dr  # noqa: E402
    assert os.path.abspath(dr.__file__).startswith(os.path.abspath(tree)), "runner resolved outside the bundle"
    real_s3 = boto3.client("s3", region_name="us-east-1")
    buckets = dr.firm_bucket_map()
    orig_builder = dict(dr.BUILDERS)
    orig_ids = dr.source_client_ids
    orig_land = dr.land

    def loader(bucket, prefix, key):
        return dr.read_previous_served(bucket, prefix, key, s3=real_s3)

    class Counting:
        def __init__(self):
            self.puts = []

        def put_object(self, Bucket, Key, Body, **kw):
            self.puts.append(Key)
            self.body = Body
            self.last = (Bucket, Key)
            self.objs = getattr(self, "objs", {})
            self.objs[Key] = Body

        def head_object(self, Bucket, Key):
            return {"ContentLength": len(self.objs[Key]), "ETag": '"x"'}

    def counted_land(fake):
        def _land(*a, **k):
            saved = sys.modules["boto3"]
            sys.modules["boto3"] = types.SimpleNamespace(client=lambda *x, **y: fake)
            try:
                return orig_land(*a, **k)
            finally:
                sys.modules["boto3"] = saved
        return _land

    out = {"label": label, "now": now, "runner_sha256_of_file": hashlib.sha256(open(dr.__file__, "rb").read()).hexdigest(), "firms": {}}
    for firm in firms:
        rec = {}
        try:
            res = dr.run_firm({"firm_id": firm}, buckets, qa=False, upload=False, local_out=None, explicit=None,
                              now=dt.date.fromisoformat(now), previous_loader=loader)
        except Exception as exc:  # noqa: BLE001 -- classified, never echoed
            out["firms"][firm] = {"error": type(exc).__name__ + ": " + str(exc)[:160]}
            continue
        p = res["payload"]
        cf = res["carried_forward"]
        rec["real"] = {"business_date": res["business_date"], "entry_count": res["entry_count"], "entries_valid": res["entries_valid"],
                       "validation_errors": len(res["validation_errors"]), "canonical_sha256": canon(p),
                       "source_client_ids": len(p.get("source_client_ids") or []), "carried_terminated": cf["terminated"],
                       "held_in_source": cf["held_in_source"], "refused": bool(cf.get("refused")),
                       "previous_as_of": cf.get("previous_as_of")}
        prev = loader(buckets[firm], dr.PROD_PREFIX, None)
        prev_keys = {dr.entry_key(e) for e in prev["payload"]["entries"] if dr.entry_key(e)}
        src_ids = set(p.get("source_client_ids") or [])
        cands = sorted({dr.entry_key(e) for e in p["entries"] if dr.entry_key(e)} & prev_keys & src_ids)
        if not cands:
            rec["victim"] = None
            out["firms"][firm] = rec
            continue
        victim = cands[0]
        rec["victim_selected"] = True

        def wrapped(fn):
            def _b(data, bd, rev):
                entries, census = fn(data, bd, rev)
                return [e for e in entries if dr.entry_key(e) != victim], census
            return _b

        for arm in ("drop", "removal"):
            fake = Counting()
            dr.BUILDERS[firm] = wrapped(orig_builder[firm])
            if arm == "removal":
                dr.source_client_ids = lambda f, d: [i for i in orig_ids(f, d) if i != victim]
            dr.land = counted_land(fake)
            try:
                r = dr.run_firm({"firm_id": firm}, buckets, qa=False, upload=True, local_out=None, explicit=None,
                                now=dt.date.fromisoformat(now), previous_loader=loader)
                landed = json.loads(fake.objs[r["landed"]["key"]].decode("utf-8")) if r["landed"]["key"] in fake.objs else {}
                marked = [e for e in landed.get("entries", []) if dr.entry_key(e) == victim
                          and (e.get("termination") or {}).get("indicator") == "TERMINATED"]
                rec[arm] = {"refused": False, "puts": len(fake.puts), "entry_count": r["entry_count"],
                            "victim_in_landed": any(dr.entry_key(e) == victim for e in landed.get("entries", [])),
                            "victim_landed_terminated": bool(marked), "carried_terminated": r["carried_forward"]["terminated"],
                            "held_in_source": r["carried_forward"]["held_in_source"]}
            except RuntimeError as exc:
                msg = str(exc)
                rec[arm] = {"refused": True, "puts": len(fake.puts), "reason": msg.split(":")[1].strip() if "BUILD_DROPS" in msg else msg[:80],
                            "names_victim_id": victim in msg, "names_other_id": any(c in msg for c in cands[1:6])}
            finally:
                dr.BUILDERS[firm] = orig_builder[firm]
                dr.source_client_ids = orig_ids
                dr.land = orig_land
        out["firms"][firm] = rec
    with open(os.path.join(scratch, "runner_%s.json" % label), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({f: {a: (v.get("refused"), v.get("puts")) for a, v in r.items() if isinstance(v, dict) and "refused" in v}
                      for f, r in out["firms"].items() if isinstance(r, dict)}))


def compose_mode(scratch, out_path, pin, built_label, live_labels):
    load = lambda lb: json.load(open(os.path.join(scratch, "runner_%s.json" % lb), encoding="utf-8"))  # noqa: E731
    built = load(built_label)
    arms = []
    for lb in live_labels:
        live = load(lb)
        for firm, b in built["firms"].items():
            lv = live["firms"].get(firm, {})
            if "error" in b or "error" in lv:
                arms.append({"name": "real_%s_%s_vs_built" % (firm, lb), "verdict": "expected-diff", "negative_control": False,
                             "detail": "NOT REPLAYED: built=%r live=%r" % (b.get("error"), lv.get("error"))})
                continue
            same_real = b["real"] == lv["real"]
            arms.append({"name": "real_%s_%s_vs_built" % (firm, lb), "verdict": "identical" if same_real else "expected-diff",
                         "negative_control": False,
                         "detail": "real source + served previous, nothing dropped: entry_count %s/%s, canonical landing hash %s/%s (without generated_at), held %s/%s, carried %s/%s"
                         % (lv["real"]["entry_count"], b["real"]["entry_count"], lv["real"]["canonical_sha256"][:12], b["real"]["canonical_sha256"][:12],
                            lv["real"]["held_in_source"], b["real"]["held_in_source"], lv["real"]["carried_terminated"], b["real"]["carried_terminated"])})
            if "drop" not in b:
                arms.append({"name": "drop_%s_%s_vs_built" % (firm, lb), "verdict": "expected-diff", "negative_control": False,
                             "detail": "no entry both in the served directory and in the source: fixture not constructible"})
                continue
            bd, ld = b["drop"], lv["drop"]
            ok_b = bd["refused"] and bd["puts"] == 0 and bd.get("names_victim_id") and not bd.get("names_other_id")
            same = bd == ld
            arms.append({"name": "drop_%s_%s_vs_built" % (firm, lb), "verdict": "identical" if same else "expected-diff", "negative_control": False,
                         "detail": "fixture: one entry the source still holds is dropped from the build. built: refused=%s puts=%s reason=%s names_only_the_dropped_id=%s. %s: refused=%s puts=%s%s"
                         % (bd["refused"], bd["puts"], bd.get("reason"), bool(bd.get("names_victim_id")) and not bd.get("names_other_id"), lb, ld["refused"], ld["puts"],
                            "" if ld["refused"] else " victim_in_landed=%s" % ld.get("victim_in_landed")) + ("" if ok_b else " ** BUILT DID NOT REFUSE WITH 0 PUTS **")})
            br, lr = b["removal"], lv["removal"]
            same_r = br == lr
            arms.append({"name": "genuine_removal_%s_%s_vs_built" % (firm, lb), "verdict": "identical" if same_r else "expected-diff", "negative_control": True,
                         "detail": "NEGATIVE CONTROL: the entry is gone from the build AND the source (a vendor removal): built refused=%s puts=%s victim_landed_terminated=%s carried=%s; %s refused=%s puts=%s victim_landed_terminated=%s carried=%s"
                         % (br["refused"], br["puts"], br.get("victim_landed_terminated"), br.get("carried_terminated"), lb, lr["refused"], lr["puts"],
                            lr.get("victim_landed_terminated"), lr.get("carried_terminated"))})
    doc = {"pin": pin, "to_id": "IRPT_BCKEND.TO-IB-pr-389", "built_label": built_label, "live_labels": live_labels,
           "method": "each bundle extracted into its own directory and driven by replay_runner_drop.py (python -I) on the real source snapshots and "
                     "real served directories (AWS reads only); the writing arms run the runner's own land() with boto3 swapped for a put-counting fake, "
                     "so nothing is put anywhere.", "arms": arms}
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print("wrote", out_path, len(arms), "arms")


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run_mode(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], (sys.argv[6] if len(sys.argv) > 6 else "inflection,cottonwood,49financial").split(","))
    else:
        compose_mode(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6].split(","))
