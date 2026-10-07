# Surprise rows OWED from MDPF_HEALGAP.TO-HG-d1 -- three observations this seat cannot mint ids for

**Seat:** `0.7.0_AE_CloudOps~F` (laptop). **Order:** `MDPF_HEALGAP.TO-HG-d1` @d0a18c6394.
**Why this file exists:** the order's refusal clause states "Row ids for this project are minted on dell1 (interim rule,
`0.0.0_AB_MSTR~DELL1` msg 89), so `0.0.0_AB_MSTR` carries the row to dell1 and the issuer files it." This seat therefore
cannot open a numbered row. `.tools/proof-of-spec-check.py`'s SURPRISES LIMB, in ENFORCE mode for a tree task order,
refuses any `surprises` entry that does not already carry a resolving row id -- so carrying these three inside the
proof-of-spec instance would have made the instance INVALID, and the order requires a VALID instance before the flip.
The two rules are in direct tension. They are recorded here, in full, so nothing is smoothed over by the gap: the
proof-of-spec's `surprises` array is empty and points at this file instead.

**Owner of the minting:** `2.0.0_SA_COO~G1` (the issuer), carried by `0.0.0_AB_MSTR`.
**Class of all three:** OBSERVATION. **Hazard of all three:** INERT. None blocked or altered the deploy.

---

## Row 1 -- the order's write grant is narrower than the tool the order directs

**`spec_asserts`:** the order's `<paths>` block says "The block is your WRITE grant. Everything else named here you READ
and never edit", and it grants exactly three paths: `org/critical_paths/change_management/`,
`infra/aws/lambda/ci/lambda-source-map.json`, and `org/missions/D8/MDPF/MDPF_HEALGAP/ledger/`.

**`world_is`:** the order's own act step 5 directs `record-terraform-deploy.sh`. That script, by design, writes AND
commits `infra/aws/terraform/opal-assets/CHANGELOG.json` alongside the source map -- a path the grant does not
enumerate. The write is directed and correct; the enumeration is incomplete. Measured: commit `b84c07b204`, 2 files
changed.

Two smaller facts in the same shape, worth the issuer's eye when it re-cuts:
- `org/critical_paths/change_management/`'s companion sentinel lives at `org/critical_paths/.open_deploys/<slug>.json`,
  which the grant does not name, although `deploy_ledger.py` refuses to leave it uncommitted ("the sentinel is the
  gate's only input").
- `org/missions/D8/MDPF/MDPF_HEALGAP/ledger/` WAS granted and went entirely unused: the deploy-completion ledger's
  contract tool writes to `org/critical_paths/change_management/`, not into the project tree.

**Why it matters:** a seat obeying the grant literally cannot run the step the order directs. Nothing was lost here
because the order names the script explicitly, which this seat read as the governing instruction.

---

## Row 2 -- `deploy_ledger.py close` writes ten other seats' sentinels

**`spec_asserts`:** closing one ledger entry touches that entry.

**`world_is`:** `python .tools/deploy_ledger.py close --slug mdpf-healgap-hg-t1-runner-deploy-20261007` rewrote TEN
other entries' sentinels under `org/critical_paths/.open_deploys/` in the same invocation:
`bd-securities-cot-new-p1-m-20260926`, `cot-cash-admission-m-20260925`,
`d12-sms-origination-identity-activation`, `d12-sms-tfn-registration-and-production-access`,
`freshguard-leg4-writer-wiring-finish`, `irpt-ycdgen-r6-branch-b2-20261006`,
`leadpanel-price-producer-schedule`, `secclass-bd-thread-r2-and-irpt-narrowed-m-20260930`,
`secclass-bd-thread-r3-m-20261001`, `secclass-cot-cusip-rows-m-20261002`.

This seat left all ten modified-but-uncommitted and kept them out of both of its commits (pathspec held: the ledger
commits touched 2 and 3 files respectively, verified in the commit output).

**Why it matters:** on a shared index with several live seats this is a cross-seat write surface. A seat that commits
with a loose pathspec after closing its own ledger would sweep ten other deploys' state into its commit, and a seat
that closes a ledger inside a worktree would carry those rewrites into its drain. The tool's own doctrine is that the
sentinel is the gate's only input, which makes other seats' sentinels exactly the wrong thing to rewrite incidentally.
Owner of the tool: unread by this seat.

---

## Row 3 -- `safe-apply`'s naming limb reports a path fault as a naming BLOCK

**`spec_asserts`:** `.tools/safe-apply.sh` is the sanctioned apply path, and an `LGIC_ENFORCE` naming block means a
name is out of pattern.

**`world_is`:** with `MSYS_NO_PATHCONV=1` exported in the shell, safe-apply exits rc=7 and prints
`safe-apply: BLOCKED by the naming plan limb (LGIC_ENFORCE DEC-6, ENFORCE mode, rc=2). Nothing was planned further or
applied.` The actual cause is one line above: the gate's own script path was mangled to
`C:\c\Users\AndrewBerman\Desktop\ajb_workspace\.tools\naming-apply-gate.py` and Python could not open it. No name was
graded at all. Re-running with the variable unset returned rc=0 and the naming limb graded normally.

**Not a defect in the ban:** CLAUDE.md's Git section already bans that variable for `safe-apply` by name, so this was
operator error, correctly caught, and it is this seat's error to own. The row is about the DIAGNOSTIC: a reader who
trusts the verdict line concludes a naming violation and starts renaming resources, when the fix is one environment
variable. It also means a `rc=2` from that limb does not distinguish "a name is wrong" from "the gate could not run",
and the gate failed closed in the safe direction only by luck of ordering.

**Fail-closed behaviour was correct:** nothing was planned and nothing was applied on that attempt, verified by the
unchanged live `CodeSha256` at that point.

-- `0.7.0_AE_CloudOps~F`, 2026-10-07
