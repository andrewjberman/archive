# DSGN_AMGTV1 round 64 -- prep (2.0.0_SA_COO~D1, 2026-10-09 ~11:4xZ)

These are carried from the round-63 close (`round63/ROUND63_CLOSE.md` @bedf70c4bd), for the cut once the CTO's round-63 analysis lands.
Read at DEV candidate `f043b827`.

1. **The MACHINE chip sits on its own line above each sentence** (walk `tmp/ui-walk/20261009T113527Z` shot 008, ASML_NA_Equity).
   - Where: `components/ThesisCards.tsx` `SentenceBlock`. The sentence is one `<button data-sentence-press class="inline ...">`.
   - Cause: Chrome lays out a `<button>` as inline-block even under `display: inline`, so a sentence wider than the line takes a line of
     its own after the chip.
   - Fix shape: the press becomes a focusable inline `<span role="button" tabIndex={0}>` with the same `aria-controls`, `onClick` and
     an Enter/Space `onKeyDown`, so the chip and the sentence flow on one line. r63b arm 4 would need the element to read `role="button"`.
2. **The event titles stand in a band with nothing tying them to their markers** (walk `...T113121Z` shot 004, NVDA).
   - Order AV-zzo-2 item 4 allowed a 1px tick from a title to its marker, and the build drew none.
   - With the titles now above the plot, a reader cannot tell which spike a title names without hovering.
3. **The ASML picker reads "type the ticker." beside buttons that make typing unnecessary.** The words are the route's served reason.
   - AMGT_RESAPP round 84's collapse rule (route ruling ADDENDUM 2) may retire the panel for ASML.
   - Otherwise the page could print its own one-line lead ("Pick one:") and keep the served reason out of it. That is a CTO call under
     C-PRESENTATION-ONLY.
