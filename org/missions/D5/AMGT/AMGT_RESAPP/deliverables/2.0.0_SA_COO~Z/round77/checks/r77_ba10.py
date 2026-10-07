"""AMGT_RESAPP round 77 -- AMGT-ba-10: the translated text on a served sentence (row Z-S221; CTO ADDENDUM 1 @3bad4be9e0).

  --crit AC1|AC2 --where local

AC1 (build): `lib.research.api.translated_text.served_translation(sentence)` returns exactly the three served fields
    `text_translated`, `translated` and `source_language`:
    C1 a drafted sentence carrying text_translated and translation{translated True, source_language "ja"} serves the
       translated text, translated True and "ja";
    C2 a sentence with no translation serves text_translated None, translated False, source_language None (no value is
       made up);
    C3 a sentence whose translation FAILED (translation{translated False, failed True, source_language "de"}) serves
       translated False, text_translated None and "de";
    C4 the function returns a NEW dict and does not change the sentence it was given.
AC2 (build): the plant tests in lib/research/api/tests/test_translated_text.py pass.
Verdict: R77 BA10 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import copy
import os
import subprocess
import sys

TEST = "lib/research/api/tests/test_translated_text.py"
FIELDS = {"text_translated", "translated", "source_language"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC2":
        if not os.path.isfile(TEST):
            clause("C1 the plant test file exists", False, TEST)
            return verdict(a, ok)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST], capture_output=True,
                           timeout=600)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C1 every plant case passes", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               f"rc={p.returncode}")
        return verdict(a, ok)

    try:
        from lib.research.api import translated_text
    except ImportError as err:
        clause("C0 lib.research.api.translated_text imports", False, str(err))
        return verdict(a, ok)
    fn = getattr(translated_text, "served_translation", None)
    if not callable(fn):
        clause("C0 translated_text.served_translation exists", False, "absent")
        return verdict(a, ok)
    yes = {"text": "ORIGINAL", "text_original": "ORIGINAL", "text_translated": "Sales guidance in English.",
           "translation": {"translated": True, "source_language": "ja", "translated_at": "2026-10-01T00:00:00Z"}}
    no = {"text": "Plain English sentence.", "text_original": "Plain English sentence."}
    failed = {"text": "Ein Satz.", "translation": {"translated": False, "failed": True, "source_language": "de"}}
    before = copy.deepcopy(yes)
    g1, g2, g3 = fn(yes), fn(no), fn(failed)
    clause("C1 a translated sentence serves the text, the flag and the language",
           set(g1) == FIELDS and g1["text_translated"] == "Sales guidance in English." and g1["translated"] is True
           and g1["source_language"] == "ja", str(g1))
    clause("C2 an untranslated sentence serves no made-up value",
           set(g2) == FIELDS and g2["text_translated"] is None and g2["translated"] is False
           and g2["source_language"] is None, str(g2))
    clause("C3 a failed translation reads translated False with its language",
           set(g3) == FIELDS and g3["text_translated"] is None and g3["translated"] is False
           and g3["source_language"] == "de", str(g3))
    clause("C4 the sentence handed in is unchanged and a new dict is returned", yes == before and g1 is not yes)
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R77 BA10 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
