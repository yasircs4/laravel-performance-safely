---
name: laravel-performance-safely
description: Diagnose and reduce repeated Laravel and Filament request work using comparable benchmarks, scoped reuse, query analysis, financial parity checks, and reversible deployments. Use for measured application slowness, not an automatic framework upgrade or server resize.
metadata:
  version: "1.0.0"
---

# Laravel performance safely

Make the requested flow faster without changing its results, authorization, or operational ownership. Diagnose the application actually serving traffic, not just its configured default server.

## 1. Establish comparable evidence

Read the active application's deployment entrypoint, runtime, database/cache/session drivers and scheduler/queue ownership. Verify the web SAPI and effective upstream: an installed Octane dependency does not prove Octane serves traffic. Never select a production target from copied application code.

Choose the user's affected pages and one authoritative calculation. Record warm/cold server processing separately from browser navigation and lazy-widget completion. Keep fixture, clock, role, filters, runtime, cache state and concurrency equivalent. Count queries without retaining bindings or sensitive URLs. A database-backed cache can turn repeated cache hits into repeated SQL.

Use `scripts/compare.py` only for its documented JSON contract in `references/measurement.md`. Treat reduced processing time as a measured result for that workload, not a site-wide speed guarantee.

## 2. Change the narrow source of repeated work

Start with request/job-scoped reuse for immutable reads. Preserve default identity, nulls, encrypted-value decoding and exceptions. Invalidate writes, renames, deletes and explicit cache invalidation. Test consecutive operations in the actual long-running worker before claiming isolation. See `references/lifecycle.md` and the executable synthetic example.

For repeated calculations, first reuse inputs inside a bounded calculation. Preserve relationship scopes, per-row clamping and rounding, deleted-record behavior, ordering and permission filters when batching queries or introducing SQL aggregates. Shared caches must never expose another role's results.

Do not silently change financial freshness. A dashboard with live totals is not equivalent to a five-minute snapshot. Do not introduce cache-failure fallbacks that convert financial settings to defaults or failed checks to healthy/zero values. Fail explicitly or perform the authoritative read according to the existing contract.

## 3. Prove correctness and deployment safety

Run complete result/export comparisons on a fixed isolated dataset, then the nearest authorization, payment-idempotency, notification and settings tests. Disable external deliveries and provider operations in the test environment. Use real rendered screenshots for private UI proof; use synthetic fixtures for public material.

Follow `references/deployment.md` for an explicit manifest, recovery proof, effective-config validation, staged observation and code-only rollback. Do not clear shared caches, start a second scheduler, alter namespaces or migrate databases as incidental optimization work.

## 4. Keep reusable evidence publishable

Keep private evidence in the application workspace. Public artifacts must be independently authored generic tools and synthetic examples, without client histories, identifiers, credentials, logs, runtime paths or screenshots. Review the actual release archive and Git history in addition to secret scanning. Public submission requires the user's applicable authorization; this skill does not grant it.

Document failed hypotheses and precise limitations. Upgrade this skill only when a verified finding changes its decisions or tools, then rerun its behavioral checks and privacy review.
