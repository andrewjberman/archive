"""CF-4 condition (3), CTO 76420: post-deploy verify by NORMALISED CONTENT.

c02_twr_engine.py is CRLF in the working tree while c00/c01 are LF, so this is the one file in
the set where the documented false-STALE trap can actually fire. The rule from 76323, restated:
a comp-pipescript STALE after deploy is NOT evidence of a stale deploy -- resolve by
LF-normalised compare; MATCH stays trustworthy one-directionally.

Compared against the COMMITTED BUILD INPUT (Rule 22a CODE), never the working tree, with the
parent commit as a negative control so the comparison is shown able to tell vintages apart.
"""
import hashlib
import subprocess
import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
import runner_common as rc  # noqa: E402

COMMIT = "cab1f8bff9"
FILE = "c02_twr_engine.py"
REL = f"data/assets/scripts/gold/runners_49f/{FILE}"
CRLF = b"\x0d\x0a"


def h(b):
    return hashlib.sha256(b).hexdigest()[:16]


def blob(ref):
    return subprocess.run(["git", "show", f"{ref}:{REL}"],
                          capture_output=True, check=True).stdout


s3b = rc.s3().get_object(Bucket="opal-data-49financial", Key=f"_code/{FILE}")["Body"].read()
cb, pb = blob(COMMIT), blob(COMMIT + "^")

print("CF-4 CONDITION (3) -- post-deploy verify by NORMALISED CONTENT\n")
print(f"  line endings   S3 object CRLF present: {CRLF in s3b}")
print(f"                 commit blob CRLF present: {CRLF in cb}")
print(f"  RAW-byte equal (S3 vs committed build input) : {s3b == cb}")
raw_note = ("raw compare AGREES, so the trap did not fire on this deploy"
            if s3b == cb else
            "raw compare DIFFERS -- this is exactly the case the normalised compare exists for")
print(f"                 -> {raw_note}")

n_s3, n_c, n_p = h(s3b.replace(CRLF, b"\x0a")), h(cb.replace(CRLF, b"\x0a")), \
    h(pb.replace(CRLF, b"\x0a"))
print(f"\n  LF-normalised sha256/16   S3 : {n_s3}")
print(f"                            commit {COMMIT} : {n_c}")
print(f"                            parent (NEG CTRL): {n_p}")
match = n_s3 == n_c
neg_ok = n_p != n_s3
print(f"\n  MATCH against build input : {match}")
print(f"  NEGATIVE CONTROL differs  : {neg_ok}  "
      f"({'the compare can tell vintages apart' if neg_ok else '*** compare is blind ***'})")
print(f"  sizes: S3 {len(s3b):,} B | commit {len(cb):,} B | parent {len(pb):,} B")
print(f"\nCF-4 CONDITION (3) VERDICT: {'PASS' if (match and neg_ok) else 'FAIL'}")
sys.exit(0 if (match and neg_ok) else 1)
