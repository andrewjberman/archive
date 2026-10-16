# TEST READ R148 -- DB-c-27 (not a serve, not a production run)

Read at 2026-10-16T06:06:50Z: 2 list calls, 1878 get calls, 0 writes, 0 invokes. Counts only.

What the page does with the real Cottonwood publish:

- 939 series documents and 939 manifests under the prefix; nothing else in the listing.
- All 939 documents parse, carry the unreported-days pair, and are read by the page's reader. None refused, none threw.
- 917 of 939 accounts print the "not reported by the source" sentence, exactly one each. The other 22 have an empty list and print nothing.
- Every printed count equals its document's list length (0 mismatches), so every listed day falls inside the account's first-data-to-as-of window.
- Listed days total 2529; the longest list is 3 days.
- Income: null on every entry of every document (939 of 939 all-null), no number anywhere. The page reads it as null and never as 0 (0 coerced).
- Income claim: the key is absent from all 939 documents.
- History scope: PARTIAL_HISTORY on all 939 documents.
- Manifests: the calendar_source key is absent on all 939 (read as ABSENT).

Looks wrong or worth a look:

- Income is null for every account in the publish. Either no income is measured yet or the publisher writes nulls for all. The page is honest about it, but no account shows income.
- Every account is PARTIAL_HISTORY. The partial-history wording will show on every screen.
- The manifests carry no calendar_source, so the calendar basis of the unreported-days statement is not stated in the manifest.
- The page's income-coercion check compares the reader's output to an untouched copy of the raw parse; it can only catch a coercion inside the reader.

No identifier, key or value is recorded here.
