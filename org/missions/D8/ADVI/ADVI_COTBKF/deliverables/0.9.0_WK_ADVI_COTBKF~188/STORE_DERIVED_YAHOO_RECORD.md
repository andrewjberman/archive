# CB-cu-1 store-derived Yahoo set against the served labels (round 99)

Read-only. Counts only; no account, name, cusip or value.

- Stores read fresh (refresh=True): cottonwood-silver-canonical-prices=2138920, cottonwood-gold-canonical-holdings=594318, rivalfunds-etfs-gold-security-market=209, etfs-bbg-testpull-ticker-history=132015, etfs-bbg-fund-daily=0, portal-canon-return-daily-values=0; row counts equal the round-97 regrade.log counts.
- Served account_day_value VersionId ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a (matches the round-98 apply); rows read 21102041.
- Sets: X=475103, S=2034027, A=471379, B=471195, A and B=471195, A minus B=184, B minus A=0. equal=False.
- Differences (A minus B, store says Yahoo, served says NOT_YAHOO): 184 points in 2 categories, all
  silver canonical linear_interpolation points. B minus A is zero.
- Not established: the cause (candidate: the as-traded basis dropping unbracketed silver linear_interpolation days), and
  whether store content changed since round 97. Full list in the JSON record.
