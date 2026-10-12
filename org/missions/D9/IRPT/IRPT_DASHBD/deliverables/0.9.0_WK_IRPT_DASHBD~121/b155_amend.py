"""IRPT_DASHBD.TO-DB-b-155: amend TIMING_CLASSES_PROPOSAL.json -- rename the first axis and its two values (CTO msg 5886).
Text-level edits only (the file's indentation, key order, line endings and final newline are kept); recomputes no segment.
Usage: python b155_amend.py <path to TIMING_CLASSES_PROPOSAL.json> <sha256 of y1_place.py>
"""
import json
import re
import sys

A = "RESTATED_CLOSES_UNDER_OTHER_TIMING"
B = "RESTATED_DOES_NOT_CLOSE_UNDER_OTHER_TIMING"
AX = "RESTATED_CLOSE"

path, sha = sys.argv[1], sys.argv[2]
raw = open(path, "rb").read()
assert b"\r" not in raw and raw.endswith(b"}\n")
s = raw.decode("utf-8")


def once(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:70])
    s = s.replace(old, new)


# ---- protect the quoted ruling block of msg 5835 (history; may name the old tokens)
i0 = s.index(' "ruling_kept_in_its_words": {')
i1 = s.index("\n },\n", i0) + len("\n },\n")
protected = s[i0:i1]
s = s[:i0] + "@@PROTECTED@@\n" + s[i1:]

# ---- the token_census: replace the two RECONCILES entries by the two new ones
c0 = s.index('  {\n   "token": "RECONCILES_YES",')
c1 = s.index('  {\n   "token": "TIMING_START",')
new_census = '''  {
   "token": "%(A)s",
   "pattern": "\\\\b%(A)s\\\\b",
   "files_scanned": 76190,
   "hits": 0,
   "what_the_hits_are": "0 occurrences in any file, taken BEFORE this order wrote the token into any file (so no hit is this order's own). No existing use: no collision. Case-insensitive (-i), native Grep tool over the worktree; denominator 76190 = 76190 tracked (git ls-files, counted at the start of this order) + 0 untracked-not-ignored (git ls-files -o --exclude-standard); gitignored files not scanned.",
   "stem_pattern": "\\\\bRESTATED_CLOSES_UNDER_OTHER\\\\b",
   "stem_hits": 0,
   "stem_what_the_hits_are": "the bare stem (the part before the last underscore, RESTATED_CLOSES_UNDER_OTHER): 0 occurrences, same corpus, same denominator, same time of reading. No collision."
  },
  {
   "token": "%(B)s",
   "pattern": "\\\\b%(B)s\\\\b",
   "files_scanned": 76190,
   "hits": 0,
   "what_the_hits_are": "0 occurrences in any file, taken before this order wrote the token into any file. No collision. Same corpus and denominator as above.",
   "stem_pattern": "\\\\bRESTATED_DOES_NOT_CLOSE_UNDER_OTHER\\\\b",
   "stem_hits": 0,
   "stem_what_the_hits_are": "the bare stem (RESTATED_DOES_NOT_CLOSE_UNDER_OTHER): 0 occurrences, same corpus, same denominator. No collision.",
   "family_note": "the shared lead word: \\\\bRESTATED_[A-Z_]+ (case-insensitive, same corpus) hits 70 times in 20 files. None is either token or either stem. They are RESTATED_TIEOUT and lowercase restated_* column and variable names of this project's restated tie-out (the same sense: a return restated under a convention), RESTATED_KEYS (an unrelated archive script of another project) and restated_flag and restated_delta_vs_chosen (an unrelated flow-ledger and slice builder). Adjacent, not a collision: no second meaning is introduced."
  },
''' % {"A": A, "B": B}
# the stem key is a label, not a token: drop the artificial "stem" field (kept simple)
new_census = re.sub(r'   "stem": "[A-Z_]+_stem",\n', "", new_census)
s = s[:c0] + new_census + s[c1:]

# ---- the instrument note gains the second census
once('"census_instrument_note": "comp-find -i',
     '"census_instrument_note": "(order DB-b-155 added: the two renamed tokens were censused with the native Grep tool alone, comp-find not run, over 76190 tracked files and 0 untracked-not-ignored; the four TIMING entries keep the earlier denominator of 76097 as filed by order DB-b-148, not re-taken.) comp-find -i')

# ---- new_tokens + superseded_tokens + the amendment note
once('"new_tokens": ["RECONCILES_YES", "RECONCILES_NO", "TIMING_START", "TIMING_MID", "TIMING_END", "TIMING_NOT_DETERMINED"],',
     '"new_tokens": ["%s", "%s", "TIMING_START", "TIMING_MID", "TIMING_END", "TIMING_NOT_DETERMINED"],\n@@SUPER@@' % (A, B))
SUPER = ('\n'
     ' "superseded_tokens": {\n'
     '  "tokens": ["RECONCILES_YES", "RECONCILES_NO"],\n'
     '  "retired_by": "1.0.0_SA_CTO~DELL2 msg 5886 (2026-10-11 ~21:40Z)",\n'
     '  "why": "END is the SERVED convention, and END closes in 0 of 51. So no segment\'s served return closes against the custodian\'s; what closes is a RESTATEMENT under START or MID. RECONCILES_YES would be read as \'our number matches\'. It does not. Nothing served is relabelled.",\n'
     '  "replaced_by": {"RECONCILES_YES": "%s", "RECONCILES_NO": "%s"},\n'
     '  "reason_for_the_chosen_tokens": "Each token carries RESTATED (what was done to the return) and OTHER_TIMING (the served timing, END, is not the one that closes), so a reader meeting the token alone cannot read it as the served number matching; the lead RESTATED also keeps the axis apart from the TIMING axis, whose name and values lead with TIMING. The negative says DOES_NOT_CLOSE rather than a bare NO, so it is not read as a label of disagreement with the served number (the served END closes in none of the 51; a segment whose only closing timing is END would also fall here).",\n'
     '  "alternative_rejected": "RESTATED_CLOSE_YES and RESTATED_CLOSE_NO: a trailing YES or NO is the very shape the ruling objected to (a reader takes the last word and reads \'closes: yes\' as \'matches\'), and neither names the timing that is not the served one. Also rejected, CLOSES_ONLY_WHEN_RESTATED: false for a segment that closed under END and under START together.",\n'
     '  "claim": "the retirement is the CTO\'s ruling (held); the replacement tokens are a proposal"\n'
     ' },\n'
     ' "amended_by": {"to": "IRPT_DASHBD.TO-DB-b-155", "worker": "0.9.0_WK_IRPT_DASHBD~121", "what": "first axis renamed from RECONCILES to %s and its two values replaced, per the ruling above; no count and no placement changed; no segment recomputed; the earlier order\'s proof instance is untouched", "tokens_in_the_record_before": ["RECONCILES_YES", "RECONCILES_NO"]},'
     % (A, B, AX))
SUPER = SUPER.lstrip("\n")

# ---- the producer sha256 (y1_place.py's printed labels changed, its logic did not)
once('"sha256": "ac52c6032bc904f0a1789ae86faad4bc9595b87fc18605ec88e5faaf43432ff5",', '"sha256": "%s",' % sha)
once('"reads": "private pickles', '"label_edit": "order DB-b-155 changed only the printed placement labels and one print caption (the old tokens to the new ones); the logic, the inputs and the counts are unchanged", "reads": "private pickles')

# ---- spelling style
once("The axis prefix (RECONCILES_, TIMING_) is carried", "The axis prefix (RESTATED_, TIMING_) is carried")

# ---- the first axis entry
a0 = s.index('  {\n   "name": "RECONCILES",')
a1 = s.index('  {\n   "name": "TIMING",')
axis = '''  {
   "name": "%(AX)s",
   "question": "When the segment's return is restated under an admitted flow timing other than the served one (START or MID; END is the served convention), does the restated return close against the other system's return within tolerance, with the dollars and flow days tying?",
   "domain": "tie-out segments whose dollars and flow days were read on both sides",
   "domain_changed_by_the_rename": "no: the set is the same 90 segments by the same membership rule. What changes is the condition: a close under END alone no longer counts (END is the served convention). No segment of the 90 is moved by that: END closes in 0 of the 51, and the 39 outside the first value fail the four-item dollar tie in every case (0 of 31, 0 of 8), so none of them could have entered it by an END close.",
   "values": ["%(A)s", "%(B)s"],
   "value_meaning": {
    "%(A)s": "the return restated under START or MID closes within 0.35 pp; AND the four dollar items tie; AND the flow-day sets are equal. It is never a statement that the served number matches: the served convention is END, and END closes in 0 of the 51",
    "%(B)s": "the segment is in the domain and at least one of those three conditions fails: no restatement under START or MID closes, or the four items do not all tie, or the flow-day sets differ"
   },
   "claim_field": "restated_close_claim",
   "claim_by_value": {"%(A)s": "measured", "%(B)s": "measured"},
   "consumer_rule": "a consumer rejects any row holding a %(AX)s value whose restated_close_claim is not measured",
   "domain_size_now": 90,
   "domain_membership_rule": "a segment is in the domain when a two-sided dollar read (custodian point for the range against the served daily series) and a flow-day comparison exist for it; today that is the 90 segments of worker 108's table"
  },
''' % {"AX": AX, "A": A, "B": B}
s = s[:a0] + axis + s[a1:]

# ---- the TIMING axis: its domain and the empty END value
once('"domain": "segments that reconcile (RECONCILES = RECONCILES_YES)",',
     '"domain": "segments whose restated return closes under another timing (%s = %s)",' % (AX, A))
once('"TIMING_END": "exactly one admitted timing closes and it is END (no member today: END closes in 0 of the 51)",',
     '"TIMING_END": "exactly one admitted timing closes and it is END (no member: END closes in 0 of the 51, and by construction of the renamed domain, which requires a close under START or MID, no member can exist; the ruling keeps the token, and the empty value is filed as a row)",')

# ---- the intent-coherence finding, rewritten in the new tokens
i0 = s.index('   "finding": "One axis, one intent. RECONCILES asks only')
i1 = s.index("\n", i0)
s = s[:i0] + ('   "finding": "One axis, one intent. %(AX)s asks only whether a RESTATEMENT closes: whether the return, restated under an admitted timing other than the served one, ties to the other system with its dollars and flow days; it is measured. TIMING asks only which convention produced the other system\'s number and is inferred. What the CTO ruling (msg 5886) found: END is the served convention and END closes in 0 of 51, so no segment\'s served return closes against the custodian\'s, and what closes is a restatement under START or MID. The first axis therefore measures a restatement closing, NOT the served number matching, and the renamed values say so; the earlier RECONCILES tokens could be read as the served number matching, which is not the case for any of the 51. No %(AX)s value says anything about which timing and no TIMING value says anything about whether the segment closes: TIMING_NOT_DETERMINED is not %(B)s (47 of 51 close when restated and cannot be timed), and %(B)s carries no timing. The label CONTESTED today mixes the two intents: it names a disagreement (the return does or does not tie) for segments whose only open question is a fact no record can state (the time of day), which is the break this proposal separates.",'
            % {"AX": AX, "B": B}) + s[i1:]

# ---- known plain-word and compound forms, then the tokens
subs = [
    ("RECONCILES_NO_39", "restated_no_close_39"),
    ("in_RECONCILES_domain", "in_RESTATED_CLOSE_domain"),
    ("RECONCILES_YES", A),
    ("RECONCILES_NO", B),
    ("RECONCILES domain", AX + " domain"),
    ("RECONCILES rule", AX + " rule"),
    ("RECONCILES_* ", AX + " "),
    ("is RECONCILES (", "is " + AX + " ("),
    ("RECONCILES is one segment's return against one custodian point", AX + " is one segment's restated returns against one custodian point"),
    ("RECONCILES values", AX + " values"),
    ("RECONCILES value", AX + " value"),
    ("(RECONCILES = ", "(" + AX + " = "),
    ("RECONCILES-", AX + "-"),
]
for old, new in subs:
    s = s.replace(old, new)

s = s.replace("@@PROTECTED@@\n", protected)
assert s.count("@@SUPER@@") == 1
s = s.replace("@@SUPER@@", SUPER)
left = [(n + 1, ln) for n, ln in enumerate(s.split("\n")) if "RECONCILES" in ln.upper() and "ruling_kept" not in ln]
print("lines still naming RECONCILES (outside the protected block):")
for n, ln in left:
    print(n, ln[:230])
json.loads(s)
open(path, "wb").write(s.encode("utf-8"))
print("written; bytes", len(s.encode("utf-8")))
