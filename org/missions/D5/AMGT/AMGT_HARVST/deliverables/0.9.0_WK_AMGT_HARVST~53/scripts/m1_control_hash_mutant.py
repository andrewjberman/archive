"""HVST-m-1 control: the AC1 comparator must report a mismatch when one byte differs (in-memory
mutation only; nothing is written anywhere). Uses one bronze article object per run."""

import m1_common as C


def main():
    key = C.bronze_articles("barrons")[0][0]
    body, meta = C.get(key)
    rec = meta.get("document-sha256")
    ok_plain = C.sha256(body) == rec
    mutated = bytearray(body)
    mutated[len(mutated) // 2] ^= 0x01
    caught = C.sha256(bytes(mutated)) != rec
    print("control object: %s" % key)
    print("unmutated bytes match recorded hash: %s" % ok_plain)
    print("one flipped bit (in memory) is reported as a mismatch: %s" % caught)
    print("CONTROL RESULT: %s" % ("FIRED-AS-EXPECTED" if ok_plain and caught else "FAILED"))


if __name__ == "__main__":
    main()
