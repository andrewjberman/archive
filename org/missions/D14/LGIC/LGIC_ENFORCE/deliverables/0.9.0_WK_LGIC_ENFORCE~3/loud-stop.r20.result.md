# Loud stop, round 20 (EN-z-3)

## planted: `python lib/opal_naming.py census --names org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/stop_planted_r20.tsv`

```
CENSUS RAISE names LAMBDA org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/stop_planted_r20.tsv:1 zzqx-unreadable-thing-r20 -- R1.f: 'zzqx' is in no vocabulary; no registry row resolves it
CENSUS: STOPPED on the first RAISE after 0 judged (0 carded): names LAMBDA 'zzqx-unreadable-thing-r20'
```
exit code: 3

## readable: `python lib/opal_naming.py census --names org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/stop_readable_r20.tsv`

```
CENSUS OUT-OF-PATTERN names LAMBDA opal-irpt-cottonwood-reporting-gold -> irpt-cot-reporting-gold-lambda
CENSUS: COMPLETE 1 judged + 0 carded (live 0+0 of 0 nameable, repo 0+0 of 0)
```
exit code: 0
