"""Append this cell's surprise rows INSIDE the channel's first fenced json array.

Append-only: no existing row is read into memory as mutable and no existing row is rewritten. The
insertion point is the LAST `]` of the first fenced block, found by scanning for the fence.
"""
import json
import os
import sys

CHANNEL = os.path.join("org", "missions", "D5", "AMGT", "AMGT_HARVST", "surprise-channel",
                       "investigations", "INVESTIGATION_v1.md")

ROWS_FILE = sys.argv[1] if len(sys.argv) > 1 else "rows.json"
ROWS = json.load(open(os.path.join(
    "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
    "0.9.0_WK_AMGT_HARVST~22", "scripts", ROWS_FILE), encoding="utf-8"))

with open(CHANNEL, "r", encoding="utf-8") as fh:
    text = fh.read()

marker = "\n]\n```"
idx = text.index(marker)
existing = json.loads(text[text.index("[", text.index("```json")):idx + 2])
existing_ids = {r["id"] for r in existing}
new = [r for r in ROWS if r["id"] not in existing_ids]
if not new:
    print("NOTHING TO APPEND -- every row id already present")
    sys.exit(0)

chunk = ",\n" + ",\n".join(
    "\n".join("  " + line for line in json.dumps(r, indent=2, ensure_ascii=True).splitlines())
    for r in new)
text = text[:idx] + chunk + text[idx:]
with open(CHANNEL, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text)

with open(CHANNEL, "r", encoding="utf-8") as fh:
    after = fh.read()
parsed = json.loads(after[after.index("[", after.index("```json")):after.index(marker) + 2])
print("appended %d row(s): %s" % (len(new), ", ".join(r["id"] for r in new)))
print("block re-parses: %d rows total; ids: %s" % (len(parsed), ", ".join(r["id"] for r in parsed)))
