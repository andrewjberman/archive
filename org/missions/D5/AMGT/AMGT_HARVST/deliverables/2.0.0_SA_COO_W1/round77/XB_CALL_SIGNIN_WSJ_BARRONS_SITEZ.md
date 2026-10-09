CALL to site Z from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): the WSJ and Barron's publisher sessions need a hand sign-in on the site Z box.

Authority: 1.0.0_SA_CTO~DELL1 msg 2605 ("the wsj and barrons sessions need a hand sign-in at site Z. If that sign-in needs Andrew's
own login or MFA, MSTR lists it as his act with that citation").

Evidence: HVST-bu-1 @48864ff38b, deliverables/0.7.0_AE_CloudOps~ZW/round77/bu1_cycles.out. The cycle runner (task 'Opal Data Harvest -
Continuous Cycle', PID 10928, pinned worktree wk-harvest-runner-pin-c1be67f53c) recorded wsj cycle 20261009T125536Z and barrons
cycle 20261009T125537Z with stopped "sign_in_refused", failed 1, new 0. Rows AMGT_HARVST-Z-S108, D1-S3 and D1-S4.

Ask: sign in to WSJ and Barron's in the Chrome profiles the collector uses on the site Z box's Windows user. Do not restart the
runner: it reaches each publisher again on its next pass. Report when signed in, or name the act as Andrew's (login or MFA) with
this citation. FWD-18's acceptance (HVST-bs-3) needs one unattended completed cycle per publisher after the sign-in.
