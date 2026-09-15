# sync-matt

`sync` is the closeout skill for the Matt Pocock idea-to-ship workflow. It runs
after an implementation batch has been built and reviewed, and reconciles the
result across the repository, Git state, issue tracker, decision records,
publication state, and completion evidence.

## Workflow position

The workflow moves through these stages:

1. Sharpen an idea with `grill-with-docs`.
2. Use `prototype` when a runnable experiment is needed to settle a design
   question.
3. For multi-session work, produce a spec and tracer-bullet tickets with
   blocking edges. For smaller work, proceed directly to implementation.
4. Build the selected ticket set with `implement`, which drives TDD and then
   performs Standards and Spec review with `code-review`.
5. Run `sync` once the implementation batch is verified.

The `wayfinder` on-ramp supplies decision tickets for large, uncertain efforts.
Those decisions can be reconciled during closeout alongside implementation
and tracker state.

## Closeout sequence

`SKILL.md` is the authoritative procedure. A run:

1. Discovers the nearest Git root, supervising checkout, branches, worktrees,
   remotes, tracker, and delivery mode.
2. Verifies the delivered implementation and distinguishes passing checks,
   unrelated baseline failures, and unresolved implementation failures.
3. Reconciles decision records, tracer tickets, local tracker projections, or
   ad-hoc maintenance state using direct delivery evidence.
4. Lands completed work and retires the exact verified worktree and branch when
   the delivery mode permits it.
5. Scans and audits intentional reconciliation changes before staging.
6. Commits and publishes the reconciliation state according to the selected
   publication policy.
7. Updates and verifies affected tickets without implicitly closing unrelated
   work.
8. Emits a receipt and the next unblocked `frontier`.

## Completion record

The receipt records the final branch or pull-request result, verification
commands, review evidence, publication and retry outcome, ticket mutations,
retired Git state, remaining technical or human gates, and the next frontier.
A merge alone is not acceptance, and an unresolved gate remains visible in the
closeout state.

## Invocation

The skill is explicit-only because it can land code, retire Git state, mutate
tickets, commit, and publish. Invoke it through the repository's skill
mechanism or reference `.agents/skills/sync/SKILL.md` from agent instructions.

The command accepts an optional ticket or effort path and `--no-push`:

```text
sync [<ticket-or-effort-path>] [--no-push]
```

The default workflow preserves unrelated dirty paths. The target repository's
issue-tracker contract remains authoritative for ticket identity, routing,
labels, and closure.

## Repository files

- [`SKILL.md`](SKILL.md): the executable workflow.
- [`references/implementation-closeout.md`](references/implementation-closeout.md):
  the shared branch, worktree, publication, and retirement contract.

## License

MIT © [qu1r0ra](https://github.com/qu1r0ra)
