# Implementation closeout

This is the shared closeout procedure used by `qu1r0ra-implement` and the
standalone `sync` skill. It is the source of truth for landing a completed
implementation and retiring its temporary Git state.

## Entry conditions

Identify the nearest Git root, the supervising checkout, the integration
branch (normally `main`), the implementation branch/worktree, the delivery
mode, and the affected ticket before mutating anything. Read the repository's
implementation contract and issue-tracker instructions.

The implementation worktree must be clean, registered, and on the exact issue
branch. The implementation must have a committed receipt with scoped checks,
full-suite evidence or an explicit exception, review-round/pair count,
repair/re-review history, and remaining gates.

Completion: all identities resolve to the intended repository, ticket, branch,
worktree, and delivery mode.

## Preflight

1. Inspect the supervising checkout's branch, status, worktrees, remotes, and
   implementation diff.
2. Preserve unrelated changes in the supervising checkout. Compare changed
   paths and the implementation diff; proceed only when the dirty paths are
   disjoint from the implementation landing. Stop before merge when they
   overlap. Never stash, reset, or overwrite user changes as a shortcut.
3. Verify the implementation worktree is clean and its branch tip is the
   intended committed implementation.
4. Preview ancestry and merge safety. A fast-forward is merely the case where
   the supervising branch can move directly to the feature tip; the closeout
   still uses a no-fast-forward merge for local-only implementations so the
   ticket receives a durable merge boundary.

Completion: the merge or pull-request operation is safe to attempt without
overwriting unrelated work.

## Local-only landing

1. From the supervising checkout, merge the exact implementation branch with a
   no-fast-forward merge commit.
2. If a clean-history merge conflict occurs, use the repository's
   merge-conflict workflow, preserve both accepted scopes, and rerun the
   relevant checks. Stop when resolution depends on an unrecorded user choice.
3. Verify the implementation commit is an ancestor of the supervising branch
   and that the supervising checkout is in the expected state.
4. If a remote exists and publication is authorized by this workflow, push the
   supervising branch. Retry once from the same verified state if the push
   fails. A repository with no remote remains local-only.

Completion: the supervising branch contains the implementation through a
verified merge commit, and publication is either verified or explicitly
recorded as unavailable.

## Remote-backed landing

1. Identify the implementation pull request and publish its feature branch,
   retrying one failed push from the same verified state.
2. Inspect required checks, required approvals, branch protection, and the
   current pull-request state. Wait for automated checks when they are pending.
3. Merge the pull request when all required automated gates pass and no human
   approval or live authorization is required. Use the repository/platform
   merge policy; do not bypass branch protection or invent an administrative
   override.
4. Verify that the pull request is actually merged and record its merge SHA.

Completion: the platform reports the pull request merged, or a named human or
technical gate remains and the feature state is preserved.

## Retire temporary Git state

1. Remove only the exact clean registered implementation worktree after the
   merge or verified pull-request merge.
2. Delete the corresponding local feature branch only after verifying its tip
   is merged. Delete the remote feature branch after a verified remote merge
   when the platform permits it.
3. Preserve the merge SHA and implementation receipt even after branch removal.
4. Use no force removal. If cleanup fails, preserve the state and report the
   exact path or branch that remains.

Completion: `git worktree list` no longer reports the retired path, and every
deleted branch is identified in the receipt.

## Update and close tickets

Update the primary implementation ticket with the implementation commits,
merge or pull-request SHA, verification evidence, review-round/pair count,
repair/re-review history, publication result, cleanup result, and remaining
gates. Update directly
affected blockers or dependents only when their state changed.

Close the ticket only when its acceptance evidence is complete and no human or
live gate remains. A merge or branch cleanup alone does not establish
acceptance. Keep the issue open with the appropriate human-review state when a
human gate remains. Verify state, labels, body/receipt, blockers, and target
routing through the live tracker after every mutation.

Completion: the ticket's live state accurately reflects landed, published,
accepted, and remaining-gate status.

## Failure states

- Unrelated dirty-path overlap: stop before merge and preserve the supervising
  checkout.
- Unclean or mismatched implementation worktree: stop before cleanup.
- Merge conflict requiring user intent: preserve the conflict and report it.
- Failed publication: retry once, then preserve the local result and leave the
  ticket open or in publication follow-up.
- Required human approval or live authorization: leave the pull request or
  issue open and record the gate.

The closeout is complete only when every requested mutation has a verified
result or a named failure state.
