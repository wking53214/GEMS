# GEMS

Executable **reconstruction baseline** from the GEMS-FER-1.0 forensic package. Minimal deterministic contracts and adapters, **not** a claim that missing historical details existed. `transport/` is a second, unreconciled salvage (ConservationGateway + hostile corpus), **not wired** into `src/gems`.

## Role Within ≡TACK

- **What it is.** A reconstruction baseline: small frozen contracts, a router, a mock workflow coordinator, a provenance validator, and a separate unwired `transport/` gateway around Conservation_Kernel. Research, off the orchestrator path. No model is called anywhere in this repo: there is no network or model-provider code in `src/gems`, `transport/` or `test-track/` (INSPECTED 2026-11-17), and the default executor is a mock.
- **Authority matrix.** Evaluation only, in `GovernanceValidator` (provenance required; a non-human artifact may not claim human authorization). `src/gems` does not define policy, enforce, authorize, authenticate or generate durable evidence (no hashing in `src/gems`). Authority is a label: an artifact whose origin is written as `human` may claim human authorization, and nothing checks who wrote it (EXECUTED 2026-11-17). `transport/` is different: its `ConservationGateway` refuses a submission the kernel does not accept, refuses to be built without the deployer's guards unless two opt-out flags are passed (EXECUTED: `UnguardedKernelError`), and keeps an append-only ledger that is not authenticated. It is not wired into `src/gems` and nothing in this repo runs it outside tests.
- **Does not own.** Running real agents (the mock executor echoes input and stamps a fixed quality score), the TIE integration beyond its source adapter, or the orchestrator path.
- **Depends on.** `conservation-kernel` for `transport/`, pinned by git commit in `pyproject.toml`. CNS is optional (section 8).
- **Depended on by.** observe-perceive's `gems_governance_adapter`, through its optional `chain` extra, which pins GEMS `f7d40fc` (re-checked 2026-11-17; see section 1).
- **Fail behavior.** Closed on its few checks: unknown capability raises `LookupError`, missing provenance raises `ValueError`. Nothing enforces human sovereignty in production.

## 1. Pipeline Position & Role

**RESEARCH / RECONSTRUCTION.** Off the orchestrator path. Re-checked 2026-11-17: observe-perceive's optional extra `chain` pins GEMS **`f7d40fc`** (GEMS PR #13, the HUMAN-origin allowlist), which is on GEMS main, 9 commits behind its head `8e4ba48`. Its `gems_governance_adapter.py` uses `GovernanceValidator`, which exists at the pin and at head. Its 16 adapter tests pass at the pin and with GEMS main installed in its place (EXECUTED 2026-11-17). So GEMS main does not break the hub today.

Earlier text here said the hub pinned `273aeea` and that the head of GEMS main would break about 16 hub tests. That described the hub's older adapter, which imported `HumanAuthorityGuard`, `HandoffValidator` and `governance/constitution.py`; GEMS deleted those and the hub's adapter was rewritten. The commit ids in that older text (`273aeea`, `bb4cf40`) and the id `f70da70` come from before GEMS main's history was rewritten and are not on main. The same commits are now `91ddb52`, `55b9e38` and `f7d40fc` (VERIFIED by commit subject and date).

## 2. Full System Scope & Architectural Depth

`src/gems` (tiny vs docs):

- Frozen: `Provenance`, `Artifact`, `Handoff`, `GemSpec`, `WorkflowState` (frozen dataclass with **mutable** `history: list`, tests append)
- `Router.route(capability)`: all gems with the cap, **sort by name, take [0]** (deterministic, content-free)
- `WorkflowCoordinator` default `MockGemExecutor`: `content = f"{gem_name} processed: {input_artifact.content}"`, `quality_score=0.85`
- `GovernanceValidator`: provenance required; epistemic in enum; refuses any non-`HUMAN`-origin artifact claiming `HUMAN_AUTHORIZATION` (allowlist: AI, JOINT, UNCERTAIN are all refused)
- `default_catalog.py`: 15 named GemSpecs, **strings only, no prompts, no implementations**
- `cognition/` and `integrations/` **empty**. `transport/` has a TIE source adapter, `TIEPackageSource`, that turns a TIE package into a kernel Artifact for `ingest_source` (TIE is its own repo); the older `require_tie_adapter` slot still raises `TIEIntegrationMissing`

Enums: `EpistemicStatus{explicit,inferred,unknown,conflicted}`, `Origin{human,ai,joint,uncertain}`, `Authority{observation,analysis,proposal,human_authorization}`. Several members reserved/tests-only.

`transport/`: `ConservationGateway` around Conservation Kernel; `BaseGem.transform` → `NotImplementedError`. pyproject declares `conservation-kernel` **for transport only**.

Docs outmass the code: about 860 KB of Markdown against about 160 KB of Python in `src/` and `transport/` (measured 2026-11-17). The suite proves dataclasses are frozen and the router is alphabetical, among other checks.

EXECUTED 2026-11-17 at `8e4ba48`, Python 3.13, each run in its own fresh environment:

- Bare checkout with pytest only: 1 failed, 122 passed, 6 skipped.
- This package installed (which brings the pinned kernel), no CNS, no TIE: 1 failed, 178 passed, 5 skipped.
- Before the CNS pin moved to v4.1.0 (2026-11-20), the way CI ran it (kernel `cc42d3f`, TIE `895ce7e`, CNS v4.0.0, `GEMS_REQUIRE_TRANSPORT=1`): 244 passed, 0 skipped.
- The same with the kernel and TIE at their mains (`8ed1636`, `7619b95`) and CNS v4.1.0: 244 passed.

`tests/test_governance_authority.py::test_cns_verdict_is_breach_not_pass_for_ai_authorization_claim` skips when CNS is absent (it failed before 2026-11-19). The 244 recorded here on 2026-11-15 needs all three siblings installed, not the kernel alone. The transport experiment script, which stopped with an `AttributeError` (EXECUTED 2026-11-17), was moved to the Graveyard repo on 2026-11-19; the hostile-corpus tests in the suite pass. Not run: GitHub CI, Python 3.11 (CI's version).

## 3. What It Does NOT Do / Non-Goals

Run specialized agents, talk to TIE, persist, deploy, or enforce human sovereignty in production.

## 4. Brutally Honest Current Status & Gaps

Commercial: **CONSULTING ENABLER at most.** The hub's `chain` extra pins `f7d40fc` and also passes at GEMS main (section 1). Catalog looks like a product roster; it is a tuple of strings. Mock executor stamps authority regardless of input. No hashing in `src/gems`.

## 5. Core Invariants & Guarantees

Unknown capability → LookupError. Missing provenance → ValueError. Authority is a label. Mock will echo.

## 6. Inputs, Outputs & Type Contracts

`Artifact{artifact_id, kind, content, provenance, metadata}`. `Handoff{task_id, sender, recipient, artifacts}`. Schema: `schemas/provenance.schema.json`.

## 7. Stack Integration Topology

```text
observe-perceive gems_governance_adapter  --optional extra--> GEMS@f7d40fc (on main; also passes at head)
transport/ ConservationGateway  --unwired--  Conservation_Kernel
TIE  --TIEPackageSource reads a TIE package (transport/ only); the old adapter slot still raises--
```

**Safe to archive for the orchestrator path** if the hub extra is dropped or re-pinned to a reconstructed adapter.

## 8. Connecting to CNS (optional)

GEMS stands alone: no runtime dependency on CNS, nothing imported from CNS when
either package loads. Without CNS the connector tests skip and one test fails
(section 2); the rest of the suite passes. If CNS
is present, two connectors express GEMS's verdicts as CNS gate results so they
can be resolved alongside gates from other repositories. Native verdicts and
behavior are unchanged.

The extra pins CNS v4.1.0 by tag. Neither `gems-infrastructure` nor its
existing dependency `conservation-kernel` is on a package index, so as things
stand install the kernel from its own repository first and then this repo from a
checkout with the extra:

```
pip install /path/to/conservation-kernel
pip install '/path/to/gems[cns]'        # or '.[cns]' from inside this checkout
```

`pip install 'gems-infrastructure[cns] @ git+https://github.com/wking53214/GEMS.git@main'`, the form the connectors' error
messages quote, installs the same extra straight from the repository. The bare `pip install 'gems-infrastructure[cns]'` does
not work: no package of that name is published.

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
| `validate_artifact` returns | `PASS` at `OMEGA`. The position is a judgment call GEMS does not settle: nothing in `src/gems` calls the validator at all (only tests do). It is placed at `OMEGA` because it judges the provenance record an artifact carries, but an artifact handed to a Gem could equally be judged on the way in. The verdict is narrow: provenance is present, the epistemic status is a known value, and an AI-origin artifact claiming `HUMAN_AUTHORIZATION` is refused. A `PASS` is still not evidence that anyone authorized anything. |
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
