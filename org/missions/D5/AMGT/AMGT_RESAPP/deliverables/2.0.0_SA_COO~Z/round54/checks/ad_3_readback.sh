#!/bin/bash
# AMGT_RESAPP round 54, AMGT-ad-3 AC1 -- the artifact upload carries a content-sha256 that STARTS WITH "/" intact, and REFUSES on a
# mangled read-back; every build script in infra/aws/terraform/harvest/ uploads through that one helper (row Z-S319 / Z-S321).
#   helper   infra/aws/terraform/harvest/upload_verified.sh, sourced; defines `upload_verified <zip>` (BUCKET, KEY, AWS from the caller),
#            chatter-axis's shape: cp with the metadata, head-object read-back, exit non-zero unless metadata AND length match.
#   harness  AWS = a bash wrapper that execs a NATIVE python.exe stub -- the same bash -> native-exe boundary the real .tools/aws shim
#            crosses, where MSYS path conversion rewrites a leading "/" argument. The stub records the metadata it received on `s3 cp`
#            and answers `s3api head-object` with it (honest arm) or with a mangled value (plant arm).
#   arms     (1) a zip whose base64 sha256 starts with "/": honest arm exit 0 AND the recorded metadata equals the local sha exactly;
#            (2) plant: head-object returns the Git-root-mangled value -> the helper exits non-zero;
#            (3) static: each of the four build-and-upload*.sh sources upload_verified.sh and carries no other `--metadata` line.
# usage: bash <this> [--helper <path>] [--scripts-dir <dir>]   (from the repo root; no AWS call, writes only a temp dir)
set -u
HELPER="infra/aws/terraform/harvest/upload_verified.sh"
SDIR="infra/aws/terraform/harvest"
while [ $# -gt 0 ]; do
  case "$1" in
    --helper) HELPER="$2"; shift 2 ;;
    --scripts-dir) SDIR="$2"; shift 2 ;;
    *) echo "unknown arg $1"; exit 2 ;;
  esac
done
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
# Windows-form paths (C:/...): the stub is a native exe, and a /tmp path handed to it under MSYS_NO_PATHCONV=1 would not resolve
command -v cygpath >/dev/null && T="$(cygpath -m "$T")"
fail=0
verdict() { echo "UPLOAD KEEPS A LEADING-SLASH SHA AND REFUSES A MANGLED READ-BACK: $1"; }

if [ ! -f "$HELPER" ]; then
  echo "helper ABSENT: $HELPER"
  verdict NO; exit 1
fi

python - "$T/a.zip" <<'PYEOF'
import base64, hashlib, sys
i = 0
while True:
    b = b"ad-3 plant %d" % i
    s = base64.b64encode(hashlib.sha256(b).digest()).decode()
    if s.startswith("/"):
        open(sys.argv[1], "wb").write(b)
        break
    i += 1
PYEOF
SHA="$(python -c "import base64,hashlib,sys; print(base64.b64encode(hashlib.sha256(open(sys.argv[1],'rb').read()).digest()).decode())" "$T/a.zip")"
echo "plant zip sha256_b64=$SHA (starts with '/')"

cat > "$T/stub.py" <<'PYEOF'
import json, os, sys
state = os.environ["STUB_STATE"]
a = sys.argv[1:]
if a[:2] == ["s3", "cp"]:
    meta = a[a.index("--metadata") + 1] if "--metadata" in a else ""
    open(state, "w").write(meta.split("content-sha256=", 1)[-1])
    open(state + ".len", "w").write(str(os.path.getsize(a[2])))
elif a[:2] == ["s3api", "head-object"]:
    v = open(state).read()
    if os.environ.get("STUB_MODE") == "mangle":
        v = "C:/Program Files/Git" + v
    print(json.dumps({"Metadata": {"content-sha256": v}, "ContentLength": int(open(state + ".len").read()), "VersionId": "stub-v1"}))
else:
    print("stub: unexpected %s" % a, file=sys.stderr); sys.exit(9)
PYEOF
printf '#!/bin/bash\nexec python "%s" "$@"\n' "$T/stub.py" > "$T/aws"; chmod +x "$T/aws"

run_arm() {  # $1 = honest|mangle ; prints rc
  ( export STUB_STATE="$T/state" STUB_MODE="$1" AWS="$T/aws" BUCKET="stub-bucket" KEY="stub/key.zip"
    # shellcheck disable=SC1090
    source "$HELPER" >/dev/null
    upload_verified "$T/a.zip" > "$T/$1.out" 2>&1 ); echo $?
}
rc_h="$(run_arm honest)"; got="$(cat "$T/state" 2>/dev/null || echo ABSENT)"
echo "honest arm: exit $rc_h; metadata received by the native stub: $got"
[ "$rc_h" = "0" ] && [ "$got" = "$SHA" ] || { echo "  BAD honest arm (exit $rc_h, metadata $got, want $SHA)"; fail=1; }
rc_m="$(run_arm mangle)"
echo "plant arm (mangled read-back): exit $rc_m"
[ "$rc_m" != "0" ] || { echo "  BAD plant arm: the helper accepted a mangled read-back"; fail=1; }

for s in build-and-upload-scoped-amgt.sh build-and-upload-print-deps-layer.sh build-and-upload.sh build-and-upload-chatter-axis.sh; do
  f="$SDIR/$s"
  src_n="$(cat "$f" | grep -c 'upload_verified\.sh')"
  meta_n="$(cat "$f" | grep -v '^[[:space:]]*#' | grep -c -- '--metadata')"
  echo "static $s: sources upload_verified.sh $src_n; other --metadata lines $meta_n"
  [ "$src_n" -ge 1 ] && [ "$meta_n" = "0" ] || { echo "  BAD static $s"; fail=1; }
done

if [ "$fail" = "0" ]; then verdict YES; exit 0; else verdict NO; exit 1; fi
