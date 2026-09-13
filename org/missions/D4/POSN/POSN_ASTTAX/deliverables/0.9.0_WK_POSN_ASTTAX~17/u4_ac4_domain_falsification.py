"""U4-AC4 -- FALSIFY THE DOMAIN. Choosing the domain is itself a claim, so it is read UNSCOPED.

THE CLAIM UNDER TEST: "the population every retag member is drawn from is the 285 rows of
dynamodb://etf-classifications."

WHY THE CRITERION'S OWN INSTRUMENT CANNOT BE THE ONLY ONE: comp-find in this worktree reads the
SPARSE CONE (6 directories), so its own denominator line prints tens of thousands of files as
UNREADABLE. A falsification run on a cone is a scoped read wearing an unscoped label -- the exact
failure this criterion exists to catch. So the corpus is re-read from the GIT OBJECT STORE, which
does not know what is checked out, and the portal submodule is read at its pin the same way.

THREE ARMS:
  ARM 1  corpus census of the classification term, cone-independent, denominator printed.
  ARM 2  the NECESSARY-DATA population (PRD s.4 C-SATELLITE-DATA: 9 satellites / 228 components,
         "every one of the 228 components MUST sort into exactly one of the five classes")
         tested for membership in the domain.
  ARM 3  every CODE site that assigns a class to a TICKER, and whether its ticker universe is a
         subset of the domain.

Usage: python u4_ac4_domain_falsification.py <scan.json> <satellites.md> [<portal_repo_dir>]
"""
import sys
import os
import re
import json
import subprocess
import collections

SCAN, SAT = sys.argv[1], sys.argv[2]
PORTAL = sys.argv[3] if len(sys.argv) > 3 else None
PORTAL_PIN = "e85f6eb84f3a1771a37011a7e77e372570bad02a"

TERM = re.compile(rb"asset_class", re.I)
TERM2 = re.compile(rb"assetClass")
MAXBLOB = 2_000_000

domain = {i["ticker"]["S"] for i in json.load(open(SCAN))["Items"]}
print("THE DOMAIN UNDER TEST: %d tickers, dynamodb://etf-classifications (full scan)" % len(domain))
print()


def census(repo, ref, label):
    """Scan EVERY blob reachable from <ref> in <repo>. Returns (files_with_term, stats)."""
    out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", ref],
                         capture_output=True, text=True).stdout
    blobs, nonblob = [], []
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        mode, typ, sha = meta.split()
        (blobs if typ == "blob" else nonblob).append((sha, path))
    print("== ARM 1 / %s ==" % label)
    print("   ref            : %s" % ref)
    print("   TREE ENTRIES   : %d" % (len(blobs) + len(nonblob)))
    print("   blobs          : %d" % len(blobs))
    print("   NON-BLOB (gitlink) entries, NAMED not absorbed: %d" % len(nonblob))
    for sha, p in nonblob:
        print("        %s  %s" % (p, sha))

    by_sha = collections.defaultdict(list)
    for sha, p in blobs:
        by_sha[sha].append(p)
    order = list(by_sha)

    chk = subprocess.run(["git", "-C", repo, "cat-file", "--batch-check"],
                         input="".join(s + "\n" for s in order),
                         capture_output=True, text=True).stdout
    size = {}
    for line in chk.splitlines():
        parts = line.split()
        if len(parts) == 3:
            size[parts[0]] = int(parts[2])
    small = [s for s in order if size.get(s, 0) <= MAXBLOB]
    big = [s for s in order if size.get(s, 0) > MAXBLOB]

    listfile = os.path.join(os.environ.get("TMPDIR", "."), "_u4_shas_%s.txt" % label.replace("/", "_"))
    with open(listfile, "w") as fh:
        fh.write("".join(s + "\n" for s in small))
    hitfiles, read, term_blobs = [], 0, 0
    with open(listfile, "rb") as fin:
        p = subprocess.Popen(["git", "-C", repo, "cat-file", "--batch"],
                             stdin=fin, stdout=subprocess.PIPE)
        buf = p.stdout
        while True:
            header = buf.readline()
            if not header:
                break
            parts = header.split()
            if len(parts) != 3:
                continue
            sha, n = parts[0].decode(), int(parts[2])
            body = buf.read(n)
            buf.read(1)
            read += 1
            if TERM.search(body) or TERM2.search(body):
                term_blobs += 1
                for path in by_sha[sha]:
                    hitfiles.append((path, sha, body))
        p.wait()
    os.remove(listfile)
    print("   READ           : %d of %d distinct blobs (%d skipped: larger than %d bytes)"
          % (read, len(order), len(big), MAXBLOB))
    print("   ARITHMETIC     : %d read + %d skipped == %d distinct blobs; %d paths"
          % (read, len(big), len(order), len(blobs)))
    print("   DENOMINATOR (paths carrying 'asset_class' or 'assetClass') : %d of %d paths"
          % (len(hitfiles), len(blobs)))
    return hitfiles, len(blobs)


super_hits, super_n = census(".", "HEAD", "superproject@HEAD")
portal_hits, portal_n = ([], 0)
if PORTAL:
    print()
    portal_hits, portal_n = census(PORTAL, PORTAL_PIN, "portal@pin")

print()
print("   TOTAL POPULATION READ: %d paths across %d repo(s); %d carry the classification term."
      % (super_n + portal_n, 1 + (1 if PORTAL else 0), len(super_hits) + len(portal_hits)))
print("   NEGATIVE CONTROL: paths carrying 'ZZZ_NO_SUCH_TOKEN_QQQ' : %d"
      % sum(1 for _, _, b in super_hits + portal_hits if b"ZZZ_NO_SUCH_TOKEN_QQQ" in b))

# -------------------------------------------------------------------- ARM 2
print()
print("=" * 78)
print("ARM 2 -- THE NECESSARY-DATA POPULATION (PRD:335-348 C-SATELLITE-DATA)")
print("=" * 78)
sat = open(SAT, encoding="utf-8").read()
rows = re.findall(r"^\|\s*([^|]+?)\s*\|\s*([A-Z0-9.\-]{1,8})\s*\|\s*([^|]*?)\s*\|\s*([\d.]+)%\s*\|\s*$",
                  sat, re.M)
comp = [(sub, tk) for sub, tk, nm, w in rows]
tickers = [t for _, t in comp]
print("   component rows parsed : %d   (the PRD's own figure is 228 across 9 satellites)" % len(comp))
print("   DISTINCT tickers      : %d" % len(set(tickers)))
outside = sorted(set(tickers) - domain)
inside = sorted(set(tickers) & domain)
print("   IN the domain         : %d" % len(inside))
print("   NOT IN the domain     : %d  -> %s" % (len(outside), outside))
print("   POSITIVE CONTROL      : GLD and VXX, which the PRD names by hand, parsed out of this")
print("                           file and present: GLD=%s VXX=%s"
      % ("GLD" in tickers, "VXX" in tickers))

# -------------------------------------------------------------------- ARM 3
print()
print("=" * 78)
print("ARM 3 -- EVERY CODE SITE THAT BINDS A TICKER TO A CLASS, AND ITS TICKER UNIVERSE")
print("=" * 78)
CLASSVAL = re.compile(
    rb"""['"](?:equity|fixed_income|hedge|cash|Equity|Fixed Income(?: / Cash)?|Structured|Commodities|Alternatives|Hedge|Cash)['"]""")
# a ticker bound to something: 'XXX': { ... }  or  'XXX': 'equity'  or  ticker: 'XXX'
BIND = re.compile(rb"""['"]([A-Z][A-Z0-9.]{0,5})['"]\s*:""")

sites = []
for path, sha, body in super_hits + portal_hits:
    if not CLASSVAL.search(body):
        continue
    keys = set(m.group(1).decode() for m in BIND.finditer(body))
    # a site qualifies only if it binds MORE THAN ONE key that looks like a ticker AND at least
    # one of those keys is a ticker the domain knows -- otherwise it is a class map, not a
    # ticker map, and is reported separately.
    known = keys & domain
    if len(keys) >= 2 and known:
        sites.append((path, sorted(keys), sorted(known), sorted(keys - domain)))

print("   files carrying the term AND a class literal : %d"
      % sum(1 for _, _, b in super_hits + portal_hits if CLASSVAL.search(b)))
print("   of those, files that BIND >=2 quoted upper-case keys incl. >=1 known ticker : %d"
      % len(sites))
print()
allout = collections.Counter()
for path, keys, known, out in sorted(sites, key=lambda s: -len(s[2])):
    print("   %s" % path)
    print("       keys bound: %d | IN domain: %d | NOT in domain: %d" % (len(keys), len(known), len(out)))
    if out:
        print("       NOT IN DOMAIN: %s" % out)
        for o in out:
            allout[o] += 1
print()
print("   UNION of out-of-domain bound keys across every site: %d" % len(allout))
for k, n in sorted(allout.items(), key=lambda kv: (-kv[1], kv[0])):
    print("       %-8s bound in %d site(s)" % (k, n))

# -------------------------------------------------------------------- ARM 4
print()
print("=" * 78)
print("ARM 4 -- THE TEST THAT DECIDES VOID: does any OUT-OF-DOMAIN binding carry a ticker that")
print("         a RATIFIED RULE WOULD MOVE? A hit outside the domain is only a VOID if it is a")
print("         MEMBER. This applies U4-AC2's own ladder to the out-of-domain population.")
print("=" * 78)
FLAT = re.compile(r"^\s*'([A-Z][A-Z0-9._]{0,8})'\s*:\s*'([a-z_]+)'\s*,?\s*(#.*)?$")
RX_MOVE = re.compile(
    r"volatil|\bvix\b|bitcoin|ether(eum)?\b|crypto|blockchain|commodit|\bgold\b|silver|\boil\b|"
    r"bullion|platinum|palladium|precious metal|\bgsci\b|real estate|\breit\b|realty", re.I)
seen = {}
for path, sha, body in super_hits:
    try:
        txt = body.decode("utf-8", "replace")
    except Exception:
        continue
    ents = [(m.group(1), m.group(2), (m.group(3) or "").strip())
            for m in (FLAT.match(line) for line in txt.split("\n")) if m]
    if len(ents) < 10:
        continue
    off = [(t, c, cm) for t, c, cm in ents if t not in domain]
    print("   %s" % path)
    print("       flat TICKER:'class' entries: %d | out of domain: %d" % (len(ents), len(off)))
    moved = [(t, c, cm) for t, c, cm in off if RX_MOVE.search(cm) or RX_MOVE.search(t)]
    print("       of those, REACHED BY A RATIFIED RULE: %d %s"
          % (len(moved), [t for t, _, _ in moved] or ""))
    for t, c, cm in off:
        seen.setdefault(t, (c, cm))
    # POSITIVE CONTROL: the same predicate over the IN-domain entries must find the members
    ctrl = [t for t, c, cm in ents if t in domain and (RX_MOVE.search(cm) or RX_MOVE.search(t))]
    print("       POSITIVE CONTROL (same predicate, in-domain entries): %d -> %s"
          % (len(ctrl), sorted(ctrl)))

print()
print("   UNION of out-of-domain TICKER:'class' bindings across every flat classification file:")
print("       %d distinct tickers" % len(seen))
moved_any = sorted(t for t, (c, cm) in seen.items() if RX_MOVE.search(cm) or RX_MOVE.search(t))
for t in sorted(seen):
    c, cm = seen[t]
    print("       %-7s bound '%s'  %s" % (t, c, cm[:72]))
print()
print("   OUT-OF-DOMAIN TICKERS A RATIFIED RULE WOULD MOVE: %d  %s"
      % (len(moved_any), moved_any or "-- NONE"))
print("   ^ THIS IS THE VOID TEST. Zero here means: there are classification bindings outside the")
print("     domain, and NONE OF THEM IS A MEMBER, so the U4-AC2 subtraction is not void. A single")
print("     name here would void it.")

print()
print("=" * 78)
print("THE VERDICT LINE IS NOT COMPUTED HERE -- the two populations above are printed with their")
print("denominators so the report can state, in words, whether every classification-bearing hit")
print("lies inside the domain, and VOID the U4-AC2 subtraction if one does not.")
print("=" * 78)
