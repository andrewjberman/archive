#!/usr/bin/env python3
"""check_en_r4 -- LGIC_ENFORCE round 4's checker. The ISSUER's fixed input; workers never edit it.

Round 4 is the REGISTRY CAMPAIGN (1.0.0_SA_CTO's round-3 analysis @969f89b0e7, R-32/R-33). Its five
cells call these subcommands as their criteria's invocations. Each prints its evidence, a
DENOMINATOR where one exists, and exactly one final line `VERDICT: PASS-<X>` / `FAIL-<X>`, and
exits 0 on PASS, 1 on FAIL, 2 on a usage error. A missing input is a FAIL verdict, never a
traceback.

NO PASS TOKEN IS A SUBSTRING OF ANOTHER: proof-of-spec-check greps <expect> UNANCHORED, so
PASS-C23-CAMPAIGN-COVERED and PASS-C23-CAMPAIGN-COVERED-BASIS would be one token to it. The tokens
below were checked pairwise at the cut (selftest-arms prints that check as its own arm).

THE BASE IS PINNED, NOT DERIVED. R4_BASE.json carries the cut's HEAD. Arms that must tell "a row
this round added" from "a row that was already there" read the registry at that commit with
`git show <base>:<path>`, never `git merge-base HEAD CLOUD` -- a worker's branch base moves under a
drain, and an issuer re-run after a merge would then grade a different set (LGIC_NAMING's
merge-base lesson, reference_an_issuer_checker_whose_base_is_merge_base_head_cloud).

WHAT EACH CELL'S ARMS READ
  EN-c-23  the campaign      RAISE_POPULATION_S6.r3.md's own table is the denominator (351 distinct
                             triples at the cut). Every triple must be MINTED (grade() no longer
                             raises) or CARDED (in the cell's NOT_JUDGED json, with a card anchor
                             that resolves in the cell's OWNER_CARDS document). The mint-basis arm
                             reads every row the round ADDS and requires owner_claim + a resolving
                             owner_basis citation. The fence arm requires exemptions.json unchanged
                             from the base: that file is the applied fence's registry source, so a
                             row there is exactly the mint R-29's guard forbids without sign-off.
  EN-h-24  the placeholders  the 8 {system} rows of round 3's report, re-graded by name and type.
  EN-s-25  the run           judged + carded == nameable on BOTH planes, no stop, the live plane's
                             `built:` vintage stated. This is FWD-5's closure bar as the CTO states
                             it -- NOT "zero carded".
  EN-d-26  DEC-4(ii)         the amended criterion text, and a validator that REFUSES a planted
                             NOT_A_PRINCIPAL claim on a bucket no live data-event selector covers
                             while still ACCEPTING one on a covered bucket (both arms, or the
                             refusal could be a validator that refuses everything).
  EN-g-27  S60               `targets` classifies every target with a per-plane `measured:`
                             instrument and 0 UNCLASSIFIED, and the cell files a disposition.

Standard library only. ASCII only. LF endings.
"""
import importlib.util
import json
import os
import re
import shutil as _shutil
import subprocess
import sys
import tempfile as _tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
# r4 -> fixed_inputs -> 2.0.0_SA_COO~G -> deliverables -> LGIC_ENFORCE -> LGIC -> D14 -> missions -> org -> repo
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
DELIV = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables"
POP = DELIV + "/0.9.0_WK_LGIC_ENFORCE~4/RAISE_POPULATION_S6.r3.md"
R3REPORT = DELIV + "/0.9.0_WK_LGIC_ENFORCE~4/NAMING_CENSUS_REPORT.r3.md"
SYSTEMS = "infra/logic/registry/systems.json"
RESOURCES = "infra/logic/registry/resources.json"
EXEMPTIONS = "infra/logic/registry/exemptions.json"
BASEFILE = os.path.join(HERE, "R4_BASE.json")

PLANES = ("live", "repo")


def say(*parts):
    print(" ".join(str(p) for p in parts))


def fail(tag, *lines):
    for ln in lines:
        say(ln)
    say("VERDICT: FAIL-" + tag)
    return 1


def ok(tag, *lines):
    for ln in lines:
        say(ln)
    say("VERDICT: PASS-" + tag)
    return 0


def git(args, cwd=None):
    r = subprocess.run(["git"] + args, capture_output=True, text=True, cwd=cwd or REPO)
    return r.returncode, r.stdout


def read(path, root=None):
    p = path if os.path.isabs(path) else os.path.join(root or REPO, path)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def base_commit():
    t = read(BASEFILE)
    if t is None:
        return None
    try:
        return (json.loads(t) or {}).get("base_commit")
    except ValueError:
        return None


def at_base(path, root=None, base=None):
    """The file's bytes at the pinned cut base, or None. `git show` with a slashed ref."""
    b = base or base_commit()
    if not b:
        return None
    rc, out = git(["show", "%s:%s" % (b, path)], cwd=root)
    return out if rc == 0 else None


def naming(root=None):
    """lib/opal_naming.py as a module, loaded from the tree under test."""
    lib = os.path.join(root or REPO, "lib")
    path = os.path.join(lib, "opal_naming.py")
    if not os.path.isfile(path):
        return None
    if lib not in sys.path:
        sys.path.insert(0, lib)
    spec = importlib.util.spec_from_file_location("opal_naming_r4", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def population(path=None, root=None):
    """The (plane, type, name) triples of RAISE_POPULATION_S6.r3.md's own table.

    The document is a MARKDOWN TABLE, not a json fence: its rows are the denominator this round is
    cut against, so they are parsed from the table the CTO's analysis cites rather than recomputed
    (a recomputed population would move under the round's own mints and could never close)."""
    t = read(path or POP, root)
    if t is None:
        return None
    rows = []
    for line in t.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        plane, typ, nm = cells[0], cells[1], cells[2].strip("`")
        if plane not in PLANES or not typ or typ == "type":
            continue
        rows.append((plane, typ, nm))
    seen, out = set(), []
    for r in rows:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def carded_index(root=None, serial="0.9.0_WK_LGIC_ENFORCE~1"):
    """{(plane, name): card} from the campaign cell's NOT_JUDGED_R4.json, plus the cards document."""
    folder = DELIV + "/" + serial
    nj = read(folder + "/NOT_JUDGED_R4.json", root)
    if nj is None:
        return {}, None
    try:
        rows = json.loads(nj)
    except ValueError:
        return {}, None
    if not isinstance(rows, list):
        return {}, None
    cards = read(folder + "/OWNER_CARDS_R4.md", root) or ""
    idx = {}
    for e in rows:
        if isinstance(e, dict) and e.get("name"):
            idx[(e.get("plane"), e.get("name"))] = e.get("card") or ""
    return idx, cards


def _anchor_resolves(card, cards_text):
    """A card reference resolves when its #anchor matches a heading in the cards document.

    A bare path with no anchor does NOT resolve: 'the card is in that file somewhere' is the claim
    this arm exists to refuse."""
    if not card or "#" not in card:
        return False
    anchor = card.split("#", 1)[1].strip().lower()
    if not anchor:
        return False
    for line in (cards_text or "").splitlines():
        if not line.startswith("#"):
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", line.lstrip("#").strip().lower()).strip("-")
        if slug and (slug == anchor.strip("-") or anchor.strip("-") in slug):
            return True
    return False


# ------------------------------------------------------------------ EN-c-23, the campaign
def c23_campaign_covered(path=None, root=None, serial="0.9.0_WK_LGIC_ENFORCE~1"):
    """Every triple of the pinned population is MINTED (no longer raises) or CARDED with a resolving card."""
    pop = population(path, root)
    if not pop:
        return fail("C23-POPULATION-UNREADABLE", "the population document is absent or carries no table rows: %s"
                    % (path or POP))
    mod = naming(root)
    if mod is None:
        return fail("C23-POPULATION-UNREADABLE", "lib/opal_naming.py absent under %s" % (root or REPO))
    idx, cards = carded_index(root, serial)
    minted, carded, open_rows, bad_card = [], [], [], []
    for plane, typ, nm in pop:
        raised = None
        try:
            mod.grade(nm, typ)
        except Exception as exc:                                  # RaiseDefect and any read defect
            raised = str(exc)
        if raised is None:
            minted.append((plane, typ, nm))
            continue
        card = idx.get((plane, nm))
        if card is None:
            open_rows.append((plane, typ, nm, raised))
        elif not _anchor_resolves(card, cards):
            bad_card.append((plane, typ, nm, card))
        else:
            carded.append((plane, typ, nm))
    say("DENOMINATOR: %d distinct (plane, type, name) triple(s) in %s" % (len(pop), path or POP))
    say("  MINTED (grade() no longer raises): %d" % len(minted))
    say("  CARDED (NOT-JUDGED with a resolving card anchor): %d" % len(carded))
    say("  STILL OPEN (neither minted nor carded): %d" % len(open_rows))
    say("  CARDED BUT THE CARD DOES NOT RESOLVE: %d" % len(bad_card))
    for plane, typ, nm, why in open_rows[:10]:
        say("    OPEN  %s %s %s -- %s" % (plane, typ, nm, why[:100]))
    for plane, typ, nm, card in bad_card[:10]:
        say("    CARD  %s %s %s -> %r does not resolve to a heading" % (plane, typ, nm, card))
    if open_rows or bad_card:
        return fail("C23-CAMPAIGN-COVERED", "every triple is minted or carded, or the cell is not done")
    return ok("C23-CAMPAIGN-COVERED", "%d minted + %d carded == %d, the population's own denominator"
              % (len(minted), len(carded), len(pop)))


def _rows_of(doc):
    """The row list of EITHER registry file. systems.json keeps its rows under `systems`, resources.json
    under `resources`; reading only one key made every systems.json row invisible to this arm, which is how
    a real mint there could read as `0 rows added` (row LGIC_ENFORCE-W1-S29, found by 0.9.0_WK_LGIC_ENFORCE~1)."""
    if isinstance(doc, dict):
        for k in ("systems", "resources"):
            if isinstance(doc.get(k), list):
                return [r for r in doc[k] if isinstance(r, dict)]
        return []
    return [r for r in doc if isinstance(r, dict)] if isinstance(doc, list) else []


def _rowkey(row):
    """systems.json identifies a row by `key`, resources.json by (name, type)."""
    return (row.get("key") or row.get("name"), row.get("type") or row.get("class"))


def _added_rows(path, root=None, base=None):
    """(added, total) registry rows: the rows at the worktree minus the rows at the pinned base, by name+type."""
    now = read(path, root)
    if now is None:
        return None, None
    old = at_base(path, root, base)
    try:
        cur = json.loads(now)
    except ValueError:
        return None, None
    rows = _rows_of(cur)
    oldkeys = set()
    if old:
        try:
            for r in _rows_of(json.loads(old)):
                oldkeys.add(_rowkey(r))
        except ValueError:
            pass
    added = [r for r in rows if _rowkey(r) not in oldkeys]
    return added, len(rows)


def _citation_resolves(basis, root=None):
    """A `path:line` or `path` citation resolves when the path exists and the line is inside it."""
    if not isinstance(basis, str) or not basis.strip():
        return False
    m = re.match(r"^([^\s:]+?)(?::(\d+))?(?:-(\d+))?(?:\s|$)", basis.strip())
    if not m:
        return False
    p = m.group(1)
    t = read(p, root)
    if t is None:
        return False
    if m.group(2):
        return int(m.group(2)) <= len(t.splitlines())
    return True


def c23_mint_basis(path=None, root=None, base=None):
    """Every row this round ADDS to systems.json or resources.json carries owner_claim and a RESOLVING owner_basis."""
    b = base or base_commit()
    if not b:
        return fail("C23-MINT-BASIS", "R4_BASE.json carries no base_commit: the added-row set cannot be measured")
    total_added, defects = 0, []
    for f in (SYSTEMS, RESOURCES):
        added, total = _added_rows(f, root, b)
        if added is None:
            return fail("C23-MINT-BASIS", "%s is absent or not json" % f)
        say("  %s: %d row(s) at the worktree, %d added since %s" % (f, total, len(added), b[:10]))
        for r in added:
            total_added += 1
            nm = _rowkey(r)[0]
            if f == RESOURCES:
                # resources.json's field set is CLOSED by lib/opal_naming.py RES_FIELDS
                # ("name", "type", "system", "evidence") and validate() refuses anything else, so an
                # owner_claim/owner_basis pair CANNOT be expressed on one of its rows. Its measured basis
                # is the `system` it names resolving to a systems.json key, plus its own evidence.
                extra = sorted(set(r) - {"name", "type", "system", "evidence"})
                if extra:
                    defects.append((f, nm, "fields outside the closed RES_FIELDS set: %s" % extra))
                elif not str(r.get("system") or "").strip():
                    defects.append((f, nm, "names no system"))
                elif r.get("system") not in _systems_keys(root):
                    defects.append((f, nm, "system=%r is not a key of systems.json" % r.get("system")))
                elif not str(r.get("evidence") or "").strip():
                    defects.append((f, nm, "carries no evidence"))
                continue
            claim = r.get("owner_claim")
            basis = r.get("owner_basis")
            if claim not in ("measured", "inferred"):
                defects.append((f, nm, "owner_claim=%r" % claim))
            elif not _citation_resolves(basis, root):
                defects.append((f, nm, "owner_basis=%r does not resolve" % basis))
    say("DENOMINATOR: %d added registry row(s); %d defective" % (total_added, len(defects)))
    for f, nm, why in defects[:10]:
        say("    DEFECT %s %s -- %s" % (f, nm, why))
    if defects:
        return fail("C23-MINT-BASIS", "a mint carries owner_claim and a citation that resolves, or it is a guess")
    if total_added == 0:
        # R-32 and R-29 both say MINT WHERE MEASURED, OTHERWISE CARD, and the CTO's closure bar is
        # judged + carded == nameable, NOT "zero carded". So a fully carded population is a legal outcome
        # and this arm must not demand a mint; whether the cards cover the population is c23-campaign-covered's
        # question, graded there. This arm grades the BASIS OF EVERY MINT, vacuously when there are none.
        return ok("C23-MINT-BASIS", "0 rows minted: no mint to grade -- the population's coverage is "
                                    "c23-campaign-covered's arm, and a fully carded campaign is legal under R-32")
    return ok("C23-MINT-BASIS", "%d of %d added rows carry their file's own measured basis"
              % (total_added, total_added))


def _systems_keys(root=None):
    try:
        return {r.get("key") for r in _rows_of(json.loads(read(SYSTEMS, root) or "null"))}
    except ValueError:
        return set()


def c23_fence_untouched(path=None, root=None, base=None):
    """R-29's guard, mechanically: exemptions.json is byte-unchanged from the pinned base.

    exemptions.json is the registry source of the APPLIED fence on opal-data-49financial
    (generated_locals.tf -> the shared-infra root), so a row added there IS the mint the guard
    forbids without never-widen sign-off. A cell that needs one cards it BLOCKING instead."""
    b = base or base_commit()
    if not b:
        return fail("C23-FENCE-UNTOUCHED", "R4_BASE.json carries no base_commit")
    now = read(EXEMPTIONS, root)
    old = at_base(EXEMPTIONS, root, b)
    if now is None or old is None:
        return fail("C23-FENCE-UNTOUCHED", "%s unreadable at the worktree or at %s" % (EXEMPTIONS, b[:10]))
    same = now.replace("\r\n", "\n") == old.replace("\r\n", "\n")
    say("DENOMINATOR: 1 applied-fence registry source (%s)" % EXEMPTIONS)
    say("  identical to %s (CRLF-normalised): %s" % (b[:10], same))
    if not same:
        return fail("C23-FENCE-UNTOUCHED", "the fence's registry source moved: that mint needs never-widen "
                                           "sign-off by 1.0.0_SA_CTO and 2.0.0_SA_COO, and is carded BLOCKING")
    return ok("C23-FENCE-UNTOUCHED", "no row was minted into the applied fence's source")


def c23_validate(path=None, root=None):
    """`lib/opal_naming.py validate` still reads OK after the campaign's mints."""
    r = subprocess.run([sys.executable, os.path.join(root or REPO, "lib", "opal_naming.py"), "validate"],
                       capture_output=True, text=True, cwd=root or REPO)
    out = (r.stdout or "") + (r.stderr or "")
    line = next((ln for ln in out.splitlines() if "VALIDATE" in ln), "(no VALIDATE line)")
    say("  %s" % line.strip()[:200])
    say("DENOMINATOR: 1 validate run; rc=%d" % r.returncode)
    if "VALIDATE: OK" not in out:
        return fail("C23-VALIDATE-OK", "the registry must still validate after a mint")
    return ok("C23-VALIDATE-OK", "the registry validates at this tree")


# ------------------------------------------------------------------ EN-h-24, the placeholders
def _placeholder_rows(path=None, root=None):
    t = read(path or R3REPORT, root)
    if t is None:
        return None
    ms = list(re.finditer(r"```json\n(.*?)\n```", t, re.S))
    if not ms:
        return None
    try:
        d = json.loads(ms[-1].group(1))
    except ValueError:
        return None
    rows = d.get("rows") or []
    return [(r.get("current"), r.get("type")) for r in rows if "{" in str(r.get("canonical", ""))]


def h24_placeholders(path=None, root=None, serial="0.9.0_WK_LGIC_ENFORCE~1"):
    """Each {system}-placeholder row of round 3's report now grades without a placeholder, or is carded."""
    rows = _placeholder_rows(path, root)
    if rows is None:
        return fail("H24-PLACEHOLDERS", "round 3's census report is unreadable: %s" % (path or R3REPORT))
    if not rows:
        return fail("H24-PLACEHOLDERS", "0 placeholder rows found in the report: an empty input cannot be graded "
                                        "(round 3 measured 8)")
    mod = naming(root)
    if mod is None:
        return fail("H24-PLACEHOLDERS", "lib/opal_naming.py absent")
    idx, cards = carded_index(root, serial)
    filled, carded, still = [], [], []
    for nm, typ in rows:
        try:
            _v, canon = mod.grade(nm, typ)
            leaked = "{" in str(canon)
        except Exception as exc:
            _v, canon, leaked = None, str(exc), True
        if not leaked:
            filled.append((nm, typ, canon))
        elif ("live", nm) in idx and _anchor_resolves(idx[("live", nm)], cards):
            carded.append((nm, typ))
        else:
            still.append((nm, typ, str(canon)[:80]))
    say("DENOMINATOR: %d placeholder row(s) in round 3's report" % len(rows))
    say("  FILLED (canonical carries no placeholder): %d" % len(filled))
    say("  CARDED with a resolving card:              %d" % len(carded))
    say("  STILL LEAKING a placeholder:               %d" % len(still))
    for nm, typ, canon in still[:10]:
        say("    LEAKS %s (%s) -> %s" % (nm, typ, canon))
    if still:
        return fail("H24-PLACEHOLDERS", "a placeholder reaches a report row unless every one is filled or carded")
    return ok("H24-PLACEHOLDERS", "%d filled + %d carded == %d" % (len(filled), len(carded), len(rows)))


# ------------------------------------------------------------------ EN-s-25, the run to the end
def _r4_report(path=None, root=None, serial="0.9.0_WK_LGIC_ENFORCE~2"):
    p = path or (DELIV + "/" + serial + "/NAMING_CENSUS_REPORT.r4.md")
    t = read(p, root)
    if t is None:
        return p, None
    ms = list(re.finditer(r"```json\n(.*?)\n```", t, re.S))
    if not ms:
        return p, None
    try:
        return p, json.loads(ms[-1].group(1))
    except ValueError:
        return p, None


def _plane_complete(d, judged, carded, total):
    j, c, n = d.get(judged), d.get(carded, 0), d.get(total)
    if not isinstance(n, int) or n <= 0 or not isinstance(j, int) or not isinstance(c, int) or c < 0:
        return False, j, c, n
    return j + c == n, j, c, n


def s25_live_complete(path=None, root=None):
    """judged_live + carded_live == live_nameable, no stop, and the live plane's built: vintage stated."""
    p, d = _r4_report(path, root)
    if d is None:
        return fail("S25-LIVE-COMPLETE", "the round-4 report is absent or has no parseable fence: %s" % p)
    den = d.get("denominators") or {}
    good, j, c, n = _plane_complete(den, "judged_live", "carded_live", "live_nameable")
    vint = str(d.get("vintage") or "")
    stopped = d.get("stopped") is not None
    say("report: %s" % p)
    say("DENOMINATOR: judged_live %s + carded_live %s of live_nameable %s; stopped=%s" % (j, c, n, stopped))
    say("  live-plane built: vintage stated: %s" % ("built:" in vint or "Built from the estate" in vint))
    if stopped:
        return fail("S25-LIVE-STOPPED", "the run stopped on a RAISE")
    if not good:
        return fail("S25-LIVE-COMPLETE", "judged + carded must equal nameable (R-32's bar, not zero carded)")
    if not ("built:" in vint or "Built from the estate" in vint):
        return fail("S25-LIVE-NO-VINTAGE", "the live plane's instrument vintage is not stated")
    return ok("S25-LIVE-COMPLETE", "%d judged + %d carded == %d nameable on the live plane" % (j, c, n))


def s25_repo_complete(path=None, root=None):
    """judged_repo + carded_repo == repo, no stop."""
    p, d = _r4_report(path, root)
    if d is None:
        return fail("S25-REPO-COMPLETE", "the round-4 report is absent or has no parseable fence: %s" % p)
    den = d.get("denominators") or {}
    good, j, c, n = _plane_complete(den, "judged_repo", "carded_repo", "repo")
    stopped = d.get("stopped") is not None
    say("DENOMINATOR: judged_repo %s + carded_repo %s of repo %s; stopped=%s" % (j, c, n, stopped))
    if stopped:
        return fail("S25-REPO-STOPPED", "the run stopped on a RAISE")
    if not good:
        return fail("S25-REPO-COMPLETE", "judged + carded must equal the repo plane's own denominator")
    return ok("S25-REPO-COMPLETE", "%d judged + %d carded == %d on the repo plane" % (j, c, n))


def s25_no_placeholder(path=None, root=None):
    """No row of the round-4 report carries a placeholder in its canonical (W2-S10's rule)."""
    p, d = _r4_report(path, root)
    if d is None:
        return fail("S25-NO-PLACEHOLDER", "the round-4 report is absent or has no parseable fence: %s" % p)
    rows = d.get("rows") or []
    leaked = [r for r in rows if "{" in str(r.get("canonical", ""))]
    say("DENOMINATOR: %d report row(s); %d carry a placeholder" % (len(rows), len(leaked)))
    for r in leaked[:10]:
        say("    PLACEHOLDER %s -> %s" % (r.get("current"), r.get("canonical")))
    if not rows:
        return fail("S25-NO-PLACEHOLDER", "an empty row set cannot be checked for placeholders")
    if leaked:
        return fail("S25-NO-PLACEHOLDER", "a placeholder reached a report row")
    return ok("S25-NO-PLACEHOLDER", "0 of %d rows carry a placeholder" % len(rows))


# ------------------------------------------------------------------ EN-d-26, DEC-4(ii)'s criterion text
TRAIL_FILES = ("infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf",
               "infra/aws/terraform/globgrph/item2e_served_write_trail.tf")
D26_TEXT = DELIV + "/0.9.0_WK_LGIC_ENFORCE~3/DEC4_II_AMENDED.r4.md"
D26_TOOL = DELIV + "/0.9.0_WK_LGIC_ENFORCE~3/fence_disposition_check.py"


def _covered_buckets(root=None):
    """Buckets named in a live CloudTrail data-event selector, read from the trail declarations."""
    found = set()
    for f in TRAIL_FILES:
        t = read(f, root) or ""
        for m in re.finditer(r"opal-data-[a-z0-9-]+", t):
            found.add(m.group(0))
    return found


def d26_text(path=None, root=None):
    """The amended DEC-4(ii) criterion text exists and carries all three of R-30's clauses."""
    t = read(path or D26_TEXT, root)
    if t is None:
        return fail("D26-TEXT-AMENDED", "the amended criterion text is absent: %s" % (path or D26_TEXT))
    low = t.lower()
    clauses = {
        "REFUSED on an uncovered bucket": "refus" in low and "data-event" in low,
        "a direct IAM-grant read is the alternative": "iam" in low and "grant" in low,
        "a NOT-JUDGED card is the other alternative": "not-judged" in low or "not_judged" in low,
        "silence in a trail that never covered the bucket is not evidence": "silence" in low,
    }
    say("DENOMINATOR: %d clause(s) R-30 requires" % len(clauses))
    for k, v in clauses.items():
        say("  %-62s %s" % (k, v))
    if not all(clauses.values()):
        return fail("D26-TEXT-AMENDED", "the amended text must carry every clause R-30 rules")
    return ok("D26-TEXT-AMENDED", "the amended criterion text carries all %d clauses" % len(clauses))


def _run_tool(tool, payload, root=None):
    d = _tempfile.mkdtemp(prefix="en_r4_d26_")
    try:
        p = os.path.join(d, "claim.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(payload, fh)
        r = subprocess.run([sys.executable, os.path.join(root or REPO, tool), p],
                           capture_output=True, text=True, cwd=root or REPO)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    finally:
        _shutil.rmtree(d, ignore_errors=True)


def d26_planted_refusal(path=None, root=None):
    """The cell's validator REFUSES a NOT_A_PRINCIPAL claim on an uncovered bucket and ACCEPTS one on a covered bucket.

    BOTH arms, in one criterion: a validator that refuses every input would pass the refusal half
    alone, which is the shape R-29's own self-test rule exists to refuse."""
    tool = path or D26_TOOL
    if read(tool, root) is None:
        return fail("D26-PLANTED-REFUSAL", "the disposition validator is absent: %s" % tool)
    covered = _covered_buckets(root)
    uncovered = "opal-data-demo"
    pick = sorted(covered)[0] if covered else None
    say("DENOMINATOR: %d bucket(s) named in a live data-event selector; probe uncovered=%s covered=%s"
        % (len(covered), uncovered, pick))
    if pick is None:
        return fail("D26-PLANTED-REFUSAL", "no covered bucket could be read from the trail declarations: the "
                                           "positive arm would be vacuous")
    if uncovered in covered:
        return fail("D26-PLANTED-REFUSAL", "%s is covered at this tree, so it is not the negative probe R-30 names"
                    % uncovered)
    rc_bad, out_bad = _run_tool(tool, {"rows": [
        {"role": "probe-role", "bucket": uncovered, "disposition": "NOT_A_PRINCIPAL",
         "evidence": "planted by the round-4 checker: CloudTrail data events show nothing for this role"}]}, root)
    rc_ok, out_ok = _run_tool(tool, {"rows": [
        {"role": "probe-role", "bucket": pick, "disposition": "NOT_A_PRINCIPAL",
         "evidence": "planted by the round-4 checker: a covered bucket, 0 events in a stated 90-day window, "
                     "query and count recorded"}]}, root)
    say("  planted claim on %s: rc=%d (must be non-zero)" % (uncovered, rc_bad))
    say("  planted claim on %s: rc=%d (must be zero)" % (pick, rc_ok))
    for ln in (out_bad.strip().splitlines() or [""])[-2:]:
        say("    uncovered says: %s" % ln[:160])
    for ln in (out_ok.strip().splitlines() or [""])[-2:]:
        say("    covered says:   %s" % ln[:160])
    if rc_bad == 0:
        return fail("D26-PLANTED-REFUSAL", "the validator accepted a NOT_A_PRINCIPAL claim on an uncovered bucket")
    if rc_ok != 0:
        return fail("D26-PLANTED-REFUSAL", "the validator refused a legitimate claim on a covered bucket: it "
                                           "refuses everything, which proves nothing")
    return ok("D26-PLANTED-REFUSAL", "refused on the uncovered bucket, accepted on a covered one")


# ------------------------------------------------------------------ EN-g-27, S60's disposition
G27_RECORD = DELIV + "/0.9.0_WK_LGIC_ENFORCE~4/S60_DISPOSITION.r4.md"


def _targets(root=None):
    r = subprocess.run([sys.executable, os.path.join(root or REPO, "lib", "opal_naming.py"), "targets"],
                       capture_output=True, text=True, cwd=root or REPO)
    out = (r.stdout or "") + (r.stderr or "")
    rows, planes = [], {}
    n = None
    for line in out.splitlines():
        m = re.match(r"^TARGETS:\s+(\d+)", line)
        if m:
            n = int(m.group(1))
        m = re.match(r"^(SHIP|REPO-ONLY|UNCLASSIFIED)\s+(\S+)\s+(\S+)\s+measured:\s*(.+)$", line)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3), m.group(4).strip()))
        m = re.match(r"^PLANE\s+(\S+):\s+(\d+)", line)
        if m:
            planes[m.group(1)] = int(m.group(2))
    return r.returncode, n, rows, planes, out


def g27_plane_instruments(path=None, root=None):
    """Every target carries a per-plane `measured:` instrument, 0 UNCLASSIFIED, and more than one plane's record is called."""
    rc, n, rows, planes, out = _targets(root)
    say("DENOMINATOR: TARGETS %s printed; %d classified row(s); rc=%d" % (n, len(rows), rc))
    if not rows or n is None:
        return fail("G27-PLANE-INSTRUMENTS", "the targets subcommand printed no classified rows")
    unclassified = [r for r in rows if r[0] == "UNCLASSIFIED"]
    no_instrument = [r for r in rows if not r[3] or r[3].lower().startswith("unknown")]
    instruments = sorted({r[3].split("(")[0].strip() for r in rows})
    say("  planes printed: %s" % (", ".join("%s=%d" % kv for kv in sorted(planes.items())) or "(none)"))
    say("  distinct measuring instruments: %d -- %s" % (len(instruments), "; ".join(i[:40] for i in instruments)))
    say("  UNCLASSIFIED: %d; rows with no instrument: %d" % (len(unclassified), len(no_instrument)))
    if len(rows) != n:
        return fail("G27-PLANE-INSTRUMENTS", "TARGETS %d but %d rows printed" % (n, len(rows)))
    if unclassified or no_instrument:
        return fail("G27-PLANE-INSTRUMENTS", "every target names the instrument that classified it")
    if len(instruments) < 2:
        return fail("G27-PLANE-INSTRUMENTS", "one classifier over every plane IS S60's undercount")
    return ok("G27-PLANE-INSTRUMENTS", "%d of %d targets classified by %d plane instruments, 0 UNCLASSIFIED"
              % (len(rows), n, len(instruments)))


def g27_disposition(path=None, root=None):
    """S60 carries a disposition: FIXED with its measurement, or CARDED with an owner and a reason."""
    t = read(path or G27_RECORD, root)
    if t is None:
        return fail("G27-DISPOSITION", "S60's disposition record is absent: %s" % (path or G27_RECORD))
    low = t.lower()
    fixed = "fixed" in low and "safe_deploy_core" in low
    carded = ("card" in low) and ("owner" in low) and ("reason" in low)
    say("DENOMINATOR: 1 record; FIXED shape=%s CARDED shape=%s" % (fixed, carded))
    if not (fixed or carded):
        return fail("G27-DISPOSITION", "the record must state FIXED with its measurement or CARDED with owner and reason")
    return ok("G27-DISPOSITION", "S60 is dispositioned (%s)" % ("FIXED" if fixed else "CARDED"))


# ------------------------------------------------------------------ the self-test
def _fixture_repo(tmp):
    """A throwaway git repo carrying the paths these arms read."""
    os.makedirs(os.path.join(tmp, "lib"), exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=tmp, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp, capture_output=True)
    return tmp


def _write(tmp, rel, text):
    p = os.path.join(tmp, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return p


STUB_NAMING = '''import sys
BAD = set(%r)
def grade(name, type):
    if name in BAD:
        raise RuntimeError("R1.c: %%r is an unresolved token" %% (name,))
    if name == "leaky":
        return "OUT-OF-PATTERN", "{system}-leaky"
    return "CONFORMANT", "opal-" + name
def _main():
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        print("VALIDATE: OK 1 system row(s)")
        return 0
    if len(sys.argv) > 1 and sys.argv[1] == "targets":
        print("TARGETS: 2")
        print("SHIP lambda a.py measured: lambda-source-map.json (1 consumer)")
        print("SHIP s3 b.py measured: safe_deploy_core (file_to_s3_target)")
        print("PLANE lambda: 1")
        print("PLANE s3: 1")
        return 0
    return 2
if __name__ == "__main__":
    sys.exit(_main())
'''

POP_FIXTURE = """# fixture population

| plane | type | name | message |
|---|---|---|---|
| live | API_GW | `alpha-api` | R1.c: 'alpha' is an unresolved token |
| repo | S3_BUCKET | `opal-data-beta` | B2: 'beta' is no scope key |
"""


def _selftest_c23():
    out = []
    base = _tempfile.mkdtemp(prefix="en_r4_c23_")
    try:
        tmp = _fixture_repo(base)
        _write(tmp, "lib/opal_naming.py", STUB_NAMING % [["alpha-api", "opal-data-beta"]][0])
        _write(tmp, POP, POP_FIXTURE)
        serial = "0.9.0_WK_LGIC_ENFORCE~1"
        # RED: neither minted nor carded
        out.append(("c23-campaign RED   (both triples open)", c23_campaign_covered(root=tmp) == 1))
        # RED: carded, but the card anchor does not resolve
        _write(tmp, DELIV + "/" + serial + "/NOT_JUDGED_R4.json",
               json.dumps([{"name": "alpha-api", "plane": "live", "card": "cards.md#no-such-heading"},
                           {"name": "opal-data-beta", "plane": "repo", "card": "cards.md#card-2-beta"}]))
        _write(tmp, DELIV + "/" + serial + "/OWNER_CARDS_R4.md", "# Cards\n\n## Card 2 beta\n\nbody\n")
        out.append(("c23-campaign RED   (one card anchor unresolved)", c23_campaign_covered(root=tmp) == 1))
        # GREEN: both carded with resolving anchors
        _write(tmp, DELIV + "/" + serial + "/OWNER_CARDS_R4.md",
               "# Cards\n\n## Card 1 alpha api\n\nbody\n\n## Card 2 beta\n\nbody\n")
        _write(tmp, DELIV + "/" + serial + "/NOT_JUDGED_R4.json",
               json.dumps([{"name": "alpha-api", "plane": "live", "card": "cards.md#card-1-alpha-api"},
                           {"name": "opal-data-beta", "plane": "repo", "card": "cards.md#card-2-beta"}]))
        out.append(("c23-campaign GREEN (both carded, anchors resolve)", c23_campaign_covered(root=tmp) == 0))
        # GREEN by MINT: the stub no longer raises
        _write(tmp, "lib/opal_naming.py", STUB_NAMING % [[]][0])
        _write(tmp, DELIV + "/" + serial + "/NOT_JUDGED_R4.json", json.dumps([]))
        out.append(("c23-campaign GREEN (both minted)", c23_campaign_covered(root=tmp) == 0))
        # population parse: a document with no table is a FAIL verdict, never a traceback
        _write(tmp, POP, "# no table here\n")
        out.append(("c23-campaign RED   (population unreadable)", c23_campaign_covered(root=tmp) == 1))
        # validate arm, both ways
        out.append(("c23-validate GREEN (stub prints OK)", c23_validate(root=tmp) == 0))
        _write(tmp, "lib/opal_naming.py", "import sys\nprint('VALIDATE: 3 error(s)')\nsys.exit(1)\n")
        out.append(("c23-validate RED   (validate not OK)", c23_validate(root=tmp) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


def _selftest_basis():
    out = []
    base = _tempfile.mkdtemp(prefix="en_r4_basis_")
    try:
        tmp = _fixture_repo(base)
        # The two registry files have DIFFERENT shapes and different field rules, and the fixtures say so:
        # systems.json keeps rows under `systems` keyed by `key` and DOES carry owner_claim/owner_basis;
        # resources.json keeps rows under `resources` keyed by (name, type) and its field set is CLOSED by
        # lib/opal_naming.py RES_FIELDS, so an owner pair there is a DEFECT, not a basis (row W1-S29).
        sys0 = {"_about": "x", "systems": [{"key": "kept", "class": "PRODUCT"}]}
        res0 = {"_about": "x", "resources": [{"name": "kept", "type": "T", "system": "kept", "evidence": "e"}]}
        _write(tmp, SYSTEMS, json.dumps(sys0))
        _write(tmp, RESOURCES, json.dumps(res0))
        _write(tmp, EXEMPTIONS, json.dumps({"opal-data-49financial": []}))
        subprocess.run(["git", "add", "-A"], cwd=tmp, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=tmp, capture_output=True)
        rc, head = git(["rev-parse", "HEAD"], cwd=tmp)
        b = head.strip()
        _write(tmp, "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r4/R4_BASE.json",
               json.dumps({"base_commit": b}))
        _write(tmp, "infra/aws/terraform/x/main.tf", "a\nb\nc\nd\n")

        # GREEN: nothing minted. R-32 permits a fully carded campaign, so this arm is VACUOUS here, not FAIL.
        out.append(("c23-mint-basis GREEN (0 rows minted, R-32 permits it)", c23_mint_basis(root=tmp, base=b) == 0))

        # THE ARM CAN SEE A systems.json MINT AT ALL -- the defect row W1-S29 named. GREEN with a resolving
        # basis, RED without the claim, RED when the citation does not resolve, RED past end of file.
        def sysrows(extra):
            d = json.loads(json.dumps(sys0))
            d["systems"].append(dict({"key": "new1", "class": "PRODUCT"}, **extra))
            return json.dumps(d)
        _write(tmp, SYSTEMS, sysrows({"owner_claim": "inferred", "owner_basis": "infra/aws/terraform/x/main.tf:3"}))
        out.append(("c23-mint-basis GREEN (systems mint, resolving basis)", c23_mint_basis(root=tmp, base=b) == 0))
        _write(tmp, SYSTEMS, sysrows({}))
        out.append(("c23-mint-basis RED  (systems mint, no owner_claim)", c23_mint_basis(root=tmp, base=b) == 1))
        _write(tmp, SYSTEMS, sysrows({"owner_claim": "inferred", "owner_basis": "no/such/file.tf:4"}))
        out.append(("c23-mint-basis RED  (basis does not resolve)", c23_mint_basis(root=tmp, base=b) == 1))
        _write(tmp, SYSTEMS, sysrows({"owner_claim": "inferred", "owner_basis": "infra/aws/terraform/x/main.tf:99"}))
        out.append(("c23-mint-basis RED  (basis line past end of file)", c23_mint_basis(root=tmp, base=b) == 1))
        _write(tmp, SYSTEMS, json.dumps(sys0))

        # resources.json: its basis is the `system` it names, and an owner pair there is REFUSED by validate().
        def resrows(extra):
            d = json.loads(json.dumps(res0))
            d["resources"].append(dict({"name": "new2", "type": "T", "system": "kept", "evidence": "e"}, **extra))
            return json.dumps(d)
        _write(tmp, RESOURCES, resrows({}))
        out.append(("c23-mint-basis GREEN (resources mint, system resolves)", c23_mint_basis(root=tmp, base=b) == 0))
        _write(tmp, RESOURCES, resrows({"owner_claim": "inferred"}))
        out.append(("c23-mint-basis RED  (resources mint outside RES_FIELDS)", c23_mint_basis(root=tmp, base=b) == 1))
        _write(tmp, RESOURCES, json.dumps({"_about": "x", "resources": res0["resources"] + [
            {"name": "new3", "type": "T", "system": "no-such-system", "evidence": "e"}]}))
        out.append(("c23-mint-basis RED  (resources mint names no real system)", c23_mint_basis(root=tmp, base=b) == 1))
        _write(tmp, RESOURCES, json.dumps(res0))

        # fence arm: GREEN unchanged, RED when the applied fence's source moves
        out.append(("c23-fence GREEN (exemptions unchanged)", c23_fence_untouched(root=tmp, base=b) == 0))
        _write(tmp, EXEMPTIONS, json.dumps({"opal-data-49financial": ["a-role"]}))
        out.append(("c23-fence RED   (a row minted into the fence)", c23_fence_untouched(root=tmp, base=b) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


def _report_doc(live_n, live_j, live_c, repo_n, repo_j, repo_c, stopped=None, vintage="built: 2026-09-17", rows=None):
    return {"vintage": vintage, "stopped": stopped,
            "denominators": {"live_nameable": live_n, "judged_live": live_j, "carded_live": live_c,
                             "repo": repo_n, "judged_repo": repo_j, "carded_repo": repo_c},
            "rows": rows if rows is not None else [{"current": "a", "canonical": "opal-a"}]}


def _selftest_s25():
    out = []
    base = _tempfile.mkdtemp(prefix="en_r4_s25_")
    try:
        tmp = _fixture_repo(base)
        rel = DELIV + "/0.9.0_WK_LGIC_ENFORCE~2/NAMING_CENSUS_REPORT.r4.md"

        def put(doc):
            _write(tmp, rel, "# r\n\n```json\n" + json.dumps(doc) + "\n```\n")
        put(_report_doc(10, 8, 2, 5, 5, 0))
        out.append(("s25-live GREEN (8+2==10)", s25_live_complete(root=tmp) == 0))
        out.append(("s25-repo GREEN (5+0==5)", s25_repo_complete(root=tmp) == 0))
        put(_report_doc(10, 7, 2, 5, 5, 0))
        out.append(("s25-live RED   (7+2!=10)", s25_live_complete(root=tmp) == 1))
        put(_report_doc(10, 8, 2, 5, 4, 0))
        out.append(("s25-repo RED   (4+0!=5)", s25_repo_complete(root=tmp) == 1))
        put(_report_doc(10, 8, 2, 5, 5, 0, stopped={"plane": "live", "type": "API_GW", "current": "x"}))
        out.append(("s25-live RED   (stopped on a RAISE)", s25_live_complete(root=tmp) == 1))
        put(_report_doc(10, 8, 2, 5, 5, 0, vintage="no vintage here"))
        out.append(("s25-live RED   (no built: vintage)", s25_live_complete(root=tmp) == 1))
        put(_report_doc(10, 8, 2, 5, 5, 0, rows=[{"current": "a", "canonical": "opal-a"}]))
        out.append(("s25-placeholder GREEN (clean rows)", s25_no_placeholder(root=tmp) == 0))
        put(_report_doc(10, 8, 2, 5, 5, 0, rows=[{"current": "a", "canonical": "{system}-a"}]))
        out.append(("s25-placeholder RED   (a leak)", s25_no_placeholder(root=tmp) == 1))
        put(_report_doc(10, 8, 2, 5, 5, 0, rows=[]))
        out.append(("s25-placeholder RED   (empty row set is not a pass)", s25_no_placeholder(root=tmp) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


def _selftest_h24():
    out = []
    base = _tempfile.mkdtemp(prefix="en_r4_h24_")
    try:
        tmp = _fixture_repo(base)
        _write(tmp, "lib/opal_naming.py", STUB_NAMING % [[]][0])
        doc = {"rows": [{"current": "leaky", "type": "CW_ALARM", "canonical": "{system}-leaky"},
                        {"current": "fine", "type": "CW_ALARM", "canonical": "opal-fine"}]}
        _write(tmp, R3REPORT, "# r3\n\n```json\n" + json.dumps(doc) + "\n```\n")
        out.append(("h24 RED   (the leaky row still leaks)", h24_placeholders(root=tmp) == 1))
        serial = "0.9.0_WK_LGIC_ENFORCE~1"
        _write(tmp, DELIV + "/" + serial + "/NOT_JUDGED_R4.json",
               json.dumps([{"name": "leaky", "plane": "live", "card": "c.md#card-1-leaky"}]))
        _write(tmp, DELIV + "/" + serial + "/OWNER_CARDS_R4.md", "# c\n\n## Card 1 leaky\n\nbody\n")
        out.append(("h24 GREEN (carded with a resolving anchor)", h24_placeholders(root=tmp) == 0))
        _write(tmp, R3REPORT, "# r3\n\n```json\n" + json.dumps({"rows": []}) + "\n```\n")
        out.append(("h24 RED   (0 placeholder rows is not a pass)", h24_placeholders(root=tmp) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


D26_STUB_GOOD = '''import json,sys,re,os
HERE=os.path.dirname(os.path.abspath(__file__))
def covered():
    s=set()
    for f in (%r, %r):
        p=os.path.join(os.getcwd(),f)
        if os.path.isfile(p):
            s|=set(re.findall(r"opal-data-[a-z0-9-]+", open(p,encoding="utf-8").read()))
    return s
d=json.load(open(sys.argv[1],encoding="utf-8"))
cov=covered(); bad=[]
for r in d.get("rows") or []:
    if r.get("disposition")=="NOT_A_PRINCIPAL" and r.get("bucket") not in cov:
        bad.append(r.get("bucket"))
print("covered buckets:",len(cov),"refused:",bad)
sys.exit(1 if bad else 0)
''' % TRAIL_FILES

D26_STUB_ALWAYS = "import sys\nprint('refuse everything')\nsys.exit(1)\n"


def _selftest_d26():
    out = []
    base = _tempfile.mkdtemp(prefix="en_r4_d26_")
    try:
        tmp = _fixture_repo(base)
        _write(tmp, TRAIL_FILES[0], 'data_resource { values = ["arn:aws:s3:::opal-data-bd/"] }\n')
        _write(tmp, TRAIL_FILES[1], 'values = ["arn:aws:s3:::opal-data-49financial/"]\n')
        out.append(("d26-refusal RED   (no validator)", d26_planted_refusal(root=tmp) == 1))
        _write(tmp, D26_TOOL, D26_STUB_ALWAYS)
        out.append(("d26-refusal RED   (a validator that refuses everything)", d26_planted_refusal(root=tmp) == 1))
        _write(tmp, D26_TOOL, D26_STUB_GOOD)
        out.append(("d26-refusal GREEN (refuses uncovered, accepts covered)", d26_planted_refusal(root=tmp) == 0))
        _write(tmp, D26_TEXT, "A NOT_A_PRINCIPAL claim on a bucket with no live CloudTrail data-event selector is "
                              "REFUSED. The disposition comes from a direct IAM-grant read, or the name is carded "
                              "NOT-JUDGED with its missing-instrument reason. Silence in a trail that never covered "
                              "the bucket is never evidence.\n")
        out.append(("d26-text GREEN (all clauses)", d26_text(root=tmp) == 0))
        _write(tmp, D26_TEXT, "A claim is refused sometimes.\n")
        out.append(("d26-text RED   (clauses missing)", d26_text(root=tmp) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


def _selftest_g27():
    out = []
    base = _tempfile.mkdtemp(prefix="en_r4_g27_")
    try:
        tmp = _fixture_repo(base)
        _write(tmp, "lib/opal_naming.py", STUB_NAMING % [[]][0])
        out.append(("g27-planes GREEN (2 instruments, 0 unclassified)", g27_plane_instruments(root=tmp) == 0))
        one = ("import sys\nprint('TARGETS: 2')\n"
               "print('SHIP s3 a.py measured: safe_deploy_core (x)')\n"
               "print('REPO-ONLY s3 b.py measured: safe_deploy_core (x)')\n")
        _write(tmp, "lib/opal_naming.py", one)
        out.append(("g27-planes RED   (one classifier over every plane -- S60)", g27_plane_instruments(root=tmp) == 1))
        unc = ("import sys\nprint('TARGETS: 2')\n"
               "print('SHIP lambda a.py measured: lambda-source-map.json (1)')\n"
               "print('UNCLASSIFIED terraform b.tf measured: none')\n")
        _write(tmp, "lib/opal_naming.py", unc)
        out.append(("g27-planes RED   (an UNCLASSIFIED row)", g27_plane_instruments(root=tmp) == 1))
        miscount = ("import sys\nprint('TARGETS: 3')\n"
                    "print('SHIP lambda a.py measured: lambda-source-map.json (1)')\n"
                    "print('SHIP s3 b.py measured: safe_deploy_core (x)')\n")
        _write(tmp, "lib/opal_naming.py", miscount)
        out.append(("g27-planes RED   (TARGETS 3 but 2 rows)", g27_plane_instruments(root=tmp) == 1))
        out.append(("g27-disposition RED  (no record)", g27_disposition(root=tmp) == 1))
        _write(tmp, G27_RECORD, "S60 is FIXED: safe_deploy_core decides the S3/DS plane only; the Lambda and "
                                "Terraform planes are measured by their own records.\n")
        out.append(("g27-disposition GREEN (FIXED with its measurement)", g27_disposition(root=tmp) == 0))
        _write(tmp, G27_RECORD, "S60 is CARDED: owner 1.0.0_SA_CTO, reason the classifier is R-16's mechanism.\n")
        out.append(("g27-disposition GREEN (CARDED with owner and reason)", g27_disposition(root=tmp) == 0))
        _write(tmp, G27_RECORD, "S60 was looked at.\n")
        out.append(("g27-disposition RED  (neither shape)", g27_disposition(root=tmp) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


def _selftest_tokens():
    """No PASS token is a substring of another: proof-of-spec greps <expect> UNANCHORED."""
    toks = ["PASS-C23-CAMPAIGN-COVERED", "PASS-C23-MINT-BASIS", "PASS-C23-FENCE-UNTOUCHED", "PASS-C23-VALIDATE-OK",
            "PASS-H24-PLACEHOLDERS", "PASS-S25-LIVE-COMPLETE", "PASS-S25-REPO-COMPLETE", "PASS-S25-NO-PLACEHOLDER",
            "PASS-D26-TEXT-AMENDED", "PASS-D26-PLANTED-REFUSAL", "PASS-G27-PLANE-INSTRUMENTS", "PASS-G27-DISPOSITION"]
    bad = [(a, b) for a in toks for b in toks if a != b and a in b]
    return [("tokens: no PASS token contains another (%d tokens)" % len(toks), not bad)]


def selftest_arms():
    """A-23: every arm driven ALONE against a doctored input that must FAIL and a fixture that must PASS."""
    results = []
    results.extend(_selftest_tokens())
    results.extend(_selftest_c23())
    results.extend(_selftest_basis())
    results.extend(_selftest_h24())
    results.extend(_selftest_s25())
    results.extend(_selftest_d26())
    results.extend(_selftest_g27())
    passed = sum(1 for _n, good in results if good)
    say("DISCRIMINATING SELF-TEST -- denominator %d arms (A-23), each exercised ALONE" % len(results))
    for n, good in results:
        say("  %-58s %s" % (n, "OK" if good else "BROKEN"))
    say("SELFTEST-ARMS: %d of %d" % (passed, len(results)))
    say("VERDICT: " + ("PASS-R4-ARMS-DISCRIMINATE" if passed == len(results) else "FAIL-R4-ARMS-DISCRIMINATE"))
    return 0 if passed == len(results) else 1


CMDS = {
    "c23-campaign-covered": c23_campaign_covered,
    "c23-mint-basis": c23_mint_basis,
    "c23-fence-untouched": c23_fence_untouched,
    "c23-validate": c23_validate,
    "h24-placeholders": h24_placeholders,
    "s25-live-complete": s25_live_complete,
    "s25-repo-complete": s25_repo_complete,
    "s25-no-placeholder": s25_no_placeholder,
    "d26-text": d26_text,
    "d26-planted-refusal": d26_planted_refusal,
    "g27-plane-instruments": g27_plane_instruments,
    "g27-disposition": g27_disposition,
    "selftest-arms": selftest_arms,
}


def main():
    if len(sys.argv) not in (2, 3):
        say("usage: check_en_r4.py <subcommand> [path] | --list | selftest-arms")
        return 2
    cmd = sys.argv[1]
    if cmd == "--list":
        for k in sorted(CMDS):
            say(k)
        return 0
    fn = CMDS.get(cmd)
    if fn is None:
        say("unknown subcommand:", cmd)
        return 2
    if len(sys.argv) == 3:
        return fn(sys.argv[2])
    return fn()


if __name__ == "__main__":
    sys.exit(main())
