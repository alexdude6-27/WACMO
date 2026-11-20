# WACMO Technical Architecture

Last reviewed: November 20, 2026.

This document describes the implemented application.
See `docs/PROJECT_STATUS.md` for remaining development.

## Project Boundaries

WACMO is a separate Python/Flask application.

Development checkout: `/home/alex/wacmo` on OrbitDesktop,
running FreeBSD.

WACMO is independent of Projekt Orbit and OrbitWork.
Do not mix their source trees, databases, secrets, or
deployment processes.

Planned production host: Bluehost VPS running Linux.

Production deployment is not implemented yet.

## Current Technology

- Python 3.12 or newer.
- Flask, as declared in `pyproject.toml`.
- Jinja HTML templates.
- CSS and JavaScript.
- JSON catalogs for historical content.
- Static PDF, image, font, and other media files.
- Pytest regression tests.
- Git for source control.

MySQL, SQLAlchemy, Alembic, and an administrative editing
interface are planned but not implemented.

## Repository Layout

| Location | Purpose |
| --- | --- |
| `wacmo/__init__.py` | Flask application factory, routes, navigation |
| `wacmo/calendar.py` | Calendar and date calculations |
| `wacmo/events_archive.py` | Historical schedule loading |
| `wacmo/event_flyers.py` | Event flyer associations |
| `wacmo/photo_albums.py` | Photo albums and event links |
| `wacmo/riding_area_maps.py` | Published map catalog |
| `wacmo/event_maps.py` | Reviewed event/map relationships |
| `wacmo/data/` | JSON records and catalogs |
| `wacmo/templates/` | Website templates |
| `wacmo/static/` | Styles, JavaScript, and original media |
| `reference/original-site/` | Preserved original website HTML |
| `tests/` | Regression and preservation tests |

## Event Architecture

Historical events have stable IDs.

Event detail pages are available at `/events/<event_id>`.

An event can have:

- Zero or more original flyer documents.
- Zero or more associated photo albums.
- Zero or more approved riding-area reference maps.

Attachments remain optional.

Current associations are maintained through JSON records
and Python loaders, not a database.

A historical schedule listing alone does not prove that
an event actually took place.

## Maps

The public map library is available at `/riding-areas`.

The catalog is `wacmo/data/riding_area_maps.json`.

It contains 26 maps originally published by WACMO.
Original PDF and thumbnail integrity is verified by tests.

The catalog also references enlarged previews.

The file `wacmo/data/event_map_associations.json`
contains 20 reviewed associations involving six maps.

These are general riding-area references, not verified
competition courses from the corresponding ride dates.

Additional historical PDFs in the original backup require
individual review before publication.

## Local Development

From `/home/alex/wacmo`:

    python3.12 -m venv .venv
    .venv/bin/python -m pip install -e '.[dev]'

Run the complete test suite:

    .venv/bin/python -m pytest -vv -rA --durations=10 --durations-min=0

Start the local development server:

    .venv/bin/python -m flask --app wacmo run --debug

The Flask development server is not intended for production.

The verified baseline on November 20, 2026 is 98 tests passed.

## Future Architecture

The planned event-management system will use:

- MySQL and SQLAlchemy.
- Alembic migrations.
- Authenticated webmaster accounts.
- Draft and published content states.
- Explicit map publication approval.
- Media upload and replacement.
- Administrative auditing and safe recovery.

The intended event lifecycle is:

Create event, upload flyer before the ride, optionally
attach photographs and an approved map afterward, then
retain the event in the historical archive.

Passing the event date must never automatically release
a competition course.

## Production Considerations

Before VPS deployment, verify that the Python package
includes all required media and data files.

`pyproject.toml` currently lists selected package-data
patterns, so nested image directories, PDFs, and JSON
catalogs require packaging verification.

Production work must also cover HTTPS, application serving,
access controls, backups, restoration, and rollback.

Source code and current tests are authoritative if these
documents become outdated.

See `AGENTS.md` for safe maintenance practices.
