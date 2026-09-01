"""P3-EXACT cycle 1 -- the UNSCOPED read of the 87-day segment, metadata plane only.

RULE 22 COVERAGE CLAUSE, applied deliberately: a per-cell pass over the LARGE class is scoped to the
members and CANNOT see a defect in what those members SHARE. 0.4.0_DS_ClientPlatform~Y localized the
whole -18.7 bp disagreement to 2025-08-28..2025-12-31 (@16f1762977). So the question this asks is not
"which cells are wrong" but "WHAT IS STRUCTURALLY DIFFERENT ABOUT THOSE PARTITIONS" -- checked on its
own, against a CONTROL segment, before any per-cell reasoning.

  SUSPECT  2025-08-28 .. 2025-12-31   in 1Y, NOT in YTD-2026   <- carries the disagreement
  CONTROL  2026-01-01 .. 2026-08-28   in YTD and 1Y            <- measured EXACT at n=3
  PRIOR    2024-07-08 .. 2025-08-27   before the 1Y window opens

METADATA PLANE ONLY (LastModified, size, schema width, row count) -- deliberately NOT the values.
A vintage/schema discontinuity at the segment boundary is a DIFFERENT and cheaper finding than a
value defect, and it is the one a per-cell pass structurally cannot produce.
PRINTS DENOMINATORS on every line. Zero vendor egress.
"""
import pyarrow.parquet as pq
import s3fs

BUCKET = "opal-data-49financial"
PREFIX = "gold/advi/canonical/twr_daily/"

SEGMENTS = [
    ("PRIOR   ", "2024-01-01", "2025-08-27"),
    ("SUSPECT ", "2025-08-28", "2025-12-31"),
    ("CONTROL ", "2026-01-01", "2026-08-28"),
]


def main():
    fs = s3fs.S3FileSystem(skip_instance_cache=True, use_listings_cache=False)
    info = fs.find("%s/%s" % (BUCKET, PREFIX), detail=True)
    parts = []
    for path, meta in info.items():
        if not path.endswith("data.parquet"):
            continue
        try:
            d = path.split("date=")[1][:10]
        except IndexError:
            continue
        parts.append((d, path, meta.get("size"), str(meta.get("LastModified"))))
    parts.sort()
    print("PARTITIONS IN HISTORY: %d  (denominator for every count below)" % len(parts))
    if not parts:
        print("ERROR: zero partitions -- OUT OF CORPUS, not an absence.")
        return 1
    print("EARLIEST %s   LATEST %s" % (parts[0][0], parts[-1][0]))
    print("")

    for name, s, e in SEGMENTS:
        sel = [p for p in parts if s <= p[0] <= e]
        if not sel:
            print("%s %s..%s : 0 partitions  <- OUT OF CORPUS for this range" % (name, s, e))
            continue
        sizes = [p[2] for p in sel if p[2]]
        vints = sorted(set(p[3][:10] for p in sel))
        print("%s %s..%s" % (name, s, e))
        print("    partitions        : %d of %d in history" % (len(sel), len(parts)))
        print("    size bytes  min/med/max : %d / %d / %d"
              % (min(sizes), sorted(sizes)[len(sizes) // 2], max(sizes)))
        print("    DISTINCT WRITE DATES (LastModified, UTC): %d -> %s"
              % (len(vints), vints if len(vints) <= 8 else vints[:8] + ["...+%d" % (len(vints) - 8)]))
        # schema width at the segment edges and middle -- a width change is a producer-shape change
        probe = [sel[0], sel[len(sel) // 2], sel[-1]]
        widths = []
        for d, path, _sz, _lm in probe:
            try:
                widths.append((d, len(pq.read_schema(path, filesystem=fs).names)))
            except Exception as exc:  # noqa: BLE001 -- surface, never swallow
                widths.append((d, "READ-FAILED: %s" % type(exc).__name__))
        print("    schema width (first/mid/last): %s" % widths)
        print("")

    # THE BOUNDARY ITSELF -- the discontinuity, if there is one, lives here.
    print("=== THE SEGMENT BOUNDARY, partition by partition (2025-12-22 .. 2026-01-09) ===")
    for d, path, sz, lm in parts:
        if "2025-12-22" <= d <= "2026-01-09":
            print("  %s  size=%-10s  written=%s" % (d, sz, lm))

    print("")
    print("=== WRITE-VINTAGE HISTOGRAM across ALL partitions (rebuild footprint) ===")
    hist = {}
    for _d, _p, _s, lm in parts:
        hist[lm[:10]] = hist.get(lm[:10], 0) + 1
    for k in sorted(hist):
        print("  written %s : %d partitions of %d" % (k, hist[k], len(parts)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
