"""The 248 unlabelled lost rows 3.0.0_SA_CVO found (cert @d60b509eb7): WHICH ABSENCE?

CVO's finding is confirmed exactly -- 248 rel_-keyed UNLABELLED rows on the evidence
leaf, every one status 'lost', and the `relationship` field carries no claim field
because it is a plain string rather than a figure. That producer defect stands and is a
re-open bundle item.

>> WHAT THIS ARM ADDS, AND IT CHANGES THE OWNER. CVO reads the 248 as "the real
   population of the member 1.0.0_SA_CTO 79716/80170 declared at 0". Measured here, they
   are a population of a DIFFERENT CAUSE, and the discriminator is clean because the
   SAME EMITTER produces both leaves:

       ruled leaf     start vintage 2026-03-24, schema 2.0, label-capable   ->   0
       evidence leaf  start vintage 2026-07-14, schema 1.0, NOT capable     -> 248

   SPINE_LABEL_ABSENT as ruled means "a rel_ key present in the pinned spine vintages
   with NO LABEL VALUE in either" -- a DATA absence, owner the spine's producer, remedy
   populate the label. These 248 are a CAPABILITY absence: the pinned start vintage has
   no `mapped` and no `registration_name` COLUMNS AT ALL, so no label could exist there
   for any key. Owner: the 49F correction campaign, which per 2.0.0_SA_COO 80210 item 4
   rewrites 2026-07-14/15 (its own epoch, on the ATTESTED branch, in the last 28 of 534).
   Remedy: that rewrite. One remedy does not move the other -- Rule 24 postulate (iv) --
   so folding these into SPINE_LABEL_ABSENT would put two owners on one member. <<

THE CONTROL IS INSIDE THE DATA, not constructed: of 478 lost relationships, 230 are
still present in the AS-OF spine and ALL 230 take their label from there; the 248 are
absent from the as-of spine, so their only possible source is the start vintage -- which
cannot carry one. Same code path, same window, two outcomes decided solely by whether
the pinned start vintage has the columns.

A SECOND FALSIFIABLE PREDICTION, sibling to the re-key one: when the campaign rewrites
2026-07-14/15 to schema 2.0, these 248 should go to 0 (or to a small residue that IS
genuine SPINE_LABEL_ABSENT). If they do not, the capability reading here is wrong and
the cause is a data absence after all.
"""
import collections
import io
import json
import pathlib
import subprocess

import boto3
import pyarrow.parquet as pq

ROOT = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True,
                                   check=True).stdout.strip())
EM = ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables/emissions"
S3 = boto3.client("s3")
FAILS = []


def check(name, cond, detail=""):
    print("  %-58s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


def spine(d):
    o = S3.get_object(Bucket="opal-data-49financial",
                      Key="gold/advi/dimensions/dim_relationship/date=%s/data.parquet" % d)
    return pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()


def label_ids(df):
    """(label-bearing relationship_ids, whether the vintage CAN carry labels at all)."""
    if "mapped" not in df.columns or "registration_name" not in df.columns:
        return set(), False
    m = df[df["mapped"].fillna(False).astype(bool)]
    return {str(k) for k in m["relationship_id"].dropna()}, True


def unlabelled_rel_rows(leaf):
    rows = [r for e in leaf["entries"] for r in e["client_table"]]
    rel = [r for r in rows
           if not str(r["relationship_id"]).startswith("UNMAPPED-RELATIONSHIP:")]
    return rel, [r for r in rel
                 if str(r["relationship"]).startswith("UNLABELLED-RELATIONSHIP:")]


print("=" * 78)
print("THE DISCRIMINATOR -- one emitter, two leaves, two start vintages")
print("=" * 78)
counts = {}
for nm, fn in (("ruled", "perfrp_book_advisor.json"),
               ("evidence", "perfrp_book_advisor_floor_aligned.json")):
    L = json.load(open(EM / fn, encoding="utf-8"))
    pins = L["window"]["upstream_pins"]
    s_d = pins["dimensions/dim_relationship@window_start"]["partition_date"]
    _, cap = label_ids(spine(s_d))
    rel, unl = unlabelled_rel_rows(L)
    counts[nm] = (s_d, cap, len(rel), len(unl))
    print("  %-9s start vintage %s  label-capable %-5s  rel_ rows %5d  UNLABELLED %3d"
          % (nm, s_d, cap, len(rel), len(unl)))

check("the label-CAPABLE start vintage yields ZERO unlabelled rel_ rows",
      counts["ruled"][1] is True and counts["ruled"][3] == 0,
      "ruled: %d" % counts["ruled"][3])
check("the NON-capable start vintage is the one carrying the population",
      counts["evidence"][1] is False and counts["evidence"][3] > 0,
      "evidence: %d" % counts["evidence"][3])
print("  ^ SAME emitter, SAME code path. The only difference is whether the pinned")
print("    start vintage HAS the label columns -- so the cause is CAPABILITY, not a")
print("    missing label value, and the owner is the campaign, not the spine's labels.")

print()
print("=" * 78)
print("CVO's FINDING, REPRODUCED (evidence leaf)")
print("=" * 78)
L = json.load(open(EM / "perfrp_book_advisor_floor_aligned.json", encoding="utf-8"))
pins = L["window"]["upstream_pins"]
e_ids, e_cap = label_ids(spine(pins["dimensions/dim_relationship@as_of"]["partition_date"]))
s_ids, s_cap = label_ids(
    spine(pins["dimensions/dim_relationship@window_start"]["partition_date"]))
rel, unl = unlabelled_rel_rows(L)
st = collections.Counter(r["status"] for r in unl)
check("248-class: every unlabelled rel_ row is status 'lost'",
      set(st) == {"lost"}, "%d rows, statuses %s" % (len(unl), dict(st)))
check("none of them has a label in EITHER pinned vintage",
      not [1 for r in unl
           if r["relationship_id"] in e_ids or r["relationship_id"] in s_ids],
      "0 recoverable of %d" % len(unl))
lost = [r for r in rel if r["status"] == "lost"]
lab_lost = [r for r in lost
            if not str(r["relationship"]).startswith("UNLABELLED-RELATIONSHIP:")]
check("THE CONTROL IS IN THE DATA: the labelled lost rows all resolve from the AS-OF "
      "spine",
      len(lab_lost) > 0
      and all(r["relationship_id"] in e_ids for r in lab_lost),
      "%d of %d labelled lost rows" % (len(lab_lost), len(lab_lost)))
print("  lost rows %d = unlabelled %d + labelled %d -- the split is exactly whether the"
      % (len(lost), len(lost) - len(lab_lost), len(lab_lost)))
print("  relationship still exists in the as-of spine. Those that do NOT could only be")
print("  labelled from the start vintage, and a schema-1.0 vintage has no label column.")

print()
print("=" * 78)
print("THE PRODUCER DEFECT CVO NAMED, CONFIRMED AND NOT ARGUED WITH")
print("=" * 78)
sample = unl[0] if unl else {}
check("`relationship` carries NO claim field (it is a string, not a figure)",
      not isinstance(sample.get("relationship"), dict),
      "type=%s -- so the row cannot say WHICH absence it is"
      % type(sample.get("relationship")).__name__)
lb = L["window"]["label_basis"]
check("the cause IS disclosed, but at WINDOW level only",
      lb["window_start_supplies_labels"] is False and bool(lb["reason_if_absent"]),
      "window.label_basis says why; the ROW does not")
print("  ^ a consumer reading one row cannot tell a capability absence from a data one.")
print("    That is the re-open item: the claim belongs ON the value (CLAUDE.md, a value")
print("    must carry its claim), not only in a window block beside 10,284 rows.")

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d FAILED: %s" % (len(FAILS), FAILS))
else:
    print("RESULT: ALL PASS. CVO's 248 are confirmed and their CAUSE is measured: a")
    print("start-vintage CAPABILITY absence (owner: the campaign), not the DATA absence")
    print("SPINE_LABEL_ABSENT describes (owner: the spine's labels). PREDICTION: the")
    print("campaign's rewrite of 2026-07-14/15 to schema 2.0 sends these 248 to ~0.")
