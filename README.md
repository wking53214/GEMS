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

## 8. Connecting to CNS (optional)

GEMS stands alone: no runtime dependency on CNS, nothing imported from CNS when
either package loads, and the whole suite passes without CNS installed. If CNS
is present, two connectors express GEMS's verdicts as CNS gate results so they
can be resolved alongside gates from other repositories. Native verdicts and
behavior are unchanged.

The extra pins CNS v1.4.0 by commit. Neither `gems-infrastructure` nor its
existing dependency `conservation-kernel` is on a package index, so as things
stand install the kernel from its own repository first and then this repo from a
checkout with the extra:

```
pip install /path/to/conservation-kernel
pip install '/path/to/gems[cns]'        # or '.[cns]' from inside this checkout
```

`pip install 'gems-infrastructure[cns]'`, the form the connectors' error
messages quote, is the same extra spelled for an index and resolves only once
both packages are published to one.

- `gems.cns_connector` covers `GovernanceValidator` in `src/gems`.
- `gems_transport.cns_connector` covers the `transport/` gateway (put
  `transport/` and `conservation-kernel` on the path, as for the experiment).

```python
from gems.cns_connector import validate_to_cns
from gems_transport.cns_connector import cns_chain, submit_to_cns, GatewaySubmission
from cns.gate import resolve

resolve([validate_to_cns(artifact, subject="handoff-7")])   # PASS or TERMINAL_BREACH
chain = cns_chain(gateway)                                   # alpha: input gate, omega: submit
alpha = chain.alpha[0].check(input_artifact)                 # before the Gem runs
omega = chain.omega[0].check(GatewaySubmission(request, proposal))   # is gateway.submit
resolve([alpha, omega])
```

| GEMS | CNS |
|---|---|
| `validate_artifact` returns | `PASS` at `OMEGA`. The position is a judgment call GEMS does not settle: nothing in `src/gems` calls the validator at all (only tests do). It is placed at `OMEGA` because it judges the provenance record an artifact carries, but an artifact handed to a Gem could equally be judged on the way in. The verdict is narrow: provenance is present and the epistemic status is a known value, nothing about `origin` or `authority`, so an AI artifact claiming `HUMAN_AUTHORIZATION` still passes. It is not evidence that anyone authorized anything. |
| `validate_artifact` raises `ValueError` | `TERMINAL_BREACH`; the reason is the validator's message. GEMS models no repair. Any other exception is not a verdict and propagates. |
| gateway input gate, `is_accepted(artifact)` (`Pipeline` refuses before the Gem runs) | `PASS` or `TERMINAL_BREACH` at `ALPHA`, reason `INPUT_GATE_REQUIRED` on refusal |
| `submit` decision `ACCEPTED` | `PASS` at `OMEGA`, only if the state is `ACCEPTED` and an accepted artifact exists |
| `submit` decision `REJECTED`, `REQUIRES_AUTHORIZATION`, `REQUIRES_VERIFICATION`, or any unknown status | `TERMINAL_BREACH`, with the decision's name and the refusal codes first in the reason. There is no `RETRY`: CNS means a re-render with an instructional delta, and this repo models no repair (`Pipeline` stops at the first refusal and raises `PipelineRejected`, and its hostile corpus expects `REJECTED` for every attack that reaches `submit`, the `REQUIRES_*` ones included). The gateway reports a forged authorization the same way as a missing one, so a retry loop would hand the refusal details straight back to the Gem. |
| judged content | `subject` label plus `subject_digest`. Validator: the artifact id and whole provenance record (enums reduced to values; `content` is not judged, so not bound). Input gate: artifact id and digest. `submit`: request and transformation ids, the registered Gem identity, source and candidate id and digest, and the kernel's `TransformationRecord.canonical_digest()`. |

`cns_chain(gateway).complete()` is `True` for the transport because both slots
are filled by the gateway's two real ends, which `Pipeline` runs on one artifact.
That is all it says: the connector is not wired into `Pipeline`, and nothing
enforces the order or that both verdicts concern one request. The two verdicts
overlap in content (the input digest is over the artifact id and digest, and the
output digest is over a different mapping that holds the same pair as its
source), but the digests themselves are different values and cannot be compared,
so a consumer cannot read "same request" off them. Running the ends in order on
the same artifact is the consumer's job, and the two gates take different
candidates (an `Artifact` for the input gate, a `GatewaySubmission` for the
output gate). For `src/gems` it is `False` by design: there is no precondition
end and the connector does not invent one. Content CNS cannot
digest (a NaN `note`, an object as `source_id`, a non-finite declared change, a
result with no record) makes the verdict `TERMINAL_BREACH` and unbound
(`cns.gate.unbound` names it), even when GEMS itself accepted. The transport
connector's `CnsOutputGate.check` is `submit`: judging and promotion are one
step there, so an accepted candidate is promoted.

Without CNS installed, the connectors' functions raise `CnsNotInstalled` with
the install command, before anything is judged. Nothing else changes.

Apache-2.0. Evidence boundary in this README is the contract; `docs/` overclaims.
