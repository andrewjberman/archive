#!/usr/bin/env python3
"""inc-2a DEPLOY-DRIFT detector tuning -- the artifact-not-full-package discriminator.

Proves check_deploy_drift()'s new size discriminator on the REAL volatility-fetcher values
(the 2026-06-17 FP) + a true-half-land CONTROL (the discriminator must NOT blind real half-lands).
The detector classifier is replicated verbatim from infrastructure_monitor.lambda_function
(the in-Lambda boto3 scan cannot run from the dev box -- broken local CA path -- so the live
re-scan is the post-deploy `aws lambda invoke`; this proves the LOGIC on the exact FP case)."""
from __future__ import annotations


def classify(art_sha, dep_sha, art_lm, func_lm, art_size, dep_size):
    """Verbatim from check_deploy_drift() (post-fix): not-full-package > direction."""
    if not art_sha or art_sha == dep_sha:
        return "clean"
    if dep_size and art_size and art_size * 10 < dep_size:
        return "artifact-not-full-package"
    if func_lm is not None and art_lm > func_lm:
        return "half-landed"
    return "deployed-ahead"


CASES = [
    # (label, art_sha, dep_sha, art_lm, func_lm, art_size, dep_size, expected)
    ("volatility-fetcher (the real FP: 6KB source-only vs 58MB deps-bundled, artifact newer)",
     "RxfpdVqaz", "DCzdNd8l", "2026-03-24", "2026-02-23", 6350, 58785015, "artifact-not-full-package"),
    ("CONTROL true half-land (same-class 5.0MB artifact newer than 5.2MB deploy -> MUST still fire)",
     "aaa", "bbb", "2026-06-17", "2026-06-10", 5_000_000, 5_200_000, "half-landed"),
    ("CONTROL deployed-ahead (artifact OLDER, same-class)",
     "aaa", "bbb", "2026-06-01", "2026-06-10", 5_000_000, 5_200_000, "deployed-ahead"),
    ("CONTROL clean (sha match)",
     "aaa", "aaa", "2026-06-17", "2026-06-10", 6350, 58785015, "clean"),
    ("edge: tiny artifact but deployed also tiny (both source-only, no layer) -> real half-land",
     "aaa", "bbb", "2026-06-17", "2026-06-10", 6000, 6500, "half-landed"),
]


def main() -> int:
    ok = True
    for label, a_sha, d_sha, a_lm, f_lm, a_sz, d_sz, exp in CASES:
        got = classify(a_sha, d_sha, a_lm, f_lm, a_sz, d_sz)
        passed = got == exp
        ok &= passed
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")
        print(f"        got={got} expected={exp}")
    print("=" * 60)
    print("VERDICT:", "ALL PASS -- FP reclassified, true half-lands + deployed-ahead preserved"
          if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
