# WACMO Project Status and Roadmap

Last updated: November 20, 2026.

**Status:** Modernized public website under development.

**Latest verified test baseline:** 98 passed.

**Development:** OrbitDesktop, FreeBSD, `/home/alex/wacmo`.

**Production target:** Bluehost Linux VPS, not yet deployed.

This is WACMO's living record of accomplished work,
outstanding features, decisions, and development sessions.

## Completed and Verified

- [x] Independent Python/Flask repository.
- [x] Responsive website and mobile navigation.
- [x] Preservation of original website HTML and branding.
- [x] Historical events calendar for available 2024–2026 data.
- [x] Dedicated historical event pages.
- [x] Original flyer archive and event associations.
- [x] Historical photo albums and event-linked galleries.
- [x] Enlarged photograph viewer and favicon.
- [x] Searchable archive of 26 published riding-area maps.
- [x] Original map PDFs, thumbnails, and enlarged previews.
- [x] Removal of the redundant historical Maps display.
- [x] Twenty reviewed event/map links involving six maps.
- [x] Event-to-map and map-to-event navigation.
- [x] Preservation and regression tests.
- [x] Complete application test suite: 98 passed.

## Next Development Priorities

- [ ] Design an easy-to-use webmaster administration interface.
- [ ] Add authenticated webmaster accounts and permissions.
- [ ] Implement creating and editing event records.
- [ ] Allow flyer PDF upload and replacement before events.
- [ ] Allow optional photo uploads after events.
- [ ] Allow selection or upload of approved maps after events.
- [ ] Establish explicit draft, published, and archive states.
- [ ] Establish specific approval for competition map release.
- [ ] Design MySQL models with SQLAlchemy and Alembic.
- [ ] Plan safe migration from existing JSON catalogs.
- [ ] Provide simple gallery, map, and flyer management tools.
- [ ] Review additional historical maps before publication.

## Before Production Launch

- [ ] Verify production packaging of all media and JSON data.
- [ ] Configure the Bluehost VPS application deployment.
- [ ] Set up HTTPS, production settings, and secrets.
- [ ] Configure backups, restoration, and rollback.
- [ ] Verify webmaster authentication and security.
- [ ] Review media ownership, privacy, and licensing.
- [ ] Complete mobile, desktop, and accessibility checks.
- [ ] Document webmaster handoff and recovery.

## Agreed Workflow

Create event → upload flyer before the ride →
optionally add photos and an approved map afterward →
retain all available materials in the archive.

Maps and photos are optional.

General riding-area maps must be distinguished from
event-specific competition maps.

An event passing its scheduled date must not automatically
publish its competition map.

Historical schedules do not necessarily prove a ride occurred.

WACMO remains separate from Projekt Orbit infrastructure.

## Development Session Log

### November 20, 2026 — Historical Maps and Events

**Accomplished**

- Reconciled historical map files against the original site.
- Preserved all 26 originally published maps.
- Created enlarged map previews and searchable map cards.
- Removed the duplicate legacy Maps section.
- Added 20 reviewed event/map links across six maps.
- Added related maps to event pages and related event links
  to the map library.
- Established board, architecture, AI-agent, and project
  status documentation for future maintainers.

**Verification**

- Full application test suite: 98 tests passed.
- Git whitespace check passed before documentation changes.
- Relevant feature commits:
  - `ee6d677` — Original riding-area map library.
  - `f60cd71` — Historical event/map integration.
- Documentation changes require review and a separate commit.

**Remaining**

- Webmaster editor and upload workflow.
- Database and migrations.
- Additional historical map review.
- Production packaging and Bluehost VPS deployment.

## End-of-Session Update Template

For each meaningful development session, add a dated entry
above the older entries.

Record:

- **Accomplished:** The features, fixes, or changes.
- **Verification:** Tests and manual checks performed.
- **Commit:** Relevant commit ID, if committed.
- **Remaining:** Bugs, incomplete work, and next priorities.
- **Decisions:** Important agreed requirements.

Update the checklist and last-updated date.

Mark a feature complete only when implemented and verified.

Keep planned, implemented, and deployed work clearly separate.
