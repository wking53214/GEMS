# Provenance — `transport/`

## What this is

`transport/` is a **salvaged, unwired** second GEMS implementation: an
enforced output boundary (`ConservationGateway`) around
[`conservation_kernel`](https://github.com/wking53214/conservation_kernel),
plus a deterministic hostile-attack corpus that exercises it.

It is a *different architecture* from the reconstruction baseline in
`src/gems/`. It is landed here so the working code is not lost, not because
the two have been reconciled.

## Origin

- Files recovered from the local `~/GEMS` working tree during a housekeeping
  pass on 2026-08-28. They were **never committed** to any branch.
- Source file mtimes are 2026-08-17. The FER-1.0 reconstruction baseline
  (`src/gems/`, commit `af91766`) is dated 2026-08-19, so this code
  **predates** the baseline — it appears to be an earlier direction that was
  set aside.
- The original working tree was a package literally named `gems/` with a
  nested `gems/gems/`, and shipped its own `pyproject.toml`
  (`name = "gems-transport"`, pinned to `conservation_kernel@d6c67dc`) and an
  MIT `LICENSE`.

## What was changed on the way in

- Top-level package `gems/` → **`gems_transport/`** (avoids colliding with
  the importable `gems` package in `src/`).
- Nested `gems/gems/` → **`gems_transport/reference_gems/`**.
- Absolute imports in `experiments/` updated to the new package names.
  All in-package imports were already relative and are unchanged.
- The bundled `pyproject.toml` and MIT `LICENSE` were **dropped**. This repo
  is Apache-2.0 (root `LICENSE`) and has one `pyproject.toml` at the root.
- Generated `experiments/results/*.json` is git-ignored.

No logic in `gems_transport/` or `experiments/` was modified.

## Verification

Run against the **current** `conservation_kernel` (`dbbb22b`), not the
commit the original pyproject pinned:

```
control_accepted:                 20
treatment_accepted:                0
treatment_rejected_or_contained:  20
reference_pipeline_accepted:    true
```

All 20 hostile transformations are rejected or contained at the gateway; the
same 20 are accepted by the "control" path that bypasses the gateway; the
5-Gem reference pipeline with a human-approval fixture is accepted.

## Known gaps

- **No unit tests.** `experiments/run_experiment.py` is the only
  verification. "20/20 blocked" is an experiment result, not a test suite.
- **Not wired into the package.** `transport/` is not on `pyproject.toml`'s
  path and is not imported by `src/gems/` or the `tests/` suite.
- **Overlaps `src/gems/` without reconciliation** — both define contracts, a
  registry, and a TIE adapter, by different designs. Choosing between them is
  future work.

## How to run

```bash
pip install -e path/to/conservation_kernel        # or put its src/ on PYTHONPATH
cd transport
PYTHONPATH=/path/to/conservation_kernel/src:. python3 -m experiments.run_experiment
```
