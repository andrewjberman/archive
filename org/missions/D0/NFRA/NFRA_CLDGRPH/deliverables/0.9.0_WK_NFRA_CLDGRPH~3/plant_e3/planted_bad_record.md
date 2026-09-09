# E3-AC1 NEGATIVE CONTROL -- a disposition record with three defects

Fed through the SAME parser as the real record. Entry 2 has NO `owner`; entry 3
carries a disposition outside the closed vocabulary; entry 4's `reason` is a
label, not a reason. A parser that scores this 4 of 4 cannot certify the real
record, so `dispositions_recorded.sh` refuses to report FIRED unless this file
comes back short.

```json
{
  "cell": "CG-s-19-CONTROL",
  "p7_row_id": "NFRA_CLDGRPH-W3-S9999",
  "artifacts": [
    {
      "artifact": "control/well_formed_store",
      "size_bytes": 123,
      "mtime": "2026-06-12 09:55 local",
      "manifest": "control manifest",
      "disposition": "HOLD_PENDING_P7",
      "owner": "3.0.0_SA_CVO",
      "reason": "A well-formed control entry that must PASS, so the control measures the parser's discrimination rather than a blanket refusal of the whole file.",
      "later_act_if_any": "none",
      "p7_status": "control"
    },
    {
      "artifact": "control/store_with_no_owner",
      "size_bytes": 456,
      "mtime": "2026-06-12 10:57 local",
      "manifest": "control manifest",
      "disposition": "RETIRE_WITH_TOMBSTONE",
      "reason": "This entry is complete except that nobody owns it, which is the exact defect a disposition record exists to prevent: an artifact with a verdict and no seat.",
      "later_act_if_any": "none",
      "p7_status": "control"
    },
    {
      "artifact": "control/store_with_invented_disposition",
      "size_bytes": 789,
      "mtime": "2026-06-12 11:00 local",
      "manifest": "control manifest",
      "disposition": "PROBABLY_FINE",
      "owner": "0.8.0_AE_CloudComp",
      "reason": "The vocabulary is closed; a fifth value invented at the call site is how a closed enum stops being closed, and the parser must reject it here.",
      "later_act_if_any": "none",
      "p7_status": "control"
    },
    {
      "artifact": "control/store_with_a_label_for_a_reason",
      "size_bytes": 1011,
      "mtime": "2026-06-12 11:01 local",
      "manifest": "control manifest",
      "disposition": "KEEP_WITH_NAMED_READER",
      "owner": "0.8.0_AE_CloudComp",
      "reason": "stale",
      "later_act_if_any": "none",
      "p7_status": "control"
    }
  ]
}
```
