"""TO-DB-b-48 sample identity: the lots stage's three tables for a SAMPLE of accounts, unbatched vs batched, sha256 of each.

Usage (from the worktree root): python <this file> <day> <sample_count> <batch_size> <out.json>
S3 reads only. The sample is the accounts holding a repeated realized lot id that day plus <sample_count> more drawn (seeded) from the
handler's own population; the tables are written as parquet under .scratch and hashed. Counts and hashes only.
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))
import handler as h  # noqa: E402

aal, ard = h.aal, h.ard


def main(day, count, batch, out):
    import boto3
    s3 = boto3.client("s3")
    doc = ard.load_declaration()
    src = ard.source_entry(doc, ard.declared_sources(doc)[0])
    spec = aal.lot_spec(src)["realized"]
    pad = int(src.get("account_id_zero_pad") or 0)
    frame = aal.read_day(s3, src, spec["table"], day)
    ids = frame[spec["close_id"]].astype(str) + "/" + frame[spec["open_id"]].astype(str)
    rep = sorted({aal._account(v, pad) for v in frame[ids.duplicated(keep=False)][spec["account"]]})
    accounts, population = aal.sample_accounts(s3, rep, int(count), 20261008)
    days = [day]
    un_tables, un_run = aal.compute_local(s3, days, accounts, workers=12, log=lambda m: None)
    ba_tables, ba_run = aal.compute_local_batched(s3, days, accounts, batch_size=int(batch), workers=12, log=lambda m: None)
    rec = {"day": day, "population_count": population, "accounts_in_sample": len(accounts),
           "accounts_with_a_repeated_realized_id_in_sample": len(rep), "batch_size": int(batch),
           "batches": -(-len(accounts) // int(batch)), "tables": {}}
    tmp = Path(tempfile.mkdtemp(prefix="b48_", dir=str(ROOT / ".scratch")))
    for t in aal.TABLES:
        sums = []
        for label, tabs in (("unbatched", un_tables), ("batched", ba_tables)):
            p = tmp / ("%s_%s.parquet" % (label, t))
            n = aal.write_parquet(t, tabs[t], p)
            sums.append((n, hashlib.sha256(p.read_bytes()).hexdigest()))
        rec["tables"][t] = {"rows_unbatched": sums[0][0], "rows_batched": sums[1][0], "sha256_unbatched": sums[0][1],
                            "sha256_batched": sums[1][1], "identical": sums[0] == sums[1]}
    rec["all_identical"] = all(v["identical"] for v in rec["tables"].values())
    rec["run_audit_counts"] = {
        "lots_audited_unbatched": len(un_run["lot_audit"]), "lots_audited_batched": len(ba_run["lot_audit"]),
        "inkind_legs_unbatched": un_run["inkind_legs"], "inkind_legs_batched": ba_run["inkind_legs"],
        "lot_tie_control_equal": un_run["lot_tie_control"] == ba_run["lot_tie_control"]}
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec))


if __name__ == "__main__":
    main(*sys.argv[1:5])
