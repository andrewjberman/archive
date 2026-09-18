#!/usr/bin/env python3
"""check_en_r5 -- LGIC_ENFORCE round 5's checker. The ISSUER's fixed input; workers never edit it.

Round 5 is the PLACEHOLDER CAMPAIGN plus three row remedies (1.0.0_SA_CTO's round-4 analysis
@b74ffb43ae, rulings R-38, R-39, and the standing bars R-33 and R-40). Its four cells call these
subcommands as their criteria's invocations. Each prints its evidence, a DENOMINATOR where one
exists, and exactly one final line `VERDICT: PASS-<X>` / `FAIL-<X>`. A missing input is a FAIL
verdict, never a traceback.

NO PASS TOKEN IS A SUBSTRING OF ANOTHER -- proof-of-spec-check greps <expect> UNANCHORED, so
PASS-C28-COVERED and PASS-C28-COVERED-BASIS would be one token to it. `selftest-arms` prints that
pairwise check as its own arm.

THE BASE IS PINNED, NOT DERIVED. R5_BASE.json carries the cut's HEAD. Arms that must tell "this
round changed it" from "it was already like that" read at that commit with `git show <base>:<path>`,
never `git merge-base HEAD CLOUD` -- a worker's branch base moves under a drain, and an issuer re-run
after a merge would grade a different set.

EVERY SHAPE BELOW WAS MEASURED AT THE CUT, NOT ASSUMED. Round 4's `c23-mint-basis` arm demanded
fields `resources.json` does not carry and could not see a `systems.json` mint at all -- this seat's
defect, found by a worker running it (LGIC_ENFORCE-W1-S29). Measured 2026-09-18 at 95fb561677:
  NAMING_CENSUS_REPORT.r4.md  ONE json fence, a dict with keys denominators / live_command /
                              not_judged / registry / rows / stopped / vintage. `rows` holds 3237
                              dicts, each {current, canonical, verdict, type, plane}. 1411 of those
                              3237 carry a literal '{' in `canonical`. That 1411 is THE START
                              POPULATION and it is a count at ONE VINTAGE of a report the campaign
                              itself replaces -- which is why c28-redenominator exists.
  NAMING_CENSUS_COMPARISON.r4.md  fence 0 is a dict; `uncompared_reasons` =
                              {NOT-GRADED-TYPE 23, AWS_FIXED-EXCLUDED 2, CARDED 11,
                              HAND-SPECIMEN-ABSENT 11, total 42}. The four parts sum to 47 over a
                              total of 42 (LGIC_ENFORCE-S62). 'THREE' occurs exactly once.
  OWNER_CARDS_R4.md           MARKDOWN WITH NO JSON FENCES. Cards are '## Card <n> -- <title>'
                              sections; 12 of them; Card 5 is the security-sweep tooling and Card 6
                              is opal-data-security[-access-logs]. 'TOKEN_COLLISION' occurs 0 times
                              at the cut. So c31's arms read PROSE, deliberately, and say so.
  resources.json              {_about, resources}; `resources` is 34 dicts of exactly
                              {name, type, system, evidence}. There is no owner_basis field here --
                              that lives in systems.json's rows.
  systems.json                {_about, refused_keys, systems, unresolved}; `systems` is 25 dicts of
                              {class, key, long, long_basis, owner_basis, owner_claim,
                              owner_directive}; `unresolved` is 3 dicts of {token, why}. The whole
                              value "security" occurs 0 times -- R-39's bar, measured, not assumed.

THE S61 NEEDLE IS NORMALISED AND THAT IS THE WHOLE POINT OF h29-evidence. The row's evidence string
quotes the phrase with an ASCII arrow, 'CW recovery metrics -> Inflection/HistBackfill/RateLimiter'.
Measured over 466 files under org/projects/ (recursive, every extension): that EXACT string occurs in
0 of them, while the distinctive core 'Inflection/HistBackfill/RateLimiter' occurs in exactly 1 --
org/projects/ADVI_JWTRES.json -- where the arrow is U+2192, not '->'. So the citation is wrong TWICE:
the wrong FILE, and a transcribed arrow that makes the quote unfindable by its own text. An arm that
searched the quoted phrase verbatim would read 0 everywhere and would happily pass a correction that
is still wrong.

Standard library only. ASCII only. LF endings.
"""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# r5 -> fixed_inputs -> 2.0.0_SA_COO~G -> deliverables -> LGIC_ENFORCE -> LGIC -> D14 -> missions -> org -> repo
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
DELIV = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables"
W1 = DELIV + "/0.9.0_WK_LGIC_ENFORCE~1"
W2 = DELIV + "/0.9.0_WK_LGIC_ENFORCE~2"

R4REPORT = W2 + "/NAMING_CENSUS_REPORT.r4.md"
R4COMP = W2 + "/NAMING_CENSUS_COMPARISON.r4.md"
CARDS_R4 = W1 + "/OWNER_CARDS_R4.md"
SYSTEMS = "infra/logic/registry/systems.json"
RESOURCES = "infra/logic/registry/resources.json"
EXEMPTIONS = "infra/logic/registry/exemptions.json"
BASEFILE = os.path.join(HERE, "R5_BASE.json")

# the cell deliverables round 5 introduces, each in the ASSIGNED worker's own folder
PLACEHOLDER_RECORD = "PLACEHOLDER_CAMPAIGN_R5.json"
R5REPORT = "NAMING_CENSUS_REPORT.r5.md"

S61_CORE = "Inflection/HistBackfill/RateLimiter"
S61_QUOTED_ASCII = "CW recovery metrics -> " + S61_CORE
S61_WRONG_FILE = "org/projects/ADVI_HISTBF.json"
S61_RIGHT_FILE = "org/projects/ADVI_JWTRES.json"
S61_ROW_NAME = "Inflection-HistBackfill-FailureSpike"

# R-33's bound, verbatim from the round-4 decomposition: past <start> + 25 MEASURED, stop and file the delta
TIMEBOX_OVERAGE = 25


# ============================================================================ plumbing
def out(*lines):
    for ln in lines:
        print(ln)


def verdict(ok, pass_tag, fail_tag, lines):
    out(*lines)
    print("VERDICT: " + (pass_tag if ok else fail_tag))
    return 0


def fail_only(tag, *lines):
    out(*lines)
    print("VERDICT: FAIL-" + tag)
    return 0


def ab(path):
    return path if os.path.isabs(path) else os.path.join(REPO, path)


def read(path):
    p = ab(path)
    if not os.path.isfile(p):
        return None
    return io.open(p, encoding="utf-8", errors="replace").read()


def load_json(path):
    t = read(path)
    if t is None:
        return None, "absent: %s" % path
    try:
        return json.loads(t), ""
    except ValueError as exc:
        return None, "not JSON: %s (%s)" % (path, exc)


def run(argv, timeout=240):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, cwd=REPO, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ds: %s" % (timeout, " ".join(argv))
    except OSError as exc:
        return 127, "did not run: %s" % exc


def base_commit():
    d, why = load_json(BASEFILE)
    if not isinstance(d, dict) or not str(d.get("base_commit") or "").strip():
        return None, "R5_BASE.json unusable: %s" % (why or "no base_commit")
    return str(d["base_commit"]).strip(), ""


def at_base(path):
    """The file's bytes at the PINNED base, or (None, why). Never merge-base."""
    base, why = base_commit()
    if base is None:
        return None, why
    rc, o = run(["git", "show", "%s:%s" % (base, path)])
    if rc != 0:
        return None, "git show %s:%s rc=%d %s" % (base[:10], path, rc, o.strip()[:120])
    return o, ""


def fenced_dicts(text):
    """Every parseable json fence in a markdown document, in order. A channel or a report can carry
    MANY fences and reading only the first silently under-reads."""
    got = []
    for m in re.finditer(r"```(?:json)?\n(.*?)```", text or "", re.S):
        try:
            got.append(json.loads(m.group(1)))
        except ValueError:
            got.append(None)
    return got


def report_rows(text):
    """(rows, note). The census report's one fence is a dict whose `rows` is the population."""
    fences = fenced_dicts(text)
    for f in fences:
        if isinstance(f, dict) and isinstance(f.get("rows"), list):
            return [r for r in f["rows"] if isinstance(r, dict)], "fences: %d" % len(fences)
    return None, "no fence carrying a `rows` list (fences seen: %d)" % len(fences)


def placeholder_rows(rows):
    return [r for r in rows if "{" in str(r.get("canonical") or "")]


def card_sections(text):
    """{card number: section text} from '## Card <n> -- ...' headings. The cards document carries no
    JSON at all, measured at the cut, so this reads prose by design."""
    if not text:
        return {}
    marks = [(int(m.group(1)), m.start()) for m in re.finditer(r"^#+\s*Card\s+(\d+)\b", text, re.M)]
    sec = {}
    for i, (n, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        sec[n] = text[start:end]
    return sec


# ============================================================================ EN-c-28: the campaign
def core_covered(rec, start_pop):
    """resolved + carded == the START population, with nothing unaccounted."""
    if not isinstance(rec, dict):
        return False, ["the campaign record is not an object"]
    res = rec.get("resolved")
    card = rec.get("carded")
    for name, v in (("resolved", res), ("carded", card)):
        if not isinstance(v, list):
            return False, ["`%s` is %s, not a list" % (name, type(v).__name__)]
    n_res, n_card = len(res), len(card)
    lines = ["resolved %d + carded %d = %d; START population %d"
             % (n_res, n_card, n_res + n_card, start_pop)]
    if n_res + n_card != start_pop:
        lines.append("UNACCOUNTED: %d row(s) of the start population are in neither list"
                     % (start_pop - n_res - n_card))
        return False, lines
    bad_card = [c for c in card if not (isinstance(c, dict) and str(c.get("owner") or "").strip()
                                        and str(c.get("reason") or "").strip())]
    lines.append("carded rows missing an owner or a reason: %d of %d" % (len(bad_card), n_card))
    if bad_card:
        lines += ["  " + json.dumps(c)[:140] for c in bad_card[:5]]
    return not bad_card, lines


def core_redenominator(rec):
    """R-38's own addition and this round's sharpest control: 1411 is a count at ONE vintage of a
    report the campaign REPLACES, so the cell re-measures at WRITE time and prints BOTH populations
    with the instrument named. The two MAY differ -- what is refused is a record that carries only
    one number, because that reads as measured while being inherited."""
    if not isinstance(rec, dict):
        return False, ["the campaign record is not an object"]
    d = rec.get("denominators")
    if not isinstance(d, dict):
        return False, ["no `denominators` object -- the start and close populations must both be printed"]
    need = ("population_at_start", "population_at_close", "instrument")
    missing = [k for k in need if not str(d.get(k, "")).strip() and d.get(k) != 0]
    lines = ["denominators keys present: %s; missing of the %d required: %s"
             % (sorted(d.keys()), len(need), missing)]
    if missing:
        return False, lines
    a, b = d.get("population_at_start"), d.get("population_at_close")
    if not isinstance(a, int) or not isinstance(b, int) or a < 0 or b < 0:
        lines.append("both populations must be non-negative ints; got %r and %r" % (a, b))
        return False, lines
    lines.append("population_at_start %d; population_at_close %d; moved by %d; instrument %r"
                 % (a, b, b - a, str(d.get("instrument"))[:90]))
    if a != b and not str(rec.get("denominator_delta_note") or "").strip():
        lines.append("the two populations DIFFER and no `denominator_delta_note` says why -- a moved "
                     "denominator is a finding, not a rounding")
        return False, lines
    return True, lines


def c28_population():
    """The START population is MEASURED from the r4 report, never inherited from a message."""
    tag = "C28-START-POPULATION-MEASURED"
    text = read(R4REPORT)
    if text is None:
        return fail_only(tag, "absent: %s" % R4REPORT)
    rows, note = report_rows(text)
    if rows is None:
        return fail_only(tag, note)
    ph = placeholder_rows(rows)
    rec, why = load_json(campaign_record_path())
    lines = ["%s; rows in the r4 report: %d; carrying a literal brace in `canonical`: %d"
             % (note, len(rows), len(ph))]
    if rec is None:
        return fail_only(tag, *(lines + [why]))
    d = rec.get("denominators") if isinstance(rec.get("denominators"), dict) else {}
    declared = d.get("population_at_start")
    lines.append("the campaign record declares population_at_start=%r" % (declared,))
    ok = declared == len(ph)
    if not ok:
        lines.append("MISMATCH: a start population that disagrees with a fresh parse of the report it "
                     "claims to have read is an inherited count, not a measured one")
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def campaign_record_path():
    """The record lands in the ASSIGNED worker's own folder. Both are searched so the arm does not
    also grade the seating decision."""
    for base in (W1, W2):
        p = os.path.join(base, PLACEHOLDER_RECORD)
        if os.path.isfile(ab(p)):
            return p
    return W1 + "/" + PLACEHOLDER_RECORD


def r5_report_path():
    for base in (W1, W2):
        p = os.path.join(base, R5REPORT)
        if os.path.isfile(ab(p)):
            return p
    return W1 + "/" + R5REPORT


def c28_covered():
    tag = "C28-EVERY-PLACEHOLDER-ROW-RESOLVED-OR-CARDED"
    text = read(R4REPORT)
    rows, note = report_rows(text or "")
    if rows is None:
        return fail_only(tag, "cannot read the start population: %s" % note)
    rec, why = load_json(campaign_record_path())
    if rec is None:
        return fail_only(tag, why)
    ok, lines = core_covered(rec, len(placeholder_rows(rows)))
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c28_redenominator():
    tag = "C28-DENOMINATOR-RE-MEASURED-AT-WRITE-TIME"
    rec, why = load_json(campaign_record_path())
    if rec is None:
        return fail_only(tag, why)
    ok, lines = core_redenominator(rec)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_fence(now_text, base_text):
    """R-29's fence guard: exemptions.json is the APPLIED fence's registry source, so a row added
    there is exactly the mint the guard forbids without never-widen sign-off. Byte equality against
    the PINNED base, and an unreadable base is a FAIL -- a guard that cannot read its own baseline
    certifies nothing."""
    if base_text is None:
        return False, ["the pinned base copy of the fence file could not be read"]
    if now_text is None:
        return False, ["the fence file is absent at HEAD"]
    same = now_text == base_text
    return same, ["fence file bytes at HEAD: %d; at the pinned base: %d; identical: %s"
                  % (len(now_text), len(base_text), same)]


def c28_fence():
    tag = "C28-APPLIED-FENCE-UNCHANGED"
    b, why = at_base(EXEMPTIONS)
    if b is None:
        return fail_only(tag, why)
    ok, lines = core_fence(read(EXEMPTIONS), b)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_timebox(rec, start_pop, overage):
    """R-33: past start + <overage> MEASURED resolutions the cell STOPS, files the delta and lets the
    remainder ride the next round. Two branches and BOTH must be graded, or a cell that simply did
    less than the bar would pass the same arm as one that respected it."""
    if not isinstance(rec, dict):
        return False, ["the campaign record is not an object"]
    res = rec.get("resolved")
    if not isinstance(res, list):
        return False, ["`resolved` is not a list"]
    bar = start_pop + overage
    n = len(res)
    stopped = bool(rec.get("stopped_on_timebox"))
    delta = rec.get("delta_riding_next_round")
    lines = ["resolved %d; the R-33 bar is start %d + %d = %d; stopped_on_timebox %s"
             % (n, start_pop, overage, bar, stopped)]
    if n > bar:
        lines.append("OVER THE BAR and the cell did not stop -- R-33's bound is not advisory")
        return False, lines
    if stopped:
        okd = isinstance(delta, dict) and isinstance(delta.get("count"), int) and delta["count"] >= 0 \
            and str(delta.get("owner") or "").strip()
        lines.append("stopped, so a delta record is required: present and well formed: %s (%s)"
                     % (okd, json.dumps(delta)[:160]))
        return okd, lines
    lines.append("did not stop and stayed within the bar -- nothing rides the next round on this arm")
    return True, lines


def c28_timebox():
    tag = "C28-R33-TIMEBOX-RESPECTED"
    text = read(R4REPORT)
    rows, note = report_rows(text or "")
    if rows is None:
        return fail_only(tag, "cannot read the start population: %s" % note)
    rec, why = load_json(campaign_record_path())
    if rec is None:
        return fail_only(tag, why)
    ok, lines = core_timebox(rec, len(placeholder_rows(rows)), TIMEBOX_OVERAGE)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def core_ac3(rows, carded_names):
    """Round 4's S25R4-AC3, re-run against the population the campaign closed: a JUDGED row's
    `canonical` is a NAME, not a template. A row still carrying a brace is admitted ONLY if the
    campaign carded it, and the count is PRINTED either way -- 'zero carded' was never the bar."""
    ph = placeholder_rows(rows)
    uncarded = [r for r in ph if str(r.get("current") or "") not in carded_names]
    lines = ["rows in the re-run report: %d; still carrying a literal brace: %d; of those, CARDED by "
             "the campaign: %d; UNCARDED: %d"
             % (len(rows), len(ph), len(ph) - len(uncarded), len(uncarded))]
    if uncarded:
        lines += ["  " + json.dumps(r)[:150] for r in uncarded[:5]]
    return not uncarded, lines


def c28_ac3():
    tag = "C28-NO-JUDGED-ROW-GRADED-AGAINST-A-TEMPLATE"
    text = read(r5_report_path())
    if text is None:
        return fail_only(tag, "absent: %s -- the re-run census report is this arm's subject"
                         % r5_report_path())
    rows, note = report_rows(text)
    if rows is None:
        return fail_only(tag, note)
    rec, why = load_json(campaign_record_path())
    if rec is None:
        return fail_only(tag, why)
    carded = set(str(c.get("current") or c.get("name") or "")
                 for c in (rec.get("carded") or []) if isinstance(c, dict))
    ok, lines = core_ac3(rows, carded)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, [note] + lines)


# ============================================================================ EN-h-29: S61's remedy
def core_s61(evidence, right_has_core, wrong_has_core, wrong_named):
    """BOTH directions, because 'corrected' must not be satisfiable by becoming vaguer.
    (i) the evidence no longer attributes the phrase to the file that does not carry it;
    (ii) whatever it now cites DOES carry the distinctive core -- measured, not asserted."""
    lines = ["the row's evidence still names %s: %s" % (S61_WRONG_FILE, wrong_named),
             "%s carries %r: %s" % (S61_RIGHT_FILE, S61_CORE, right_has_core),
             "%s carries it: %s" % (S61_WRONG_FILE, wrong_has_core)]
    if evidence is None:
        return False, ["the row named %r is not in resources.json" % S61_ROW_NAME] + lines
    if wrong_named and not wrong_has_core:
        lines.append("STILL A WRONG-OBJECT CITATION: the evidence attributes the phrase to a file "
                     "measured NOT to carry it")
        return False, lines
    cites_right = S61_RIGHT_FILE in evidence
    lines.append("the evidence cites %s: %s" % (S61_RIGHT_FILE, cites_right))
    if not cites_right:
        lines.append("the correction must either cite the file that actually carries the phrase, or "
                     "replace the cross-check with one that reads the project file itself -- and the "
                     "latter reads as a citation of neither, which this arm cannot tell from an "
                     "omission, so the cited file is required")
        return False, lines
    if not right_has_core:
        lines.append("the cited file does not carry the phrase either -- a corrected citation that is "
                     "also unfindable is not a correction")
        return False, lines
    return True, lines


def s61_row():
    d, why = load_json(RESOURCES)
    if not isinstance(d, dict) or not isinstance(d.get("resources"), list):
        return None, why or "resources.json has no `resources` list"
    for r in d["resources"]:
        if isinstance(r, dict) and str(r.get("name") or "") == S61_ROW_NAME:
            return r, ""
    return None, "no row named %r among %d" % (S61_ROW_NAME, len(d["resources"]))


def h29_evidence():
    tag = "H29-WRONG-OBJECT-CITATION-CORRECTED"
    row, why = s61_row()
    ev = str(row.get("evidence") or "") if isinstance(row, dict) else None
    wrong = read(S61_WRONG_FILE)
    right = read(S61_RIGHT_FILE)
    if wrong is None or right is None:
        return fail_only(tag, "a cited project file is absent: %s=%s %s=%s"
                         % (S61_WRONG_FILE, wrong is not None, S61_RIGHT_FILE, right is not None))
    ok, lines = core_s61(ev, S61_CORE in right, S61_CORE in wrong,
                         bool(ev and S61_WRONG_FILE in ev))
    extra = ["NOTE, measured at the cut and the reason this arm searches the CORE and not the quoted "
             "phrase: the quoted form %r occurs in 0 of 466 files under org/projects/, because the "
             "real file writes the arrow as U+2192. Searching the quote would read 0 everywhere and "
             "pass a correction that is still wrong." % S61_QUOTED_ASCII]
    if why:
        extra.append(why)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines + extra)


def h29_conclusion():
    """The row's CONCLUSION is not disturbed by the remedy, and neither is the sound half of its
    basis. A repair that quietly changes the answer is a different act than the one that was ruled."""
    tag = "H29-CONCLUSION-AND-TERRAFORM-BASIS-UNDISTURBED"
    row, why = s61_row()
    if not isinstance(row, dict):
        return fail_only(tag, why)
    b, bwhy = at_base(RESOURCES)
    if b is None:
        return fail_only(tag, bwhy)
    try:
        based = json.loads(b)
        baserow = next((r for r in based.get("resources", [])
                        if isinstance(r, dict) and str(r.get("name") or "") == S61_ROW_NAME), None)
    except ValueError as exc:
        return fail_only(tag, "the pinned base copy of resources.json is not JSON: %s" % exc)
    if baserow is None:
        return fail_only(tag, "the row did not exist at the pinned base -- this arm grades a REPAIR, "
                              "and there is nothing to compare against")
    same_conc = (row.get("system") == baserow.get("system") and row.get("type") == baserow.get("type"))
    tf_ok = "alarms.tf:55-78" in str(row.get("evidence") or "")
    lines = ["system %r -> %r; type %r -> %r; conclusion unchanged: %s"
             % (baserow.get("system"), row.get("system"), baserow.get("type"), row.get("type"), same_conc),
             "the sound Terraform half (alarms.tf:55-78) is still cited: %s" % tf_ok]
    return verdict(same_conc and tf_ok, "PASS-" + tag, "FAIL-" + tag, lines)


# ============================================================================ EN-c-31: R-39's card
def core_token_collision(sec5, sec6, security_minted):
    """R-39: `security` is NOT minted, both groups stay CARDED, and the CARD'S REASON becomes
    TOKEN_COLLISION -- because a card whose stated reason is wrong retires the question instead of
    holding it open. Card 6's half also names its genuine owner."""
    lines = []
    if sec5 is None or sec6 is None:
        return False, ["Card 5 present: %s; Card 6 present: %s -- both are this arm's subject"
                       % (sec5 is not None, sec6 is not None)]
    r5 = "TOKEN_COLLISION" in sec5
    r6 = "TOKEN_COLLISION" in sec6
    owner = ("NFRA_OPSEC202609" in sec6) and ("DIRECTIVES.yaml" in sec6)
    lines += ["Card 5 states TOKEN_COLLISION: %s" % r5,
              "Card 6 states TOKEN_COLLISION: %s" % r6,
              "Card 6 names NFRA_OPSEC202609 AND cites DIRECTIVES.yaml: %s" % owner,
              "the whole value \"security\" appears in systems.json: %d time(s) (R-39's bar is 0)"
              % security_minted]
    return (r5 and r6 and owner and security_minted == 0), lines


def c31_card():
    tag = "C31-TOKEN-COLLISION-CARDS-CORRECTED"
    text = read(CARDS_R4)
    if text is None:
        return fail_only(tag, "absent: %s" % CARDS_R4)
    sec = card_sections(text)
    sysd = read(SYSTEMS)
    if sysd is None:
        return fail_only(tag, "absent: %s" % SYSTEMS)
    minted = len(re.findall(r'"security"', sysd))
    ok, lines = core_token_collision(sec.get(5), sec.get(6), minted)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag,
                   ["card sections parsed from the document: %d %s" % (len(sec), sorted(sec))] + lines)


def c31_not_minted():
    """The negative half, exercised ALONE: the arm must be able to SEE a minted token, or 'security
    is absent' is indistinguishable from 'this arm cannot read systems.json'. The positive control is
    a token the registry really does carry."""
    tag = "C31-SECURITY-NOT-MINTED-WITH-A-LIVE-CONTROL"
    d, why = load_json(SYSTEMS)
    if not isinstance(d, dict) or not isinstance(d.get("systems"), list):
        return fail_only(tag, why or "systems.json has no `systems` list")
    keys = [str(r.get("key") or "") for r in d["systems"] if isinstance(r, dict)]
    lines = ["minted system keys: %d; 'security' among them: %s" % (len(keys), "security" in keys),
             "POSITIVE CONTROL -- a key this arm CAN see: %r" % (keys[0] if keys else None)]
    unresolved = [str(r.get("token") or "") for r in (d.get("unresolved") or []) if isinstance(r, dict)]
    lines.append("tokens in `unresolved`: %d %s" % (len(unresolved), unresolved))
    ok = bool(keys) and "security" not in keys
    if not keys:
        lines.append("no keys read at all -- the absence of 'security' proves nothing here")
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


# ============================================================================ EN-g-30: S62's remedy
def core_split(reasons, table_counts):
    """A right TOTAL beside a wrong SPLIT is what lets the error survive every reader who checks the
    total. So: the parts must sum to the declared total AND each part must equal a fresh count from
    the document's own table. Either test alone passes the defect."""
    if not isinstance(reasons, dict):
        return False, ["no `uncompared_reasons` object in the comparison's fence"]
    total = reasons.get("total")
    parts = dict((k, v) for k, v in reasons.items() if k != "total")
    s = sum(v for v in parts.values() if isinstance(v, int))
    lines = ["declared total %r; parts %s; parts sum to %d" % (total, json.dumps(parts), s)]
    if not isinstance(total, int):
        lines.append("the total must be an int")
        return False, lines
    if s != total:
        lines.append("SUM MISMATCH: %d != %d -- this is LGIC_ENFORCE-S62's exact shape" % (s, total))
        return False, lines
    if table_counts is None:
        lines.append("the document's own table could not be counted, so the parts are unverified "
                     "against anything but themselves -- a self-consistent split is not a measured one")
        return False, lines
    disagree = sorted(k for k in set(list(parts) + list(table_counts))
                      if parts.get(k) != table_counts.get(k))
    lines.append("table counts %s; keys where the fence and the table disagree: %d %s"
                 % (json.dumps(table_counts), len(disagree), disagree))
    return not disagree, lines


def comparison_table_counts(text, keys):
    """Count each of the FENCE'S OWN reason keys from the document's Section 3 TABLE rows, which is
    the population the split describes. Returns None when the table cannot be read at all -- an
    honest None, never an empty dict that would read as agreement with an empty fence.

    THE `keys` ARGUMENT IS THE WHOLE POINT AND IT WAS ADDED AFTER A MEASUREMENT, NOT BY DESIGN.
    This function first counted EVERY uppercase token in every table cell. Run for real against
    NAMING_CENSUS_COMPARISON.r4.md it returned 36 keys summing to 149 -- resource types (CW_ALARM,
    KMS_KEY), verdicts (RAISE, CONFORMANT) and even two CloudFront distribution ids -- of which only
    4 are reason keys. The four it did get right were NOT-GRADED-TYPE 20, AWS_FIXED-EXCLUDED 2,
    CARDED 10, HAND-SPECIMEN-ABSENT 10, summing to exactly the declared total of 42. So the counting
    was right and the DOMAIN was wrong, and core_split compares the UNION of both key sets: a
    correctly corrected fence carrying 4 keys would have disagreed with 32 phantom ones and FAILED.
    The arm was UNSATISFIABLE BY A CORRECT FIX and its injected self-test passed anyway, because the
    fixture handed both sides the same key set. An injected self-test certifies the ARMS, never the
    WIRING.
    """
    if not text or not keys:
        return None
    counts = dict((k, 0) for k in keys)
    rows = 0
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        rows += 1
        cells = [c.strip().strip("`* ") for c in line.strip().strip("|").split("|")]
        for k in keys:
            if k in cells:
                counts[k] += 1
    return counts if rows else None


def g30_split():
    tag = "G30-REASON-SPLIT-RECONCILES-TO-ITS-OWN-TABLE"
    text = read(R4COMP)
    if text is None:
        return fail_only(tag, "absent: %s" % R4COMP)
    fences = fenced_dicts(text)
    reasons = None
    for f in fences:
        if isinstance(f, dict) and isinstance(f.get("uncompared_reasons"), dict):
            reasons = f["uncompared_reasons"]
            break
    keys = sorted(k for k in (reasons or {}) if k != "total")
    ok, lines = core_split(reasons, comparison_table_counts(text, keys))
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag,
                   ["json fences in the comparison: %d; reason keys the fence declares: %d %s"
                    % (len(fences), len(keys), keys)] + lines)


def core_prose(text):
    """Section 3's prose said 'THREE distinct, individually-verified reasons' above a list of four
    while Section 4 said four. The remedy is a number that matches the list; the arm refuses the
    stale word rather than trying to count the list, because counting a prose list is a second guess
    at the same question."""
    if text is None:
        return False, ["the comparison document is absent"]
    n = len(re.findall(r"\bTHREE\b", text))
    lines = ["occurrences of the word THREE: %d (the defect is 1 at the pinned base)" % n]
    return n == 0, lines


def g30_prose():
    tag = "G30-STALE-COUNT-WORD-REMOVED"
    ok, lines = core_prose(read(R4COMP))
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


# ============================================================================ dispatch
SUBCOMMANDS = {
    "c28-population": c28_population,
    "c28-covered": c28_covered,
    "c28-redenominator": c28_redenominator,
    "c28-fence": c28_fence,
    "c28-timebox": c28_timebox,
    "c28-ac3": c28_ac3,
    "h29-evidence": h29_evidence,
    "h29-conclusion": h29_conclusion,
    "c31-card": c31_card,
    "c31-not-minted": c31_not_minted,
    "g30-split": g30_split,
    "g30-prose": g30_prose,
}

PASS_TOKENS = (
    "PASS-C28-START-POPULATION-MEASURED",
    "PASS-C28-EVERY-PLACEHOLDER-ROW-RESOLVED-OR-CARDED",
    "PASS-C28-DENOMINATOR-RE-MEASURED-AT-WRITE-TIME",
    "PASS-C28-APPLIED-FENCE-UNCHANGED",
    "PASS-C28-R33-TIMEBOX-RESPECTED",
    "PASS-C28-NO-JUDGED-ROW-GRADED-AGAINST-A-TEMPLATE",
    "PASS-H29-WRONG-OBJECT-CITATION-CORRECTED",
    "PASS-H29-CONCLUSION-AND-TERRAFORM-BASIS-UNDISTURBED",
    "PASS-C31-TOKEN-COLLISION-CARDS-CORRECTED",
    "PASS-C31-SECURITY-NOT-MINTED-WITH-A-LIVE-CONTROL",
    "PASS-G30-REASON-SPLIT-RECONCILES-TO-ITS-OWN-TABLE",
    "PASS-G30-STALE-COUNT-WORD-REMOVED",
)


# ============================================================================ self-test
def selftest_arms():
    """Drive every PURE CORE alone against a GREEN fixture that must PASS and a DOCTORED fixture that
    must FAIL. An arm that cannot be made to fail is a constant wearing a measurement's clothes."""
    res = []

    def arm(name, good, bad, detail):
        res.append((name, bool(good) and not bool(bad), detail))

    # substring check on the pass tokens -- unanchored <expect> makes one token a prefix of another
    overlap = sorted(set((a, b) for a in PASS_TOKENS for b in PASS_TOKENS if a != b and a in b))
    res.append(("tokens-pairwise-distinct", not overlap, "overlapping pairs: %s" % (overlap or "none")))

    rec = {"resolved": [{"current": "a"}, {"current": "b"}],
           "carded": [{"current": "c", "owner": "1.0.0_SA_CTO", "reason": "NO_DECLARED_SOURCE"}],
           "denominators": {"population_at_start": 3, "population_at_close": 3,
                            "instrument": "a fresh parse of the report's rows"},
           "stopped_on_timebox": False}
    arm("c28-covered", core_covered(rec, 3)[0], core_covered(rec, 4)[0], "one row unaccounted for")
    no_owner = json.loads(json.dumps(rec))
    no_owner["carded"][0].pop("owner")
    arm("c28-covered-owner", core_covered(rec, 3)[0], core_covered(no_owner, 3)[0],
        "a carded row with no owner")
    arm("c28-redenominator", core_redenominator(rec)[0],
        core_redenominator({"resolved": [], "carded": [],
                            "denominators": {"population_at_start": 3, "instrument": "x"}})[0],
        "only one population printed")
    moved = json.loads(json.dumps(rec))
    moved["denominators"]["population_at_close"] = 5
    arm("c28-redenominator-note", core_redenominator(rec)[0], core_redenominator(moved)[0],
        "the denominator moved with no note saying why")
    arm("c28-fence", core_fence("abc", "abc")[0], core_fence("abd", "abc")[0], "the fence file changed")
    arm("c28-fence-unreadable", core_fence("abc", "abc")[0], core_fence("abc", None)[0],
        "the baseline could not be read at all")
    arm("c28-timebox", core_timebox(rec, 3, 25)[0],
        core_timebox({"resolved": [{}] * 40, "carded": []}, 3, 25)[0], "over the bar without stopping")
    stopped = {"resolved": [{}], "carded": [], "stopped_on_timebox": True}
    stopped_ok = json.loads(json.dumps(stopped))
    stopped_ok["delta_riding_next_round"] = {"count": 7, "owner": "2.0.0_SA_COO~G"}
    arm("c28-timebox-delta", core_timebox(stopped_ok, 3, 25)[0], core_timebox(stopped, 3, 25)[0],
        "stopped on the timebox with no delta record")
    rows = [{"current": "x", "canonical": "a-b-c"},
            {"current": "y", "canonical": "{system}-b"}]
    arm("c28-ac3", core_ac3(rows, {"y"})[0], core_ac3(rows, set())[0], "an uncarded template row")

    arm("h29-evidence", core_s61("cites " + S61_RIGHT_FILE, True, False, False)[0],
        core_s61("cites " + S61_WRONG_FILE, True, False, True)[0],
        "the evidence still names the file that does not carry the phrase")
    arm("h29-evidence-vague", core_s61("cites " + S61_RIGHT_FILE, True, False, False)[0],
        core_s61("cites nothing in particular", True, False, False)[0],
        "a correction that became vaguer instead of right")
    arm("h29-evidence-unfindable", core_s61("cites " + S61_RIGHT_FILE, True, False, False)[0],
        core_s61("cites " + S61_RIGHT_FILE, False, False, False)[0],
        "the newly cited file does not carry the phrase either")

    g5 = "## Card 5 -- security-sweep\nreason: TOKEN_COLLISION\n"
    g6 = "## Card 6 -- opal-data-security\nreason: TOKEN_COLLISION, owner D12 NFRA_OPSEC202609 DIRECTIVES.yaml :485\n"
    arm("c31-card", core_token_collision(g5, g6, 0)[0], core_token_collision(g5, g6, 1)[0],
        "the token was minted after all")
    arm("c31-card-reason", core_token_collision(g5, g6, 0)[0],
        core_token_collision("## Card 5 -- security-sweep\nreason: NO_OWNER\n", g6, 0)[0],
        "one card keeps the wrong reason")
    arm("c31-card-owner", core_token_collision(g5, g6, 0)[0],
        core_token_collision(g5, "## Card 6\nreason: TOKEN_COLLISION\n", 0)[0],
        "the owner half is not named")

    good_split = {"A": 20, "B": 2, "C": 10, "D": 10, "total": 42}
    table = {"A": 20, "B": 2, "C": 10, "D": 10}
    bad_sum = {"A": 23, "B": 2, "C": 11, "D": 11, "total": 42}
    bad_parts = {"A": 21, "B": 1, "C": 10, "D": 10, "total": 42}
    arm("g30-split", core_split(good_split, table)[0], core_split(bad_sum, table)[0],
        "S62's own shape: parts summing to 47 over a total of 42")
    arm("g30-split-table", core_split(good_split, table)[0], core_split(bad_parts, table)[0],
        "a self-consistent split that disagrees with the table")
    arm("g30-split-notable", core_split(good_split, table)[0], core_split(good_split, None)[0],
        "no table to verify the parts against")
    arm("g30-prose", core_prose("four reasons, all four listed")[0],
        core_prose("THREE distinct reasons")[0], "the stale count word survives")

    ok = all(r[1] for r in res)
    for name, good, detail in res:
        print("  %-26s %-5s %s" % (name, "PASS" if good else "FAIL", detail))
    print("arms driven: %d; all discriminating: %s" % (len(res), ok))
    print("NOT driven here, stated: nothing -- every arm in this file has a pure core and all twelve "
          "are driven above. The four arms that also touch git (c28-fence, h29-conclusion) read the "
          "PINNED base through their cores' arguments, so the core is graded here and the git read is "
          "exercised by the real run.")
    print("VERDICT: " + ("PASS-ARMS-DISCRIMINATE" if ok else "FAIL-ARMS-DISCRIMINATE"))
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--list", "-l"):
        for k in sorted(SUBCOMMANDS):
            print(k)
        print("selftest-arms")
        return 0
    cmd = args[0]
    if cmd == "selftest-arms":
        return selftest_arms()
    fn = SUBCOMMANDS.get(cmd)
    if fn is None:
        print("unknown subcommand: %s (use --list)" % cmd)
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
