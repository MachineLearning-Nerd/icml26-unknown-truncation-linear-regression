# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_fc4f68476218", "created_at": "2026-07-22T11:49:18+00:00", "title": "Executive summary", "pinned": true, "pinned_at": "2026-07-22T11:49:18+00:00"}
-->
## Outcome

The CPU-only local gate passes all six anchored claim checks with explicit scope: theorem, assumption, smoothness, and asymptotic statements are verified by primary-source audit; Phase I/II numerical behavior is reproduced by a full unmodified author run and independent controls.

## Scope & cost

| | This reproduction | Full replication |
| --- | --- | --- |
| Scope | Released 10D synthetic protocol, R=10 | Paper theory plus all possible deployments |
| Hardware | Single CPU core, 15 GB host | Not specified by paper |
| Time | About 24 min source run + 12 s independent control | N/A |
| Cost | $0 local CPU | N/A |
| Outcome | Gate passed; full method 0.653 vs wrong set 7.171 / OLS 9.853 | Theorem statements source-audited, not re-proved |
