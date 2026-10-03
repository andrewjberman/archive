# Item 85 -- H-1..H-3 proof walk (1.0.0_SA_CTO batch 178, CTO_FOLD_IN_IRPT_THREE_BRIEFS_20261002.md section 3)

By `2.0.0_SA_COO~D`, 2026-10-02. Build: localhost:5174 on portal DEV 16c6690e, which carries item 85 at 97cd8dea. The
walker account was signed in (UI-walker, GET-only, 0 guard aborts) and disarmed after each walk, with a login after
disarm refused 401.

The step is the walker's `--map-tiles`. It counts the Securities map's drawn tile rects on the Holdings tab's default
view against the distinct map-eligible securities in the served snapshot that view shows. A security is map-eligible
when it is a SECURITY or CASH node of any basis, with a served `of_total` and a non-zero amount, counted once per
`security_id`, else once per node id. That is the page's own rule (`treemapLeavesFrom`). Client names and figures stay
in the local walk folders (gitignored), per the walker's contract.

| Client (by role) | Walk (local) | Tiles drawn | Of them small (no text) | Served distinct securities | Equal | Grouped word on page |
|---|---|---|---|---|---|---|
| 49 Financial's largest client by custody (7 accounts) | `tmp/ui-walk/20261002T192927Z` | 17 | 2 | 17 | yes | no |
| an 18-account Cottonwood client | `tmp/ui-walk/20261002T191055Z` | 467 | 447 | 467 | yes | no |

Independent read: `2.0.0_SA_COO~M` counted the 49 Financial client from the served publication (rev 3413e2b5a3bd) by
the same rule and got 17 (msg 104379: 75 SECURITY/TARGET, 5 CASH/TARGET and 1 CASH/OBSERVED nodes). All of this
client's securities are model TARGET rows, so the map draws a model's target mix where no position detail is served.
The Securities table states that in words.

Screenshots looked at (local):
- 49 Financial: shot 017 (`...-holdings-map-tiles.png`). 17 tiles in class colours. One hovered tile reads its name,
  Value, Weight and Asset Class. The legend shows Cash, Fixed Income, Equity and Structured.
- Cottonwood: shot 008 (`...-holdings-map-tiles.png`). 467 tiles: about 20 carry text on the left, and 447 small tiles fill
  the right half as thin coloured strips. A hovered small tile reads name, Value, Weight and Asset Class. No Other
  Securities tile, legend entry or footnote.

Observation, not a defect against H-1's text: at 467 securities the map is mostly strips too thin to read or to aim at
without hovering. H-1 asks for every security as its own tile, and that is what draws. Whether a large client's map
should read differently is a design call for Andrew, not this seat's.

Walk anomaly: the Cottonwood walk's browser closed at 19:21:30Z during the generic Holdings explore, after the map step
had finished. The second client named in that run was not reached. The 49 Financial client was then walked alone.
