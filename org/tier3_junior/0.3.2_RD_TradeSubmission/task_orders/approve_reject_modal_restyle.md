# TradeSubmission — Approve/Reject Modal Restyle

**Owner:** `0.3.2_RD_TradeSubmission`
**From:** `0.3.0_DE_TradingOperations`
**Priority:** High
**Status:** complete

---

## Problem

Andrew flagged the Approve modal on the Approvals tab as having "shit coloring and styling." Root cause review confirms multiple anti-patterns versus the canonical popup-modal style we ship on PortfolioManagement (`SecurityDetailModal.tsx`).

### Specific bugs in `ApproveModal.tsx`

| Line | Class | Problem |
|------|-------|---------|
| 56 | `text-[hsl(var(--bg-header))]` on the subtitle `{fund} • {submissionId}` | `--bg-header` is `navy-dark` (11% lightness) — a BACKGROUND token. Painting dark text on the dark card = invisible/illegible. |
| 72 | `text-[hsl(var(--primary))]` on the main body paragraph | `--primary` is the action/brand purple, not a body-copy token. |
| 75 | `text-[hsl(var(--bg-header))]` on the second body paragraph | Same root cause as line 56 — dark text on dark card. |
| 43 | `border-[hsl(var(--success))]/20` on the modal shell | Whole-card green tint. PM modals use neutral `border-white/20`. |
| 47 | `bg-[hsl(var(--success))]/10` + `border-[hsl(var(--success))]/20` on the header | Heavy green wash across the entire header band. PM uses neutral `bg-[hsl(var(--bg-header))]` + `border-white/10`; accent color belongs on the icon chip, not the whole header. |
| 41–45 | Dual-div backdrop with `pointer-events-none` / `pointer-events-auto` | Non-canonical. PM uses a single overlay div with `onClick={onClose}` and `e.stopPropagation()` on the inner shell. |
| 53 | `text-[hsl(var(--success))]` on the H2 title | PM headings are `text-white` regardless of action — accent only on the icon chip. |

`RejectModal.tsx` has the exact same parallel bugs (lines 54, 58, 64, 67, 83, 95). Fix both modals in this TO.

---

## Reference — Canonical PM Modal Pattern

Source of truth: `portal/src/pages/PortfolioManagement/components/SecurityDetailModal.tsx` (lines 64–306). Mirror its structure exactly.

### Outer overlay (single div, click-to-close)

```tsx
<div
  className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm"
  onClick={onClose}
>
```

Drop the `pointer-events-none` + `pointer-events-auto` dance and the wrapping `<>` fragment. One overlay, one click handler.

### Inner shell

```tsx
<div
  className="bg-[hsl(var(--bg-card))] border border-white/20 rounded-lg shadow-2xl max-w-md w-full mx-4 overflow-hidden flex flex-col"
  onClick={(e) => e.stopPropagation()}
>
```

- `border-white/20` — NEUTRAL, not success/danger tinted
- `rounded-lg` (not `rounded-xl`)
- Keep `max-w-md` for these confirmation modals (PM's SecurityDetailModal is `max-w-4xl` because it's a data viewer; confirms stay tight)

### Header (neutral bg, accent ONLY on icon chip)

```tsx
<div className="px-6 py-4 border-b border-white/10 bg-[hsl(var(--bg-header))] flex items-center justify-between flex-shrink-0">
  <div className="flex items-center gap-3">
    <div className="p-2 rounded-lg bg-[hsl(var(--success))]/20">
      <CheckCircle size={20} className="text-[hsl(var(--success))]" />
    </div>
    <div>
      <h2 className="text-lg font-semibold text-white">Approve Trade Submission</h2>
      <p className="text-sm text-white/60 mt-0.5">{fund} <span className="mx-1 text-white/30">·</span> {submissionId}</p>
    </div>
  </div>
  <button
    onClick={onClose}
    className="p-2 text-white/40 hover:text-white/80 hover:bg-white/10 rounded transition-colors"
    disabled={isSubmitting}
  >
    <X size={20} />
  </button>
</div>
```

Key changes:
- Header bg = `bg-[hsl(var(--bg-header))]` (NOT `bg-[hsl(var(--success))]/10`)
- Border = `border-white/10` (NOT `border-[hsl(var(--success))]/20`)
- H2 = `text-white` (NOT `text-[hsl(var(--success))]`)
- Subtitle = `text-white/60` with a `·` separator (NOT `text-[hsl(var(--bg-header))]` + bullet)
- The icon chip — `bg-[hsl(var(--success))]/20` + colored icon — is the ONLY place success-green appears in the header. That's the entire visual cue for "this is the approve action."
- Close X uses PM's hover treatment: `text-white/40 hover:text-white/80 hover:bg-white/10`

### Body content

```tsx
<div className="px-6 py-5 bg-[hsl(var(--bg-header))]">
  <p className="text-sm text-white/80 mb-3">
    You are about to approve this trade submission with <span className="font-semibold text-white">{securitiesCount} securities</span>.
  </p>
  <p className="text-sm text-white/60">
    Once approved, the trade will move to the <span className="font-semibold text-white/80">Execution</span> tab where it can be executed and sent to the brokerage.
  </p>
</div>
```

- Body bg `bg-[hsl(var(--bg-header))]` — unifies with header and footer (PM's `flex-1 overflow-y-auto bg-[hsl(var(--bg-header))]` pattern).
- Primary text `text-white/80`, secondary `text-white/60`. NEVER `text-[hsl(var(--bg-header))]` and NEVER `text-[hsl(var(--primary))]`.
- Inline emphasis: `font-semibold text-white` for hard emphasis, `font-semibold text-white/80` for soft.

### Footer (mirror PM)

```tsx
<div className="px-6 py-3 border-t border-white/10 bg-[hsl(var(--bg-header))] flex items-center justify-end gap-3 flex-shrink-0">
  <Button variant="outline" onClick={onClose} disabled={isSubmitting}>Cancel</Button>
  <Button variant="success" onClick={handleConfirm} disabled={isSubmitting}>
    {isSubmitting ? 'Approving...' : 'Approve Trade'}
  </Button>
</div>
```

- `bg-[hsl(var(--bg-header))]` so the footer band reads as one piece with header + body
- `border-t border-white/10` (PM uses white/10 throughout for internal dividers)
- `flex-shrink-0` so the footer doesn't compress on small viewports

---

## RejectModal — Apply the same pattern

Mirror everything above, swapping `success` → `danger` and `CheckCircle` → `AlertTriangle`. The accent appears in:
- Icon chip: `bg-[hsl(var(--danger))]/20` + `text-[hsl(var(--danger))]` icon
- Required-field asterisk: keep `text-[hsl(var(--danger))]` on the `*`
- Textarea focus ring: keep `focus:ring-[hsl(var(--danger))]`
- Submit button: `variant="danger"`

Everything ELSE — H2 color, subtitle color, body text, borders, header bg — goes neutral white-on-navy per the PM pattern.

For the textarea:
- Keep `bg-black/20` + `border-white/20` + `placeholder-white/40` + `text-white`
- Label color: `text-white/80` (NOT `text-[hsl(var(--primary))]`)
- Helper text under the textarea: `text-xs text-white/50` (NOT `text-[hsl(var(--bg-header))]`)

---

## Color rule (commit this to memory)

| Token | What it IS | Where it's allowed |
|-------|------------|-------------------|
| `--bg-header` | navy-dark BACKGROUND (11% lightness) | `bg-*` classes only. NEVER `text-*`. |
| `--bg-card` | navy-light BACKGROUND | `bg-*` classes only. NEVER `text-*`. |
| `--primary` | brand action purple | Action buttons, focus rings, active states. NEVER body copy. |
| `--success` / `--danger` | semantic accent | Icon chips, action buttons, focus rings, the `*` on required fields. NEVER full-header washes, NEVER body copy, NEVER H2 titles. |
| `text-white`, `text-white/80`, `text-white/60`, `text-white/40` | the body-copy ladder | All H2/H3/paragraph/label text on dark modals. This is the PM pattern. |

If you ever feel like reaching for `text-[hsl(var(--bg-header))]` on a dark surface — stop. That's a background token. Use `text-white/{60|80}` instead.

---

## Acceptance Criteria

1. `ApproveModal.tsx` and `RejectModal.tsx` use the single-overlay pattern (no `pointer-events-none`/`pointer-events-auto` dual-div).
2. Both modals' headers use `bg-[hsl(var(--bg-header))]` and `border-white/10` — no full-header success/danger wash.
3. Both modals' H2 titles render in `text-white` — accent color only on the icon chip and (Reject) the `*` and focus ring.
4. Zero occurrences of `text-[hsl(var(--bg-header))]` or `text-[hsl(var(--primary))]` in either file. Body text uses the `text-white/{40|60|80}` ladder exclusively.
5. Modal shell border is `border-white/20` (neutral), not success/danger tinted.
6. Both modals open and close cleanly (overlay click, X button, Cancel button, Esc still works if it did before).
7. `bun run lint` from `portal/` produces zero NEW warnings on these two files.
8. `bun run build` from `portal/` succeeds with no NEW TypeScript errors on these two files.
9. Visual check: open Approvals tab, click Approve — modal looks visually consistent with PortfolioManagement → Trade tab → click any security → SecurityDetailModal. Same border treatment, same header bg, same text-on-dark legibility. Then do the same for Reject.

---

## Out of Scope

- `TradeDetailsModal.tsx` and `ExecuteModal.tsx` — leave alone. If the same bugs are present there, raise it back to me as a follow-up TO; do not expand scope here.
- The Approvals tab card grid itself — only the two modals.

---

## Reference Files

- Source of truth: `portal/src/pages/PortfolioManagement/components/SecurityDetailModal.tsx`
- Files to fix: `portal/src/pages/TradeSubmission/components/ApproveModal.tsx`, `portal/src/pages/TradeSubmission/components/RejectModal.tsx`
- Color tokens: `portal/src/index.css` lines 33–106

---

## Commit & Sign-Off

```bash
git commit --author="0.3.2_RD_TradeSubmission <0.3.2_RD_TradeSubmission@opal.agent>" \
  -m "0.3.2_RD_TradeSubmission: TradeSubmission -- restyle Approve/Reject modals to match PM SecurityDetailModal canonical pattern" \
  -- portal/src/pages/TradeSubmission/components/ApproveModal.tsx \
     portal/src/pages/TradeSubmission/components/RejectModal.tsx
```

When done: flip `<status>pending</status>` → `<status>complete</status>` in this file and MCP me back with the commit hash. I'll hand off to 0.3.0_DT_TradingOperations for the DEV push.
