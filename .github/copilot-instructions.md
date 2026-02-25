<!-- Auto-generated guidance for AI coding agents for the nexfil repo. -->
# Copilot instructions — nexfil

Purpose
- Help an AI agent become productive quickly by pointing to the runtime entrypoints,
  developer commands, and repo-specific caveats discovered in `src/nexfil`.

Top pointers (read these first)
- `pyproject.toml` — package metadata and console script (`nexfil -> nexfil.cli:cli`).
- `README.md` — install and CLI usage examples (see `nexfil -u user`).
- `src/nexfil/cli.py` — runtime flow, CLI flags, and `SCRIPT_V` (version string).
- `src/nexfil/url_store.json` — primary list of probe URLs; modify with care.

Concrete examples and commands
- Install editable package:
  ```bash
  python -m pip install -e .
  ```
- Run (installed):
  ```bash
  nexfil -u alice
  ```
- Run (module mode):
  ```bash
  python -m nexfil.cli -u alice
  ```

Key implementation notes (discoverable in `src/nexfil`)
- Versioning: `SCRIPT_V` is defined at the top of `src/nexfil/cli.py` — update that
  constant to change the package version used by `pyproject.toml`'s dynamic attr.
- URL data: `src/nexfil/url_store.json` holds the probe definitions (fields: `url`,
  `test`, `data`). The CLI loads this at startup (`cli()` -> `url_store_path`).
- Headless driver: `cli.py` attempts to import `undetected_chromedriver` and starts
  a Chrome driver (headless). If the import fails the code continues with `driver=False`.
  See `cli.py` for the `try/except` around `uc.Chrome` setup — agents should expect
  different behavior in headless vs full Chrome and that a local Chrome installation may be required.
- Network: the tool mixes `requests` (for update checks) and `aiohttp` (for probes).
  Expect transient network errors and timeouts (handled in `query()` and logged via `nexfil.write_log`).

Paths & runtime behavior to remember
- Local logs and dumps: `~/.local/share/nexfil/exceptions.log` and `.../dumps/` (created at runtime).
- Results: when hits are found an autosave file is written into the `dumps` folder.

Conventions and agent workflow
- Keep CLI parsing inside `src/nexfil/cli.py`; change flags there and test via
  `python -m nexfil.cli -u testuser` before editing packaging metadata.
- For changes to probing logic, update the specific test functions under files like
  `src/nexfil/url.py`, `src/nexfil/method.py`, `src/nexfil/alt.py`, and run a small live probe.
- If adding dependencies (e.g., `selenium` or `undetected_chromedriver`), update
  `pyproject.toml` and re-install editable package.

What to avoid
- Do not edit `src/nexfil/url_store.json` blindly — tests and manual review are required.
- Avoid committing local build artifacts; repo has no `dist/` or CI build files to expect.

Next steps I can take
- Add line-specific examples from `src/nexfil/cli.py` or any other file (tell me which file).
- Push the commit to the remote if you want (I'll ask for credentials or use your git auth).

Questions for maintainers
- Preferred test framework/location for tests? (no tests present today)
- Any env vars for proxies or credentials to document?

If you want more detail, tell me which file to extract example lines from and I'll update this file.
