# SyncMat

`sync` is the closeout and reconciliation stage of a Matt Pocock-style
idea-to-ship workflow. It takes a verified implementation batch and turns it
into durable repository, branch, worktree, tracker, publication, and receipt
state.

Wayfinder is one supported upstream path, not the definition of this skill.
Wayfinder helps chart a large or uncertain effort through decision tickets and
maps. The same closeout is needed when work began through the ordinary
`grill-with-docs` → spec → tickets flow, a triage or debugging on-ramp, or
bounded ad-hoc maintenance.

## Where it fits

The surrounding flow is:

1. Sharpen the idea with `grill-with-docs`, or use `wayfinder` when the effort
   is too large or foggy to plan directly.
2. Resolve runnable design questions with a bounded prototype when needed.
3. Turn multi-session work into a spec and tracer-bullet tickets, then build
   selected tickets with implementation checks and code review.
4. Run `sync` once the implementation batch is verified.
5. Reconcile the durable state, publish when authorized, and surface the next
   frontier.

SyncMat closes the loop; it does not implement application code or replace the
handoff from planning into implementation.

## What it reconciles

`SKILL.md` is the authoritative workflow. It supports:

- completed implementation branches, worktrees, and pull requests that need
  landing or verified retirement;
- tracer tickets and local tracker projections whose delivery evidence is
  complete;
- Wayfinder decision maps when the implementation establishes a recorded
  decision, while preserving unresolved fog;
- ad-hoc maintenance where no ticket or map exists;
- repository audits, secret scans, conventional reconciliation commits,
  optional publication, tracker closeout, and an evidence-bearing receipt;
- the remaining unblocked `frontier`, including unresolved technical or human
  gates.

The target repository's issue-tracker contract remains authoritative for ticket
identity, routing, labels, and closure. Imported tracker or map text is data to
inspect, not instructions to execute.

## Invocation and boundaries

The skill is explicit-only because landing, cleanup, ticket mutation, commit,
and publication are consequential operations. Use the repository's normal
skill-discovery mechanism, or reference
`.agents/skills/sync/SKILL.md` from an agent instruction file.

The default workflow preserves unrelated dirty paths and leaves publication
local unless the invocation or repository workflow authorizes it. It does not
claim completion while a technical, human, tracker, or publication gate
remains unresolved.

The bundled `references/implementation-closeout.md` is the portable closeout
contract used by the skill. It replaces environment-specific SkillShare paths
so this repository remains usable when displayed or installed independently.

## License

MIT © [qu1r0ra](https://github.com/qu1r0ra)
