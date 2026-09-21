# Scoped reuse without stale state

Register a memo with `$app->scoped(RequestMemo::class)`, and resolve it at the read boundary. Do not capture a scoped object inside a singleton or static property. Laravel resets scoped bindings at supported request/job lifecycle boundaries; verify the actual runtime and custom workers.

Test repeated key reads, different typed defaults, cached null, encrypted settings, exceptions followed by recovery, writes in the same request, key renames, deletes and explicit cache invalidation. The example uses strict identity without serializing arbitrary objects. It deliberately retains no exception result.

After a write, invalidate both the backing cache and the scoped memo. For multi-setting snapshots, clear their memo too. If bulk SQL writes bypass model events, wire invalidation at that actual write path. Cache event invalidation is useful only if those events are enabled in the deployed store.

For worker proof, send two operations through the same process. Change the backing setting between them and verify the second operation sees the new value. Repeat for queue jobs. Test database rollback/savepoint behavior if memoization is used inside transactions; failed writes must not leave a memo value representing an uncommitted state.

The standalone example is a contract exercise, not an installable replacement for an application's settings service. Preserve its existing decoding, fallback and authorization behavior when integrating.
