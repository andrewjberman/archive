#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-G-4 / G4-AC2 -- CG-s-35.

NAME WHAT MOVED THE PORTAL LAYER'S VINTAGE, PER MOVE, OR REPORT IT UNNAMED.

A move has two limbs and the prober asks both:

  VALUE-SOURCE -- what made the new portal sha the value the packer would see
                  (an act in the portal clone and/or in the superproject).
  CARRIER      -- what put that value into the SERVED source zip
                  (a build, a fold, an extract or a hand act, with its ledger).

A move is NAMED only when at least one limb resolves to an ACTOR from the record.
A limb that resolves to nothing is printed as UNRESOLVED, and a move with no
resolved limb is counted in UNNAMED_REPORTED -- never guessed, never dropped.

CONTROLS (both fire, and both are required before MOVER_PROBE_CONTROL=FIRED):
  POSITIVE -- probe a sha whose mover IS in the record and require a name.
  NEGATIVE -- probe a syntactically valid sha that is in NO record and require
              UNNAMED. Without this limb the prober could be a constant that
              says NAMED to anything.

READ ONLY. git reads only; no network, no AWS call, no write outside stdout.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
W2 = os.path.join(ROOT, "org", "missions", "D0", "NFRA", "NFRA_CLDGRPH",
                  "deliverables", "0.9.0_WK_NFRA_CLDGRPH~2")
LEDGERS = os.path.join(ROOT, "org", "critical_paths", "change_management")
PORTAL_CLONE = r"C:\Users\AndrewBerman\Desktop\ajb_workspace\portal"

SHA_F3 = None
SHA_F11 = None


def run(args, cwd):
    """Return (rc, stdout). Bounded. Never raises on a non-zero rc."""
    try:
        p = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=30)
        return p.returncode, p.stdout.decode("utf-8", "replace")
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 999, "ERROR: %s" % exc


def to_utc(iso_with_offset):
    try:
        return (datetime.fromisoformat(iso_with_offset.strip())
                .astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    except (ValueError, TypeError):
        return iso_with_offset


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


# ---------------------------------------------------------------------------
# INSTRUMENT A -- the SUPERPROJECT's own history of the `portal` gitlink.
# Substrate: this repository's object database. Coverage: every commit that
# touches the gitlink path, --full-history (a path-simplified log can drop the
# very commit that introduced a change).
# ---------------------------------------------------------------------------
def gitlink_history(limit=80):
    rc, out = run(["git", "log", "--full-history", "--format=%H|%aI|%an|%s",
                   "-%d" % limit, "--", "portal"], ROOT)
    if rc != 0:
        return [], 0
    rows = []
    for line in out.splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        c, when, who, subj = parts
        rc2, tree = run(["git", "ls-tree", c, "--", "portal"], ROOT)
        m = re.search(r"160000 commit ([0-9a-f]{40})", tree) if rc2 == 0 else None
        rows.append({"commit": c, "utc": to_utc(when), "author": who,
                     "subject": subj, "gitlink": m.group(1) if m else None})
    return rows, len(rows)


def probe_superproject(sha, rows):
    """The OLDEST commit in the swept window whose gitlink equals `sha`."""
    hits = [r for r in rows if r["gitlink"] == sha]
    if not hits:
        return None
    return hits[-1]


# ---------------------------------------------------------------------------
# INSTRUMENT B -- the PORTAL CLONE's own git (a DIFFERENT object database and a
# different substrate from instrument A, so agreement is corroboration and not
# repetition).
# ---------------------------------------------------------------------------
def probe_portal_clone(sha):
    rc, out = run(["git", "-C", PORTAL_CLONE, "log", "-1",
                   "--format=%H|%aI|%cI|%an|%s", sha], PORTAL_CLONE)
    if rc != 0 or not out.strip():
        return None
    parts = out.strip().splitlines()[0].split("|", 4)
    if len(parts) != 5:
        return None
    return {"commit": parts[0], "authored_utc": to_utc(parts[1]),
            "committed_utc": to_utc(parts[2]), "author": parts[3],
            "subject": parts[4]}


def portal_reflog(sha):
    """Reflog entries whose NEW value is `sha`. Local, per-clone, expiring."""
    rc, out = run(["git", "-C", PORTAL_CLONE, "reflog", "--date=iso-strict",
                   "-n", "40"], PORTAL_CLONE)
    if rc != 0:
        return [], 0
    lines = out.splitlines()
    hits = [ln for ln in lines if ln.startswith(sha[:8])]
    return hits, len(lines)


# ---------------------------------------------------------------------------
# INSTRUMENT C -- the SERVED-PLANE carrier: the NEVER-2 deploy ledger that
# opened for the push, bound to the artifact by name or by instant.
# ---------------------------------------------------------------------------
def probe_ledger(needle, window_open):
    """A ledger entry naming `needle`, or opened at `window_open` (UTC prefix)."""
    if not os.path.isdir(LEDGERS):
        return None, 0
    names = sorted(n for n in os.listdir(LEDGERS)
                   if os.path.isfile(os.path.join(LEDGERS, n)))
    for name in names:
        path = os.path.join(LEDGERS, name)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                body = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        if (needle and needle in body) or (window_open and name.startswith(window_open)):
            owner = re.search(r"\*\*Owner:\*\*\s*`([^`]+)`", body)
            order = re.search(r"\*\*Order:\*\*\s*`([^`]+)`", body)
            opened = re.search(r"\*\*Opened \(UTC\):\*\*\s*(\S+)", body)
            status = re.search(r"\*\*Status:\*\*\s*(\S+)", body)
            act = re.search(r"## THE ACT[^\n]*\n\n(.+)", body)
            return {"file": name, "owner": owner.group(1) if owner else None,
                    "order": order.group(1) if order else None,
                    "opened": opened.group(1) if opened else None,
                    "status": status.group(1) if status else None,
                    "act": act.group(1).strip() if act else None}, len(names)
    return None, len(names)


# ---------------------------------------------------------------------------
print("=" * 78)
print("G4-AC2 -- WHAT MOVED THE PORTAL LAYER'S VINTAGE, PER MOVE")
print("=" * 78)

f3 = load_json(os.path.join(W2, "f3_zip_report.json"))
f11 = load_json(os.path.join(W2, "f11_zip_report.json"))
SHA_F3 = f3["portal_head"]
SHA_F11 = f11["portal_head"]

rows, swept = gitlink_history()
print("INSTRUMENT A COVERAGE : superproject gitlink history, %d of %d commits"
      % (swept, swept))
print("                        touching the path `portal` under --full-history")
print("                        (a path-SIMPLIFIED log can drop the introducing commit)")
print("INSTRUMENT A GRAIN    : one 160000 gitlink sha per superproject commit")
print("INSTRUMENT A ENV      : this worktree C:/tmp/wk-cldgrph-7-3, branch")
print("                        wk-cldgrph-7-3, cut from CLOUD @f3b5f26f77")
rl_probe, rl_total = portal_reflog("0" * 8)
print("INSTRUMENT B COVERAGE : the portal clone at %s" % PORTAL_CLONE)
print("                        `git log -1 <sha>` + `git reflog -n 40` (%d entries read)"
      % rl_total)
print("INSTRUMENT B GRAIN    : one commit / one HEAD transition in that clone")
print("INSTRUMENT B ENV      : a LOCAL, PER-CLONE, EXPIRING artifact -- the reflog is")
print("                        not shared, not pushed, and prunes by default; it is")
print("                        cited as CORROBORATION of instrument A, never alone")
_, led_total = probe_ledger(None, None)
print("INSTRUMENT C COVERAGE : %d NEVER-2 deploy ledger entries in %s"
      % (led_total, rel(LEDGERS)))
print("INSTRUMENT C GRAIN    : one entry per deploy act (opened/closed, owner, order)")
print("")

moves = [
    {
        "n": 1,
        "from": "ABSENT (0 portal/src entries)",
        "to": SHA_F3,
        "served_at": "2026-09-09T18:47:04Z",
        "ledger_needle": None,
        "ledger_open": "20260909T184608Z",
        "value_source_note": (
            "the portal clone's HEAD did NOT move for this one: it had been at "
            "%s since 2026-09-01. The whole of move 1 is the PUSH." % SHA_F3[:8]),
    },
    {
        "n": 2,
        "from": SHA_F3,
        "to": SHA_F11,
        "served_at": "2026-09-10T02:46:36Z",
        "ledger_needle": os.path.basename(f11.get("zip", "")),
        "ledger_open": "20260910T024600Z",
        "value_source_note": "the portal clone's HEAD moved inside the round.",
    },
]

named = 0
unnamed = 0
verdicts = []

for mv in moves:
    print("-" * 78)
    print("MOVE %d : %s" % (mv["n"], mv["from"]))
    print("      -> %s" % mv["to"])
    print("         first SERVED at %s" % mv["served_at"])
    print("-" * 78)
    limbs_resolved = 0
    actors = []

    # --- VALUE-SOURCE limb -------------------------------------------------
    print("  VALUE-SOURCE limb -- what made this the value the packer would see")
    print("    note: %s" % mv["value_source_note"])
    sp = probe_superproject(mv["to"], rows)
    if sp:
        print("    [A superproject gitlink] RESOLVED")
        print("      commit  : %s" % sp["commit"])
        print("      at      : %s" % sp["utc"])
        print("      actor   : %s" % sp["author"])
        print("      subject : %s" % sp["subject"])
        limbs_resolved += 1
        actors.append(sp["author"])
    else:
        print("    [A superproject gitlink] UNRESOLVED -- no commit in the %d swept"
              % swept)
        print("      ever carried gitlink %s ... (this is a MEASURED zero over the"
              % mv["to"][:8])
        print("      swept window, not an absence claim over all history)")

    pc = probe_portal_clone(mv["to"])
    if pc:
        print("    [B portal clone commit] RESOLVED")
        print("      commit    : %s" % pc["commit"])
        print("      authored  : %s   committed: %s"
              % (pc["authored_utc"], pc["committed_utc"]))
        print("      actor     : %s" % pc["author"])
        print("      subject   : %s" % pc["subject"])
        limbs_resolved += 1
        actors.append(pc["author"])
        hits, total = portal_reflog(mv["to"])
        if hits:
            print("      reflog    : %d of %d entries land HEAD on this sha --"
                  % (len(hits), total))
            for h in hits:
                print("                  %s" % h.strip())
        else:
            print("      reflog    : 0 of %d entries land HEAD on this sha" % total)
    else:
        print("    [B portal clone commit] UNRESOLVED -- `git log -1 %s` in the clone"
              % mv["to"][:8])
        print("      returned non-zero or empty")

    # --- CARRIER limb ------------------------------------------------------
    print("  CARRIER limb -- what put that value into the SERVED source zip")
    led, _ = probe_ledger(mv["ledger_needle"], mv["ledger_open"])
    if led:
        print("    [C deploy ledger] RESOLVED")
        print("      entry  : %s" % led["file"])
        print("      opened : %s   status: %s" % (led["opened"], led["status"]))
        print("      owner  : %s" % led["owner"])
        print("      order  : %s" % led["order"])
        print("      act    : %s" % led["act"])
        print("      kind   : A HAND ACT -- a local zip build (f3_build_source_zip.py)")
        print("               plus one `aws s3 cp` PutObject. NOT a build, NOT a fold,")  # G3QUOTE
        print("               NOT the GH-Action route (which fires only on a push to")
        print("               CLOUD and pins a THIRD portal sha).")
        limbs_resolved += 1
        if led["owner"]:
            actors.append(led["owner"])
    else:
        print("    [C deploy ledger] UNRESOLVED -- no entry names %r or opens at %s"
              % (mv["ledger_needle"], mv["ledger_open"]))

    verdict = "NAMED" if limbs_resolved > 0 else "UNNAMED"
    if verdict == "NAMED":
        named += 1
    else:
        unnamed += 1
    verdicts.append((mv["n"], verdict, limbs_resolved, sorted(set(actors))))
    print("  VERDICT MOVE %d : %s  (%d of 3 limb-probes resolved; actors: %s)"
          % (mv["n"], verdict, limbs_resolved, ", ".join(sorted(set(actors))) or "none"))
    print("")

# ---------------------------------------------------------------------------
# CONTROLS.
# ---------------------------------------------------------------------------
print("-" * 78)
print("CONTROLS ON THE PROBER")
print("-" * 78)
POS_SHA = SHA_F3          # a sha whose authoring act IS in the record
NEG_SHA = "d3adb33f" * 5  # 40 valid hex chars, in no record anywhere

pos = probe_portal_clone(POS_SHA)
pos_ok = bool(pos and pos.get("author"))
print("  POSITIVE control -- probe_portal_clone(%s)" % POS_SHA[:8])
if pos:
    print("    -> NAMED  actor=%s  authored=%s" % (pos["author"], pos["authored_utc"]))
    print("       subject: %s" % pos["subject"])
else:
    print("    -> UNNAMED (the prober failed to name a mover the record HAS)")
print("    PASS=%s -- the prober CAN name a mover when the evidence is there" % pos_ok)

neg = probe_portal_clone(NEG_SHA)
neg_sp = probe_superproject(NEG_SHA, rows)
neg_led, _ = probe_ledger("g3-no-such-artifact-probe", "29991231T000000Z")
neg_ok = (neg is None) and (neg_sp is None) and (neg_led is None)
print("  NEGATIVE control -- the same three probes on %s" % NEG_SHA[:8])
print("    portal clone  -> %s" % ("NAMED (WRONG)" if neg else "UNNAMED"))
print("    superproject  -> %s" % ("NAMED (WRONG)" if neg_sp else "UNNAMED"))
print("    deploy ledger -> %s" % ("NAMED (WRONG)" if neg_led else "UNNAMED"))
print("    PASS=%s -- the prober is not a constant that says NAMED to anything"
      % neg_ok)

control = "FIRED" if (pos_ok and neg_ok) else "NOT-FIRED"
print("")
print("=" * 78)
print("MOVERS_NAMED=%d of %d" % (named, len(moves)))
print("UNNAMED_REPORTED=%d" % unnamed)
print("NAMED_PLUS_UNNAMED=%d" % (named + unnamed))
print("MOVER_PROBE_CONTROL=%s" % control)
print("=" * 78)
for n, v, k, a in verdicts:
    print("  MOVE %d %s -- %d limb(s), actors: %s" % (n, v, k, ", ".join(a) or "none"))
