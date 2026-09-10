#!/usr/bin/env python3
"""TO-CG-F-7 / CG-s-27 -- F7-AC3: THE RENDERED HEADER, FIVE ARMS ON REAL RENDERS.

Every line below comes from `_provenance.format_provenance_header(db_path)` -- the function
the estate calls -- on a TEMP store with FAKE bytes. No engine is opened, no loader is run,
no main-workspace store or manifest is touched: a manifest is a JSON file beside a path and
the path's bytes may be any file.

Each arm prints the FULL rendered header, then one ARM_<NAME>=<the rendered line, stripped>
summary line. The summary is a restatement of the render above it, never a substitute.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.getcwd()
sys.path.insert(0, os.path.join(_ROOT, "infra", "aws", "globgrph"))
import _provenance  # noqa: E402

FAKE = b"fake kuzu store bytes -- no engine ever opens this file\n"


def fake_store(base, name="kuzu_db", payload=FAKE):
    p = os.path.join(base, name)
    with open(p, "wb") as fh:
        fh.write(payload)
    return p


def render(db):
    return _provenance.format_provenance_header(db, check_nessie_distance=False)


def show(title, db):
    text = render(db)
    print("--- %s ---" % title)
    print(text)
    print("")
    return text.splitlines()


def find(lines, needle):
    for ln in lines:
        if needle in ln:
            return ln.strip()
    return "NOT-RENDERED(%s)" % needle


def main():
    base = tempfile.mkdtemp(prefix="f7_arms_")
    try:
        summary = []

        # ARM 1 -- the claim BESIDE the counts (a healthy, fully stamped manifest)
        db = fake_store(base, "kuzu_db_healthy")
        _provenance.write_manifest(db, source_kind="nessie",
                                   source_vintage={"nodes_snapshot_id": "1", "edges_snapshot_id": "2"},
                                   node_count=1166, edge_count=2488,
                                   edge_count_semantics="attempted",
                                   artifact_claim="historical")
        lines = show("ARM 1: fully stamped manifest -- the claim beside the counts", db)
        db_line = find(lines, "DB: ")
        claim_line = find(lines, "counts: ")
        beside = ("1166 nodes / 2488 edges" in db_line
                  and claim_line.startswith("counts: 1166 nodes / 2488 edges")
                  and "edge_count_semantics=attempted" in claim_line
                  and "artifact_claim=historical" in claim_line
                  and lines.index("  " + claim_line) == lines.index("  " + db_line) + 1)
        summary.append("ARM_CLAIM_BESIDE_COUNTS=%s" % ("true" if beside else "false"))
        summary.append("ARM_CLAIM_LINE_AS_RENDERED=%s" % claim_line)

        # ARM 2 -- no manifest at all (the negative arm the PRD keeps)
        db2 = fake_store(base, "kuzu_db_no_manifest")
        lines = show("ARM 2: no manifest beside the store", db2)
        summary.append("ARM_NO_MANIFEST=%s" % find(lines, "UNKNOWN VINTAGE"))

        # ARM 3 -- source_kind beginning UNKNOWN
        db3 = fake_store(base, "kuzu_db_unknown_kind")
        _provenance.write_manifest(db3, source_kind="UNKNOWN_tarball", source_vintage={},
                                   node_count=1166, edge_count=2488,
                                   edge_count_semantics="stored",
                                   artifact_claim="historical")
        lines = show("ARM 3: source_kind UNKNOWN_tarball", db3)
        summary.append("ARM_UNKNOWN_KIND=%s" % find(lines, "source_kind UNKNOWN_tarball"))

        # ARM 4 -- a manifest with NO claim key (a pre-CG-s-27 stamp, written by hand)
        db4 = fake_store(base, "kuzu_db_claimless")
        with open(_provenance.manifest_path(db4), "w", encoding="utf-8") as fh:
            json.dump({"schema_version": 1, "source_kind": "stitch", "source_vintage": {},
                       "built_at": _provenance.datetime.now(
                           _provenance.timezone.utc).isoformat(),
                       "node_count": 1166, "edge_count": 2488}, fh)
        lines = show("ARM 4: manifest with no claim key (pre-CG-s-27)", db4)
        summary.append("ARM_CLAIM_ABSENT=%s" % find(lines, "provenance_claim: absent"))

        # ARM 5 -- bytes rewritten AFTER the manifest (W3-S11)
        db5 = fake_store(base, "kuzu_db_bytes_newer")
        _provenance.write_manifest(db5, source_kind="stitch", source_vintage={},
                                   node_count=1166, edge_count=2488,
                                   edge_count_semantics="attempted",
                                   artifact_claim="interim_local_projection")
        before = render(db5)
        with open(db5, "wb") as fh:
            fh.write(b"REWRITTEN bytes -- the manifest describes the OLD store\n")
        newer = os.path.getmtime(db5) + 60.0
        os.utime(db5, (newer, newer))
        lines = show("ARM 5: store bytes rewritten after the manifest", db5)
        summary.append("ARM_BYTES_NEWER=%s" % find(lines, "BYTES NEWER THAN MANIFEST"))
        # the control that makes arm 5 a measurement rather than a constant:
        summary.append("ARM_BYTES_NEWER_NEGATIVE_CONTROL=%s"
                       % ("clean-before-rewrite"
                          if "BYTES NEWER THAN MANIFEST" not in before else "ALWAYS-FIRES"))

        print("=== SUMMARY (each value is the line as rendered above) ===")
        for s in summary:
            print(s)
        return 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
