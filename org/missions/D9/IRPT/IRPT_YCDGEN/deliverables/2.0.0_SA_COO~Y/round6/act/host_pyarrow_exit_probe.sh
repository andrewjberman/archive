set -u
# READ-ONLY (tmp only): which pyarrow usage aborts at interpreter exit on this host, and what avoids it. Each case is its own python process; the exit code is printed.
B=opal-313476888478-lambda-artifacts
KEY=ec2/investor-reporting-ycharts/resident/deps/pyarrow-18.1.0-cp312-awssdkpandas16.tar.gz
WANT=dad8a09e088722e1fc4b506b921583a3d62b7097a7eacf0907bce6f284393506
T=/tmp/r6-arrow-exit
rm -rf $T; mkdir -p $T/lib; chmod 777 $T
aws s3 cp "s3://$B/$KEY" $T/pa.tar.gz --only-show-errors --region us-east-1 || exit 30
[ "$(sha256sum $T/pa.tar.gz | cut -d' ' -f1)" = "$WANT" ] || exit 31
tar -xzf $T/pa.tar.gz -C $T/lib; chmod -R a+rX $T
aws s3 cp "s3://opal-data-etfs/bbg/2026-10-02/characteristics.parquet" $T/c.parquet --only-show-errors --region us-east-1 || exit 33
chmod 644 $T/c.parquet
run() {
  label="$1"; shift
  out=$(sudo -u ec2-user env PYTHONPATH=$T/lib "$@" 2>&1); rc=$?
  echo "CASE $label -> exit $rc $(echo "$out" | tail -2 | tr '\n' ' ' | cut -c1-150)"
}
run "A import pyarrow only" /usr/bin/python3.12 -c "import pyarrow; print('ok')"
run "B import pyarrow.parquet only" /usr/bin/python3.12 -c "import pyarrow.parquet; print('ok')"
run "C read_table from path" /usr/bin/python3.12 -c "import pyarrow.parquet as pq; t=pq.read_table('$T/c.parquet'); print(t.num_rows)"
run "D read_table from BytesIO (the producer's call)" /usr/bin/python3.12 -c "import io,pyarrow.parquet as pq; t=pq.read_table(io.BytesIO(open('$T/c.parquet','rb').read())); print(t.num_rows)"
run "E same as D, use_threads=False" /usr/bin/python3.12 -c "import io,pyarrow.parquet as pq; t=pq.read_table(io.BytesIO(open('$T/c.parquet','rb').read()),use_threads=False); print(t.num_rows)"
run "F same as D, pandas-free to_pylist" /usr/bin/python3.12 -c "import io,pyarrow.parquet as pq; t=pq.read_table(io.BytesIO(open('$T/c.parquet','rb').read())); r=t.to_pylist(); print(len(r))"
run "G same as F with ARROW_DEFAULT_MEMORY_POOL=system" env ARROW_DEFAULT_MEMORY_POOL=system /usr/bin/python3.12 -c "import io,pyarrow.parquet as pq; t=pq.read_table(io.BytesIO(open('$T/c.parquet','rb').read())); r=t.to_pylist(); print(len(r))"
run "H same as F with the host pydeps (boto3 etc) on the path" env PYTHONPATH=$T/lib:/opt/investor-reporting-ycharts/pydeps /usr/bin/python3.12 -c "import boto3,io,pyarrow.parquet as pq; t=pq.read_table(io.BytesIO(open('$T/c.parquet','rb').read())); r=t.to_pylist(); print(len(r))"
run "I same as H with the S3 client created and used first" env PYTHONPATH=$T/lib:/opt/investor-reporting-ycharts/pydeps /usr/bin/python3.12 -c "import boto3,io; s=boto3.client('s3',region_name='us-east-1'); b=s.get_object(Bucket='opal-data-etfs',Key='bbg/2026-10-02/characteristics.parquet')['Body'].read(); import pyarrow.parquet as pq; t=pq.read_table(io.BytesIO(b)); r=t.to_pylist(); print(len(r))"
rm -rf $T
echo "probe dir removed"
