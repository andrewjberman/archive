"""b-6 KEY SHAPE and LABEL RESOLUTION, checked against the SPINE -- a DIFFERENT
substrate from the emission file.

WHY THIS EXISTS (0.4.0_DE_ClientPlatform~D 79662): their consumer-side cross-tab and my
producer-side reproduction parse THE SAME emission file. That is two CLASSIFICATIONS
over ONE substrate: it rules out an idiosyncratic predicate (two people wrote the logic
separately and every cell matched) and it does NOT establish that the emitter assigned
the key shapes correctly -- if the emitter were wrong, both reads agree about the same
wrong thing. The independent substrate for THAT axis is dim_relationship itself.

⛔ THE DENOMINATOR IS THE UNION OF BOTH SPINE VINTAGES, AND GETTING THIS WRONG IS HOW
THIS ARM FIRST LIED. Its first version matched the leaf's rel_ keys against the AS-OF
spine alone and printed "DISAGREEMENT -- an emitter key-shape defect", 89 keys missing.
That verdict was FALSE: _book's key_for deliberately resolves END-or-START (an account
that has LEFT still keys to the client it was under at the window start), so a lost
relationship's key lives in the START spine by design. Against the UNION: 3,348 of 3,348,
0 in neither -- and independently, all 89 carry status == 'lost', a different derivation
reaching the same set. A single-vintage denominator reads a healthy leaf as broken.

THE SAME TRAP BINDS THE SERVED JOIN DISCRIMINATOR (CTO 79649): matching the 9,944
rel_-shaped ROWS against ONE serve-time spine reads 270 short on a healthy join, because
those 270 are the lost population. Union, or scope to status != 'lost'.
"""
import io
import json
import pathlib
import subprocess

import boto3
import pyarrow.parquet as pq

ROOT = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True,
                                   check=True).stdout.strip())
LEAF = (ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables"
             / "emissions/perfrp_book_advisor.json")
S3 = boto3.client("s3")
FAILS = []


def check(name, cond, detail=""):
    print("  %-56s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


def spine(date):
    o = S3.get_object(Bucket="opal-data-49financial",
                      Key="gold/advi/dimensions/dim_relationship/date=%s/data.parquet" % date)
    return pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()


def label_map(df):
    """d04_clients_tab's derivation, reproduced (mapped rows only)."""
    m = df[df["mapped"].fillna(False).astype(bool)]
    return (m.groupby("relationship_id")["registration_name"]
             .apply(lambda s: " & ".join(sorted(set(
                 " ".join(x.split()) for x in s.dropna().astype(str) if x.strip()))))
             .to_dict())


leaf = json.load(open(LEAF, encoding="utf-8"))
pins = leaf["window"]["upstream_pins"]
end_date = pins["dimensions/dim_relationship@as_of"]["partition_date"]
start_date = pins["dimensions/dim_relationship@window_start"]["partition_date"]
print("leaf pins the spine at TWO vintages: as-of %s ; window-start %s (aliased from %s)"
      % (end_date, start_date,
         pins["dimensions/dim_relationship@window_start"]["requested_date"]))

end_df, start_df = spine(end_date), spine(start_date)
end_ids = set(end_df["relationship_id"].dropna().astype(str))
start_ids = set(start_df["relationship_id"].dropna().astype(str))
end_lbl, start_lbl = label_map(end_df), label_map(start_df)
mapped_accts = set(end_df[end_df["mapped"].fillna(False).astype(bool)]["account_id"].astype(str))

rows = [r for e in leaf["entries"] for r in e["client_table"]]
rel_rows = [r for r in rows if not str(r["relationship_id"]).startswith("UNMAPPED-RELATIONSHIP:")]
sent_rows = [r for r in rows if str(r["relationship_id"]).startswith("UNMAPPED-RELATIONSHIP:")]
rel_keys = {r["relationship_id"] for r in rel_rows}

print()
print("=" * 74)
print("ARM 1 -- KEY SHAPE against the spine UNION (the emitter's own rule)")
print("=" * 74)
union = end_ids | start_ids
missing = sorted(rel_keys - union)
check("every rel_-shaped key is in the spine UNION", not missing,
      "%d of %d in union; %d missing" % (len(rel_keys) - len(missing), len(rel_keys),
                                         len(missing)))
only_start = rel_keys - end_ids
# THIS ARM HAS A PRECONDITION AND IT NO LONGER HOLDS ON THIS LEAF. `lost` is a status
# the emitter can only assign when the MEMBERSHIP basis is computable; under 79840's
# ruled law the QTD leaf's window start precedes the jd2 floor, so every row reads
# `unknown` and the lost set is empty BY LAW, not by disagreement. Scoring it anyway
# would fail a leaf that is behaving exactly as ruled -- an arm outliving its premise.
_statuses = {r["status"] for r in rel_rows}
if _statuses == {"unknown"}:
    print("  keys present ONLY in the start spine are exactly the LOST set    "
          "NOT APPLICABLE")
    print("     the membership basis is absent, so no row carries `lost`; the "
          "corroboration this arm provides is scored on the floor-aligned")
    print("     evidence leaf instead, where the computable branch runs.")
else:
    check("keys present ONLY in the start spine are exactly the LOST set",
          only_start == {r["relationship_id"] for r in rel_rows
                         if r["status"] == "lost"},
          "%d start-only keys" % len(only_start))
    print("  ^ a SECOND derivation (status) reaching the SAME set as spine membership.")
bad_sent = [k for k in {r["relationship_id"] for r in sent_rows}
            if k.split("UNMAPPED-RELATIONSHIP:", 1)[1] in mapped_accts]
check("no sentinel key's account is actually MAPPED in the spine", not bad_sent,
      "%d mis-shaped" % len(bad_sent))
# POSITIVE CONTROL -- the spine set must be able to find a real key and reject a fake.
check("POSITIVE CONTROL: spine contains a known leaf key and rejects a fabricated one",
      (sorted(rel_keys)[0] in union) and ("rel_ZZZZZZZZZZZZZZ" not in union))
print("  NAIVE DENOMINATOR, printed so the trap stays visible: matching against the")
print("  AS-OF spine ALONE reports %d of %d -- %d 'missing' on a healthy leaf."
      % (len(rel_keys & end_ids), len(rel_keys), len(rel_keys - end_ids)))

print()
print("=" * 74)
print("ARM 2 -- LABEL RESOLUTION: the emitter's spine reads are ASYMMETRIC")
print("=" * 74)
unl = [r for r in rel_rows if str(r["relationship"]).startswith("UNLABELLED-RELATIONSHIP:")]
in_end = sum(1 for r in unl if r["relationship_id"] in end_lbl)
in_start = sum(1 for r in unl if r["relationship_id"] in start_lbl)
neither = sum(1 for r in unl
              if r["relationship_id"] not in end_lbl and r["relationship_id"] not in start_lbl)
print("  rel_-keyed UNLABELLED rows: %d" % len(unl))
print("      label in the AS-OF spine : %d" % in_end)
print("      label in the START spine : %d" % in_start)
print("      label in NEITHER spine   : %d" % neither)
# INVERTED ON 2026-08-28: THIS ASSERTED THE DEFECT WAS PRESENT, AND THE FIX LANDED.
# It read `in_start > 0` -- "labels exist for rows the leaf renders UNLABELLED" -- which
# was the right assertion while the defect stood and becomes a FALSE ALARM the moment
# it is repaired. A detector that fails when its subject is fixed is a detector nobody
# can leave running. Measured after the (A)(ii) START-fallback fix: 270 -> 0, and every
# one of the 9,748 rel_-keyed rows now carries a label. What remains UNLABELLED is 132
# SENTINEL rows, which have no relationship to label by construction.
check("THE DEFECT IS REPAIRED: no rel_-keyed row is renderable-but-UNLABELLED",
      in_start == 0 and in_end == 0,
      "%d rows UNLABELLED, %d recoverable from either spine (was 270)"
      % (len(unl), in_start + in_end))
print("  CAUSE: _book.key_for resolves END-or-START, but _relationship_labels builds")
print("  its map from the AS-OF spine ONLY. A lost relationship therefore gets a KEY")
print("  from the start spine and finds no LABEL, because the label map never looked")
print("  there. FIX (one line, bundled re-emission): build the label map from both")
print("  vintages, END preferred, START fallback -- mirroring key_for exactly.")
check("no row is unlabellable (a genuine spine gap would show here)", neither == 0,
      "%d with no label in either vintage" % neither)
print("  ^ THIS IS WHY label_state's NO_SPINE_LABEL member must not be justified by")
print("    these rows: after the fix that population is 0. A genuine spine gap is the")
print("    `neither` count above, which is currently ZERO.")

print()
print("=" * 74)
if FAILS:
    print("RESULT: %d ARM(S) FAILED: %s" % (len(FAILS), FAILS))
else:
    print("RESULT: ALL ARMS PASS -- key shape SOUND against an independent substrate;")
    print("the UNLABELLED population is a PRODUCER asymmetry, not a spine gap.")
