"""AMGT-ba-13 equal_reads.py -- every object whose READ the cell moves, loaded through each
module's OWN loader (or, where a module reads inline, through that module's own path constant),
and one sha256 per object.

  python equal_reads.py --write before/reads.json   # run at the base, BEFORE any edit
  python equal_reads.py                              # after the edits: compares to before/reads.json

Output on the compare run: one line per object (EQUAL / DIFF), then `EQUAL n of n` and exit 0 only
when every object's sha256 matches. A `HOMES` line then states how many objects are now read from a
path that does not name a worker folder (informational; the verdict is the hash equality).

Reads only. A loader that needs AWS (the crosswalk's pool object) reads; nothing here writes. No
vendor, SEC or model call. Run from the repo root with PYTHONPATH set to it.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BEFORE = os.path.join(HERE, "before", "reads.json")
NEEDLE = "0.9.0_WK_AMGT_RESAPP~"
ROOT = os.getcwd()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

_DELIV = os.path.join(
    "org", "missions", "D5", "AMGT", "AMGT_RESAPP", "deliverables", "0.9.0_WK_AMGT_RESAPP~5", "lists"
)


def digest(obj):
    body = json.dumps(obj, sort_keys=True, ensure_ascii=True, separators=(",", ":"), default=str)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _abs(path):
    return path if os.path.isabs(path) else os.path.join(ROOT, path)


def _load_json(path):
    with open(_abs(path), encoding="utf-8") as fh:
        return json.load(fh)


class _NoPool(object):
    """A client whose every call fails, so engine.load_union_universe reads its named local fallback."""

    def get_object(self, **kwargs):
        raise RuntimeError("equal_reads: pool deliberately not read; the local fallback is the object")


def objects(at_base=False):
    """[(name, loader_description, home_path_or_None, object)]"""
    out = []

    from lib.research.identity import crosswalk
    cov_path = crosswalk.coverage_path()
    coverage_doc = crosswalk._read_json(_abs(cov_path))
    out.append(("crosswalk.coverage_doc", "crosswalk._read_json(crosswalk.coverage_path())", cov_path, coverage_doc))

    built = crosswalk.build_crosswalk(
        "2026-01-01", coverage_doc=coverage_doc, pilots=crosswalk.load_pilots(),
        coverage_source="equal_reads://fixed-label", registrations=[],
    )
    keys = sorted(str(r.get("security_key")) for r in built["records"])
    out.append(("crosswalk.built_record_keys", "crosswalk.build_crosswalk(coverage_doc=<its coverage doc>, fixed label)",
                None, {"n": len(keys), "keys": keys}))

    xdoc, _index, _amb = crosswalk.load_crosswalk()
    xkeys = sorted(str(r.get("security_key")) for r in xdoc["records"])
    out.append(("crosswalk.pool_document", "crosswalk.load_crosswalk() (pool read)", None,
                {"n_records": len(xkeys), "keys": xkeys, "document": xdoc}))

    from lib.research.peers import universe as pu
    mb_dir = pu.MODEL_BLOCK_DIR_DEFAULT
    blocks = {}
    for key, path in pu._model_block_files(mb_dir):
        blocks[key] = _load_json(path)
    out.append(("peers.universe.model_block_dir", "peers.universe._model_block_files(MODEL_BLOCK_DIR_DEFAULT)",
                mb_dir, blocks))

    from lib.research.peers import engine as pe
    udoc, _src = pe.load_union_universe("0000-00-00", client=_NoPool())
    out.append(("peers.engine.universe_fallback", "peers.engine.load_union_universe(pool refused)",
                pe.UNIVERSE_FALLBACK, udoc))
    block = pe._load_model_block("BABACVOCTRL_US_Equity", pe.MODEL_BLOCK_DIR_DEFAULT, read_pool=False)
    out.append(("peers.engine.model_block_BABACVOCTRL", "peers.engine._load_model_block(read_pool=False)",
                pe.MODEL_BLOCK_DIR_DEFAULT, block))

    from lib.research.posture import packs, fit
    pdoc, _psrc = packs.load_model_block("BA_US_Equity")
    out.append(("posture.packs.model_block_BA_US_Equity", "posture.packs.load_model_block('BA_US_Equity')",
                packs.MODEL_BLOCK_DIR, pdoc))
    reg = fit.load_registry()
    out.append(("posture.fit.scanner_factor_metadata", "posture.fit.load_registry()", fit.REGISTRY_PATH,
                {"factors": reg[0], "asOf": reg[1]}))

    from lib.research.metrics import chatter_axis
    out.append(("metrics.chatter_axis.universe_tickers", "chatter_axis.read_universe_tickers()",
                chatter_axis.DEFAULT_UNIVERSE_PATH, chatter_axis.read_universe_tickers()))

    from lib.research.freshness import build_view
    out.append(("freshness.build_view.universe", "build_view.DEFAULT_UNIVERSE_PATH, the module's own open()",
                build_view.DEFAULT_UNIVERSE_PATH, _load_json(build_view.DEFAULT_UNIVERSE_PATH)))

    from lib.research.identity import coverage_pass
    out.append(("identity.coverage_pass.landed_universe", "coverage_pass.LANDED_UNIVERSE_PATH, the module's own open()",
                coverage_pass.LANDED_UNIVERSE_PATH, _load_json(coverage_pass.LANDED_UNIVERSE_PATH)))
    out.append(("identity.coverage_pass.sa_ids", "coverage_pass.SA_IDS_PATH, the module's own open()",
                coverage_pass.SA_IDS_PATH, _load_json(coverage_pass.SA_IDS_PATH)))

    from lib.research.coverage import run_reader
    out.append(("coverage.run_reader.manifest_tickers", "run_reader._run_manifest_tickers(repo_root)", None,
                run_reader._run_manifest_tickers(ROOT)))

    from lib.research.social import collect
    out.append(("social.collect.read_security_BA_US_Equity", "collect.read_security('BA_US_Equity')",
                getattr(collect, "UNIVERSE_PATH", None), collect.read_security("BA_US_Equity")["company_name"]))
    if hasattr(collect, "UNIVERSE_PATH"):  # the base: a local file in a worker folder
        out.append(("social.collect.universe_document", "collect.UNIVERSE_PATH, read_security's own read",
                    collect.UNIVERSE_PATH, _load_json(os.path.join(str(collect.REPO_ROOT), collect.UNIVERSE_PATH))))
    else:  # after: the pool object through the reader collect._union_universe uses (pool read, no fallback)
        udoc, usrc = collect._union_universe()
        out.append(("social.collect.universe_document", "collect._union_universe() (peers.engine.load_union_universe)",
                    None, udoc))

    from lib.research.lists import rot
    data_dir = os.path.join(os.path.dirname(os.path.abspath(rot.__file__)), "data")
    lists_home = _DELIV if at_base else data_dir  # at the base the files live only in the record folder
    for name in rot.LIST_NAMES:
        out.append(("lists.%s" % name, "the file read_list_register opens (rot module data/), else the record folder at the base",
                    lists_home, _load_json(os.path.join(lists_home, "%s.json" % name))))
    return out


def main(argv):
    write = len(argv) >= 2 and argv[0] == "--write"
    rows = {}
    homes = {}
    for name, loader, home, obj in objects(at_base=write):
        rows[name] = digest(obj)
        homes[name] = {"loader": loader, "home": home}
    if write:
        os.makedirs(os.path.dirname(BEFORE), exist_ok=True)
        with open(argv[1] if os.path.isabs(argv[1]) else os.path.join(ROOT, argv[1]), "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"sha256": rows, "homes": homes}, fh, indent=2, sort_keys=True)
            fh.write("\n")
        for name in sorted(rows):
            print("WROTE %s %s" % (rows[name][:16], name))
        print("WROTE %d object(s)" % len(rows))
        return 0
    with open(BEFORE, encoding="utf-8") as fh:
        before = json.load(fh)["sha256"]
    names = sorted(set(before) | set(rows))
    same = 0
    for name in names:
        ok = before.get(name) == rows.get(name)
        same += 1 if ok else 0
        print("%s %s %s" % ("EQUAL" if ok else "DIFF ", (rows.get(name) or "absent")[:16], name))
    off = sum(1 for h in homes.values() if h["home"] and NEEDLE not in str(h["home"]))
    named = sum(1 for h in homes.values() if h["home"])
    from lib.research.api import scoped_amgt
    served = sorted(k for k, v in scoped_amgt.read_list_register()["reads"].items() if v.get("status") == scoped_amgt.POOL_SERVED)
    print("INFO read_list_register served from the packaged data/: %s" % served)
    print("HOMES %d of %d path-reads are off a worker folder" % (off, named))
    print("%s %d of %d" % ("EQUAL" if same == len(names) else "NOT EQUAL", same, len(names)))
    return 0 if same == len(names) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
