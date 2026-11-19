# WACMO Website

Website modernization project for the Washington Association
of Competitive Mounted Orienteering.

## Overview

A lightweight, volunteer-friendly website for WACMO.

Planned features:

- Event calendar and ride schedules
- Ride flyers with automatic archives
- Event photo galleries
- Riding-area information and maps
- Simple administration for volunteer webmasters

## Technology

- Python 3.12+
- Flask
- MySQL (planned)
- SQLAlchemy / Alembic (planned)
- HTML, CSS, and JavaScript

## Development

Development host: orbithome (FreeBSD)

Create the Python environment:

    python3.12 -m venv .venv

Install dependencies:

    .venv/bin/python -m pip install -e '.[dev]'

Run tests:

    .venv/bin/python -m pytest -vv -rA

Start the development server:

    .venv/bin/python -m flask --app wacmo run --debug

The Flask development server is for local development only.

## Deployment

Production target: Bluehost VPS (Linux).

Production configuration and deployment instructions
will be documented when implemented.

## Licensing

Copyright (C) 2026 Alex Ekstrom.

Original website software is licensed under AGPL-3.0-only.

See LICENSE and LICENSING.md.

WACMO photographs, logos, flyers, maps, and third-party
materials retain their respective rights.
