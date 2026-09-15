#!/usr/bin/env python3
"""POSN_AGGFIX.TO-B2-1 (slot ~3) -- build the PROOF_OF_SPEC instance from the RECORDED outputs.

criterion_verbatim and invocation are read from the task order's own <criterion> elements (placeholders expanded to
this folder's files), never retyped. output_evidence is the recorded run file, verbatim. Every mechanical row's `expect`
must match its recorded output or this builder refuses to write the instance.

Usage (from the workspace root): python <this>
"""
import json
import os
import re
import subprocess

D = 'org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~3'
TO = 'org/missions/D4/POSN/POSN_AGGFIX/task-orders/POSN_AGGFIX.TO-B2-1.holdings-tab-restores-the-aggregate-book.md'
OUT = D + '/POSN_AGGFIX.TO-B2-1.holdings-tab-restores-the-aggregate-book.proof_of_spec.json'
PORTAL_COMMIT = subprocess.run(['git', '-C', 'portal', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
PLACE = {
    'PRIOR_LAYOUT_MAP_B2': D + '/b2_ac1_prior_layout_map.py',
    'AGG_DOM_B2': D + '/b2_agg_dom.mjs',
    'FIVE_BOOKS_DOM_B': D + '/b_five_books_dom.mjs',
    'TYPECHECK_RUN_B': D + '/b_typecheck_run.sh',
}
IDS = ['B2-AC%d' % i for i in range(1, 12)]


def rd(name):
    return open(os.path.join(D, name), encoding='utf-8').read()


to_txt = open(TO, encoding='utf-8').read()
crit = {}
for m in re.finditer(r'<criterion id="(B2-AC\d+)"[^>]*?(?:/>(.*?)\n|><invocation>(.*?)</invocation><expect>(.*?)</expect></criterion>)', to_txt, re.S):
    cid = m.group(1)
    if m.group(3) is not None:
        inv = m.group(3)
        for k, v in PLACE.items():
            inv = inv.replace('<' + k + '>', v)
        crit[cid] = {'invocation': inv, 'verbatim': m.group(4).strip()}
    else:
        crit[cid] = {'invocation': 'JUDGMENT -- no invocation; graded at L9', 'verbatim': m.group(2).strip()}
assert sorted(crit) == sorted(IDS), sorted(crit)

ac1 = rd('b2_ac1_prior_layout_map.txt')
m_den = re.search(r'DENOMINATOR: d53049a0 removed (\d+) lines', ac1)
m_sum = re.search(r'SUM: .* = (\d+) of (\d+)', ac1)
m_add = re.search(r'the (\d+) added lines of `git diff', ac1)
m_ctl = re.search(r'CONTROL -- the same counter over the (\d+) lines.*?TOTAL (\d+) \(must be', ac1, re.S)
m_res = re.search(r'RESTORED (\d+) of (\d+)', ac1)
ac1_den = ('%s of %s removed lines assigned (restored elements %s of %s, 5 dead elements, 4 named non-aggregate classes, 0 '
           'unassigned); 4 forbidden classes counted over %s added lines = 0, the same counter over %s removed group lines = %s; '
           'the group FIRST in 4 of 4 regions.' % (m_sum.group(1), m_den.group(1), m_res.group(1), m_res.group(2), m_add.group(1),
                                                    m_ctl.group(1), m_ctl.group(2)))

ac10 = (
    "JUDGMENT -- READINGS ONLY, NO VERDICT (graded by 3.0.0_SA_CVO~Z at L9). Read from the screenshots in this folder at portal "
    + PORTAL_COMMIT[:10] + " beside the removal diff `git -C portal show d53049a0 -- src/pages/Positioning/tabs/HoldingsTab.tsx` "
    "(old = d53049a0^).\n\n"
    "READING 1 -- THE SELECTOR ENTRY. Before the removal the book selector was a strip of filled chips, each labelled with the "
    "book's CODE (old :1029-1043, `{portfolio.id}`), so the aggregate read 'AGG', first, in opalIndigo. At HEAD the selector is "
    "today's segmented idiom (DSGN_REBRND RB-s-5, weight and a 2px rule for the active book, no fill) and the entry reads "
    "'Aggregate' (the wording B2-AC2 names), first, in the same opalIndigo #5e72e4, followed by UST ST INT LT ULT in their locked "
    "ladder colours (b2_ac2_opal_staff_lands_on_aggregate.png, the Portfolio Composition header strip: 'AGGREGATE' underlined, "
    "then the five codes). The five chips' colours are unchanged because the aggregate is kept out of their ramp. What differs "
    "from before: the label is the name rather than the code, and the chip style is today's, not the removed filled chip.\n\n"
    "READING 2 -- THE MODEL BREAKDOWN GROUP. Before: a group header 'MODEL BREAKDOWN' in text-orange-300 semibold over an "
    "orange-500/10 tint (old :1225-1226), five 45px columns placed first after Weight (old :1169-1177, :1273-1291), body cells "
    "in a white monospace over bg-orange-500/5 (old :1452-1476). At HEAD: the same five columns, the same 45px widths, the same "
    "position (first after Weight in the colgroup, both header rows and the body, b2_ac1) and the same header tint recipe; the "
    "header text is now the band's ink #e6eaf4 in bold rather than orange, the figures are Lato tabular numerals rather than "
    "monospace, and the body tint is a 5% orange laid over the opaque panel base. In b2_ac2 and b2_ac6 the group reads as a "
    "slightly warmer strip between WEIGHT and the green-tinted ETF CHARACTERISTICS group; its figures are brighter than the "
    "neighbouring green header labels (measured 10.99-12.46:1 against the reference Yield header's 9.02-10.71:1). The orange "
    "identity now rests on the tint alone.\n\n"
    "READING 3 -- THE 'ALL OF OPAL' LABEL. It is in ONE place: the group header, which reads 'MODEL BREAKDOWN - ALL OF OPAL' "
    "on one line in the screenshots. It appears only while Aggregate is selected and only in the Characteristics view -- the "
    "Performance view renders no Model Breakdown group and so no label, and the selector entry and the Portfolio Composition "
    "panel say 'Aggregate' with nothing naming Opal. The page header above reads 'Asset allocation and holdings breakdown "
    "across model portfolios.' Advisors and clients never see the entry or the label (b2_ac4_*.png).\n\n"
    "READING 4 -- WHAT WAS NOT CARRIED, VISIBLY. The removed ETF CHARACTERISTICS header toggled its top-right corner class "
    "when AGG was selected (old :1229); HEAD keeps that neighbour's class as it is (b2_ac1 N4). The removed grand-total "
    "filler cells carried their own white/10 fill on top of the row's; the restored fillers carry none, so the row's own fill "
    "shows through them, one layer lighter than the ETF fillers beside them.\n\n"
    "No verdict is offered."
)

rows = [
    ('B2-AC1', 'command', ac1, ac1_den,
     r"HEAD 3ec1f83cab.*UNASSIGNED removed lines: 0\n.*RESTORED 12 of 12 .*text-white\s+0\n\s+text-orange-300\s+0\n\s+bg-white/10\s+0\n\s+bg-orange-500/5\s+0\n.*TOTAL 0\n.*TOTAL [1-9]\d* \(must be > 0.*-> MET\nEXIT=0"),
    ('B2-AC2', 'command', rd('b2_ac2_opal_staff_fresh.txt'),
     "1 page load as Opal staff with no remembered book: 6 selector entries; 30 of 30 composition data nodes (28 drawn, 28 "
     "labelled -- two nodes too small to draw) and 30 of 30 breakdown holding rows against the fixture's 30 AGG holdings; 5 of 5 "
     "columns in order after Weight; 3 of 3 sampled tickers equal; 1 screenshot.",
     r"HEAD 3ec1f83cab.*SELECTOR FIRST ENTRY: \"Aggregate\"\nSELECTED BOOK LABEL \(the landing\): \"Aggregate\".*COMPOSITION: data nodes=30 .*\(fixture AGG holdings=30\)\nBREAKDOWN: holding rows=30 .*COLUMN GROUP AFTER BASIC INFO: \"Model Breakdown - All of Opal\"\nCOLUMNS AFTER Weight: \[\"UST\",\"ST\",\"INT\",\"LT\",\"ULT\"\]\n\"All of Opal\" label in the table header: true.*SAMPLES EQUAL: 3 of 3.*SCREENSHOT: .*b2_ac2_opal_staff_lands_on_aggregate\.png.*VERDICT INPUTS MET: true"),
    ('B2-AC3', 'command', rd('b2_ac3_remembered_st.txt'),
     "1 page load as Opal staff with ST remembered, then 1 selection of Aggregate: 30 of 30 composition data nodes and 30 of 30 "
     "breakdown holding rows against the fixture's 30; 2 screenshots.",
     r"HEAD 3ec1f83cab.*SELECTED BOOK LABEL \(the landing\): \"ST\".*AFTER SELECTING Aggregate: selected=\"Aggregate\" composition data nodes=30 .*breakdown holding rows=30  \(fixture AGG holdings=30\).*VERDICT INPUTS MET: true"),
    ('B2-AC4', 'command', rd('b2_ac4_advisor_client_remembered_agg.txt'),
     "2 of 2 viewers (advisor, client), each with 'AGG' seeded before load: 5 selector entries each and 0 Aggregate; landing INT "
     "each; 0 of 146 requests to opal_aggregate.json each; no Model Breakdown group in either DOM.",
     r"HEAD 3ec1f83cab.*ADVISOR: .*Aggregate entry present: false\n\s+SELECTED BOOK LABEL \(the landing\): \"INT\"  ordinary default model: INT\n\s+REQUESTS TO opal_aggregate\.json: 0 .*MODEL BREAKDOWN GROUP IN THE DOM: false.*CLIENT: .*Aggregate entry present: false\n\s+SELECTED BOOK LABEL \(the landing\): \"INT\"  ordinary default model: INT\n\s+REQUESTS TO opal_aggregate\.json: 0 .*MODEL BREAKDOWN GROUP IN THE DOM: false.*EXIT=0"),
    ('B2-AC5', 'command', rd('b2_ac5_compare_before.txt'),
     "10 of 10 advisor and client captures compared against B_DOM_BEFORE.json (edf85ce503) and identical; 1 of 1 mutated-weight "
     "control reported DIFFERENT; the same fixture bytes as the BEFORE run.",
     r"HEAD 3ec1f83cabb1780d4468c4f80fd16453df800f00.*SAME FIXTURES AS THE BEFORE RUN: true.*IDENTICAL 10 of 10\n.*CONTROL advisor/UST with the mutated weight: DIFFERENT.*EXIT=0"),
    ('B2-AC6', 'command', rd('b2_ac6_legibility.txt'),
     "10 of 10 Model Breakdown cells (5 header, 5 body) measured on the nearest opaque ancestor and on the composited ground, "
     "every ratio at least 10.99; 2 reference cells (the Yield column) printed beside them.",
     r"HEAD 3ec1f83cab.*SELECTED BOOK LABEL: \"Aggregate\".*header UST .*body ULT .*REFERENCE header Yield .*REFERENCE body Yield .*MODEL BREAKDOWN CELLS MEASURED: 10 of 10; minimum ratio \(either ground\) (\d+\.?\d*); cells at or above 4\.5 on both grounds: 10 of 10.*VERDICT INPUTS MET: true"),
    ('B2-AC7', 'command', rd('b2_ac7_unavailable.txt'),
     "1 page load as Opal staff with the UNAVAILABLE payload served (1 request): 5 selector entries and 0 Aggregate; landing INT; "
     "no Model Breakdown group; 0 page errors.",
     r"HEAD 3ec1f83cab.*status UNAVAILABLE.*Aggregate entry present: false\nSELECTED BOOK LABEL \(the landing\): \"INT\"  ordinary default model: INT.*MODEL BREAKDOWN GROUP IN THE DOM: false.*PAGE ERRORS: 0\n.*VERDICT INPUTS MET: true"),
    ('B2-AC8', 'command', rd('b2_ac8_typecheck.txt'),
     "2 of 2 runs: the portal worktree at HEAD (error_TS_line_count 0) and a scratch copy of HEAD with one injected error "
     "(error_TS_line_count 1, on the injected line). The recorded file is the SECOND run of this invocation: the first "
     "(b2_ac8_typecheck.attempt1.txt, identical values) was refused by the checker's count-bar limb on the runner's old "
     "wording 'EXIT=2  error', which reads as a count; the runner now prints key=value fields (row POSN_AGGFIX-Z-W3-S4).",
     r"HEAD 3ec1f83cabb1780d4468c4f80fd16453df800f00.*TYPECHECK COMMAND \(package\.json scripts\.typecheck at HEAD\): tsc -b --noEmit.*RUN 1: exit_code=0; error_TS_line_count=0\n.*bookSet\.ts\(762,14\): error TS2322.*RUN 2: exit_code=2; error_TS_line_count=1; on_injected_line=1\n.*\nEXIT=0\nSHELL-EXIT=0"),
    ('B2-AC9', 'diff', rd('b2_ac9_diff_stat.txt'),
     "5 files changed under src between edf85ce503 and HEAD 3ec1f83cab: the 4 named (portal-proxy.ts, Positioning.tsx, "
     "bookSet.ts, HoldingsTab.tsx) and the permitted fifth, src/pages/Positioning/README.md; no other file.",
     r"portal HEAD 3ec1f83cab.*\n src/api/portal-proxy\.ts\s+\|.*\n src/pages/Positioning/Positioning\.tsx\s+\|.*\n src/pages/Positioning/README\.md\s+\|.*\n src/pages/Positioning/shared/bookSet\.ts\s+\|.*\n src/pages/Positioning/tabs/HoldingsTab\.tsx\s+\|.*\n 5 files changed"),
    ('B2-AC11', 'command', rd('b2_ac11_network_arms.txt'),
     "6 of 6 arms (opal-staff, advisor, client x Models, ETFs), each on /positioning with the family pressed as named; 146-147 "
     "requests per arm, every URL recorded in network_arms_requests_3ec1f83cab.json.",
     r"HEAD 3ec1f83cab.*Models\s+opal-staff\s+1\s+\(.*Models\s+advisor\s+0\s+\(.*Models\s+client\s+0\s+\(.*ETFs\s+opal-staff\s+0\s+\(.*ETFs\s+advisor\s+0\s+\(.*ETFs\s+client\s+0\s+\(.*staff exactly 1, advisor 0, client 0; ETFs: 0, 0, 0\): MET"),
]

acceptance = []
for cid, method, ev, den, exp in rows:
    if not re.search(exp, ev, re.S | re.M):
        raise SystemExit('BLOCKED: the expect for ' + cid + ' does not match its recorded output')
    acceptance.append({
        'criterion_id': cid, 'criterion_verbatim': crit[cid]['verbatim'], 'method': method,
        'invocation': crit[cid]['invocation'], 'output_evidence': ev, 'denominator': den, 'status': 'PASS', 'expect': exp,
    })
acceptance.append({
    'criterion_id': 'B2-AC10', 'criterion_verbatim': crit['B2-AC10']['verbatim'], 'method': 'manual_read_with_citation',
    'invocation': crit['B2-AC10']['invocation'], 'output_evidence': ac10,
    'denominator': '4 readings recorded (the selector entry; the Model Breakdown group; the All of Opal label; what was visibly not carried), 0 verdicts offered.',
    'status': 'UNVERIFIABLE-BY-INSTRUMENT', 'judgment': True,
    'status_reason': 'Judgment criterion: the task order marks it judgment="true" and grades it at L9. The readings are recorded in output_evidence and NO verdict is offered; the oracle is 3.0.0_SA_CVO~Z at L9.',
})
order = {c: i for i, c in enumerate(IDS)}
acceptance.sort(key=lambda r: order[r['criterion_id']])

portal_ev = ('LOCAL commit ' + PORTAL_COMMIT + ' on wk-aggfix-1-3-portal in the portal repo, parent 63edeeeb51 (TO-B1-1, cut from '
             'edf85ce503 origin/PROD). No gitlink move, no push, no promote (C-PORTAL-PROMOTE); the drain is 2.0.0_SA_COO~Z\'s. The '
             'portal repo is a separate object store, so this workspace checker announces the pin rather than resolving it. '
             'PORTAL_REFS.md carries the appended line "wk-aggfix-1-3-portal | 3ec1f83cab | 63edeeeb51", committed with this instance.')
arts = [
    {'path_or_key': 'portal/src/pages/Positioning/tabs/HoldingsTab.tsx', 'kind': 'frontend_component', 'commit_or_etag': PORTAL_COMMIT,
     'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE', 'deploy_evidence': portal_ev,
     'artifact_covered_by': ['B2-AC1', 'B2-AC2', 'B2-AC3', 'B2-AC4', 'B2-AC5', 'B2-AC6', 'B2-AC7', 'B2-AC8', 'B2-AC9', 'B2-AC10']},
    {'path_or_key': 'portal/src/pages/Positioning/Positioning.tsx', 'kind': 'frontend_component', 'commit_or_etag': PORTAL_COMMIT,
     'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE', 'deploy_evidence': portal_ev + ' This order\'s change to it: the two HoldingsTab mount props only.',
     'artifact_covered_by': ['B2-AC2', 'B2-AC8', 'B2-AC9', 'B2-AC11']},
]
for name, kind, cov, why in [
    ('b2_agg_dom.mjs', 'test', ['B2-AC2', 'B2-AC3', 'B2-AC4', 'B2-AC6', 'B2-AC7'], '<AGG_DOM_B2>.'),
    ('b2_ac1_prior_layout_map.py', 'script', ['B2-AC1'], '<PRIOR_LAYOUT_MAP_B2>.'),
    ('b2_ac2_opal_staff_lands_on_aggregate.png', 'doc', ['B2-AC2', 'B2-AC10'], 'Screenshot, Opal staff fresh load at HEAD.'),
    ('b2_ac3_opal_staff_remembered_st.png', 'doc', ['B2-AC3'], 'Screenshot, Opal staff with ST remembered.'),
    ('b2_ac3_opal_staff_then_aggregate.png', 'doc', ['B2-AC3', 'B2-AC10'], 'Screenshot, after selecting Aggregate.'),
    ('b2_ac4_advisor_remembered_agg.png', 'doc', ['B2-AC4', 'B2-AC10'], 'Screenshot, advisor with AGG seeded.'),
    ('b2_ac4_client_remembered_agg.png', 'doc', ['B2-AC4'], 'Screenshot, client with AGG seeded.'),
    ('b2_ac6_legibility.png', 'doc', ['B2-AC6', 'B2-AC10'], 'Screenshot, the legibility measurement page.'),
    ('b2_ac7_opal_staff_unavailable.png', 'doc', ['B2-AC7'], 'Screenshot, the UNAVAILABLE payload.'),
]:
    arts.append({'path_or_key': D + '/' + name, 'kind': kind, 'commit_or_etag': 'PENDING-THIS-COMMIT',
                 'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
                 'deploy_evidence': 'Workspace deliverable, rides the commit that carries this proof. ' + why,
                 'artifact_covered_by': cov})
# b_fixtures.mjs and b_five_books_dom.mjs are TRACKED (TO-B1-1) and modified by this order, so they are NOT pending rows
# (the CCX class); their changes are stated in compiler_tools and ride the same commit.

inst = {
    'schema_version': '1.0',
    'to_id': 'POSN_AGGFIX.TO-B2-1',
    'decomp_ref': {'doc': 'org/missions/D4/POSN/POSN_AGGFIX/decompositions/POSN_AGGFIX_DECOMP.md', 'vintage_commit': '605c03f81f', 'to_ref': TO},
    'phase': 'BUILD-GENERAL',
    'spec_ref': {'doc': 'org/missions/D4/POSN/POSN_AGGFIX/prd/POSN_AGGFIX_PRD.md', 'group': 'B', 'vintage_commit': 'cbd85e5cff'},
    'assignee': '0.9.0_WK_POSN_AGGFIX~3',
    'artifacts_produced': arts,
    'acceptance': acceptance,
    'controls': {
        'mutant': {
            'description': 'FOUR controls, one per instrument that could otherwise only pass. (1) B2-AC8: a scratch copy of portal HEAD with one injected type error, run through the same command read from package.json. (2) B2-AC5: one fixture weight mutated and one advisor capture compared against B_DOM_BEFORE.json the same way. (3) B2-AC1: the forbidden-class counter run over the lines d53049a0 removed from the Model Breakdown group. (4) B2-AC4 / B2-AC7: the negative arms of the render harness -- AGG seeded for an advisor and a client, and the UNAVAILABLE payload for Opal staff -- each on the same harness that reads the aggregate as present for B2-AC2.',
            'expected': 'the copy exits non-zero on the injected line; the mutated capture reads DIFFERENT; the counter finds the classes (> 0); no Aggregate entry and no group in the negative arms',
            'observed': "(1) 'bookSet.ts(762,14): error TS2322' and 'RUN 2: exit_code=2; error_TS_line_count=1; on_injected_line=1'. (2) 'CONTROL advisor/UST with the mutated weight: DIFFERENT -- .composition.tile_count: BEFORE=13  NOW=14'. (3) control TOTAL " + m_ctl.group(2) + " over " + m_ctl.group(1) + " removed lines. (4) 'Aggregate entry present: false' in 3 of 3 negative loads, 'MODEL BREAKDOWN GROUP IN THE DOM: false' in 3 of 3.",
            'status': 'FIRED-AS-EXPECTED',
        },
        'determinism': {
            'method': 'Every render read settles only on three consecutive identical DOM reads after a 4 s window for the aggregate request. Each B2 arm ran twice on the same fixture bytes (md5 d35f3c4a1844980817f6ee556dad9bc7; the UNAVAILABLE build acad8f850c3fa99e27eecb73973d886c): once on the uncommitted tree during authoring and once at the commit for this record.',
            'observed': 'the two runs agree: selector entries, landing labels, 30/30 counts, 3 of 3 samples, and the ten contrast ratios (12.46 / 10.99 / 11.74) identical; the network table identical to TO-B1-1\'s B1-AC5 except the staff selector now leads with Aggregate.',
            'status': 'STABLE',
        },
    },
    'declared_exclusions': [
        {'item': 'live served bytes: opal_aggregate.json and the shared file after the producer change', 'reason': 'Every render ran on fixtures pinned by VersionId (b_fixtures.mjs MANIFEST). TO-B3-1 (AF1-s-16) renders this HEAD on live bytes.'},
        {'item': 'the portal drain, DEV/PROD promote and any push', 'reason': 'COMMIT YES, PROMOTE NO (the order header; C-PORTAL-PROMOTE). The drain ref is 2.0.0_SA_COO~Z\'s.'},
        {'item': 'the ETF CHARACTERISTICS header corner class toggle the removal diff carried (old :1229)', 'reason': 'A class on the neighbouring group, not part of the Model Breakdown group; stated as N4 in b2_ac1 and in B2-AC10 reading 4.'},
        {'item': 'the contrast of the selector entry itself (opalIndigo #5e72e4 on the panel header strip)', 'reason': 'B2-AC6 names the Model Breakdown header and body cells; the selector entry is the removed shape restored as-is and was not measured.'},
        {'item': 'the Performance view', 'reason': 'The removed group rendered only in the Characteristics view (old :1165-1177 inside `viewMode === \'characteristics\'`); restored the same way, no criterion reads the Performance view.'},
        {'item': 'a real client session\'s claims', 'reason': 'AuthContext has no client class; the constructed client claim set of row POSN_AGGFIX-Z-W3-S2 (TO-B1-1) is reused and printed.'},
    ],
    'surprises': [
        "POSN_AGGFIX-Z-W3-S3: the order's canvas premise ('ink on white panels') does not hold for the Holdings tab -- both panels are Panel variant=\"chart\", the dark band; the group was authored in the band's ink token with the four named classes kept out, and legibility left to B2-AC6.",
        "POSN_AGGFIX-Z-W3-S4: proof-of-spec-check's count-bar limb refused the first B2-AC8 row on the shared runner's wording 'EXIT=2  error' (an exit code read as an error count), while TO-B1-1's B1-AC7 passed the same wording spelled [ ]{2}; the runner now prints key=value fields and B2-AC8 was re-run once, the refused record kept as attempt1.",
    ],
    'session_log': D + '/',
    'compiler_tools': [
        {'tool': 'tsc 5.9.3 (the portal typecheck, tsc -b --noEmit, read from package.json)', 'invocation': 'timeout 900 bash ' + PLACE['TYPECHECK_RUN_B'],
         'result': 'HEAD exit 0 with 0 error lines; the injected scratch copy exit 2 on the injected line.'},
        {'tool': 'playwright-core + system Edge, vite started from this worktree (b2_agg_dom.mjs, b_five_books_dom.mjs)',
         'invocation': 'timeout 900 node ' + PLACE['AGG_DOM_B2'] + ' <arm> | timeout 900 node ' + PLACE['FIVE_BOOKS_DOM_B'] + ' --compare-before | --network-arms',
         'result': 'every arm EXIT=0 at HEAD. During authoring the legibility arm threw once on the uncommitted tree (its colour parser read only rgb(); Tailwind v4 serializes oklch) -- the parser now resolves any CSS colour through a 1x1 canvas; the recorded run is at HEAD. b_five_books_dom.mjs (TO-B1-1\'s) was changed in two places for B2-AC11: its bar is now staff EXACTLY 1, and at any HEAD but 63edeeeb51 it writes network_arms_requests_<HEAD10>.json so TO-B1-1\'s record is not overwritten. b_fixtures.mjs gained opts.aggregate = \'unavailable\' (contract 1.1 shape); its default build is byte-identical (same md5 as TO-B1-1).'},
        {'tool': 'b2_ac1_prior_layout_map.py', 'invocation': 'timeout 120 python ' + PLACE['PRIOR_LAYOUT_MAP_B2'],
         'result': 'The FIRST recorded run (b2_ac1_prior_layout_map.attempt1.txt, EXIT=1, NOT MET) was an instrument defect: E7 anchored on the colgroup\'s line, so 3 removed lines stayed unassigned. Fixed (E7 on a <th colSpan={5}> line, N4 named, an overlap guard added) and re-run once; the recorded file is the re-run. Stated imprecision in the re-run, verdict unaffected: E7\'s PRINTED span reads old :1217-1228 because the BASIC INFO header\'s own <th colSpan={5}> (old :1218) matched first; the only removed lines inside that span are :1224-1228, the header cell itself, so every assignment, the 294 of 294 sum and RESTORED 12 of 12 stand as printed.'},
        {'tool': 'proof-of-spec-check.py (this worktree\'s copy)', 'invocation': 'python .tools/proof-of-spec-check.py ' + OUT + ' ' + ','.join(IDS),
         'result': 'see b2_proof_check.txt beside this instance.'},
    ],
}
s = json.dumps(inst, indent=1, ensure_ascii=True)
open(OUT, 'wb').write((s + '\n').encode('ascii'))
print('WROTE ' + OUT + ' bytes=' + str(len(s) + 1) + ' acceptance rows=' + str(len(acceptance)))
print('AC1 denominator: ' + ac1_den)
