"""PRF-a-5's acceptance against the SERVED leaderboard -- what is and is not testable.

a-5's acceptance (decomp row 84, cited by COO 79175 and standing per CVO): "the Book
view's relationship set == the leaderboard entry's set for the same advisor + window".

TWO QUESTIONS, and they have different answers:
 (1) CTO 79581's key-space precondition (leaf relationship_id == portal client_key):
     can it be tested tonight?
 (2) Can a-5's SET equality be tested against the served leaderboard at all?
"""
import io
import json
import pathlib
import subprocess

import boto3

ROOT = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True,
                                   check=True).stdout.strip())
# Read the SERVED leaderboard directly -- no scratch dependency, so this arm is
# re-runnable at any seat. Read-only; the build-only cap forbids writing, not reading.
_o = boto3.client("s3").get_object(Bucket="opal-data-portal-v2",
                                   Key="platinum/advi/49financial/leaderboard.json")
lb = json.load(io.BytesIO(_o["Body"].read()))
print("served leaderboard LastModified: %s"
      % _o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"))
book = json.load(open(ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables"
                             / "emissions/perfrp_book_advisor.json", encoding="utf-8"))

entries = lb["windows"]["QTD"]["entries"]
lb_keys = set()
for e in entries:
    lb_keys |= {k for k in e}
print("=" * 76)
print("(1) THE KEY-SPACE PRECONDITION -- is it testable from the served leaderboard?")
print("=" * 76)
print("  leaderboard entry fields: %s" % sorted(lb_keys))
has_set = [k for k in lb_keys if "client" in k.lower() and isinstance(entries[0].get(k), list)]
print("  fields carrying a CLIENT KEY LIST: %s" % (has_set or "NONE"))
print()
print("  VERDICT: the leaderboard carries client_count / account_count -- COUNTS, not")
print("  a key set. It exposes NO relationship key space, so it cannot test whether the")
print("  leaf's relationship_id equals the portal's client_key.")
print("  1.0.0_SA_CTO 79581's 'nothing tonight can test it' is CONFIRMED, on a surface")
print("  their message did not cite -- checked rather than accepted.")

print()
print("=" * 76)
print("(2) a-5's SET EQUALITY -- does it have a counterpart on the served plane?")
print("=" * 76)
print("  a-5 asks for SET == SET. The served leaderboard has no SET to compare against.")
print("  So the acceptance as WORDED has no served counterpart; what IS comparable is")
print("  COUNT vs COUNT. That is a weaker claim and should be named as one.")

# COUNT comparison, with the confound stated up front.
lb_by_name = {e["name"]: e for e in entries}
book_by_name = {e["key"]: e for e in book["entries"]}
print()
print("  CONFOUND, stated BEFORE the numbers: the served leaderboard is a 2026-08-21")
print("  artifact with QTD window_bounds %s..%s; my b-6 leaf is QTD ending %s."
      % (lb["window_bounds"]["QTD"]["start"], lb["window_bounds"]["QTD"]["end"],
         book["window"]["window_end"]))
print("  Different END dates, so a mismatch is expected and a MATCH would be the")
print("  surprise. This measures the SHAPE of the agreement, never a pass/fail.")
print()
shared = sorted(set(lb_by_name) & set(book_by_name))
print("  advisors: leaderboard %d, leaf %d, SHARED BY NAME %d"
      % (len(lb_by_name), len(book_by_name), len(shared)))
only_lb = sorted(set(lb_by_name) - set(book_by_name))
only_leaf = sorted(set(book_by_name) - set(lb_by_name))
print("  only in leaderboard: %d %s" % (len(only_lb), only_lb[:3]))
print("  only in leaf       : %d %s" % (len(only_leaf), only_leaf[:3]))

exact = close = far = 0
worst = []
for n in shared:
    lc = lb_by_name[n]["client_count"]
    bc = book_by_name[n]["tiles"]["relationships"]["headline"]["value"]
    d = bc - lc
    if d == 0:
        exact += 1
    elif abs(d) <= 3:
        close += 1
    else:
        far += 1
        worst.append((n, lc, bc, d))
print()
print("  client_count vs the leaf's relationships headline, over %d shared advisors:"
      % len(shared))
print("      EXACT match      : %d" % exact)
print("      within 3         : %d" % close)
print("      differ by > 3    : %d" % far)
for n, lc, bc, d in sorted(worst, key=lambda t: -abs(t[3]))[:5]:
    print("        %-24s leaderboard %4d  leaf %4d  delta %+d" % (n[:24], lc, bc, d))
