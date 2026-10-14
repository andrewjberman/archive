"""Compare two Lambda zips member by member by sha256; print a JSON summary."""
import base64
import hashlib
import json
import sys
import zipfile


def manifest(path):
    z = zipfile.ZipFile(path)
    names = [i.filename for i in z.infolist() if not i.is_dir()]
    return {n: hashlib.sha256(z.read(n)).hexdigest() for n in names}


def zipinfo(path):
    data = open(path, "rb").read()
    digest = hashlib.sha256(data).digest()
    return len(data), hashlib.sha256(data).hexdigest(), base64.b64encode(digest).decode()


def main(argv):
    live_zip, cand_zip, out = argv[1], argv[2], argv[3]
    live = manifest(live_zip)
    cand = manifest(cand_zip)
    delta = sorted(k for k in set(live) & set(cand) if live[k] != cand[k])
    only_live = sorted(set(live) - set(cand))
    only_rel = sorted(set(cand) - set(live))
    bl, hl, cl = zipinfo(live_zip)
    br, hr, cr = zipinfo(cand_zip)
    res = {
        "live_bytes": bl,
        "live_zip_sha256": hl,
        "live_codesha_b64": cl,
        "cand_bytes": br,
        "cand_zip_sha256": hr,
        "cand_codesha_b64": cr,
        "member_count_live": len(live),
        "member_count_cand": len(cand),
        "delta_vs_live": delta,
        "only_in_live": only_live,
        "only_in_release": only_rel,
        "codesha_equal": cl == cr,
    }
    print(json.dumps(res, indent=1))
    if out != "-":
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
