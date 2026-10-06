set -u
# READ-ONLY (tmp only) real-client-stack proof for branch B2, BEFORE any install. CTO ruling msg 105485 point 4: show both gaps closed.
# Fetches the B2 package tar and the pinned pyarrow tar by key into /tmp, verifies their sha256, extracts them there, and runs the producer's real
# readers from that tree as the service user and the host role: the classification client (the packaged member), the characteristics read through
# layout_overview._read_characteristics with pyarrow, and the process exit code of that read (the host abort found on 2026-10-06). No install, no
# service change, no write to any AWS service; the assume-role is a credential fetch only.
B=opal-313476888478-lambda-artifacts
K=ec2/investor-reporting-ycharts/resident
PKEY=$K/irpt-resident-409e3066d1-st24.tar.gz
PWANT=91d23ab3367bed1cc3dbb7f5cba0ac51dfec0816f6a2a6679341ed5596b51a04
AKEY=$K/deps/pyarrow-18.1.0-cp312-awssdkpandas16.tar.gz
AWANT=dad8a09e088722e1fc4b506b921583a3d62b7097a7eacf0907bce6f284393506
T=/tmp/r6-b2-proof
rm -rf $T; mkdir -p $T/root $T/arrow; chmod 777 $T
aws s3 cp "s3://$B/$PKEY" $T/pkg.tar.gz --only-show-errors --region us-east-1 || { echo "ERROR: fetch package failed"; exit 30; }
aws s3 cp "s3://$B/$AKEY" $T/pa.tar.gz --only-show-errors --region us-east-1 || { echo "ERROR: fetch pyarrow failed"; exit 31; }
[ "$(sha256sum $T/pkg.tar.gz | cut -d' ' -f1)" = "$PWANT" ] || { echo "ERROR: package tar is not the built bytes"; exit 32; }
[ "$(sha256sum $T/pa.tar.gz | cut -d' ' -f1)" = "$AWANT" ] || { echo "ERROR: pyarrow tar is not the pinned bytes"; exit 33; }
echo "package and pyarrow tars sha256 verified"
tar -xzf $T/pkg.tar.gz -C $T/root || exit 34
tar -xzf $T/pa.tar.gz -C $T/arrow || exit 35
(cd $T/root && sha256sum -c SHA256SUMS --quiet) && echo "package SHA256SUMS OK ($(wc -l < $T/root/SHA256SUMS) members)" || { echo "ERROR: SHA256SUMS"; exit 36; }
chmod -R a+rX $T
cat > $T/proof.py <<'PY'
import io, os, sys
root, arrow = "/tmp/r6-b2-proof/root", "/tmp/r6-b2-proof/arrow"
for rel in ("intake", "ops", "reports", "_keys", "_authz", "_gate", "ycharts/session", "ycharts/extract", "ycharts/generate"):
    sys.path.insert(0, os.path.join(root, rel))
sys.path.insert(0, root)
sys.path.append(os.path.join(root, "ycharts", "research"))   # as resident_worker.load_opal_producer appends it
sys.path.append(arrow)
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
out = {}
def step(name, fn):
    try:
        out[name] = fn()
    except Exception as e:
        out[name] = "FAILED %s: %s" % (type(e).__name__, str(e)[:170])
    print("%-40s %s" % (name, out[name]))
import boto3
import layout_overview as lo
def classifier():
    c = lo._default_classifier()
    row = c.get_classification("SPY")
    return "ETFClassifier from %s; get_classification(SPY) -> %s" % (os.path.basename(os.path.dirname(sys.modules[type(c).__module__].__file__)), sorted(row)[:5] if row else row)
step("classification client (packaged member)", classifier)
def chars():
    import pyarrow
    s3 = boto3.client("s3", region_name="us-east-1")
    key_field = lo.held_data.KEY_FIELD[lo.held_data.CHARACTERISTICS]
    # which tickers exist: read the same parquet once, directly, for the key column only
    p = s3.list_objects_v2(Bucket="opal-data-etfs", Prefix="bbg/", Delimiter="/")
    days = sorted(c["Prefix"] for c in p.get("CommonPrefixes", []))
    import pyarrow.parquet as pq
    body = s3.get_object(Bucket="opal-data-etfs", Key=days[-1] + "characteristics.parquet")["Body"].read()
    rows = pq.read_table(io.BytesIO(body), use_threads=False).to_pylist()
    indexed = lo.held_data.index_by_ticker(rows, key_field)   # the reader's own ticker keys
    want = sorted(indexed)[:3]
    fields = ["NAME"]
    got = lo._read_characteristics(set(want), fields, s3=s3)
    sample = {t: {k: str(v)[:24] for k, v in r.items() if k == "NAME"} for t, r in list(got.items())[:2]}
    return "pyarrow %s; asked %s -> _read_characteristics returned %d of %d rows (key field %s); sample %s" % (pyarrow.__version__, want, len(got), len(want), key_field, sample)
step("characteristics read (pyarrow, real)", chars)
def assume():
    sts = boto3.client("sts", region_name="us-east-1")
    r = sts.assume_role(RoleArn="arn:aws:iam::%s:role/irpt-cot-ycharts-research-role" % sts.get_caller_identity()["Account"], RoleSessionName="ycdgen-b2-readcheck", DurationSeconds=900)
    return "AssumeRole ok"
step("sts AssumeRole research role", assume)
print("B2_PROOF_RESULT", "PASS" if not any(str(v).startswith("FAILED") for v in out.values()) else "FAIL")
PY
chmod 644 $T/proof.py
echo "--- the proof, as ec2-user (its exit code is the point: the host abort was at exit):"
sudo -u ec2-user HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 $T/proof.py
echo "proof process exit code: $?"
echo "--- control: the CURRENT st22 root has no classification client:"
sudo -u ec2-user env PYTHONPATH=/opt/irpt-resident/3d705e700f-st22/ycharts/research /usr/bin/python3.12 -c "import etf_classifications_dynamodb" 2>&1 | tail -1
rm -rf $T
echo "proof dir removed"
