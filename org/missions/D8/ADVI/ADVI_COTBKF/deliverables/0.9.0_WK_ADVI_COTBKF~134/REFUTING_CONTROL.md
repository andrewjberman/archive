# CB-bw-3 refuting control (round 75, 0.9.0_WK_ADVI_COTBKF~134)

Rule unchanged (round 74, VALIDATED_UNADJUSTED.json): equal within 0.5 percent; compared = own-date bar plus previous bar within 5 days; match on own or previous bar; validated >= 10 compared and >= 0.80; refuted >= 10 compared and <= 0.30; else unreadable. Only the cache column was switched. Nothing fetched.

- Reproduced on Close over 270 series: 33 validated / 0 refuted / 237 unreadable.
- Control on Adj Close over the 33: 33 refuted (19 left_on_store, 14 substituted), 0 unreadable, 0 validated. Adjusted matches 6 of 804 compared dates (matching share 0.00 to 0.17).
- Not refuted: none. For every fund the last distribution step in the cache window falls after all compared dates (0 percent after it).
- arm_shown_able_to_refute: true. A fund with small or recent distributions would read the same on both columns; none of these 33 does.
- Sensitivity (not the result): R would need only be >= 0.1667 for all 33 adjusted to refute; the lowest unadjusted share is 0.8966, so no unadjusted column refutes at that R.
- Companion fact (round 74): adjusted also matches 6 of 804 dates inside the 33 (19 of 944 overall); this control agrees.
- Not established: behaviour for funds with small or recent distributions; status of the 237 unreadable.
