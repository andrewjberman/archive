# IB-rtf-14 result (first pass): NO GRANT IS SIGNED. The cause is not an IAM gap -- the address has no writer and is not declared, and the UNEXPECTED is an exception-CLASS mapping bug. R71-AC1 FAIL 1 of 4, STOPPED at the halves exactly as the face expects

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-14.the-export-role-reads-the-receipt-it-serves.md` @`19ccf82226`. GO msg 98314.

**Packet:** `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-14.md`, blob `a50a7d0e5b38d7b7cbce3ddedffac146c6790d32` @`1df0578d76`. **Halves: 0 of 2 (both ABSENT).**

**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`. Base: CLOUD merged, `53fa406bf4`.

**Graded run:** `timeout 1800 py -3.12 .../battery_ib_rtf_14.py` @`07d682522c`, 19:12:37-19:12:48Z, rc 1.

---

## R71-AC1: FAIL, by output -- 1 of 4 arms hold

| arm | verdict |
|---|---|
| (a) the cause, measured | **PASS** (see the qualifier in s.2 -- one sub-instrument was unavailable and was substituted) |
| (b) the packet + the halves | **FAIL** -- packet committed and unchanged, halves **0 of 2** |
| (c) apply | **NOT RUN** -- there is nothing to apply, and no half is at HEAD |
| (d) the live proof | **NOT RUN** -- gated behind (c) |

The token was not printed. **This is the face's own expected first-pass outcome** (*"ABSENT = STOP, FAIL truthfully, ONE report with the blob (the expected first-pass outcome)"*), with one difference from what the face anticipated: **the second pass will not apply anything either, because the packet signs NO GRANT.**

---

## 1. THE ANSWER: the order's second branch, taken on measurement

The face gave two branches and this is the second: *"OR, if (a)(iv) shows the receipt is absent, NO grant and instead a ROW for the CTO ... the packet states which."*

**(a)(iv) shows ABSENT -- and the measurement goes further than the branch anticipated:**

1. **The key is OUTSIDE the grant.** `investor-reporting/export/{firm}/{export_id}/receipt.json` (`export/entry.py:63-64` @`53fa406bf4`, `IRPT_EXPORT_RECEIPT_KEY` **UNSET** on the deployed function). `fnmatch` against **all 7** of the role's `s3:GetObject` resource ARNs (of **15** across **4** policies, read live): **0 match -> OUTSIDE**.
2. **The object does not exist -- and neither does anything else at that address.** `list-objects-v2` under `investor-reporting/export/` (the **whole** template root, not the one key): **KeyCount 0**. The policy's prefix holds the writer's evidence: **2** objects, both `firms/49financial/generations/GENRT8PROOF/attempts/1/exports/<rev>/bundle.json`.
3. **The address is not a DECLARED prefix.** `core/layout.json` @`53fa406bf4` -- terraform-generated, and its own `_meta` says *"IB-s-5 binds the FirmDestinationPolicy and the per-firm IAM conditions to THIS declaration"* -- declares **three** families, all `firms/{firm_id}/...`, plus `quarantine/`. `_keys/keys.py:109-113` holds the same three as the runtime source, cross-checked by `verify_against_layout()`. `investor-reporting/export/` is in **neither**.
4. **No writer produces it.** Writer census over **38,998** files (tracked + untracked, this worktree): **3** sites build a `receipt.json` object key -- `intake/poller.py:418`, `ycharts/generate/job.py:325` and `:478` -- **all three** through the declared families. `export/handler.py:126-130` writes the export's own evidence at `.../exports/<rev>/bundle.json`, the grant's exact shape. **Writers of the reader's address: 0.**

**So a grant would widen an IAM role onto an UNDECLARED prefix of the shared evidence bucket, to reach an object nothing writes.** That is refused, and the packet says so in terms.

> **THE FACE'S OWN PARENTHETICAL IS CONTRADICTED, AND IT IS THE HINGE.** (a)(i) states the concrete key is `firms/<firm>/...`. It is not. Had that premise held, branch 1 -- one resource-ARN correction -- would have been right. **The key is in a different address space entirely**, which is what converts the answer from "one ARN" to "no grant". Recorded here rather than silently corrected, because the issuer's next cut depends on it.

---

## 2. THE INSTRUMENT THE FACE NAMED WAS NOT AVAILABLE -- what replaced it, and what it cannot cover

The face requires *"the recorder-patched diagnostic pair AS THE ROLE printing the swallowed exception verbatim (code, action, resource)"*. **That instrument cannot run, for two structural reasons, and this is the one place where this seat's PASS on (a) differs from the face's literal words:**

- `irpt-export-render-role`'s trust policy names **`lambda.amazonaws.com` only** -> `sts:AssumeRole` returns AccessDenied for `user/Andrew_Berman`. **The role is not assumable by this seat at all.**
- The boundary records internal errors to a **None sink (S91)**, so the class is not recoverable from the served answer or from CloudWatch.

**Two instruments replaced it, and between them they close the question anyway:**

**(A) THE LIVE INVOKE PAIR, as the deployed role** -- the discriminator that the failure IS the read:

| arm | result |
|---|---|
| the S3 receipt read, as deployed | 200, `public_reason_code` **UNEXPECTED**, `firm_id` present |
| `receipt_fixture {}` (read bypassed) | 200, **no refusal code**, `firm_id` present |

**(B) THE REAL WIRE CLASSES, on the same object.** An UNSIGNED request reproduces the exact 403 the role receives; the requester does not change how botocore parses the response:

| request | HTTP | code | class | the handler's test |
|---|---|---|---|---|
| UNSIGNED, the concrete key | **403** | `AccessDenied` | `botocore.errorfactory.AccessDenied` | **NOT mapped -> propagates -> UNEXPECTED** |
| operator, the concrete key | **404** | `NoSuchKey` | `botocore.errorfactory.NoSuchKey` | mapped -> `ExportRefused` -> NOT_FOUND |
| UNSIGNED, a key inside the grant | 403 | `AccessDenied` | `botocore.errorfactory.AccessDenied` | NOT mapped (control) |
| operator, a key inside the grant | 200 | -- | -- | the object reads (positive control) |

`export/entry.py:100-103` @`53fa406bf4` tests `exc.__class__.__name__ in ("NoSuchKey", "ClientError")`. **That is the whole of S104's operator-vs-role asymmetry: one code path, two served answers, no code difference between them.**

**What the substitute does NOT cover, stated so nobody reads more into it:** the live exception object itself is still never printed. The wire arm proves what class a 403 on this object produces and what the handler does with it; it does not prove that the live invocation's exception was that object. **The chain is: the pair shows the failure is in the read; the read can only fail as a 403 for this role (simulate: implicitDeny, controls 6 of 6); a 403 produces `AccessDenied`; `AccessDenied` is unmapped.** Every link is measured, and the conclusion is an inference across them rather than one printed traceback.

---

## 3. THE STUB AND THE WIRE DISAGREED, AND THE STUB READ GREEN

The battery runs **both**, and keeps both in the record:

- **Stub arm:** a hand-built `botocore.exceptions.ClientError` carrying error code `AccessDenied`, raised through the **deployed bytes** -> `_load_receipt` raises `entry.ExportRefused`. **GREEN. And wrong about the live class.**
- **Wire arm:** the real 403 -> `botocore.errorfactory.AccessDenied`. **NOT mapped.**

**A stub asserts the class its author assumed; botocore's errorfactory mints a MODELED class per error code and raised a different one.** Measured with botocore 1.43.0: `AccessDenied->AccessDenied`, `NoSuchKey->NoSuchKey`, `NoSuchBucket->NoSuchBucket`, `KMS.AccessDeniedException->ClientError`. **Of the four codes this route can receive, three produce a name the handler's list does not carry**, and the one it catches -- the KMS denial -- is caught by accident of not being modeled.

**Had this packet been built on the stub alone, it would have signed an IAM grant to fix an exception-mapping defect.**

---

## 4. TWO CORRECTIONS THIS SEAT OWES ON ITS OWN PRIOR WORK

1. **`kms:Decrypt` is ALLOWED for this role, not denied.** The rtf-12 record's remedy notes carried `implicitDeny` for `kms:Decrypt`. **That was the instrument, not the world:** the statement is conditioned on `kms:ViaService`, and `simulate-principal-policy` with no `--context-entries` returns `implicitDeny` byte-identically to a real deny (the documented false-deny mode 2). With the context supplied: **allowed**, positive control allowed, negative control implicitDeny. **KMS is not part of this defect, and any remedy touching the KMS grant would be widening for nothing.**
2. **The writer census matched its own source.** The first exercise counted **4** sites; the 4th was `battery_ib_rtf_14.py` itself, because the filter tested `"infra/aws/lambda/" in ln` and this file carries that fragment as a string literal. The published count would have been wrong in both halves (4, and "all via the declared families"). Fixed @`07d682522c` by keying on the **path field**; the graded run is the one after that commit, and the true count is **3**.

---

## 5. R71-AC2: JUDGMENT, recorded for `3.0.0_SA_CVO`, not self-graded

1. **The class of "the handler maps NoSuchKey and ClientError but the swallowed denial is neither."** It is a **Rule 24(i) forward-list defect**: the set of "errors that mean refused" is written as a list of two names its author had in mind, rather than as a subtraction from what the call can raise -- and it omits the single most likely production error on a least-privilege role. **The remedy is not "add `AccessDenied` to the tuple"**, which is the same forward list one name longer; it is to decide on the error **CODE** (`exc.response["Error"]["Code"]`, present on every `ClientError` subclass) or on `isinstance(exc, botocore.exceptions.ClientError)`, and to let genuinely unexpected classes propagate. **What the boundary must carry:** a role-plane failure must arrive as a NAMED refusal with its action and resource, which today is impossible because the recorder's sink is `None` (S91) -- so the mapping fix and the sink fix are **two** remedies, and neither moves the other.
2. **Was the receipt key's prefix ever inside the policy's declared reach?** **No -- they were written from different assumptions, and the evidence is that they never overlapped.** The policy is derived from `core/layout.json`'s `generations` family; the reader's template is a **free-typed string literal** in `entry.py:63-64` with an env override that Terraform never sets. There is no vintage at which `investor-reporting/export/` was a declared family: it appears in neither `layout.json` nor `_keys.PREFIX_FAMILIES`, and the route's own writer (`export/handler.py:126-130`) uses `s3_evidence_key` while its reader does not. **The divergence is that the READER bypassed the key builder the WRITER uses.**
3. **What an IAM grant's acceptance instrument must do.** `simulate-principal-policy` **false-ALLOWs on conditions it cannot evaluate and false-DENIES on conditions it evaluates without context** -- this seat hit the second half of that today (s.4.1). So it may never be the only evidence: an acceptance instrument must **exercise the real call as the real principal** (the live invoke pair here, which needs no assumable role), must run its **positive control as a separate invocation** (mode 1 disarms an in-call control), and must **name the class and code it actually received** -- which on this estate requires the boundary's sink to exist. **Today, for this route, a grant could be accepted only by the invoke pair, and the pair can report the served code but not the class.**

---

## 6. WHAT THE NEXT STEP NEEDS

1. **The two halves** read the packet at blob `a50a7d0e5b38d7b7cbce3ddedffac146c6790d32` and sign **the non-act**, or refuse it and say branch 1 should be signed instead -- in which case the seat re-cuts with the ARN, a new plan and a new digest (**a re-signature, not an amendment**).
2. **Rows `S105` (the address) and `S106` (the mapping)** are filed `ARMED`, `disarm_owner: 1.0.0_SA_CTO`, both with measurable disarm conditions. **Both remedies are source changes this order bars in terms.**
3. **S106 names a census it did not run:** whether other handlers in this estate use the same class-NAME test. It is named in the row so it has a carrier.
4. **Nothing on the served plane changes from this pass.** The route still answers UNEXPECTED, and the packet says so rather than implying a cure.
