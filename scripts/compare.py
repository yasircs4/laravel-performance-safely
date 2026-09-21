#!/usr/bin/env python3
"""Compare equivalent benchmark runs and reject missing or changed results."""
import argparse
import json
import math
import statistics
from pathlib import Path

CONTEXT = ('dataset', 'clock', 'runtime', 'database', 'role', 'cache_state', 'concurrency', 'measurement')


def read_run(path):
    run = json.loads(Path(path).read_text())
    if not isinstance(run, dict) or not isinstance(run.get('samples'), list):
        raise ValueError('Run must be an object with a samples array')
    context = run.get('context', {})
    if not isinstance(context, dict):
        raise ValueError('Context must be an object')
    if any(not isinstance(context.get(k), str) or not context[k].strip() for k in CONTEXT):
        raise ValueError('Every context field must be a nonempty string')
    cases = {}
    for sample in run.get('samples', []):
        if not isinstance(sample, dict):
            raise ValueError('Each sample must be an object')
        case = sample.get('case')
        duration = sample.get('duration_ms')
        queries = sample.get('queries')
        digest = sample.get('result_hash')
        if not isinstance(case, str) or not case.strip():
            raise ValueError('Missing case')
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0:
            raise ValueError('Duration must be positive and finite')
        if type(queries) is not int or queries < 0:
            raise ValueError('Query count must be a nonnegative integer')
        if type(sample.get('status')) is not int or sample['status'] != 200:
            raise ValueError('Every sample must have a successful 200 status')
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('Missing canonical SHA-256 result')
        cases.setdefault(case, []).append(sample)
    if not cases or any(len(samples) < 3 for samples in cases.values()):
        raise ValueError('Each case needs at least three measured samples')
    return context, cases


def compare(before_path, after_path):
    before_context, before = read_run(before_path)
    after_context, after = read_run(after_path)
    if before_context != after_context:
        raise ValueError('Benchmark contexts differ')
    if before.keys() != after.keys():
        raise ValueError('Benchmark case sets differ')
    result = []
    for case in sorted(before):
        hashes = {s['result_hash'] for s in before[case] + after[case]}
        if len(hashes) != 1:
            raise ValueError('Authoritative result changed or is unstable: ' + case)
        old = statistics.median(s['duration_ms'] for s in before[case])
        new = statistics.median(s['duration_ms'] for s in after[case])
        result.append({'case': case, 'baseline_median_ms': old, 'candidate_median_ms': new,
                       'processing_reduction_percent': round((old-new)/old*100, 2),
                       'baseline_median_queries': statistics.median(s['queries'] for s in before[case]),
                       'candidate_median_queries': statistics.median(s['queries'] for s in after[case]),
                       'result_matches': True})
    return {'context': before_context, 'comparisons': result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline')
    parser.add_argument('candidate')
    parser.add_argument('--max-regression', type=float, help='Reject a processing regression above this percent')
    parser.add_argument('--min-reduction', type=float, help='Require this processing reduction on every selected target case')
    parser.add_argument('--target-case', action='append', default=[], help='Case for the minimum-reduction gate; repeat as needed, defaults to all')
    args = parser.parse_args()
    try:
        for threshold in (args.max_regression, args.min_reduction):
            if threshold is not None and (not math.isfinite(threshold) or threshold < 0):
                raise ValueError('Thresholds must be finite and nonnegative')
        result = compare(args.baseline, args.candidate)
        cases = {row['case'] for row in result['comparisons']}
        if set(args.target_case) - cases:
            raise ValueError('Target case missing from the benchmark')
        failures = []
        for row in result['comparisons']:
            reduction = (row['baseline_median_ms'] - row['candidate_median_ms']) / row['baseline_median_ms'] * 100
            if args.max_regression is not None and reduction < -args.max_regression:
                failures.append(row['case'] + ': regression exceeds threshold')
            if args.min_reduction is not None and (not args.target_case or row['case'] in args.target_case) and reduction < args.min_reduction:
                failures.append(row['case'] + ': reduction below threshold')
        result['threshold_failures'] = failures
        print(json.dumps(result, indent=2, allow_nan=False))
        if failures:
            return 3
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, 'Comparison rejected: ' + str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
