# Reversible deployment checklist

1. Verify the actual target, active release, web SAPI, document root/upstream and process owner. Read effective configuration, not only a conventional filename. Preserve dirty workspaces and record source hashes.
2. Back up data, uploads and configuration securely. Test restoration in isolation. Confirm rollback restores code/configuration without replacing newly written production data.
3. Prepare prerequisites, dependencies and release-specific compiled caches before activation. Verify runtime `env()` use before configuration caching. Avoid broad cache clears and preserve application keys and operational namespaces.
4. Use the existing deployment mechanism. If shadow workers are supported, keep one scheduler/queue owner and use an explicit memory budget. For shared hosting, verify what activation and OPcache invalidation are actually supported. Do not improvise a server migration. Announce a necessary maintenance window before using it.
5. Validate the effective route to the candidate before retiring the previous process. Drain requests, verify session continuity, warm critical pages and inspect error rates and financial parity.
6. Observe each stage for its agreed duration before proceeding. Monitor final health and performance for the agreed follow-up period. A running monitor is not a completed review; recording samples alone is not active alerting or automatic rollback.
7. Roll back for changed finances/authorization/session behavior, repeated new errors, or a sustained agreed regression. Restore code/configuration, keep current records and retain incident evidence.

An installed runtime package is not evidence that it serves web traffic. Check the web SAPI and effective application entry point. Invoke the exact verified PHP binary in commands: the shell default can select another major version. Reproduce the database engine as well as its version when restoring backups; do not rewrite a financial backup merely to import it into a different engine.

If existing scheduler evidence is stale, inspect ownership and queued work before restarting anything. A performance release must not trigger a backlog of messages or provider synchronization as a side effect.
