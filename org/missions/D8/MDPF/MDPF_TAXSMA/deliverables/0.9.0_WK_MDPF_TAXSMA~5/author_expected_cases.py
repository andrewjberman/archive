#!/usr/bin/env python3
"""MDPF_TAXSMA TX-v-1 -- author the independent expected-case manifest (PRD s.4, A01-A08).

Writes data/mdpf/tests/taxsma/expected_cases.json.

INDEPENDENCE: standard library only. This script imports no TAXSMA engine module (nothing under
data/mdpf/scripts/**, infra/aws/ec2/opal-gateway/app/** or infra/aws/lambda/**). Every expectation
is derived from the PRD and data-contract TEXT, read at pinned commits through `git show`, never
from the code under test. Every expected number is worked by Decimal arithmetic into the
manifest's `ledger`, and every expected observable refers to a number only as {"num": <ledger id>}.

Usage: py -3.12 author_expected_cases.py [--out PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from decimal import Decimal
from pathlib import Path

PRD_PATH = "org/missions/D8/MDPF/MDPF_TAXSMA/prd/MDPF_TAXSMA_PRD.md"
PRD_COMMIT = "671925aecc"
CONTRACT_PATH = "org/standards/MDPF_TAXSMA_DATA_CONTRACT.json"
CONTRACT_COMMIT = "91b11ff0c9"
DECOMP_PATH = "org/missions/D8/MDPF/MDPF_TAXSMA/decompositions/MDPF_TAXSMA_DECOMP.md"
DECOMP_COMMIT = "7f65001ab3"
TO_PATH = "org/missions/D8/MDPF/MDPF_TAXSMA/task-orders/MDPF_TAXSMA.TO-TX-v-1.expected-cases.md"
OUT_REL = "data/mdpf/tests/taxsma/expected_cases.json"
GENERATOR_REL = "org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~5/author_expected_cases.py"

TWO = Decimal("0.01")


def repo_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(Path(__file__).resolve().parent),
                         capture_output=True, check=True)
    return Path(out.stdout.decode("utf-8").strip())


def git_show(root: Path, commit: str, path: str) -> str:
    out = subprocess.run(["git", "-C", str(root), "show", f"{commit}:{path}"], capture_output=True, check=True)
    return out.stdout.decode("utf-8")


# ---------------------------------------------------------------- PRD s.4 clause segmentation
ROW_RE = re.compile(r"^\| (A0[1-8]) [^|]*\| (FWD-\d) \| (.*) \|\s*$", re.M)
SEGMENTATION_RULE = ("Each PRD s.4 table row's third cell is split into sentences at whitespace that follows a "
                     "period and precedes a capital letter, then each sentence at '; '; outer whitespace and a "
                     "trailing period are stripped. Clause ids are <property>.c<n> in reading order.")


def prd_clauses(text: str) -> dict:
    out = {}
    for pid, fwd, cell in ROW_RE.findall(text):
        clauses = []
        for sent in re.split(r"(?<=\.)\s+(?=[A-Z])", cell.strip()):
            for c in sent.split("; "):
                c = c.strip().rstrip(".")
                if c:
                    clauses.append(c)
        out[pid] = {"outcome": fwd, "clauses": clauses}
    return out


# ---------------------------------------------------------------- ledger (Decimal, worked)
def rend(d: Decimal, unit: str) -> str:
    s = format(d.quantize(TWO), "f") if unit == "USD" else str(int(d))
    return f"({s})" if d < 0 else s


class Ledger:
    def __init__(self, amounts: dict):
        self.amounts = amounts
        self.entries: list = []
        self.by_id: dict = {}

    def _val(self, t: str) -> Decimal:
        if t in self.amounts:
            return Decimal(self.amounts[t]["value"])
        if t in self.by_id:
            return Decimal(self.by_id[t]["result"])
        raise KeyError(t)

    def _put(self, e: dict) -> None:
        if e["id"] in self.by_id or e["id"] in self.amounts:
            raise ValueError("duplicate ledger id " + e["id"])
        self.entries.append(e)
        self.by_id[e["id"]] = e

    def sum(self, lid: str, unit: str, terms: list, meaning: str) -> None:
        vals = [self._val(t) for t in terms]
        r = sum(vals, Decimal("0"))
        res = format(r.quantize(TWO), "f") if unit == "USD" else str(int(r))
        worked = " + ".join(rend(v, unit) for v in vals) + " = " + res
        self._put({"id": lid, "op": "sum", "unit": unit, "terms": terms, "result": res, "worked": worked,
                   "meaning": meaning})

    def sub(self, lid: str, unit: str, terms: list, meaning: str) -> None:
        vals = [self._val(t) for t in terms]
        r = vals[0]
        for v in vals[1:]:
            r = r - v
        res = format(r.quantize(TWO), "f") if unit == "USD" else str(int(r))
        worked = " - ".join(rend(v, unit) for v in vals) + " = " + res
        self._put({"id": lid, "op": "sub", "unit": unit, "terms": terms, "result": res, "worked": worked,
                   "meaning": meaning})

    def count(self, lid: str, members: list, meaning: str) -> None:
        n = len(set(members))
        worked = "count_distinct(" + ", ".join(members) + ") = " + str(n)
        self._put({"id": lid, "op": "count_distinct", "unit": "count", "members": members, "result": str(n),
                   "worked": worked, "meaning": meaning})


def N(lid: str) -> dict:
    return {"num": lid}


# ---------------------------------------------------------------- synthetic fixture world
# Every account-shaped token is drawn from the reserved synthetic block: eight digits beginning 99
# (full canonical form 0099xxxxxx). Master identities are referenced by contract path, never by digits.
KEYS = {
    "K1": ("99000001", "Traded=Yes; long plus cash; BD ACTIVE"),
    "K2": ("99000002", "Traded=Yes, Ready=No; long/short; BD PENDING_RESOLUTION; the account most arms perturb"),
    "K3": ("9900-0003", "Traded=Yes; margin debit; hyphen form in the workbook; BD absent"),
    "K4": ("99000004", "funded-but-untraded: Traded=No with a custodian value"),
    "K5": ("99000005", "new Traded=Yes discovered after the bootstrap snapshot"),
    "K6": ("99000006", "retained Traded=No history, later Traded=Yes"),
    "K7": ("99000007", "Traded=No account that a disposition tries to activate"),
    "K8": ("99000008", "custodian Tax-labelled candidate with no workbook claim"),
    "K9": ("99000009", "rekey / transfer target of K2"),
    "K20": ("99000020", "base (non-Tax) population member"),
    "K21": ("99000021", "base (non-Tax) population member"),
}


def full_key(raw: str) -> str:
    return "00" + raw.replace("-", "")


AMOUNTS_SPEC = [
    ("AMT-K1-NET", "1500000.25", "K1 canonical net_mv_plus_cash, every fixture business date"),
    ("AMT-K1-LONG", "1450000.00", "K1 long market value (trace only)"),
    ("AMT-K1-SHORT", "0.00", "K1 short market value (trace only)"),
    ("AMT-K1-CASH", "50000.25", "K1 cash (trace only)"),
    ("AMT-K2-NET", "820000.10", "K2 canonical net_mv_plus_cash, every fixture business date"),
    ("AMT-K2-LONG", "1000000.00", "K2 long market value (trace only)"),
    ("AMT-K2-SHORT", "-250000.00", "K2 short market value, negative (trace only)"),
    ("AMT-K2-CASH", "70000.10", "K2 cash (trace only)"),
    ("AMT-K3-NET", "360000.05", "K3 canonical net_mv_plus_cash, every fixture business date"),
    ("AMT-K3-LONG", "600000.00", "K3 long market value (trace only)"),
    ("AMT-K3-SHORT", "0.00", "K3 short market value (trace only)"),
    ("AMT-K3-CASH", "-239999.95", "K3 cash, a margin debit (trace only)"),
    ("AMT-K4-NET", "400000.00", "K4 canonical value: funded but untraded, never a contribution"),
    ("AMT-K5-NET", "275000.15", "K5 canonical value"),
    ("AMT-K6-NET", "190000.20", "K6 canonical value"),
    ("AMT-K7-NET", "150000.00", "K7 canonical value"),
    ("AMT-K8-NET", "510000.00", "K8 canonical value (candidate)"),
    ("AMT-K9-NET", "820000.10", "K9 canonical value (transfer target of K2)"),
    ("AMT-ZERO", "0.00", "an actual zero reported by the canonical source (A04 zero case)"),
    ("AMT-K2-NET-RESTATED", "820500.10", "K2 canonical value restated the same day (A08 correction)"),
    ("AMT-K2-GROSS-EXPOSURE", "1250000.00", "K2 gross long plus absolute short exposure in the holdings fixture"),
    ("AMT-K2-SALES-EST-USD", "4500000.00", "K2 workbook AUM (Mn) 4.5 read as dollars: the sales estimate"),
    ("AMT-K2-BD-QUARTERLY", "790000.00", "K2 Black Diamond quarterly value"),
    ("AMT-K2-ACCRUAL-PLACEHOLDER", "0.00", "K2 accrued_income placeholder (PENDING-RULING)"),
    ("AMT-K2-ACCRUAL-UNVERIFIED", "1500.00", "K2 unverified accrual candidate that must not be added"),
    ("AMT-49F-BASE", "41000000.00", "49financial base_excluding_tax_aua (includes Client and every non-Tax member)"),
    ("AMT-49F-CLIENT", "9000000.00", "49financial Client residual inside the base"),
    ("AMT-49F-SMA-OTHER", "3000000.00", "49financial SMA members other than Tax-Managed SMA"),
    ("AMT-49F-ALT-OTHER", "3500000.00", "49financial ALT Strategies members other than SMA"),
    ("AMT-OF1-TOTAL", "12000000.00", "other_firm_1 complete total"),
    ("AMT-OF2-TOTAL", "7500000.00", "other_firm_2 complete total"),
]
SALES_ESTIMATES_MN = ["1.5", "4.5", "0.4", "0.5", "2.0", "8.9"]
TRADED_READY_VALUES = ["Yes", "No", "", "Maybe"]

def slot(rn: int, index, acct: str, n: int, strategy: str, aum: str, ready: str, incep: str, last: str,
         traded: str, headers: list) -> dict:
    cells = {h: "" for h in headers}
    cells.update({"Index": index, "Account Number": acct, "Strategy": strategy, "AUM (Mn)": aum, "Ready": ready,
                  "Inception Date": incep, "Last Trade Date": last, "Traded": traded})
    if acct or strategy or aum or ready or traded:
        cells.update({"Name": f"SYNTH-NAME-{n:02d}", "Advisor Contact": f"SYNTH-ADVISOR-{n:02d}",
                      "Leverage": f"SYNTH-LEVERAGE-{n:02d}", "Divest Securities": f"SYNTH-DIVEST-{n:02d}",
                      "Instruction": f"SYNTH-INSTRUCTION-{n:02d}", "Comment": f"SYNTH-COMMENT-{n:02d}"})
    return {"row": f"r{rn}", "row_number": rn, "cells": cells}


def build_world(contract: dict) -> tuple:
    wb = contract["workbook"]
    headers = list(wb["expected_headers_after_outer_whitespace_trim"])
    amounts = {a: {"value": v, "unit": "USD", "synthetic": True, "role": r} for a, v, r in AMOUNTS_SPEC}
    tax = "SYNTH-TAX-STRATEGY"
    base_rows = [
        slot(2, 1, "99000001", 1, tax, "1.5", "Yes", "2026-08-03", "2026-09-11", "Yes", headers),
        slot(3, 2, "99000002", 2, tax, "4.5", "No", "2026-08-10", "2026-09-10", "Yes", headers),
        slot(4, 3, "9900-0003", 3, tax, "0.4", "Yes", "2026-08-17", "2026-09-09", "Yes", headers),
        slot(5, 4, "99000004", 4, tax, "0.5", "Yes", "", "", "No", headers),
        slot(6, 5, "", 5, tax, "2.0", "", "", "", "", headers),
        slot(7, 6, "", 6, "", "", "", "", "", "", headers),
        {"row": "r8", "row_number": 8, "cells": dict({h: "" for h in headers}, **{"Index": "Total", "AUM (Mn)": "8.9"})},
    ]
    base_rows[4]["cells"]["Account Number"] = ""
    full_rows = [dict(r) for r in base_rows[:6]]
    full_rows.append(slot(8, 7, "99000002", 7, tax, "4.5", "No", "2026-08-10", "2026-09-10", "Yes", headers))
    full_rows.append({"row": "r9", "row_number": 9, "cells": dict({h: "" for h in headers},
                                                                   **{"Index": "Total", "AUM (Mn)": "8.9"})})
    val = {k: {"net_mv_plus_cash": amounts[f"AMT-{k}-NET"]["value"], "amount_id": f"AMT-{k}-NET"}
           for k in ("K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8")}
    fixtures = {
        "keys": {k: {"raw": raw, "full": full_key(raw), "role": role} for k, (raw, role) in KEYS.items()},
        "synthetic_key_block": "every account-shaped token begins 99 (eight digits) or 0099 (ten digits); "
                               "hyphen forms begin 99; malformed probes derive from these keys",
        "WB-BASE": {"kind": "full-sheet workbook", "sheet": "Sheet1", "item": "CONTRACT:workbook.item_id",
                    "headers": headers, "used_rows_including_header": 8, "rows": base_rows,
                    "row_roles": {"r2": "traded K1", "r3": "traded K2 (Ready=No)", "r4": "traded K3 (hyphen form)",
                                  "r5": "funded-but-untraded K4", "r6": "prospect (no account)",
                                  "r7": "blank indexed slot", "r8": "Total marker row"}},
        "WB-FULL": {"kind": "full-sheet workbook", "sheet": "Sheet1", "item": "CONTRACT:workbook.item_id",
                    "headers": headers, "used_rows_including_header": 9, "rows": full_rows,
                    "row_roles": {"r2": "traded K1", "r3": "traded K2", "r4": "traded K3", "r5": "funded-but-untraded K4",
                                  "r6": "prospect", "r7": "blank", "r8": "conflict: duplicate full key K2, same Yes",
                                  "r9": "Total marker row"}},
        "SNAP-S0": {"workbook": "WB-BASE", "observed_at": "2026-09-14T13:30:00Z",
                    "role": "first accepted complete observation; the history boundary is 2026-09-14"},
        "SNAP-S1": {"workbook": "WB-BASE", "observed_at": "2026-09-15T13:30:00Z"},
        "SNAP-S2": {"workbook": "WB-BASE", "observed_at": "2026-09-16T13:30:00Z"},
        "SNAP-S3": {"workbook": "WB-BASE", "observed_at": "2026-09-17T13:30:00Z"},
        "SNAP-S4": {"workbook": "WB-BASE", "observed_at": "2026-09-18T13:30:00Z"},
        "CAN-BASE": {"kind": "b00 canonical_valuation rows (IN_CLIENT_BOOK)", "keys": ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8"],
                     "business_dates": ["2026-09-11", "2026-09-14", "2026-09-15", "2026-09-16", "2026-09-17",
                                        "2026-09-18", "2026-09-21"],
                     "value_by_key": val, "boundary_version": "SYNTH-B00-BOUNDARY-1",
                     "schema_version": "SYNTH-B00-SCHEMA-1", "source_pipeline": "SYNTH-B00",
                     "_ingested_at": "equal to business_date", "accrual_status": "PENDING-RULING",
                     "note": "one row per key per business date, the key's value constant across dates"},
        "BAL-BASE": {"kind": "dim_balance components, trace only",
                     "K1": {"long_market_value": "1450000.00", "short_market_value": "0.00", "cash": "50000.25"},
                     "K2": {"long_market_value": "1000000.00", "short_market_value": "-250000.00", "cash": "70000.10"},
                     "K3": {"long_market_value": "600000.00", "short_market_value": "0.00", "cash": "-239999.95"}},
        "SUB-BASE": {"kind": "rejected substitutes present beside the canonical value",
                     "K2": {"gross_exposure": "1250000.00", "workbook_aum_mn": "4.5", "sales_estimate_usd": "4500000.00",
                            "bd_quarterly_value": "790000.00", "accrued_income_placeholder": "0.00",
                            "accrued_income_unverified": "1500.00"}},
        "CUS-BASE": {"kind": "0833 fact_acc custodian records",
                     "records": {k: {"master_ref": "CONTRACT:identity.reporting_master", "strategy": tax,
                                     "custodian_status": "SYNTH-OPEN", "partition": "SYNTH-FACTACC-PARTITION-A"}
                                 for k in ("K1", "K2", "K3", "K4", "K8")}},
        "POP-BASE": {"kind": "base (non-Tax) dated population under CONTRACT:identity.base_master_control",
                     "members": ["K20", "K21"]},
        "BD-BASE": {"kind": "existing BD roster, technical axis only", "K1": "ACTIVE", "K2": "PENDING_RESOLUTION"},
        "CAT-BASE": {"kind": "category baseline", "registry": {"member_id": "tax", "member": "Tax-Managed SMA",
                                                               "parent": "SMA", "root": "ALT Strategies",
                                                               "source_basis": "ADDITIVE"},
                     "49financial": {"base_excluding_tax_aua": "41000000.00", "client": "9000000.00",
                                     "sma_other": "3000000.00", "alt_other": "3500000.00"},
                     "other_firm_1": {"total": "12000000.00"}, "other_firm_2": {"total": "7500000.00"},
                     "note": "other_firm_1/2 stand for whichever non-49financial firms the harness's Global fixture holds"},
        "CAL-BASE": {"kind": "canonical exchange calendar sessions", "sessions": ["2026-09-11", "2026-09-14",
                     "2026-09-15", "2026-09-16", "2026-09-17", "2026-09-18", "2026-09-21"],
                     "non_sessions": ["2026-09-19", "2026-09-20"],
                     "rule": "a Gold run at 13:30 UTC on knowledge date X values the latest session strictly before X"},
        "GW-BASE": {"kind": "synthetic Gateway", "route": "CONTRACT:capability.route", "method": "GET",
                    "configured_identity": {"tid": "SYNTH-TID-A", "oid": "SYNTH-OID-A",
                                            "designation": "CONTRACT:capability.named_identity"},
                    "route_bearer": "SYNTH-CAPABILITY-BEARER-A", "delegated_token": "SYNTH-DELEGATED-TOKEN-A",
                    "generic_credentials": {"MCP": "SYNTH-MCP-CRED", "ms-ingest": "SYNTH-MSINGEST-CRED",
                                            "OTP": "SYNTH-OTP-CRED"},
                    "generic_route": "/ms/SYNTH-GENERIC", "graph": "synthetic Graph serving WB-BASE with stable ETag"},
        "sales_estimates_mn": SALES_ESTIMATES_MN,
        "traded_ready_values": TRADED_READY_VALUES,
    }
    led = Ledger(amounts)
    for k in ("K1", "K2", "K3"):
        led.sum(f"L-{k}-NET-IDENTITY", "USD", [f"AMT-{k}-LONG", f"AMT-{k}-SHORT", f"AMT-{k}-CASH"],
                f"{k} long + short + cash, equal to its canonical net_mv_plus_cash")
    for k in ("K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9"):
        led.sum(f"L-{k}-VALUE", "USD", [f"AMT-{k}-NET"], f"{k} expected value_usd: the canonical value, to the cent")
    led.sum("L-ZERO-VALUE", "USD", ["AMT-ZERO"], "an account value the source reports as an actual zero")
    led.sub("L-K2-GROSS-EXPOSURE", "USD", ["AMT-K2-LONG", "AMT-K2-SHORT"], "K2 long + |short|: the rejected gross exposure")
    led.sum("L-K2-SALES-EST", "USD", ["AMT-K2-SALES-EST-USD"], "the rejected sales estimate")
    led.sum("L-K2-BD-QUARTERLY", "USD", ["AMT-K2-BD-QUARTERLY"], "the rejected quarterly value")
    led.sum("L-K2-WITH-ACCRUAL-WRONG", "USD", ["AMT-K2-NET", "AMT-K2-ACCRUAL-UNVERIFIED"], "K2 plus an unverified accrual: forbidden")
    led.sum("L-TAX-D14", "USD", ["AMT-K1-NET", "AMT-K2-NET", "AMT-K3-NET"], "complete Tax for K1, K2, K3 on any fixture date")
    led.sum("L-TAX-WITH-K4-WRONG", "USD", ["L-TAX-D14", "AMT-K4-NET"], "Tax wrongly including funded-untraded K4")
    led.sum("L-TAX-WITH-K8", "USD", ["L-TAX-D14", "AMT-K8-NET"], "Tax including K8: correct only once K8 carries Traded=Yes")
    led.sum("L-SUBTOTAL-K1-K3", "USD", ["AMT-K1-NET", "AMT-K3-NET"], "confirmed subtotal while K2 is unresolved")
    led.sum("L-SUBTOTAL-K1-K2", "USD", ["AMT-K1-NET", "AMT-K2-NET"], "confirmed subtotal while K3 is unresolved")
    led.sum("L-TAX-K1-ZERO", "USD", ["AMT-ZERO", "AMT-K2-NET", "AMT-K3-NET"], "complete Tax when K1 reports an actual zero")
    led.sum("L-TAX-WITH-K5", "USD", ["L-TAX-D14", "AMT-K5-NET"], "complete Tax once K5 is an observed member")
    led.sum("L-TAX-WITH-K6", "USD", ["L-TAX-D14", "AMT-K6-NET"], "complete Tax once K6 is an observed member")
    led.sum("L-TAX-K1-K3", "USD", ["AMT-K1-NET", "AMT-K3-NET"], "complete Tax after K2 is explicitly inactive")
    led.sum("L-TAX-K9", "USD", ["AMT-K1-NET", "AMT-K9-NET", "AMT-K3-NET"], "Tax with K9 in K2's place")
    led.sum("L-TAX-RESTATED", "USD", ["AMT-K1-NET", "AMT-K2-NET-RESTATED", "AMT-K3-NET"], "Tax after the K2 restatement")
    led.sub("L-RESTATEMENT-DELTA", "USD", ["AMT-K2-NET-RESTATED", "AMT-K2-NET"], "the K2 restatement")
    led.sum("L-TAX-DOUBLED-WRONG", "USD", ["L-TAX-D14", "L-TAX-D14"], "a duplicate invocation's doubled Tax: forbidden")
    led.sub("L-ZERO-DIFF", "USD", ["AMT-K1-NET", "AMT-K1-NET"], "the per-account difference bar against the canonical value")
    led.sum("L-SMA-BEFORE", "USD", ["AMT-49F-SMA-OTHER"], "SMA before the Tax contribution")
    led.sum("L-SMA-AFTER", "USD", ["AMT-49F-SMA-OTHER", "L-TAX-D14"], "SMA with Tax added once")
    led.sum("L-ALT-BEFORE", "USD", ["AMT-49F-SMA-OTHER", "AMT-49F-ALT-OTHER"], "ALT Strategies before the Tax contribution")
    led.sum("L-ALT-AFTER", "USD", ["L-ALT-BEFORE", "L-TAX-D14"], "ALT Strategies with Tax added once")
    led.sum("L-49F-BEFORE", "USD", ["AMT-49F-BASE"], "49financial before the Tax contribution")
    led.sum("L-49F-AFTER", "USD", ["AMT-49F-BASE", "L-TAX-D14"], "49financial = base_excluding_tax + complete_tax, once")
    led.sum("L-CLIENT", "USD", ["AMT-49F-CLIENT"], "49financial Client, unchanged")
    led.sum("L-OF1", "USD", ["AMT-OF1-TOTAL"], "other_firm_1, unchanged")
    led.sum("L-OF2", "USD", ["AMT-OF2-TOTAL"], "other_firm_2, unchanged")
    led.sum("L-GLOBAL-BEFORE", "USD", ["AMT-49F-BASE", "AMT-OF1-TOTAL", "AMT-OF2-TOTAL"], "Global before the Tax contribution")
    led.sum("L-GLOBAL-AFTER", "USD", ["L-49F-AFTER", "AMT-OF1-TOTAL", "AMT-OF2-TOTAL"], "Global = sum of completed firm totals, once")
    led.sum("L-GLOBAL-TAX-LEAF", "USD", ["L-TAX-D14"], "Global Tax leaf = sum of firm Tax leaves (only 49financial carries one)")
    for nm, a, b in (("SMA", "L-SMA-AFTER", "L-SMA-BEFORE"), ("ALT", "L-ALT-AFTER", "L-ALT-BEFORE"),
                     ("49F", "L-49F-AFTER", "L-49F-BEFORE"), ("GLOBAL", "L-GLOBAL-AFTER", "L-GLOBAL-BEFORE")):
        led.sub(f"L-{nm}-DELTA", "USD", [a, b], f"{nm} after minus before: exactly one Tax")
    for nm, a in (("CLIENT", "AMT-49F-CLIENT"), ("OF1", "AMT-OF1-TOTAL"), ("OF2", "AMT-OF2-TOTAL")):
        led.sub(f"L-{nm}-DELTA", "USD", [a, a], f"{nm} after minus before: unchanged")
    led.sum("L-GLOBAL-DOUBLE-ADD-WRONG", "USD", ["L-GLOBAL-AFTER", "L-TAX-D14"], "Global with Tax added a second time: forbidden")
    led.sum("L-49F-DOUBLE-ADD-WRONG", "USD", ["L-49F-AFTER", "L-TAX-D14"], "49financial with Tax added a second time: forbidden")
    counts = {
        "N-NONE": [], "N-K1K2K3": ["K1", "K2", "K3"], "N-K1K2K3K4": ["K1", "K2", "K3", "K4"],
        "N-K1K2K3-DUP": ["K1", "K2", "K3", "K2"], "N-K1K2K3K5": ["K1", "K2", "K3", "K5"],
        "N-K1K2K3K6": ["K1", "K2", "K3", "K6"], "N-K1K2K3K8": ["K1", "K2", "K3", "K8"],
        "N-K2-CLOSE-EVENTS": ["OBSERVE_TRADED:K2@2026-09-14", "OBSERVE_INACTIVE:K2@2026-09-16"],
        "N-K1K2K3K7": ["K1", "K2", "K3", "K7"],
        "N-K1K3": ["K1", "K3"], "N-K1K2": ["K1", "K2"], "N-K2": ["K2"], "N-K3": ["K3"], "N-K5": ["K5"],
        "N-K6": ["K6"], "N-K8": ["K8"], "N-K1K9K3": ["K1", "K9", "K3"],
        "N-K2-ROWS": ["r3", "r8"], "N-MALFORMED-CLAIM": ["r3-claim"],
        "N-HEADERS": headers, "N-PROJECTED": list(wb["projected_columns"]), "N-ROW-META": list(wb["row_metadata"]),
        "N-RESPONSE-FIELDS": list(contract["capability"]["response_fields"]),
        "N-AUDIT-FIELDS": list(contract["capability"]["audit_fields"]),
        "N-BASE-SHIPPED-ROWS": ["r2", "r3", "r4", "r5", "r6", "r7", "r8"],
        "N-FULL-SHIPPED-ROWS": ["r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"],
        "N-INSERTED-SHIPPED-ROWS": ["r2", "r3", "r4", "r5", "r6", "r7", "r8", "ins-blank", "ins-prospect"],
        "N-S0-EVENTS": ["OBSERVE_TRADED:K1", "OBSERVE_TRADED:K2", "OBSERVE_TRADED:K3", "OBSERVE_INACTIVE:K4"],
        "N-S0-EVENTS-PLUS-ONE": ["OBSERVE_TRADED:K1", "OBSERVE_TRADED:K2", "OBSERVE_TRADED:K3",
                                 "OBSERVE_INACTIVE:K4", "OBSERVE_TRADED:K4"],
        "N-K2-REACTIVATION-EVENTS": ["OBSERVE_TRADED:K2@2026-09-14", "OBSERVE_INACTIVE:K2@2026-09-16",
                                     "OBSERVE_TRADED:K2@2026-09-18"],
        "N-SAMEDAY-EVENTS": ["K2@2026-09-16T09:00:00Z", "K2@2026-09-16T15:00:00Z"],
        "N-ONE-LEAF": ["leaf-1"], "N-TWO-LEAVES": ["leaf-1", "leaf-2"],
        "N-ONE-OBJECT": ["date=2026-09-15/data.parquet"], "N-TWO-OBJECTS": ["date=2026-09-15/data.parquet", "second same-date leaf"],
        "N-ONE-WRITER": ["opal-assets-mdpf-portal-publisher"],
        "N-OLD-NEW-OBS": ["obs-K2-2026-09-14@2026-09-15", "obs-K2-2026-09-14@2026-09-16"],
        "N-ONE-OBS": ["obs-K2-2026-09-14@2026-09-15"],
        "N-ONE-CALL": ["one call"], "N-ONE-AUDIT": ["audit record"], "N-ONE-HIT": ["planted synthetic value"],
        "N-FIVE-VARIANTS": ["configured pair", "wrong tid", "wrong oid", "both wrong", "missing pair"],
        "N-A05-REASONS": ["MISSING_CUSTODIAN", "TRADED_STATUS_UNVERIFIED", "TRADED_HISTORY_UNVERIFIED",
                          "SOURCE_SCHEMA_INVALID", "AUTH_REQUIRED", "SOURCE_STALE", "BASE_OVERLAP_UNVERIFIED",
                          "CALENDAR_UNAVAILABLE"],
        "N-A05-COLLAPSED": ["unavailable", "unavailable", "unavailable", "unavailable", "unavailable",
                            "unavailable", "unavailable", "unavailable"],
        "N-CANDIDATES": ["K8"],
    }
    for cid, members in counts.items():
        led.count(cid, members, "count of the listed distinct members")
    led.sub("N-EXCLUDED-HEADERS", "count", ["N-HEADERS", "N-PROJECTED"], "headers never returned by the capability")
    led.sum("N-CHK-COVERED-PLUS-UNRESOLVED", "count", ["N-K1K3", "N-K2"], "covered + unresolved = expected (known denominator)")
    return fixtures, amounts, led


# ---------------------------------------------------------------- arms
OUTCOME = {"A01": "FWD-1", "A02": "FWD-2", "A03": "FWD-3", "A04": "FWD-4", "A05": "FWD-5", "A06": "FWD-6",
           "A07": "FWD-7", "A08": "FWD-8"}
LOCAL_EXEC = "TX-v-2 local controlled journey harness"
ARMS: list = []


def FI(valuation="2026-09-14", knowledge="2026-09-15", history=("SNAP-S0", "SNAP-S1"), workbook="WB-BASE", **extra):
    d = {"workbook": workbook, "history": list(history), "canonical": "CAN-BASE", "balance_components": "BAL-BASE",
         "substitutes": "SUB-BASE", "custodian": "CUS-BASE", "base_population": "POP-BASE", "bd_roster": "BD-BASE",
         "category_baseline": "CAT-BASE", "calendar": "CAL-BASE", "gateway": "GW-BASE",
         "valuation_date": valuation, "knowledge_date": knowledge, "gold_run_at": f"{knowledge}T13:30:00Z"}
    d.update(extra)
    return d


def TOTALS():
    return {"sma": N("L-SMA-AFTER"), "alt_strategies": N("L-ALT-AFTER"), "49financial": N("L-49F-AFTER"),
            "global": N("L-GLOBAL-AFTER")}


def NULLS():
    return {"sma": None, "alt_strategies": None, "49financial": None, "global": None}


def UNCH():
    return {"client": N("L-CLIENT"), "other_firm_1": N("L-OF1"), "other_firm_2": N("L-OF2")}


def COMPLETE(total="L-TAX-D14", expected="N-K1K2K3"):
    return {"expected_accounts": N(expected), "covered_accounts": N(expected), "unresolved_accounts": N("N-NONE"),
            "tax": {"value_status": "COMPLETE", "complete_value": N(total)}}


def K2_UNRESOLVED(identity_status, reason, business="N-K1K2K3", expected="N-K1K2K3"):
    return {"business_active_accounts": N(business) if business else None,
            "expected_accounts": N(expected) if expected else None,
            "covered_accounts": N("N-K1K3"), "unresolved_accounts": N("N-K2"),
            "accounts": {"K2": {"identity_status": identity_status, "value_usd": None, "reason_codes_include": [reason]}},
            "tax": {"value_status": "INCOMPLETE", "complete_value": None, "confirmed_subtotal": N("L-SUBTOTAL-K1-K3"),
                    "reason_codes_include": [reason]},
            "affected_complete_totals": NULLS(), "unchanged": UNCH()}


def K2_MATCHED():
    return {"business_active_accounts": N("N-K1K2K3"), "expected_accounts": N("N-K1K2K3"),
            "covered_accounts": N("N-K1K2K3"), "unresolved_accounts": N("N-NONE"),
            "accounts": {"K2": {"identity_status": "EXACT_MATCH", "value_usd": N("L-K2-VALUE")}},
            "tax": {"value_status": "COMPLETE", "complete_value": N("L-TAX-D14"), "confirmed_subtotal": N("L-TAX-D14")},
            "affected_complete_totals": TOTALS(), "unchanged": UNCH()}


def diff(cond, e_in, e_obs, d_in, d_obs, differs_on, invariant_within=()):
    return {"kind": "DIFFERENCE", "condition": cond, "engaged": {"input": e_in, "expected_observable": e_obs},
            "disengaged": {"input": d_in, "expected_observable": d_obs}, "differs_on": list(differs_on),
            "invariant_within": list(invariant_within)}


def inv(cond, e_in, e_obs, d_in, d_obs, invariant_on, contrast):
    return {"kind": "INVARIANCE", "condition": cond, "engaged": {"input": e_in, "expected_observable": e_obs},
            "disengaged": {"input": d_in, "expected_observable": d_obs}, "invariant_on": list(invariant_on),
            "contrast_arm": contrast}


def arm(aid, clauses, title, surfaces, fi, control, members=(), environment="LOCAL", executes_in=LOCAL_EXEC,
        readings=(), cases=None):
    a = {"id": aid, "property": aid[:3], "outcome": OUTCOME[aid[:3]], "title": title,
         "prd_clauses": [f"{aid[:3]}.{c}" for c in clauses], "covers_members": list(members),
         "surfaces": list(surfaces), "environment": environment, "executes_in": executes_in,
         "fixture_input": fi, "control": control, "expected_observable": control["engaged"]["expected_observable"],
         "readings": list(readings)}
    if cases:
        a["cases"] = cases
    ARMS.append(a)


def set_cell(snaps, row, col, value):
    return {"op": "set_cell", "snapshots": list(snaps), "row": row, "column": col, "value": value}


def arms_a01_a03() -> None:
    S01 = ("SNAP-S0", "SNAP-S1")
    # ---- A01 business membership
    arm("A01-01", ["c1"], "full-sheet fixture classifies every row kind", ["S01", "S02", "S19", "S03"],
        FI(workbook="WB-FULL"),
        diff("the full 14-header sheet versus the same sheet with the Traded header renamed",
             [{"op": "use_workbook", "workbook": "WB-FULL", "snapshots": list(S01)}],
             {"headers_count": N("N-HEADERS"), "projected_fields_count": N("N-PROJECTED"),
              "silver_rows": N("N-FULL-SHIPPED-ROWS"),
              "rows": {"r2": {"row_kind": "ACCOUNT_SLOT", "business_status": "TRADED_CLAIM"},
                       "r3": {"row_kind": "ACCOUNT_SLOT", "identity_status": "DUPLICATE_ACCOUNT"},
                       "r4": {"row_kind": "ACCOUNT_SLOT", "business_status": "TRADED_CLAIM"},
                       "r5": {"row_kind": "ACCOUNT_SLOT", "business_status": "UNTRADED"},
                       "r6": {"row_kind": "ACCOUNT_SLOT", "business_status": "PROSPECT"},
                       "r7": {"row_kind": "BLANK", "business_status": "BLANK"},
                       "r8": {"row_kind": "ACCOUNT_SLOT", "identity_status": "DUPLICATE_ACCOUNT"},
                       "r9": {"row_kind": "TOTAL"}},
              "business_active_accounts": N("N-K1K2K3-DUP"), "reason_codes_include": ["DUPLICATE_ACCOUNT"]},
             [{"op": "rename_header", "snapshots": list(S01), "from": "Traded", "to": "Traded Status"}],
             {"capability_error": "SOURCE_SCHEMA_INVALID", "business_active_accounts": None, "silver_rows": None,
              "reason_codes_include": ["SOURCE_SCHEMA_INVALID"], "complete_empty_cohort": False},
             ["business_active_accounts", "reason_codes_include", "silver_rows"]),
        members=["traded", "funded-but-untraded", "prospect", "blank", "conflict rows"], readings=["R1", "R14"])
    arm("A01-02", ["c2"], "flipping only Traded No to Yes changes the live count automatically", ["S03"],
        FI(),
        diff("K4's Traded cell flipped No to Yes at SNAP-S1, nothing else changed",
             [set_cell(["SNAP-S1"], "r5", "Traded", "Yes")],
             {"business_active_accounts": N("N-K1K2K3K4"), "source_observed_at": "2026-09-15T13:30:00Z",
              "events_emitted": [{"kind": "OBSERVE_TRADED", "account": "K4", "effective_date": "2026-09-15",
                                  "membership_date_basis": "FIRST_OBSERVED_UTC"}],
              "human_activation_calls": N("N-NONE")},
             [],
             {"business_active_accounts": N("N-K1K2K3"), "source_observed_at": "2026-09-15T13:30:00Z",
              "events_emitted": [], "human_activation_calls": N("N-NONE")},
             ["business_active_accounts", "events_emitted"], ["source_observed_at"]))
    arm("A01-03", ["c3"], "changing Ready alone does not change the live count", ["S03"],
        FI(),
        inv("Ready flipped on a traded and an untraded row at SNAP-S1 versus no change",
            [set_cell(["SNAP-S1"], "r3", "Ready", "Yes"), set_cell(["SNAP-S1"], "r5", "Ready", "No")],
            {"business_active_accounts": N("N-K1K2K3"), "events_emitted": []},
            [], {"business_active_accounts": N("N-K1K2K3"), "events_emitted": []},
            ["business_active_accounts", "events_emitted"], "A01-02"),
        members=["Ready"])
    arm("A01-04", ["c3"], "funding alone does not change the live count or the Tax value", ["S03", "S05"],
        FI(),
        inv("K4 (Traded=No) funded with a custodian value versus K4 unfunded",
            [], {"business_active_accounts": N("N-K1K2K3"), "tax": {"complete_value": N("L-TAX-D14"),
                                                                       "complete_value_not": N("L-TAX-WITH-K4-WRONG")}},
            [{"op": "remove_record", "fixture": "CAN-BASE", "account": "K4"},
             {"op": "remove_record", "fixture": "CUS-BASE", "account": "K4"}],
            {"business_active_accounts": N("N-K1K2K3"), "tax": {"complete_value": N("L-TAX-D14"),
                                                                "complete_value_not": N("L-TAX-WITH-K4-WRONG")}},
            ["business_active_accounts", "tax.complete_value"], "A01-02"),
        members=["funding"])
    k2_gone = [{"op": "remove_record", "fixture": "CUS-BASE", "account": "K2"},
               {"op": "remove_record", "fixture": "CAN-BASE", "account": "K2", "business_date": "2026-09-14"}]
    obs = K2_UNRESOLVED("MISSING_CUSTODIAN", "MISSING_CUSTODIAN")
    obs["accounts"]["K2"]["business_status"] = "TRADED_CLAIM"
    arm("A01-05", ["c4"], "a deleted Schwab record keeps the live count and withholds the complete value",
        ["S03", "S04", "S05", "S06", "S07"], FI(),
        diff("K2's custodian and canonical records deleted while Traded stays Yes", k2_gone, obs, [], K2_MATCHED(),
             ["covered_accounts", "unresolved_accounts", "tax.complete_value", "affected_complete_totals.global",
              "accounts.K2.identity_status"], ["business_active_accounts", "unchanged.client"]))
    dup = K2_UNRESOLVED("DUPLICATE_ACCOUNT", "DUPLICATE_ACCOUNT", business="N-K1K2K3-DUP")
    dup["k2_rows_retained"] = N("N-K2-ROWS")
    dup["arbitrary_duplicate_row_selected"] = False
    arm("A01-06", ["c5"], "duplicate full keys count once and retain the conflict", ["S03", "S04"],
        FI(workbook="WB-FULL"),
        diff("WB-FULL (K2 on r3 and r8, both Yes) versus WB-BASE", [{"op": "use_workbook", "workbook": "WB-FULL"}],
             dup, [{"op": "use_workbook", "workbook": "WB-BASE"}], K2_MATCHED(),
             ["accounts.K2.identity_status", "covered_accounts", "tax.complete_value"], ["business_active_accounts"]),
        readings=["R1"])
    bad = {"business_active_accounts": None, "expected_accounts": None, "covered_accounts": N("N-K1K3"),
           "unresolved_accounts": N("N-MALFORMED-CLAIM"),
           "rows": {"r3": {"business_status": "CONFLICT", "identity_status": "INVALID_ACCOUNT",
                           "reason_codes_include": ["INVALID_ACCOUNT"]}},
           "yes_claims_retained_in_protected_evidence": N("N-K1K2K3"), "tax": {"complete_value": None},
           "claims_vanished": N("N-NONE")}
    arm("A01-07", ["c6"], "an invalid YES identity yields an unknown complete count, never a vanished claim",
        ["S03", "S04"], FI(),
        diff("r3 carries a masked account on a Yes row at both snapshots versus the valid K2",
             [set_cell(S01, "r3", "Account Number", "****0002")], bad, [], K2_MATCHED(),
             ["business_active_accounts", "expected_accounts", "tax.complete_value"]),
        members=["invalid YES identities"], readings=["R2"])
    unk = {"business_active_accounts": None, "expected_accounts": None, "covered_accounts": N("N-K1K3"),
           "unresolved_accounts": N("N-K2"),
           "accounts": {"K2": {"business_status": "CONFLICT", "reason_codes_include": ["TRADED_STATUS_UNVERIFIED"]}},
           "yes_claims_retained_in_protected_evidence": N("N-K1K3"), "claims_vanished": N("N-NONE"),
           "tax": {"complete_value": None}}
    arm("A01-08", ["c6"], "an unknown Traded on an identified account yields an unknown complete count",
        ["S03"], FI(),
        diff("K2's Traded blank at both snapshots versus Yes", [set_cell(S01, "r3", "Traded", "")], unk, [],
             K2_MATCHED(), ["business_active_accounts", "tax.complete_value"]),
        members=["unknown identified Traded"], readings=["R2"])
    same = {"business_active_accounts": N("N-K1K2K3"), "silver_rows": N("N-BASE-SHIPPED-ROWS"),
            "business_status_by_key": {"K1": "TRADED_CLAIM", "K2": "TRADED_CLAIM", "K3": "TRADED_CLAIM", "K4": "UNTRADED"},
            "events_emitted": []}
    arm("A01-09", ["c7"], "reordered rows preserve every row, field, status and lineage", ["S02", "S19", "S03"],
        FI(),
        inv("SNAP-S1 rows shipped in the order r4, r2, r6, r3, r7, r5, r8 versus original order",
            [{"op": "reorder_rows", "snapshots": ["SNAP-S1"], "order": ["r4", "r2", "r6", "r3", "r7", "r5", "r8"]}],
            dict(same, silver_lineage_fields=["bronze_address", "response_sha256", "snapshot_id"]), [],
            dict(same, silver_lineage_fields=["bronze_address", "response_sha256", "snapshot_id"]),
            ["business_active_accounts", "silver_rows", "business_status_by_key", "events_emitted"], "A01-02"),
        members=["Reordered"])
    arm("A01-10", ["c7"], "inserted rows are discovered and every original row survives", ["S01", "S02", "S19", "S03"],
        FI(),
        diff("a blank row and a nameless prospect inserted before r4 at SNAP-S1 versus none",
             [{"op": "insert_rows", "snapshots": ["SNAP-S1"], "before": "r4",
               "rows": [{"Index": 7}, {"Index": 8, "Strategy": "SYNTH-TAX-STRATEGY", "AUM (Mn)": "0.5"}]}],
             {"silver_rows": N("N-INSERTED-SHIPPED-ROWS"), "business_active_accounts": N("N-K1K2K3"),
              "original_rows_retained": N("N-BASE-SHIPPED-ROWS"), "code_edit_required": False},
             [], {"silver_rows": N("N-BASE-SHIPPED-ROWS"), "business_active_accounts": N("N-K1K2K3"),
                  "original_rows_retained": N("N-BASE-SHIPPED-ROWS"), "code_edit_required": False},
             ["silver_rows"], ["business_active_accounts", "original_rows_retained"]),
        members=["inserted rows"])
    arm("A01-11", ["c7"], "Bronze/Silver replay preserves rows, fields and lineage without a duplicate", ["S02", "S19", "S03"],
        FI(),
        diff("the identical SNAP-S1 response body replayed versus a new acquisition envelope for the same logical rows",
             [{"op": "replay_bronze", "snapshot": "SNAP-S1", "times": 2}],
             {"silver_leaves_for_snapshot": N("N-ONE-LEAF"), "silver_rows": N("N-BASE-SHIPPED-ROWS"),
              "silver_business_columns": N("N-PROJECTED"), "silver_metadata_columns": N("N-ROW-META"),
              "silver_lineage_fields": ["bronze_address", "response_sha256", "snapshot_id"], "events_emitted": [],
              "bronze_body_rewritten": False},
             [{"op": "reacquire", "snapshot": "SNAP-S1", "observed_at": "2026-09-15T13:45:00Z", "same_logical_rows": True}],
             {"silver_leaves_for_snapshot": N("N-TWO-LEAVES"), "silver_rows": N("N-BASE-SHIPPED-ROWS"),
              "silver_business_columns": N("N-PROJECTED"), "silver_metadata_columns": N("N-ROW-META"),
              "silver_lineage_fields": ["bronze_address", "response_sha256", "snapshot_id"], "events_emitted": [],
              "bronze_body_rewritten": False},
             ["silver_leaves_for_snapshot"], ["events_emitted", "silver_rows"]),
        members=["Bronze/Silver replay"])
    arm("A01-12", ["c8"], "a failed Silver keeps the prior cohort and never makes a complete empty cohort",
        ["S19", "S03", "S07"], FI(),
        diff("the SNAP-S1 Silver write fails versus succeeds",
             [{"op": "fail_stage", "stage": "S19", "snapshot": "SNAP-S1", "mode": "missing output"}],
             {"business_active_accounts": None, "freshness": "SOURCE_UNAVAILABLE",
              "reason_codes_include": ["SOURCE_UNAVAILABLE"], "last_good_snapshot": "SNAP-S0",
              "retained_prior_cohort": N("N-K1K2K3"), "complete_empty_cohort": False},
             [], {"business_active_accounts": N("N-K1K2K3"), "freshness": "CURRENT", "reason_codes_include": [],
                  "last_good_snapshot": "SNAP-S1", "retained_prior_cohort": N("N-K1K2K3"),
                  "complete_empty_cohort": False},
             ["business_active_accounts", "freshness", "last_good_snapshot"], ["complete_empty_cohort"]))
    arm("A01-13", ["c8"], "a first-run Silver failure leaves the denominator unknown, not zero", ["S19", "S03", "S05"],
        FI(history=("SNAP-S0",), knowledge="2026-09-14", valuation="2026-09-11"),
        diff("the bootstrap SNAP-S0 Silver write fails versus succeeds",
             [{"op": "fail_stage", "stage": "S19", "snapshot": "SNAP-S0", "mode": "corrupt output"}],
             {"business_active_accounts": None, "expected_accounts": None, "reason_codes_include": ["SOURCE_SCHEMA_INVALID"],
              "complete_empty_cohort": False},
             [], {"business_active_accounts": N("N-K1K2K3"), "expected_accounts": None,
                  "reason_codes_include": ["TRADED_HISTORY_UNVERIFIED"], "complete_empty_cohort": False},
             ["business_active_accounts", "reason_codes_include"], ["expected_accounts", "complete_empty_cohort"]),
        readings=["R13"])

    # ---- A02 exact reconciliation
    arm("A02-01", ["c1"], "full identities match in both directions", ["S04"], FI(),
        diff("K3's custodian record present versus deleted",
             [], {"forward_matched": N("N-K1K2K3"), "reverse_unclaimed_candidates": N("N-CANDIDATES"),
                  "accounts": {"K1": {"identity_status": "EXACT_MATCH", "technical_enrollment": "ACTIVE"},
                               "K2": {"identity_status": "EXACT_MATCH", "technical_enrollment": "PENDING_RESOLUTION"},
                               "K3": {"identity_status": "EXACT_MATCH", "technical_enrollment": "ABSENT"}},
                  "covered_accounts": N("N-K1K2K3")},
             [{"op": "remove_record", "fixture": "CUS-BASE", "account": "K3"}],
             {"forward_matched": N("N-K1K2"), "reverse_unclaimed_candidates": N("N-CANDIDATES"),
              "accounts": {"K1": {"identity_status": "EXACT_MATCH", "technical_enrollment": "ACTIVE"},
                           "K2": {"identity_status": "EXACT_MATCH", "technical_enrollment": "PENDING_RESOLUTION"},
                           "K3": {"identity_status": "MISSING_CUSTODIAN", "technical_enrollment": "ABSENT"}},
              "covered_accounts": N("N-K1K2")},
             ["forward_matched", "accounts.K3.identity_status", "covered_accounts"], ["reverse_unclaimed_candidates"]))
    for aid, form, cell in (("A02-02", "suffix-only", "0002"), ("A02-03", "masked", "****0002")):
        o = K2_UNRESOLVED("INVALID_ACCOUNT", "INVALID_ACCOUNT", business=None, expected=None)
        o["unresolved_accounts"] = N("N-MALFORMED-CLAIM")
        o["accounts"] = {"K2": {"matched_by_suffix": False}}
        o["rows"] = {"r3": {"business_status": "CONFLICT", "identity_status": "INVALID_ACCOUNT"}}
        arm(aid, ["c2", "c4"], f"a {form} account on a Yes row stays unresolved; corrected, it matches", ["S04"], FI(),
            diff(f"r3 Account Number {form} at both snapshots versus the full key (the mismatch corrected)",
                 [set_cell(S01, "r3", "Account Number", cell)], o, [], K2_MATCHED(),
                 ["covered_accounts", "tax.complete_value", "business_active_accounts"]),
            members=[form], readings=["R2"])
    d = K2_UNRESOLVED("DUPLICATE_ACCOUNT", "DUPLICATE_ACCOUNT", business="N-K1K2K3-DUP")
    d["first_row_selected"] = False
    arm("A02-04", ["c2", "c4"], "a duplicate full key stays unresolved; with one row it matches", ["S04"],
        FI(workbook="WB-FULL"),
        diff("WB-FULL duplicate K2 versus the duplicate row removed", [{"op": "use_workbook", "workbook": "WB-FULL"}], d,
             [{"op": "use_workbook", "workbook": "WB-BASE"}], K2_MATCHED(),
             ["accounts.K2.identity_status", "covered_accounts"]),
        members=["duplicate"], readings=["R1"])
    mal = [("nine-digit", {"kind": "STRING", "string_value": "990000021"}),
           ("other-length", {"kind": "STRING", "string_value": "9900002"}),
           ("padded suffix", {"kind": "STRING", "string_value": "2"}),
           ("scientific-notation string", {"kind": "STRING", "string_value": "9.9000002E7"}),
           ("fractional", {"kind": "STRING", "string_value": "99000002.5"}),
           ("non-ASCII digits", {"kind": "STRING", "string_value": "٩٩٠٠٠٠٠٢"}),
           ("multiple separators", {"kind": "STRING", "string_value": "99-00-0002"}),
           ("misplaced separator", {"kind": "STRING", "string_value": "990-00002"}),
           ("blank", {"kind": "NULL"})]
    ok = [("eight ASCII digits", {"kind": "STRING", "string_value": "99000002"}),
          ("ten ASCII digits beginning 00", {"kind": "STRING", "string_value": "0099000002"}),
          ("four digits, hyphen, four digits", {"kind": "STRING", "string_value": "9900-0002"}),
          ("finite integral eight-digit Excel number", {"kind": "INTEGER", "integer_value": 99000002})]
    o = K2_UNRESOLVED("INVALID_ACCOUNT", "INVALID_ACCOUNT", business=None, expected=None)
    o["unresolved_accounts"] = N("N-MALFORMED-CLAIM")
    arm("A02-05", ["c2", "c4"], "every malformed account form stays unresolved; each accepted form matches the same key",
        ["S04"], FI(),
        diff("r3 Account Number set to each rejected form versus each accepted form (full key 0099000002)",
             [{"op": "set_cell_each_case", "snapshots": list(S01), "row": "r3", "column": "Account Number",
               "cases": "rejected"}], o,
             [{"op": "set_cell_each_case", "snapshots": list(S01), "row": "r3", "column": "Account Number",
               "cases": "accepted"}], K2_MATCHED(),
             ["covered_accounts", "business_active_accounts"]),
        members=["malformed"], readings=["R15"],
        cases={"rejected": [{"form": f, "scalar": s} for f, s in mal],
               "accepted": [{"form": f, "scalar": s, "normalizes_to": "K2"} for f, s in ok]})
    for aid, member, cond, delta, idst, fix in (
            ("A02-06", "master", "K2's custodian record under the money-manager master or the base master control",
             [{"op": "set_field", "fixture": "CUS-BASE", "account": "K2", "field": "master_ref",
               "each_of": ["CONTRACT:identity.trading_master_role", "CONTRACT:identity.base_master_control"]}],
             "MASTER_CONFLICT", "reporting master restored"),
            ("A02-07", "strategy", "K2's custodian strategy label conflicts with the workbook claim",
             [{"op": "set_field", "fixture": "CUS-BASE", "account": "K2", "field": "strategy",
               "value": "SYNTH-NONTAX-STRATEGY"}], "STRATEGY_CONFLICT", "compatible strategy restored")):
        o = K2_UNRESOLVED(idst, idst)
        o["accounts"]["K2"]["business_status"] = "TRADED_CLAIM"
        o["alias_applied"] = False
        arm(aid, ["c2", "c4"], f"a {member} conflict stays unresolved while the live claim stays; corrected, it matches",
            ["S04"], FI(), diff(cond + " versus " + fix, delta, o, [], K2_MATCHED(),
                                ["accounts.K2.identity_status", "covered_accounts"], ["business_active_accounts"]),
            members=[member])
    arm("A02-08", ["c2", "c4"], "a rekeyed claim stays TRANSFER_UNRESOLVED until a transfer is confirmed", ["S03", "S04"],
        FI(history=("SNAP-S0", "SNAP-S1")),
        diff("r3 shows K9 Yes at SNAP-S1 (K2 was Yes at SNAP-S0) versus the same plus a CONFIRM_TRANSFER K2 to K9",
             [set_cell(["SNAP-S1"], "r3", "Account Number", "99000009"),
              {"op": "add_record", "fixture": "CUS-BASE", "account": "K9"}],
             {"business_active_accounts": None, "accounts": {"K2": {"identity_status": "TRANSFER_UNRESOLVED",
                                                                    "reason_codes_include": ["TRANSFER_UNRESOLVED"]}},
              "k2_retained_in_expected_population": True, "dispositions_retained": True},
             [set_cell(["SNAP-S1"], "r3", "Account Number", "99000009"),
              {"op": "add_record", "fixture": "CUS-BASE", "account": "K9"},
              {"op": "add_disposition", "kind": "CONFIRM_TRANSFER", "from": "K2", "to": "K9",
               "actor": "SYNTH-OPERATOR-1", "evidence_ref": "SYNTH-EVIDENCE-TRANSFER-1"}],
             {"business_active_accounts": N("N-K1K9K3"), "accounts": {"K2": {"reason_codes_exclude": ["TRANSFER_UNRESOLVED"]}},
              "k2_retained_in_expected_population": True, "dispositions_retained": True},
             ["business_active_accounts"], ["dispositions_retained"]),
        members=["transfer"], readings=["R10"])
    arm("A02-09", ["c3"], "additional custodian candidates stay outside live membership", ["S04"], FI(),
        diff("K8 (custodian Tax label) with no workbook claim versus K8 added to the workbook with Traded=Yes",
             [], {"business_active_accounts": N("N-K1K2K3"), "expected_accounts": N("N-K1K2K3"),
                  "protected_candidates": N("N-CANDIDATES"), "workbook_writes": N("N-NONE"),
                  "tax": {"complete_value": N("L-TAX-D14")}},
             [{"op": "append_row", "snapshots": list(S01), "before": "r8",
               "cells": {"Index": 7, "Account Number": "99000008", "Strategy": "SYNTH-TAX-STRATEGY", "Traded": "Yes"}}],
             {"business_active_accounts": N("N-K1K2K3K8"), "expected_accounts": N("N-K1K2K3K8"),
              "protected_candidates": N("N-NONE"), "workbook_writes": N("N-NONE"),
              "tax": {"complete_value": N("L-TAX-WITH-K8")}},
             ["business_active_accounts", "tax.complete_value"], ["workbook_writes"]),
        readings=["R4"])
    arm("A02-10", ["c5"], "no private ID appears in consumer or log outputs", ["S04", "S08", "S10"], FI(),
        diff("the privacy boundary intact versus a synthetic full key planted into one log line",
             [], {"synthetic_key_hits_in_consumer_json": N("N-NONE"), "synthetic_key_hits_in_logs": N("N-NONE"),
                  "protected_evidence_carries_keys": True},
             [{"op": "plant_token", "target": "run log", "value": "KEYS.K1.full"}],
             {"synthetic_key_hits_in_consumer_json": N("N-NONE"), "synthetic_key_hits_in_logs": N("N-ONE-HIT"),
              "protected_evidence_carries_keys": True},
             ["synthetic_key_hits_in_logs"], ["synthetic_key_hits_in_consumer_json"]))

    # ---- A03 activation and dated correction
    k5_row = {"op": "append_row", "snapshots": ["SNAP-S1", "SNAP-S2"], "before": "r8",
              "cells": {"Index": 7, "Account Number": "99000005", "Strategy": "SYNTH-TAX-STRATEGY", "Traded": "Yes"}}
    k5_cus = {"op": "add_record", "fixture": "CUS-BASE", "account": "K5"}
    arm("A03-01", ["c1"], "a new Traded Yes outside the original extent opens membership automatically", ["S01", "S03"],
        FI(),
        diff("K5 appended past SNAP-S0's extent with Yes versus with No",
             [k5_row, k5_cus],
             {"business_active_accounts": N("N-K1K2K3K5"), "source_observed_at": "2026-09-15T13:30:00Z",
              "events_emitted": [{"kind": "OBSERVE_TRADED", "account": "K5", "effective_date": "2026-09-15",
                                  "membership_date_basis": "FIRST_OBSERVED_UTC", "actor": "S03 service identity",
                                  "evidence_ref": "protected Bronze/Silver lineage of SNAP-S1"}],
              "human_activation_calls": N("N-NONE"), "code_edit_required": False},
             [dict(k5_row, cells=dict(k5_row["cells"], Traded="No")), k5_cus],
             {"business_active_accounts": N("N-K1K2K3"), "source_observed_at": "2026-09-15T13:30:00Z",
              "events_emitted": [{"kind": "OBSERVE_INACTIVE", "account": "K5", "effective_date": "2026-09-15",
                                  "membership_date_basis": "FIRST_OBSERVED_UTC", "actor": "S03 service identity",
                                  "evidence_ref": "protected Bronze/Silver lineage of SNAP-S1"}],
              "human_activation_calls": N("N-NONE"), "code_edit_required": False},
             ["business_active_accounts", "events_emitted"], ["human_activation_calls"]))
    arm("A03-02", ["c2"], "with valid values the first-observed UTC day is included", ["S03", "S05"],
        FI(history=("SNAP-S0", "SNAP-S1", "SNAP-S2"), valuation="2026-09-15", knowledge="2026-09-16"),
        diff("valuation date 2026-09-15 (K5's first-observed day) versus 2026-09-14 (the day before)",
             [k5_row, k5_cus],
             dict(COMPLETE("L-TAX-WITH-K5", "N-K1K2K3K5"),
                  accounts={"K5": {"membership_date_status": "OBSERVED_TRADED", "value_usd": N("L-K5-VALUE")}}),
             [k5_row, k5_cus, {"op": "set_run", "valuation_date": "2026-09-14"}],
             {"expected_accounts": None, "covered_accounts": N("N-K1K2K3"), "unresolved_accounts": N("N-K5"),
              "tax": {"value_status": "INCOMPLETE", "complete_value": None},
              "accounts": {"K5": {"membership_date_status": "UNVERIFIED", "value_usd": None}}},
             ["accounts.K5.membership_date_status", "tax.complete_value"]))
    arm("A03-03", ["c3"], "the date before a new account's history stays TRADED_HISTORY_UNVERIFIED, never a zero",
        ["S03", "S05"], FI(),
        diff("K5 discovered Yes at SNAP-S1 versus K5 never in the workbook, valuation 2026-09-14",
             [k5_row, k5_cus],
             {"business_active_accounts": N("N-K1K2K3K5"), "expected_accounts": None,
              "covered_accounts": N("N-K1K2K3"), "unresolved_accounts": N("N-K5"),
              "accounts": {"K5": {"membership_date_status": "UNVERIFIED", "value_status": "UNAVAILABLE",
                                  "value_usd": None, "reason_codes_include": ["TRADED_HISTORY_UNVERIFIED"]}},
              "tax": {"value_status": "INCOMPLETE", "complete_value": None, "confirmed_subtotal": N("L-TAX-D14")}},
             [], dict(COMPLETE(), business_active_accounts=N("N-K1K2K3")),
             ["expected_accounts", "tax.complete_value"]),
        readings=["R13"])
    k6 = [{"op": "append_row", "snapshots": ["SNAP-S0"], "before": "r8",
           "cells": {"Index": 7, "Account Number": "99000006", "Strategy": "SYNTH-TAX-STRATEGY", "Traded": "No"}},
          {"op": "append_row", "snapshots": ["SNAP-S1"], "before": "r8",
           "cells": {"Index": 7, "Account Number": "99000006", "Strategy": "SYNTH-TAX-STRATEGY", "Traded": "Yes"}},
          {"op": "add_record", "fixture": "CUS-BASE", "account": "K6"}]
    arm("A03-04", ["c4"], "a retained complete NO-to-YES history proves earlier inactivity", ["S03", "S05"], FI(),
        diff("K6 No at SNAP-S0 and Yes at SNAP-S1 versus K6 absent at SNAP-S0 and Yes at SNAP-S1",
             k6, dict(COMPLETE(), accounts={"K6": {"membership_date_status": "OBSERVED_INACTIVE"}}),
             k6[1:], {"expected_accounts": None, "covered_accounts": N("N-K1K2K3"), "unresolved_accounts": N("N-K6"),
                      "accounts": {"K6": {"membership_date_status": "UNVERIFIED",
                                          "reason_codes_include": ["TRADED_HISTORY_UNVERIFIED"]}},
                      "tax": {"value_status": "INCOMPLETE", "complete_value": None}},
             ["accounts.K6.membership_date_status", "tax.complete_value"]))
    h3 = ("SNAP-S0", "SNAP-S1", "SNAP-S2")
    arm("A03-05", ["c5"], "an explicit NO closes membership exclusively on its date", ["S03", "S05"],
        FI(history=h3, valuation="2026-09-16", knowledge="2026-09-17"),
        diff("K2 No at SNAP-S2 (2026-09-16T13:30:00Z) versus K2 still Yes",
             [set_cell(["SNAP-S2"], "r3", "Traded", "No")],
             {"membership_date_status_by_valuation_date": {"2026-09-15": {"K2": "OBSERVED_TRADED"},
                                                           "2026-09-16": {"K2": "OBSERVED_INACTIVE"}},
              "k2_interval": {"start": "2026-09-14", "end_exclusive": "2026-09-16"},
              "business_active_accounts": N("N-K1K3"), "accounts": {"K2": {"business_status": "INACTIVE_CONFIRMED"}},
              "tax": {"complete_value": N("L-TAX-K1-K3")}},
             [], {"membership_date_status_by_valuation_date": {"2026-09-15": {"K2": "OBSERVED_TRADED"},
                                                               "2026-09-16": {"K2": "OBSERVED_TRADED"}},
                  "k2_interval": {"start": "2026-09-14", "end_exclusive": None},
                  "business_active_accounts": N("N-K1K2K3"), "accounts": {"K2": {"business_status": "TRADED_CLAIM"}},
                  "tax": {"complete_value": N("L-TAX-D14")}},
             ["k2_interval.end_exclusive", "business_active_accounts", "tax.complete_value"]),
        members=["explicit NO exclusive closure"])
    arm("A03-06", ["c5"], "NO-to-YES reactivation opens a new interval", ["S03"],
        FI(history=("SNAP-S0", "SNAP-S1", "SNAP-S2", "SNAP-S4"), valuation="2026-09-18", knowledge="2026-09-19"),
        diff("K2 No at SNAP-S2 then Yes at SNAP-S4 (2026-09-18T13:30:00Z) versus No at both",
             [set_cell(["SNAP-S2"], "r3", "Traded", "No"), set_cell(["SNAP-S4"], "r3", "Traded", "Yes")],
             {"k2_intervals": [{"start": "2026-09-14", "end_exclusive": "2026-09-16"},
                               {"start": "2026-09-18", "end_exclusive": None}],
              "membership_date_status_by_valuation_date": {"2026-09-17": {"K2": "OBSERVED_INACTIVE"},
                                                           "2026-09-18": {"K2": "OBSERVED_TRADED"}},
              "k2_events": N("N-K2-REACTIVATION-EVENTS")},
             [set_cell(["SNAP-S2", "SNAP-S4"], "r3", "Traded", "No")],
             {"k2_intervals": [{"start": "2026-09-14", "end_exclusive": "2026-09-16"}],
              "membership_date_status_by_valuation_date": {"2026-09-17": {"K2": "OBSERVED_INACTIVE"},
                                                           "2026-09-18": {"K2": "OBSERVED_INACTIVE"}},
              "k2_events": N("N-K2-CLOSE-EVENTS")},
             ["k2_intervals", "membership_date_status_by_valuation_date"]),
        members=["reactivation"])
    arm("A03-07", ["c5"], "same-UTC-day transitions keep every event and the day's latest state", ["S03"],
        FI(history=("SNAP-S0", "SNAP-S1"), valuation="2026-09-16", knowledge="2026-09-17"),
        diff("K2 No at 2026-09-16T09:00:00Z then Yes at 15:00:00Z versus Yes at 09:00:00Z then No at 15:00:00Z",
             [{"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-16T09:00:00Z", "set": {"r3.Traded": "No"}},
              {"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-16T15:00:00Z", "set": {"r3.Traded": "Yes"}}],
             {"k2_day_state_2026_09_16": "YES", "same_day_events_retained": N("N-SAMEDAY-EVENTS"),
              "membership_date_status_by_valuation_date": {"2026-09-16": {"K2": "OBSERVED_TRADED"}}},
             [{"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-16T09:00:00Z", "set": {"r3.Traded": "Yes"}},
              {"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-16T15:00:00Z", "set": {"r3.Traded": "No"}}],
             {"k2_day_state_2026_09_16": "NO", "same_day_events_retained": N("N-SAMEDAY-EVENTS"),
              "membership_date_status_by_valuation_date": {"2026-09-16": {"K2": "OBSERVED_INACTIVE"}}},
             ["k2_day_state_2026_09_16", "membership_date_status_by_valuation_date"], ["same_day_events_retained"]),
        members=["same-day ordering"], readings=["R16"])
    arm("A03-08", ["c5"], "replaying a logical snapshot creates no duplicate transition or shifted date", ["S03"], FI(),
        diff("SNAP-S1's logical snapshot replayed at 2026-09-15T13:45:00Z versus a new logical snapshot with K4 Yes",
             [{"op": "replay_snapshot", "snapshot": "SNAP-S1", "retry_at": "2026-09-15T13:45:00Z"}],
             {"events_total": N("N-S0-EVENTS"), "source_event_ids_changed": False, "effective_dates_shifted": False},
             [{"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-15T13:45:00Z", "set": {"r5.Traded": "Yes"}}],
             {"events_total": N("N-S0-EVENTS-PLUS-ONE"), "source_event_ids_changed": False, "effective_dates_shifted": False},
             ["events_total"], ["source_event_ids_changed"]),
        members=["idempotent replay"])
    arm("A03-09", ["c5"], "an older unseen snapshot cannot roll current state backward", ["S03"],
        FI(history=h3, valuation="2026-09-15", knowledge="2026-09-16"),
        diff("a K2-No snapshot observed 2026-09-15T20:00:00Z delivered after the SNAP-S2 watermark versus before it",
             [{"op": "deliver_late_snapshot", "after": "SNAP-S2", "observed_at": "2026-09-15T20:00:00Z",
               "set": {"r3.Traded": "No"}}],
             {"reason_codes_include": ["TRADED_EVENT_ORDER_CONFLICT"], "accounts": {"K2": {"business_status": "TRADED_CLAIM"}},
              "late_snapshot_retained_as_history": True, "business_active_accounts": N("N-K1K2K3")},
             [{"op": "deliver_snapshot_in_order", "before": "SNAP-S2", "observed_at": "2026-09-15T20:00:00Z",
               "set": {"r3.Traded": "No"}}],
             {"reason_codes_include": [], "accounts": {"K2": {"business_status": "TRADED_CLAIM"}},
              "late_snapshot_retained_as_history": False, "business_active_accounts": N("N-K1K2K3"),
              "k2_events_include": [{"kind": "OBSERVE_INACTIVE", "effective_date": "2026-09-15"},
                                    {"kind": "OBSERVE_TRADED", "effective_date": "2026-09-16"}]},
             ["reason_codes_include", "late_snapshot_retained_as_history"], ["business_active_accounts"]),
        members=["out-of-order refusal"],
        cases={"same_observed_at_conflict": {"input": "two snapshots with one observed_at and different K2 states",
                                             "expected_observable": {"refused": True, "events_emitted": []}}})
    blank_obs = {"business_active_accounts": None, "k2_interval_end_exclusive": None,
                 "accounts": {"K2": {"business_status": "CONFLICT", "reason_codes_include": ["TRADED_STATUS_UNVERIFIED"]}},
                 "k2_retained_in_expected_population": True}
    arm("A03-10", ["c5"], "an invalid or blank Traded after a proven Yes never closes the interval", ["S03"],
        FI(history=h3, valuation="2026-09-16", knowledge="2026-09-17"),
        diff("K2 Traded blank (and, as a case, 'Maybe') at SNAP-S2 versus an explicit No",
             [set_cell(["SNAP-S2"], "r3", "Traded", "")], blank_obs,
             [set_cell(["SNAP-S2"], "r3", "Traded", "No")],
             {"business_active_accounts": N("N-K1K3"), "k2_interval_end_exclusive": "2026-09-16",
              "accounts": {"K2": {"business_status": "INACTIVE_CONFIRMED", "reason_codes_exclude": ["TRADED_STATUS_UNVERIFIED"]}},
              "k2_retained_in_expected_population": False},
             ["business_active_accounts", "k2_interval_end_exclusive", "accounts.K2.business_status"]),
        members=["invalid/blank Traded"],
        cases={"invalid_value": {"input": [set_cell(["SNAP-S2"], "r3", "Traded", "Maybe")], "expected_observable": "same as engaged"}})
    for aid, what, delta, st, rc in (
            ("A03-11", "removed", [{"op": "delete_row", "snapshots": ["SNAP-S2"], "row": "r3"}],
             "REMOVED_UNCONFIRMED", "REMOVED_UNCONFIRMED"),
            ("A03-12", "rekeyed", [set_cell(["SNAP-S2"], "r3", "Account Number", "99000009"),
                                   {"op": "add_record", "fixture": "CUS-BASE", "account": "K9"}],
             "REMOVED_UNCONFIRMED", "TRANSFER_UNRESOLVED")):
        arm(aid, ["c5"], f"a {what} prior Yes claim stays unresolved and in the population", ["S03", "S04"],
            FI(history=h3, valuation="2026-09-16", knowledge="2026-09-17"),
            diff(f"K2's row {what} at SNAP-S2 versus K2 explicitly No at SNAP-S2", delta,
                 {"business_active_accounts": None, "accounts": {"K2": {"business_status": st, "reason_codes_include": [rc]}},
                  "k2_interval_end_exclusive": None, "k2_retained_in_expected_population": True},
                 [set_cell(["SNAP-S2"], "r3", "Traded", "No")],
                 {"business_active_accounts": N("N-K1K3"), "accounts": {"K2": {"business_status": "INACTIVE_CONFIRMED",
                                                                              "reason_codes_exclude": [rc]}},
                  "k2_interval_end_exclusive": "2026-09-16", "k2_retained_in_expected_population": False},
                 ["business_active_accounts", "k2_interval_end_exclusive"]),
            members=["removed/rekeyed claims"])
    arm("A03-13", ["c6"], "a correction retains the old and the new observation", ["S03", "S05"],
        FI(history=("SNAP-S0", "SNAP-S1", "SNAP-S2"), valuation="2026-09-14", knowledge="2026-09-16"),
        diff("K2's strategy conflict in the 2026-09-15 object resolved by RESOLVE_STRATEGY versus left unresolved",
             [{"op": "set_field", "fixture": "CUS-BASE", "account": "K2", "field": "strategy",
               "value": "SYNTH-NONTAX-STRATEGY", "until_knowledge_date": "2026-09-15"},
              {"op": "add_disposition", "kind": "RESOLVE_STRATEGY", "account": "K2", "actor": "SYNTH-OPERATOR-1",
               "evidence_ref": "SYNTH-EVIDENCE-STRATEGY-1", "recorded_at": "2026-09-15T18:00:00Z"}],
             {"k2_observations_for_2026_09_14": N("N-OLD-NEW-OBS"), "new_observation_supersedes_old": True,
              "resolved": {"value_status": "COMPLETE", "complete_value": N("L-TAX-D14")},
              "old_object_2026_09_15_unchanged": True},
             [{"op": "set_field", "fixture": "CUS-BASE", "account": "K2", "field": "strategy",
               "value": "SYNTH-NONTAX-STRATEGY"}],
             {"k2_observations_for_2026_09_14": N("N-ONE-OBS"), "new_observation_supersedes_old": False,
              "resolved": {"value_status": "INCOMPLETE", "complete_value": None},
              "old_object_2026_09_15_unchanged": True},
             ["k2_observations_for_2026_09_14", "resolved.complete_value"], ["old_object_2026_09_15_unchanged"]))
    arm("A03-14", ["c6"], "a correction cannot invent a Traded flag or a historical date", ["S03"], FI(),
        diff("a disposition carrying traded_value YES and effective_date 2026-09-01 for K7 (Traded No), plus a legacy "
             "CONFIRM_EFFECTIVE_MEMBERSHIP record, versus a source observation of K7 Yes at SNAP-S1",
             [{"op": "append_row", "snapshots": list(S01), "before": "r8",
               "cells": {"Index": 7, "Account Number": "99000007", "Strategy": "SYNTH-TAX-STRATEGY", "Traded": "No",
                         "Inception Date": "2026-08-03", "Last Trade Date": "2026-09-11"}},
              {"op": "add_record", "fixture": "CUS-BASE", "account": "K7"},
              {"op": "add_disposition", "kind": "CORRECT_IDENTITY", "account": "K7", "traded_value": "YES",
               "effective_date": "2026-09-01", "actor": "SYNTH-OPERATOR-1", "evidence_ref": "SYNTH-EVIDENCE-2"},
              {"op": "add_legacy_record", "legacy_kind": "CONFIRM_EFFECTIVE_MEMBERSHIP", "account": "K7"}],
             {"accounts": {"K7": {"business_status": "UNTRADED"}}, "k7_membership_opened": False,
              "invented_flag_accepted": False, "backdated_effective_date_accepted": False,
              "legacy_record_accepted_as_activation": False, "business_active_accounts": N("N-K1K2K3")},
             [{"op": "append_row", "snapshots": ["SNAP-S0"], "before": "r8",
               "cells": {"Index": 7, "Account Number": "99000007", "Strategy": "SYNTH-TAX-STRATEGY", "Traded": "No"}},
              {"op": "append_row", "snapshots": ["SNAP-S1"], "before": "r8",
               "cells": {"Index": 7, "Account Number": "99000007", "Strategy": "SYNTH-TAX-STRATEGY", "Traded": "Yes",
                         "Inception Date": "2026-08-03", "Last Trade Date": "2026-09-11"}},
              {"op": "add_record", "fixture": "CUS-BASE", "account": "K7"}],
             {"accounts": {"K7": {"business_status": "TRADED_CLAIM"}}, "k7_membership_opened": True,
              "k7_effective_date": "2026-09-15", "k7_effective_date_not": ["2026-09-01", "2026-08-03", "2026-09-11"],
              "invented_flag_accepted": False, "backdated_effective_date_accepted": False,
              "legacy_record_accepted_as_activation": False, "business_active_accounts": N("N-K1K2K3K7")},
             ["k7_membership_opened", "accounts.K7.business_status"], ["invented_flag_accepted"]),
        readings=["R17"])
    arm("A03-15", ["c7", "c8", "c9"], "a NO at 2026-09-16T00:30Z closes on Sep16 UTC and preserves Sep15", ["S03", "S05"],
        FI(history=("SNAP-S0", "SNAP-S1"), valuation="2026-09-15", knowledge="2026-09-16"),
        diff("K2 No observed 2026-09-16T00:30:00Z (Sep15 20:30 EDT) versus No observed 2026-09-15T23:30:00Z",
             [{"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-16T00:30:00Z", "set": {"r3.Traded": "No"}}],
             {"k2_effective_date": "2026-09-16",
              "membership_date_status_by_valuation_date": {"2026-09-15": {"K2": "OBSERVED_TRADED"},
                                                           "2026-09-16": {"K2": "OBSERVED_INACTIVE"}},
              "comparison": "ISO calendar date start <= valuation_date < end", "local_time_shift_applied": False},
             [{"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-15T23:30:00Z", "set": {"r3.Traded": "No"}}],
             {"k2_effective_date": "2026-09-15",
              "membership_date_status_by_valuation_date": {"2026-09-15": {"K2": "OBSERVED_INACTIVE"},
                                                           "2026-09-16": {"K2": "OBSERVED_INACTIVE"}},
              "comparison": "ISO calendar date start <= valuation_date < end", "local_time_shift_applied": False},
             ["k2_effective_date", "membership_date_status_by_valuation_date"], ["local_time_shift_applied"]))
    k5_late = [{"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-16T00:30:00Z",
                "append_before_r8": {"Index": 7, "Account Number": "99000005", "Strategy": "SYNTH-TAX-STRATEGY",
                                     "Traded": "Yes"}}, k5_cus]
    k5_no_hist = [{"op": "append_row", "snapshots": list(S01), "before": "r8",
                   "cells": {"Index": 7, "Account Number": "99000005", "Strategy": "SYNTH-TAX-STRATEGY", "Traded": "No"}}]
    arm("A03-16", ["c10"], "a YES with no prior history at 2026-09-16T00:30Z leaves Sep15 unverified", ["S03", "S05"],
        FI(history=("SNAP-S0", "SNAP-S1"), valuation="2026-09-15", knowledge="2026-09-16"),
        diff("K5 first seen Yes at 2026-09-16T00:30:00Z versus K5 with retained No history at SNAP-S0 and SNAP-S1",
             k5_late, {"k5_effective_date": "2026-09-16",
                       "accounts": {"K5": {"membership_date_status": "UNVERIFIED",
                                           "reason_codes_include": ["TRADED_HISTORY_UNVERIFIED"]}},
                       "expected_accounts": None, "tax": {"complete_value": None}},
             k5_no_hist + k5_late, {"k5_effective_date": "2026-09-16",
                                    "accounts": {"K5": {"membership_date_status": "OBSERVED_INACTIVE"}},
                                    "expected_accounts": N("N-K1K2K3"), "tax": {"complete_value": N("L-TAX-D14")}},
             ["accounts.K5.membership_date_status", "expected_accounts", "tax.complete_value"], ["k5_effective_date"]))
    arm("A03-17", ["c11"], "the current live count changes immediately at source_observed_at", ["S03"],
        FI(history=("SNAP-S0", "SNAP-S1"), valuation="2026-09-15", knowledge="2026-09-16"),
        diff("K5 Yes observed 2026-09-16T00:30:00Z versus K5 No at the same instant",
             k5_late, {"business_active_accounts": N("N-K1K2K3K5"), "source_observed_at": "2026-09-16T00:30:00Z",
                       "valuation_date": "2026-09-15", "expected_accounts": None},
             [dict(k5_late[0], append_before_r8=dict(k5_late[0]["append_before_r8"], Traded="No")), k5_cus],
             {"business_active_accounts": N("N-K1K2K3"), "source_observed_at": "2026-09-16T00:30:00Z",
              "valuation_date": "2026-09-15", "expected_accounts": N("N-K1K2K3")},
             ["business_active_accounts", "expected_accounts"], ["source_observed_at", "valuation_date"]))
    arm("A03-18", ["c12"], "no local-time shift and no invented weekend session", ["S03", "S05", "S07"],
        FI(history=("SNAP-S0", "SNAP-S1", "SNAP-S4"), valuation="2026-09-18", knowledge="2026-09-19"),
        diff("K5 Yes observed Saturday 2026-09-19T14:00:00Z versus Friday 2026-09-18T12:00:00Z",
             [{"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-19T14:00:00Z",
               "append_before_r8": {"Index": 7, "Account Number": "99000005", "Traded": "Yes"}}, k5_cus,
              {"op": "run_knowledge_dates", "dates": ["2026-09-19", "2026-09-20", "2026-09-21", "2026-09-22"]}],
             {"k5_effective_date": "2026-09-19",
              "valuation_date_by_knowledge_date": {"2026-09-19": "2026-09-18", "2026-09-20": "2026-09-18",
                                                   "2026-09-21": "2026-09-18", "2026-09-22": "2026-09-21"},
              "valuation_dates_never_produced": ["2026-09-19", "2026-09-20"],
              "membership_date_status_by_valuation_date": {"2026-09-18": {"K5": "UNVERIFIED"},
                                                           "2026-09-21": {"K5": "OBSERVED_TRADED"}}},
             [{"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-18T12:00:00Z",
               "append_before_r8": {"Index": 7, "Account Number": "99000005", "Traded": "Yes"}}, k5_cus,
              {"op": "run_knowledge_dates", "dates": ["2026-09-19", "2026-09-20", "2026-09-21", "2026-09-22"]}],
             {"k5_effective_date": "2026-09-18",
              "valuation_date_by_knowledge_date": {"2026-09-19": "2026-09-18", "2026-09-20": "2026-09-18",
                                                   "2026-09-21": "2026-09-18", "2026-09-22": "2026-09-21"},
              "valuation_dates_never_produced": ["2026-09-19", "2026-09-20"],
              "membership_date_status_by_valuation_date": {"2026-09-18": {"K5": "OBSERVED_TRADED"},
                                                           "2026-09-21": {"K5": "OBSERVED_TRADED"}}},
             ["k5_effective_date", "membership_date_status_by_valuation_date"],
             ["valuation_date_by_knowledge_date", "valuation_dates_never_produced"]),
        readings=["R7", "R11"])


def arms_a04_a06() -> None:
    trace = {"basis": "dim_balance.net_mv_plus_cash via b00 canonical_valuation", "canonical_source_ref": "present",
             "balance_source_ref": "present", "source_hashes": "present", "valuation_date": "2026-09-14",
             "boundary_version": "SYNTH-B00-BOUNDARY-1", "accrual_limitation_carried": True}
    for aid, k, member, cond, d_in, d_obs in (
            ("A04-01", "K1", "cash", "K1's canonical row present versus missing",
             [{"op": "remove_record", "fixture": "CAN-BASE", "account": "K1", "business_date": "2026-09-14"}],
             {"value_status": "UNAVAILABLE", "value_usd": None, "reason_codes_include": ["CANONICAL_MISSING"]}),
            ("A04-02", "K2", "long/short exposure", "K2's canonical row present versus missing",
             [{"op": "remove_record", "fixture": "CAN-BASE", "account": "K2", "business_date": "2026-09-14"}],
             {"value_status": "UNAVAILABLE", "value_usd": None, "reason_codes_include": ["CANONICAL_MISSING"]}),
            ("A04-03", "K3", "margin", "one K3 canonical row versus two K3 rows for 2026-09-14",
             [{"op": "duplicate_record", "fixture": "CAN-BASE", "account": "K3", "business_date": "2026-09-14"}],
             {"value_status": "UNAVAILABLE", "value_usd": None, "reason_codes_include": ["CANONICAL_DUPLICATE"]})):
        e = {"accounts": {k: dict(trace, value_status="COMPLETE", value_usd=N(f"L-{k}-VALUE"))},
             "components_identity": N(f"L-{k}-NET-IDENTITY")}
        if k == "K2":
            e["accounts"][k]["value_usd_not"] = N("L-K2-GROSS-EXPOSURE")
        arm(aid, ["c1", "c2"], f"{member}: the value equals the canonical net value to the cent", ["S05"], FI(),
            diff(cond, [], e, d_in, {"accounts": {k: d_obs}, "components_identity": N(f"L-{k}-NET-IDENTITY")},
                 [f"accounts.{k}.value_usd", f"accounts.{k}.value_status"], ["components_identity"]),
            members=[member])
    arm("A04-04", ["c1"], "an actual zero is KNOWN_ZERO only when the source reports it", ["S05"], FI(),
        diff("K1's canonical value an actual 0.00 versus K1's canonical row missing",
             [{"op": "set_field", "fixture": "CAN-BASE", "account": "K1", "field": "net_mv_plus_cash", "value": "0.00",
               "amount_id": "AMT-ZERO"}],
             {"accounts": {"K1": {"value_status": "KNOWN_ZERO", "value_usd": N("L-ZERO-VALUE")}},
              "tax": {"value_status": "COMPLETE", "complete_value": N("L-TAX-K1-ZERO")}},
             [{"op": "remove_record", "fixture": "CAN-BASE", "account": "K1", "business_date": "2026-09-14"}],
             {"accounts": {"K1": {"value_status": "UNAVAILABLE", "value_usd": None,
                                  "reason_codes_include": ["CANONICAL_MISSING"]}},
              "tax": {"value_status": "INCOMPLETE", "complete_value": None}},
             ["accounts.K1.value_status", "tax.complete_value"]),
        members=["actual zero"])
    arm("A04-05", ["c2"], "the cohort value is exact to the cent with a source/date/boundary trace", ["S05", "S06"], FI(),
        diff("every canonical value finite versus K2's value non-finite (NaN)",
             [], {"tax": {"value_status": "COMPLETE", "complete_value": N("L-TAX-D14"),
                          "storage_type": "decimal128(20,2)"},
                  "per_account_trace": {"K1": trace, "K2": trace, "K3": trace}},
             [{"op": "set_field", "fixture": "CAN-BASE", "account": "K2", "field": "net_mv_plus_cash", "value": "NaN"}],
             {"tax": {"value_status": "INCOMPLETE", "complete_value": None, "storage_type": "decimal128(20,2)",
                      "reason_codes_include": ["INVALID_VALUE"]},
              "per_account_trace": {"K1": trace, "K2": trace, "K3": trace}},
             ["tax.complete_value"], ["per_account_trace"]))
    subs = (("A04-06", "Gross exposure", "gross_exposure", "L-K2-GROSS-EXPOSURE"),
            ("A04-07", "sales estimate", "sales_estimate_usd", "L-K2-SALES-EST"),
            ("A04-08", "quarterly data", "bd_quarterly_value", "L-K2-BD-QUARTERLY"),
            ("A04-09", "unverified accrual", "accrued_income_unverified", "L-K2-WITH-ACCRUAL-WRONG"))
    for aid, member, field, wrong in subs:
        arm(aid, ["c3"], f"{member} cannot replace the canonical value", ["S05"], FI(),
            diff(f"K2's canonical value present beside SUB-BASE.K2.{field} versus the canonical row missing with the "
                 f"substitute still present",
                 [], {"accounts": {"K2": {"value_usd": N("L-K2-VALUE"), "value_usd_not": N(wrong),
                                          "value_status": "COMPLETE"}}},
                 [{"op": "remove_record", "fixture": "CAN-BASE", "account": "K2", "business_date": "2026-09-14"}],
                 {"accounts": {"K2": {"value_usd": None, "value_usd_not": N(wrong), "value_status": "UNAVAILABLE",
                                      "reason_codes_include": ["CANONICAL_MISSING"]}}},
                 ["accounts.K2.value_usd", "accounts.K2.value_status"], ["accounts.K2.value_usd_not"]),
            members=[member], readings=["R18"] if field.startswith("accrued") else [])
    arm("A04-10", ["c1", "c2"], "authorized dated-source cases equal the canonical value to the cent", ["S05"],
        {"source": "authorized dated 0833/b00 reads under their own authorization", "values_in_repository": False},
        diff("the observation compared to canonical net_mv_plus_cash versus to gross exposure",
             [{"op": "compare", "against": "canonical net_mv_plus_cash"}],
             {"per_account_difference": N("L-ZERO-DIFF"), "printed_as": "counts only"},
             [{"op": "compare", "against": "gross exposure"}],
             {"per_account_difference": None, "nonzero_for_accounts_with_short_or_margin": True,
              "printed_as": "counts only"},
             ["per_account_difference"]),
        environment="AUTHORIZED", executes_in="not the local harness: authorized dated-source reads", readings=["R12"])

    # ---- A05 honest incompleteness
    a05 = [
        ("A05-01", "remove a claimed account at Schwab", ["c1", "c3"],
         [{"op": "remove_record", "fixture": "CUS-BASE", "account": "K2"},
          {"op": "remove_record", "fixture": "CAN-BASE", "account": "K2", "business_date": "2026-09-14"}],
         K2_UNRESOLVED("MISSING_CUSTODIAN", "MISSING_CUSTODIAN"), "MISSING_CUSTODIAN"),
        ("A05-02", "invalidate an identified Traded value", ["c1", "c4"],
         [set_cell(["SNAP-S1"], "r3", "Traded", "Maybe")],
         {"business_active_accounts": None, "reason_codes_include": ["TRADED_STATUS_UNVERIFIED"],
          "accounts": {"K2": {"business_status": "CONFLICT", "membership_date_status": "OBSERVED_TRADED"}},
          "tax": {"value_status": "COMPLETE", "complete_value": N("L-TAX-D14")}}, "TRADED_STATUS_UNVERIFIED"),
        ("A05-03", "request a date before trustworthy membership history", ["c1", "c4"],
         [{"op": "set_run", "valuation_date": "2026-09-11"}],
         {"expected_accounts": None, "reason_codes_include": ["TRADED_HISTORY_UNVERIFIED"],
          "membership_date_status_by_key": {"K1": "UNVERIFIED", "K2": "UNVERIFIED", "K3": "UNVERIFIED"},
          "tax": {"value_status": "UNAVAILABLE", "complete_value": None}, "shown_as_zero": False},
         "TRADED_HISTORY_UNVERIFIED"),
        ("A05-04", "fail the existing source schema", ["c1", "c4"],
         [{"op": "rename_header", "snapshots": ["SNAP-S1"], "from": "Traded", "to": "Traded Status"}],
         {"capability_error": "SOURCE_SCHEMA_INVALID", "business_active_accounts": None,
          "reason_codes_include": ["SOURCE_SCHEMA_INVALID"], "last_good_snapshot": "SNAP-S0",
          "current_census_empty": False}, "SOURCE_SCHEMA_INVALID"),
        ("A05-05", "deny capability access", ["c1", "c4"],
         [{"op": "gateway_state", "delegated_principal": "revoked"}],
         {"capability_error": "AUTH_REQUIRED", "freshness": "AUTH_REQUIRED", "reason_codes_include": ["AUTH_REQUIRED"],
          "business_active_accounts": None, "last_good_snapshot": "SNAP-S0", "last_successful_snapshot_date": "2026-09-14",
          "retained_prior_cohort": N("N-K1K2K3"), "empty_workbook_manufactured": False}, "AUTH_REQUIRED"),
        ("A05-06", "stale a source", ["c1", "c4"],
         [{"op": "truncate_after", "fixture": "CAN-BASE", "last_business_date": "2026-09-14"},
          {"op": "set_run", "valuation_date": "2026-09-15", "knowledge_date": "2026-09-16"}],
         {"freshness": "STALE", "reason_codes_include": ["SOURCE_STALE"], "last_complete_date": "2026-09-14",
          "tax": {"complete_value": None, "historical_display_value": N("L-TAX-D14"),
                  "historical_display_date": "2026-09-14"}}, "SOURCE_STALE"),
        ("A05-07", "omit overlap evidence", ["c1", "c4"],
         [{"op": "remove_fixture", "fixture": "POP-BASE"}],
         {"reason_codes_include": ["BASE_OVERLAP_UNVERIFIED"], "tax": {"complete_value": None},
          "affected_complete_totals": NULLS(), "unchanged": UNCH(), "passed_by_absence": False}, "BASE_OVERLAP_UNVERIFIED"),
        ("A05-08", "break the calendar", ["c1", "c4"],
         [{"op": "remove_fixture", "fixture": "CAL-BASE"}],
         {"reason_codes_include": ["CALENDAR_UNAVAILABLE"], "valuation_date": None, "weekday_subtraction_used": False,
          "tax": {"complete_value": None}}, "CALENDAR_UNAVAILABLE"),
    ]
    healthy = dict(K2_MATCHED(), freshness="CURRENT", reason_codes_include=[], valuation_date="2026-09-14")
    for aid, member, clauses, delta, obs, reason in a05:
        o = dict(obs)
        o["rendered_reason_codes"] = [reason]
        h = dict(healthy, rendered_reason_codes=[])
        arm(aid, clauses, f"{member}: the limitation is visible, distinct and dated", ["S02", "S03", "S04", "S05", "S07", "S08", "S09", "S10"],
            FI(), diff(f"{member} versus the healthy fixture", delta, o, [], h, ["rendered_reason_codes"]),
            members=[member], readings=["R3"] if aid == "A05-02" else ["R9"] if aid == "A05-05" else [])
    arm("A05-09", ["c2"], "the eight reasons stay distinct through the rendered consumer", ["S08", "S09", "S10", "S11"],
        {"runs": [f"A05-0{i}" for i in range(1, 9)]},
        diff("the consumer renders each reason code versus a consumer that collapses them to one 'unavailable'",
             [{"op": "render", "consumer": "TX-c-2 CategoryViewTree"}],
             {"distinct_rendered_reason_sets": N("N-A05-REASONS")},
             [{"op": "render", "consumer": "mutant collapsing reasons"}],
             {"distinct_rendered_reason_sets": N("N-A05-COLLAPSED")},
             ["distinct_rendered_reason_sets"]))
    arm("A05-10", ["c4"], "an uncertain census or date shows null, never zero", ["S07", "S08", "S10", "S11"],
        {"runs": ["A05-02", "A05-03", "A05-04", "A05-05", "A05-06", "A05-07", "A05-08"]},
        diff("nulls carried with their coverage versus a mutant coercing null to 0",
             [], {"unknown_rendered_as_zero": N("N-NONE"), "null_carries_coverage": True},
             [{"op": "mutant", "coerce_null_to_zero": True}],
             {"unknown_rendered_as_zero": N("N-ONE-HIT"), "null_carries_coverage": False},
             ["unknown_rendered_as_zero", "null_carries_coverage"]))
    k5 = [{"op": "append_row", "snapshots": ["SNAP-S1"], "before": "r8",
           "cells": {"Index": 7, "Account Number": "99000005", "Strategy": "SYNTH-TAX-STRATEGY", "Traded": "Yes"}},
          {"op": "add_record", "fixture": "CUS-BASE", "account": "K5"}]
    arm("A05-11", ["c5"], "the page distinguishes the source-dated business count from valuation-dated counts",
        ["S08", "S09", "S10", "S11"], FI(),
        diff("K5 discovered at SNAP-S1 (the counts diverge) versus no K5",
             k5, {"business_active_accounts": N("N-K1K2K3K5"), "business_count_label_date": "2026-09-15T13:30:00Z",
                  "expected_accounts": None, "covered_accounts": N("N-K1K2K3"), "dated_count_label_date": "2026-09-14",
                  "labels_distinct": True},
             [], {"business_active_accounts": N("N-K1K2K3"), "business_count_label_date": "2026-09-15T13:30:00Z",
                  "expected_accounts": N("N-K1K2K3"), "covered_accounts": N("N-K1K2K3"),
                  "dated_count_label_date": "2026-09-14", "labels_distinct": True},
             ["business_active_accounts", "expected_accounts"], ["labels_distinct", "dated_count_label_date"]))
    arm("A05-12", ["c6"], "correcting the missing input restores only the eligibility its evidence and date justify",
        ["S04", "S05"], FI(knowledge="2026-09-16", history=("SNAP-S0", "SNAP-S1", "SNAP-S2")),
        diff("K2's canonical 2026-09-14 row restored at knowledge 2026-09-16 versus still missing",
             [{"op": "remove_record", "fixture": "CAN-BASE", "account": "K2", "business_date": "2026-09-14",
               "until_knowledge_date": "2026-09-15"}],
             {"by_valuation_date": {"2026-09-14": {"value_status": "COMPLETE", "complete_value": N("L-TAX-D14")},
                                    "2026-09-11": {"value_status": "UNAVAILABLE", "complete_value": None,
                                                   "reason_codes_include": ["TRADED_HISTORY_UNVERIFIED"]}},
              "restored_observation_supersedes": True},
             [{"op": "remove_record", "fixture": "CAN-BASE", "account": "K2", "business_date": "2026-09-14"}],
             {"by_valuation_date": {"2026-09-14": {"value_status": "INCOMPLETE", "complete_value": None},
                                    "2026-09-11": {"value_status": "UNAVAILABLE", "complete_value": None,
                                                   "reason_codes_include": ["TRADED_HISTORY_UNVERIFIED"]}},
              "restored_observation_supersedes": False},
             ["by_valuation_date.2026-09-14.complete_value"], ["by_valuation_date.2026-09-11"]))

    # ---- A06 additive arithmetic
    on = {"tax_leaf": N("L-TAX-D14"), "sma": N("L-SMA-AFTER"), "alt_strategies": N("L-ALT-AFTER"),
          "49financial": N("L-49F-AFTER"), "global": N("L-GLOBAL-AFTER"), "global_tax_leaf": N("L-GLOBAL-TAX-LEAF"),
          "delta": {"sma": N("L-SMA-DELTA"), "alt_strategies": N("L-ALT-DELTA"), "49financial": N("L-49F-DELTA"),
                    "global": N("L-GLOBAL-DELTA")},
          "aggregate_basis": "INCLUDES_ADDITIVE", "base_excluding_tax_aua": N("L-49F-BEFORE"),
          "tax_additive_aua": N("L-TAX-D14"), "tax_source_basis": "ADDITIVE",
          "values_not": {"49financial": N("L-49F-DOUBLE-ADD-WRONG"), "global": N("L-GLOBAL-DOUBLE-ADD-WRONG")},
          "unchanged": UNCH()}
    off = {"tax_leaf": None, "sma": N("L-SMA-BEFORE"), "alt_strategies": N("L-ALT-BEFORE"), "49financial": N("L-49F-BEFORE"),
           "global": N("L-GLOBAL-BEFORE"), "global_tax_leaf": None, "unchanged": UNCH()}
    arm("A06-01", ["c1"], "known Tax cents add exactly once to Tax, SMA, ALT Strategies, 49financial and Global",
        ["S06", "S07"], FI(),
        diff("the complete Tax contribution versus the fixed synthetic baseline with no Tax member",
             [], on, [{"op": "use_baseline_without_tax"}], off,
             ["tax_leaf", "sma", "alt_strategies", "49financial", "global"], ["unchanged"]),
        members=["Tax", "SMA", "ALT Strategies", "49financial", "Global"])
    arm("A06-02", ["c2"], "Client and other firms stay unchanged", ["S06", "S07"], FI(),
        inv("the Tax contribution versus the baseline without it",
            [], {"unchanged": UNCH(), "delta": {"client": N("L-CLIENT-DELTA"), "other_firm_1": N("L-OF1-DELTA"),
                                                 "other_firm_2": N("L-OF2-DELTA")}},
            [{"op": "use_baseline_without_tax"}], {"unchanged": UNCH(), "delta": {"client": N("L-CLIENT-DELTA"),
                                                  "other_firm_1": N("L-OF1-DELTA"), "other_firm_2": N("L-OF2-DELTA")}},
            ["unchanged", "delta"], "A06-01"))
    blocked = {"tax": {"complete_value": None}, "affected_complete_totals": NULLS(), "unchanged": UNCH(),
               "netting_applied": False, "client_carve_out_applied": False}
    arm("A06-03", ["c3"], "a deliberate overlapping full ID blocks the total", ["S04", "S06", "S07"], FI(),
        diff("K1 also in the same-date base population versus disjoint populations",
             [{"op": "add_member", "fixture": "POP-BASE", "account": "K1"}],
             dict(blocked, reason_codes_include=["BASE_OVERLAP"]), [],
             {"tax": {"complete_value": N("L-TAX-D14")}, "affected_complete_totals": TOTALS(), "unchanged": UNCH(),
              "netting_applied": False, "client_carve_out_applied": False, "reason_codes_include": []},
             ["tax.complete_value", "affected_complete_totals.global"], ["unchanged"]),
        members=["overlapping full ID"])
    arm("A06-04", ["c3"], "a basis disagreement blocks the total", ["S05", "S06", "S07"], FI(),
        diff("the registry's tax source_basis set to SYNTH-NON-ADDITIVE versus ADDITIVE on both sides",
             [{"op": "set_field", "fixture": "CAT-BASE", "path": "registry.source_basis", "value": "SYNTH-NON-ADDITIVE"}],
             dict(blocked, reason_codes_include=["BASIS_MISMATCH"], contribution_refused=True), [],
             {"tax": {"complete_value": N("L-TAX-D14")}, "affected_complete_totals": TOTALS(), "unchanged": UNCH(),
              "netting_applied": False, "client_carve_out_applied": False, "reason_codes_include": [],
              "contribution_refused": False},
             ["tax.complete_value", "contribution_refused"], ["unchanged"]),
        members=["basis disagreement"])
    arm("A06-05", ["c4"], "replaying and reconstructing Global keeps tax/source_basis without a second addition",
        ["S06", "S07"], FI(),
        diff("Global reconstructed twice through the fixed-key path versus the legacy rule that adds sma_additive_aum again",
             [{"op": "reconstruct_global", "times": 2}],
             {"global": N("L-GLOBAL-AFTER"), "global_tax_leaf": N("L-GLOBAL-TAX-LEAF"), "tax_entry_present": True,
              "tax_source_basis": "ADDITIVE"},
             [{"op": "mutant", "legacy_readd_sma_additive_aum": True}],
             {"global": N("L-GLOBAL-DOUBLE-ADD-WRONG"), "global_tax_leaf": N("L-GLOBAL-TAX-LEAF"),
              "tax_entry_present": True, "tax_source_basis": "ADDITIVE"},
             ["global"], ["tax_source_basis"]))
    arm("A06-06", ["c1"], "a missing aggregate_basis declaration is a schema failure, never the old addition",
        ["S06", "S07"], FI(),
        diff("the 49financial series carries aggregate_basis=INCLUDES_ADDITIVE versus the declaration removed",
             [], {"49financial": N("L-49F-AFTER"), "schema_failure": False, "fallback_old_addition_rule_used": False},
             [{"op": "remove_field", "series": "49financial", "field": "aggregate_basis"}],
             {"49financial": None, "schema_failure": True, "fallback_old_addition_rule_used": False},
             ["49financial", "schema_failure"], ["fallback_old_addition_rule_used"]))


def req(**over):
    d = {"op": "request", "method": "GET", "route": "CONTRACT:capability.route", "bearer": "GW-BASE.route_bearer",
         "principal": {"tid": "SYNTH-TID-A", "oid": "SYNTH-OID-A", "validated": True,
                       "designation": "CONTRACT:capability.named_identity"}, "selectors": {}}
    d.update(over)
    return d


def SUCCESS():
    return {"result": "SUCCESS", "delegated_token_fetches": N("N-ONE-CALL"), "graph_requests_nonzero": True,
            "rows_returned": True, "audit_records": N("N-ONE-AUDIT")}


def REFUSED(err=None, generic=False):
    o = {"result": "REFUSED", "delegated_token_fetches": N("N-NONE"), "graph_requests": N("N-NONE"),
         "rows_returned": False, "audit_records": N("N-ONE-AUDIT")}
    if err:
        o["capability_error"] = err
    if generic:
        o["generic_handler_calls"] = N("N-NONE")
    return o


def arms_a07_a08() -> None:
    gw = ["S01", "S18"]
    # ---- A07 protected traceability
    arm("A07-01", ["c1"], "automatic Traded events are traceable through protected evidence", ["S03"], FI(),
        diff("S03's source events versus a mutant event record without source_event_id",
             [], {"traced_events": N("N-S0-EVENTS"), "event_fields_present": ["source_event_id", "actor", "evidence_ref",
                  "workbook_snapshot_id", "source_observed_at", "traded_value", "membership_date_basis"],
                  "untraceable_events": N("N-NONE")},
             [{"op": "mutant", "drop_field": "source_event_id"}],
             {"traced_events": N("N-NONE"), "event_fields_present": ["actor", "evidence_ref"],
              "untraceable_events": N("N-S0-EVENTS")},
             ["traced_events", "untraceable_events"]),
        members=["automatic Traded events"])
    arm("A07-02", ["c1"], "the original observed date survives a replay", ["S03"], FI(),
        diff("SNAP-S0 replayed at 2026-09-15T20:00:00Z versus a new logical observation of K4 Yes at that time",
             [{"op": "replay_snapshot", "snapshot": "SNAP-S0", "retry_at": "2026-09-15T20:00:00Z"}],
             {"k1_event_source_observed_at": "2026-09-14T13:30:00Z", "new_events": []},
             [{"op": "add_snapshot", "base": "WB-BASE", "observed_at": "2026-09-15T20:00:00Z", "set": {"r5.Traded": "Yes"}}],
             {"k1_event_source_observed_at": "2026-09-14T13:30:00Z",
              "new_events": [{"kind": "OBSERVE_TRADED", "account": "K4", "effective_date": "2026-09-15"}]},
             ["new_events"], ["k1_event_source_observed_at"]),
        members=["original observed dates"])
    arm("A07-03", ["c1"], "identity joins are traceable in protected evidence and absent from ordinary output", ["S04"], FI(),
        diff("K2's custodian record present versus deleted",
             [], {"k2_join_evidence": ["master_ref", "custodian_status", "strategy", "partition", "source_hash"],
                  "accounts": {"K2": {"identity_status": "EXACT_MATCH"}}, "join_evidence_in_ordinary_json": False},
             [{"op": "remove_record", "fixture": "CUS-BASE", "account": "K2"}],
             {"k2_join_evidence": ["partition searched", "source_hash"],
              "accounts": {"K2": {"identity_status": "MISSING_CUSTODIAN"}}, "join_evidence_in_ordinary_json": False},
             ["accounts.K2.identity_status", "k2_join_evidence"], ["join_evidence_in_ordinary_json"]),
        members=["identity joins"])
    arm("A07-04", ["c1"], "publication is traceable and a status-only change republishes", ["S08"], FI(),
        diff("the control state gains a CORRECTION_PENDING status while numerical Gold bytes are unchanged, versus no change",
             [{"op": "set_control", "freshness": "CORRECTION_PENDING", "correction_pending_since": "2026-09-15"}],
             {"served_generation_changed": True, "numerical_values_changed": False, "freshness": "CORRECTION_PENDING",
              "publication_manifest_links": ["gold parquet sha256", "control state version", "served generation"]},
             [], {"served_generation_changed": False, "numerical_values_changed": False, "freshness": "CURRENT",
                  "publication_manifest_links": ["gold parquet sha256", "control state version", "served generation"]},
             ["served_generation_changed", "freshness"], ["numerical_values_changed"]),
        members=["publication"])
    arm("A07-05", ["c2"], "ordinary JSON, page and logs carry no names, full IDs, row values or tokens",
        ["S01", "S08", "S10", "S11"], FI(),
        diff("the privacy boundary intact versus one planted value of each class in a log",
             [], {"hits_in_ordinary_outputs": {"names": N("N-NONE"), "full_ids": N("N-NONE"),
                                               "row_values": N("N-NONE"), "tokens": N("N-NONE")}},
             [{"op": "plant_token", "target": "run log", "values": ["SYNTH-NAME-01", "KEYS.K1.full", "SYNTH-COMMENT-01",
                                                                       "GW-BASE.delegated_token"]}],
             {"hits_in_ordinary_outputs": {"names": N("N-ONE-HIT"), "full_ids": N("N-ONE-HIT"),
                                           "row_values": N("N-ONE-HIT"), "tokens": N("N-ONE-HIT")}},
             ["hits_in_ordinary_outputs.names", "hits_in_ordinary_outputs.tokens"]),
        members=["names", "full IDs", "row values", "tokens"])
    controls = [
        ("A07-06", "Wrong identity", [req(principal={"tid": "SYNTH-TID-B", "oid": "SYNTH-OID-B", "validated": True,
                                                    "designation": "SYNTH-OTHER-DESIGNATION"})], REFUSED("AUTH_REQUIRED"), []),
        ("A07-07", "route", [req(route="/ms/taxsma-workbooks"), req(route="/ms/taxsma-workbook/rows")], REFUSED(), ["R6"]),
        ("A07-08", "method", [req(method="POST"), req(method="PUT"), req(method="DELETE")], REFUSED(), ["R6"]),
        ("A07-09", "bearer", [req(bearer="SYNTH-WRONG-BEARER")], REFUSED("UNAUTHORIZED_CAPABILITY"), []),
        ("A07-10", "workbook", [req(selectors={"item_id": "SYNTH-OTHER-ITEM"}), req(selectors={"sheet": "Sheet2"}),
                                req(selectors={"range": "A1:B2"}), req(selectors={"site_id": "SYNTH-OTHER-SITE"}),
                                req(selectors={"url": "SYNTH-OTHER-URL"})], REFUSED(), ["R6"]),
        ("A07-12", "revoked", [dict(req(), capability_state="revoked")], REFUSED("UNAUTHORIZED_CAPABILITY"), []),
    ]
    for aid, member, bad, obs, rd in controls:
        arm(aid, ["c3"], f"the {member.lower()} control fails before any delegated token or Graph request", gw, FI(),
            diff(f"{member.lower()} varied versus the exact valid request", bad, obs, [req()], SUCCESS(),
                 ["result", "rows_returned", "delegated_token_fetches"], ["audit_records"]),
            members=[member], readings=rd)
    arm("A07-11", ["c3"], "a denied SharePoint access fails after the token fetch and is recorded as such", gw, FI(),
        diff("the synthetic Graph returns accessDenied for the configured item versus serves it",
             [req(), {"op": "graph_state", "item_access": "denied"}],
             {"result": "REFUSED", "delegated_token_fetches": N("N-ONE-CALL"), "graph_requests": N("N-ONE-CALL"),
              "rows_returned": False, "audit_records": N("N-ONE-AUDIT"), "audit_result_distinct_from_guard_denial": True},
             [req()], SUCCESS(), ["result", "rows_returned"], ["delegated_token_fetches"]),
        members=["denied"], readings=["R5"])
    arm("A07-13", ["c4"], "the exact named identity and exact route succeed and are audited", gw, FI(),
        diff("the exact valid request versus the same request with the capability disabled",
             [req()], dict(SUCCESS(), response_fields=N("N-RESPONSE-FIELDS"), audit_fields=N("N-AUDIT-FIELDS"),
                           audit_exclusions_present=False),
             [req(), {"op": "set_config", "capability_enabled": False}],
             dict(REFUSED(), response_fields=None, audit_fields=N("N-AUDIT-FIELDS"), audit_exclusions_present=False),
             ["result", "rows_returned"], ["audit_exclusions_present"]))
    arm("A07-14", ["c5"], "exactly the seven business fields and three row metadata fields are returned", gw, FI(),
        diff("the contract projection versus a mutant projection that also returns Name",
             [req()], {"business_fields_per_row": N("N-PROJECTED"), "metadata_fields_per_row": N("N-ROW-META"),
                       "excluded_headers": N("N-EXCLUDED-HEADERS"), "excluded_values_in_response": N("N-NONE")},
             [req(), {"op": "mutant", "extra_projected_field": "Name"}],
             {"business_fields_per_row": None, "metadata_fields_per_row": N("N-ROW-META"),
              "excluded_headers": N("N-EXCLUDED-HEADERS"), "excluded_values_in_response": N("N-ONE-HIT")},
             ["excluded_values_in_response", "business_fields_per_row"], ["excluded_headers"]))
    arm("A07-15", ["c6"], "a pre-Graph guard denial and a SharePoint access failure are two distinct results", gw, FI(),
        diff("wrong tid (guard) versus accessDenied from the synthetic Graph (SharePoint)",
             [req(principal={"tid": "SYNTH-TID-B", "oid": "SYNTH-OID-A", "validated": True,
                             "designation": "CONTRACT:capability.named_identity"})],
             dict(REFUSED("AUTH_REQUIRED"), denial_plane="pre-Graph guard"),
             [req(), {"op": "graph_state", "item_access": "denied"}],
             {"result": "REFUSED", "delegated_token_fetches": N("N-ONE-CALL"), "graph_requests": N("N-ONE-CALL"),
              "rows_returned": False, "audit_records": N("N-ONE-AUDIT"), "denial_plane": "SharePoint access"},
             ["graph_requests", "delegated_token_fetches", "denial_plane"], ["rows_returned"]),
        readings=["R5"])
    arm("A07-16", ["c7"], "production activation proves the exact binding and the controlled capability read", ["S16"],
        {"environment": "production activation under its release conditions (G-W, G-P, G-O)", "rows_in_record": False},
        diff("the configured validated tid/oid binding verified and the controlled GET succeeds versus the binding fails",
             [{"op": "activation_read", "binding": "configured validated pair"}],
             {"binding_verified": True, "controlled_read_result": "SUCCESS", "activated": True,
              "protected_record_fields": ["principal", "request_id", "time", "result"], "rows_or_tokens_in_record": False},
             [{"op": "activation_read", "binding": "mismatch"}],
             {"binding_verified": False, "controlled_read_result": "REFUSED", "activated": False,
              "protected_record_fields": ["principal", "request_id", "time", "result"], "rows_or_tokens_in_record": False},
             ["activated", "binding_verified"], ["rows_or_tokens_in_record"]),
        environment="PRODUCTION_ACTIVATION", executes_in="TX-r-3 (not the local harness)", readings=["R12"])
    arm("A07-17", ["c8"], "the capability guard runs before generic /ms/* dispatch", gw, FI(),
        diff("a generic MCP credential sent to the capability route versus to the generic route",
             [req(bearer="GW-BASE.generic_credentials.MCP")], REFUSED("UNAUTHORIZED_CAPABILITY", generic=True),
             [req(bearer="GW-BASE.generic_credentials.MCP", route="GW-BASE.generic_route")],
             {"result": "GENERIC_HANDLED", "generic_handler_calls": N("N-ONE-CALL"), "rows_returned": False,
              "delegated_token_fetches": N("N-NONE")},
             ["generic_handler_calls", "result"], ["rows_returned"]))
    principal_cases = [
        ("A07-18", "wrong tid", {"tid": "SYNTH-TID-B", "oid": "SYNTH-OID-A", "validated": True}),
        ("A07-19", "wrong oid", {"tid": "SYNTH-TID-A", "oid": "SYNTH-OID-B", "validated": True}),
        ("A07-20", "missing", {"tid": None, "oid": None, "validated": True}),
        ("A07-21", "unvalidated claims", {"tid": "SYNTH-TID-A", "oid": "SYNTH-OID-A", "validated": False,
                                          "source": "caller-supplied headers / unvalidated decode"}),
        ("A07-22", "revoked principal", {"tid": "SYNTH-TID-A", "oid": "SYNTH-OID-A", "validated": True, "revoked": True}),
    ]
    for aid, member, p in principal_cases:
        p = dict(p, designation="CONTRACT:capability.named_identity")
        arm(aid, ["c9"], f"same email, {member}: denied before token fetch or Graph", gw, FI(),
            diff(f"{member} with otherwise identical valid inputs versus the configured validated pair",
                 [req(principal=p)], REFUSED("AUTH_REQUIRED"), [req()], SUCCESS(),
                 ["result", "delegated_token_fetches"], ["audit_records"]),
            members=[member])
    arm("A07-23", ["c10"], "only the configured validated pair succeeds", gw, FI(),
        diff("binding by validated tid/oid versus a mutant binding by the designated email",
             [{"op": "request_each", "principals": "N-FIVE-VARIANTS, all with the same designation"}],
             {"variants": N("N-FIVE-VARIANTS"), "successes": N("N-ONE-CALL")},
             [{"op": "mutant", "bind_by": "email"}],
             {"variants": N("N-FIVE-VARIANTS"), "successes": N("N-FIVE-VARIANTS")},
             ["successes"], ["variants"]))
    for aid, member in (("A07-24", "MCP"), ("A07-25", "ms-ingest"), ("A07-26", "OTP")):
        arm(aid, ["c11"], f"a generic {member} credential cannot open the capability", gw, FI(),
            diff(f"the {member} credential versus the route-only bearer",
                 [req(bearer=f"GW-BASE.generic_credentials.{member}")], REFUSED("UNAUTHORIZED_CAPABILITY", generic=True),
                 [req()], SUCCESS(), ["result", "rows_returned"], ["audit_records"]),
            members=[member])

    # ---- A08 repeat / recovery
    arm("A08-01", ["c1"], "a duplicate invocation cannot duplicate an observation or a total", ["S05", "S07", "S08"], FI(),
        diff("a second invocation for knowledge date 2026-09-15 versus the first",
             [{"op": "invoke", "knowledge_date": "2026-09-15", "times": 2}],
             {"run_result": "NO_CHANGE", "observations_for_knowledge_date": N("N-K1K2K3"),
              "gold_objects_for_date": N("N-ONE-OBJECT"), "tax": {"complete_value": N("L-TAX-D14"),
                                                                  "complete_value_not": N("L-TAX-DOUBLED-WRONG")}},
             [{"op": "invoke", "knowledge_date": "2026-09-15", "times": 1}],
             {"run_result": "COMPLETE", "observations_for_knowledge_date": N("N-K1K2K3"),
              "gold_objects_for_date": N("N-ONE-OBJECT"), "tax": {"complete_value": N("L-TAX-D14"),
                                                                  "complete_value_not": N("L-TAX-DOUBLED-WRONG")}},
             ["run_result"], ["observations_for_knowledge_date", "gold_objects_for_date", "tax.complete_value"]))
    for aid, member, act in (("A08-02", "Corrupt", "corrupt_object"), ("A08-03", "delete", "delete_object")):
        arm(aid, ["c2"], f"{member.lower()} a local served artifact with unchanged source hash: the same publisher repairs it",
            ["S08"], FI(),
            diff(f"{member.lower()} the local 49financial category-views.json versus the destination intact",
                 [{"op": act, "target": "local served 49financial category-views.json"}],
                 {"destination_check": "DESTINATION_MISMATCH", "repaired_by": "opal-assets-mdpf-portal-publisher",
                  "destination_rewritten": True, "readback_matches_generation": True, "writers": N("N-ONE-WRITER"),
                  "reason_codes_include": ["DESTINATION_MISMATCH"]},
                 [], {"destination_check": "MATCH", "repaired_by": None, "destination_rewritten": False,
                      "readback_matches_generation": True, "writers": N("N-ONE-WRITER"), "reason_codes_include": []},
                 ["destination_rewritten", "destination_check"], ["readback_matches_generation", "writers"]),
            members=[member])
    arm("A08-04", ["c3", "c4"], "a mid-run failure is visible and recovery preserves history, dates and one writer",
        ["S05", "S07", "S08", "S15"], FI(),
        diff("a failure injected after S05 creates the 2026-09-15 object and before S07, then a retry, versus no failure",
             [{"op": "fail_stage", "stage": "S07", "after": "S05 object created"}, {"op": "retry"}],
             {"first_run_result": "FAILED", "first_run_reason_codes": ["RUNTIME_FAILED"],
              "served_before_retry": "prior generation kept, never a complete-looking zero",
              "retry_s05_run_result": "NO_CHANGE", "final_run_result": "COMPLETE",
              "observations_for_knowledge_date": N("N-K1K2K3"), "gold_objects_for_date": N("N-ONE-OBJECT"),
              "writers": N("N-ONE-WRITER"), "tax": {"complete_value": N("L-TAX-D14")}, "unchanged": UNCH()},
             [], {"first_run_result": "COMPLETE", "first_run_reason_codes": [], "served_before_retry": None,
                  "retry_s05_run_result": None, "final_run_result": "COMPLETE",
                  "observations_for_knowledge_date": N("N-K1K2K3"), "gold_objects_for_date": N("N-ONE-OBJECT"),
                  "writers": N("N-ONE-WRITER"), "tax": {"complete_value": N("L-TAX-D14")}, "unchanged": UNCH()},
             ["first_run_result", "first_run_reason_codes"],
             ["final_run_result", "observations_for_knowledge_date", "gold_objects_for_date", "writers", "tax.complete_value"]))
    arm("A08-05", ["c3", "c4"], "a pending same-day correction queues for the next partition and keeps both observations",
        ["S05", "S07", "S08"], FI(knowledge="2026-09-15"),
        diff("K2's 2026-09-14 value restated at 2026-09-15T18:00:00Z after the 2026-09-15 object exists versus no restatement",
             [{"op": "set_field", "fixture": "CAN-BASE", "account": "K2", "business_date": "2026-09-14",
               "field": "net_mv_plus_cash", "value": "820500.10", "amount_id": "AMT-K2-NET-RESTATED",
               "at": "2026-09-15T18:00:00Z"}, {"op": "invoke", "knowledge_date": "2026-09-15"},
              {"op": "invoke", "knowledge_date": "2026-09-16"}],
             {"same_day_run_result": "CORRECTION_QUEUED", "freshness_before_next_partition": "CORRECTION_PENDING",
              "correction_pending_since": "2026-09-15", "served_value_before_next_partition": N("L-TAX-D14"),
              "object_2026_09_15_unchanged": True, "k2_observations_for_2026_09_14": N("N-OLD-NEW-OBS"),
              "resolved_complete_value": N("L-TAX-RESTATED"), "restatement": N("L-RESTATEMENT-DELTA")},
             [{"op": "invoke", "knowledge_date": "2026-09-15"}, {"op": "invoke", "knowledge_date": "2026-09-16"}],
             {"same_day_run_result": "NO_CHANGE", "freshness_before_next_partition": "CURRENT",
              "correction_pending_since": None, "served_value_before_next_partition": N("L-TAX-D14"),
              "object_2026_09_15_unchanged": True, "k2_observations_for_2026_09_14": N("N-ONE-OBS"),
              "resolved_complete_value": N("L-TAX-D14"), "restatement": None},
             ["same_day_run_result", "k2_observations_for_2026_09_14", "resolved_complete_value"],
             ["object_2026_09_15_unchanged", "served_value_before_next_partition"]))
    arm("A08-06", ["c4"], "recovery cannot mint a second same-date leaf", ["S05", "S15"], FI(),
        diff("an operator retry through the same producer versus a mutant retry that writes a new same-date leaf",
             [{"op": "retry", "through": "same producer"}],
             {"gold_objects_for_date": N("N-ONE-OBJECT"), "dates_changed": False, "writers": N("N-ONE-WRITER")},
             [{"op": "mutant", "retry_writes_new_leaf": True}],
             {"gold_objects_for_date": N("N-TWO-OBJECTS"), "dates_changed": False, "writers": N("N-ONE-WRITER")},
             ["gold_objects_for_date"], ["writers"]))
    arm("A08-07", ["c5"], "disable and restore the extension: the affected display changes, non-Tax results do not",
        ["S07", "S08", "S10", "S11"], FI(),
        diff("the extension disabled versus restored",
             [{"op": "disable_extension"}],
             {"run_result": "DISABLED", "reason_codes_include": ["DISABLED"], "tax": {"complete_value": None,
              "historical_display_date": "2026-09-14"}, "affected_complete_totals": NULLS(), "unchanged": UNCH(),
              "shown_as_zero": False},
             [{"op": "disable_extension"}, {"op": "enable_extension"}],
             {"run_result": "COMPLETE", "reason_codes_include": [], "tax": {"complete_value": N("L-TAX-D14"),
              "historical_display_date": None}, "affected_complete_totals": TOTALS(), "unchanged": UNCH(),
              "shown_as_zero": False},
             ["run_result", "tax.complete_value", "affected_complete_totals.global"], ["unchanged", "shown_as_zero"]))


CLAUSE_MEMBERS = {
    "A01.c1": ["traded", "funded-but-untraded", "prospect", "blank", "conflict rows"],
    "A01.c3": ["Ready", "funding"],
    "A01.c6": ["invalid YES identities", "unknown identified Traded"],
    "A01.c7": ["Reordered", "inserted rows", "Bronze/Silver replay"],
    "A02.c2": ["suffix-only", "masked", "duplicate", "malformed", "master", "strategy", "transfer"],
    "A03.c5": ["explicit NO exclusive closure", "reactivation", "same-day ordering", "idempotent replay",
               "out-of-order refusal", "invalid/blank Traded", "removed/rekeyed claims"],
    "A04.c1": ["cash", "long/short exposure", "margin", "actual zero"],
    "A04.c3": ["Gross exposure", "sales estimate", "quarterly data", "unverified accrual"],
    "A05.c1": ["remove a claimed account at Schwab", "invalidate an identified Traded value",
               "request a date before trustworthy membership history", "fail the existing source schema",
               "deny capability access", "stale a source", "omit overlap evidence", "break the calendar"],
    "A06.c1": ["Tax", "SMA", "ALT Strategies", "49financial", "Global"],
    "A06.c3": ["overlapping full ID", "basis disagreement"],
    "A07.c1": ["automatic Traded events", "original observed dates", "identity joins", "publication"],
    "A07.c2": ["names", "full IDs", "row values", "tokens"],
    "A07.c3": ["Wrong identity", "route", "method", "bearer", "workbook", "denied", "revoked"],
    "A07.c9": ["wrong tid", "wrong oid", "missing", "unvalidated claims", "revoked principal"],
    "A07.c11": ["MCP", "ms-ingest", "OTP"],
    "A08.c2": ["Corrupt", "delete"],
}

READINGS = {
    "R1": "Duplicate rows of one full key with the same Yes: the PRD fixes 'count once, retain conflict' and S04's "
          "DUPLICATE_ACCOUNT, not which business_status the duplicate rows carry, so that value is not asserted; the key "
          "is valid, so the dated expected count stays known (3) with K2 unresolved.",
    "R2": "An invalid identity or an unknown Traded on a Yes/identified claim leaves the identity/membership census "
          "unresolved, so expected_accounts is null as well as business_active_accounts; covered/unresolved enumerate the "
          "known claims.",
    "R3": "An invalid Traded observed after a proven Yes never closes the interval, so a valuation date the history "
          "already proves (2026-09-14, proven by SNAP-S0) keeps its complete value while the current count is null.",
    "R4": "PRD s.3.4's candidate label UNCONFIRMED has no contract enumeration member (row MDPF_TAXSMA-W5-S1); the "
          "candidate observable is stated without a status label.",
    "R5": "The contract fixes no error code for a SharePoint denial after the token fetch; the arms fix what makes it "
          "distinct from a guard denial: one token fetch, one Graph request and a distinct audit result.",
    "R6": "The contract fixes no error code for a wrong route, wrong method or a caller selector; the arms fix the "
          "refusal, zero token fetches, zero Graph requests and no rows.",
    "R7": "A Gold run at 13:30 UTC on knowledge date X values the latest exchange session strictly before X (PRD s.3.8 "
          "'expected completed session'); weekends and holidays advance knowledge, never the valuation date.",
    "R8": "Master identities are referenced by contract path (CONTRACT:identity.*), never as digits, so no real "
          "identifier enters the manifest.",
    "R9": "'Deny capability access' is exercised as the Gateway reporting AUTH_REQUIRED for a revoked delegated "
          "principal; the pipeline carries AUTH_REQUIRED (reason_codes has no UNAUTHORIZED_CAPABILITY).",
    "R10": "After CONFIRM_TRANSFER the arm asserts only that TRANSFER_UNRESOLVED clears and the current count is known; "
           "K9's dated coverage for dates before its own observation is not asserted.",
    "R11": "Weekend knowledge runs value the prior Friday session and produce no valuation date for Saturday or Sunday.",
    "R12": "A04-10 (authorized dated-source cases) and A07-16 (production activation) are not local-harness arms; "
           "their observables are rules and aggregate counts, with no value or identifier in the repository.",
    "R13": "A valuation date earlier than any trustworthy history leaves expected_accounts null (unknown), never zero.",
    "R14": "The fixture carries the explicit Total marker in the Index column; the contract fixes that the marker is "
           "unique and explicit, not which column carries it.",
    "R15": "A FLOAT-kind Excel scalar equal to an integral eight-digit value is left unasserted (the contract both admits "
           "finite integral Excel numbers and forbids coercing a float); the INTEGER kind is asserted as accepted.",
    "R16": "Same-UTC-day transitions: the day's latest accepted state governs that valuation date; every event is retained.",
    "R17": "The legacy CONFIRM_EFFECTIVE_MEMBERSHIP kind appears only in an arm's input, never in an expected observable, "
           "because it is not a current contract disposition kind.",
    "R18": "The accrual placeholder is carried as a limitation; an unverified accrual is never added to the value.",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    root = repo_root()
    prd = git_show(root, PRD_COMMIT, PRD_PATH)
    contract = json.loads(git_show(root, CONTRACT_COMMIT, CONTRACT_PATH))
    clauses = prd_clauses(prd)
    fixtures, amounts, led = build_world(contract)
    ARMS.clear()
    arms_a01_a03()
    arms_a04_a06()
    arms_a07_a08()
    for a in ARMS:
        a["fixture_input_sha256"] = hashlib.sha256(json.dumps(a["fixture_input"], sort_keys=True, separators=(",", ":"),
                                                              ensure_ascii=True).encode("ascii")).hexdigest()
    clause_text = {f"{p}.c{i}": c for p, v in clauses.items() for i, c in enumerate(v["clauses"], 1)}
    summary = {}
    for p in sorted(clauses):
        mine = [a for a in ARMS if a["property"] == p]
        summary[p] = {"outcome": clauses[p]["outcome"], "clauses": len(clauses[p]["clauses"]), "arms": len(mine),
                      "local_arms": sum(1 for a in mine if a["environment"] == "LOCAL"),
                      "difference_controls": sum(1 for a in mine if a["control"]["kind"] == "DIFFERENCE"),
                      "invariance_controls": sum(1 for a in mine if a["control"]["kind"] == "INVARIANCE")}
    fixtures["amounts"] = amounts
    manifest = {
        "manifest": "MDPF_TAXSMA expected cases, PRD s.4 A01-A08 (S14, cell TX-v-1)",
        "schema_version": "1.0",
        "authored_by": "0.9.0_WK_MDPF_TAXSMA~5",
        "task_order": TO_PATH,
        "generator": GENERATOR_REL,
        "independence": "standard library only; no TAXSMA engine module imported; expectations derived from the PRD "
                        "and data-contract text read at the pinned commits",
        "prd_ref": {"path": PRD_PATH, "commit": PRD_COMMIT, "section": "4"},
        "contract_ref": {"path": CONTRACT_PATH, "version": contract["version"], "commit": CONTRACT_COMMIT},
        "decomp_ref": {"path": DECOMP_PATH, "commit": DECOMP_COMMIT, "cell": "TX-v-1"},
        "environments": {"LOCAL": "controlled local artifacts in the TX-v-2 harness; certifies no live deployment",
                         "AUTHORIZED": "authorized dated-source reads; aggregate results only",
                         "PRODUCTION_ACTIVATION": "TX-r-3 under its release conditions"},
        "conventions": {"number_references": "every expected number is {\"num\": <ledger id>}; the ledger records "
                                             "its Decimal arithmetic", "control_kinds": {
                            "DIFFERENCE": "engaged and disengaged observables must differ on every differs_on path "
                                          "and agree on every invariant_within path",
                            "INVARIANCE": "engaged and disengaged observables agree on every invariant_on path; the "
                                          "named contrast_arm is a DIFFERENCE arm that shows the harness can move"},
                        "fixture_input_sha256": "sha256 of the arm's fixture_input as canonical JSON (sorted keys, "
                                                "compact separators, ASCII); output hashes are the executing harness's",
                        "inputs": "control inputs are declarative deltas applied to the fixture_input"},
        "segmentation_rule": SEGMENTATION_RULE,
        "prd_clause_text": clause_text,
        "clause_members": CLAUSE_MEMBERS,
        "summary": summary,
        "readings": READINGS,
        "fixture_world": fixtures,
        "ledger": led.entries,
        "arms": ARMS,
    }
    out = Path(args.out) if args.out else root / OUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="ascii", newline="\n") as fh:
        fh.write(json.dumps(manifest, indent=1, ensure_ascii=True) + "\n")
    print(f"OK: wrote {out} -- {len(ARMS)} arms, {len(led.entries)} ledger entries, "
          f"{sum(len(v['clauses']) for v in clauses.values())} PRD clauses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
