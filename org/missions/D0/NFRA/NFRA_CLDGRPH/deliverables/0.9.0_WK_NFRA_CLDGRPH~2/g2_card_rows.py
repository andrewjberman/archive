#!/usr/bin/env python3
"""g2_card_rows -- ONE ROW PER CARRIER, EACH COMPLETE: the structural read of the card set.

NFRA_CLDGRPH.TO-CG-G-3 / CG-s-34, criterion G3-AC3. Slot 0.9.0_WK_NFRA_CLDGRPH~2.

WHAT IT CHECKS, and why each check is separate from the schema's:
  .tools/substrate-card-check.py answers whether each FILE is a well-formed card. It cannot answer
  the question this order actually asks -- whether the SET has one row per carrier, whether each
  carrier answers all seven Rule 28 questions, whether each row carries its own owner, and whether
  question 7 is answered concretely rather than deferred. Those are cross-file and cross-field
  properties, so they need a reader the schema cannot host.

THE CARRIER SET IS DERIVED FROM THE CARD, NOT FROM THIS FILE. The three carrier cards are read out
of the set card's artifact.location.projection_of, and each carrier's NAME is read out of that
card's own subject id -- never from the filename, because a filename and a subject id are two
carriers of one value and this project has spent a round on exactly that class of defect. A
carrier card present on disk but absent from the set card's enumeration is therefore INVISIBLE
here, deliberately and disclosed: the set's denominator is its own enumeration, which is the
failure mode the set card's own trust.failure_mode row names.

CUT DISCIPLINE: every count prints its denominator and what the denominator excludes.

Usage: python g2_card_rows.py     (exit 0 when every carrier is complete, 1 otherwise)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
CARDS = ROOT / "org/missions/D0/NFRA/NFRA_CLDGRPH/cards"
SET_CARD = CARDS / "stitch-producer-archive-read.card.json"

# The seven questions of Rule 28, at the three declared grains, as the schema names them.
QUESTIONS = [
    ("PROCESS", "1 methodology", ("process", "methodology"), ("how", "determinism")),
    ("PROCESS", "2 cadence", ("process", "cadence"), ("declared_rhythm", "actual_trigger",
                                                      "live_matches_declared")),
    ("ARTIFACT", "3 persistence", ("artifact", "persistence"), ("persisted", "authority_role",
                                                                "mutation_policy")),
    ("ARTIFACT", "4 location", ("artifact", "location"), ("home", "projection_of")),
    ("TRUST", "5 coverage", ("trust", "coverage"), ("universe", "denominator", "explicitly_out")),
    ("TRUST", "6 key", ("trust", "key"), ("identity_space", "key_is_stable", "crosses_spaces")),
    ("TRUST", "7 failure mode", ("trust", "failure_mode"), ("returns_on_failure",
                                                            "distinguishable_from_true_negative")),
]


def dig(card: dict, path: tuple):
    node = card
    for k in path:
        if not isinstance(node, dict) or k not in node:
            return None
        node = node[k]
    return node


def carrier_name(card: dict) -> str:
    sid = str(card.get("subject", {}).get("id", ""))
    if "CARRIER:" in sid:
        return sid.split("CARRIER:", 1)[1].strip()
    return "UNNAMED"


def main() -> int:
    if not SET_CARD.exists():
        print("BLOCKED: set card absent at %s" % SET_CARD)
        return 1
    set_card = json.loads(SET_CARD.read_text(encoding="utf-8"))

    refs = [r.get("id", "") for r in dig(set_card, ("artifact", "location", "projection_of")) or []]
    carrier_paths = [ROOT / r for r in refs
                     if r.endswith(".card.json") and not r.endswith("/stitch-producer-archive-read.card.json")]
    on_disk = sorted(p.name for p in CARDS.glob("*.card.json"))

    print("G2 CARD ROWS -- the card set read as one row per carrier")
    print("  SET CARD: %s" % SET_CARD.relative_to(ROOT).as_posix())
    print("  CARRIER SET DERIVED FROM: the set card's artifact.location.projection_of -- %d card "
          "reference(s) of %d entries total." % (len(carrier_paths), len(refs)))
    print("  UNSCOPED CONTROL on that derivation: %d *.card.json file(s) present in %s -- %s. A "
          "file on disk that the set card does not enumerate would NOT be read here, and this "
          "line is how a reader sees that."
          % (len(on_disk), CARDS.relative_to(ROOT).as_posix(), ", ".join(on_disk)))
    print("  GRAIN: one CARRIER per card; seven Rule 28 questions per carrier; one owner per "
          "question. DENOMINATOR of the completeness counts below: %d carrier(s) x 7 question(s) "
          "= %d row(s)." % (len(carrier_paths), len(carrier_paths) * 7))
    print("")

    complete_q, complete_owner, distinguishable, owners_seen = 0, 0, 0, {}
    carriers, answered_per_carrier = [], []
    for p in carrier_paths:
        if not p.exists():
            print("BLOCKED: card enumerated by the set card is absent on disk: %s" % p)
            return 1
        card = json.loads(p.read_text(encoding="utf-8"))
        name = carrier_name(card)
        carriers.append(name)
        print("=" * 96)
        print("CARRIER %s -- %s" % (name, p.name))

        answered, owned, missing = 0, 0, []
        for grain, label, path, fields in QUESTIONS:
            row = dig(card, path)
            if not isinstance(row, dict):
                missing.append(label + " (row absent)")
                continue
            blanks = [f for f in fields if row.get(f) in (None, "", [], {})
                      and not isinstance(row.get(f), bool)]
            owner = str(row.get("owner", "")).strip()
            basis = str(row.get("basis", "")).strip()
            evid = str(row.get("evidence", "")).strip()
            ok_row = not blanks and basis in ("measured", "inferred", "held", "absent") and len(evid) > 20
            if ok_row:
                answered += 1
            else:
                missing.append("%s (blank fields %s, basis %r, evidence %d chars)"
                               % (label, blanks, basis, len(evid)))
            if owner:
                owned += 1
                owners_seen[owner] = owners_seen.get(owner, 0) + 1
            print("    %-8s %-16s basis=%-9s owner=%-28s evidence=%d chars  vintage_cited=%s"
                  % (grain, label, basis, owner or "MISSING", len(evid), "@" in evid))

        fm = dig(card, ("trust", "failure_mode")) or {}
        dist = str(fm.get("distinguishable_from_true_negative", ""))
        paths_named = fm.get("silent_degrade_paths") or []
        concrete = (dist in ("yes", "no")
                    and len(str(fm.get("returns_on_failure", ""))) >= 80
                    and len(paths_named) >= 1)
        if concrete:
            distinguishable += 1
        answered_per_carrier.append(answered)
        if answered == 7:
            complete_q += 1
        if owned == 7:
            complete_owner += 1
        print("  QUESTIONS ANSWERED: %d of 7   OWNERS PRESENT: %d of 7" % (answered, owned))
        if missing:
            print("  INCOMPLETE: %s" % "; ".join(missing))
        print("  QUESTION 7 ANSWERED CONCRETELY: %s -- distinguishable_from_true_negative=%s, "
              "returns_on_failure %d chars, %d named silent-degrade path(s). An 'unmeasured' here "
              "would be a deferral, not an answer." % (concrete, dist or "MISSING",
                                                       len(str(fm.get("returns_on_failure", ""))),
                                                       len(paths_named)))
        print("  VERDICT ON THIS CARRIER: %s -- %s" % (dig(card, ("verdict", "standing")),
                                                       str(dig(card, ("verdict", "why")))[:150]))

    n = len(carrier_paths)
    print("=" * 96)
    print("OWNER DISTRIBUTION over %d owned row(s) across %d carrier(s) -- the card's own premise, "
          "counted rather than assumed:" % (sum(owners_seen.values()), n))
    for owner, cnt in sorted(owners_seen.items(), key=lambda kv: (-kv[1], kv[0])):
        print("    %-28s %d row(s)" % (owner, cnt))
    print("  %d distinct owner(s) over %d rows. Rule 24(iv) asks whether the remedies move "
          "together; this line is the measurement a reader can argue with." % (len(owners_seen),
                                                                               sum(owners_seen.values())))
    print("")
    print("SUMMARY")
    print("CARD_ROWS=%d of %d carrier(s) -- %s" % (n, 3, ", ".join(carriers)))
    min_answered = min(answered_per_carrier) if answered_per_carrier else 0
    print("QUESTIONS_PER_ROW=%d of 7 (the MINIMUM across carriers, so one incomplete carrier "
          "cannot be averaged away; %d of %d carrier(s) at 7)" % (min_answered, complete_q, n))
    print("OWNER_PER_ROW=%d of %d (carriers whose seven rows each carry an owner)" % (complete_owner, n))
    print("FAILURE_MODE_DISTINGUISHABLE=%d of %d (carriers answering question 7 concretely)"
          % (distinguishable, n))
    ok = (n == 3 and complete_q == 3 and complete_owner == 3 and distinguishable == 3)
    print("SET_COMPLETE=%s" % ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
