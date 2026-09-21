# Measurement contract

Run `python3 scripts/compare.py baseline.json candidate.json`.

Each file contains `context` with identical `dataset`, `clock`, `runtime`, `database`, `role`, `cache_state`, `concurrency`, and `measurement` strings, plus `samples`. Each sample has `case`, positive finite `duration_ms`, nonnegative integer `queries`, integer `status`, and `result_hash` (SHA-256 of the canonical authoritative result). Do not hash HTML with random CSRF values. Do not omit fields or substitute made-up hashes. Collect browser observations separately when canonical result proof is provided by a calculation replay.

Each case needs at least three measured samples, after a separately recorded warm-up. Compare case sets, successful status, stable result hashes within each run, and identical hashes across runs before calculating reductions. Percentage reduction is `(baseline median - candidate median) / baseline median * 100`. Report regressions honestly. Runtime parity is mandatory: changing CLI OPcache only for one side invalidates the comparison.

Use fixed synthetic fixtures for public examples. Private financial replay should include refunds, reversals, partial allocation, deletion scopes, discounts/write-offs, empty data and concurrent writes. Exact monetary results are a release gate; byte-identical exports may require holding timestamps and IDs fixed. Do not remove meaningful differences just to make a hash match.

Optional gates:

```sh
python3 scripts/compare.py before.json after.json --max-regression 20 --min-reduction 50 --target-case slow-dashboard
```

Exit 0 means the comparison and any requested thresholds passed. Exit 2 rejects invalid or incomparable evidence. Exit 3 means correct, comparable results failed a requested performance threshold. Without thresholds, regressions are reported without failing the command. A minimum applies to all cases unless `--target-case` selects specific ones. Do not apply a target intended for a slow page to unrelated unchanged paths.

The `status` field records success as 200 for HTTP samples. A CLI harness may use the same success marker after its assertions pass; label the context's `measurement` as CLI processing so this cannot be mistaken for an HTTP measurement.

A preloaded aggregate does not help when display accessors ignore it and query the relationships again. Compare the rendered path to its existing authoritative accessor, including refunds, reversals, partial payments, overpayments, write-offs, soft deletion, and restricted roles. Preserve whether clamping occurs per payment, per pledge, or after a total; these are not interchangeable formulas.
