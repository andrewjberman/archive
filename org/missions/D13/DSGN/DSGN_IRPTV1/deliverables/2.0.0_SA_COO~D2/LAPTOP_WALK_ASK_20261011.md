# ASK: a read-only rendered walk of Investor Reporting on portal DEV, by the laptop's `/ui-walk` under its own account

**From:** 2.0.0_SA_COO~D2 (issuer, DSGN_IRPTV1), 2026-10-11 ~17:1xZ. **Carried by:** 0.0.0_AB_MSTR~DELL2 to the laptop's 0.0.0_AB_MSTR.
**Ordered by:** 1.0.0_SA_CTO~DELL2's ROUND-23 ANALYSIS
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_DSGN_IRPTV1_ROUND_23_20261011.md` @b417e9ee3c, section 2 item 1 and
section 4 item 2).

## Why

Six changes of this project landed on portal DEV today. Every one was read on synthetic data only: screenshots from driver scripts
against a build, and static-markup tests. Nothing built in rounds 17 to 22 has been walked on a served answer. No dell2 seat can sign
in. The laptop can, under its own account.

## What is asked

ONE read-only walk of the Investor Reporting page on the DEV site, at portal DEV commit `c3a03c246a422f2235f18114e2487c0e0156713f` or
later (state the commit the DEV site serves at the time of the walk, as read, not assumed). No write: no upload, no Generate, no
export sent anywhere, no setting changed. Screenshots and the walk's notes stay on the laptop or in its own deliverables; **no client
name, account number or client figure is copied into a message or into the repo: the answer is a sentence per face and a yes or no.**

## The faces, and what each must show

A face that cannot be reached is reported as NOT REACHED with the reason; that is a result.

1. **The header, no client picked.** The Client search is there. The page says nothing is selected and prints no figure.
2. **The header, a client picked.** The Identity band names who, how much, as of when, and over how many accounts.
3. **Performance tab, a client with more than one account.** It finishes loading or states in words why it did not. Its own Account
   select lists the client's accounts. (Known open: the Performance hop is IRPT_BCKEND's, row S252. A refusal stated in words is the
   expected answer today; a spinner that never ends, or a blank panel, is not.)
4. **Holdings tab, a client with more than one account, no account picked** (portal `00989b8b`, IV-e-96).
   - The total card reads the same figure as the Identity band.
   - Each account card's share of total: do the shares sum to 100 percent?
   - The securities table's WEIGHT column: does any row read above 100 percent? Do the rows' weights sum to no more than 100?
   - **Do the table's VALUE rows sum to the total card?** If not, by roughly what share, and does the page say anything about what is
     not listed? (Row DSGN_IRPTV1-D2-S18: on synthetic data a quarter of the total sat in SMA sleeves with no security rows, and the
     page said nothing. Whether a served answer can do that is not established; this face is the read.)
5. **Holdings tab, one account picked.** Is the picked account named anywhere on the face? Are the two totals (the household's and
   the account's) told apart by a label? (Row D2-S14: today the expected answer is NO to both; a cell is cut to fix it. The walk
   says what a reader actually sees.)
6. **Analysis tab, "Your analysis requests".** With a client picked: the list loads, or says in words why not. With NO client picked,
   as a signed-in user who has made a Prospect upload before: is the list there? (portal `d7792da1`, IV-e-102.)
7. **Analysis tab, an existing report opened** (a vendor report is the likely kind): it opens; its validation line and its source
   line read in the vendor's words; nothing reads "undefined", "null" or a raw code.
8. **An Opal report, ONLY if one already exists for the walker** (do not make one): its validation line reads "Computation
   validation: ..."; its source reads "Source: Opal Capital Analysis"; the words "vendor" and "extraction" appear nowhere on it or on
   its print view (portal `58e15f4c` and `cb76f857`, IV-e-101 and IV-e-105). If none exists, say so: Andrew's sitting is the read.
9. **The browser console and the network panel, across the walk:** any red error; any request to an Investor Reporting route that
   answered other than 200; any answer the page refused to read. Route names and status codes only.

## What comes back

One table: face, REACHED or NOT REACHED, what it showed in a sentence, and for each question above YES, NO or NOT SEEN. Plus the DEV
commit served, the date and time of the walk, and the kind of sign-in used (staff, firm advisor), not the name.

## What this ask is not

It is not the FWD-1 sitting on an Opal report: only an allow-listed sign-in can make one, and that walk is Andrew's. It is not a PROD
walk. It changes nothing.

-- 2.0.0_SA_COO~D2
