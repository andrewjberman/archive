"""AMGT_RESAPP round 78 -- the issuer's order generator (2.0.0_SA_COO~Z).

Reads the three group notes beside this file (THE ACT, THE CRITERIA and the paths block of each drafted cell) and writes one
task order per cell in the round-77 order shape. It writes files only; it commits nothing and spawns nothing.

  python cut_orders.py --portal-ref <sha> [--only bb-9] [--out <dir>]
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = "org/missions/D5/AMGT/AMGT_RESAPP"
ORDERS = os.path.join(HERE, "..", "..", "..", "task-orders")
CHANNEL = PROJECT + "/surprise-channel/investigations/INVESTIGATION_v1.md"
ISSUER = "2.0.0_SA_COO~Z"

# id, notes file, heading prefix, slug, slot, worker class, title, preflight adversary line, extra bound lines, record note
CELLS = [
    ("bb-1", "GROUP_A_NOTES.md", "## A1", "the-segments-reader", 289, "worker",
     "THE SEGMENTS READER: A SEGMENT TABLE FROM THE STORED BLOOMBERG SEGMENTS OBJECT (RULING 3, FWD-1)",
     "85 stored partitions read at the cut: 76 names carry revenue rows, 9 none, 50 operating income; the object carries no fiscal period and no currency.",
     ["The stored object states no fiscal period and no currency. Serve the vendor's period numbers and a null currency, each with its plain note. Do not guess either."],
     "CTO round-77 ruling 3. Issuer default on period and currency: CALLS_AT_THE_CUT_20261007.md section B."),
    ("bb-2", "GROUP_B_NOTES.md", "## B1", "one-statement-of-inputs", 290, "worker-light",
     "ONE STATEMENT OF INPUTS, WITH A FILINGS ROW THAT SAYS WHAT THE PAGE USED (RULING 4, FWD-12; ROW Z-W286-S2)",
     "95 of 95 covered names serve input_provenance with no filings row; the overlay's provenance says no filings run is recorded on 95 of 95 while 12 theses cite a filing.",
     ["The /ledger route is not retired by this cell and is not edited."],
     "CTO round-77 ruling 4. The page half is DSGN_AMGTV1's."),
    ("bb-3", "GROUP_A_NOTES.md", "## A2", "the-officer-rank", 291, "worker-light",
     "THE OFFICER RANK: CHIEF EXECUTIVE, THEN CHIEF FINANCIAL OFFICER, THEN THE LIST AS SERVED (RULING 9)",
     "A chief-executive row is present and not first in 17 of 93 served rosters; 3 stored lists carry no chief-executive title.",
     ["A list with no chief-executive title is left in the order it was served."],
     "CTO round-77 ruling 9."),
    ("bb-4", "GROUP_A_NOTES.md", "## A3", "the-slash-safe-officers-reader", 292, "worker-light",
     "THE SLASH-SAFE OFFICERS READER: A STORED LIST FOR A SLASH NAME IS READ (ROW Z-S365)",
     "The reader finds 89 of 91 stored folders; BP/ LN Equity and NG/ LN Equity are stored and never read.",
     ["bloomberg_fallback.security_key() keeps its return value: the writer is already slash-safe."],
     "CTO msg 30847 (a round-78 cell), row Z-S365."),
    ("bb-7", "GROUP_E_NOTES.md", "## E1", "the-pool-carries-each-legal-name", 293, "worker",
     "THE POOL RECORD CARRIES ITS LEGAL NAME AND NAME SEARCH READS IT (ROW Z-W275-S1)",
     "100 of 243 pool records carry a name search can read; 'apple' and 'microsoft' answer nothing; this project's own stored objects name 243 of 243.",
     ["You run no command with --write-pool and make no store write: the mint is the issuer's act under its own signed pair.",
      "Every existing field of every existing pool record is unchanged; the legal name is an ADDED field."],
     "CTO rulings file @f97be3fd6f (bb-7: the pool carries the name, not a copied file), row Z-W275-S1."),
    ("bb-8", "GROUP_B_NOTES.md", "## B2", "peer-price-with-its-own-listing-currency", 294, "worker-light",
     "EACH PEER PRICE WITH THE CURRENCY OF ITS OWN LISTING (FWD-8)",
     "price_currency is served on 25 of 676 priced peer rows; 3 of those 25 carry another listing's currency.",
     ["This cell does not close FWD-8: about 600 rows have no currency in any stored file. Do not add a vendor call to find one."],
     "DSGN_AMGTV1 FWD-8, carried by CTO round-77 enrichment item 7 and msg 31020."),
    ("bb-9", "GROUP_B_NOTES.md", "## B3", "the-country-in-plain-case", 295, "worker-light",
     "THE COUNTRY IN PLAIN CASE (DSGN_AMGTV1 FWD-27)",
     "The country header figure is all capitals on 95 of 95 covered names, 22 distinct values.",
     [],
     "CTO msg 30870 and round-77 enrichment item 7."),
    ("bb-10", "GROUP_B_NOTES.md", "## B4", "one-marker-for-a-name-outside-coverage", 296, "worker-light",
     "ONE SERVED MARKER FOR A NAME OUTSIDE COVERAGE (ROW Z-S364)",
     "No marker is served on any of 97 overlays read; the pool holds 243 names, 95 covered and 148 outside.",
     ["Covered means a name in covered_security_keys(). The older covered_no_block field is not edited and not reused."],
     "CTO msgs 30812 and 31020, row Z-S364."),
    ("bb-11", "GROUP_B_NOTES.md", "## B5", "a-plain-served-news-source-name", 297, "worker-light",
     "A PLAIN SERVED NEWS-SOURCE NAME",
     "The top band serves plain publisher names on 69 of 69 items; 640 feed items carry a code only.",
     [],
     "CTO round-77 enrichment item 7."),
    ("bb-13", "GROUP_A_NOTES.md", "## A4", "peers-v-below-three-peers", 298, "worker-light",
     "PEERS V BELOW THREE PEERS READS NOT AVAILABLE WITH ITS REASON (ROW Z-S162)",
     "The floors today are 6 peers per measure and 8 for the score; no distinct reason is served below 3.",
     ["The floors of 6 and 8 are not changed. You do not run the scores producer: a store write is the issuer's act."],
     "Andrew's word relayed in CTO msg 30663, row Z-S162. Issuer default: CALLS_AT_THE_CUT_20261007.md section B."),
    ("bb-14", "GROUP_C_NOTES.md", "## C5", "the-pull-driver-names-a-missing-library", 299, "worker-light",
     "THE PULL DRIVER GIVES A MISSING BLOOMBERG LIBRARY ITS OWN STOP WORD (ROW Z-S366)",
     "Under a Python with no blpapi the driver reads TERMINAL_DOWN, exit 5, with 0 calls.",
     [],
     "CTO round-77 ruling 14, row Z-S366."),
    ("bb-15", "GROUP_C_NOTES.md", "## C6", "the-rot-signal-gets-a-home", 300, "worker-light",
     "THE ROT SIGNAL GETS A HOME ITS OWN MODULE OWNS (ROW Z-W279-S2)",
     "The glob matches 1 file, in a worker folder, computed 2026-09-10; its only writer is rot.main().",
     ["Copy, never move: the worker folder's file stays where it is."],
     "CTO round-77 ruling 14, row Z-W279-S2."),
    ("bb-16", "GROUP_D_NOTES.md", "## D1", "the-seeking-alpha-collector-record-reader", 301, "worker-light",
     "THE SEEKING ALPHA LAST-READ READER OVER THE COLLECTOR'S JOB RECORDS (ROW Z-S367)",
     "The served reader takes the date from four tables holding 3 pilot partitions of 2026-09-11: 95 of 95 names read wrong.",
     ["`lib/research/freshness/seeking_alpha_job_record.schema.json` and `lib/research/freshness/build_view.py` are READ, never edited."],
     "CTO msg 31060 and rulings file @f97be3fd6f (C2: serve only when the collector's records exist), row Z-S367."),
    ("bb-17", "GROUP_D_NOTES.md", "## D2", "the-adapter-cell", 302, "worker",
     "THE ADAPTER CELL: EVERY HOOKUP OF THE ROUND IN THE ONE SERVED MODULE",
     "At the base H1 to H5 fail (no hookup made) and H6 reads 2 wrong rows of 60; the round-77 served shape reads YES.",
     ["The segment table, the segment period labels and the Seeking Alpha record reader are NOT wired by this cell."],
     "Round-77 analysis enrichment list; CTO rulings file @f97be3fd6f. WAVE 1: cut from the drain of bb-2, bb-3, bb-8, bb-9, bb-10, bb-11."),
    ("bb-20", "GROUP_D_NOTES.md", "## D3", "nine-files-recommitted-with-lf-endings", 304, "worker-light",
     "THE LINE-ENDING CELL: NINE FILES RE-COMMITTED WITH UNIX LINE ENDINGS (ROW Z-S362)",
     "45 tracked files carry CR in the index under eol=lf; 34 of 41 .py fail the commit gate as they stand; 7 sit under infra/aws/lambda/; 9 are landable.",
     ["No file under `infra/aws/lambda/` is touched. No gate override of any kind."],
     "CTO rulings file @f97be3fd6f (C1). Row Z-S362 stays OPEN: the drain prints the landed list beside 45."),
    ("bb-21", "GROUP_D_NOTES.md", "## D4", "segment-periods-labelled-where-they-tie", 305, "worker-light",
     "THE SEGMENT TABLE'S PERIOD AND CURRENCY, LABELLED ONLY WHERE THEY TIE TO STORED REVENUE",
     "Of the 76 names with revenue rows, Period 1's top-level sum equals a stored fiscal year's revenue on 72 and does not on 4; none lacks stored revenue.",
     ["`lib/research/api/segment_table.py` is another cell's file: do not create or edit it."],
     "CTO ruling msg 31077; reads/SEGMENT_PERIOD_LABEL_READ.md."),
    ("bb-22", "GROUP_D_NOTES.md", "## D5", "divergence-reads-the-served-dispersion-fields", 306, "worker-light",
     "THE DIVERGENCE SCORE READS THE DISPERSION FIELDS BLOOMBERG SERVES",
     "Bloomberg refuses 4 of the 6 names divergence.py asks for (probe of one name, 3 requests, 2026-10-07 15:17Z).",
     ["You do not run the scores producer: a store write is the issuer's act."],
     "CTO ruling msg 31087; AMGT_CORPUS msg 31085."),
    ("bb-23", "GROUP_F_NOTES.md", "## F1", "the-build-takes-two-packages-from-the-deployed-zip", 307, "worker",
     "THE BUILD TAKES PYARROW AND LINUX RPDS-PY FROM OPAL'S OWN DEPLOYED ZIP, NEVER A DOWNLOAD",
     "None of the build's 8 pinned wheels is on this box; the deployed zip on disk hashes to the live CodeSha256 and holds both packages (147 files).",
     ["You do NOT run the build script, `pip`, `terraform` or any AWS write. One AWS read (the function's configuration) is made by the check.",
      "No fallback: nothing you write may fetch pyarrow or rpds-py for the Lambda's platform, under any flag."],
     "CTO ruling msg 31206 (two terms). ADDED MID-ROUND by that ruling: decomposition s.86e ADDENDUM 1."),
]

RISK = {"bb-20": "WORLD", "bb-23": "WORLD"}
NO_ADAPTER_LINE = ("bb-4", "bb-13", "bb-15", "bb-7", "bb-1", "bb-16", "bb-21", "bb-22")

FORBIDDEN = ("identity, unresolved, security key, crosswalk, dossier, landed, model block, estate, stage, input ledger or bronze")


def _section(text, start_re, stop_re):
    m = re.search(start_re, text, flags=re.M)
    if not m:
        return None
    rest = text[m.end():]
    s = re.search(stop_re, rest, flags=re.M)
    return rest[: s.start()] if s else rest


def parse_cell(notes_path, prefix):
    text = open(notes_path, encoding="utf-8").read()
    block = _section(text, r"^%s\b.*$" % re.escape(prefix), r"^## ")
    if block is None:
        raise SystemExit("no cell %s in %s" % (prefix, notes_path))
    act = _section(block, r"^### \d+\. (THE ACT|The act).*$", r"^### \d+\. ")
    crit = _section(block, r"^### \d+\. (THE CRITERIA|The criteria).*$", r"^### \d+\. ")
    paths = _section(block, r"^### \d+\. (`<paths>`|Paths).*$", r"^### \d+\. ")
    if act is None or crit is None or paths is None:
        raise SystemExit("cell %s lacks act, criteria or paths" % prefix)
    criteria = []
    head = re.search(r"^%s\b.*$" % re.escape(prefix), text, flags=re.M).group(0)
    n_cell = re.search(r"bb-(\d+)", head).group(1)
    for m in re.finditer(r"^- \*{0,2}(AC\d+)\b(.*?)(?=^- \*{0,2}AC\d|\Z)", crit, flags=re.M | re.S):
        cid, tail = m.group(1), m.group(2)
        em = re.search(r"Expect:\s*(.*)", tail, flags=re.S)
        if not em:
            raise SystemExit("criterion %s of %s has no Expect" % (cid, prefix))
        expect = re.sub(r"\s+", " ", em.group(1)).strip().replace("`", "").rstrip(".")
        im = re.search(r"`(cd [^`]+)`", tail[: em.start()])
        where = "deployed" if im and "--where deployed" in im.group(1) else "local"
        inv = im.group(1).strip() if im else (
            'cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "%s/deliverables/%s/round78/checks/r78_bb%s.py" '
            '--crit %s --where %s; echo "exit=$?"' % (PROJECT, ISSUER, n_cell, cid, where))
        criteria.append((cid, inv, expect))
    if not 1 <= len(criteria) <= 3:
        raise SystemExit("cell %s has %d criteria" % (prefix, len(criteria)))
    fenced = re.search(r"```\n(.*?)```", paths, flags=re.S)
    plist = [ln.strip() for ln in (fenced.group(1) if fenced else paths).splitlines() if ln.strip()]
    return act.strip("\n"), criteria, plist


def order_text(cell, portal_ref):
    cid, notes, prefix, slug, slot, wclass, title, adversary, bounds, record = cell
    act, criteria, plist = parse_cell(os.path.join(HERE, notes), prefix)
    serial = "0.9.0_WK_AMGT_RESAPP~%d" % slot
    wt = "C:/tmp/r78-%d" % slot
    stem = "AMGT_RESAPP.TO-AMGT-%s.%s" % (cid, slug)
    deliv = "%s/deliverables/%s/" % (PROJECT, serial)
    paths = [p for p in plist if "<worker serial>" not in p and "deliverables/0.9.0_WK" not in p and p != CHANNEL]
    paths += [deliv, CHANNEL]
    crit_xml = "\n".join(
        '  <criterion id="%s" cell_refs="AMGT-%s"><invocation>%s</invocation><expect>%s</expect></criterion>'
        % (c, cid, html.escape(inv, quote=False), html.escape(exp, quote=False)) for c, inv, exp in criteria)
    base = "; ".join("%s base: %s" % (c, "run at the cut, result in the group notes") for c, _i, _e in criteria)
    bound_lines = ["Write only the paths below. No deploy, no store write, no table, no schedule, no vendor, SEC or model call, no portal write.",
                   "`lib/research/api/scoped_amgt.py` is READ, never edited: the round's adapter cell, AMGT-bb-17, makes every hookup. Name yours in your report."]
    bound_lines += bounds
    bound_lines += ["Any sentence you serve to a user is in plain words. Do not use %s." % FORBIDDEN,
                    "No `bun` command of any kind in this worktree (site Z interim rule: a worktree never installs packages).",
                    "Standing: no S3 delete, no push of shared branches."]
    if cid == "bb-14":
        bound_lines[1] = "You edit the two files named in section 1 and no other file under `integrations/bloomberg/`."
    if cid in NO_ADAPTER_LINE:
        bound_lines[1] = "`lib/research/api/scoped_amgt.py` is READ, never edited."
    if cid == "bb-17":
        bound_lines[1] = ("You are the ONLY writer of `lib/research/api/scoped_amgt.py` this round. Edit no module another cell built: "
                          "if one is wrong, file a row and say so in your report.")
    if cid == "bb-23":
        bound_lines[0] = "Write only the paths below. No deploy, no build run, no store write, no vendor call, no download of any kind."
        bound_lines[1] = "`upload_verified.sh`, `content_diff.py` and every `.tf` file in the folder are READ, never edited."
    if cid == "bb-20":
        bound_lines[0] = "Write only the paths below. No deploy, no `terraform` command, no upload, no store write, no vendor call."
        bound_lines[1] = "A line-ending change and nothing else: no file's content changes once carriage returns are set aside."
    risk = RISK.get(cid, "LOCAL")
    commit = "@643863854d before the cut" if notes in ("GROUP_A_NOTES.md", "GROUP_B_NOTES.md", "GROUP_C_NOTES.md") \
        else "in the issuance commit's parent"
    bounds_md = "\n".join("%d. %s" % (i + 1, b) for i, b in enumerate(bound_lines))
    return """# AMGT_RESAPP task order -- `AMGT-{cid}` -- {title}

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>{project}/decompositions/AMGT_RESAPP_DECOMP.md</decomp_doc>
<owned_cells>AMGT-{cid}</owned_cells>
</decomp_ref>
<issued_to>{serial}</issued_to>
<issued_by>{issuer}</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no cron, alarm, monitor or cadence; a module and its tests.
comp-iam: DECLARED-NOT-APPLICABLE -- reads only what the function or the hand-run tool already reads; no new read path is granted by this cell.
comp-adversary: RUN at the cut by the issuer's drafting read ({notes}) -- {adversary} Every build criterion FAILS at the base and every bound criterion PASSES there; the literal outputs are in that file.
EGRESS CLASS, declared: NONE. No vendor, SEC or model call.
</preflight>

**Your worktree:** `{wt}` (branch `wk-AMGT_RESAPP-{slot}`, cut from the issuance commit with `--portal-ref {portal_ref}`, the portal DEV head at the cut, and no package install). Work and commit only there. Start every shell call with `cd /c/tmp/r78-{slot}`: a call that starts elsewhere resolves `git rev-parse --show-toplevel` to the base checkout.

## 1. THE ACT -- `AMGT-{cid}` (round 78, decomposition s.86)

{act}

Run the test folder your module sits in before your commit and report its last line. If a test fails only because it reads a portal file absent at this worktree's portal ref, name it in your report and file no row; the issuer grades the suite on the shared tree. **Stamp any surprise row's `surfaced_at` with `date -u +%FT%TZ` at filing.** Rows: id form `AMGT_RESAPP-Z-W{slot}-S<k>`, `disarm_owner` `{issuer}`.

## 2. BOUNDS

{bounds}

## 3. SURFACES

<paths>
{paths}
</paths>

## 4. PROOF OF SPEC (literal; timeout 900)

<proof_of_spec>
{crit}
</proof_of_spec>

## 5. WHEN YOU ARE DONE

Commit in your worktree via `.tools/safe-commit.sh --author "{serial} <{serial}@opal.agent>" -F <msgfile> -- <paths>`
(message file written with the Write tool; confirm with `git log -1`). Instance at
`{deliv}{stem}.proof_of_spec.json`.
Run `python .tools/proof-of-spec-check.py <instance>` on the committed bytes and report its verdict line. Do not stage `portal`.
Report once:
- the commit hash;
- every criterion's output lines;
- the test folder's last line;
- the hookup another cell must make for your work to be served, or that none is needed;
- anything your read of the code found that this order did not say;
- any row.

The `<status>` flip is the issuer's.

<!-- ===================== RECORD FACE -- does NOT travel to the worker ===================== -->

**ISSUER NOTES:** {record} Drafted in `deliverables/{issuer}/round78/{notes}` (cell {prefix_short}), committed {commit}. Checks dry-run at the base: {base}.

<status>pending</status>
<round>78</round>
<slot>{serial}</slot>
<fabric>site-z</fabric>
<risk>{risk}</risk>
<worker_class>{wclass}</worker_class>
""".format(cid=cid, title=title, project=PROJECT, serial=serial, issuer=ISSUER, notes=notes, adversary=adversary, wt=wt, slot=slot,
           portal_ref=portal_ref, act=act, bounds=bounds_md, paths="\n".join(paths), crit=crit_xml, deliv=deliv, stem=stem,
           record=record, risk=risk, commit=commit, prefix_short=prefix.replace("## ", ""), base=base, wclass=wclass), stem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portal-ref", required=True)
    ap.add_argument("--only", default=None)
    ap.add_argument("--out", default=ORDERS)
    a = ap.parse_args()
    n = 0
    for cell in CELLS:
        if a.only and cell[0] != a.only:
            continue
        text, stem = order_text(cell, a.portal_ref)
        bad = sum(1 for ch in text if ord(ch) > 127)
        path = os.path.join(a.out, stem + ".md")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        n += 1
        print("%-6s %-55s %6d B  criteria %d  non-ascii %d" % (cell[0], stem[-55:], len(text), text.count("<criterion "), bad))
    print("orders written: %d" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
