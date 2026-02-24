<!-- Auto-generated guidance for AI coding agents. Please review and iterate. -->
# Copilot instructions — nexfil

Purpose
- Help AI coding agents become productive quickly in this repository by describing the
  repository layout, development commands, and project-specific conventions.

Quick facts
- Language: Python (>=3.10) — see `pyproject.toml`.
- Console script / entrypoint: `nexfil` → `nexfil.cli:cli` (defined in `pyproject.toml`).
- Packaging: setuptools via `pyproject.toml` (dynamic version from `nexfil.cli.SCRIPT_V`).
- No CI workflows detected in `.github/workflows` (only `FUNDING.yml` present).

What to read first
- `pyproject.toml` — dependency list and entrypoint (`nexfil.cli:cli`).
- `README.md` — install and usage examples (`nexfil -u user` usage shown).
- `src/nexfil` (or `nexfil/`) — implementation modules; start at `cli.py` to see runtime flow.

Architecture notes (how this repo is organized)
- Single Python package providing a CLI that probes many websites for a username.
- CLI is the public surface — most work happens in modules under the package (search for
  lookup/website modules in `src/nexfil`).
- IO: network-bound (uses `aiohttp`, `requests`, and `undetected_chromedriver`).

Developer workflows (concrete commands)
- Install locally (editable):
  ```bash
  python -m pip install -e .
  ```
- Run the CLI directly after install:
  ```bash
  nexfil -u alice
  # or without installing:
  python -m nexfil.cli -u alice
  ```
- There are no test scripts or `tests/` directory in the repo root; don't assume a test runner.

Project-specific conventions and notes
- Entrypoint: keep CLI argument parsing in `nexfil/cli.py`. Changes to CLI flags must be
  reflected in `pyproject.toml` only if the console-script name or module path changes.
- Dynamic versioning: the package declares `version = {attr = "nexfil.cli.SCRIPT_V"}` —
  update `SCRIPT_V` in `cli.py` to change the packaged version rather than editing
  `pyproject.toml` manually.
- Dependencies: the project depends on `undetected_chromedriver`. Agents should note
  that running code using that package may require a matching Chrome browser and
  will behave differently in headless vs full-browser environments.

Integration points & external dependencies
- Network calls to many third-party sites; expect long-tail HTTP failures and timeouts.
- No message queues or databases; results are written to files as per README.

What to avoid editing
- Do not assume build artifacts exist; there is no `dist/` or `build/` in repo.
- Avoid changing generated or vendored assets if present — search for `gen/` or `vendor/`.

How this agent will operate here
- Start by opening `pyproject.toml`, `README.md`, and `src/nexfil/cli.py`.
- When modifying network probing logic, run small live checks using a single username
  (e.g., `nexfil -u testuser`) rather than attempting large batches.
- If adding dependencies, update `pyproject.toml` and run `pip install -e .` locally.

References (examples in this repo)
- Entrypoint: `pyproject.toml` → `[project.scripts] nexfil = "nexfil.cli:cli"`.
- Usage example: `README.md` contains concrete CLI flags and sample invocations.

Questions for humans
- Are there unit or integration tests expected to be added later? If yes, where should
  they be placed and what test runner should be used?
- Are there private site credentials or env var conventions (e.g., `NEXFIL_PROXY`)?

If anything here is unclear, ask for a quick pointer to the file you want prioritized
and I will update these instructions with precise line examples.
