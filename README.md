# GEMS

Executable **reconstruction baseline** from the GEMS-FER-1.0 forensic package. Minimal deterministic contracts and adapters — **not** a claim that missing historical details existed. `transport/` is a second, unreconciled salvage (ConservationGateway + hostile corpus), **not wired** into `src/gems`.

## 1. Pipeline Position & Role

**RESEARCH / RECONSTRUCTION.** Off the live path. Optional observe-perceive extra `chain` pins GEMS **`273aeea`** (parent of `bb4cf40`, which **deleted** `HumanAuthorityGuard`, `HandoffValidator`, `governance/constitution.py` that `gems_governance_adapter.py` still imports). **Head of GEMS main will break ~16 hub tests.**

## 2. Full System Scope & Architectural Depth

`src/gems` (tiny vs docs):

- Frozen: `Provenance`, `Artifact`, `Handoff`, `GemSpec`, `WorkflowState` (frozen dataclass with **mutable** `history: list` — tests append)
- `Router.route(capability)`: all gems with the cap, **sort by name, take [0]** (deterministic, content-free)
- `WorkflowCoordinator` default `MockGemExecutor`: `content = f"{gem_name} processed: {input_artifact.content}"`, `quality_score=0.85`
- `GovernanceValidator`: provenance required; epistemic in enum. Does **not** block AI claiming `HUMAN_AUTHORIZATION` at construction
- `default_catalog.py`: 15 named GemSpecs — **strings only, no prompts, no implementations**
- `cognition/` and `integrations/` **empty**. TIE adapter in `transport/` raises `TIEIntegrationMissing`

Enums: `EpistemicStatus{explicit,inferred,unknown,conflicted}`, `Origin{human,ai,joint,uncertain}`, `Authority{observation,analysis,proposal,human_authorization}`. Several members reserved/tests-only.

`transport/`: `ConservationGateway` around Conservation Kernel; `BaseGem.transform` → `NotImplementedError`. pyproject declares `conservation-kernel` **for transport only**.

Docs + 2.6MB chat transcript outmass the code. ~94 tests prove dataclasses frozen and router alphabetical.

## 3. What It Does NOT Do / Non-Goals

Run specialized agents, talk to TIE, persist, deploy, or enforce human sovereignty in production.

## 4. Brutally Honest Current Status & Gaps

Commercial: **CONSULTING ENABLER at most.** Adapter pin must stay on `273aeea` or hub extra `chain` errors. Catalog looks like a product roster; it is a tuple of strings. Mock executor stamps authority regardless of input. No hashing in `src/gems`.

## 5. Core Invariants & Guarantees

Unknown capability → LookupError. Missing provenance → ValueError. Authority is a label. Mock will echo.

## 6. Inputs, Outputs & Type Contracts

`Artifact{artifact_id, kind, content, provenance, metadata}`. `Handoff{task_id, sender, recipient, artifacts}`. Schema: `schemas/provenance.schema.json`.

## 7. Stack Integration Topology

```text
observe-perceive gems_governance_adapter  --requires--> GEMS@273aeea (NOT current main)
transport/ ConservationGateway  --unwired--  Conservation_Kernel
TIE  --raises missing--
```

**Safe to archive for live path** if the hub extra is dropped or re-pinned to a reconstructed adapter.

Apache-2.0. Evidence boundary in this README is the contract; `docs/` overclaims.
