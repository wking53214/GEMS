# GEMS Forensic Audit: Phase 1 Baseline

**Date**: 2026-09-20  
**Status**: INSPECTION COMPLETE - FINDINGS DOCUMENTED

---

## Executive Summary

The repository contains **three materially different things** that must not be confused:

1. **`src/gems/`** - Reconstruction baseline with forensic data model
2. **`transport/`** - Orphaned implementation direction (unreconciled)
3. **`test-track/`** - Simulation harness claiming to test real GEMS

**Critical Finding**: The Phase 2 test-track 91.7/100 score is **simulation evidence only**, not GEMS runtime evidence.

---

## PART 1: `src/gems/` - Current State

### What Exists

**Core Components**:
- `core/registry.py` - In-memory GemRegistry (stores GemSpecs by name)
- `core/router.py` - Deterministic Router (filter by capability, alphabetic sort, return first)
- `core/workflow.py` - WorkflowState (minimal: task_id, status, baseline, history)
- `contracts/models.py` - Immutable data model (Artifact, Provenance, Handoff, GemSpec - all frozen)
- `governance/validator.py` - GovernanceValidator (checks Provenance exists, EpistemicStatus valid)

**Exported API**:
```python
GemRegistry, Router, WorkflowState, GovernanceValidator
+ all contracts (Artifact, Provenance, Handoff, GemSpec, etc.)
```

### What Is Missing

**Critical Gap: No Workflow Coordinator/Executor**

There is no component that:
- Takes a capability request
- Routes to a Gem (via Router)
- Invokes/executes the Gem
- Creates a Handoff
- Handles the result
- Tracks workflow state

The Router returns a `Route(gem_name, capability)` but there is no code that **acts on** that route.

### Routing Analysis

Current router behavior:
```python
def route(self, capability: str) -> Route:
    matches = [g for g in self.registry.list() if capability in g.capabilities]
    if not matches:
        raise LookupError(f"No Gem advertises capability: {capability}")
    matches.sort(key=lambda g: g.name)  # alphabetic sort
    selected = matches[0]
    return Route(selected.name, capability)
```

**Findings**:
- ✅ Exact capability match
- ✅ Deterministic (alphabetic tie-break)
- ✅ No-match throws LookupError
- ❓ Multiple-match: first alphabetically (no policy, no customization)
- ❓ No provenance tracking of routing decision
- ❓ No human constraint support
- ❓ No governance veto capability

**Assessment**: Sufficient for basic routing, but lacks richness for complex multi-specialist workflows.

### Handoff Analysis

Current Handoff contract:
```python
@dataclass(frozen=True)
class Handoff:
    task_id: str = ""
    sender: str = ""
    recipient: str = ""
    artifacts: tuple[Artifact, ...] = ()
```

**What it preserves**:
- ✅ Artifact identity (by reference)
- ✅ Source relationship (sender/recipient)
- ✅ Workflow identity (task_id)
- ✅ Provenance (artifacts carry it)

**What is not tested**:
- Authority escalation during handoff
- Epistemic status preservation across handoff
- Parent artifact lineage tracking
- Transformation detection

### Authority Analysis

**Current Model**:
- Authority enum: OBSERVATION, ANALYSIS, PROPOSAL, HUMAN_AUTHORIZATION
- Provenance carries authority
- GovernanceValidator checks Provenance exists
- **No runtime enforcement** of authority transitions

**Problem**: Authority is data, not enforced logic. A Gem could theoretically create an Artifact with `authority=HUMAN_AUTHORIZATION` and the system wouldn't reject it (no validation happens at creation time).

---

## PART 2: `transport/` - Orphaned Direction

### What It Contains

**ConservationGateway class**: An "accepted-artifact boundary" that:
- Depends on external `conservation_kernel` (not in repository)
- Implements EvidenceRegistry, AuthorizationEvent, VerificationResult
- Has TransformationLedger for tracking handoffs
- Implements `ingest_source()`, `accept_transformation()` methods

**Status**: 
- ❌ **NOT RUNNABLE** - Missing `conservation_kernel` dependency
- ❌ **NOT INTEGRATED** - No imports in `src/gems/`
- ❓ **RELATIONSHIP UNCLEAR** - Is this supposed to be part of GEMS? External integration boundary? Abandoned experiment?

### Architectural Relationship

No evidence in current codebase that reconciles `transport/` with `src/gems/`. Two possibilities:

1. **External Boundary**: `transport/` should remain separate, represents an external governance system
2. **Abandoned**: `transport/` was a research direction that didn't ship

**Decision Pending**: Requires explicit architectural analysis (Phase 10).

---

## PART 3: `test-track/` - The Simulation Problem

### Execution Path

```
run_phase2.py
  ├─ WorkflowEngine (test-track/harness/engine.py)
  │   ├─ load_gems_catalog() [hardcoded names only]
  │   ├─ execute_workflow()
  │   │   ├─ For each step:
  │   │   │   ├─ Check: gem_name in catalog? (routing_correct)
  │   │   │   ├─ Check: dependencies met? (context_preserved)
  │   │   │   └─ Call: gem_executors[gem] OR _default_executor()
  │   │   │
  │   │   └─ _default_executor() ← SIMULATION ENDPOINT
  │   │       └─ return {
  │   │           "authority_respected": True,      # hardcoded
  │   │           "quality_score": 0.85,            # hardcoded
  │   │           "errors": [],
  │   │           **{f"output_{inp}": ...}
  │   │       }
  │   │
  │   └─ calculate_aggregate_scores()
  │
  ├─ MetricsCollector
  │   └─ routing_accuracy: (gems in catalog) / total
  │   └─ continuity_preservation: (dependencies met) / total
  │   └─ authority_violations: (not authority_respected) → always 0
  │   └─ output_quality: average quality_score → always 0.85
  │
  └─ ScoringRubric
      └─ score_workflow()
          ├─ routing_accuracy × 30 pts
          ├─ continuity_preservation × 30 pts
          ├─ authority_respect: 20 - (violations × 5) → always 20
          ├─ output_quality × 15 pts
          ├─ efficiency × 5 pts
          └─ total ≈ 91.7/100
```

### Why 91.7 Score Is Misleading

**Routing accuracy**: Checks `gem_name in gems_catalog` → dictionary lookup, not actual GEMS Router
**Continuity preservation**: Checks dependencies in context dict → simulated state, not actual Handoff
**Authority violations**: Always 0 because `_default_executor()` hardcodes `authority_respected=True`
**Output quality**: Always 0.85 because `_default_executor()` hardcodes it
**No GEMS code is actually executed**

### What It Claims vs Reality

| Claim | Reality |
|-------|---------|
| "Real GEMS workflow execution" | Simulation with hardcoded responses |
| "91.7/100 GEMS quality" | 91.7/100 simulation harness quality |
| "Routing accuracy verified" | Dictionary key lookup, not Router.route() |
| "Authority violations checked" | Hardcoded True, never actually verified |
| "Output quality assessed" | Hardcoded 0.85, never actually generated |

---

## PART 4: Tests - What They Actually Test

### `test_forensic_analysis.py` (6 tests)

**What**: Data structure creation and immutability
**Example**: 
```python
def test_workflow_state_with_baseline():
    artifact = Artifact(content="data", provenance=...)
    state = WorkflowState(baseline=(artifact,))
    assert state.baseline[0].content == "baseline data"
```

**Assessment**: ✅ Valid unit tests for data model, ❌ no execution logic tested

### `test_forensic_variants.py` (50 tests)

**What**: Combination/variant testing of data structures
**Assessment**: ✅ Valid, but same limitation - data structure tests only

### `test_registry_router.py`

**What**: Not yet inspected in detail

---

## PART 5: Triad+42

**Location**: `src/gems/cognition/triad42.py`

**Status**: 
- ✅ Present in codebase
- ❓ Not imported anywhere in current `src/gems/__init__.py`
- ❓ Relationship to GEMS execution unclear
- ❓ Appears to be removed during forensic stripping phase

**Decision Pending**: Requires evidence-based analysis (Phase 11).

---

## Classification of Current State

| Component | Classification | Evidence |
|-----------|-----------------|----------|
| `src/gems` contracts | RECOVERED | Frozen dataclasses, Provenance model, clear intent |
| `src/gems` Router | RECOVERED | Simple, deterministic capability matching |
| `src/gems` WorkflowState | INFERRED | Minimal forensic tracking, reconstructed |
| `src/gems` Coordinator | MISSING | No execution logic exists |
| test-track 91.7 score | SIMULATION ONLY | Hardcoded responses, no GEMS invocation |
| `transport/` ConservationGateway | EVIDENCE-BLOCKED | Depends on missing `conservation_kernel` |
| Triad+42 role | UNKNOWN | Not integrated, relationship unclear |

---

## Required Next Steps

### Phase 2: Test Boundary Definition

Create clear distinction:
- **UNIT**: Router.route() with various inputs
- **INTEGRATION**: Router → Gem execution → Handoff
- **END-TO-END**: Multi-step workflow with multiple Gems
- **SIMULATION**: Test harness with _default_executor (clearly labeled)

### Phase 3: Rebuild Test Track

1. Keep workflow definitions, metrics concepts, persistence
2. Change execution: actual GEMS Router and (once built) Coordinator instead of simulation
3. Separate simulation tests from real tests

### Phase 4: Build Missing Coordinator

Create `src/gems/core/coordinator.py` that:
- Takes a capability request + initial Artifact
- Routes via Router
- Invokes a Gem (needs to handle "what is a Gem" - currently specs only)
- Creates Handoff with provenance preserved
- Tracks WorkflowState

### Phase 5-9: Audit & Fix Each Component

Routing, Workflow, Handoff, TIE, Authority

### Phase 10: Reconcile transport/

Determine relationship to GEMS

### Phase 11: Triad+42

Establish role or document as removed

---

## Honest Assessment

**Current GEMS status**:
- ✅ Data model is sound (Provenance, Artifact, Handoff, frozen contracts)
- ✅ Router is simple but functional
- ✅ Governance validator catches basic violations
- ❌ **No execution runtime** - missing Coordinator/Executor
- ❌ **No actual Gem definitions** - only specs, no implementations
- ❌ **Test score is fraudulent** - measures simulation, not runtime

**Do NOT ship this as "GEMS is ready for production".**

The system is a reconstruction baseline with a simulation test harness. Real engineering remains.

---

## Next Decision Point

Proceed to Phase 2-3 to rebuild test track around actual GEMS execution?

**Prerequisite**: Build WorkflowCoordinator that invokes actual Gems (Phase 4).
