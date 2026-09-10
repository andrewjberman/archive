#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-I-4 / I4-AC3 -- CG-s-44. THE REMEDY: TAKEN, OR FILED WITH ITS OWNER.
#
# I4-AC2 chose WRITER_KEY. This script settles what happened to that choice, and it settles
# it the honest way: the branch is FILED, because the act the choice names is out of this
# worker's reach for TWO independent reasons, and either one alone would be enough.
#
# THE CHEAPEST WRONG MOVE HERE IS TO 'FIX' A DATED KEY BY WRITING TO IT. That is why this
# criterion prints the acts NOT to take on BOTH branches: a reader who agrees with the
# finding and reaches for the obvious repair destroys the last surviving evidence.
#
# WHAT IS ACTUALLY DONE IN-GRANT, and it is not nothing: this order's own record is written
# in the citation grammar (bucket/key@ETag), the table is measured live, and the spec-vs-
# world divergence that decides the choice is on the channel as a row with a disarm owner.
# Filing is a real act with a named owner; it is not a deferral.
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../../../../../.." && pwd)"
CHANNEL="$ROOT/org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md"
ROW_ID="NFRA_CLDGRPH-W3-S20"

echo "=============================================================================="
echo "I4-AC3 -- THE REMEDY, AND THE ACTS THAT MUST NOT BE TAKEN MEANWHILE"
echo "=============================================================================="
echo "TREE          : $ROOT"
echo "  branch      : $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
echo "  HEAD        : $(git -C "$ROOT" rev-parse HEAD)"
echo "CHOSEN (AC2)  : WRITER_KEY -- the archive key names the write, not the calendar day"
echo ""

echo "BRANCH=FILED"
echo ""
echo "BLOCKER printed -- TWO, and either alone is sufficient:"
echo "  BLOCKER 1 (LANE). The act edits infra/aws/globgrph/derive_runner.py:493. This order's"
echo "    <paths> block grants exactly three surfaces:"
echo "      org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/"
echo "      org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md"
echo "      org/missions/D0/NFRA/NFRA_CLDGRPH/task-orders/NFRA_CLDGRPH.TO-CG-I-4.*.md"
echo "    The producer is named in SURFACES as READ, 'edit only on the writer branch'. A path"
echo "    this face does not grant is a BLOCKING ROW AND A REPORT, NEVER AN OVERRIDE."
echo "  BLOCKER 2 (EGRESS HOLD). Even with the lane, landing it is an image build + push +"
echo "    ECS revision, and every one of those is FORBIDDEN to this round by name. The hold is"
echo "    estate law about egress off Opal infrastructure plus a live SMS subscription on the"
echo "    derive's topic; Andrew's 'take off any holds on CLDGRPH' does not lift it and this"
echo "    worker may not read it as doing so."
echo "  NOT A BLOCKER, said so the filing is not read as helplessness: the CODE change itself"
echo "    is one f-string, and the only in-estate reader resolves snapshots/latest.txt, a"
echo "    pointer -- so the conformant key breaks no reader (measured, i4_layers.py)."
echo ""

echo "OWNER_NAMED printed:"
echo "  PRIMARY   0.8.0_AE_CloudComp -- the engine owner; the disarm owner already carried by"
echo "            rows W1-S43 and W2-S61, and by W3-S20 filed in this cell."
echo "  SECOND    AE 0.7.0 -- owner of the record-retention-policy-v1 row that declares this"
echo "            key a Tier-1 INDEFINITE durable audit record. Two writers of one property,"
echo "            so two rules are read and both owners are named rather than one assumed."
echo "  IF THE SPEC IS TO MOVE INSTEAD OF THE PRODUCER (a legitimate outcome, and it is NOT"
echo "            this worker's to choose): 1.0.0_SA_CTO, because the PRD line, the retention"
echo "            tier and the Terraform justification for versioning-off all move together."
echo "            Andrew ratified the retention row on 2026-06-12; weakening it is his word."
echo ""

echo "WHERE IT IS FILED (a filing nobody can find is a deferral with better manners):"
# grep -q AS A PURE PREDICATE on ONE named file -- the search rail's stated
# non-application, and the only instrument here that reads an MSYS path correctly (a
# Windows python cannot open /c/tmp/...; that is what this check got wrong first).
# POSITIVE CONTROL FIRST: if the control string is not found either, the instrument is
# blind and an ABSENT verdict on the row id would be meaningless.
if ! grep -q "NFRA_CLDGRPH -- surprise channel" "$CHANNEL"; then
  echo "  BLOCKED: the channel predicate cannot see the file's own title -- instrument blind."
  exit 2
fi
if grep -q "$ROW_ID" "$CHANNEL"; then
  echo "  $ROW_ID PRESENT in the project's surprise channel (checked at this run)"
  echo "  channel: org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md"
  echo "  class OBSERVATION, hazard_standing ARMED, disarm_owner 0.8.0_AE_CloudComp,"
  echo "  disposition UNDER_INVESTIGATION -- so it reaches L9 with an owner attached."
  FILED_OK=1
else
  echo "  ERROR: $ROW_ID NOT FOUND on the channel -- the filing has not happened."
  FILED_OK=0
fi
echo "  and in the record: org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/CG-s-44.dated-archive-key.result.md"
echo ""

echo "ACTS_NOT_TO_TAKE printed -- while this sits with its owner:"
echo "  1. DO NOT write to a dated snapshot key for any reason, including to 'preserve',"
echo "     'pin' or 're-date' it. A write to snapshots/<date>/graph-<date>.tar.gz on an"
echo "     unversioned bucket destroys the object it is trying to protect."
echo "  2. DO NOT re-run a derive to 'restore' a cited vintage. A re-derive writes DIFFERENT"
echo "     bytes to the SAME key: it cannot recover the old bytes and it destroys the"
echo "     current ones, which are themselves now cited by this cell."
echo "  3. DO NOT copy an archive object to a new key as a rescue. It is an S3 write, it is"
echo "     forbidden this round, and the bytes worth rescuing are already gone -- what would"
echo "     be copied is the surviving write, which is not what any citation names."
echo "  4. DO NOT back-fill an ETag into an existing citation. The bytes cannot be re-read,"
echo "     so any ETag written beside an old citation would be a FABRICATED vintage that"
echo "     reads exactly like a measured one. UNDECIDABLE is the correct, permanent answer"
echo "     for those citations, and I4-AC1 counts them rather than repairing them."
echo "  5. DO NOT enable bucket versioning as a quick fix. It is an infrastructure act with"
echo "     an owner and a written justification for its current state (s3.tf), it costs"
echo "     storage on every future write, and it is outside the two remedies this cell"
echo "     compared. It is named in AC2 as the thing NEITHER remedy covers -- for its owner."
echo "  6. DO NOT build a monitor, alarm or freshness checker on any of this. Standing"
echo "     moratorium; a monitor on an unsettled route measures the wrong thing precisely."
echo ""

echo "TAKEN IN-GRANT (the part that needed nobody's permission):"
python "$HERE/i4_restate.py" || echo "  WARN: restatement helper returned non-zero"
echo ""
echo "  PROJECT_CITATIONS_RESTATED=0 -- and the ZERO IS THE FINDING, not an omission."
echo "  This project's live citations sit in rows on an APPEND-ONLY channel, in other seats'"
echo "  proof-of-spec instances and in captured run outputs. Rewriting them is forbidden"
echo "  (never edit an existing row) and, for the OVERWRITTEN and UNDECIDABLE ones, it would"
echo "  be fabrication rather than restatement -- see ACT 4 above. What is restated is the"
echo "  KEY TABLE above, measured this run, which is the only half of the remedy that can be"
echo "  applied retrospectively without inventing a vintage."
echo ""

if [ "$FILED_OK" = "1" ]; then
  echo "OK: I4-AC3 complete -- BRANCH=FILED, two blockers named, owners named, six acts held."
  exit 0
fi
echo "ERROR: I4-AC3 -- the row is not on the channel; the filing is not real."
exit 1
