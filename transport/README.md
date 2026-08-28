# `transport/` — enforced conservation gateway (salvaged, unwired)

An earlier, **independent** GEMS direction: instead of reconstructing the
Gem infrastructure from evidence (`../src/gems/`), this builds the one thing
`conservation_kernel` says a library cannot provide for itself — an enforced
transport boundary.

See [`PROVENANCE.md`](PROVENANCE.md) for where it came from, what was changed
to land it, and its gaps (no unit tests; not wired into the package).

## The idea

`conservation_kernel` verifies typed transformations but cannot stop a
downstream process from ignoring a rejection. `ConservationGateway`
(`gems_transport/transport.py`) is that missing choke point:

- a Gem's output is an untrusted **proposal**, never an accepted artifact;
- the gateway resolves the input artifact from **its own** accepted-artifact
  map, not from whatever the request claims;
- only `submit()` can promote a candidate, and only if the kernel accepts it;
- everything downstream (`Pipeline`) only ever sees accepted artifacts.

`experiments/` is a deterministic corpus of 20 attack types
(`AttackType`, `AdversarialGem`) that each try to smuggle an unauthorized
status/origin/authority change past the gateway, plus a control path that
bypasses it.

## Layout

```text
gems_transport/
  transport.py       ConservationGateway, GatewayReconstruction
  pipeline.py        Pipeline — only forwards accepted artifacts
  contracts.py       GEMS/0.1 wire contracts (proposal/record/decision/result)
  registry.py        GemRegistry allow-list, append-only TransformationLedger
  artifact.py        re-exports the kernel Artifact model + lineage refs
  tie_adapter.py     TIE integration point (raises TIEIntegrationMissing)
  reference_gems/    BaseGem + researcher/reviewer/summarizer/requirements/
                     architecture + AdversarialGem
experiments/
  corpus.py          synthetic TIE source, human-approval fixture
  attacks.py         run_hostile_corpus, control_outcomes
  run_experiment.py  writes results/initial_run.json
```

## Run

```bash
cd transport
PYTHONPATH=/path/to/conservation_kernel/src:. python3 -m experiments.run_experiment
```
