# Laravel Performance Safely

A practical agent skill for making Laravel applications faster while preserving financial results, authorization, and existing user flows.

It helps you prove where time goes, make a narrow change, compare equivalent runs, and prepare a reversible release. It does not deploy code or change production automatically.

## Install version 1.0.1

Clone this public repository at the release tag into a new skill directory:

```sh
git clone --branch v1.0.1 --depth 1 https://github.com/yasircs4/laravel-performance-safely.git "$HOME/.codex/skills/laravel-performance-safely"
```

For agents using the shared registry, use `$HOME/.agents/skills/laravel-performance-safely` as the destination instead. If either directory exists, review it before upgrading. Do not overwrite local changes. Restart or reload the agent's skill catalog, then invoke:

```text
Use $laravel-performance-safely to profile the slow pages, preserve financial and permission behavior, and verify a reversible improvement.
```

Start with [SKILL.md](SKILL.md). The skill is a workflow, not a promise of a particular percentage improvement.

## What is included

- A diagnostic workflow for settings amplification, repeated queries, runtime differences, and financial freshness.
- A dependency-free Python comparison tool that rejects changed results, mismatched contexts, failed requests, and invalid samples.
- A standalone PHP memoization contract and a synthetic example using actual Laravel container, database, and cache components.
- Lifecycle, financial parity, privacy, and deployment verification guidance.

## Run the checks

Requirements: Python 3.10+, PHP 8.2+, and PDO SQLite for the Laravel example. The generic helpers do not require a running website or access to a client project.

```sh
python3 -m unittest discover -s tests -v
php examples/request-memo.php
```

To reproduce the Laravel example, install its dependencies in a separate scratch directory. Never modify a production application's dependencies just to run this example.

```sh
mkdir /tmp/laravel-performance-example
cd /tmp/laravel-performance-example
composer require 'illuminate/container:^12.0' 'illuminate/cache:^12.0' 'illuminate/database:^12.0'
```

Back in this repository:

```sh
php examples/laravel-benchmark.php /tmp/laravel-performance-example/vendor/autoload.php /tmp/laravel-performance-results
python3 scripts/compare.py /tmp/laravel-performance-results/baseline.json /tmp/laravel-performance-results/candidate.json
```

Choose new output directories for subsequent runs. The example performs 2,000 reads of one synthetic currency setting per sample. Both variants use a warm database cache. Request-scoped reuse reduces cache-table reads from 2,000 to one while preserving all 2,000 returned values. Timing depends on your machine. This is a deliberately amplified example, not a production speed claim.

## Measure your application

Use the [measurement format](references/measurement.md). Record the dataset, clock, exact PHP executable and settings, database engine/version, role, cache state, concurrency, and measurement type. Compare server processing separately from browser navigation and network latency.

Canonical result hashes must cover authoritative report rows, totals, ordering, and export data. Exclude only documented nondeterministic fields. Do not remove a financial difference to make a hash pass. A matching hash is evidence for the measured cases, not proof that every possible workflow is correct.

The comparator reports median processing-time reduction as `(baseline - candidate) / baseline × 100`. A negative number means a regression. It reports regressions rather than silently hiding them; apply your own release threshold after correctness checks.

## Compatibility and limits

Validated with Laravel 12.64 components, PHP 8.4 and 8.5, and Python 3. The synthetic benchmark uses SQLite. A private application workflow additionally checked a MariaDB restore and report parity; no private data or application code is distributed here.

The workflow also discusses Octane and queue lifecycles. Scoped bindings alone do not fix services that capture a scoped object in a long-lived singleton. The example does not exercise an actual Octane server, payment gateway, or queue daemon. Verify those in your own application and installed framework version.

Do not copy example memoization around encrypted settings without preserving decoding, defaults, null handling, invalidation, and exception behavior. Do not turn currently live financial summaries into delayed background caches without an explicit product decision. Do not infer an application's web runtime from installed packages or the shell's default `php` command.

## Privacy and releases

Only generic, selected files belong in this repository. Keep application source, database dumps, configuration, client names, domains, records, logs, and production screenshots private. Review filenames, metadata, Git history, and the exact publication tree in addition to secret scanning.

Changes are versioned in [CHANGELOG.md](CHANGELOG.md). Contributions should include a reproducible synthetic case and the relevant correctness checks. MIT licensed. Author: [Yasir Najeep](https://yasirnajeep.com/).
