# GEMS Infrastructure

**Status: reconstruction baseline — not a claim of the historical canonical repository.**

This repository is the first executable baseline built from the supplied **GEMS-FER-1.0** forensic package. It intentionally separates recovered requirements from implementation choices made during this reconstruction.

## Evidence boundary

Recovered as strong/explicit evidence:
- specialized role-oriented Gems
- Workflow Coordinator responsibilities
- governed/typed handoffs
- provenance and epistemic-status preservation
- TIE as a foundational evidence-preserving source / "Gem Layer 1"
- Cognitive Continuity constraints, including human sovereignty and no silent AI→human authority conversion
- Triad+42 as a conceptual review/challenge mechanism

Not recovered from the supplied package:
- historical canonical repository tree
- production Gem implementations/prompts
- canonical universal Gem schema
- concrete transport/API
- database/vector store/deployment

Accordingly, this repository implements **minimal deterministic contracts and adapters**, not a reconstructed claim that these missing historical details existed.

## Layout

```text
src/gems/
  contracts/       typed contracts and provenance/epistemic models
  core/            registry, router, workflow coordinator, handoff
  governance/      human authority and validation boundaries
  integrations/    TIE package adapter
  cognition/       Triad+42 review mechanisms
schemas/           machine-readable baseline schemas
prompts/           recovered/preserved prompt references
```

## Run tests

```bash
python -m pytest
```

## `transport/` — a second, unreconciled direction

`transport/` holds an earlier, independent implementation salvaged from the
local working tree (never previously committed): an enforced
`ConservationGateway` around `conservation_kernel` plus a 20-attack hostile
corpus. It is landed as-is and **not wired into this package** — different
architecture, overlapping `src/gems/` on contracts/registry/TIE without being
reconciled. See `transport/PROVENANCE.md`.

## Design rule

The implementation preserves the distinction between:
- **recovered evidence**
- **reconstruction choices**
- **unknown historical details**

See `docs/RECONSTRUCTION_STATUS.md`.
