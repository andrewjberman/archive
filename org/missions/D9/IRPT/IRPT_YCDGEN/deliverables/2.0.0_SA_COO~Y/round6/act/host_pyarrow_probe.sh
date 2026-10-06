set -u
# READ-ONLY (tmp only) proof on the resident host that the pinned pyarrow tar imports on this host and reads the real characteristics parquet.
# Writes only under /tmp/r6-arrow-probe; no install; no service change; no write to any AWS service.
B=opal-313476888478-lambda-artifacts
KEY=ec2/investor-reporting-ycharts/resident/deps/pyarrow-18.1.0-cp312-awssdkpandas16.tar.gz
WANT=dad8a09e088722e1fc4b506b921583a3d62b7097a7eacf0907bce6f284393506
T=/tmp/r6-arrow-probe
rm -rf $T; mkdir -p $T/lib; chmod 777 $T
aws s3 cp "s3://$B/$KEY" $T/pa.tar.gz --only-show-errors --region us-east-1 || { echo "ERROR: fetch failed"; exit 30; }
[ "$(sha256sum $T/pa.tar.gz | cut -d' ' -f1)" = "$WANT" ] || { echo "ERROR: tar is not the pinned bytes"; exit 31; }
echo "pinned tar sha256 verified"
tar -xzf $T/pa.tar.gz -C $T/lib || exit 32
chmod -R a+rX $T
echo "host: $(. /etc/os-release; echo $PRETTY_NAME) glibc $(ldd --version | head -1 | awk '{print $NF}') $(uname -m)"
sudo -u ec2-user PYTHONPATH=$T/lib:/opt/investor-reporting-ycharts/pydeps /usr/bin/python3.12 - <<'PY'
import io, boto3
import pyarrow, pyarrow.parquet as pq
print("pyarrow", pyarrow.__version__, "imports from", pyarrow.__file__)
try:
    import numpy
    print("numpy present", numpy.__version__)
except ImportError:
    print("numpy absent (optional)")
s3 = boto3.client("s3", region_name="us-east-1")
p = s3.list_objects_v2(Bucket="opal-data-etfs", Prefix="bbg/", Delimiter="/")
days = sorted(c["Prefix"] for c in p.get("CommonPrefixes", []))
for d in reversed(days):
    k = d + "characteristics.parquet"
    try:
        body = s3.get_object(Bucket="opal-data-etfs", Key=k)["Body"].read()
    except Exception:
        continue
    t = pq.read_table(io.BytesIO(body))
    rows = t.to_pylist()
    print("read", k, len(body), "bytes,", t.num_rows, "rows,", t.num_columns, "columns; to_pylist ok:", bool(rows))
    print("first columns:", t.column_names[:8])
    break
PY
rm -rf $T
echo "probe dir removed"
