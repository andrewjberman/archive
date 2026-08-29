#!/usr/bin/env python3
"""D1_CATVIEWS.TS1-AC2 -- STAGED SCORER for the served L2 render.

CRITERION (verbatim from D1_CATVIEWS.TO-S1-DE.per-client-row-suppression):
    TS1-AC2  "HIS WORKED CASE IS THE ACCEPTANCE TEST, BOTH DIRECTIONS. `Opal Fixed
              Income` RENDERS for Cottonwood and IS ABSENT for Inflection under
              `Custom Models`. Exhibit BOTH -- an absence with no positive control
              proves nothing."

WHAT THIS SCORES, STATED SO NOBODY OVER-READS IT
    Plane: the SERVED `category-views.json` object, evaluated through the SHIPPED
    render gate chain. It answers "does the shipped renderer put this row on the
    page, given these served bytes" -- NOT "were these pixels drawn". The pixel
    question is TS1-AC3's, which requires a rendered before/after READ by an agent
    and is deliberately NOT mechanised here.
    A PASS from this tool is therefore: the served bytes + the shipped predicate
    chain produce RENDERS at cottonwood and ABSENT at inflection.

WHY IT IS AN INSTRUMENT AND NOT A RE-STATEMENT OF ONE LINE
    Five DIFFERENT gates in CategoryViewTree.tsx can each independently make a row
    absent. Four of them make it absent for a reason that has nothing to do with
    Andrew's rule. An "is it absent?" check that does not say WHICH gate fired
    scores a broken build as a pass, because the absence half looks identical.
    This tool walks the chain and NAMES the gate.

  G0  the L0 node exists in `nodes`                            (absent -> WRONG-CAUSE)
  G1  node.predicate !== 'unavailable'      :273-274           (absent -> WRONG-CAUSE)
  G2  the L1 row survives the L1 sibling guard   :274          (absent -> WRONG-CAUSE)
  G3  rows.length > 0, so the block renders at all  :321       (absent -> WRONG-CAUSE)
  G4  canL2: the drill is enabled                   :329       (absent -> WRONG-CAUSE)
  G5  the member survives the L2 sibling guard      :198       (absent -> ON-RULE)
    ONLY a G5 absence is the criterion being satisfied. G0-G4 absences are the
    feature being deleted by something else, and this tool reports them as FAIL.

THE PREDICATE IS NOT MINE AND THIS FILE IS ITS SECOND CARRIER
    `_visible_constituents` below is a PORT of `visibleConstituents`
    (portal/src/components/CategoryViewTree.tsx:135-139). Two durable records of
    one rule drift from minute one. So the TSX is the NAMED PRIMARY and this file
    pins its normalized sha256: if the primary moves, the fidelity self-test
    REFUSES rather than scoring against a stale copy. A scorer that silently keeps
    using yesterday's predicate is worse than no scorer.

TIMING -- THE GUARD IS IN THE TOOL, NOT IN THE INVOKER'S HEAD
    Three fires, two EventBridge planes:
        13:00Z  etf-positioning-producer   (RULES)      -> D4, not this criterion
        13:30Z  mdpf-gold-lambda           (SCHEDULER)  -> the GOLD rung
        13:50Z  mdpf-portal-publisher      (SCHEDULER)  -> THE SERVED OBJECT  <- this one
    A run at 13:30Z reads the pre-publish object, sees the OLD values, and reports
    a CORRECT fix as FAILED. So freshness is decided from `_provenance.written_at`
    INSIDE the bytes -- never the wall clock, never the invoker's assurance. The
    vintage travels with the artifact (2.0.0_SA_COO~Z 13878).

NULL IS NOT 0.00
    A member with no dollars emits null deliberately. This tool NEVER coalesces
    null to 0: it reports four distinct member states (VALUE / ZERO / NULL /
    ABSENT-KEY) with denominators, so a build where nothing is mapped cannot be
    read as a build where everything is legitimately zero. Note the shipped rule
    treats NULL and ZERO the SAME at render time (Andrew's overrule) -- the
    distinction is kept for the DIAGNOSIS, which is where it does the work.

NEGATIVE CONTROL -- PINNED TO A COMMIT, NOT TO A MINUTE
    3.0.0_SA_CVO~Z's pre-fix baseline, 4 of 4 scopes, at bc9d11dd8e (on
    origin/SITEZ, is-ancestor verified with a discriminating negative control).
    Those bytes carry as_of 2026-08-27 / written_at 2026-08-28T13:50:49-51Z, and
    the fix deployed at 17:28:29Z -- ~3.6h LATER, so their pre-fix status is
    STRUCTURAL, not a lucky fetch window.
    PRECISION CARRIED VERBATIM FROM ITS MEASURER: those are the SERVED bytes as
    delivered through the edge, sha256-pinned at capture. They are NOT claimed
    byte-identical to an `s3api` read -- that comparison was never run. This tool
    stamps which source every verdict came from, for exactly that reason.
    No second snapshot is taken here. One fact, one named primary.

USAGE
    --self-test                      both arms against bc9d11dd8e. Run this first.
    --from-git [COMMIT]              score committed bytes (control arm)
    --from-file DIR                  score a directory of category-views.<scope>.json
    --from-s3 BUCKET                 score `aws s3api get-object` bytes (DIFFERENT
                                     plane from the edge -- stamped as such)
    --from-edge BASE_URL             score the bytes the portal actually fetches
                                     (--bearer required; mint from /auth/login)
    --control                        bypass the freshness guard, stamp the output
                                     LOUDLY. For the failability arm only.

EXIT CODES
    0  PASS       both directions satisfied, on-rule
    1  FAIL       criterion not met (the cause is named)
    2  BLOCKED    not scoreable yet (pre-publish / unreachable source)
    3  REFUSED    the predicate primary drifted; this file is stale

0.4.0_DE_ClientPlatform~Z -- D1_CATVIEWS.TO-S1-DE
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

# --------------------------------------------------------------------------
# PINS
# --------------------------------------------------------------------------

# this file lives at org/tier2_senior/<serial>/deliverables/, so the workspace
# root is five levels up. Counted, not guessed -- an off-by-one here makes the
# fidelity check read a path that does not exist and REFUSE, which is the safe
# direction but still the wrong answer.
REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..")
)

PREDICATE_SOURCE = "portal/src/components/CategoryViewTree.tsx"
PREDICATE_FN = "visibleConstituents"
# sha256 of the whitespace-normalized function text, read at source 2026-08-28
# from portal @192b086562 (portal DEV working tree).
PREDICATE_PIN = "638473a474a5886d9a3a06e0dacaf117f3c139e442966bfc0b84fb4a5de391dd"

BASELINE_COMMIT = "bc9d11dd8e"
BASELINE_DIR = (
    "org/tier1_exec/3.0.0_SA_CVO/deliverables/cvoZ_D1_PREDEPLOY_BASELINE_20260828"
)

# The 4 SERVED scopes. This is the denominator for any coverage claim.
SERVED_SCOPES = ("global", "49financial", "cottonwood", "inflection")

# TS1-AC2's worked case. `Custom Models` = L0 `Models` -> L1 `Custom`.
L0_NODE = "Models"
L1_NODE = "Custom"
# Join on the STABLE key. `display_name` is "Fixed Income", Andrew says "Opal Fixed
# Income", and the member_id is "opal_fixed_income" -- three renderings of one
# thing, and matching on the prose is how a grain mismatch manufactures an absence.
MEMBER_ID = "opal_fixed_income"

RENDERS_SCOPE = "cottonwood"
ABSENT_SCOPE = "inflection"

# The producer vintage carried by the pre-fix control. A FAIL while as_of is STILL
# this value means the GOLD rung emitted no new values -- a different fault from
# "the fix did not work", and the two are indistinguishable from the verdict alone.
# Reported, never refused on: a vintage that has not moved is the ordinary Monday
# (and post-holiday) state, and refusing on it false-alarms every such morning.
CONTROL_AS_OF = "2026-08-27"

# The publisher writes the served object at ~13:50Z. Boundary is UTC.
PUBLISHER_HOUR_UTC = 13
PUBLISHER_MINUTE_UTC = 50

# Member states. Deliberately four, not two.
ST_VALUE = "VALUE"        # a real number, non-zero
ST_ZERO = "ZERO"          # explicitly 0 -- a measurement someone took
ST_NULL = "NULL"          # key present, null -- deliberate "no dollars"
ST_ABSENT = "ABSENT-KEY"  # no `aum` key at all -- nobody has mapped it


class Refused(Exception):
    """The instrument cannot be trusted to answer. Never scored as FAIL."""


class Blocked(Exception):
    """The subject is not scoreable yet. Never scored as FAIL."""


# --------------------------------------------------------------------------
# FIDELITY -- the primary carrier is the TSX, not this file
# --------------------------------------------------------------------------

def read_predicate_source(repo_root: str) -> str:
    path = os.path.join(repo_root, PREDICATE_SOURCE)
    if not os.path.exists(path):
        raise Refused(
            "predicate primary not found at %s -- cannot verify this port is current"
            % path
        )
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    # Grab from the function keyword to its closing brace at column 0.
    m = re.search(
        r"^function\s+" + PREDICATE_FN + r"\b.*?^\}", text, re.S | re.M
    )
    if not m:
        raise Refused(
            "function %s no longer found in %s -- the shipped predicate was renamed "
            "or removed; this port is stale by construction"
            % (PREDICATE_FN, PREDICATE_SOURCE)
        )
    return m.group(0)


def fidelity_check(repo_root: str) -> Tuple[bool, str, str]:
    """Return (ok, actual_sha, normalized_text). Raises Refused if unreadable."""
    src = read_predicate_source(repo_root)
    norm = re.sub(r"\s+", " ", src).strip()
    sha = hashlib.sha256(norm.encode("utf-8")).hexdigest()
    return (sha == PREDICATE_PIN, sha, norm)


# --------------------------------------------------------------------------
# THE PORTED PREDICATE  (CategoryViewTree.tsx:135-139)
# --------------------------------------------------------------------------

def _is_mapped(aum: Any, key_present: bool) -> bool:
    """TS: `i.aum !== null && i.aum !== undefined`.

    JS has no "key absent" distinct from undefined, so a missing key and an
    explicit null are BOTH unmapped there. Kept faithful on purpose -- the four
    states are separated for the DIAGNOSIS below, never inside the predicate.
    """
    if not key_present:
        return False
    return aum is not None


def _visible_constituents(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Port of visibleConstituents. THE SIBLING GUARD IS THE SAFETY PROPERTY.

    When NOTHING at a level carries a value, that is the producer not having
    mapped it and NOTHING is suppressed -- a flat "suppress null or zero" would
    delete the whole L2 layer with no error state. When SOME sibling carries a
    value, a null or zero beside it genuinely means "not held" and it goes.
    A NEGATIVE VALUE IS MONEY AND STAYS -- the test is `!= 0`, never `> 0`.
    """
    any_mapped = any(_is_mapped(i.get("aum"), "aum" in i) for i in items)
    if not any_mapped:
        return list(items)
    return [
        i
        for i in items
        if _is_mapped(i.get("aum"), "aum" in i) and i.get("aum") != 0
    ]


def member_state(item: Dict[str, Any]) -> str:
    if "aum" not in item:
        return ST_ABSENT
    v = item.get("aum")
    if v is None:
        return ST_NULL
    if v == 0:
        return ST_ZERO
    return ST_VALUE


# --------------------------------------------------------------------------
# THE GATE CHAIN
# --------------------------------------------------------------------------

RENDERS = "RENDERS"
ABSENT = "ABSENT"

# Only G5 is Andrew's rule doing its job. Everything else is a different
# mechanism removing the row, and must never be scored as the criterion met.
ON_RULE_GATE = "G5"


def evaluate(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Walk the shipped render chain for MEMBER_ID under L0_NODE > L1_NODE."""
    out = {
        "verdict": None,
        "gate": None,
        "why": None,
        "on_rule": False,
        "member_state": None,
        "sibling_states": {},
        "sibling_denominator": 0,
        "l1_aum": None,
        "any_mapped_at_l2": None,
    }

    nodes = doc.get("nodes") or {}

    # G0 -- the L0 node exists at all.
    node = nodes.get(L0_NODE)
    if node is None:
        out.update(
            verdict=ABSENT, gate="G0",
            why="L0 node %r is not in the served object at all" % L0_NODE,
        )
        return out

    # G1 -- predicate unavailable blanks the whole child list (:273-274).
    if node.get("predicate") == "unavailable":
        out.update(
            verdict=ABSENT, gate="G1",
            why="%r carries predicate='unavailable', so rows=[] and EVERY L1/L2 "
                "row under it is gone regardless of any AUM" % L0_NODE,
        )
        return out

    # G2 -- the L1 sibling guard runs over the L1 children (:274).
    children = node.get("children") or {}
    # Faithful to l1RowsOf: the guard reads `aum` off the child node.
    l1_rows_keyed = []
    for label, child in children.items():
        row = dict(child)
        row["_key"] = label
        l1_rows_keyed.append(row)
    visible_l1 = _visible_constituents(l1_rows_keyed)
    visible_l1_keys = [r["_key"] for r in visible_l1]

    if L1_NODE not in children:
        out.update(
            verdict=ABSENT, gate="G2",
            why="L1 node %r is not among %r's children (%d children served)"
                % (L1_NODE, L0_NODE, len(children)),
        )
        return out

    out["l1_aum"] = children[L1_NODE].get("aum")

    if L1_NODE not in visible_l1_keys:
        out.update(
            verdict=ABSENT, gate="G2",
            why="L1 row %r was suppressed by the L1 sibling guard (its own aum=%r "
                "beside mapped siblings), so its L2 drawer is unreachable"
                % (L1_NODE, children[L1_NODE].get("aum")),
        )
        return out

    # G3 -- the block only renders when rows survive (:321).
    if len(visible_l1) == 0:
        out.update(
            verdict=ABSENT, gate="G3",
            why="no L1 row survived, so the whole %r block does not render" % L0_NODE,
        )
        return out

    # G4/G5 -- the L2 sibling guard (:198), and the drill gate that reads it (:329).
    members = children[L1_NODE].get("members") or []
    out["sibling_denominator"] = len(members)
    states = {}
    for m in members:
        states[m.get("member_id")] = member_state(m)
    out["sibling_states"] = states
    out["member_state"] = states.get(MEMBER_ID)
    out["any_mapped_at_l2"] = any(
        _is_mapped(m.get("aum"), "aum" in m) for m in members
    )

    if MEMBER_ID not in states:
        out.update(
            verdict=ABSENT, gate="G2",
            why="member %r is not carried under %s > %s at all (%d members served) "
                "-- absent from the REGISTRY, not suppressed by the rule"
                % (MEMBER_ID, L0_NODE, L1_NODE, len(members)),
        )
        return out

    visible = _visible_constituents(members)
    visible_ids = [m.get("member_id") for m in visible]

    # G4 -- if nothing survives, the chevron is disabled and L2 never opens.
    if len(visible) == 0:
        out.update(
            verdict=ABSENT, gate="G4",
            why="no member survived the L2 guard, so canL2=false and the %r drawer "
                "cannot be opened at all" % L1_NODE,
        )
        return out

    if MEMBER_ID in visible_ids:
        out.update(
            verdict=RENDERS, gate=ON_RULE_GATE,
            why="member survives the L2 sibling guard (state=%s, any_mapped=%s)"
                % (out["member_state"], out["any_mapped_at_l2"]),
            on_rule=True,
        )
        return out

    out.update(
        verdict=ABSENT, gate=ON_RULE_GATE,
        why="member suppressed by the L2 sibling guard (state=%s) while %d of %d "
            "siblings carry a mapped value -- this is Andrew's rule firing"
            % (out["member_state"],
               sum(1 for m in members if _is_mapped(m.get("aum"), "aum" in m)),
               len(members)),
        on_rule=True,
    )
    return out


# --------------------------------------------------------------------------
# FRESHNESS -- decided from the bytes, never the clock or the invoker
# --------------------------------------------------------------------------

def _parse_iso_z(s: str) -> dt.datetime:
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=dt.timezone.utc
    )


def last_publisher_boundary(now: dt.datetime) -> dt.datetime:
    """The most recent ~13:50Z publisher boundary at or before `now` (UTC)."""
    today = now.replace(
        hour=PUBLISHER_HOUR_UTC, minute=PUBLISHER_MINUTE_UTC,
        second=0, microsecond=0,
    )
    if now >= today:
        return today
    return today - dt.timedelta(days=1)


def freshness(doc: Dict[str, Any], now: dt.datetime) -> Dict[str, Any]:
    """BLOCKED if the served object predates the publisher run we must score."""
    prov = doc.get("_provenance") or {}
    written_at = prov.get("written_at")
    if not written_at:
        raise Blocked(
            "the object carries no _provenance.written_at, so its vintage cannot "
            "be read from the bytes -- refusing to fall back to the wall clock"
        )
    w = _parse_iso_z(written_at)
    boundary = last_publisher_boundary(now)
    return {
        "written_at": written_at,
        "as_of": doc.get("as_of"),
        "written_by": prov.get("written_by"),
        "boundary": boundary.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stale": w < boundary,
        "age_h": round((now - w).total_seconds() / 3600.0, 2),
    }


# --------------------------------------------------------------------------
# SOURCES -- every verdict is stamped with which plane it came from
# --------------------------------------------------------------------------

def src_git(scope: str, commit: str, repo_root: str) -> Dict[str, Any]:
    path = "%s/category-views.%s.json" % (BASELINE_DIR, scope)
    ref = "%s:%s" % (commit, path)
    env = dict(os.environ)
    env["MSYS_NO_PATHCONV"] = "1"
    # Never 2>/dev/null a git show: a mangled path returns clean-empty and an
    # ABSENT verdict then looks identical to a real one.
    p = subprocess.run(
        ["git", "show", ref], cwd=repo_root, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if p.returncode != 0 or not p.stdout.strip():
        raise Blocked(
            "git show %s returned rc=%d, %d bytes. stderr: %s"
            % (ref, p.returncode, len(p.stdout), p.stderr.decode("utf-8", "replace").strip())
        )
    return json.loads(p.stdout.decode("utf-8"))


def src_file(scope: str, directory: str) -> Dict[str, Any]:
    path = os.path.join(directory, "category-views.%s.json" % scope)
    if not os.path.exists(path):
        raise Blocked("no such file: %s" % path)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def src_s3(scope: str, bucket: str, repo_root: str) -> Dict[str, Any]:
    key = "platinum/mdpf/%s/category-views.json" % scope
    dest = os.path.join(
        os.environ.get("TEMP", "/tmp"), "ts1ac2_%s.json" % scope
    )
    aws = os.path.join(repo_root, ".tools", "aws")
    p = subprocess.run(
        [aws, "s3api", "get-object", "--bucket", bucket, "--key", key, dest],
        cwd=repo_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if p.returncode != 0:
        raise Blocked(
            "s3api get-object s3://%s/%s rc=%d: %s"
            % (bucket, key, p.returncode,
               p.stderr.decode("utf-8", "replace").strip())
        )
    with open(dest, "r", encoding="utf-8") as fh:
        return json.load(fh)


def src_edge(scope: str, base_url: str, bearer: Optional[str]) -> Dict[str, Any]:
    import urllib.error
    import urllib.request

    url = "%s/api/general/mdpf/%s/category-views.json" % (
        base_url.rstrip("/"), scope,
    )
    req = urllib.request.Request(url)
    if bearer:
        req.add_header("Authorization", "Bearer %s" % bearer)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # A 401 here is the classic default-render failure: the route guard
        # passes on a stub while the edge 401s the data. Never a criterion FAIL.
        raise Blocked("GET %s -> HTTP %d %s" % (url, e.code, e.reason))
    except Exception as e:  # noqa: BLE001 -- any transport failure is BLOCKED
        raise Blocked("GET %s -> %s" % (url, e))


# --------------------------------------------------------------------------
# SCORING
# --------------------------------------------------------------------------

def _frontier_note(now: dt.datetime) -> str:
    """Expected T-1 trading frontier, via the ONE frontier in lib/trading_calendar.

    Defensive by design: a diagnostic hint must never be able to crash a scorer.
    If the calendar cannot be loaded the note says so rather than guessing.
    """
    try:
        if REPO_ROOT not in sys.path:
            sys.path.insert(0, REPO_ROOT)
        from lib.trading_calendar import calendar_source, expected_last_trading_day

        exp = expected_last_trading_day(now.date())
        return ("expected last trading day is %s (calendar: %s); today is %s"
                % (exp.isoformat(), calendar_source(), now.strftime("%A")))
    except Exception as e:  # noqa: BLE001 -- a hint, never a failure path
        return ("lib.trading_calendar unavailable (%s), so count trading days by "
                "hand before concluding" % e)


def fmt_states(states: Dict[str, str]) -> str:
    counts = {}
    for v in states.values():
        counts[v] = counts.get(v, 0) + 1
    n = len(states)
    return ", ".join(
        "%s %d of %d" % (k, counts[k], n) for k in sorted(counts)
    ) or "(no members)"


def score(loader, source_label, control, now, out=sys.stdout):
    """Returns an exit code. `loader(scope) -> doc`."""
    print("", file=out)
    print("D1_CATVIEWS.TS1-AC2 -- served L2 render scorer", file=out)
    print("  SOURCE PLANE : %s" % source_label, file=out)
    print("  SUBJECT      : %s > %s > %s" % (L0_NODE, L1_NODE, MEMBER_ID), file=out)
    print("  DIRECTIONS   : RENDERS@%s  +  ABSENT@%s (both required)"
          % (RENDERS_SCOPE, ABSENT_SCOPE), file=out)
    if control:
        print("  ** CONTROL RUN -- freshness guard BYPASSED. This output is a "
              "FAILABILITY exercise, NOT a score of the live plane. **", file=out)
    print("", file=out)

    results = {}
    for scope in (RENDERS_SCOPE, ABSENT_SCOPE):
        doc = loader(scope)
        fr = freshness(doc, now)
        if fr["stale"] and not control:
            raise Blocked(
                "BLOCKED at scope %s: written_at %s PREDATES the publisher "
                "boundary %s (object is %.2fh old). Scoring now would read the "
                "PRE-PUBLISH object and report a correct fix as FAILED. This is "
                "the 13:30Z-vs-13:50Z trap; wait for the publisher."
                % (scope, fr["written_at"], fr["boundary"], fr["age_h"])
            )
        ev = evaluate(doc)
        results[scope] = (fr, ev)

        print("  [%s]" % scope, file=out)
        print("     vintage    : as_of %s | written_at %s | by %s"
              % (fr["as_of"], fr["written_at"], fr["written_by"]), file=out)
        print("     freshness  : %s (boundary %s)"
              % ("STALE" if fr["stale"] else "OK", fr["boundary"]), file=out)
        print("     L1 %-9s: aum=%r" % (L1_NODE, ev["l1_aum"]), file=out)
        print("     L2 states  : %s" % fmt_states(ev["sibling_states"]), file=out)
        print("     any_mapped : %r  (sibling guard %s)"
              % (ev["any_mapped_at_l2"],
                 "ACTIVE -- suppressing" if ev["any_mapped_at_l2"]
                 else "INERT -- nothing mapped, nothing suppressed"), file=out)
        print("     subject    : state=%s" % ev["member_state"], file=out)
        print("     VERDICT    : %s at gate %s%s"
              % (ev["verdict"], ev["gate"],
                 "" if ev["on_rule"] else "   <- NOT the rule's gate"), file=out)
        print("     why        : %s" % ev["why"], file=out)
        print("", file=out)

    fr_r, ev_r = results[RENDERS_SCOPE]
    fr_a, ev_a = results[ABSENT_SCOPE]

    findings = []
    if ev_r["verdict"] != RENDERS:
        findings.append(
            "POSITIVE DIRECTION FAILED: %s must RENDER for %s, but it is %s "
            "(gate %s). %s" % (MEMBER_ID, RENDERS_SCOPE, ev_r["verdict"],
                               ev_r["gate"], ev_r["why"])
        )
    if ev_a["verdict"] != ABSENT:
        findings.append(
            "ABSENCE DIRECTION FAILED: %s must be ABSENT for %s, but it %s "
            "(gate %s). %s" % (MEMBER_ID, ABSENT_SCOPE, ev_a["verdict"],
                               ev_a["gate"], ev_a["why"])
        )
    elif not ev_a["on_rule"]:
        findings.append(
            "ABSENCE IS AT THE WRONG GATE: %s is absent for %s, but at gate %s, "
            "not %s. The row is being removed by a DIFFERENT mechanism; the "
            "criterion is about the suppression rule, and an absence produced by "
            "anything else is the feature breaking, not the rule working. %s"
            % (MEMBER_ID, ABSENT_SCOPE, ev_a["gate"], ON_RULE_GATE, ev_a["why"])
        )

    if findings:
        print("  RESULT: FAIL  (%d finding(s))" % len(findings), file=out)
        for f in findings:
            print("    ERROR: %s" % f, file=out)
        stalled = [
            s for s in (RENDERS_SCOPE, ABSENT_SCOPE)
            if results[s][0]["as_of"] == CONTROL_AS_OF
        ]
        if stalled:
            print("", file=out)
            print("    WARN: ATTRIBUTION -- as_of is STILL %s at %s (%d of 2 scopes "
                  "scored). The publisher wrote a fresh object, so the freshness "
                  "guard correctly stood down, but the PRODUCER VINTAGE HAS NOT "
                  "MOVED. A FAIL here may be the gold rung emitting no new values "
                  "rather than the fix failing -- those are different faults with "
                  "different owners, and the verdict alone cannot separate them."
                  % (CONTROL_AS_OF, ", ".join(stalled), len(stalled)), file=out)
            print("    WARN: resolve it on the TRADING CALENDAR before calling "
                  "anything broken -- %s. Friday IS Monday's answer."
                  % _frontier_note(now), file=out)
        print("", file=out)
        return 1

    print("  RESULT: PASS  -- both directions satisfied, absence on-rule at %s"
          % ON_RULE_GATE, file=out)
    print("    %s RENDERS for %s (state=%s) and is ABSENT for %s (state=%s)"
          % (MEMBER_ID, RENDERS_SCOPE, ev_r["member_state"],
             ABSENT_SCOPE, ev_a["member_state"]), file=out)
    print("    NOTE: this is the SERVED-BYTES + SHIPPED-PREDICATE plane. It does "
          "NOT discharge TS1-AC3, which requires a rendered read.", file=out)
    print("", file=out)
    return 0


# --------------------------------------------------------------------------
# SELF-TEST -- an instrument that cannot be shown to fail is an assertion
# --------------------------------------------------------------------------

def _mutate(doc, aum_value):
    """Set the subject member's aum. Returns a deep-ish copy."""
    d = json.loads(json.dumps(doc))
    members = d["nodes"][L0_NODE]["children"][L1_NODE]["members"]
    for m in members:
        if m.get("member_id") == MEMBER_ID:
            if aum_value is _SENTINEL_DELETE:
                m.pop("aum", None)
            else:
                m["aum"] = aum_value
    return d


class _Sentinel(object):
    pass


_SENTINEL_DELETE = _Sentinel()


def self_test(repo_root, now, out=sys.stdout):
    print("", file=out)
    print("=" * 74, file=out)
    print("TS1-AC2 SCORER SELF-TEST -- exercised in BOTH directions", file=out)
    print("=" * 74, file=out)

    ok, sha, _norm = fidelity_check(repo_root)
    print("", file=out)
    print("ARM 0 -- PREDICATE FIDELITY (the primary carrier is the TSX)", file=out)
    print("  primary : %s :: %s" % (PREDICATE_SOURCE, PREDICATE_FN), file=out)
    print("  pinned  : %s" % PREDICATE_PIN, file=out)
    print("  actual  : %s" % sha, file=out)
    if not ok:
        print("  REFUSED: the shipped predicate MOVED. This port is stale and "
              "every verdict below would be scored against yesterday's rule.",
              file=out)
        return 3
    print("  OK: this port matches the shipped predicate byte-for-byte "
          "(whitespace-normalized).", file=out)

    base = {}
    for scope in (RENDERS_SCOPE, ABSENT_SCOPE):
        base[scope] = src_git(scope, BASELINE_COMMIT, repo_root)
    print("", file=out)
    print("  control bytes: %s @ %s (%d of %d served scopes loaded; the other %d "
          "are not part of AC2's worked case)"
          % (BASELINE_DIR, BASELINE_COMMIT, len(base), len(SERVED_SCOPES),
             len(SERVED_SCOPES) - len(base)), file=out)

    failures = []

    # ARM 1 -- the real pre-fix control MUST FAIL, and on the absence half.
    print("", file=out)
    print("-" * 74, file=out)
    print("ARM 1 -- NEGATIVE CONTROL: the real pre-fix bytes @%s" % BASELINE_COMMIT,
          file=out)
    print("  EXPECT: FAIL, on the ABSENCE direction, with the positive direction "
          "PASSING (nothing is mapped, so the guard is inert and every member "
          "renders at BOTH scopes).", file=out)
    print("-" * 74, file=out)
    rc = score(lambda s: base[s], "git %s (committed pre-fix baseline, SERVED "
               "bytes as delivered through the edge -- NOT an s3api read)"
               % BASELINE_COMMIT, True, now, out)
    ev_r = evaluate(base[RENDERS_SCOPE])
    ev_a = evaluate(base[ABSENT_SCOPE])
    if rc != 1:
        failures.append("ARM 1 returned %d, expected 1 (FAIL)" % rc)
    if ev_r["verdict"] != RENDERS:
        failures.append(
            "ARM 1: positive direction should PASS on the control "
            "(got %s) -- if BOTH halves fail the control is not discriminating"
            % ev_r["verdict"]
        )
    if ev_a["verdict"] != RENDERS:
        failures.append(
            "ARM 1: absence direction should fail by RENDERING (got %s)"
            % ev_a["verdict"]
        )
    if rc == 1 and ev_r["verdict"] == RENDERS and ev_a["verdict"] == RENDERS:
        print("  OK: the control FAILS, and it fails on exactly one half. The "
              "positive half passing is what makes this a discriminating "
              "control rather than a build where everything is broken.", file=out)

    # ARM 2 -- a synthetically-fixed object MUST PASS.
    print("", file=out)
    print("-" * 74, file=out)
    print("ARM 2 -- POSITIVE ARM: control bytes with the subject MAPPED", file=out)
    print("  MUTATION: cottonwood %s aum -> 8425603.56 (held); inflection %s "
          "aum -> 0.0 (not held). Siblings left unmapped is not enough -- the "
          "guard needs a mapped sibling to arm, so the mutation maps one sibling "
          "at each scope too." % (MEMBER_ID, MEMBER_ID), file=out)
    print("-" * 74, file=out)
    fixed = {}
    for scope, subject_aum in ((RENDERS_SCOPE, 8425603.56), (ABSENT_SCOPE, 0.0)):
        d = _mutate(base[scope], subject_aum)
        # Arm the guard: give one OTHER sibling a real value, as the post-fix
        # producer will. Without a mapped sibling the guard stays inert and the
        # absence half cannot be satisfied at all.
        for m in d["nodes"][L0_NODE]["children"][L1_NODE]["members"]:
            if m.get("member_id") != MEMBER_ID:
                m["aum"] = 1_000_000.0
                break
        fixed[scope] = d
    rc2 = score(lambda s: fixed[s], "SYNTHETIC MUTANT of %s (self-test only)"
                % BASELINE_COMMIT, True, now, out)
    if rc2 != 0:
        failures.append("ARM 2 returned %d, expected 0 (PASS)" % rc2)
    else:
        print("  OK: the scorer PASSES a correctly-fixed object. Combined with "
              "ARM 1 this shows it discriminates rather than always failing.",
              file=out)

    # ARM 3 -- targeted mutants, each must FAIL for a NAMED reason.
    print("", file=out)
    print("-" * 74, file=out)
    print("ARM 3 -- WRONG-CAUSE MUTANTS: each must FAIL, and the tool must name "
          "the gate. An absence at the wrong gate scoring as a pass is the "
          "single defect this instrument exists to prevent.", file=out)
    print("-" * 74, file=out)

    def _mut_unavailable():
        d = json.loads(json.dumps(fixed[ABSENT_SCOPE]))
        d["nodes"][L0_NODE]["predicate"] = "unavailable"
        return d

    def _mut_drop_member():
        d = json.loads(json.dumps(fixed[ABSENT_SCOPE]))
        ms = d["nodes"][L0_NODE]["children"][L1_NODE]["members"]
        d["nodes"][L0_NODE]["children"][L1_NODE]["members"] = [
            m for m in ms if m.get("member_id") != MEMBER_ID
        ]
        return d

    def _mut_l1_suppressed():
        d = json.loads(json.dumps(fixed[ABSENT_SCOPE]))
        d["nodes"][L0_NODE]["children"][L1_NODE]["aum"] = 0
        return d

    def _mut_null_not_zero():
        # The subject is NULL rather than 0 at the absence scope. Under Andrew's
        # overrule this STILL suppresses -- so this mutant must PASS the absence
        # half. It is here to prove the tool does NOT secretly require a literal 0.
        d = json.loads(json.dumps(fixed[ABSENT_SCOPE]))
        for m in d["nodes"][L0_NODE]["children"][L1_NODE]["members"]:
            if m.get("member_id") == MEMBER_ID:
                m["aum"] = None
        return d

    def _mut_negative_is_money():
        # A NEGATIVE value is money and must RENDER (the test is != 0, not > 0).
        d = json.loads(json.dumps(fixed[RENDERS_SCOPE]))
        for m in d["nodes"][L0_NODE]["children"][L1_NODE]["members"]:
            if m.get("member_id") == MEMBER_ID:
                m["aum"] = -42.0
        return d

    mutants = [
        ("predicate=unavailable at L0", _mut_unavailable, ABSENT_SCOPE, "G1", ABSENT),
        ("subject dropped from registry", _mut_drop_member, ABSENT_SCOPE, "G2", ABSENT),
        ("L1 'Custom' row suppressed", _mut_l1_suppressed, ABSENT_SCOPE, "G2", ABSENT),
    ]
    for name, fn, scope, want_gate, want_verdict in mutants:
        ev = evaluate(fn())
        got = "%s@%s" % (ev["verdict"], ev["gate"])
        good = ev["verdict"] == want_verdict and ev["gate"] == want_gate
        print("  %-32s -> %-12s expected %s@%s   %s"
              % (name, got, want_verdict, want_gate,
                 "OK" if good else "MUTANT SURVIVED"), file=out)
        if not good:
            failures.append("mutant %r gave %s, expected %s@%s"
                            % (name, got, want_verdict, want_gate))
        if good and ev["on_rule"]:
            failures.append(
                "mutant %r was flagged on_rule=True -- a wrong-cause absence "
                "would score as the criterion met" % name
            )

    ev_null = evaluate(_mut_null_not_zero())
    good_null = ev_null["verdict"] == ABSENT and ev_null["on_rule"]
    print("  %-32s -> %-12s expected %s@%s   %s"
          % ("subject NULL not 0 (overrule)", "%s@%s" % (ev_null["verdict"], ev_null["gate"]),
             ABSENT, ON_RULE_GATE, "OK" if good_null else "WRONG"), file=out)
    if not good_null:
        failures.append(
            "NULL at the absence scope should suppress ON-RULE (Andrew's "
            "overrule: 'A null is a 0 in this case'); got %s@%s on_rule=%s"
            % (ev_null["verdict"], ev_null["gate"], ev_null["on_rule"])
        )

    ev_neg = evaluate(_mut_negative_is_money())
    good_neg = ev_neg["verdict"] == RENDERS
    print("  %-32s -> %-12s expected %s@%s   %s"
          % ("subject NEGATIVE (money, stays)", "%s@%s" % (ev_neg["verdict"], ev_neg["gate"]),
             RENDERS, ON_RULE_GATE, "OK" if good_neg else "WRONG"), file=out)
    if not good_neg:
        failures.append(
            "a NEGATIVE aum is money and must RENDER (the shipped test is "
            "`!== 0`, never `> 0`); got %s" % ev_neg["verdict"]
        )

    # ARM 4 -- the freshness guard must actually refuse.
    print("", file=out)
    print("-" * 74, file=out)
    print("ARM 4 -- FRESHNESS GUARD: the 13:30Z-vs-13:50Z trap", file=out)
    print("-" * 74, file=out)
    # A day after the control was written, the control bytes are stale.
    future = _parse_iso_z("2026-08-29T13:55:00Z")
    try:
        score(lambda s: base[s], "git %s" % BASELINE_COMMIT, False, future, out)
        failures.append(
            "ARM 4: the freshness guard did NOT refuse a stale object -- the "
            "scorer would read the pre-publish object and report a correct fix "
            "as FAILED"
        )
        print("  MUTANT SURVIVED: guard did not fire.", file=out)
    except Blocked as e:
        print("  OK: guard fired -> %s" % e, file=out)
    # And it must NOT refuse a fresh one (a guard that always refuses is useless).
    just_after = _parse_iso_z("2026-08-28T13:55:00Z")
    try:
        f = freshness(base[RENDERS_SCOPE], just_after)
        if f["stale"]:
            failures.append("ARM 4: guard refuses even a FRESH object")
            print("  WRONG: guard calls a fresh object stale.", file=out)
        else:
            print("  OK: guard passes the same bytes when read at 13:55Z on their "
                  "OWN publish day -- it discriminates by vintage, not by "
                  "always saying no.", file=out)
    except Blocked as e:
        failures.append("ARM 4 fresh-side raised: %s" % e)

    print("", file=out)
    print("=" * 74, file=out)
    if failures:
        print("SELF-TEST: FAILED (%d)" % len(failures), file=out)
        for f in failures:
            print("  ERROR: %s" % f, file=out)
        print("=" * 74, file=out)
        return 1
    print("SELF-TEST: OK -- the instrument fails on the pre-fix control, passes "
          "on a fixed object, names the gate on every wrong-cause mutant, "
          "honours null-is-zero and negative-is-money, and its freshness guard "
          "both fires and stands down.", file=out)
    print("=" * 74, file=out)
    return 0


# --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="D1_CATVIEWS.TS1-AC2 staged scorer (served L2 render)."
    )
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--self-test", action="store_true")
    g.add_argument("--from-git", nargs="?", const=BASELINE_COMMIT, metavar="COMMIT")
    g.add_argument("--from-file", metavar="DIR")
    g.add_argument("--from-s3", metavar="BUCKET")
    g.add_argument("--from-edge", metavar="BASE_URL")
    ap.add_argument("--bearer", default=os.environ.get("PORTAL_BEARER"))
    ap.add_argument("--control", action="store_true",
                    help="bypass the freshness guard; stamps the output")
    ap.add_argument("--repo-root", default=REPO_ROOT)
    a = ap.parse_args(argv)

    now = dt.datetime.now(dt.timezone.utc)

    try:
        if a.self_test:
            return self_test(a.repo_root, now)

        ok, sha, _ = fidelity_check(a.repo_root)
        if not ok:
            raise Refused(
                "the shipped predicate at %s::%s has MOVED (pinned %s, actual %s). "
                "This file is its second carrier and is now stale. Re-read the "
                "primary and re-pin before scoring anything."
                % (PREDICATE_SOURCE, PREDICATE_FN, PREDICATE_PIN, sha)
            )

        if a.from_git:
            label = ("git %s (committed bytes; SERVED as delivered through the "
                     "edge at capture -- NOT an s3api read)" % a.from_git)
            loader = lambda s: src_git(s, a.from_git, a.repo_root)  # noqa: E731
        elif a.from_file:
            label = "file %s" % a.from_file
            loader = lambda s: src_file(s, a.from_file)  # noqa: E731
        elif a.from_s3:
            label = ("s3api get-object s3://%s/platinum/mdpf/<scope>/"
                     "category-views.json (S3 PLANE, not the edge)" % a.from_s3)
            loader = lambda s: src_s3(s, a.from_s3, a.repo_root)  # noqa: E731
        elif a.from_edge:
            label = "edge GET %s/api/general/mdpf/<scope>/category-views.json" % (
                a.from_edge.rstrip("/"))
            loader = lambda s: src_edge(s, a.from_edge, a.bearer)  # noqa: E731
        else:
            ap.print_help()
            print("\nERROR: name a source. Start with --self-test.")
            return 2

        return score(loader, label, a.control, now)

    except Refused as e:
        print("\nREFUSED: %s\n" % e)
        return 3
    except Blocked as e:
        print("\nBLOCKED: %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
