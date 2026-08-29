"""ADVI_PERFRP PRF-b-2: the c02 VINTAGE DISCRIMINATOR.

THE QUESTION IT ANSWERS: "this emission read the CORRECTED twr_daily" is a claim.
Taken from the campaign's own ledger it is a SELF-REPORT. This looks for a signature
in the DATA that differs between a partition the P14-VEHICLE campaign has rewritten
and one it has not -- evidence that WOULD look different if the claim were false.

MEASURED 2026-08-28 (0.4.0_DS_ClientPlatform~V), two partitions:
    corrected  date=2024-11-07  LastModified 2026-08-28T19:18:17Z
    control    date=2025-06-02  LastModified 2026-08-19T01:13:27Z (pre-campaign)
  -> `flow_boundary` column PRESENT in the corrected partition, ABSENT in the control.
  -> status enum differs: corrected carries NO-PRIOR-BALANCE-ACCOUNT-ABSENT,
     the control carries REFUSED-NO-BMV.
Either difference separates the two vintages without trusting the ledger.

⛔ SHELF LIFE, STATED SO A LATER READER DOES NOT MISREAD A PASS: this arm needs a
partition the campaign has NOT yet rewritten. The campaign is walking forward through
all 534 partitions; when it completes there is NO pre-campaign control left on the
live plane, and this script will report "no control available" rather than silently
comparing two corrected partitions and finding no difference. A no-difference result
from two corrected partitions would look exactly like a FAILED discriminator.

⛔ SCOPE: shape is used here as a VINTAGE discriminator, NOT as a figure-state
classifier. The contract's SHAPE_IS_A_VALID_CLASSIFIER = False governs the latter and
is untouched by this -- the emitter keys figure state on `status`.

Usage: python perfrp_b2_c02_vintage_discriminator.py [corrected_date] [control_date]
"""
import io
import sys

import boto3
import pyarrow.parquet as pq

GOLD = "opal-data-49financial"
KEY = "gold/advi/canonical/twr_daily/date=%s/data.parquet"
FLOW_COLS = ["cf_net", "cf_gross", "flow_convention", "flow_boundary"]
S3 = boto3.client("s3")


def load(date):
    o = S3.get_object(Bucket=GOLD, Key=KEY % date)
    return pq.read_table(io.BytesIO(o["Body"].read())).to_pandas(), o["LastModified"]


def profile(df, lm, label, date):
    print("=" * 74)
    print("%s  date=%s  LastModified=%s" % (label, date, lm.strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("  rows %d   accounts %d" % (len(df), df["account_id"].nunique()))
    print("  status: %s" % df["status"].astype(str).value_counts().to_dict())
    for c in FLOW_COLS:
        if c not in df.columns:
            print("  [%s] ABSENT" % c)
            continue
        s = df[c]
        if s.dtype == object:
            print("  [%s] %s" % (c, s.astype(str).value_counts().to_dict()))
        else:
            nz = int((s.fillna(0) != 0).sum())
            print("  [%s] nonzero %d of %d  sum_abs=%.2f" % (c, nz, len(s), float(s.abs().sum())))
    both = df[["r_net", "r_gross"]].dropna()
    if len(both):
        eq = int((both["r_net"] == both["r_gross"]).sum())
        print("  r_net == r_gross on %d of %d non-null rows (%.2f%%)"
              % (eq, len(both), 100.0 * eq / len(both)))
    return set(df.columns)


def main():
    corrected_date = sys.argv[1] if len(sys.argv) > 1 else "2024-11-07"
    control_date = sys.argv[2] if len(sys.argv) > 2 else "2025-06-02"
    cdf, clm = load(corrected_date)
    kdf, klm = load(control_date)
    ccols = profile(cdf, clm, "CORRECTED (campaign-rewritten)", corrected_date)
    kcols = profile(kdf, klm, "CONTROL (expected pre-campaign)", control_date)

    print("=" * 74)
    if klm >= clm:
        print("NO CONTROL AVAILABLE: the 'control' partition is NOT older than the")
        print("corrected one (control %s >= corrected %s). The campaign has caught up"
              % (klm.strftime("%Y-%m-%dT%H:%M:%SZ"), clm.strftime("%Y-%m-%dT%H:%M:%SZ")))
        print("to this date. A no-difference result here would be MEANINGLESS -- both")
        print("partitions are corrected. Pick a control the campaign has not reached,")
        print("or retire this arm: post-campaign it has no subject by construction.")
        return 2

    only_c = sorted(ccols - kcols)
    only_k = sorted(kcols - ccols)
    print("SCHEMA DELTA: only in corrected %s ; only in control %s" % (only_c, only_k))
    if only_c or only_k:
        print("DISCRIMINATOR HOLDS: the two vintages are separable from the DATA alone.")
        return 0
    print("*** DISCRIMINATOR DID NOT FIRE *** -- identical column sets. Either the")
    print("control is already rewritten (check LastModified above) or the correction")
    print("leaves no structural fingerprint; do not claim a corrected read on shape.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
