## 6. Infrastructure -- by `0.0.0_AB_MSTR~Z`, from its own record

Labels as in the report: [measured] read from git, the broker or a file at ~04:40Z 2026-10-18; [record] from my session record, not
re-measured; [inferred] a judgment. This section is a census of what I did, not of the box.

**6.1 Box passes** [measured]
- The box pass (take CLOUD into box/sitez, push box/sitez) runs once per laptop-integrator cycle and on demand. 282 of my 314
  commits since 2026-10-16 are box-sync merge commits (git log by author).
- box/sitez is 0 behind CLOUD and 5 ahead (ls-remote, 04:3xZ). [record] Every pass I ran in the last day finished (rc 0 after any
  skip-and-retry while another pass was running). Earlier holds were a peer's uncommitted crossbox file and an open peer merge;
  both cleared.

**6.2 Seats on this box** [measured: seat-liveness, read-only]
- 10 seats: 6 moving, 3 quiet, 1 flagged HUNG, 0 dead. No seat left the roster here (the laptop and dell1 each lost seats).
- The HUNG flag is `0.7.0_AE_CloudOps~MDPF1`. Measured not stuck: broker LIVE, its own status reads idle until the 2026-10-18
  14:00Z reread.
- `0.7.0_AE_CloudOps~MDPF1` was seated on 10-17 04:24Z on the CTO's word (rule 34, the one MDPF macro lane); crossbox DQ-t-70 and
  TO-DQ-t34 point at it. [record] On 10-16 the four old CloudOps lanes were consolidated to `~NFRA1` under rule 34.

**6.3 Crossbox orders delivered to site Z seats** [measured: committed records]
- Six receiving-side records are committed and on origin: a277, c3ae, cd36, e568, 7343 (all to `0.0.3_BG_BBGTerminal`, the
  rivalfunds orders) and bbde (to `0.7.0_AE_CloudOps~MDPF1`). Each was acked by the named seat.
- 7507 was addressed to a lane that is not seated here (`~ZQ`); it was superseded by bbde and never acked.
- Each order waited for its commit to reach CLOUD before delivery (PULL-FIRST), then went in the box pass that took CLOUD. I read
  the 7343 ack about an hour late and said so on the bus.

**6.4 Relays and cross-box windows for dell1** [measured: my bus sends]
- Host-owner and gold-owner windows: I carried dell1's notices to the CTO and its answers back for HVST C-9, C-10, cg-2, cg-3, cf-5
  and ch-5. For each never-widen pair I hashed the COO half myself; all matched.
- Gateway: carried the HOLD of 1753c741d9 while OG-ap-36 was in flight, then the swap that let dell1 deploy first. 1753c741d9 is
  now in sitez's lineage (landed by `~NFRA1`, drained by `2.0.0_SA_COO~O`), on origin/box/sitez and CLOUD.
- Scratch refs pushed for dell1 so it could cut on a live commit (no merge, no CLOUD change): rel-nfra-og-ap-31-live,
  rel-nfra-og-ap-34-live, rel-nfra-og-ap-36-live, rel-nfra-og-live-efcc8ae19f, rel-nfra-og-live-d077cef043. dell1 deleted the
  first two after checking them contained in CLOUD (04:41Z). Still on origin: ap-36-live (a superseded candidate, not in CLOUD;
  the commit also sits on a local branch here), and the two live-sha refs (not in CLOUD). I deleted none.
- Rivalfunds: relayed each result of the Terminal seat (ORDER 2 step 1 through ORDER 5) to dell1 as the seat's figures, and the
  CTO's ruling on what may travel (the per-fund table, not the replay json).
- Black Diamond fees silver (rows Z-S368/Z-S369): carried to the laptop MSTR, and the laptop CTO's ruling (record the gap, probe
  first) back to the site Z CTO and COO.

**6.5 Tools and fixes I committed** [measured: commits, all in HEAD]
- teams-watch.py never emits a blank preview (dfdfaf4f46; 19 tests; a quote-reply class added).
- Executor grant in the owned-paths registry (c45003275a, 7e67d37195; 28 self-test arms).
- Broker delivery torn-write fix in org/mcp/server.py (c5fff4d8f1). **Open:** a seat loads it only on restart.
- ms as an agentbus destination (a6aaf8b889, 3d04d8130b, 6de42e354e); python3 shim (a9147c39fb).
- 14 sweep commits carrying `0.0.3_BG_BBGTerminal`'s records, and the Bloomberg prompt-fence correction (66b1c7d3e9).
- On ms's request I started the `mson` worker in a PowerShell window (the window must stay open).

**6.6 Open on the infrastructure side** [measured]
- The client-data check's hashed account-id list is absent on this box (the check fails open on every box). Ruled: an HMAC list
  from a dell2 job; I place the file here when it exists.
- This box's AWS caller identity reads `user/Andrew_Berman`, unlike dell1 and dell2 (per-box agent users). The read waits on the
  laptop CTO.
- /unstick could not take focus on a seat's tab while another window held the foreground (reproduced 4 times); a person clicking
  the tab is the fix.
