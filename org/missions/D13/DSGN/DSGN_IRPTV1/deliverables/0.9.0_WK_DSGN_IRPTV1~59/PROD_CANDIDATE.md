# The PROD candidate, in plain words

Written by 0.9.0_WK_DSGN_IRPTV1~59 for task order DSGN_IRPTV1.TO-IV-e-106. Nothing here has been pushed, to DEV or to PROD. The exact record is `PROD_CANDIDATE.json` beside this page.

## What it is

One portal commit, `9d3f43eff28a5d7ba5ceac0f0f524283d6ab5ad4`, on top of what DEV holds today. PROD today is `37aa1247ee4ba487e5610dc5b78d65ae28468a99`. Between the two there are 127 commits and 127 changed files. 60 of the commits are this project's. 67 belong to other projects, so your word on this push would cover their work too.

## What changes, page by page

**Pages a client or partner firm can open (38 files, and one build file pair):**
- Model Portfolios: the Global trend work (two extra moving-average bands), with a small change in the file that reads paired provenance. Not this project's.
- Advisor Intelligence: a new panel showing one billed quarter's fee. Not this project's.
- Investor Reporting's shared code: the part of the report code that the print view also uses. The print view opens on a pass the browser reads without checking, so I cannot show a client login is kept out of it. I have therefore classed that shared code as client-facing.
- The build files add one test-only tool, from this project's earlier work. They add nothing to a page that I measured.

**Pages only Opal staff can open (89 files, 66 of them tests):**
- Investor Reporting itself: only an administrator of Opal Capital whose user type is Dev can open it. You told me it is client-facing; the router does not show that for the page, so I classed the page's own files staff-only and recorded the difference as row DSGN_IRPTV1-D2-W59-S2. It changes nothing about whether you must approve, because the pages above are in the range.
- Ticket Center and Security Analysis: staff only, with changes from other projects.

## What this order added

The report sections reader used to drop the saved-report reference that the service may send with a report. It now keeps it when it is sent and leaves it out when it is not. No page shows it yet. A test holds both cases, and a deliberate break of the code made that test fail.

The two missing status reads, the Branded PDF link and the original-file link, are both in the candidate. PROD has neither. Nobody has called either against a live service.

## What was read only on synthetic data

The Opal report wording, the Opal document and its export, the Holdings change, and the history list after a prospect request were all checked on made-up data only. The rows D2-S16, D2-W58-S4 and D2-W57-S3 say so. The new saved-report reference was checked on made-up answers only.

## What is not in this

No push. No live call. The 67 commits from other projects were not read, run or photographed by this project.

## After it

Once this is on PROD, the history reader that IRPT_ANLREQ's release 5 needs is there, and release 5 can return.

Checks at the candidate: lint 0 errors, typecheck clean, Investor Reporting test run 1164 passed, 27 skipped, 0 failed (the base run was 1161, 27, 0).
