# sync

An end-of-task reconciliation skill for coding agents. It synchronizes
repository state with the applicable issue tracker and decision maps, lands
completed implementations, retires verified temporary Git state, publishes
when authorized, and emits an evidence-bearing receipt.

## Scope

`SKILL.md` is the authoritative workflow. It supports:

- discovery of the nearest Git root, tracker, branch, and worktree;
- verification before tracker or map mutation;
- reconciliation of Wayfinder maps, tracer tickets, or ad-hoc maintenance;
- safe landing and retirement of completed implementation work;
- secret scanning, repository audits, commit, optional publication, and
  tracker closeout;
- a final receipt containing verification, publication, cleanup, and frontier
  state.

The bundled `references/implementation-closeout.md` is the portable closeout
contract used by the skill. It replaces environment-specific SkillShare paths
so this repository remains usable when displayed or installed independently.

## Invocation

The skill is explicit-only because landing, cleanup, ticket mutation, commit,
and publication are consequential operations. Use the repository's normal
skill-discovery mechanism, or reference `.agents/skills/sync/SKILL.md` from an
agent instruction file.

The default workflow preserves unrelated dirty paths and leaves publication
local unless the invocation or repository workflow authorizes it. It never
claims completion when a technical, human, tracker, or publication gate
remains unresolved.

## Related workflow

This skill is designed to close out work produced by an implementation
workflow. It does not implement application code or replace a handoff. The
target repository's own issue-tracker contract remains authoritative for
ticket identity, routing, and closure.

## License

MIT © [qu1r0ra](https://github.com/qu1r0ra)
