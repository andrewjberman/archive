#!/usr/bin/env python3
"""POSN_AGGFIX.TO-B1-1 (slot ~3) -- build the PROOF_OF_SPEC instance from the RECORDED outputs.

criterion_verbatim and invocation are read from the task order's own <criterion> elements (placeholders expanded
to this folder's files), never retyped. output_evidence is the recorded run file, verbatim; where a line is
computed here (hunk summaries) it is labelled as computed by this builder.

Usage (from the workspace root): python <this>
"""
import json
import os
import re
import subprocess

D = 'org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~3'
TO = 'org/missions/D4/POSN/POSN_AGGFIX/task-orders/POSN_AGGFIX.TO-B1-1.portal-fetch-viewer-gate-and-remembered-choice.md'
OUT = D + '/POSN_AGGFIX.TO-B1-1.portal-fetch-viewer-gate-and-remembered-choice.proof_of_spec.json'
PORTAL_COMMIT = subprocess.run(['git', '-C', 'portal', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
PLACE = {
    'PREDICATE_READ_B1': D + '/b1_ac1_predicate_read.py',
    'FIVE_BOOKS_DOM_B': D + '/b_five_books_dom.mjs',
    'UNIT_RUN_B1': D + '/b1_unit_run.sh',
    'TYPECHECK_RUN_B': D + '/b_typecheck_run.sh',
}


def rd(name):
    return open(os.path.join(D, name), encoding='utf-8').read()


to_txt = open(TO, encoding='utf-8').read()
crit = {}
for m in re.finditer(r'<criterion id="(B1-AC\d)"[^>]*?(?:/>(.*?)\n|><invocation>(.*?)</invocation><expect>(.*?)</expect></criterion>)', to_txt, re.S):
    cid = m.group(1)
    if m.group(3) is not None:
        inv = m.group(3)
        for k, v in PLACE.items():
            inv = inv.replace('<' + k + '>', v)
        crit[cid] = {'invocation': inv, 'verbatim': m.group(4).strip()}
    else:
        crit[cid] = {'invocation': 'JUDGMENT -- no invocation; graded at L9', 'verbatim': m.group(2).strip()}
assert sorted(crit) == ['B1-AC%d' % i for i in range(1, 10)], sorted(crit)


def hunks(diff_text):
    """(header, old_start, removed_old_lines, added_new_lines) per hunk."""
    out = []
    cur = None
    for ln in diff_text.split('\n'):
        mh = re.match(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@(.*)$', ln)
        if mh:
            cur = {'header': ln, 'o': int(mh.group(1)), 'n': int(mh.group(2)), 'rem': [], 'add': []}
            out.append(cur)
            continue
        if cur is None or ln.startswith('---') or ln.startswith('+++'):
            continue
        if ln.startswith('-'):
            cur['rem'].append(cur['o'])
            cur['o'] += 1
        elif ln.startswith('+'):
            cur['add'].append(cur['n'])
            cur['n'] += 1
        elif ln.startswith(' '):
            cur['o'] += 1
            cur['n'] += 1
    return out


def span(src, opener, closer_re):
    lines = src.split('\n')
    for i, ln in enumerate(lines):
        if ln.startswith(opener):
            for j in range(i, len(lines)):
                if re.match(closer_re, lines[j]):
                    return (i + 1, j + 1)
    return None


def show(ref, path):
    return subprocess.run(['git', '-C', 'portal', 'show', ref + ':' + path], capture_output=True).stdout.decode('utf-8')


# ---- B1-AC3: the portal-proxy diff, with a computed hunk summary --------------------------------------------
ac3 = rd('b1_ac3_diff_portal_proxy.txt')
h3 = hunks(ac3)
base_proxy = show('edf85ce503', 'src/api/portal-proxy.ts')
gpd = span(base_proxy, 'export async function getPositioningData(', r'^\}')
inside = sum(1 for h in h3 for x in h['rem'] if gpd[0] <= x <= gpd[1])
ac3_summary = ('\nSUMMARY (computed by b1_build_proof.py from the diff above): hunks=%d; lines added=%d; lines removed=%d; '
               'getPositioningData spans base :%d-%d and the diff removes %d line(s) there; the one hunk sits after '
               'getEtfPositioningData (base :1376-1378).' % (len(h3), sum(len(h['add']) for h in h3),
                                                               sum(len(h['rem']) for h in h3), gpd[0], gpd[1], inside))

# ---- B1-AC6: the bookSet diff, with capabilitiesFor / BookSetCapabilities checked line by line ----------------
ac6 = rd('b1_ac6_diff_bookset.txt')
h6 = hunks(ac6)
base_bs = show('edf85ce503', 'src/pages/Positioning/shared/bookSet.ts')
head_bs = show(PORTAL_COMMIT, 'src/pages/Positioning/shared/bookSet.ts')
b_iface, h_iface = span(base_bs, 'export interface BookSetCapabilities {', r'^\}'), span(head_bs, 'export interface BookSetCapabilities {', r'^\}')
b_caps, h_caps = span(base_bs, 'export const capabilitiesFor = ', r'^  MODE_CAPABILITIES\[mode\]'), span(head_bs, 'export const capabilitiesFor = ', r'^  MODE_CAPABILITIES\[mode\]')
b_mc, h_mc = span(base_bs, 'export const MODE_CAPABILITIES', r'^\}'), span(head_bs, 'export const MODE_CAPABILITIES', r'^\}')


def touched(rng_old, rng_new):
    rem = sum(1 for h in h6 for x in h['rem'] if rng_old[0] <= x <= rng_old[1])
    add = sum(1 for h in h6 for x in h['add'] if rng_new[0] <= x <= rng_new[1])
    return rem, add


t_iface, t_caps, t_mc = touched(b_iface, h_iface), touched(b_caps, h_caps), touched(b_mc, h_mc)
ac6_summary = ('\nSUMMARY (computed by b1_build_proof.py from the diff above): hunks=%d -> %s\n'
               '  BookSetCapabilities  base :%d-%d / HEAD :%d-%d  removed %d, added %d\n'
               '  capabilitiesFor      base :%d-%d / HEAD :%d-%d  removed %d, added %d\n'
               '  MODE_CAPABILITIES    base :%d-%d / HEAD :%d-%d  removed %d, added %d' % (
                   len(h6), json.dumps([h['header'] for h in h6]),
                   b_iface[0], b_iface[1], h_iface[0], h_iface[1], t_iface[0], t_iface[1],
                   b_caps[0], b_caps[1], h_caps[0], h_caps[1], t_caps[0], t_caps[1],
                   b_mc[0], b_mc[1], h_mc[0], h_mc[1], t_mc[0], t_mc[1]))

ac9 = (
    "JUDGMENT -- READINGS ONLY, NO VERDICT (graded by 3.0.0_SA_CVO~Z at L9). Read at portal " + PORTAL_COMMIT[:10] +
    " (Positioning.tsx unless named).\n\n"
    "READING 1 -- NO PARTNER FIRM SELECTION REACHES MODELS MODE. `selectedFirmId` (:294-296, defaulting to "
    "satelliteSelectableFirms()[0] ?? COTTONWOOD_FIRM_ID) is read in exactly one place, `const satelliteFirm = internal ? "
    "selectedFirmId : undefined` (:301), which keys and parameterises the satellites REGISTRY query only (:440-441). The "
    "firm selector itself is commented out (TO-10-DE AC5, :568-575). An internal viewer in Models mode has no partner firm "
    "selected in any live sense: nothing on the page takes a firm there, and the Models payload is not firm-scoped.\n\n"
    "READING 2 -- THE AGGREGATE CARRIES NO FIRM AND IS MODELS-ONLY. Its query key is ['opal-aggregate'] (:371), with no "
    "firm in it; it is enabled only by `aggregateWanted = internal && mode === 'models'` (:369, :373), and the merge hands "
    "over a null payload outside that gate (:384). In Satellites mode -- the one mode where a firm (Cottonwood by default) "
    "is in play -- the aggregate is neither fetched nor merged, and the satellites adapter is handed the UNMERGED "
    "`positioningData` (:466). No path at this commit puts current_holdings.AGG beside a satellite firm's books.\n\n"
    "READING 3 -- WHAT RENDERS THE MERGED OBJECT AT THIS COMMIT. It reaches only `dataByMode.models` (:471) and so "
    "PositioningSummary, which reads current_holdings only where SUBCATEGORY_SOURCE is 'current_holdings' (bookSet.ts "
    ":144-148, models = 'attribution'; PositioningSummary.tsx :555, :572). The Holdings tab renders its own "
    "getPositioningData fetch (HoldingsTab.tsx :649, :653, :729), so at this commit no panel shows the aggregate to any "
    "viewer (row POSN_AGGFIX-Z-W3-S1); the viewer-facing entry is TO-B2-1's.\n\n"
    "READING 4 -- WHAT A VIEWER HAS TO GO ON. In Models mode the page header names the family ('Asset allocation and "
    "holdings breakdown across model portfolios.', MODE_DESCRIPTIONS.models) and never a firm; the only on-screen firm "
    "carrier on this page is the satellites selector, which is commented out. The label that would tell an Opal user the "
    "book is all of Opal is TO-B2-1's (the 'All of Opal' label, AF1-s-14) and is not present at this commit.\n\n"
    "No verdict is offered."
)

P = PLACE
rows = [
    ('B1-AC1', 'command', rd('b1_ac1_predicate_read.txt') if os.path.exists(os.path.join(D, 'b1_ac1_predicate_read.txt')) else None,
     "25 of 850 AuthContext.tsx lines name firmId or userType, all enumerated; 3 of 3 parseClaims call sites with their "
     "payload source; 2 of 2 predicate bodies; 1 page predicate line (Positioning.tsx :267 of 652); 1 class admitted "
     "beyond Opal staff.",
     r"PAGE PREDICATE: firmId === 'opal-capital' OR userType === 'Dev'.*ADMITTED BEYOND OPAL STAFF: a viewer whose server-issued userType is 'Dev' at ANY firmId"),
    ('B1-AC2', 'command', rd('b1_ac2_capture_before.txt'),
     "10 of 10 captures (advisor and client x UST ST INT LT ULT), each on /positioning with its book selected; composition "
     "tiles 13-19 and breakdown holding rows 14-19 per book; 0 page errors in both viewers.",
     r"HEAD edf85ce503aad961b84b5ea3b2074eb84d416a16.*HEAD == BASE: true.*CLAIMS advisor.*CLAIMS client.*WROTE .*B_DOM_BEFORE\.json.*CAPTURED 10 of 10"),
    ('B1-AC3', 'diff', ac3 + ac3_summary,
     "1 hunk of 1 in src/api/portal-proxy.ts: %d lines added, %d removed; the hunk is outside getPositioningData (base :%d-%d)." % (
         sum(len(h['add']) for h in h3), sum(len(h['rem']) for h in h3), gpd[0], gpd[1]),
     r"@@ -1377,6 \+1377,65 @@ export async function getEtfPositioningData.*\+export async function getOpalAggregate\(\): Promise<OpalAggregateResponse> \{.*apiRequest<OpalAggregateResponse>\('/api/general/positioning/opal_aggregate\.json'\).*hunks=1; lines added=59; lines removed=0"),
    ('B1-AC4', 'test_suite', rd('b1_ac4_unit_control.txt'),
     "18 of 18 real cases PASS (4 merge, 6 book set, 6 remembered choice, 2 capabilities -- capabilitiesFor compared for 3 of 3 "
     "modes) and 1 of 1 negative control fired.",
     r"HEAD 63edeeeb51b9bec8988f86c12dc92b5768ca2532.*PASS  c1 .*CONTROL FIRED: with the check disabled the client lands on 'AGG'.*REAL CASES 18[ ]{3}PASS 18[ ]{3}FAIL 0[ ]{3}NEGATIVE CONTROL FIRED"),
    ('B1-AC5', 'command', rd('b1_ac5_network_arms.txt'),
     "6 of 6 arms (opal-staff, advisor, client x Models, ETFs), each on /positioning with the family pressed as named; 146-147 "
     "requests per arm, every URL recorded in b1_ac5_network_arms_requests.json.",
     r"Models\s+opal-staff\s+1\s+\(.*Models\s+advisor\s+0\s+\(.*Models\s+client\s+0\s+\(.*ETFs\s+opal-staff\s+0\s+\(.*ETFs\s+advisor\s+0\s+\(.*ETFs\s+client\s+0\s+\(.*0\): MET$"),
    ('B1-AC6', 'diff', ac6 + ac6_summary,
     "%d hunks of %d in src/pages/Positioning/shared/bookSet.ts (the type import, the two rationale comments, the helpers after "
     "resolveBooks); changed lines inside BookSetCapabilities, capabilitiesFor and MODE_CAPABILITIES: none." % (len(h6), len(h6)),
     r"@@ -1,4 \+1,5 @@.*@@ -38,13 \+39,19 @@.*@@ -221,6 \+228,104 @@ export const resolveBooks.*\+ \* POSN_AGGFIX RESTORES IT AS A VIEWER-SCOPED BOOK.*BookSetCapabilities .* removed 0, added 0\n  capabilitiesFor .* removed 0, added 0"),
    ('B1-AC7', 'command', rd('b1_ac7_typecheck.txt'),
     "2 of 2 runs: the portal worktree at HEAD and a scratch copy of HEAD with one injected error; 1 error line in the copy, on the injected line.",
     r"TYPECHECK COMMAND \(package\.json scripts\.typecheck at HEAD\): tsc -b --noEmit.*RUN 1: EXIT=0[ ]{2}error TS lines=0\b.*INJECTED at src/pages/Positioning/shared/bookSet\.ts:762.*bookSet\.ts\(762,14\): error TS2322.*RUN 2: EXIT=2"),
    ('B1-AC8', 'command', rd('b1_ac8_compare_before.txt'),
     "10 of 10 captures compared against B_DOM_BEFORE.json and identical; 1 of 1 mutated-weight control reported DIFFERENT.",
     r"HEAD 63edeeeb51b9bec8988f86c12dc92b5768ca2532.*SAME FIXTURES AS THE BEFORE RUN: true.*IDENTICAL 10 of 10.*CONTROL advisor/UST with the mutated weight: DIFFERENT"),
]

acceptance = []
for cid, method, ev, den, exp in rows:
    if ev is None:
        raise SystemExit('BLOCKED: no recorded output for ' + cid)
    if not re.search(exp, ev, re.S | re.M):
        raise SystemExit('BLOCKED: the expect for ' + cid + ' does not match its recorded output')
    acceptance.append({
        'criterion_id': cid, 'criterion_verbatim': crit[cid]['verbatim'], 'method': method,
        'invocation': crit[cid]['invocation'], 'output_evidence': ev, 'denominator': den, 'status': 'PASS', 'expect': exp,
    })
acceptance.append({
    'criterion_id': 'B1-AC9', 'criterion_verbatim': crit['B1-AC9']['verbatim'], 'method': 'manual_read_with_citation',
    'invocation': crit['B1-AC9']['invocation'], 'output_evidence': ac9,
    'denominator': '4 readings recorded (firm selection vs Models mode; the aggregate query and merge gate; what renders the merged object at this commit; what the viewer has to go on), 0 verdicts offered.',
    'status': 'UNVERIFIABLE-BY-INSTRUMENT', 'judgment': True,
    'status_reason': 'Judgment criterion: the task order marks it judgment="true" and grades it at L9. The readings are recorded in output_evidence and NO verdict is offered; the oracle is 3.0.0_SA_CVO~Z at L9.',
})

portal_ev = ('LOCAL commit ' + PORTAL_COMMIT + ' on wk-aggfix-1-3-portal in the portal repo, cut from edf85ce503 (origin/PROD). '
             'No gitlink move, no push, no promote (C-PORTAL-PROMOTE); drained by 2.0.0_SA_COO~Z. The portal repo is a separate '
             'object store, so this workspace checker announces the pin rather than resolving it.')
arts = [
    {'path_or_key': 'portal/src/api/portal-proxy.ts', 'kind': 'frontend_component', 'commit_or_etag': PORTAL_COMMIT,
     'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE', 'deploy_evidence': portal_ev, 'artifact_covered_by': ['B1-AC3', 'B1-AC5', 'B1-AC7']},
    {'path_or_key': 'portal/src/pages/Positioning/Positioning.tsx', 'kind': 'frontend_component', 'commit_or_etag': PORTAL_COMMIT,
     'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE', 'deploy_evidence': portal_ev, 'artifact_covered_by': ['B1-AC5', 'B1-AC7', 'B1-AC8', 'B1-AC9']},
    {'path_or_key': 'portal/src/pages/Positioning/shared/bookSet.ts', 'kind': 'frontend_component', 'commit_or_etag': PORTAL_COMMIT,
     'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE', 'deploy_evidence': portal_ev, 'artifact_covered_by': ['B1-AC4', 'B1-AC6', 'B1-AC7']},
    {'path_or_key': 'portal/src/pages/Positioning/README.md', 'kind': 'doc', 'commit_or_etag': PORTAL_COMMIT,
     'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE', 'deploy_evidence': portal_ev + ' Note 1a only; no criterion grades it.'},
]
for name, kind, cov, why in [
    ('B_DOM_BEFORE.json', 'test', ['B1-AC2', 'B1-AC8'], 'The five model views as advisor and client at edf85ce503; TO-B2-1 and TO-B3-1 compare against it and it is never re-captured.'),
    ('b_five_books_dom.mjs', 'test', ['B1-AC2', 'B1-AC5', 'B1-AC8'], '<FIVE_BOOKS_DOM_B>.'),
    ('b_fixtures.mjs', 'test', ['B1-AC2', 'B1-AC5', 'B1-AC8'], 'The fixtures, by VersionId with md5 refusal.'),
    ('b1_unit_control.ts', 'test', ['B1-AC4'], 'The unit control and its negative control.'),
    ('b1_unit_run.sh', 'script', ['B1-AC4'], '<UNIT_RUN_B1>.'),
    ('b_typecheck_run.sh', 'script', ['B1-AC7'], '<TYPECHECK_RUN_B>.'),
    ('b1_ac1_predicate_read.py', 'script', ['B1-AC1'], '<PREDICATE_READ_B1>.'),
]:
    arts.append({'path_or_key': D + '/' + name, 'kind': kind, 'commit_or_etag': 'PENDING-THIS-COMMIT',
                 'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE', 'deploy_evidence': 'Workspace deliverable, rides the commit that carries this proof. ' + why,
                 'artifact_covered_by': cov})
# PORTAL_REFS.md is NOT an artifact row: it is a tracked ledger file, so a PENDING row on it reads as the CCX class in a
# dry run (measured: the first check of this instance refused exactly that). Its one appended line is stated in the
# portal rows' deploy_evidence instead, and it rides the same commit as this instance.
portal_ev_refs = (' PORTAL_REFS.md carries the appended line "wk-aggfix-1-3-portal | ' + PORTAL_COMMIT[:10] +
                  ' | edf85ce503 (origin/PROD)", committed with this instance.')
for a in arts[:4]:
    a['deploy_evidence'] += portal_ev_refs

inst = {
    'schema_version': '1.0',
    'to_id': 'POSN_AGGFIX.TO-B1-1',
    'decomp_ref': {'doc': 'org/missions/D4/POSN/POSN_AGGFIX/decompositions/POSN_AGGFIX_DECOMP.md', 'vintage_commit': '605c03f81f', 'to_ref': TO},
    'phase': 'BUILD-GENERAL',
    'spec_ref': {'doc': 'org/missions/D4/POSN/POSN_AGGFIX/prd/POSN_AGGFIX_PRD.md', 'group': 'B', 'vintage_commit': 'cbd85e5cff'},
    'assignee': '0.9.0_WK_POSN_AGGFIX~3',
    'artifacts_produced': arts,
    'acceptance': acceptance,
    'controls': {
        'mutant': {
            'description': 'THREE mutants, one per instrument that could otherwise only pass. (1) B1-AC7: a scratch copy of portal HEAD (git archive, node_modules junctioned to the same install) with one injected type error in bookSet.ts, run through the SAME command read from package.json. (2) B1-AC4: the remembered-choice check disabled IN MEMORY (a client book list whose includes() answers true). (3) B1-AC8: one fixture weight mutated (shared-file UST holdings[0] VGSH 0.1451 -> 0.1951) and one advisor capture compared against B_DOM_BEFORE.json the same way.',
            'expected': 'the copy exits non-zero with an error on the injected line; the client lands on AGG; the mutated capture reads DIFFERENT',
            'observed': "(1) 'src/pages/Positioning/shared/bookSet.ts(762,14): error TS2322: Type 'string' is not assignable to type 'number'.' RUN 2: EXIT=2, injected-line hits 1. (2) 'client lands on  = \"AGG\"   CONTROL FIRED'. (3) 'CONTROL advisor/UST with the mutated weight: DIFFERENT -- .composition.tile_count: BEFORE=13  NOW=14'.",
            'status': 'FIRED-AS-EXPECTED',
        },
        'determinism': {
            'method': 'Every render capture settles only on three consecutive identical DOM reads. The BEFORE capture (portal edf85ce503) and the compare run (portal ' + PORTAL_COMMIT[:10] + ') read the same fixture bytes: 3 of 3 raw objects md5-matched to the manifest in both runs and the built fixtures md5 d35f3c4a1844980817f6ee556dad9bc7 printed in both, with every unfixtured request answered 404 identically. The unit control ran twice on the same inputs (the uncommitted tree, then the commit).',
            'observed': 'unit control 18 of 18 PASS with the control fired in both runs; SAME FIXTURES AS THE BEFORE RUN: true; advisor and client captures IDENTICAL 10 of 10 across the two runs.',
            'status': 'STABLE',
        },
    },
    'declared_exclusions': [
        {'item': '`internal` handed to the HoldingsTab mount (AF1-s-13)', 'reason': 'HoldingsTab declares no internal prop: the pass fails the portal typecheck (TS2322 at the mount, measured in b1_mount_internal_prop_typecheck_measure.txt) and HoldingsTab.tsx is outside this order\'s <paths>. Not committed. Row POSN_AGGFIX-Z-W3-S1.'},
        {'item': 'the merged aggregate reaching the Holdings tab (AF1-s-13, "the Positioning data object the tab reads")', 'reason': 'In Models mode the tab renders its own getPositioningData fetch (HoldingsTab.tsx :727-737 @edf85ce503), not the page object. The merge feeds the page\'s dataByMode.models (PositioningSummary, which reads current_holdings only for etfs and satellites). Same row W3-S1.'},
        {'item': 'the Holdings tab UI: the Aggregate selector entry, both panels on the aggregate, the Model Breakdown group, the landing', 'reason': 'TO-B2-1 (AF1-s-14); the order says HoldingsTab.tsx is not this order\'s.'},
        {'item': 'live served bytes: opal_aggregate.json and the shared file after the producer change', 'reason': 'Every render ran on fixtures pinned by VersionId (b_fixtures.mjs MANIFEST). TO-B3-1 (AF1-s-16) reads the live bytes.'},
        {'item': "whether any issued account carries userType 'Dev' with a firmId other than 'opal-capital'", 'reason': "An auth-plane fact the portal cannot answer; B1-AC1 states the predicate admits that class and says so. `comp-find 'userType' infra/aws/auth` read 2 DOC hits across 9 files (ARCHITECTURE.md :42, :59), no issuing source."},
        {'item': 'a real client session\'s claims', 'reason': 'AuthContext has no client class; the client claim set was constructed and printed on every run. Row POSN_AGGFIX-Z-W3-S2.'},
        {'item': 'the unfixtured requests in every render run (advisor-intelligence prefetches, portal-content, the json manifest, the analytics ingest)', 'reason': 'Answered 404 and listed (B_DOM_BEFORE.json meta.unfixtured) so the BEFORE/AFTER comparison measures the page and not the network.'},
    ],
    'surprises': [
        "POSN_AGGFIX-Z-W3-S1: AF1-s-13's `internal` to the HoldingsTab mount and its merge 'into the data object the tab reads' cannot land inside TO-B1-1's <paths>: HoldingsTab has no internal prop (TS2322, measured) and renders its own Models fetch; TO-B2-1 holds HoldingsTab.tsx but not Positioning.tsx.",
        "POSN_AGGFIX-Z-W3-S2: AuthContext.tsx has no client class (Claims: firmId, userType, advisorId, firmRole, advisorRole); the client claim set for the renders was constructed at the parseClaims deny-floor and recorded.",
    ],
    'session_log': D + '/',
    'compiler_tools': [
        {'tool': 'tsc 5.9.3 (the portal typecheck, tsc -b --noEmit, read from package.json)', 'invocation': 'timeout 900 bash ' + P['TYPECHECK_RUN_B'],
         'result': 'HEAD exit 0 with 0 error lines; the injected scratch copy exit 2 on the injected line. The runner\'s FIRST run exited 127 (tsc not found: a C:/ root inside PATH) -- an instrument defect, fixed in the runner and re-run; the recorded file is the re-run.'},
        {'tool': 'bun 1.3.14 (TypeScript executed directly, as POSN_ASTTAX ~26 recorded)', 'invocation': 'timeout 300 bash ' + P['UNIT_RUN_B1'], 'result': 'exit 0; 18 of 18 real cases PASS; the negative control fired.'},
        {'tool': 'playwright-core + system Edge, vite started from this worktree (b_five_books_dom.mjs)', 'invocation': 'timeout 900 node ' + P['FIVE_BOOKS_DOM_B'] + ' --capture-before | --network-arms | --compare-before',
         'result': 'CAPTURED 10 of 10 at edf85ce503; network arms MET; IDENTICAL 10 of 10 with the control DIFFERENT. The first BEFORE attempt timed out writing nothing (a read of innerText on an SVG node threw every time) -- fixed in the harness, diagnosed with its --probe mode, then captured once.'},
        {'tool': 'proof-of-spec-check.py (this worktree\'s copy)', 'invocation': 'python .tools/proof-of-spec-check.py ' + OUT + ' B1-AC1,B1-AC2,B1-AC3,B1-AC4,B1-AC5,B1-AC6,B1-AC7,B1-AC8,B1-AC9',
         'result': 'see b1_proof_check.txt beside this instance.'},
    ],
}
s = json.dumps(inst, indent=1, ensure_ascii=True)
open(OUT, 'wb').write((s + '\n').encode('ascii'))
print('WROTE ' + OUT + ' bytes=' + str(len(s) + 1) + ' acceptance rows=' + str(len(acceptance)))
print(ac3_summary.strip())
print(ac6_summary.strip())
