# GEMS Baseline Architecture

```text
                         GEMS
                          |
          +---------------+----------------+
          |               |                |
       Registry         Router        Governance
          |               |                |
          +---------------+----------------+
                          |
                  Workflow Coordinator
                          |
                    Typed Handoff
                          |
                 Specialized Gems
                          |
                    TIE Adapter
                          |
                    TIE_PACKAGE

              Triad+42 = review/challenge plane
```

The diagram is a reconstruction baseline, not a historical recovered diagram.

## Core invariants

1. A Gem has a bounded role and capability set.
2. Handoffs preserve provenance and epistemic status.
3. AI-originated material cannot be represented as human authorization without explicit human action.
4. TIE-derived material remains evidence-linked.
5. Review mechanisms may challenge a proposal but do not silently create authority.
6. Unknown historical details remain explicit rather than fabricated.

Workflow execution exposes a typed lifecycle (`created`, `running`, `completed`,
`failed`). The existing `execute()` API remains compatible, while
`execute_enveloped()` additionally returns a structured result containing the
task and artifact identity, provenance, execution state, and explicit
placeholders for integrity, telemetry, and verification supplied by future
integrations.

`gems.integrations.verified_artifact` defines the future integration boundary
for external artifact verification and lineage. It carries source/output
artifacts, external identities, transformation identity, and verification
status, but deliberately does not implement hashing, canonicalization,
attestation, or repository-specific dependencies.
