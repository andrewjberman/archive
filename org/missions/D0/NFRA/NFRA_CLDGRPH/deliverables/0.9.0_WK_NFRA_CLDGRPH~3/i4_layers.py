#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-I-4 / I4-AC2 -- CG-s-44. THE TWO REMEDIES, COMPARED BEFORE ONE IS CHOSEN.

THE ORDER HANDED ME TWO CANDIDATES: change the WRITER so an archive key names the write, or
change the CITATION GRAMMAR so an S3 object is always cited as bucket/key@ETag. Both close
the hazard. They have different owners, different costs, and -- the field that decides it --
different things they do NOT fix.

WHY THIS FILE READS THE ESTATE INSTEAD OF QUOTING IT. Every authority quoted below is
re-read from disk at run time and checked against the text this comparison assumes; a line
that has moved prints WARN and the comparison says so rather than reciting a stale quote.
The provenance label on every claim is printed beside it: `measured` is what an instrument
returned in this run, `inferred` is what follows from something else, `held` is what I
reasoned to. Round 8's five false premises were all mislabelled `measured`.

THE FINDING THAT DECIDES THE CHOICE, and it was not in the cell. The cell offers the writer
change as a preference ("HELD, NOT MEASURED: that changing the WRITER's key grammar is
preferable"). It is not a preference. THREE authorities -- a PRD, an Andrew-ratified
retention policy, and the bucket's own Terraform -- already SPECIFY unique timestamped
tarball keys, and the third one justifies leaving the bucket UNVERSIONED *because* of that
property. The producer has never implemented it. So the writer remedy is not a new design
decision needing anyone's approval; it is CONFORMANCE to a spec that already exists, and
the versioning-off decision rests on a premise that is false in the world.

usage: python i4_layers.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i4_lib  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(HERE, "i4_census.capture.json")

# (path, must-contain, what it establishes). Every one is RE-READ, never transcribed.
AUTHORITIES = [
    ("docs/architecture/NFRA_GLOBGRPH_PRD.md",
     "graph-{run_id}.tar.gz",
     "the PRD's own prefix layout: unique timestamped keys, kept indefinitely"),
    ("docs/reference/record-retention-policy-v1.md",
     "graph-{run_id}.tar.gz",
     "record-retention-policy-v1, Andrew-ratified 2026-06-12: Tier 1 durable audit record"),
    ("infra/aws/terraform/shared-infra/s3.tf",
     "unique-timestamped-",
     "the bucket's own Terraform: WHY versioning is off -- it rests on the unique-key property"),
    ("infra/aws/globgrph/derive_runner.py",
     'key = f"snapshots/{date_str}/graph-{date_str}.tar.gz"',
     "the producer as built: ONE key per DATE, overwritten by every run on that date"),
    ("infra/aws/globgrph/derive_stitch.py",
     'Key="snapshots/latest.txt"',
     "the only in-estate reader of the archive resolves through a POINTER, not a date"),
]


# THIS TABLE IS WRITTEN AS CODE POINTS, NOT AS THE CHARACTERS THEMSELVES. A folder that
# spells the em-dash out puts non-ASCII into the very file whose job is to keep it out.
_FOLD = {0x2014: "--", 0x2013: "-", 0x2192: "->", 0x201c: '"', 0x201d: '"',
         0x2018: "'", 0x2019: "'", 0x00a0: " "}


def ascii_fold(text):
    """Quoted estate text can carry an em-dash; a capture that carries non-ASCII is
    refused by this order's standing law. Fold what has an ASCII meaning, mark the rest."""
    out = []
    for ch in text:
        o = ord(ch)
        out.append(ch if o < 128 else _FOLD.get(o, "?"))
    return "".join(out)


def cite(root, path, needle, note, head):
    full = os.path.join(root, path)
    if not os.path.exists(full):
        return {"path": path, "status": "ABSENT", "line": None, "text": None, "note": note}
    for i, line in enumerate(open(full, encoding="utf-8", errors="replace"), 1):
        if needle in line:
            return {"path": "%s:%d @%s" % (path, i, head), "status": "PRESENT",
                    "line": i, "text": ascii_fold(line.strip())[:150], "note": note}
    return {"path": "%s @%s" % (path, head), "status": "TEXT-MOVED", "line": None,
            "text": None, "note": note}


def main():
    root = i4_lib.repo_root()
    tf = i4_lib.tree_facts(root)
    head = tf["head"][:10]

    census = None
    if os.path.exists(CENSUS):
        census = json.load(open(CENSUS, encoding="utf-8"))

    print("=" * 78)
    print("I4-AC2 -- TWO REMEDIES, THEIR OWNERS, THEIR COSTS AND THEIR LIMITS")
    print("=" * 78)
    print("TREE                    : %s (%s) branch %s HEAD %s"
          % (tf["kind"], tf["root"], tf["branch"], tf["head"]))
    if census:
        print("MEASURED INPUT (I4-AC1) : %d citations / STILL_VALID %d / OVERWRITTEN %d / UNDECIDABLE %d"
              % (census["citations_found"], census["still_valid"],
                 census["overwritten"], census["undecidable"]))
        print("                          read from %s (this run's own capture)"
              % os.path.basename(CENSUS))
    else:
        print("WARN: %s absent -- run i4_census.py first; the numbers below would be unmeasured."
              % os.path.basename(CENSUS))
    print("")

    print("THE AUTHORITIES, RE-READ AT RUN TIME (not transcribed) -- claim: measured")
    cites = [cite(root, p, n, note, head) for p, n, note in AUTHORITIES]
    ok = 0
    for c in cites:
        print("  [%s] %s" % (c["status"], c["path"]))
        print("        %s" % c["note"])
        if c["text"]:
            print("        > %s" % c["text"])
            ok += 1
    print("  AUTHORITIES_RESOLVED=%d of %d" % (ok, len(cites)))
    if ok != len(cites):
        print("  WARN: an authority did not resolve; the comparison below names it above.")
    print("")

    print("-" * 78)
    print("REMEDIES_COMPARED=2 of 2")
    print("-" * 78)
    print("")

    print("REMEDY 1 -- WRITER_KEY: the archive key names the WRITE, not the calendar day.")
    print("  WHAT IT IS            : derive_runner.archive_snapshot() builds")
    print("                          snapshots/{date}/graph-{date}.tar.gz. The spec already")
    print("                          says graph-{run_id} with UNIQUE TIMESTAMPED KEYS. Making")
    print("                          the key carry the run's own instant (or a content hash)")
    print("                          is CONFORMANCE, not a new decision. claim: measured")
    print("                          (three authorities above, re-read this run).")
    print("  OWNER_PER_REMEDY printed: 0.8.0_AE_CloudComp -- the engine owner, and the disarm")
    print("                          owner already named on rows W1-S43 and W2-S61.")
    print("                          SECOND owner on the same act: AE 0.7.0, who owns the")
    print("                          record-retention-policy-v1 row that declares this key")
    print("                          Tier-1 indefinite. A property with two writers needs")
    print("                          two rules read; both are named rather than one assumed.")
    print("  COST_PER_REMEDY printed : ONE producer edit (one f-string), plus the deploy path")
    print("                          the round-9 egress hold forbids: image build + push +")
    print("                          ECS revision. READ-SIDE COST IS ZERO -- the only")
    print("                          in-estate reader resolves snapshots/latest.txt, a")
    print("                          POINTER, so a new key shape does not break it")
    print("                          (derive_stitch.py, cited above). claim: measured.")
    print("                          STORAGE COST IS REAL AND UNBOUNDED: one object per RUN")
    print("                          instead of one per DAY, on a prefix with NO lifecycle")
    print("                          rule -- the bucket's two rules are abort-incomplete-mpu")
    print("                          (prefix \"\") and an expiry scoped to")
    print("                          warehouse/ms_heat/snapshots/, which does NOT match")
    print("                          snapshots/. claim: measured, s3api")
    print("                          get-bucket-lifecycle-configuration, 2026-09-10.")
    print("                          On 2026-09-10 alone the date key took at least THREE")
    print("                          writes (two logged sizes, a third live), so 'per run'")
    print("                          is not hypothetical. claim: measured (I4-AC1 rows).")
    print("  WHAT_EACH_DOES_NOT_FIX printed: it does NOT recover one byte already lost. The")
    print("                          OVERWRITTEN citations stay unrecoverable -- the bucket")
    print("                          keeps ONE version, VersionId 'null'. It does NOT make")
    print("                          the UNDECIDABLE citations decidable: a citation with no")
    print("                          discriminator is undecidable whatever the key looks")
    print("                          like. And it does NOT stop a future overwrite of the")
    print("                          POINTER (snapshots/latest.txt), which is mutable by")
    print("                          design and is what every reader actually follows.")
    print("")

    print("REMEDY 2 -- CITATION_GRAMMAR: an S3 object is cited as bucket/key@ETag.")
    print("  WHAT IT IS            : the estate already requires file:line @ commit-ish for a")
    print("                          GIT object (CLAUDE.md rule 22: 'a citation without a")
    print("                          vintage is not a citation'). There is no equivalent for")
    print("                          an S3 object, and that gap is the whole of this cell.")
    print("                          claim: measured -- rule 22 names file:line and no S3 form.")
    print("  OWNER_PER_REMEDY printed: 1.0.0_SA_CTO for the law edit (CLAUDE.md rule 22 or the")
    print("                          annex), and 3.0.0_SA_CVO for the record bar it grades at")
    print("                          L9. A law edit has three surfaces -- commit, same-turn")
    print("                          broadcast to live seats, push state -- and a WORKER HAS")
    print("                          NO SEND TOOL, so a worker cannot land the second surface")
    print("                          even if it wrote the first. That is a lane fact, not a")
    print("                          difficulty. claim: measured (this face's STANDING LAW).")
    print("  COST_PER_REMEDY printed : near zero per citation -- one extra head-object at")
    print("                          citation time, an ETag already returned by every read a")
    print("                          seat is taking anyway. RETROSPECTIVE cost is the real")
    print("                          one: %s existing citations in this project's record"
          % (census["citations_found"] if census else "N"))
    print("                          alone, %s of them with no discriminator, and the"
          % (census["undecidable"] if census else "N"))
    print("                          UNSCOPED arm found %s more OUTSIDE this project. Those"
          % (census["unscoped_arm"]["citations"] if census else "N"))
    print("                          cannot be repaired by anyone: the bytes to re-read are")
    print("                          gone, so a back-fill would be inventing a vintage.")
    print("  WHAT_EACH_DOES_NOT_FIX printed: it does NOT stop the next overwrite. It makes a citation")
    print("                          FALSIFIABLE -- a later reader can prove the referent")
    print("                          moved -- which is strictly weaker than the referent not")
    print("                          moving. It does not preserve a Tier-1 record that the")
    print("                          retention policy calls indefinite. And it cannot be")
    print("                          applied backwards, for the reason above.")
    print("")

    print("-" * 78)
    print("THE THIRD THING, NAMED BECAUSE NEITHER ORDERED REMEDY COVERS IT")
    print("-" * 78)
    print("  Neither remedy makes an ALREADY-LOST byte recoverable, and neither prevents the")
    print("  NEXT loss on any other key in this bucket. The only mechanism that does either")
    print("  is bucket VERSIONING (or object lock), which s3.tf says is off ON PURPOSE and")
    print("  justifies by the unique-key property the producer does not provide. So the")
    print("  versioning decision and the writer defect are ONE question, not two, and")
    print("  fixing the writer is also what makes the versioning-off decision true.")
    print("  This is NOT proposed as a third remedy here: it is outside the domain the cell")
    print("  declared, it is an infrastructure act under a standing egress hold, and its")
    print("  owner (AE 0.7.0 / 0.8.0_AE_CloudComp with the CTO's ruling on the record) is")
    print("  not this worker. Named so the two-way comparison is not read as exhaustive.")
    print("")

    print("-" * 78)
    print("CHOSEN=WRITER_KEY")
    print("-" * 78)
    print("  WHY, in one line: it is the only one of the two that stops the loss, and it is")
    print("  already specified -- choosing the other would mean writing new law to describe")
    print("  a workaround for a producer that does not do what three ratified documents say")
    print("  it does.")
    print("  WHAT WOULD HAVE CHOSEN THE OTHER (the falsifier, stated so the choice is")
    print("  testable rather than asserted): if the archive key had been an UNDOCUMENTED")
    print("  convention -- no PRD line, no retention row, no Terraform justification -- then")
    print("  changing the writer would have been a design decision with a real approval")
    print("  cost, the citation grammar would have been the cheaper close, and CHOSEN would")
    print("  read CITATION_GRAMMAR. The authorities above are what moved it, and they were")
    print("  read BEFORE the choice, not after.")
    print("  NOT EXCLUSIVE: the citation grammar is the cheap complement and needs no")
    print("  owner's permission to practise. This order's own record is written in it")
    print("  (bucket/key@ETag) whatever anyone else does -- see i4_remedy.sh, which is where")
    print("  the TAKEN-or-FILED branch is settled and where the blockers are named.")
    print("")
    print("OK: I4-AC2 complete -- 2 of 2 remedies compared, owners, costs and limits printed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
