"""AMGT_RESAPP round 79 -- the issuer's order generator (2.0.0_SA_COO~Z).

Reads the group notes beside this file (THE ACT, THE CRITERIA and the paths block of each drafted cell) and writes one
task order per cell in the round-77 order shape. It writes files only; it commits nothing and spawns nothing.

  python cut_orders.py --portal-ref <sha> [--only cc-3] [--out <dir>]
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
    ("cc-1", "GROUP_A_NOTES.md", "## A1", "the-segment-reader-finds-a-stored-table", 308, "worker-light",
     "At the base the reader looks at five objects of a folder; AMD's table sits under later pulls and its read costs 4 bodies where 2 are needed.",
     ["You edit `lib/research/api/segment_table.py` and its test file only."],
     "CTO round-78 analysis R1 and enrichment item 1 (bb-1's residual)."),
    ("cc-2", "GROUP_A_NOTES.md", "## A2", "one-served-segment-table-with-its-labels", 309, "worker",
     "76 of 85 stored names serve rows; Period 1 ties to stored revenue on 72 and does not on 4; nothing serves the table today.",
     ["`lib/research/api/segment_table.py` and `segment_period.py` are READ, never edited: another cell edits the first."],
     "CTO round-78 analysis R1 (FWD-1); CTO ruling msg 31077 (label only where the tie holds)."),
    ("cc-3", "GROUP_B_NOTES.md", "## B1", "the-seeking-alpha-store-reader", 310, "worker",
     "105 job records in 104 folders, 105 of 105 parse; 23 of 95 covered names hold one: read 11, checked 12, no record 72.",
     ["`lib/research/freshness/collector_record.py`, the schema file and `build_view.py` are READ, never edited.",
      "Three states are kept apart: read, checked with nothing new, no record. No record is never a date and never stale (CTO msg 31672)."],
     "CTO round-78 analysis R1 (FWD-7); CTO ruling msg 31672 (serve now, read-only grant, three states)."),
    ("cc-4", "GROUP_C_NOTES.md", "## C1", "five-stored-sections-served", 311, "worker",
     "Over 95 covered names the five stored sections hold a value on 48, 18, 13, 13 and 13; no route serves any of them.",
     ["`lib/research/corpus/dossier.py` is READ, never edited. The stored text is served byte for byte: never re-worded, never trimmed."],
     "CTO ruling msg 31623 and round-78 analysis enrichment item 2."),
    ("cc-5", "GROUP_E_NOTES.md", "## E1", "the-build-side-repairs", 312, "worker",
     "At CLOUD HEAD the build's own generated-prefixes gate exits 1 (the registry hash went stale after another project's registry edits), and the function has no read grant on the job-record prefix.",
     ["You run NO `terraform` command, no `safe-apply` and no AWS write: the apply is a leg of the redeploy order under its own pair.",
      "No S3 address is typed: every prefix is the generator's output."],
     "CTO ruling msg 31672 term one (the grant); the stale gate was found by the issuer at the cut."),
    ("cc-6", "GROUP_D_NOTES.md", "## D1", "the-adapter-cell", 313, "worker",
     "At the base the three served keys are absent on every route; last round's six hookups read YES.",
     ["Every existing served key and value is unchanged: ADDED keys, and the Seeking Alpha fields the notes name as replaced."],
     "CTO round-78 analysis R1: each hookup is named, and the redeploy's pair lists them. WAVE 1: cut from the drain of cc-1 to cc-5."),
]

RISK = {"cc-5": "WORLD"}
NO_ADAPTER_LINE = ("cc-1", "cc-2", "cc-3", "cc-4", "cc-5")

FORBIDDEN = ("identity, unresolved, security key, crosswalk, dossier, landed, model block, estate, stage, input ledger or bronze")


def _section(text, start_re, stop_re):
    m = re.search(start_re, text, flags=re.M)
    if not m:
        return None
    rest = text[m.end():]
    s = re.search(stop_re, rest, flags=re.M)
    return rest[: s.start()] if s else rest


def _title(notes_path, prefix):
    text = open(notes_path, encoding="utf-8").read()
    head = re.search(r"^%s\b.*$" % re.escape(prefix), text, flags=re.M).group(0)
    return head.split(" -- ", 2)[-1].strip()


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
    n_cell = re.search(r"cc-(\d+)", head).group(1)
    for m in re.finditer(r"^- \*{0,2}(AC\d+)\b(.*?)(?=^- \*{0,2}AC\d|\Z)", crit, flags=re.M | re.S):
        cid, tail = m.group(1), m.group(2)
        em = re.search(r"Expect:\s*(.*)", tail, flags=re.S)
        if not em:
            raise SystemExit("criterion %s of %s has no Expect" % (cid, prefix))
        expect = re.sub(r"\s+", " ", em.group(1)).strip().replace("`", "").rstrip(".")
        im = re.search(r"`(cd [^`]+)`", tail[: em.start()])
        where = "deployed" if im and "--where deployed" in im.group(1) else "local"
        inv = im.group(1).strip() if im else (
            'cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "%s/deliverables/%s/round79/checks/r79_cc%s.py" '
            '--crit %s --where %s; echo "exit=$?"' % (PROJECT, ISSUER, n_cell, cid, where))
        criteria.append((cid, inv, expect))
    if not 1 <= len(criteria) <= 3:
        raise SystemExit("cell %s has %d criteria" % (prefix, len(criteria)))
    fenced = re.search(r"```\n(.*?)```", paths, flags=re.S)
    plist = [ln.strip() for ln in (fenced.group(1) if fenced else paths).splitlines() if ln.strip()]
    return act.strip("\n"), criteria, plist


def order_text(cell, portal_ref):
    cid, notes, prefix, slug, slot, wclass, adversary, bounds, record = cell
    title = _title(os.path.join(HERE, notes), prefix)
    act, criteria, plist = parse_cell(os.path.join(HERE, notes), prefix)
    serial = "0.9.0_WK_AMGT_RESAPP~%d" % slot
    wt = "C:/tmp/r79-%d" % slot
    stem = "AMGT_RESAPP.TO-AMGT-%s.%s" % (cid, slug)
    deliv = "%s/deliverables/%s/" % (PROJECT, serial)
    paths = [p for p in plist if "<worker serial>" not in p and "deliverables/0.9.0_WK" not in p and p != CHANNEL]
    paths += [deliv, CHANNEL]
    crit_xml = "\n".join(
        '  <criterion id="%s" cell_refs="AMGT-%s"><invocation>%s</invocation><expect>%s</expect></criterion>'
        % (c, cid, html.escape(inv, quote=False), html.escape(exp, quote=False)) for c, inv, exp in criteria)
    base = "; ".join("%s base: %s" % (c, "run at the cut, result in the group notes") for c, _i, _e in criteria)
    bound_lines = ["Write only the paths below. No deploy, no store write, no table, no schedule, no vendor, SEC or model call, no portal write.",
                   "`lib/research/api/scoped_amgt.py` is READ, never edited: the round's adapter cell, AMGT-cc-6, makes every hookup. Name yours in your report."]
    bound_lines += bounds
    bound_lines += ["Any sentence you serve to a user is in plain words. Do not use %s." % FORBIDDEN,
                    "No `bun` command of any kind in this worktree (site Z interim rule: a worktree never installs packages).",
                    "Standing: no S3 delete, no push of shared branches."]
    if cid in NO_ADAPTER_LINE:
        bound_lines[1] = "`lib/research/api/scoped_amgt.py` is READ, never edited."
    if cid == "cc-6":
        bound_lines[1] = ("You are the ONLY writer of `lib/research/api/scoped_amgt.py` this round. Edit no module another cell built: "
                          "if one is wrong, file a row and say so in your report.")
    if cid == "cc-5":
        bound_lines[0] = "Write only the paths below. No deploy, no build run, no store write, no vendor call, no download of any kind."
        bound_lines[1] = "`upload_verified.sh`, `content_diff.py` and every `.tf` file in the folder are READ, never edited."
    risk = RISK.get(cid, "LOCAL")
    commit = "before the cut, in the issuance commit's ancestry"
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

**Your worktree:** `{wt}` (branch `wk-AMGT_RESAPP-{slot}`, cut from the issuance commit with `--portal-ref {portal_ref}`, the portal DEV head at the cut, and no package install). Work and commit only there. Start every shell call with `cd /c/tmp/r79-{slot}`: a call that starts elsewhere resolves `git rev-parse --show-toplevel` to the base checkout.

## 1. THE ACT -- `AMGT-{cid}` (round 79, decomposition s.87)

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

**ISSUER NOTES:** {record} Drafted in `deliverables/{issuer}/round79/{notes}` (cell {prefix_short}), committed {commit}. Checks dry-run at the base: {base}.

<status>pending</status>
<round>79</round>
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
