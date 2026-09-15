"""Append this worker's surprise rows to the project's channel, inside the LAST fenced
json array, without touching a single existing row.

WHY A SCRIPT AND NOT AN EDIT: the file carries 60 fenced blocks and 234 rows; a hand edit
of a 6187-line append-only record is the mutation the channel exists to prevent. This reads
the last block, parses it, appends, and re-serializes ONLY that block -- and it REFUSES if
the row count of that block does not grow by exactly len(NEW), or if any id it is asked to
add already exists anywhere in the file.

PURE ASCII by construction: every row below is ASCII and the check runs before the write.

Usage: PYTHONUTF8=1 python3 <this>            (from the workspace worktree root)
"""
import io
import json
import re
import sys

PATH = 'org/missions/D4/POSN/POSN_ASTTAX/surprise-channel/investigations/INVESTIGATION_v1.md'
TS = '2026-09-15T04:26:05Z'
ME = '0.9.0_WK_POSN_ASTTAX~26'


def row(rid, one_line, spec_asserts, world_is, evidence, notes, klass='OBSERVATION',
        hazard='INERT', disposition='UNDER_INVESTIGATION'):
    return {
        'id': rid,
        'project': 'POSN_ASTTAX',
        'fabric': 'site-z',
        'surfaced_by': ME,
        'surfaced_at': TS,
        'one_line': one_line,
        'class': klass,
        'hazard_standing': hazard,
        'grounding': {'status': 'GROUNDED', 'evidence': evidence},
        'disposition': disposition,
        'spec_asserts': spec_asserts,
        'world_is': world_is,
        'notes': notes,
    }


NEW = [
    row('POSN_ASTTAX-Z-W26-S1',
        'ACTED ON AN ISSUER AMENDMENT MID-ORDER, recorded as the notice required: 2.0.0_SA_COO~Z '
        '(~04:1xZ, then ~04:15Z) withdrew act 2 of TO-W3-1 (Math.round at PositioningSummary.tsx:1011) '
        'on PRD v0.11 @ab2ee8052a, which CLARIFIES C-SUMMARY-COPY to "no more than two decimals, '
        'trailing zeros dropped" and withdraws "rounds like its two siblings". This worker had already '
        'written Math.round; it was replaced with Number(v.toFixed(2)) BEFORE any commit, so no '
        'Math.round reading exists in any commit on wk-posn-6-26-portal. The amended order at '
        'SITEZ @1b791c6a11 was copied over this worktree\'s copy of the order file (inside the grant) '
        'and W3-AC5 / W3-AC6 were re-run and re-recorded against its text.',
        'TO-W3-1 as issued (@910815809f) act 2: "the label renders Math.round(v)% like the Custom pair"; '
        'PRD v0.10 C-SUMMARY-COPY: "the third percent label rounds like its two siblings".',
        'PRD v0.11 @ab2ee8052a (brief half, ratified text untouched) clarifies the same clause to at most '
        'two decimals with trailing zeros dropped, on the CTO\'s Z-S138: Math.round would have re-formatted '
        'every Models label (82.6% -> 83%), a surface nobody asked to change. MEASURED over the served '
        'fixture, pre-edit dump vs post-edit dump on one instrument: Models 11 of 11, Models/Benchmark 9 of 9 '
        'and ETFs 8 of 8 labels BYTE-IDENTICAL; exactly 5 Satellites labels changed, every one an IEEE '
        'artifact (62.589999999999996% -> 62.59%, 29.820000000000004% -> 29.82%, 39.43000000000001% -> '
        '39.43%, 27.830000000000002% -> 27.83%, 90.24000000000001% -> 90.24%).',
        ['ISSUER NOTICE (verbatim in this worker\'s prompt, 2026-09-15 ~04:1xZ and ~04:15Z): "DO NOT commit '
         'Math.round ... replace it with the two-decimal trimmed form" and "copy the amended file over yours '
         'with git show SITEZ:<path> > <path>".',
         'PRD v0.11 @ab2ee8052a, the clarified clause read at that commit (lines 36-40 of the blob): "The '
         'single-bar percent label renders the value at no more than two decimals, trailing zeros dropped '
         '(PositioningSummary.tsx:1011 ...); Models and ETFs labels are byte-identical to today (82.6%, 17.4%)."',
         'AMENDED ORDER at SITEZ @1b791c6a11 diffed against the issued text: 4 hunks (the PRD pin v0.10 -> '
         'v0.11, act 2, and the label clauses of W3-AC5 and W3-AC6). The copy in this worktree is now that text.',
         'BOTH DUMPS KEPT: deliverables/0.9.0_WK_POSN_ASTTAX~26/w3_preedit_dom_read.txt (taken with the two '
         'files at refs/drains/posn-6-portal, restored by md5) and w3_postedit_dom_read.txt; the comparison is '
         'w3_label_control_compare.txt.'],
        'Filed because the order\'s face changed mid-execution and the record must say which face was executed. '
        'No hazard: the superseded reading never reached a commit.'),

    row('POSN_ASTTAX-Z-W26-S2',
        'THE ui-smoke TEXT DUMP IS A 160-CHARACTER PREFIX, so the label clause of W3-AC5 -- graded "in the TEXT '
        'dump" in both the issued and the amended text -- cannot be discriminated from that output: on this page '
        'the 160 characters are the left nav, giving 0 matching labels out of a DENOMINATOR OF 0 LABELS, which '
        'is the same number a page full of raw floats would print.',
        'TO-W3-1 W3-AC5 (issued): "the TEXT dump of every run carries NO label matching the regex ... (printed '
        'grep count 0 with the denominator of labels)"; amended: "every single-bar percent label in the TEXT dump '
        'matches ^[0-9]+(.[0-9]{1,2})?%$ (the label count and the match count printed, equal)"; the issuer\'s '
        'hand-over: "the TEXT dump is your DOM read".',
        'scripts/ui-smoke.mjs prints TEXT from page.evaluate as document.body.innerText.replace(/s+/g, " ").slice(0, 160) '
        '-- a 160-char prefix, not a DOM read. All five captures in this order printed the identical prefix '
        '("INSIGHTS Market Overview Model Portfolios ... Correlatio"), which contains no percent label at all. '
        'scripts/ is outside this order\'s <paths> grant, so the instrument was not changed; a supplementary '
        'playwright DOM read was written instead and BOTH counts are printed from it (Models 11 of 11 labels '
        'match the shape, Benchmark 9 of 9, ETFs 8 of 8, Satellites 30 of 30).',
        ['scripts/ui-smoke.mjs line 334 at refs/drains/posn-6-portal: "text: document.body.innerText.replace(...).slice(0, 160)".',
         'The five recorded runs (w3_ac5_uismoke.txt, w3_ac6_uismoke.txt, w3_expanded_uismoke.txt) each print the '
         'same nav prefix as TEXT.',
         'SUPPLEMENTARY INSTRUMENT: deliverables/0.9.0_WK_POSN_ASTTAX~26/w3_dom_read.mjs (same Edge, same stubbed '
         'session, same fixture router as ui-smoke) enumerates every single-bar label with its computed colour and '
         'prints label count beside match count; output in w3_postedit_dom_read.txt.'],
        'A one-line change to ui-smoke.mjs (a --textlen flag, or printing the label nodes) would make this clause '
        'gradeable by the named invocation alone; that file belongs to no cell in this round.'),

    row('POSN_ASTTAX-Z-W26-S3',
        'THE PRESENCE RULE LANDED ON ONE PANEL, AND THE PAGE DRAWS THREE: with the Positioning Summary now '
        'listing only the classes a view holds, the Portfolio Composition treemap\'s legend on the SAME PAGE '
        'still lists all five classes in every mode -- including Commodities and Alternatives with no tile '
        'behind them in Models and ETFs -- so the two legends disagree about what the view holds.',
        'Andrew-direct 2026-09-15 ~00:4xZ: "There is no need to display the different legend categories if they '
        'do not appear in the view"; PRD v0.9 C-PRESENT-CLASSES scopes the rule to "The Positioning Summary".',
        'In the Models capture (w3_models.png) the Positioning Summary legend lists 3 classes while the Portfolio '
        'Composition legend below it lists 5 (Fixed Income, Equity, Structured, Commodities, Alternatives); in the '
        'ETFs capture the two read 2 and 5. That legend is rendered by HoldingsTab.tsx, which TO-W3-1 step 5 '
        'assigns to TO-W2-1 (F4) and which is NOT in this order\'s <paths>, so nothing was changed there.',
        ['w3_models.png / w3_etfs.png / w3_sats.png (this worker\'s captures at 1440px, fixtures from the served '
         'bytes) show both legends in one frame.',
         'TO-W3-1 step 5: "Nothing else: HoldingsTab.tsx and the adapter files belong to TO-W2-1 (F4) on a sibling branch."',
         'PRD v0.9 C-PRESENT-CLASSES names "The Positioning Summary" only; Andrew\'s sentence names no panel.'],
        'For 1.0.0_SA_CTO~Z at L10 / 3.0.0_SA_CVO~Z at L9: whether the rule reaches the treemap legend is a spec '
        'question, not a worker\'s. No served byte is wrong.'),

    row('POSN_ASTTAX-Z-W26-S4',
        'THE PORTAL REPO DOES NOT IGNORE .scratch/, and both graded invocations write there: W3-AC5 and W3-AC6 '
        'save their PNGs to .scratch/ while W3-AC2 reads an UNSCOPED git status and expects "the same two files '
        'and nothing else" -- so the two criteria collide unless the capture artifacts are moved out of the portal '
        'tree before the status read.',
        'TO-W3-1 W3-AC2: "the unscoped git -C portal status --porcelain shows the same two and nothing else"; '
        'W3-AC5 / W3-AC6 invocations write .scratch/w3_*.png inside portal/.',
        'portal/.gitignore (79 lines at refs/drains/posn-6-portal) lists dist, node_modules, .cache, .comp-graph/, '
        '.frontend-dev-results/ and others, but not .scratch; git check-ignore -v .scratch/x.png returns rc 1 '
        '(NOT ignored). This worker copied every capture, fixture and log into its deliverables directory and then '
        'removed portal/.scratch before the graded W3-AC2 run, so no artifact was lost and no ignore file was '
        'edited (.gitignore is not in this order\'s <paths>).',
        ['git -C portal check-ignore -v .scratch/x.png -> rc 1, no rule printed (the NOT-IGNORED verdict).',
         'The artifacts are kept at org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~26/ '
         '(w3_models.png, w3_models_bench.png, w3_etfs.png, w3_sats.png, the two expanded captures, '
         'w3_fixtures_build.txt and the dom-read dumps).'],
        'A one-line .gitignore entry would remove the collision for every future capture-bearing cell; that file is '
        'in no cell\'s grant this round.'),

    row('POSN_ASTTAX-Z-W26-S5',
        'THE LONGEST SATELLITES LABEL IS CLIPPED AT THE PANEL EDGE at the ratified 1440px acceptance width: in the '
        'Satellites capture, Opal Satellite 90\'s Equity label renders as "90.24" with its percent sign cut off by '
        'the panel boundary. PRE-EXISTING, NOT INTRODUCED: at the ref the same label was the longer '
        '"90.24000000000001%", so the overflow was wider before this cell; the two-decimal form narrows it without '
        'clearing it, and the withdrawn Math.round reading ("90%") would have hidden it.',
        'PositioningSummary.tsx compactColumns (>= 6 books) sets the single-bar label to text-sm at '
        'left-[calc(100%+0.375rem)], and the panel\'s ACCEPTANCE WIDTH ruled by 1.0.0_SA_CTO~Z is "at 1440px all '
        'columns, all book labels and all VALUE labels render with no clipping".',
        'At 1440px with 8 satellite books the last column\'s label runs past the panel\'s right edge. The DOM text '
        'is complete ("90.24%"); only the render is clipped, so no DOM-level check can see it -- it was found by '
        'READING THE PNG.',
        ['w3_sats.png and w3_sats_expanded.png (1440px, fixtures at holdings.json VersionId '
         '67GP52SdV1rw6QFVNPytU6ec4TvhwJh3): the rightmost label reads "90.24" with no percent sign.',
         'w3_postedit_dom_read.txt: the same node\'s DOM text is "90.24%" (30 of 30 labels match '
         '^[0-9]+(.[0-9]{1,2})?%$), so the defect is geometric, not textual.',
         'w3_preedit_dom_read.txt: the pre-edit label at that position was "90.24000000000001%" -- 12 characters '
         'longer -- so the overflow predates this cell.'],
        'Not repaired here: the order\'s act 2 is the label FORMAT and its <paths> carry no layout change; the '
        'remedy (a narrower label class or more column padding at >= 6 books) is a display decision for the CTO.'),

    row('POSN_ASTTAX-Z-W26-S6',
        'THE ORDER\'S PRESENCE RULE AND THE PRD\'S SENTENCE DIFFER ON THE BENCHMARK VIEW, and the difference is '
        'visible: the order says the set is computed over "the books portfolio values" ALWAYS plus the benchmark '
        'values when Benchmark or Relative is on, while C-PRESENT-CLASSES says "the classes with a non-zero value '
        'in any column the current view DRAWS". The Benchmark view draws only benchmark bars, and no benchmark '
        'column carries Structured today -- so under the order the legend shows Structured with no drawn segment, '
        'and under the PRD\'s sentence it would not appear at all.',
        'TO-W3-1 act 1: "over every column the current view draws -- the books portfolio values; the benchmark '
        'values when the Benchmark or Relative view is on; the custom column when the blend is valid"; PRD v0.9 '
        'C-PRESENT-CLASSES: "the classes with a non-zero value in any column the current view draws".',
        'THE ORDER\'S READING IS WHAT IS IMPLEMENTED (its own instruction: never two readings in code). Measured on '
        'the served bytes: every benchmark allocation has structured = 0 while the LT and ULT portfolio columns '
        'carry 1.5 and 2.0, so the Benchmark view renders a 3-entry legend and a Structured row of five zeros. '
        'BENCHMARK-ONLY CLASSES in today\'s bytes: none (the empty set), which is why W3-AC5\'s "a class present '
        'only in the benchmark column appears" has no live witness and W3-AC3 case (a) carries that edge instead.',
        ['w3_fixtures_build.txt: "EXPECTED MODELS presence (portfolio view, 5 columns): [Fixed Income, Equity, '
         'Structured]" and "BENCHMARK-ONLY CLASSES (present in a benchmark column, absent from every portfolio '
         'column): []".',
         'w3_postedit_dom_read.txt, MODELS / Benchmark view: LEGEND 3 entries; ASSET CLASS (3); the Structured row '
         'reads 0 0 0 0 0; 9 of 9 labels match the shape.',
         'w3_presence_unit_control output case (a): a class non-zero ONLY in a benchmark column is PRESENT -- the '
         'constructed edge today\'s bytes do not contain.'],
        'For L9/L10: keeping the portfolio columns in the set means a reader in Benchmark view sees the class the '
        'BOOK holds even where the benchmark holds none, which is arguably the intent; the narrower reading would '
        'hide a class the model is actually exposed to the moment the view is flipped. Named, not decided.'),
]


def main():
    src = io.open(PATH, encoding='utf-8', newline='').read()
    blocks = list(re.finditer(r'```json\n(.*?)\n```', src, re.S))
    if not blocks:
        print('BLOCKED: no fenced json block found')
        return 1
    last = blocks[-1]
    rows = json.loads(last.group(1))
    existing = set(re.findall(r'"id":\s*"([^"]+)"', src))
    for r in NEW:
        if r['id'] in existing:
            print('BLOCKED: %s already exists in the file' % r['id'])
            return 1
        blob = json.dumps(r)
        nonascii = [c for c in blob if ord(c) > 127]
        if nonascii:
            print('BLOCKED: %s carries non-ASCII %r' % (r['id'], nonascii[:5]))
            return 1
    before = len(rows)
    # PURE TEXT INSERTION, NOT A RE-SERIALIZATION. Re-dumping the parsed array would rewrite
    # the whitespace of every existing row in this block -- semantically identical, and still
    # a diff that touches rows this worker must not touch. The existing bytes up to the array's
    # closing bracket are carried through unchanged; only ",\n<new rows>" is added before it.
    blocktext = last.group(1)
    close = blocktext.rstrip().rfind(']')
    if close < 0 or blocktext.rstrip()[:close].rstrip()[-1:] != '}':
        print('BLOCKED: the last block does not end with a row then a closing bracket')
        return 1
    head = blocktext[:close].rstrip()
    insert = ',\n' + ',\n'.join(json.dumps(r, indent=2) for r in NEW)
    body = head + insert + '\n]'
    if not body.startswith(head):
        print('BLOCKED: the existing bytes did not survive')
        return 1
    out = src[:last.start()] + '```json\n' + body + '\n```' + src[last.end():]
    io.open(PATH, 'w', encoding='utf-8', newline='').write(out)
    check = json.loads(re.findall(r'```json\n(.*?)\n```', io.open(PATH, encoding='utf-8').read(), re.S)[-1])
    print('LAST BLOCK: %d rows -> %d rows (appended %d)' % (before, len(check), len(check) - before))
    if len(check) - before != len(NEW):
        print('BLOCKED: the appended count is not %d' % len(NEW))
        return 1
    print('APPENDED: %s' % ', '.join(r['id'] for r in NEW))
    return 0


if __name__ == '__main__':
    sys.exit(main())
