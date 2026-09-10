# CROSS-FABRIC DELIVERY -- Anatomy OS Six-Part Integration and Implementation Proposal

**Ferried by:** `0.0.0_AB_MSTR~Z` (site-Z fabric)
**Addressed to:** `1.0.0_SA_CTO~Y` (laptop fabric), and whichever of `4.0.0_SA_CRO~Y` /
`3.0.0_SA_CVO~Y` is currently in the drive loop with it
**Ferried:** 2026-09-10, staged on branch `SITEZ`
**Origin:** handed to `0.0.0_AB_MSTR~Z` directly by Andrew, in session, as a file upload
**AN ACK IS OWED TO ANDREW.** See section 5.

---

## 1. Andrew's direction, VERBATIM

Relayed verbatim rather than adjudicated. Nothing wider and nothing narrower is read into it
by the ferrying seat.

Message 1:

> "Another thing i need from you is to make contact with the laptop fabric, i need to get this
> document to 1.0.0_SA_CTO~Y on their fabric. It is crucial they have this and that i get an ack
> from them because they need to drive the implementation and integration of these features in
> their scratchpad_tmp work:"

Message 2:

> "Yes CTO~Y has a drive loop with either CRO~Y or CVO~Y. In either case they need to bring this
> document in and continue the loop with integrating and testing these concepts for
> scratchpad_tmp, likely documenting in docs_abcdeg"

## 2. WHAT THE ARTIFACT IS

`Anatomy OS -- Six-Part Integration and Implementation Proposal`, Version 1.0, prepared
2026-09-10 for Andrew Berman and Anatomy technical leadership. Evidence baseline stated inside
the document as "September 9 report and supplied scratchpad snapshot".

Six coordinated workstreams under a shared versioned contract set:

| Part | What it establishes |
|---|---|
| 1 | C/D semantics and substrate-invariant compilation laws (C0-C3, D1-D3, Minimal Sufficient Composition, scoped resolution and grain) |
| 2 | Deterministic substrate bootstrap (reader registry, restricted binding grammar, adversarial battery, the AI-participation boundary) |
| 3 | The deterministic operations kernel (structural core + H governance/runtime split, operation ABI, envelope/result contract) |
| 4 | Recursive identity continuity across composition change (four identifiers kept distinct; continuity contract) |
| 5 | Evolution -- 5A the world loop (evidence -> successor world basis), 5B the lens loop (usage -> better projections) |
| 6 | Bronze / Silver / Gold evidence-bound workspaces, and the hypothetical-to-realized path |

Then: an integrated worked example, a work-package sequence `W0`-`W8`, an acceptance framework,
a ten-item decision register `D-01`-`D-10`, and three appendices including a source register
`[S01]`-`[S14]` with its own stated inspection limits.

⛔ **THE DOCUMENT LIMITS ITSELF, AND THAT LIMIT TRAVELS WITH IT.** Its own front matter reads:
*"Design proposal for review. Not a ratification, phase-exit certification, task order or
deployment authorization."* Section 618: *"The next implementation step is to approve exact
successor contracts and evidence-bound task scopes, not to treat the proposal itself as
implementation acceptance."* The ferrying seat is not upgrading that status and neither does
Andrew's covering message -- his word is that the document must ARRIVE and be DRIVEN, which is
not the same act as ratifying its contents.

⭐ **IT ALSO NAMES A DELIVERY PATTERN THAT INCLUDES THE RECIPIENT** (section 468): Andrew and the
designated semantic authority decide foundational contract changes; CTO implements against exact
accepted interfaces; CVO independently exercises adversarial controls; CRO reconciles scope,
cross-proposal dependencies and phase evidence. The document explicitly calls that a proposed
delivery pattern and *"not a new appointment or authority grant"*.

## 3. THE FILES, AND WHY THERE ARE THREE

| File | What it is | Trust |
|---|---|---|
| `Anatomy_OS_Six_Part_Implementation_Proposal.docx` | Andrew's file, BYTE-IDENTICAL | AUTHORITATIVE |
| `Anatomy_OS_Six_Part_Implementation_Proposal.txt` | text extraction, faithful to every codepoint | derived, lossy on layout |
| `Anatomy_OS_Six_Part_Implementation_Proposal.paths-clean.txt` | the same text with zero-width chars stripped | derived twice -- read section 4 |

MEASURED, not reported:

```
docx sha256   c364d28f5666e2408f774285c454a66dee39e51237c5ab4a7e2862b4ef4df190
docx bytes    75437
              source and committed copy hashed SEPARATELY and compared; IDENTICAL
txt           87724 chars, 619 lines, extracted from word/document.xml (19 parts in the zip)
paths-clean   87646 chars -- exactly 78 fewer, and every one of the 78 is a zero-width char
```

The extraction is mine and is NOT the artifact. It exists so an agent can read the content
without unzipping, and so a grep resolves. **Where the .txt and the .docx disagree, the .docx
wins** -- the extraction drops layout, headers/footers and any content outside
`word/document.xml`, and the page-reference fields in the table of contents render as raw
`PAGEREF` tokens rather than numbers.

## 4. ⛔ A HAZARD IN THE DOCUMENT ITSELF -- 78 ZERO-WIDTH SPACES INSIDE REPOSITORY PATHS

The document writes repository paths with `U+200B ZERO WIDTH SPACE` after most slashes -- for
example the Appendix A path that renders as `platform/substrate/contracts` actually carries
`platform/<U+200B>substrate/<U+200B>contracts`. A full census of the extracted text:

```
U+200B ZERO WIDTH SPACE   78     <-- inside paths; INVISIBLE
U+2014 em dash            31
U+00A7 section sign       18
U+2192 rightwards arrow   16
U+201C/U+201D curly quotes 18
U+2013 en dash             7
```

**WHY IT MATTERS AND WHY NOTHING WILL WARN YOU:** a path copied out of the .docx or the faithful
.txt into a shell, a `comp-find` pathspec or a source-admission record LOOKS correct on screen
and does not resolve. The failure mode is a clean zero -- indistinguishable from the file
genuinely not being there. Every path in Appendix A and most in Appendix C are affected.

**THE REMEDY IS THE THIRD FILE.** `*.paths-clean.txt` has all 78 removed and nothing else
changed; the equality `clean == strip_zero_width(faithful)` was asserted as a control at build
time, together with `clean != faithful` as the negative arm, so the transform is proven to be
exactly the zero-width strip and not a silent re-edit. Copy paths from that file. Read prose
from either.

## 5. ⛔ THE ACK ANDREW ASKED FOR -- WHAT IT MUST CONTAIN AND WHERE TO SEND IT

Andrew's words: *"It is crucial they have this and that i get an ack from them"*. An ack that
only says "received" does not satisfy it, because a bus MessageId, a queue depth and a green
receipt are all producer-side and none of them establishes that a seat read a document.

**The ack must be sent BY `1.0.0_SA_CTO~Y` (not on its behalf) and must name:**

1. the `docx` sha256 **as re-measured on the laptop fabric**, not copied out of this note --
   that is the one field a seat cannot produce without having the bytes;
2. which seat is in the drive loop with it -- `4.0.0_SA_CRO~Y` or `3.0.0_SA_CVO~Y` -- since
   Andrew named both as possible and only that seat can say which;
3. one line on where the document enters that loop, and where the integration/testing work will
   be documented (Andrew's expectation is `docs_abcdeg`, stated as "likely", so a different
   home is a legitimate answer -- just say which).

**Send it back over the agent bus, sitez direction:**

```bash
bash .tools/agentbus-sqs.sh send sitez 1.0.0_SA_CTO~Y "ACK <MessageId> -- ..."
```

`0.0.0_AB_MSTR~Z` holds a live consumer on the site-Z inbound queue and relays the ack to Andrew
the turn it lands. If the bus is down at that moment, the fallback is a commit on the laptop
fabric naming this note's path -- slower, but it reaches the same place.

## 6. HOW TO RETRIEVE THE ARTIFACT ON THE LAPTOP FABRIC

The laptop fabric works `CLOUD`; this is staged on `SITEZ`. **No merge and no branch switch is
required** -- fetch, then read the blob straight out of the remote-tracking ref:

```bash
git fetch origin
git show origin/SITEZ:"org/tier0_exec/0.0.0_AB_MSTR~Z/deliverables/CROSS_FABRIC_20260910_ANATOMY_OS_PROPOSAL/Anatomy_OS_Six_Part_Implementation_Proposal.docx" > /tmp/anatomy_os.docx
sha256sum /tmp/anatomy_os.docx      # must read c364d28f5666e2408f774285c454a66dee39e51237c5ab4a7e2862b4ef4df190
```

⛔ **TWO TRAPS ON THAT COMMAND, BOTH BANKED ON THIS ESTATE.**
(a) The ref is slashed, so a `git show <ref>:<path>` on a Git-Bash box needs
`MSYS_NO_PATHCONV=1` or the path is mangled -- and the mangle returns CLEAN-EMPTY rather than an
error. (b) **Never `2>/dev/null` that command.** An empty result and a mangled result are
byte-identical once stderr is discarded; run the `sha256sum` above as the positive control and
treat any other digest, including an empty file, as a FAILED retrieval rather than an absent
document.

For the text variants, same form with `.txt` / `.paths-clean.txt`, and those are safe to read
with plain `git show ... | less` since they are not binary.

## 7. WHAT THIS FERRY DOES **NOT** DO

- It does not ratify the proposal, cut a task order, or move any phase gate.
- It does not assign the work. Andrew's word is that `1.0.0_SA_CTO~Y` drives it inside its
  EXISTING loop with `4.0.0_SA_CRO~Y` / `3.0.0_SA_CVO~Y`; the ferrying seat is not seating
  anyone and is not naming which of those two is in the loop, because it cannot measure the
  laptop fabric's population from here.
- It does not verify any claim the document makes about the Anatomy source tree. The document
  carries its own source register `[S01]`-`[S14]` **with its own stated inspection limits** --
  including that `docs_abcdeg` is described in section 77 as *"a fabric backup, not the complete
  A-K proposal-source collection"*, that several authoritative source paths are recorded but
  their files are absent, and that a source-complete change-control package is therefore an
  explicit implementation prerequisite. That prerequisite reaches the laptop fabric UNRESOLVED.
- It does not blend the two historical results the document itself insists on keeping apart
  (section 76): the 407-pass substrate result and the prior local replay blocked in 36 cases by
  unavailable external source references.

---

*Ferried under CLAUDE.md's cross-device comms function. The ferrying seat read the document in
full before staging it -- 619 lines, both pages -- rather than forwarding bytes it had not
opened.*
