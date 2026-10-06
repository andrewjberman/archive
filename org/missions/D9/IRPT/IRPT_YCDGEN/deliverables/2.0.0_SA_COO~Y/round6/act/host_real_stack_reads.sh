set -u
# READ-ONLY proof on the resident host, as the service user and the host role, that the Opal producer's real client stack reaches what it needs.
# No put, no write, no service change. The assume-role is a credential fetch only; nothing is written with it.
sudo -u ec2-user PYTHONPATH=/opt/irpt-resident/09139ee34d-st23 /usr/bin/python3.12 - <<'PY'
import io, json, os, sys
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
out = {}
def step(name, fn):
    try:
        out[name] = fn()
    except Exception as e:
        out[name] = "FAILED %s: %s" % (type(e).__name__, str(e)[:160])
    print("%-34s %s" % (name, out[name]))
import boto3
def pyarrow_import():
    import pyarrow.parquet as pq
    import pyarrow
    return "pyarrow %s" % pyarrow.__version__
step("pyarrow import", pyarrow_import)
def classifier():
    sys.path[:0] = ["/opt/irpt-resident/09139ee34d-st23/" + p for p in ("reports", "_authz", "_scope", "_ids", "ops", "intake", "_keys", "_gate", "ycharts/session", "ycharts/extract", "ycharts/generate", "ycharts/research")]
    sys.path.insert(0, "/opt/irpt-resident/09139ee34d-st23")
    import resident_installed as ri
    import resident_worker
    from etf_classifications_dynamodb import ETFClassifier  # the installed shared client the layout reads through
    return "ETFClassifier import ok (class %s); installer imports ok" % ETFClassifier.__name__
step("classifier opener (installer)", classifier)
def getitem():
    t = boto3.resource("dynamodb", region_name="us-east-1").Table("etf-classifications")
    r = t.get_item(Key={"ticker": "SPY"})
    it = r.get("Item") or {}
    return "GetItem ok, item keys %s" % sorted(it)[:6]
step("dynamodb GetItem etf-classifications", getitem)
s3 = boto3.client("s3", region_name="us-east-1")
def listbbg():
    p = s3.list_objects_v2(Bucket="opal-data-etfs", Prefix="bbg/", Delimiter="/")
    cps = sorted(c["Prefix"] for c in p.get("CommonPrefixes", []))
    return "ListBucket ok, %d dated folders on page 1, latest %s" % (len(cps), cps[-1] if cps else None)
step("s3 ListBucket opal-data-etfs bbg/", listbbg)
def getchar():
    p = s3.list_objects_v2(Bucket="opal-data-etfs", Prefix="bbg/", Delimiter="/")
    days = sorted(c["Prefix"] for c in p.get("CommonPrefixes", []))
    for d in reversed(days):
        k = d + "characteristics.parquet"
        try:
            h = s3.head_object(Bucket="opal-data-etfs", Key=k)
        except Exception:
            continue
        body = s3.get_object(Bucket="opal-data-etfs", Key=k)["Body"].read()
        import pyarrow.parquet as pq
        t = pq.read_table(io.BytesIO(body))
        return "GetObject ok %s %d bytes, %d rows, %d columns" % (k, len(body), t.num_rows, t.num_columns)
    return "no characteristics.parquet in the listed folders"
step("s3 GetObject characteristics+pyarrow", getchar)
def assume():
    sts = boto3.client("sts", region_name="us-east-1")
    acct = sts.get_caller_identity()["Account"]
    r = sts.assume_role(RoleArn="arn:aws:iam::%s:role/irpt-cot-ycharts-research-role" % acct, RoleSessionName="ycdgen-r6-readcheck", DurationSeconds=900)
    return "AssumeRole ok, expires %s" % r["Credentials"]["Expiration"].isoformat()
step("sts AssumeRole research role", assume)
def render():
    return "render_pdf.cjs present: %s" % os.path.isfile("/opt/irpt-resident/09139ee34d-st23/ycharts/research/render_pdf.cjs")
step("render_pdf.cjs in the package", render)
print("REAL_STACK_RESULT", "PASS" if not any(str(v).startswith("FAILED") for v in out.values()) else "FAIL")
PY
