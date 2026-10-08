## Reason for the convention (written by hand after reading the result above)

**Chosen: end of day (the default stays `FLOW_TIMING = "end"`).** On the 937 fully priced flow months, end of day MATCHes
242 and start of day 241, with the median |diff| of the DIFFs 6.31 against 6.67 points. The rule picks end on more MATCH;
the margin is one month, so the honest reading is that neither timing explains the flow-month DIFFs: moving the flow from
the end of the day to the start of the day does not close a 6-point median gap. The cause of the flow-month DIFFs is
elsewhere (the flow's size or sign, a flow the table treats as internal, or what Commonwealth's Month TWR itself does with
flows), not the timing.

Control: the 2,676 no-flow months grade identically under both (control_same=True), as the formulas coincide when the flow
is zero. The control covers months graded under BOTH timings. 624 months are graded under end only, 208 with a flow and 416
without; the start rule blanks a zero or negative base as ZERO_BASE (the order's rule), which includes the days after a
negative prior-day value, while the end rule computes them. Those 416 no-flow months are therefore not "identical", they
are blank under start; they are excluded from the comparison and listed in the table above, and filed as a surprise row.

**Tax withholding.** With ftax/stax as an outflow (the earlier flow table) the flow-month MATCH was 217 under end; with them
INTERNAL it was 241 over the same months (the first run, before the change), and 242 against 216 in the run above over this
run's flow months. The count is higher, so `commonwealth_flows.py` now carries ftax and stax as INTERNAL: 4,324 rows (4,212
ftax, 112 stax). Reason: the withholding is taken from the income or proceeds before the account books them, so it is not
client money crossing the boundary. The main table above is run with ftax/stax INTERNAL for both timings (242 end, 241 start), so the choice
of end holds with the change in.
