# WACMO Repository Instructions for Coding Agents

Read `README.md`, `ARCHITECTURE.md`, and
`docs/PROJECT_STATUS.md` before modifying the application.

The current repository and tests are authoritative.

## Environment

- Repository: `/home/alex/wacmo` on OrbitDesktop, FreeBSD.
- Work only in this WACMO repository.
- Never modify Projekt Orbit or OrbitWork as part of WACMO work.
- Prefer `.venv/bin/python`.
- Flask application factory: `wacmo:create_app`.
- Do not assume a database or webmaster editor already exists.

## Before Editing

Check Git status and inspect the relevant source and tests.

Preserve unrelated local changes.

Prefer small changes over broad rewrites.

Use FreeBSD-compatible, copy/paste-ready commands.

For multi-file edits, use guarded Python scripts that:

1. Validate source files and exact expected anchors.
2. Prepare all changes before writing.
3. Check syntax and important invariants.
4. Write only after all validations pass.
5. Print CHECK, VALIDATED, WROTE, and SUCCESS messages.

When writing a shell here-document, choose a unique
terminator that does not appear anywhere inside its content.

Never nest an identical here-document terminator.

Do not put shell exit commands into copy/paste batches.
Avoid `exit 1`, `set -e`, and `|| exit 1`.

Do not require downloadable patches or SCP transfers.

## Historical Content Rules

Original WACMO materials are historical evidence.

Do not silently alter originals or replace them with
unrelated content.

Maintain file provenance and checksums where available.

Do not infer event relationships from generic names alone.

A riding-area reference map is not necessarily a competition
course from that event.

Never automatically publish unreviewed maps, course clues,
upcoming competition courses, or private participant details.

Do not infer that a scheduled event actually occurred.

Photos and maps remain optional event attachments.

Respect original WACMO and third-party media rights.

## Verification

Run focused regression tests first.

Then run the complete suite:

    .venv/bin/python -m pytest -vv -rA --durations=10 --durations-min=0

Review changes:

    git diff --check
    git status --short
    git --no-pager diff

Before committing, stage intended files explicitly and
review the staged diff.

Do not deploy as a side effect of committing.

## Documentation Maintenance

Keep README.md understandable to board members.

Update ARCHITECTURE.md when implemented architecture changes.

Update docs/PROJECT_STATUS.md at the end of meaningful
development sessions.

Record completed changes, verified tests, outstanding work,
and relevant commit hashes.

Distinguish planned features from implemented and deployed
features.

When unsure about privacy, historical facts, or publication,
stop the proposed edit and report the uncertainty.
