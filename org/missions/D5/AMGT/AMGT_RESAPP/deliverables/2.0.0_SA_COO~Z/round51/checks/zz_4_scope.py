"""AMGT_RESAPP round 51, AMGT-zz-4 AC2 -- REGISTRY_HASH is SCOPED to the registry rows the four prefix constants derive from (CTO round-50
ruling 4; row Z-S306: the whole-registry hash went RED on HEAD for the 4th time while the four constants stayed byte-identical).

`infra/aws/terraform/harvest/gen_harvest_prefixes.py` exposes `scoped_registry_hash(registry_dir=None) -> str`, hashing ONLY what the
constants derive from (today: `systems.json` rows amgt / seeking-alpha / bright-data / bloomberg and `scopes.json` row harvest). On a
TEMP COPY of `infra/logic/registry/`:
  (a) an edit to an UNRELATED file (tiers.json gains a trailing newline) -> the scoped hash is UNCHANGED;
  (b) an edit to the `amgt` row of systems.json (its "long" value gains a character) -> the scoped hash CHANGES (difference control).
usage: python <this>   (from the repo root; the real registry is never written)"""
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

GEN = "infra/aws/terraform/harvest/gen_harvest_prefixes.py"
REG = Path("infra/logic/registry")


def main():
    sys.path.insert(0, ".")
    spec = importlib.util.spec_from_file_location("gen", GEN)
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    if not hasattr(gen, "scoped_registry_hash"):
        print("gen_harvest_prefixes has no scoped_registry_hash")
        print("THE REGISTRY STAMP IS SCOPED TO WHAT THE CONSTANTS READ: NO")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "registry"
        shutil.copytree(REG, d)
        h0 = gen.scoped_registry_hash(registry_dir=str(d))
        (d / "tiers.json").write_bytes((d / "tiers.json").read_bytes() + b"\n")
        h1 = gen.scoped_registry_hash(registry_dir=str(d))
        systems = json.loads((d / "systems.json").read_text(encoding="utf-8"))
        rows = systems if isinstance(systems, list) else next(v for v in systems.values() if isinstance(v, list))
        row = next(r for r in rows if isinstance(r, dict) and r.get("key") == "amgt")
        field = "long" if "long" in row else next(k for k, v in row.items() if isinstance(v, str) and k != "key")
        row[field] = row[field] + "x"
        (d / "systems.json").write_text(json.dumps(systems, indent=2), encoding="utf-8")
        h2 = gen.scoped_registry_hash(registry_dir=str(d))
    print("(a) unrelated edit: %s -> %s (%s)" % (h0[:12], h1[:12], "UNCHANGED" if h0 == h1 else "MOVED"))
    print("(b) amgt row edit:  %s -> %s (%s)" % (h1[:12], h2[:12], "CHANGED" if h1 != h2 else "UNCHANGED"))
    ok = h0 == h1 and h1 != h2
    print("THE REGISTRY STAMP IS SCOPED TO WHAT THE CONSTANTS READ: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
