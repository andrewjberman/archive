AMGT-rm-2 AC1 -- idiom-category exclusions, PanelHeader.tsx / PanelFooter.tsx

Census (portal/scripts/ui-class-census.mjs), after the weight/radius fix:
  src/components/PageHeaderVariants.tsx           idiom=0 size=0 weight=0 radius=0 shadow=0 total=0
  src/ui/components/panels/PanelFooter.tsx        idiom=4 size=0 weight=0 radius=0 shadow=0 total=4
  src/ui/components/panels/PanelHeader.tsx        idiom=4 size=1 weight=0 radius=0 shadow=0 total=5
  FILES 3 TOTAL 9

weight=0 / radius=0 / shadow=0 on all three files: CLEAN (this cell's target). idiom hits remain
(8 across the two panel-chrome files) -- each is a `text-white` / `text-white/NN` idiom on the
title strip, whose background is `bg-[hsl(var(--bg-header))]` (the dark band colour). Per
portal/DESIGN.md C5 ("The inversion rule -- carrying a light-on-dark idiom onto the light
ground"), a translucent-white ink idiom on a genuinely dark surface (the strip IS one of the
persistent dark surfaces, DESIGN.md C3's "band" role) is not a light-ground violation -- C5
governs carrying a DARK-mode idiom ONTO a LIGHT ground, and this strip is not a light ground.
Declared per the issuer's routing (task order s.1, WHAT YOU BUILD (2)): legal here, excluded
from the violating total under the clause "C5 inversion on a dark strip."

PanelHeader.tsx (idiom=4):
  :75  `text-sm font-bold text-white uppercase tracking-wide` (title, h3)         -- C5 inversion on a dark strip
  :83  `text-white/40 hover:text-white/70 ...` (help icon, two matches)          -- C5 inversion on a dark strip (x2)
  :89  `text-sm text-white/60` (subtitle)                                        -- C5 inversion on a dark strip

PanelFooter.tsx (idiom=4):
  :8   `- Subtle muted text (text-white/40)` -- JSDoc comment describing the pattern, not a class
       actually applied in code (the real classes below use /50 and /30); the census counts
       comments deliberately (script docstring: "a forbidden idiom in a comment is a false hit
       the reader can see"). Declared as a documentation-only hit, same clause if it were live.
  :104 `text-white/50 text-left flex-1 min-w-0` (leftContent/caption wrapper)     -- C5 inversion on a dark strip
  :110 `text-white/50` (formatted timestamp span)                                -- C5 inversion on a dark strip
  :111 `text-white/30 mx-2` (separator span)                                     -- C5 inversion on a dark strip

TOTAL after exclusions (categories governed by this cell -- weight, radius, shadow, idiom): 0.

OUT OF SCOPE, unchanged by this cell: PanelHeader.tsx `size=1` (`DataTimestamp`'s
`className="text-[10px]"`, :99) -- a C2/typography-size concern, not C1 (weight) or C11
(radius/shadow); pre-existing before this edit and after it (was already size=1 in the round-38
starting census, FILES 3 TOTAL 11). Confirmed live via ui-contract-check.mjs --scope main: sizes
reads FAIL [10] on `thesis` and `model` only (the two states whose fixtures set a `timestamp`),
matching the issuer's note 1 baseline exactly ("sizes [10] on thesis and model only").

RADIUS CENSUS BLIND SPOT (confirmed by re-running the RADIUS_NAMED pattern directly against the
pre-edit HEAD bytes, git show HEAD:<path> | node one-liner):
  RADIUS_NAMED = /rounded-(md|lg|xl|2xl|3xl)\b/g
  PanelHeader.tsx `rounded-t-lg` (pre-edit, :62)  -> named-pattern hits: 0
  PanelFooter.tsx `rounded-b-lg` (pre-edit, :93)  -> named-pattern hits: 0
The pattern requires "rounded-" immediately followed by one of md/lg/xl/2xl/3xl; "rounded-t-lg"
and "rounded-b-lg" insert a "t-"/"b-" side token first, so the census's own RADIUS_NAMED regex
does not match either form -- it read radius=0 on both files before this edit despite each
rendering an 8px (Tailwind `.rounded-lg`) corner. The census's RADIUS_ARBITRARY pattern
(`rounded-\[(\d+)px\]`) DOES see the post-edit `rounded-t-[4px]` / `rounded-b-[4px]` forms and
correctly reads them as legal (4 is in {2,3,4}).
