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
