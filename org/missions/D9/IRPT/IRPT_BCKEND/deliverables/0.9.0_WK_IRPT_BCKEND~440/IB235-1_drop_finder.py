#!/usr/bin/env python3
"""IB-pr-604 (TO IRPT_BCKEND.TO-IB-pr-604) -- locate the STAGE and the KEY CATEGORY at which the one account of class
in_source_with_positions is dropped from the 49 Financial candidate. A COPY of the set-up lines of the IB-pr-584 anatomy
harness (IB220-1) and of the IB-pr-602 driver (IB233-1), extended with a stage trace. READ-ONLY: only get_object,
head_object and list_objects_v2 pass the wrapper; every other S3 call raises. Nothing is landed, written or published.

Prints COUNTS, STAGE NAMES, and KEY CATEGORIES (type names, lengths, shape flags) only. No account id, security
identifier, name or value is printed or written to any file.

    python IB235-1_drop_finder.py <scratch_tree_root> <worktree_root>
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

READ_OPS = ("get_object", "head_object", "list_objects_v2")


class ReadOnlyS3:
    """Wraps the boto3 S3 client: a read operation passes; any other attribute raises (a write is refused)."""

    def __init__(self, client):
        self._client = client
        self.refused = Counter()

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        if name == "get_paginator":
            def paginator(operation_name, *args, **kwargs):
                if operation_name not in READ_OPS:
                    self.refused["get_paginator:" + str(operation_name)] += 1
                    raise RuntimeError("READ-ONLY guard: refused paginator %s" % operation_name)
                return self._client.get_paginator(operation_name, *args, **kwargs)
            return paginator
        if name not in READ_OPS:
            self.refused[name] += 1
            raise RuntimeError("READ-ONLY guard: refused S3 call %s" % name)
        return getattr(self._client, name)


def shape(value):
    """A KEY CATEGORY for one raw key value: its type, its length and shape flags. Never the value."""
    text = str(value)
    stripped = text.strip()
    flags = []
    if text != stripped:
        flags.append("whitespace")
    if any(c.islower() for c in stripped):
        flags.append("lowercase")
    if any(not c.isalnum() for c in stripped):
        flags.append("non_alnum")
    if stripped.endswith(".0"):
        flags.append("float_suffix")
    if stripped.startswith("0") and len(stripped) > 1:
        flags.append("leading_zero")
    return "type=%s len=%d flags=%s" % (type(value).__name__, len(text), ",".join(flags) or "none")


def key_difference(pos_raw, bal_raw):
    """The dimensions on which a position-side raw key differs from a balance-side raw key (categories only)."""
    dims = []
    if type(pos_raw) is not type(bal_raw):
        dims.append("type %s->%s" % (type(pos_raw).__name__, type(bal_raw).__name__))
    p, b = str(pos_raw).strip(), str(bal_raw).strip()
    if str(pos_raw) != str(bal_raw) and p == b:
        dims.append("whitespace_only")
    if p != b:
        if p.upper() == b.upper():
            dims.append("case")
        if p.lstrip("0") == b.lstrip("0"):
            dims.append("zero_padding")
        if p.endswith(".0") and p[:-2] == b:
            dims.append("float_suffix")
        if re.sub(r"[^0-9A-Za-z]", "", p).upper() == re.sub(r"[^0-9A-Za-z]", "", b).upper():
            dims.append("punctuation")
        if not dims:
            dims.append("other")
    return dims or ["none"]


def norm(value):
    """The loosest comparison: alphanumerics only, upper-cased, leading zeros and a float suffix removed."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return re.sub(r"[^0-9A-Za-z]", "", text).upper().lstrip("0")


def main():
    scratch = Path(sys.argv[1]).resolve()
    worktree = Path(sys.argv[2]).resolve()
    sys.path.insert(0, str(scratch / "data" / "assets" / "scripts" / "gold" / "investor_reporting"))
    import boto3
    import holdings_snapshot as hs
    import holdings_49f

    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(worktree)).decode("ascii").strip()
    print("OK: base=%s" % base)
    s3 = ReadOnlyS3(boto3.client("s3", region_name="us-east-1"))
    firm_id = "49financial"
    builder = hs.BUILDERS[firm_id]
    if builder is not holdings_49f.build_49f_meshed:
        print("ERROR: BUILDERS[49financial] is not holdings_49f.build_49f_meshed")
        sys.exit(2)
    bucket = hs.firm_bucket_map().get(firm_id, "")
    print("OK: 49financial builder is holdings_49f.build_49f_meshed; firm scope long-id equals firm key: %s"
          % (hs.lookup(firm_id)["long"] == firm_id))

    today = hs.select_business_date()
    publisher = hs.HoldingsPublication(s3, firm_id, qa=False)
    expected = publisher.begin()
    inputs = hs.VersionedInputs(s3)
    snapshot = hs.build_snapshot(firm_id, inputs, today)
    served = hs.served_publication(publisher, expected)
    closed_set = hs.closed_account_ids(s3, bucket, firm_id)
    candidate_day = (snapshot.get("clocks") or {}).get("business_date")
    print("OK: candidate_day=%s served_present=%s closed_directory_count=%d" % (candidate_day, served is not None, len(closed_set)))

    have = set((snapshot.get("scope") or {}).get("account_ids") or []) | hs._gate_account_ids(snapshot.get("nodes") or [])
    lost = set(served["account_ids"]) - have
    closed_gone = closed_set & lost
    lost_gate = lost - closed_gone
    evidence = hs.source_evidence_for(builder, firm_id, inputs, hs._absent_candidate_day(builder, snapshot),
                                      lost_ids=lost)
    exempt_ids, _details = hs.absent_at_source_exempt(lost_gate, evidence) if (evidence and lost_gate) else (set(), {})
    present = set()
    for table in hs.ABSENT_AT_SOURCE_TABLES:
        for label in ("candidate", "prior"):
            part = (((evidence or {}).get(table) or {}).get(label) or {})
            present |= set(part.get("accounts_with_positions") or ())
    in_src = (lost_gate - exempt_ids) & present
    print("OK: lost=%d closed_gone=%d exempted=%d remaining=%d in_source_with_positions=%d"
          % (len(lost), len(closed_gone), len(exempt_ids), len(lost_gate - exempt_ids), len(in_src)))
    if len(in_src) != 1:
        print("STOP: the in_source_with_positions class does not hold exactly one account (%d)" % len(in_src))
        sys.exit(3)
    target = next(iter(in_src))

    # ---- STAGE TRACE (presence of the one account at each stage; identifiers never printed) ----
    frames = holdings_49f.load_49f_sources(inputs, today)
    bal, pos, smx = frames["balance"], frames["positions"], frames["map"]
    custody_day = frames["custody_date"]
    prior_day = hs.tcal.prev_trading_day(custody_day).isoformat()
    print("OK: custody day (candidate) and prior day are the evidence's two days: %s" % (custody_day == hs._absent_candidate_day(builder, snapshot)))
    text_key = lambda raw: hs.opaque_id("account", firm_id, holdings_49f._text(raw))  # noqa: E731
    pad_key = lambda raw: hs.opaque_id("account", firm_id, hs._pad10(holdings_49f._text(raw)))  # noqa: E731
    # Per day and per table: rows whose key maps to the account under the text key (as minted) and under the pad10 key.
    day_frames = {custody_day: (bal, pos)}
    day_frames[prior_day] = (hs._read_parquet(inputs, holdings_49f.SOURCE_BUCKET, holdings_49f.SCHWAB_PREFIX + "dim_balance/date=%s/data.parquet" % prior_day),
                             hs._read_parquet(inputs, holdings_49f.SOURCE_BUCKET, holdings_49f.SCHWAB_PREFIX + "dim_position/date=%s/data.parquet" % prior_day))
    for label, day in (("candidate", custody_day), ("prior", prior_day)):
        for tname, frame in zip(("balance", "position"), day_frames[day]):
            recs = frame.to_dict("records")
            t_rows = [r for r in recs if text_key(r["account_id"]) == target]
            p_rows = [r for r in recs if pad_key(r["account_id"]) == target]
            print("STAGE 1 %s day %s: rows matching target under text key=%d, under pad10 key=%d"
                  % (label, tname, len(t_rows), len(p_rows)))
            for r in p_rows[:1]:
                print("STAGE 1 %s day %s pad10-matching key category: %s" % (label, tname, shape(r["account_id"])))
            if label == "candidate" and tname == "balance":
                bal_rows = t_rows or p_rows
            if label == "candidate" and tname == "position":
                pos_rows = t_rows or p_rows
    smx_rows = [r for r in smx.to_dict("records") if hs.opaque_id("account", firm_id, hs._pad10(r["account_number"])) == target]
    print("STAGE 1 silver allocation-map rows for the account (pad10 key): %d" % len(smx_rows))
    for r in smx_rows[:1]:
        print("STAGE 1 allocation-map key category: %s" % shape(r["account_number"]))
    bal_key_cats = Counter(shape(r["account_id"]) for r in bal.to_dict("records") if pad_key(r["account_id"]) == target)
    for c, n in bal_key_cats.items():
        print("STAGE 1 candidate-day balance key category for the account: %s rows=%d" % (c, n))
    print("STAGE 1 candidate ACCOUNT node minted under the pad10 key of the account: %s"
          % any(hs.opaque_id("account", firm_id, hs._pad10(holdings_49f._text(r["account_id"]))) in have
                for r in bal_rows if pad_key(r["account_id"]) == target))

    # Balance-side value refusal (holdings_49f.build_49f_actual refuses an account whose value is not numeric).
    refused_value = 0
    for r in bal_rows:
        for col in ("net_mv_plus_cash", "net_mv_positions"):
            try:
                holdings_49f._num(r[col])
            except holdings_49f.FortyNineRefused:
                refused_value += 1
    print("STAGE 2 balance rows refused for a non-numeric value: %d" % refused_value)
    print("STAGE 3 candidate ACCOUNT node present for the account: %s" % (target in have))

    # Key difference: the position-side raw key against the balance-side raw keys (categories only).
    bal_norm = {}
    for r in bal.to_dict("records"):
        bal_norm.setdefault(norm(holdings_49f._text(r["account_id"])), []).append(r["account_id"])
    dims = Counter()
    matches = 0
    for r in pos_rows:
        cands = bal_norm.get(norm(holdings_49f._text(r["account_id"])), [])
        if cands:
            matches += 1
            dims[" | ".join(key_difference(r["account_id"], cands[0]))] += 1
    print("STAGE 4 position rows whose loose key matches a balance key: %d of %d" % (matches, len(pos_rows)))
    for d, n in dims.most_common():
        print("STAGE 4 key difference (position vs balance): %s rows=%d" % (d, n))

    # Loose key on the candidate day: the account's prior-day custody key (or its SmartX overlay key) against every
    # candidate-day custody row, by alphanumeric content only. Categories and counts only.
    prior_t = [r for r in day_frames[prior_day][0].to_dict("records") if text_key(r["account_id"]) == target]
    ref_raw = prior_t[0]["account_id"] if prior_t else (smx_rows[0]["account_number"] if smx_rows else None)
    print("STAGE 5 reference key for the loose check: %s" % (shape(ref_raw) if ref_raw is not None else "absent"))
    if ref_raw is not None:
        ref_norm = norm(holdings_49f._text(ref_raw))
        for tname, frame in (("balance", bal), ("position", pos)):
            loose = [r for r in frame.to_dict("records") if norm(holdings_49f._text(r["account_id"])) == ref_norm]
            print("STAGE 5 candidate-day %s rows with the same loose key: %d" % (tname, len(loose)))
            for d, n in Counter(" | ".join(key_difference(r["account_id"], ref_raw)) for r in loose).most_common():
                print("STAGE 5 candidate-day %s key difference vs reference: %s rows=%d" % (tname, d, n))
    print("NEGATIVE CONTROL: the loosest norm of an identical key equals itself: %s"
          % (norm(" 0012 ") == norm("0012") == "12"))
    print("COUNTERS: refused_s3=%s" % dict(s3.refused))


if __name__ == "__main__":
    main()
