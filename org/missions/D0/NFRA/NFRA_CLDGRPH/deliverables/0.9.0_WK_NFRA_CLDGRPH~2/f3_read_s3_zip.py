#!/usr/bin/env python3
"""Read the SERVED source zip in S3 without downloading it.

F3-AC2's claim is about the OBJECT AT THE KEY, not about a local file this seat
happens to hold, so the numbers are taken from the served bytes. A 173 MiB
download every time the criterion runs would not fit the order's `timeout 120`,
so this reads the ZIP structure with three RANGED GETs:

  1. the last 64 KiB      -> the End Of Central Directory record (cd offset+size)
  2. [cd_offset, +cd_size)-> the central directory: every entry name, and the
                             local-header offset + compressed size of the one
                             entry whose contents we need
  3. that one entry       -> stitch_source_sha.txt, inflated in memory (< 1 KiB)

Nothing is written. Prints JSON on stdout.
"""
import argparse
import datetime
import json
import struct
import sys
import zlib

import boto3

EOCD_SIG = b"PK\x05\x06"
CEN_SIG = b"PK\x01\x02"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket", default="opal-313476888478-globgrph")
    ap.add_argument("--key", default="stitch-source/source.zip")
    ap.add_argument("--prefix", default="portal/src/")
    ap.add_argument("--read-entry", default="stitch_source_sha.txt")
    a = ap.parse_args()

    s3 = boto3.client("s3", region_name="us-east-1")
    read_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    h = s3.head_object(Bucket=a.bucket, Key=a.key)
    size = h["ContentLength"]
    lm = h["LastModified"].astimezone(datetime.timezone.utc)

    def rng(start, end):
        return s3.get_object(Bucket=a.bucket, Key=a.key,
                             Range="bytes=%d-%d" % (start, end))["Body"].read()

    tail_len = min(65536, size)
    tail = rng(size - tail_len, size - 1)
    i = tail.rfind(EOCD_SIG)
    if i < 0:
        print(json.dumps({"error": "EOCD not found in last %d bytes" % tail_len}))
        return 1
    total_entries, cd_size, cd_off = struct.unpack("<HII", tail[i + 10:i + 20])

    cd = rng(cd_off, cd_off + cd_size - 1)
    names = []
    want = None
    p = 0
    while p + 46 <= len(cd) and cd[p:p + 4] == CEN_SIG:
        method, = struct.unpack("<H", cd[p + 10:p + 12])
        csize, usize = struct.unpack("<II", cd[p + 20:p + 28])
        fn_len, ex_len, cm_len = struct.unpack("<HHH", cd[p + 28:p + 34])
        lho, = struct.unpack("<I", cd[p + 42:p + 46])
        name = cd[p + 46:p + 46 + fn_len].decode("utf-8", "replace")
        names.append(name)
        if name == a.read_entry:
            want = {"method": method, "csize": csize, "usize": usize, "lho": lho}
        p += 46 + fn_len + ex_len + cm_len

    entry_value = None
    if want:
        raw = rng(want["lho"], want["lho"] + 30 + 4096 + want["csize"])
        fn_len, ex_len = struct.unpack("<HH", raw[26:30])
        data = raw[30 + fn_len + ex_len:30 + fn_len + ex_len + want["csize"]]
        if want["method"] == 8:
            data = zlib.decompress(data, -15)
        entry_value = data.decode("utf-8", "replace").strip()

    out = {
        "read_at_utc": read_at,
        "bucket": a.bucket,
        "key": a.key,
        "content_length": size,
        "last_modified_utc": lm.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "etag": h["ETag"],
        "central_directory_entries": total_entries,
        "names_parsed": len(names),
        "prefix": a.prefix,
        "prefix_count": len([n for n in names if n.startswith(a.prefix)]),
        "portal_any_count": len([n for n in names if n.startswith("portal/")]),
        "read_entry": a.read_entry,
        "read_entry_value": entry_value,
        "ranged_gets": 3 if want else 2,
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
