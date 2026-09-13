#!/usr/bin/env python3
"""
POSN_ASTTAX.TO-T4-1 / cell AT3-s-4 / T4-AC3 -- the simulated re-seed control.

WHAT IS SIMULATED AND WHAT IS NOT:
  The TARGET is an in-process scratch store -- a plain dict, rebuilt per arm. There is
  no network client anywhere in this process: `boto3` is replaced in sys.modules BEFORE the
  seeder source is executed, and every arm asserts the replacement is still in place
  afterwards. The live etf-classifications table is never opened, read or written by this
  script.
  The SEEDER and the MODULE are real bytes, not re-implementations: the OLD arm executes
  `git show HEAD:...` bytes dumped to .scratch/head/, the NEW arm executes the worktree
  bytes. That is the whole point -- a control that re-implements the producer proves
  nothing about the producer.

THE SCRATCH TABLE REPRODUCES ONE MEASURED PROPERTY OF THE REAL ONE: a key attribute of a
GSI cannot carry an empty string. Measured 2026-09-11 against etf-classifications itself
with a conditional put that could not land:
    ValidationException ... The AttributeValue for a key attribute cannot contain an empty
    string value. IndexName: sub-asset-class-index, IndexKey: sub_asset_class
and the identical request with a non-empty value returned ConditionalCheckFailedException,
so the empty string is what is refused. BatchWriteItem rejects the WHOLE request when any
item in it is invalid, which the fake reproduces too.
This matters because it is why the BEFORE arm is run TWICE -- see ARM 1 vs ARM 2.
"""
import copy
import io
import os
import sys
import types
from contextlib import redirect_stdout

SIX = ["DBC", "GLD", "GSG", "IAU", "SLV", "USO"]

ROOT = os.getcwd()
SCRATCH = os.path.join(ROOT, ".scratch", "run")

SEEDER_NEW = os.path.join(ROOT, "infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-classifications.py")
SEEDER_OLD = os.path.join(ROOT, ".scratch/head/yang_pipeline_seed-etf-classifications.py")
MODULE_NEW = os.path.join(ROOT, "infra/aws/lambda/v2_portal/_shared/etf_classification.py")
MODULE_OLD = os.path.join(ROOT, ".scratch/head/_shared_etf_classification.py")

GSI_KEY_ATTRS = ("asset_class", "sub_asset_class")


class ValidationException(Exception):
    pass


class ScratchTable(object):
    """An in-process stand-in for the DynamoDB table. Backed by a dict, never the network."""

    SCAN_PAGE = 3  # deliberately tiny so the seeder's pagination loop is actually exercised

    def __init__(self, store, enforce_gsi_empty_string=True):
        self.store = store
        self.enforce = enforce_gsi_empty_string
        self.writes = 0
        self.rejected_batches = 0

    # --- read side -------------------------------------------------------------
    def scan(self, **kwargs):
        keys = sorted(self.store)
        start = kwargs.get("ExclusiveStartKey")
        idx = keys.index(start) + 1 if start in keys else 0
        page = keys[idx:idx + self.SCAN_PAGE]
        out = {"Items": [copy.deepcopy(self.store[k]) for k in page]}
        if idx + self.SCAN_PAGE < len(keys):
            out["LastEvaluatedKey"] = page[-1]
        return out

    # --- write side ------------------------------------------------------------
    def _validate(self, item):
        if not self.enforce:
            return
        for attr in GSI_KEY_ATTRS:
            if attr in item and item[attr] == "":
                raise ValidationException(
                    "One or more parameter values are not valid. A value specified for a "
                    "secondary index key is not supported. The AttributeValue for a key "
                    "attribute cannot contain an empty string value. IndexName: "
                    "%s-index, IndexKey: %s" % (attr.replace("_", "-"), attr))

    def batch_writer(self):
        return _BatchWriter(self)


class _BatchWriter(object):
    """Reproduces BatchWriteItem semantics: buffer 25, and an invalid item kills the BATCH."""

    BATCH = 25

    def __init__(self, table):
        self.table = table
        self.buffer = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self._flush()
        return False

    def put_item(self, Item=None, **_):
        self.buffer.append(copy.deepcopy(Item))
        if len(self.buffer) >= self.BATCH:
            self._flush()

    def _flush(self):
        if not self.buffer:
            return
        batch, self.buffer = self.buffer, []
        for item in batch:
            try:
                self.table._validate(item)
            except ValidationException:
                self.table.rejected_batches += 1
                raise
        for item in batch:
            self.table.store[item["ticker"]] = item
            self.table.writes += 1


def make_fake_boto3(table):
    mod = types.ModuleType("boto3")
    mod.__IS_FAKE__ = True

    class _Resource(object):
        def Table(self, name):
            print("SCRATCH TARGET: Table(%r) intercepted -> in-process scratch store "
                  "(no network client exists in this process)" % name)
            return table

    def resource(name, **kwargs):
        return _Resource()

    def client(*a, **k):
        raise AssertionError("the control must never construct a real client")

    mod.resource = resource
    mod.client = client
    return mod


def load_module_from(path, name):
    """Execute a module's real bytes into a fresh namespace. No import side effects shared."""
    with open(path, "rb") as fh:
        src = fh.read().decode("utf-8")
    mod = types.ModuleType(name)
    mod.__file__ = path
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod


def run_seeder(seeder_path, module_path, table, label):
    """Execute the REAL seeder bytes against the scratch table. Returns (rc, output, error)."""
    # The classification module the seeder will import, chosen by this arm.
    etf_mod = load_module_from(module_path, "etf_classification")
    saved_etf = sys.modules.get("etf_classification")
    saved_boto = sys.modules.get("boto3")
    sys.modules["etf_classification"] = etf_mod
    sys.modules["boto3"] = make_fake_boto3(table)

    buf = io.StringIO()
    rc, err = None, None
    try:
        with open(seeder_path, "rb") as fh:
            src = fh.read().decode("utf-8")
        seeder = types.ModuleType("seeder_under_test")
        seeder.__file__ = SEEDER_NEW  # so its sys.path.insert resolves to the real tree
        seeder.__name__ = "seeder_under_test"
        with redirect_stdout(buf):
            exec(compile(src, seeder_path, "exec"), seeder.__dict__)
            rc = seeder.seed_table(region="us-east-1", dry_run=False)
    except Exception as exc:
        err = "%s: %s" % (type(exc).__name__, exc)
    finally:
        assert sys.modules["boto3"].__IS_FAKE__ is True, "the fake boto3 was displaced"
        if saved_etf is None:
            sys.modules.pop("etf_classification", None)
        else:
            sys.modules["etf_classification"] = saved_etf
        if saved_boto is None:
            sys.modules.pop("boto3", None)
        else:
            sys.modules["boto3"] = saved_boto
    return rc, buf.getvalue(), err


def baseline_store(seventh):
    """The scratch registry as AT2-s-5 left the live one: the six curated to 'passive'."""
    sub = {"DBC": "Commodities", "GLD": "Gold", "GSG": "Commodities",
           "IAU": "Gold", "SLV": "Silver", "USO": "Oil"}
    store = {}
    for t in SIX:
        store[t] = {"ticker": t, "asset_class": "hedge", "sub_asset_class": sub[t],
                    "management_style": "passive", "sector": sub[t],
                    "name": t, "last_updated": "2026-09-11T00:00:00Z",
                    "updated_by": "seed-script"}
    # THE SEVENTH ROW IS THE GENERALISATION TEST. It is curated in the table and absent from
    # ETF_MANAGEMENT_STYLE in BOTH the old and the new module, so populating the map (limb A)
    # cannot save it and only the merge (limb B) can.
    store[seventh] = {"ticker": seventh, "asset_class": "equity",
                      "sub_asset_class": "US Large Cap", "management_style": "active",
                      "sector": "Broad", "name": seventh,
                      "last_updated": "2026-09-11T00:00:00Z", "updated_by": "a-curator"}
    return store


def pick_seventh():
    """A ticker the seeder writes but NEITHER module carries a management_style for."""
    import ast

    def maps_of(path):
        with open(path, "rb") as fh:
            tree = ast.parse(fh.read().decode("utf-8"))
        out = {}
        for node in tree.body:
            targets = node.targets if isinstance(node, ast.Assign) else (
                [node.target] if isinstance(node, ast.AnnAssign) else [])
            for tgt in targets:
                if isinstance(tgt, ast.Name) and tgt.id.startswith("ETF_"):
                    try:
                        out[tgt.id] = ast.literal_eval(node.value)
                    except Exception:
                        pass
        return out

    new = maps_of(MODULE_NEW)
    old = maps_of(MODULE_OLD)
    union = set()
    for nm in ("ETF_CLASSIFICATIONS", "ETF_MANAGEMENT_STYLE",
               "ETF_SUB_ASSET_CLASS", "ETF_SECTOR_MAPPING"):
        union |= set(new.get(nm, {}))
    cands = sorted(t for t in union
                   if t not in new.get("ETF_MANAGEMENT_STYLE", {})
                   and t not in old.get("ETF_MANAGEMENT_STYLE", {}))
    return cands[0], len(cands)


def read_six(store, seventh):
    rows = {t: store.get(t, {}).get("management_style", "<ROW ABSENT>") for t in SIX}
    rows[seventh] = store.get(seventh, {}).get("management_style", "<ROW ABSENT>")
    return rows


def arm(n, title, seeder_path, module_path, enforce, seventh, results):
    store = baseline_store(seventh)
    before = read_six(store, seventh)
    table = ScratchTable(store, enforce_gsi_empty_string=enforce)
    rc, out, err = run_seeder(seeder_path, module_path, table, title)
    after = read_six(store, seventh)

    print("")
    print("=" * 104)
    print("ARM %d -- %s" % (n, title))
    print("  seeder bytes : %s" % os.path.relpath(seeder_path, ROOT))
    print("  module bytes : %s" % os.path.relpath(module_path, ROOT))
    print("  scratch table enforces the measured GSI empty-string refusal: %s"
          % ("YES" if enforce else "NO (counterfactual: the crash removed)"))
    print("-" * 104)
    print("SEEDER OUTPUT, VERBATIM:")
    print(out.rstrip() if out.strip() else "  <no stdout>")
    if err:
        print("SEEDER RAISED: %s" % err)
    print("  return code: %r   items written to scratch: %d   batches rejected: %d"
          % (rc, table.writes, table.rejected_batches))
    print("-" * 104)
    print("  %-8s %-14s %-14s %s" % ("TICKER", "BEFORE", "AFTER", "VERDICT"))
    reverted = []
    for t in SIX + [seventh]:
        verdict = "SURVIVED" if after[t] == before[t] else "CHANGED"
        if after[t] != before[t]:
            reverted.append(t)
        print("  %-8s %-14s %-14s %s%s"
              % (t, before[t], after[t], verdict, "  <-- the 7th, generalisation test"
                 if t == seventh else ""))
    survived = len([t for t in SIX if after[t] == before[t]])
    print("  SIX SURVIVED: %d of %d;  seventh: %s"
          % (survived, len(SIX), "SURVIVED" if after[seventh] == before[seventh] else "REVERTED"))
    results[n] = {"six_survived": survived, "seventh_survived": after[seventh] == before[seventh],
                  "rc": rc, "err": err, "writes": table.writes, "after": after}
    return results[n]


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    for p in (SEEDER_OLD, MODULE_OLD):
        if not os.path.exists(p):
            print("BLOCKED: old bytes missing at %s -- dump them with `git show HEAD:<path>`" % p)
            return 1

    seventh, n_cands = pick_seventh()
    print("T4-AC3 -- SIMULATED RE-SEED AGAINST A SCRATCH TARGET. THE LIVE TABLE IS NEVER OPENED.")
    print("=" * 104)
    print("SCRATCH BASELINE = the six as AT2-s-5 left them (management_style='passive',")
    print("asset_class='hedge') plus a SEVENTH curated row.")
    print("SEVENTH ROW CHOSEN: %s -- absent from ETF_MANAGEMENT_STYLE in BOTH the old and the"
          % seventh)
    print("new module (1 of %d such tickers), curated in the table to 'active'. Populating the"
          % n_cands)
    print("map cannot save it; only the merge can. It is how this control tells a FIX apart")
    print("from SIX HARDCODED VALUES.")

    results = {}

    arm(1, "BEFORE / old bytes, scratch table faithful to the measured constraint",
        SEEDER_OLD, MODULE_OLD, True, seventh, results)
    arm(2, "BEFORE / old bytes, constraint LIFTED -- the hazard with its accidental shield removed",
        SEEDER_OLD, MODULE_OLD, False, seventh, results)
    arm(3, "AFTER / new bytes, faithful",
        SEEDER_NEW, MODULE_NEW, True, seventh, results)
    arm(4, "ISOLATION / OLD module + NEW seeder -- does the MERGE alone hold the line?",
        SEEDER_NEW, MODULE_OLD, True, seventh, results)
    arm(5, "ISOLATION / NEW module + OLD seeder -- does populating the map alone hold it?",
        SEEDER_OLD, MODULE_NEW, False, seventh, results)

    print("")
    print("=" * 104)
    print("FALSIFY ARM -- old bytes in BOTH positions, asserted as if they were the fix.")
    print("This assertion MUST FAIL. If it passes, the control cannot tell the old world from")
    print("the new one and every PASS above is worthless.")
    print("=" * 104)
    a2 = results[2]
    falsify_claim = (a2["six_survived"] == len(SIX) and a2["seventh_survived"])
    print("  claim under test : 'old module + old seeder preserves all six AND the seventh'")
    print("  measured         : six survived %d of %d, seventh survived %s"
          % (a2["six_survived"], len(SIX), a2["seventh_survived"]))
    print("  ASSERTION RESULT : %s" % ("PASSED -- CONTROL IS BROKEN" if falsify_claim
                                       else "FAILED, as required"))
    try:
        assert falsify_claim, ("old bytes do NOT preserve the curated values -- "
                               "this is the expected failure")
        falsify_ok = False
    except AssertionError as exc:
        falsify_ok = True
        print("  AssertionError raised, verbatim: %s" % exc)

    print("")
    print("=" * 104)
    print("SUMMARY")
    print("=" * 104)
    rows = [
        (1, "BEFORE faithful   (old+old, constraint on) ", "old seeder DIES on batch 1; nothing written"),
        (2, "BEFORE unshielded (old+old, constraint off)", "the revert the row names, made visible"),
        (3, "AFTER             (new+new)                ", "the fix"),
        (4, "ISOLATION         (old module + new seeder)", "merge alone"),
        (5, "ISOLATION         (new module + old seeder)", "map alone"),
    ]
    print("  ARM  CONFIGURATION                            SIX      SEVENTH    rc/raise")
    for n, label, _ in rows:
        r = results[n]
        print("  %-4d %s %d of 6   %-9s  %s"
              % (n, label, r["six_survived"],
                 "SURVIVED" if r["seventh_survived"] else "REVERTED",
                 r["err"] if r["err"] else ("rc=%r" % r["rc"])))
    for n, label, why in rows:
        print("  ARM %d %s-- %s" % (n, label, why))

    ok = (results[2]["six_survived"] == 0
          and results[3]["six_survived"] == 6 and results[3]["seventh_survived"]
          and results[4]["six_survived"] == 6 and results[4]["seventh_survived"]
          and not results[5]["seventh_survived"]
          and results[1]["err"] is not None
          and falsify_ok)
    print("")
    print("CONTROL VERDICT: %s" % ("OK: the control discriminates -- it fails on the old bytes "
                                   "(arm 2, 0 of 6 survive) and passes on the new ones (arm 3, "
                                   "6 of 6 plus the seventh), and the falsify arm failed as "
                                   "required" if ok else "ERROR: the control did not behave as "
                                                         "specified"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
