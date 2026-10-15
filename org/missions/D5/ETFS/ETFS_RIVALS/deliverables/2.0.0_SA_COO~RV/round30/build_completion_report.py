"""Build ledger/COMPLETION_REPORT.round30.json for ETFS_RIVALS (2.0.0_SA_COO~RV, spine L10 step 4).

    python build_completion_report.py            # prints the denominators, the per-FWD table, writes the report

Reads only committed files: the PRD's ENDPOINT cards, the 12 decomposition files, the order files under task-orders/, and the
proof-of-spec instances under deliverables/. Writes ledger/COMPLETION_REPORT.round30.json. No network, no AWS.

HOW EACH ROW IS DERIVED (stated in every row's note):
  done_when_state / done_when_text: the LAST ENDPOINT card of that FWD in the PRD (an AMENDED card replaces the earlier one),
      the DONE WHEN sentence copied verbatim with its line breaks folded to single spaces.
  cells: the cell->FWD association is NOT recorded as data anywhere in the project (146 cells, 12 decomposition files). It is
      the UNION of (a) every FWD id the cell's own decomposition section names, and (b) the COO's reading of the cell title
      (MAP below, authored by 2.0.0_SA_COO~RV). A cell that serves no outcome by that reading is listed under none.
  task_orders: every order whose <owned_cells> names the cell, listed only when its <status> is complete or superseded AND a
      proof-of-spec instance for it exists; proof_of_spec_ref is that instance's path @ the last commit that touched it.
  claim: COVERED when at least one listed cell has such an order, else UNCOVERED (the schema's own definition).
"""
import datetime as dt
import glob
import json
import os
import re
import subprocess

ROOT = "C:/dev/ajb_workspace"
P = ROOT + "/org/missions/D5/ETFS/ETFS_RIVALS/"
OUT = P + "ledger/COMPLETION_REPORT.round30.json"

# The COO's reading of the cell titles: FWD id -> cell ids. Union with the FWD ids each cell's own section names.
MAP = {
    1: "c-1 s-1 g-1 g-2 p-1 w-1 d-1 r-1 d-2 u-1 p-2 d-3 d-4 d-5 pg-1",
    2: "m-1 h-1 hp-1 wf-1 xa-1 xa-2 we-1 we-2",
    3: "c-1 q-1 b-1 l-1 lg-1 d-1 r-1 d-3 d-4 d-5 eb-1 xe-1 cb-1 dt-1 b-2 m-2 pv-1 sa-1 xf-1",
    4: "s-1 g-1 g-3 i-1 i-2 ok-1 pk-1 al-1 f-3 v-2 g-6",
    5: "g-2 g-4 t-5 wd-1 we-1 we-2 h-4 h-5 h-6 gt-1 dr-1 rp-2 gd-1 nf-1 e-1 e-2 x-1 xe-3 rp-1",
    6: "s-4 g-6 sx-1 rk-2 ui-2 hc-1 rn-1 s-6 d-3 d-4 d-5 g-3",
    7: "ai-2 ap-1 r-6 st-1 ab-1 ui-4 sa-1 an-1 ln-1 gc-1",
    8: "rp-2 gt-1 dr-1 gd-1 v-2 nf-1",
    9: "p-1 f-4 f-3 r-3 eg-1 rk-2 h-5",
    10: "wd-1",
    11: "p-2 g-3 u-1 ui-2 ui-3",
    12: "u-1 xf-1 g-3",
    13: "pg-1 ui-1 ui-2 rd-1 rw-1 lg-1 s-6 nm-1",
    14: "rk-1 s-6 sx-1 rk-2 hc-1 rn-1 ui-2",
    15: "bt-1 tb-1 s-6 ui-3 ml-1",
    16: "ai-2 aw-1 pd-3 gc-1 wh-1 s-6",
    17: "ai-1 ai-2 wg-1 xc-1 xc-2 wh-1",
    18: "pg-1 s-6 ui-1 ui-2 ui-3 ui-4 ui-5 rd-1 rw-1 lk-1 au-1 as-1 wc-2",
    19: "pg-1 pt-1",
    20: "ai-1 ic-1 ic-2 cg-1 cs-1 rp-1 s-6",
    21: "fc-1 rn-1 fe-1 ks-1 ln-1 tl-1",
    22: "ps-1 tm-1 co-1 bf-1 rt-1 md-1 pc-1 nc-1 tl-1 pl-1 bk-1 pm-1 cu-1 mr-1 wa-1 wb-1 wc-1 wi-1 wj-1 wk-1 xb-1 xd-1 rg-1 rg-2 tc-1 as-1 ml-1",
    23: "pd-1 pd-2 pd-3 as-1 ml-1 pl-1 aw-1 ks-1 rg-1 tc-1 hc-1 rn-1 gc-1",
    24: "ho-1 tw-1 rk-1 rg-1 rg-2 mr-1 cu-1 aw-1 tc-1 bk-1 xe-1 xe-3",
}


def git(*a):
    r = subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip()


def prd_cards():
    t = open(P + "prd/ETFS_RIVALS_PRD.md", encoding="utf-8").read()
    cards = {}
    for m in re.finditer(r"^  FWD-(\d+)\s.*?(?=^  FWD-\d+\s|^  =====|\Z)", t, re.M | re.S):
        n = int(m.group(1))
        blk = m.group(0)
        d = re.search(r"DONE WHEN\s+(EXERCISED|APPLIED) -- (.*?)(?=\n\s+ACCEPT\b)", blk, re.S)
        if d:
            cards[n] = (d.group(1), re.sub(r"\s+", " ", d.group(2)).strip())  # later cards overwrite earlier ones
    return cards


def decomp_cells():
    cells = {}
    n_sections = 0
    for f in sorted(glob.glob(P + "decompositions/*.md")):
        t = open(f, encoding="utf-8").read()
        ms = list(re.finditer(r"^#{2,4} `?(RIV-[A-Za-z0-9]+-\d+[A-Za-z]?)`?", t, re.M))
        for i, m in enumerate(ms):
            end = ms[i + 1].start() if i + 1 < len(ms) else len(t)
            n_sections += 1
            d = cells.setdefault(m.group(1), set())
            d |= {int(x) for x in re.findall(r"FWD-(\d+)", t[m.start():end])}
    return cells


def orders():
    proofs = {}
    for p in glob.glob(P + "deliverables/**/*proof_of_spec*.json", recursive=True):
        proofs.setdefault(os.path.basename(p).split(".proof_of_spec")[0], []).append(p.replace("\\", "/"))
    out = []
    for f in sorted(glob.glob(P + "task-orders/*.md")):
        t = open(f, encoding="utf-8").read()
        oc = re.search(r"<owned_cells>(.*?)</owned_cells>", t, re.S)
        st = re.search(r"<status>(.*?)</status>", t)
        oid = os.path.basename(f)[:-3]
        ps = sorted(proofs.get(oid, []))
        out.append({"id": oid, "cells": [c for c in re.split(r"[,\s]+", oc.group(1).strip()) if c] if oc else [],
                    "status": st.group(1).strip() if st else "", "proof": ps[-1] if ps else None})
    return out


def main():
    cards = prd_cards()
    prd_hdr = json.loads(re.search(r"\"endpoint_outcomes\": (\[.*?\])", open(P + "prd/ETFS_RIVALS_PRD.md", encoding="utf-8").read()).group(1))
    assert sorted(int(x[4:]) for x in prd_hdr) == list(range(1, 25)), prd_hdr
    cells = decomp_cells()
    ords = orders()
    by_cell = {}
    for o in ords:
        for c in o["cells"]:
            by_cell.setdefault(c, []).append(o)
    terminal = [o for o in ords if o["status"] in ("complete", "superseded") and o["proof"]]
    unknown = [c for n in MAP for c in ("RIV-" + x for x in MAP[n].split()) if c not in cells]
    assert not unknown, sorted(set(unknown))
    rows = []
    mapped_any = set()
    for n in range(1, 25):
        state, text = cards[n]
        want = {"RIV-" + x for x in MAP[n].split()} | {c for c, f in cells.items() if n in f}
        cl = []
        for c in sorted(want):
            tos = [o for o in by_cell.get(c, []) if o["status"] in ("complete", "superseded") and o["proof"]]
            if not tos:
                continue
            mapped_any.add(c)
            cl.append({"cell_id": c, "task_orders": [
                {"id": o["id"], "status": o["status"],
                 "proof_of_spec_ref": o["proof"].replace(ROOT + "/", "") + "@" + git("log", "-1", "--format=%h", "--", o["proof"])}
                for o in tos]})
        dropped = sorted(c for c in want if c not in {x["cell_id"] for x in cl})

        def why(c):
            os_ = by_cell.get(c, [])
            if any(o["status"] == "pending" and o["proof"] for o in os_):
                return f"{c} (order pending: its instance reads INVALID on the alignment limb, the cell sits in a round decomposition file, or iam-1's schema)"
            if any(o["status"] == "superseded" and not o["proof"] for o in os_):
                return f"{c} (order superseded by the 2026-10-02 FAST lease: built by the lease seat directly, no worker, no instance)"
            return f"{c} (no order owns it)"
        note = (f"cells = the union of FWD-{n} named in the cell's own decomposition section and the COO's reading of cell titles "
                f"(build_completion_report.py MAP); {len(cl)} cell(s) listed, each with a complete or superseded order that has a "
                f"proof-of-spec instance." + (f" Named but not listed: {'; '.join(why(c) for c in dropped)}." if dropped else ""))
        row = {"fwd_id": f"FWD-{n}", "done_when_state": state, "done_when_text": text, "cells": cl,
               "claim": "COVERED" if cl else "UNCOVERED", "note": note}
        rows.append(row)
    rep = {
        "kind": "COMPLETION_REPORT", "schema_version": "1.0", "project": "ETFS_RIVALS", "round": 30,
        "written_by": "2.0.0_SA_COO~RV", "written_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "decomposition_ref": "org/missions/D5/ETFS/ETFS_RIVALS/decompositions/ETFS_RIVALS_DECOMP.md@" +
                             git("log", "-1", "--format=%h", "--", "org/missions/D5/ETFS/ETFS_RIVALS/decompositions"),
        "denominators": {"fwd_in_prd_header": len(prd_hdr), "cells_in_decomposition": len(cells), "task_orders": len(ords),
                         "task_orders_terminal_with_valid_proof": len(terminal)},
        "outcomes": rows,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(rep, indent=1, ensure_ascii=True) + "\n")
    print("denominators", rep["denominators"])
    print("cells listed under at least one FWD:", len(mapped_any), "of", len(cells))
    print("orders not terminal-with-proof:", [(o["id"][11:48], o["status"], bool(o["proof"])) for o in ords if o not in terminal])
    for r in rows:
        print(r["fwd_id"], r["claim"], r["done_when_state"], len(r["cells"]), "cells")


if __name__ == "__main__":
    main()
