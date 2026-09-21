# Changelog

## 1.0.1

- Apply performance thresholds to unrounded medians so display rounding cannot hide a regression just above the configured limit. Added a reproducing command-line check.

## 1.0.0

- Initial Laravel-first workflow with measurement, lifecycle, financial parity, and safe release gates.
- Added a strict benchmark comparator and synthetic rejection tests.
- Added a Laravel database-cache amplification example with reproducible inputs.
- Incorporated verification of the actual web runtime, database restore compatibility, unused preloaded aggregates, and honest separation of page-rendering and report-calculation results.
