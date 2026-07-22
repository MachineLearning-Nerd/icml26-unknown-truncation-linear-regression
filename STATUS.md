# Status — DsV89lJ58l

Current step: local publication gate.

Pinned upstream: `alexkouridakis/truncated-regression@a14732163158aff75113e3e1c50a90ecc27b4250`.

Initial source audit: the release contains a NumPy/SciPy implementation of a
positive-only interval learner followed by PSGD.  The documented default uses
10 outer replications, 4,500 PSGD iterations, and batch size 128; it is
CPU-only.  No claim is credited yet.

The unmodified source's ten-repetition (`R=10`) paper-scale configuration has
completed. Its mean errors are OLS `9.852682`, wrong-set PSGD `7.170760`,
true-set PSGD `0.522706`, and full algorithm `0.653189`; `source_r10.png` and
the full Trackio command/output transcript are retained. The independent
controls pass after deliberately strengthening an initially too-weak shifted
reference negative control: positive-only error `0.007899` vs disjoint-control
error `0.515311`; correct-set likelihood error `0.007669` vs wrong-set
`0.099420`.

Completed calibration: unmodified pinned source, full 4,500-step configuration,
one repetition.  Final parameter errors were OLS `9.813993`, wrong-set PSGD
`7.075335`, true-set PSGD `0.480995`, and full algorithm `0.572865`; plot
`outputs/source_r1.png`.  The run finished cleanly in roughly three minutes.
The paper-scale ten-repetition source protocol is the active next run.

Next: execute `repro/src/run_publication_gate.py`, perform the secret scan,
initialize/push the public GitHub repository, then atomically enqueue only if
the local gate remains affirmative. The first independent-control attempt is
retained in Trackio as a failed, too-weak negative control and is not evidence.
