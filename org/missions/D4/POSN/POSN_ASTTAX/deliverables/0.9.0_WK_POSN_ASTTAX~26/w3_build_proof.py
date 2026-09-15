"""Build the PROOF-OF-SPEC instance for POSN_ASTTAX.TO-W3-1 (slot ~26).

WHY A BUILDER AND NOT A HAND-WRITTEN JSON: three of this instance's fields are JOINS the
checker re-computes and refuses on -- `criterion_verbatim` must be the TO's own words,
`invocation` must match the TO's <invocation> with only the declared placeholders expanded,
and `expect` must be a pattern the row's own output_evidence MATCHES. All three are read or
verified here, from the TO file in this worktree and from the captured run logs, so a typo
cannot pass as a citation. It REFUSES to write if any expect fails to match its evidence.

Usage (from the workspace worktree root): PYTHONUTF8=1 python3 <this>
"""
import io
import json
import os
import re
import sys

D = 'org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~26'
TO_PATH = ('org/missions/D4/POSN/POSN_ASTTAX/task-orders/'
           'POSN_ASTTAX.TO-W3-1.positioning-summary-presence-rounding-footer-copy.md')
OUT = os.path.join(D, 'POSN_ASTTAX.TO-W3-1.positioning-summary-presence-rounding-footer-copy'
                      '.proof_of_spec.json')
PORTAL_PIN = '10a2799c67c519288fcd7d4ae6e3b86d5ed48b5a'
# The workspace commit that CARRIED the ledger append and the first cut of this instance;
# read back from git (2191049ef1~0.9.0_WK_POSN_ASTTAX~26~L7(POSN_ASTTAX.TO-W3-1 ...)), never assumed.
LEDGER_PIN = '2191049ef15440df83a00ef131ea972fb8f0f7e2'

# The placeholder values this worker resolved, ONE value per token (the checker
# back-references a repeated token, so a second value would diverge).
SUB = {
    'PORT': '5179',
    'FIXTURES': '.scratch/w3_fixtures.json',
    'PRESENCE_UNIT_CONTROL': '../' + D + '/w3_presence_unit_control.ts',
}


def read(path):
    return io.open(path, encoding='utf-8', newline='').read()


def to_criteria():
    """{id: (invocation, expect)} read from the TO in this worktree (the AMENDED text)."""
    text = read(TO_PATH)
    out = {}
    for m in re.finditer(r'<criterion id="([^"]+)"[^>]*>(.*?)</criterion>', text, re.S):
        cid, body = m.group(1), m.group(2)
        inv = re.search(r'<invocation>(.*?)</invocation>', body, re.S)
        exp = re.search(r'<expect>(.*?)</expect>', body, re.S)
        out[cid] = (inv.group(1).strip() if inv else None,
                    exp.group(1).strip() if exp else None)
    return out


def expand(inv):
    for k, v in SUB.items():
        inv = inv.replace('<%s>' % k, v)
    return inv


CRIT = to_criteria()

AC1_EV = read(os.path.join(D, 'w3_ac1.txt')).strip() + """

GRAIN, STATED: `prd-signoff.py status` grades THE PRD IN THE TREE IT RUNS IN. This worktree is
the round-6 issuance commit (910815809f), which carries PRD v0.10 @59113e257a -- the pin the
order carried when it was cut. The order was AMENDED mid-execution to PRD v0.11 @ab2ee8052a;
that pin's sign-off state, read from the shared branch SITEZ @1b791c6a11 (w3_ac1_v011_pin.txt):
  4.0.0_SA_CRO~Z.json : prd_version v0.11, prd_pin ab2ee8052a7660af407a49b444979e42ee286781,
                        half "brief", verdict SIGNED, signed_at 2026-09-15T04:10:52Z
  3.0.0_SA_CVO~Z.json : half "ratified-text", verdict SIGNED at half_hash 809d97ea...5ab9
                        (v0.11 changes the brief half only -- "ENDPOINT untouched, so the
                        ratified-text signature stands"), so both halves are SIGNED at the
                        amended pin as well."""

AC2_EV = read(os.path.join(D, 'w3_ac2.txt')).strip()
AC3_EV = read(os.path.join(D, 'w3_ac3_presence_unit_control.txt')).strip()
AC4_EV = read(os.path.join(D, 'w3_ac4_tsc.txt')).strip()
AC7_EV = read(os.path.join(D, 'w3_ac7.txt')).strip()


def dom_section(path, title):
    text = read(path)
    parts = re.split(r'\n=+ (.*?) =+\n', text)
    for i in range(1, len(parts), 2):
        if parts[i].strip() == title:
            return parts[i + 1].rstrip()
    # the first section has no leading newline before its banner
    m = re.search(r'=+ ' + re.escape(title) + r' =+\n(.*?)(?=\n=+ |\Z)', text, re.S)
    return m.group(1).rstrip() if m else '(SECTION NOT FOUND: %s)' % title


def keep(block, prefixes):
    out = []
    for line in block.split('\n'):
        if any(line.startswith(p) for p in prefixes):
            out.append(line)
    return '\n'.join(out)


POST = os.path.join(D, 'w3_postedit_dom_read.txt')
PRE = os.path.join(D, 'w3_preedit_dom_read.txt')
KEEP = ('SUBTITLE', 'LEGEND', '   "', 'COUNTS', 'ROWS(', 'LABELS(', 'LABEL SHAPE',
        'LABEL JOIN RESULT', 'RAW-FLOAT LABELS', 'NOTICES', 'FOOTERS', '   [')

AC5_EV = """W3-AC5's THREE NAMED CAPTURES RAN AS WRITTEN, rc 0 (w3_ac5_uismoke.txt): each printed
IDENTITY firmId=opal-capital, VIEWPORT 1440x900, LOC /positioning, SAVED .scratch/w3_models.png /
.scratch/w3_models_bench.png / .scratch/w3_etfs.png, and "FIXTURES: 6 declared" with the clicks
CLICKED: Benchmark and CLICKED: ETFs. FIXTURES FROM THE SERVED BYTES, VersionIds printed by
w3_fixture_manifest.txt: positioning_data.json AqBtm_5o.2QeiCBRP_veC8HV2Xk0OSaj; etfs
positioning_data.json MkASX8obEltFZpHHzNa81cuAVXKf7wR2; holdings_attribution_data.json
mOBBmXhjOyNPM2ue_.3C9G1eR79lUrlk; satellites registry.json xfm3WLmuZh3G4YtGpHUMs0R4Hyr4gCoN,
holdings.json 67GP52SdV1rw6QFVNPytU6ec4TvhwJh3, characteristics.json rt61ogajZQy79meUlsY1X_mIdPngxJTZ.

THE PNGs READ (the Read tool renders them; w3_models.png, w3_models_bench.png, w3_etfs.png, and
the supplementary w3_models_expanded.png which opens the matrix the named invocation leaves
collapsed): MODELS -- legend Fixed Income (Bonds & Cash), Equity (Stocks), Structured (Options,
VIX & overlays); bars 100% | 82.6%/17.4% | 32.8%/67.2% | 12.7%/85.8%/1.5% | 8.1%/89.9%/2%; no
Commodities, no Alternatives, no zero row; ASSET CLASS (3) over three rows. BENCHMARK -- the same
3-class legend, bars 100% | 85%/15% | 40%/60% | 15%/85% | 15%/85%. ETFS -- legend Fixed Income and
Equity only; bars 0.62%/99.38% | 0.95%/99.05% | 0.09%/99.9% | 0.63%/99.36%.

THE DOM READ of the same four states (supplementary instrument, w3_dom_read.mjs; row W26-S2 records
why the named instrument's TEXT dump cannot carry this clause -- ui-smoke.mjs:334 slices
body.innerText to 160 characters, which on this page is the left nav, so its label denominator is 0):

-- MODELS / Portfolio view --
__MODELS_BLOCK__

-- MODELS / Benchmark view --
__BENCH_BLOCK__

-- ETFS / Portfolio view --
__ETFS_BLOCK__

THE BENCHMARK SET, EXPLAINED FROM THE FIXTURE (w3_fixtures_build.txt, computed from the served
bytes BEFORE any render was read): "EXPECTED MODELS presence (portfolio view, 5 columns):
[Fixed Income, Equity, Structured]"; "EXPECTED MODELS presence (benchmark view, 10 columns =
portfolio + benchmark): [Fixed Income, Equity, Structured]"; "BENCHMARK-ONLY CLASSES (present in a
benchmark column, absent from every portfolio column): []". SO: NO CLASS IS BENCHMARK-ONLY IN
TODAY'S BYTES -- said plainly, as the criterion asks. Structured appears in the Benchmark view
because the LT and ULT PORTFOLIO columns carry 1.5 and 2.0 while every benchmark column carries 0;
the constructed benchmark-only edge is W3-AC3 case (a), and the reading is row W26-S6.

THE MODELS LABELS AGAINST THE PRE-EDIT CONTROL (w3_label_control_compare.txt -- the same
instrument, fixtures, port and states, with the two files swapped to refs/drains/posn-6-portal and
restored by md5):
  MODELS / Portfolio view   PRE  (11 labels): ["100%","82.6%","17.4%","32.8%","67.2%","12.7%","85.8%","1.5%","8.1%","89.9%","2%"]
                            POST (11 labels): ["100%","82.6%","17.4%","32.8%","67.2%","12.7%","85.8%","1.5%","8.1%","89.9%","2%"]
                            VERDICT: BYTE-IDENTICAL
  MODELS / Benchmark view   VERDICT: BYTE-IDENTICAL (9 labels)
  ETFS / Portfolio view     VERDICT: BYTE-IDENTICAL (8 labels)
  SECTIONS COMPARED: 4 of 4."""
AC5_EV = (AC5_EV
  .replace("__MODELS_BLOCK__", keep(dom_section(POST, "MODELS / Portfolio view (Expand Details open)"), KEEP))
  .replace("__BENCH_BLOCK__", keep(dom_section(POST, "MODELS / Benchmark view"), KEEP))
  .replace("__ETFS_BLOCK__", keep(dom_section(POST, "ETFS / Portfolio view"), KEEP)))

AC6_EV = """W3-AC6's NAMED CAPTURE RAN AS WRITTEN, rc 0 (w3_ac6_uismoke.txt): CLICKED: Satellites,
VIEWPORT 1440x900, SAVED .scratch/w3_sats.png, "FIXTURES: 6 declared; 5 matched >=1 URL" (the ETF
key is dead in this mode by construction). holdings.json at VersionId
67GP52SdV1rw6QFVNPytU6ec4TvhwJh3, as_of 2026-09-14.

THE PNG READ (w3_sats.png, and the supplementary w3_sats_expanded.png for the matrix): legend
Fixed Income (green), Equity (blue), Structured (pink), Commodities (yellow) -- FOUR, in
ASSET_CLASSES order, the three shared with the Models render drawn in the same swatches; ASSET
CLASS (4) over exactly four rows Fixed Income (%) / Equity (%) / Structured (%) / Commodities (%),
no Alternatives; the panel footer reads "Source: Black Diamond, holdings as of 2026-09-14"; the
subtitle reads "Asset allocation and holdings breakdown across Opal Satellites, from their Black
Diamond holdings."; no notice is rendered (no unresolved satellite in these bytes).

THE DOM READ (colour tokens as COMPUTED VALUES, not source literals):
__SATS_BLOCK__

THE COLOUR COMPARISON, the two renders side by side (same three tokens for the three shared
classes -- so hiding Alternatives shifted nothing):
  Models      Fixed Income rgb(16, 185, 129) | Equity rgb(59, 130, 246) | Structured rgb(236, 72, 153)
  Satellites  Fixed Income rgb(16, 185, 129) | Equity rgb(59, 130, 246) | Structured rgb(236, 72, 153)
              + Commodities rgb(234, 179, 8)

THE SATELLITES LABELS BESIDE THEIR RAW SERVED SUMS (the join is computed from the fixture by a
second implementation of the rule; 30 of 30 agree, w3_postedit_dom_read.txt):
  Opal Satellite 15  Fixed Income raw=74.16              -> 74.16%
  Opal Satellite 30  Fixed Income raw=62.589999999999996 -> 62.59%
  Opal Satellite 30  Equity       raw=29.820000000000004 -> 29.82%
  Opal Satellite 50  Fixed Income raw=39.43000000000001  -> 39.43%
  Opal Satellite 60  Fixed Income raw=27.830000000000002 -> 27.83%
  Opal Satellite 90  Equity       raw=90.24000000000001  -> 90.24%
  (every other label's raw sum already carried at most two decimals and is unchanged)

THE MODELS FOOTER CONTROL, two planes:
  RENDERED, this branch: the Positioning Summary footer in Models, Benchmark and ETFs modes reads
  "Source: Bloomberg." -- FOOTERS [0] in the three non-satellite sections above.
  SOURCE, pre-change vs now (w3_footer_control.txt):
    refs/drains/posn-6-portal:...PositioningSummary.tsx:1382
        <SmartPanelFooter sourceKey="model_pkl" content="Source: Bloomberg." />
    wk-posn-6-26-portal:...PositioningSummary.tsx:1503
        <SmartPanelFooter sourceKey="model_pkl" content="Source: Bloomberg." />
  BYTE-IDENTICAL in both planes.

DISCLOSED, NOT MINE: footers [1] and [2] in the Satellites section still read "Source: Bloomberg."
-- the Portfolio Composition and Holdings panels are HoldingsTab.tsx, which TO-W3-1 step 5 assigns
to TO-W2-1 (F4); the issuer already carries that as POSN_ASTTAX-Z-S136."""
AC6_EV = AC6_EV.replace("__SATS_BLOCK__", keep(dom_section(POST, "SATELLITES / Portfolio view"), KEEP))

AC8_EV = """JUDGMENT -- the readings, with NO verdict (3.0.0_SA_CVO~Z grades this at L9).

READING 1 -- DOES AN ABSENT ROW READ AS "THIS BOOK HOLDS NONE"?
WHAT AN ANALYST NOW SEES (measured, not imagined): in Models the legend lists 3 classes and the
matrix 3 rows; in ETFs 2 and 2; in Satellites 4 and 4. The five-class vocabulary is NEVER shown in
one place on this panel, so a reader who has not seen another mode has no way, from this panel
alone, to learn that Alternatives exists at all -- the absence is silent, which is what "no row"
means. THREE THINGS CUT THE OTHER WAY, all on the same page: (a) flipping modes changes the list
(Models 3 -> Satellites 4), so the vocabulary is discoverable by using the control the page already
has; (b) the Portfolio Composition panel directly below still prints all five classes in its legend
in every mode (row W26-S3), so the five ARE on screen -- though as a second, disagreeing claim
rather than as an answer; (c) the matrix rows and the bar segments now agree with the legend by
construction, so nothing on the panel asserts a class the books do not hold. WHAT THE OLD ZERO ROW
SAID: "Alternatives (%) 0 0 0 0 0" is an explicit "this book holds none", and its removal is
Andrew's own ruling (~00:4xZ, ~02:1xZ) against F2's design comment, which had argued exactly the
opposite ("a zero row ... is a different and truer statement than an absent row"). The cost of the
new state is that "holds none" and "is not part of the vocabulary" now render identically ON THIS
PANEL; the cost of the old one was five rows of zeros on every book in every mode.

READING 2 -- DOES THE LABEL FORMAT LOSE A DISTINCTION A SMALL SLEEVE CARRIED?
THE ORDER'S ACT 2 WAS AMENDED MID-EXECUTION (PRD v0.11 @ab2ee8052a, row W26-S1), and the amendment
turns on exactly this question: Math.round WOULD have lost it. MEASURED on today's served bytes,
had Math.round shipped: PFDE's Fixed Income sleeve 0.09% would render "0%" beside a drawn bar --
a label asserting zero for a class the same panel draws as present; Opal Satellite 30's Structured
0.35% and Satellite 15's Equity 17.5% would read "0%" and "18%"; every Models label would change
(82.6% -> 83%). THE SHIPPED RULE (at most two decimals, trailing zeros dropped) loses NOTHING the
served rows carry: the served weights are two-decimal, and the 5 labels that changed against the
pre-edit control are IEEE artifacts collapsing onto the served value (62.589999999999996% ->
62.59%). WHAT IS STILL LOST, stated: a sleeve below 0.005% would render "0%" under this rule too,
and no such sleeve exists in today's six served keys. WHAT THE READER GAINS: 27 of 30 Satellites
labels and 7 of 8 ETFs labels carry two decimals -- a denser label than the whole-percent siblings
beside them, which is a legibility judgment this worker does not grade."""


ROWS = [
    dict(cid='W3-AC1', method='live_read', ev=AC1_EV,
         den='3 clauses of 3: ancestry, the served VersionId, the PRD verdict; 6 of 6 fixture keys headed',
         expect=r'REF-IS-ANCESTOR.*67GP52SdV1rw6QFVNPytU6ec4TvhwJh3.*ADMITTED'),
    dict(cid='W3-AC2', method='diff', ev=AC2_EV,
         den='2 of 2 expected paths changed; 0 of 0 paths under shared/, tabs/ or src/api',
         expect=r'2 files changed, 168 insertions\(\+\), 32 deletions\(-\).*'
                r'PATHS CHANGED: 2 of 2 expected.*F4 SURFACES \(shared/, tabs/, src/api\): 0 of 0 expected'),
    dict(cid='W3-AC3', method='test_suite', ev=AC3_EV,
         den='6 real cases (a,b,c,d,e,f) + 1 deliberately-wrong falsifier = 7 printed',
         expect=r'REAL CASES: 6 \(a,b,c,d,e,f\) -- failures 0 of 6.*'
                r'FALSIFIER  : case g printed FAIL as required.*RESULT: OK \(exit 0\)'),
    dict(cid='W3-AC4', method='command', ev=AC4_EV,
         den='2027 files checked (tsc -b --listFiles, of which 481 under src/); 1 injected error, 1 run failed',
         expect=r'RUN 1: the build as the criterion names it ===\nEXIT=0.*'
                r'INJECTED-RUN EXIT=2.*RUN 2: the build again, after the revert ===\nEXIT=0'),
    dict(cid='W3-AC5', method='manual_read_with_citation', ev=AC5_EV,
         den='3 named captures + 1 supplementary expanded capture; labels 11 of 11 (Models), '
             '9 of 9 (Benchmark), 8 of 8 (ETFs) match the shape; 3 of 3 label dumps byte-identical to the control',
         expect=r'LEGEND   : 3 entries.*ASSET CLASS \(3\).*11 match of 11 labels  EQUAL.*'
                r'LEGEND   : 2 entries.*ASSET CLASS \(2\).*8 match of 8 labels  EQUAL.*BYTE-IDENTICAL'),
    dict(cid='W3-AC6', method='manual_read_with_citation', ev=AC6_EV,
         den='1 named capture + 1 supplementary expanded capture; legend 4 of 4 classes; '
             '30 of 30 labels match the shape and 30 of 30 agree with the served sums; 3 footers read per mode',
         expect=r'LEGEND   : 4 entries.*"Commodities"  rgb\(234, 179, 8\).*ASSET CLASS \(4\).*'
                r'Source: Black Diamond, holdings as of 2026-09-14.*30 match of 30 labels  EQUAL.*'
                r'content="Source: Bloomberg\." />'),
    dict(cid='W3-AC7', method='command', ev=AC7_EV,
         den='1 of 1 commit above the ref, 0 by another author; gitlink read 2 ways; 1 ledger line',
         expect=r'10a2799c67c519288fcd7d4ae6e3b86d5ed48b5a 0\.9\.0_WK_POSN_ASTTAX~26.*'
                r'160000 commit e85f6eb84f3a1771a37011a7e77e372570bad02a\s+portal.*wk-posn-6-26-portal'),
    dict(cid='W3-AC8', method='manual_read_with_citation', ev=AC8_EV,
         den='2 readings recorded (the absent row; the label format), 0 verdicts offered',
         expect=None, judgment=True),
]

SURPRISES = [
    'POSN_ASTTAX-Z-W26-S1: acted on the issuer\'s mid-order amendment -- act 2 (Math.round) superseded by '
    'PRD v0.11 @ab2ee8052a; the two-decimal trimmed label shipped instead, and the amended order text was '
    'copied from SITEZ @1b791c6a11 into this worktree before the status flip.',
    'POSN_ASTTAX-Z-W26-S2: scripts/ui-smoke.mjs prints a 160-character prefix of body.innerText, so the '
    'label clause graded "in the TEXT dump" has a denominator of 0 labels there; a supplementary DOM read '
    'carries it (label count beside match count, per mode).',
    'POSN_ASTTAX-Z-W26-S3: the presence rule landed on the Positioning Summary while the Portfolio '
    'Composition legend on the same page still lists all five classes in every mode (HoldingsTab.tsx, F4\'s '
    'file, outside this order\'s <paths>).',
    'POSN_ASTTAX-Z-W26-S4: the portal repo does not ignore .scratch/, so W3-AC5/W3-AC6 write capture '
    'artifacts into a path W3-AC2\'s unscoped status reads; the artifacts were copied to deliverables and '
    'the directory removed before the graded run.',
    'POSN_ASTTAX-Z-W26-S5: at the 1440px acceptance width the longest Satellites label ("90.24%") is clipped '
    'at the panel edge -- PRE-EXISTING (the pre-edit string was 12 characters longer) and narrowed, not '
    'introduced, by this cell.',
    'POSN_ASTTAX-Z-W26-S6: the order\'s presence rule (portfolio columns ALWAYS in the set) and '
    'C-PRESENT-CLASSES\'s sentence ("any column the current view DRAWS") differ on the Benchmark view; the '
    'order\'s reading is what is implemented, and it shows Structured with no drawn benchmark segment.',
]

INST = {
    'schema_version': '1.0',
    'to_id': 'POSN_ASTTAX.TO-W3-1',
    'firm': 'COT',
    'decomp_ref': {
        'doc': 'org/missions/D4/POSN/POSN_ASTTAX/decompositions/POSN_ASTTAX_DECOMP_round6.md',
        'vintage_commit': '910815809f',
        'to_ref': TO_PATH,
    },
    'phase': 'BUILD-GENERAL',
    'spec_ref': {
        'doc': 'org/missions/D4/POSN/POSN_ASTTAX/prd/POSN_ASTTAX_PRD.md',
        'group': 'W',
        'vintage_commit': 'ab2ee8052a',
    },
    'assignee': '0.9.0_WK_POSN_ASTTAX~26',
    'artifacts_produced': [
        {
            'path_or_key': 'portal/src/pages/Positioning/panels/PositioningSummary.tsx',
            'kind': 'frontend_component',
            'commit_or_etag': PORTAL_PIN,
            'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
            'deploy_evidence': 'The frontend freeze bars the gitlink move, any promote and any push; this '
                               'commit sits on wk-posn-6-26-portal inside the portal submodule, cut from '
                               'refs/drains/posn-6-portal (dd1d33c6db) for the COO to drain. Verified at the '
                               'worktree root: git ls-tree HEAD -- portal still prints 160000 commit '
                               'e85f6eb84f3a1771a37011a7e77e372570bad02a and git diff --cached -- portal is empty.',
            'artifact_covered_by': ['W3-AC2', 'W3-AC3', 'W3-AC4', 'W3-AC5', 'W3-AC6', 'W3-AC7'],
        },
        {
            'path_or_key': 'portal/src/pages/Positioning/Positioning.tsx',
            'kind': 'frontend_component',
            'commit_or_etag': PORTAL_PIN,
            'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
            'deploy_evidence': 'Same commit and same freeze as the panel above; the three page strings that '
                               'described the removed blend (MODE_DESCRIPTIONS.satellites, the unresolved '
                               'notice, the models-unavailable copy) are read back rendered in W3-AC6.',
            'artifact_covered_by': ['W3-AC2', 'W3-AC6', 'W3-AC7'],
        },
        {
            'path_or_key': 'org/missions/D4/POSN/POSN_ASTTAX/ledger/PORTAL_REFS.md',
            'kind': 'doc',
            'commit_or_etag': LEDGER_PIN,
            'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
            'deploy_evidence': 'One appended row naming branch wk-posn-6-26-portal at '
                               '10a2799c67c519288fcd7d4ae6e3b86d5ed48b5a, cut from dd1d33c6db, drain ref '
                               'refs/drains/posn-6-portal. RE-PINNED after the commit that carried it '
                               '(Z-S105): this instance first went in as PENDING-THIS-COMMIT and the row now '
                               'names the workspace commit git log reports for it, '
                               '2191049ef15440df83a00ef131ea972fb8f0f7e2. A ledger append is a record, not a '
                               'deploy.',
            'artifact_covered_by': ['W3-AC7'],
        },
    ],
    'acceptance': [],
    'controls': {
        'mutant': {
            'description': 'TWO mutants, one per instrument that could otherwise only pass. (1) W3-AC4: a type '
                           'error injected into the file under change (const __W3_AC4_POSITIVE_CONTROL: number = '
                           'presentClassKeys([])) run through the criterion\'s own command. (2) W3-AC3: the unit '
                           'control\'s case (g) asserts a deliberately WRONG expectation, and the harness exits '
                           'non-zero unless that case prints FAIL.',
            'expected': 'the tsc command fails (non-zero) with a TS2322 on the injected line and passes again '
                        'after the revert; case (g) prints FAIL and the run still exits 0 because the falsifier '
                        'fired as designed',
            'observed': 'tsc: "src/pages/Positioning/panels/PositioningSummary.tsx(94,7): error TS2322: Type '
                        '\'AssetClassKey[]\' is not assignable to type \'number\'." INJECTED-RUN EXIT=2; after the '
                        'revert (md5 0b64b45312d56781ece5976974ef7ea7 before and after, control line absent) '
                        'EXIT=0. Unit control: "FAIL  g  DELIBERATELY WRONG EXPECTATION -- this line MUST read '
                        'FAIL" with "FALSIFIER  : case g printed FAIL as required".',
            'status': 'FIRED-AS-EXPECTED',
        },
        'determinism': {
            'method': 'The render evidence was produced TWICE end-to-end on the same fixtures and the same port '
                      '(5179): once with the two files at refs/drains/posn-6-portal and once on this branch, with '
                      'the files restored by md5 between the runs. The fixtures were also rebuilt from a second '
                      'download of the six served keys, and the builder re-verified every md5 against the '
                      'fetch-time manifest.',
            'observed': 'Both runs enumerated the same four states with the same book sets; the pre/post label '
                        'dumps are byte-identical for Models (11), Benchmark (9) and ETFs (8) and differ in '
                        'exactly 5 of 30 Satellites labels, all IEEE artifacts. The second fixture build printed '
                        'the same six VersionIds and the same six md5s, so the bytes under both runs are one set.',
            'status': 'STABLE',
        },
    },
    'declared_exclusions': [
        {'item': 'HoldingsTab.tsx, satelliteAdapter.ts and the other shared/ and tabs/ files',
         'reason': 'TO-W3-1 step 5: they belong to TO-W2-1 (F4) on a sibling branch; this order\'s <paths> '
                   'name only the two files changed here, and W3-AC2 measures that.'},
        {'item': 'The Portfolio Composition legend\'s five-class list and the Holdings panels\' footers in '
                 'Satellites mode',
         'reason': 'Both are HoldingsTab.tsx, outside the grant. Filed as POSN_ASTTAX-Z-W26-S3; the footers are '
                   'already the issuer\'s POSN_ASTTAX-Z-S136, carried into F4.'},
        {'item': 'The Satellites label clipped at the panel\'s right edge at 1440px',
         'reason': 'A layout change, not a label-format change; the order\'s act 2 is the format and its <paths> '
                   'carry no geometry. PRE-EXISTING at the ref. Filed as POSN_ASTTAX-Z-W26-S5.'},
        {'item': 'A gitlink move, a promote, a push, or any DEV/PROD deploy',
         'reason': 'The frontend freeze; the round\'s portal commits land on refs/drains/posn-6-portal and the '
                   'COO drains them. W3-AC7 measures the gitlink UNMOVED two ways.'},
        {'item': 'The `models-unavailable` notice KEY and the STATE COHERENCE comment above it '
                 '(Positioning.tsx), which still describe the models feed as the state\'s cause',
         'reason': 'Act 4 names the three COPY strings; renaming a notice state and its axis documentation is a '
                   'wider edit than the order authorises. The copy no longer mentions the blend.'},
    ],
    'surprises': SURPRISES,
    'session_log': 'org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~26/',
    'compiler_tools': [
        {'tool': 'tsc (bun run tsc -b)',
         'invocation': 'cd portal && bun run tsc -b   (and bun run tsc -b --force --listFiles for the count)',
         'result': 'exit 0; 2027 files checked, 481 under src/; an injected type error fails the same command (exit 2).'},
        {'tool': 'bun (TypeScript executed directly)',
         'invocation': 'cd portal && bun ../' + D + '/w3_presence_unit_control.ts',
         'result': 'exit 0; 6 of 6 real cases PASS over constructed column sets, the deliberately wrong case prints FAIL.'},
        {'tool': 'playwright-core via scripts/ui-smoke.mjs (system Edge, stubbed session)',
         'invocation': 'node scripts/ui-smoke.mjs positioning <out>.png --port 5179 --fixtures .scratch/w3_fixtures.json [--click ...]',
         'result': '5 captures, all rc 0, all READ; fixtures from the served bytes with every VersionId printed.'},
        {'tool': 'proof-of-spec-check.py',
         'invocation': 'python3 .tools/proof-of-spec-check.py ' + OUT + ' W3-AC1,W3-AC2,W3-AC3,W3-AC4,W3-AC5,W3-AC6,W3-AC7,W3-AC8',
         'result': 'see the run recorded beside this instance (w3_proof_check.txt).'},
    ],
}

for r in ROWS:
    inv, exp_text = CRIT[r['cid']]
    row = {
        'criterion_id': r['cid'],
        'criterion_verbatim': exp_text,
        'method': r['method'],
        'invocation': expand(inv),
        'output_evidence': r['ev'],
        'denominator': r['den'],
        'status': 'PASS',
    }
    if r.get('judgment'):
        row['judgment'] = True
        row['status'] = 'UNVERIFIABLE-BY-INSTRUMENT'
        row['status_reason'] = ('Judgment criterion: the task order marks it judgment="true" and grades it at L9. '
                                'The readings are recorded in output_evidence and NO verdict is offered; the '
                                'oracle is 3.0.0_SA_CVO~Z at L9.')
    if r.get('expect'):
        row['expect'] = r['expect']
    INST['acceptance'].append(row)

# ---- REFUSE BEFORE WRITING: every expect must match its own evidence, and every row must be ASCII.
bad = 0
for row in INST['acceptance']:
    exp = row.get('expect')
    if exp:
        if re.search(exp, row['output_evidence'], re.S | re.M):
            print('OK    %s: expect matches its output_evidence' % row['criterion_id'])
        else:
            print('BLOCKED %s: expect does NOT match its output_evidence' % row['criterion_id'])
            bad += 1
    else:
        print('OK    %s: no expect (judgment row, graded at L9)' % row['criterion_id'])
blob = json.dumps(INST, indent=2)
na = sorted({c for c in blob if ord(c) > 127})
if na:
    print('BLOCKED: non-ASCII in the instance: %r' % na)
    bad += 1
if bad:
    sys.exit(1)
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(blob + '\n')
print('WROTE %s (%d bytes, %d acceptance rows, %d surprises)'
      % (OUT, len(blob) + 1, len(INST['acceptance']), len(INST['surprises'])))
