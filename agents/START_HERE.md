# WACMO AI-Assisted Development Guide

This guide helps a volunteer use an AI coding assistant
to maintain the WACMO website.

You do not need to understand the entire application before
asking an AI agent to investigate a specific task.

## Start With the Correct Repository

The WACMO checkout is `/home/alex/wacmo` on OrbitDesktop.

It is completely separate from Projekt Orbit.

Before starting, check:

    cd /home/alex/wacmo
    git status --short
    git --no-pager log -5 --oneline

Share the results with the AI assistant.

Do not share private credentials or member information.

## Suggested First Prompt

Copy the following paragraph into your coding assistant
and replace the bracketed task description.

> We are maintaining the WACMO website on FreeBSD in
> /home/alex/wacmo, separately from Projekt Orbit.
> Read README.md, ARCHITECTURE.md, AGENTS.md, and
> docs/PROJECT_STATUS.md before making changes.
> The live source code and tests are authoritative.
> My task is: [describe the requested change].
> First inspect the relevant code and existing tests.
> Preserve original historical content and do not publish
> unreviewed competition courses.
> Provide guarded, FreeBSD-compatible commands with unique
> here-document terminators. Do not use shell exit commands.
> Test focused changes, run the full verbose test suite,
> inspect Git diffs, and review before committing.
> Keep deployment separate from development.

## Useful Follow-Up Requests

Ask the AI assistant to:

- Inspect the existing implementation without changing it.
- Explain the smallest safe modification.
- Add regression tests for the requested feature.
- Review the Git diff before committing.
- Explain completed work in plain language for the board.
- Update the project status document at session end.

## Finishing a Session

Verify tests, review changes, and record:

- What was completed.
- What was tested.
- Which commit contains the changes.
- What remains unfinished.
- Any decisions or uncertainties for future maintainers.

The living record is `docs/PROJECT_STATUS.md`.

Do not claim production deployment or administration tools
exist until they have actually been implemented and verified.
