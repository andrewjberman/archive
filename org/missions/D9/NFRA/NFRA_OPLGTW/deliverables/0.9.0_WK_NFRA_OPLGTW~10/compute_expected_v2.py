"""NFRA_OPLGTW OG-v-6 -- independent instrument that computes each version 2 real-data question's
expected answer (WALKTHROUGH_PROTOCOL.md section 4, RQ2-1..RQ2-7), seals it as a salted hash and
writes the plaintext answers OUTSIDE the repository. Extends OG-v-3's compute_expected.py
(0.9.0_WK_NFRA_OPLGTW~6): same decode, same exact decimal.Decimal arithmetic, same
sha256(salt || canonical_json(answer)) digest, a fresh secrets.token_hex(32) salt.

INSTRUMENT: pyarrow.parquet (decode only -- no query, filter, group-by or aggregate) + stdlib
decimal.Decimal for every sum + Python collections. No pandas float aggregation, no DuckDB, no read
or import of infra/aws/ec2/opal-gateway/app/integrations/schwab/. Object keys and VersionIds come
from GRAIN_DECLARATION.json (measure_grain.py: markers -> closure.tables[*].object), and every
GetObject is checked against the pinned VersionId.

Writes (nothing customer-valued reaches stdout or any repository file):
  <SEALED_DIR>/expected/<id>.txt   plaintext canonical answers (outside the repository)
  <SEALED_DIR>/expected/SALT.txt   the salt (outside the repository)
  SEALED_EXPECTED_V2.json          dates, VersionIds, ids, kinds, digests, pre-seal absence record
SEALED_DIR = OG_SEALED_DIR, else %LOCALAPPDATA%/opal/og-salt/v2. Run ONCE; refuses to overwrite.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import secrets
import subprocess
import sys
from decimal import Decimal

import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import og_v6_common as C  # noqa: E402

EXPECTED_DIR = os.path.join(C.SEALED_DIR, "expected")
GC_PATH = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/1.0.0_SA_CTO~A/G-C_CONTROLLED_IDENTITY_AND_GRANT.md"
GD_PATH = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/CONTROLLED_WALKTHROUGH_RECORD.md"
SX, BD = "08242234", "08335338"

INSTRUMENT = (
    "pyarrow.parquet Table read (columnar Parquet decode only; no query/filter/group-by/aggregate by "
    "pyarrow) + Python stdlib decimal.Decimal exact summation and collections; no pandas float "
    "aggregation, no DuckDB, no import or read of infra/aws/ec2/opal-gateway/app/integrations/schwab/."
)

# id, kind, masters, dates (D_PREV/D_NEW tags), dataset -- the table in WALKTHROUGH_PROTOCOL.md section 4.
QUESTIONS = [
    ("RQ2-1", "units", [BD], ["D_NEW"], "dim_position"),
    ("RQ2-2", "units", [BD], ["D_NEW"], "dim_balance"),
    ("RQ2-3", "balance_overlap", [BD], ["D_NEW"], "dim_balance"),
    ("RQ2-4", "between_dates", [SX], ["D_PREV", "D_NEW"], "dim_balance"),
    ("RQ2-5", "between_dates", [BD], ["D_PREV", "D_NEW"], "dim_balance"),
    ("RQ2-6", "between_masters", [SX, BD], ["D_NEW"], "dim_balance"),
    ("RQ2-7", "paged_read", [BD], ["D_NEW"], "dim_position"),
]


def git(*args):
    r = subprocess.run(["git", "-C", C.REPO_ROOT] + list(args), capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def preseal_absence():
    rc, head = git("rev-parse", "HEAD")
    rec = {"commit": head, "branch": git("rev-parse", "--abbrev-ref", "HEAD")[1], "checks": []}
    for label, path in (("G-C", GC_PATH), ("G-D", GD_PATH)):
        rc, out = git("cat-file", "-e", f"HEAD:{path}")
        rec["checks"].append({"record": label, "path": path, "command": f"git cat-file -e HEAD:{path}",
                              "rc": rc, "result": "PRESENT" if rc == 0 else "ABSENT"})
    # Positive control: a path known present at HEAD reads rc 0 through the same command shape.
    ctl = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~6/SEALED_EXPECTED.json"
    rc, out = git("cat-file", "-e", f"HEAD:{ctl}")
    rec["positive_control"] = {"path": ctl, "command": f"git cat-file -e HEAD:{ctl}", "rc": rc,
                               "result": "PRESENT" if rc == 0 else "ABSENT"}
    # Extra read, beside the ordered HEAD read: the shared trunk tip, in case the walkthrough record
    # landed there after this worktree was cut.
    rc, trunk = git("rev-parse", "--verify", "-q", "CLOUD")
    if rc == 0:
        rc2, _ = git("cat-file", "-e", f"CLOUD:{GD_PATH}")
        rec["trunk_check"] = {"ref": "CLOUD", "commit": trunk, "record": "G-D", "rc": rc2,
                              "result": "PRESENT" if rc2 == 0 else "ABSENT"}
    return rec


def load_snapshots():
    with open(C.GRAIN_PATH, "r", encoding="utf-8") as fh:
        g = json.load(fh)
    snaps = {(s["master"], s["tag"], s["dataset"]): s for s in g["snapshots"]}
    return g, snaps


def table(snaps, master, tag, dataset):
    s = snaps[(master, tag, dataset)]
    path = C.fetch_silver(s["key"], s["version_id"], f"{master}_{dataset}_{s['date']}_{s['version_id']}.parquet")
    return pq.read_table(path), s


def dec_sum(t, col):
    total = Decimal(0)
    for v in t.column(col).to_pylist():
        if v is not None:
            total += v if isinstance(v, Decimal) else Decimal(str(v))
    return total


def dstr(d):
    return format(d, "f")


def scale_of(t, col):
    return t.schema.field(col).type.scale


def sign_word(d):
    return "positive" if d > 0 else ("negative" if d < 0 else "zero")


def refusal(reason, master, date, dataset):
    return {"master": master, "business_date": date, "dataset": dataset,
            "outcome": "UNAVAILABLE", "reason": reason,
            "note": "C3 refusal: the declared source grain collides on this date; no value, including a "
                    "de-duplicated one, is an acceptable answer."}


def build_answers(g, snaps):
    D_NEW, D_PREV = g["dates"]["D_NEW"], g["dates"]["D_PREV"]
    A, cls, used = {}, {}, {}

    def load(master, tag, dataset):
        t, s = table(snaps, master, tag, dataset)
        used[(master, tag, dataset)] = s
        return t, s

    # RQ2-1 units, dim_position, BlackDiamond, D_NEW -- the grain collides, so the rows read is refused.
    t, s = load(BD, "D_NEW", "dim_position")
    assert s["status"] == "COLLIDES", "RQ2-1 expected the C3 refusal branch"
    a = refusal("duplicate_source_grain", BD, D_NEW, "dim_position")
    a["described_scale"] = {"quantity_settled_unsettled": scale_of(t, "quantity_settled_unsettled"),
                            "market_value_settled_unsettled": scale_of(t, "market_value_settled_unsettled")}
    A["RQ2-1"], cls["RQ2-1"] = a, "C3_REFUSAL"

    # RQ2-2 units, dim_balance, BlackDiamond, D_NEW -- value fields: sums, signs, negative counts, scale.
    t, s = load(BD, "D_NEW", "dim_balance")
    assert s["status"] == "HOLDS"
    fields = {}
    for col in ("mkt_value_long", "mkt_value_short"):
        vals = t.column(col).to_pylist()
        tot = dec_sum(t, col)
        fields[col] = {"sum": dstr(tot), "sign_of_sum": sign_word(tot),
                       "accounts_negative": sum(1 for v in vals if v is not None and v < 0),
                       "accounts_positive": sum(1 for v in vals if v is not None and v > 0),
                       "accounts_zero": sum(1 for v in vals if v is not None and v == 0),
                       "accounts_null": sum(1 for v in vals if v is None),
                       "described_scale": scale_of(t, col)}
    A["RQ2-2"], cls["RQ2-2"] = {"master": BD, "business_date": D_NEW, "dataset": "dim_balance",
                                "fields": fields}, "VALUE"

    # RQ2-3 balance overlap, BlackDiamond, D_NEW -- three sums reported separately, never added.
    A["RQ2-3"], cls["RQ2-3"] = {
        "master": BD, "business_date": D_NEW, "dataset": "dim_balance",
        "sum_net_mv_positions": dstr(dec_sum(t, "net_mv_positions")),
        "sum_cash_balance_settled_only": dstr(dec_sum(t, "cash_balance_settled_only")),
        "sum_net_mv_plus_cash": dstr(dec_sum(t, "net_mv_plus_cash")),
        "combined_total": "NEVER COMPUTED -- different balance fields are never added (PRD C3)."}, "VALUE"

    # RQ2-4 / RQ2-5 between dates -- two separate snapshots and an exact decimal delta of one field.
    for qid, master, col in (("RQ2-4", SX, "net_mv_plus_cash"), ("RQ2-5", BD, "cash_balance_settled_only")):
        tp, sp = load(master, "D_PREV", "dim_balance")
        tn, sn = load(master, "D_NEW", "dim_balance")
        assert sp["status"] == "HOLDS" and sn["status"] == "HOLDS"
        prev, new = dec_sum(tp, col), dec_sum(tn, col)
        A[qid], cls[qid] = {
            "master": master, "dataset": "dim_balance", "field": col,
            "snapshots": {D_PREV: {"sum": dstr(prev)}, D_NEW: {"sum": dstr(new)}},
            "delta_new_minus_prev": dstr(new - prev),
            "note": "two separately authorized snapshots and an exact decimal delta; no sum across the two dates."}, "VALUE"

    # RQ2-6 between masters -- two snapshot answers, no combined total.
    ts, ss = load(SX, "D_NEW", "dim_balance")
    tb, sb = load(BD, "D_NEW", "dim_balance")
    A["RQ2-6"], cls["RQ2-6"] = {
        "dataset": "dim_balance", "field": "net_mv_positions",
        "smartx_08242234": {"business_date": D_NEW, "sum": dstr(dec_sum(ts, "net_mv_positions"))},
        "blackdiamond_08335338": {"business_date": D_NEW, "sum": dstr(dec_sum(tb, "net_mv_positions"))},
        "combined_total": "NEVER COMPUTED -- the two masters' snapshots are never added (PRD C3)."}, "VALUE"

    # RQ2-7 paged read of dim_position, BlackDiamond, D_NEW -- no unique grain, paging refused.
    t, s = load(BD, "D_NEW", "dim_position")
    assert s["status"] == "COLLIDES", "RQ2-7 expected the paged-refusal branch"
    A["RQ2-7"], cls["RQ2-7"] = refusal("paging_refused_no_unique_grain", BD, D_NEW, "dim_position"), "C3_REFUSAL"
    return A, cls, used


def main():
    if os.path.exists(os.path.join(EXPECTED_DIR, "SALT.txt")) or os.path.exists(C.SEALED_PATH):
        raise SystemExit("REFUSED: already sealed; this instrument runs once")
    pre = preseal_absence()
    gd = [c for c in pre["checks"] if c["record"] == "G-D"][0]
    trunk_gd = pre.get("trunk_check", {}).get("result")
    if gd["result"] != "ABSENT" or trunk_gd == "PRESENT":
        raise SystemExit("BLOCKED: the G-D walkthrough record is PRESENT; a seal is worthless -- not sealing")

    g, snaps = load_snapshots()
    answers, classes, used = build_answers(g, snaps)

    # Every question whose dataset COLLIDES on its date is sealed with the C3 refusal.
    for qid, kind, masters, tags, dataset in QUESTIONS:
        for m in masters:
            for tg in tags:
                if snaps[(m, tg, dataset)]["status"] == "COLLIDES":
                    assert classes[qid] == "C3_REFUSAL", qid

    os.makedirs(EXPECTED_DIR, exist_ok=True)
    salt = secrets.token_hex(32)
    with open(os.path.join(EXPECTED_DIR, "SALT.txt"), "w", encoding="ascii") as fh:
        fh.write(salt)
    sealed_q = []
    for qid, kind, masters, tags, dataset in QUESTIONS:
        canonical = json.dumps(answers[qid], sort_keys=True, separators=(",", ":"))
        with open(os.path.join(EXPECTED_DIR, f"{qid}.txt"), "w", encoding="ascii") as fh:
            fh.write(canonical)
        digest = hashlib.sha256((salt + canonical).encode("ascii")).hexdigest()
        sealed_q.append({"id": qid, "kind": kind, "masters": masters,
                         "dates": [g["dates"][t] for t in tags], "dataset": dataset,
                         "expected_class": classes[qid],
                         "expected_answer_hash": f"sha256:{digest}"})
    now = datetime.datetime.now(datetime.timezone.utc)
    sealed = {
        "schema_version": "1.0", "cell": "OG-v-6", "worker": "0.9.0_WK_NFRA_OPLGTW~10",
        "sealed_at_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "instrument": INSTRUMENT,
        "hash_algorithm": "sha256(salt || canonical_json(answer)); canonical_json = json.dumps(sort_keys=True, separators=(',', ':')); ascii",
        "salt_and_answers_local": "<OG_SEALED_DIR or %LOCALAPPDATA%/opal/og-salt/v2>/expected/{SALT,<id>}.txt (outside the repository)",
        "ssm_copy_of_record": {"prefix": f"/opal/nfra_oplgtw/ogv6/seal_v2_{now.strftime('%Y%m%d')}/",
                               "names": [q[0] for q in QUESTIONS] + ["SALT"], "type": "SecureString"},
        "dates": g["dates"], "markers": g["markers"],
        "qualified_objects_used": [
            {"master": m, "tag": tg, "dataset": ds, "date": s["date"], "key": s["key"],
             "version_id": s["version_id"], "grain_status": s["status"]}
            for (m, tg, ds), s in sorted(used.items())],
        "questions": sealed_q,
        "preseal_absence_check": pre,
    }
    with open(C.SEALED_PATH, "w", encoding="ascii") as fh:
        json.dump(sealed, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("OK: sealed", len(sealed_q), "of", len(QUESTIONS), "questions; wrote", C.SEALED_PATH)


if __name__ == "__main__":
    main()
