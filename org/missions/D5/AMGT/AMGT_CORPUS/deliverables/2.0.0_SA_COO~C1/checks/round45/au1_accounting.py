"""AMGT_CORPUS round 45, CRPS-au-1 -- the FWD-1 accounting identity over the site-Z evidence file. READ-ONLY.

  python au1_accounting.py <evidence file>      print one line, exit 0 only when the identity holds
  python au1_accounting.py --selftest           one GREEN arm and one RED arm on built-in samples

Reads four lines the order's evidence file carries whole:
  census     `folders F_d files F`                              (library --census, the LAST one in the file)
  write      `resolved_folders A files_in_resolved R stored S (put_performed P existed E) read_failed X`
  unresolved `unresolved_files K in J folders`
  verify     `objects N files M match M mismatch Z`

The identity: census F == R + K  (every drive file is in a resolved folder or in a named unresolved one),
S == R and X == 0 (every resolved-folder file is stored, none unreadable), N == R and Z == 0 (every object re-opens).
A line that is missing prints NOT-DERIVABLE and exits 1: an absent line is never a pass.
"""
import re
import sys

CENSUS = re.compile(r"^folders (\d+) files (\d+)$", re.M)
WRITE = re.compile(r"^resolved_folders (\d+) files_in_resolved (\d+) stored (\d+) \(put_performed (\d+) existed (\d+)\) read_failed (\d+)$", re.M)
UNRES = re.compile(r"^unresolved_files (\d+) in (\d+) folders$", re.M)
VERIFY = re.compile(r"^objects (\d+) files (\d+) match (\d+) mismatch (\d+)$", re.M)


def grade(text):
    missing = [name for name, rx in (("census", CENSUS), ("write", WRITE), ("unresolved", UNRES), ("verify", VERIFY))
               if not rx.findall(text)]
    if missing:
        return "au1 accounting NOT-DERIVABLE missing %s" % ",".join(missing), False
    f = int(CENSUS.findall(text)[-1][1])
    _a, r, s, _p, _e, x = (int(v) for v in WRITE.findall(text)[-1])
    k = int(UNRES.findall(text)[-1][0])
    n, _m, match, z = (int(v) for v in VERIFY.findall(text)[-1])
    ok = (f == r + k) and (s == r) and (x == 0) and (n == r) and (z == 0) and (match == n)
    return ("au1 accounting census %d resolved %d unresolved %d objects %d identity %s"
            % (f, r, k, n, "OK" if ok else "BROKEN")), ok


SAMPLE_GREEN = """folders 102 files 378
resolved_folders 96 files_in_resolved 370 stored 370 (put_performed 14 existed 356) read_failed 0
unresolved_files 8 in 6 folders
objects 370 files 370 match 370 mismatch 0
"""


def main(argv):
    if argv and argv[0] == "--selftest":
        print(grade(SAMPLE_GREEN)[0])
        print(grade(SAMPLE_GREEN.replace("stored 370", "stored 369"))[0])
        return 0
    text = open(argv[0], encoding="utf-8", errors="replace").read()
    line, ok = grade(text)
    print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
