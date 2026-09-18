# Knowledge Architect Routing Rules

## Automatic Escalation Rules

The Router automatically escalates work to Knowledge Architect (in addition to primary specialist) when:

### 1. Architecture Decisions (Priority: HIGH)

Any decision affecting:
- Module relationships or dependencies
- Component interfaces or contracts
- System design or layer organization
- Communication patterns between specialists
- Workflow routing or handoff mechanisms

**Routing:** `Router → [Primary Specialist, Knowledge Architect]`

### 2. Functional Changes (Priority: HIGH)

- Removing functionality (no matter how small)
- Replacing existing functionality
- Changing or deprecating interfaces
- Modifying data structures or schemas
- Changing how work flows through the system

**Routing:** `Router → [Primary Specialist, Knowledge Architect]`

### 3. Governance Changes (Priority: HIGH)

- Authority boundary changes
- Decision right modifications
- Approval process changes
- Security policy changes
- Constraint modifications

**Routing:** `Router → [Primary Specialist, CCC, Knowledge Architect]`

### 4. Integration Points (Priority: MEDIUM)

- Connecting new systems to existing architecture
- Defining new inter-Gem interfaces
- Establishing new handoff protocols
- Adding new external dependencies

**Routing:** `Router → [Integration Guardian, Knowledge Architect]`

### 5. Design Alternatives (Priority: MEDIUM)

When multiple design approaches are under consideration:
- Document each alternative
- Document rationale for selection
- Document why alternatives were rejected
- Preserve for future reference

**Routing:** `Router → [Engineering Architecture & Evolution, Knowledge Architect]`

### 6. Technical Debt Identification (Priority: MEDIUM)

When known limitations, workarounds, or incomplete implementations are identified:
- Document the limitation
- Document the reason it exists
- Document the impact
- Preserve for future prioritization

**Routing:** `Router → [Engineering Architecture & Evolution, Knowledge Architect]`

### 7. Contradiction Resolution (Priority: HIGH)

When documentation conflicts with implementation:
- Document the conflict
- Identify which is authoritative
- Preserve both positions until reconciliation
- Flag for future resolution

**Routing:** `Router → [Primary Specialist, Knowledge Architect]`

### 8. Historical Context Recovery (Priority: MEDIUM)

When reason for a decision is unknown or unclear:
- Research available context
- Document what is known
- Document what is uncertain
- Document what is unknown
- Flag for future clarification

**Routing:** `Router → [Research Analyst, Knowledge Architect]`

### 9. System Integration Changes (Priority: HIGH)

When TIE, Conservation Kernel, Governance Gateway, Triad-42, or CCC interact with changes:
- Document the interaction
- Preserve boundary rules
- Document assumptions
- Preserve integration rationale

**Routing:** `Router → [Integration Guardian, Knowledge Architect, relevant specialized system]`

### 10. Specification Formalization (Priority: MEDIUM)

When implicit architecture is formalized into specification:
- Document what was implicit
- Document what is now explicit
- Document why formalization occurred
- Preserve rationale for formalization

**Routing:** `Router → [Engineering Architecture & Evolution, Knowledge Architect]`

---

## Conditional Escalation Triggers

### Escalate if ANY of these apply:

1. **Change affects more than one specialist domain**
   - Recommendation: Escalate to Knowledge Architect + Integration Guardian

2. **Change reverses a previous decision**
   - Recommendation: Escalate to Knowledge Architect + original decision maker (if available)

3. **Change is preceded by "we tried this before"**
   - Recommendation: Escalate to Knowledge Architect to recover historical context

4. **Implementation contradicts documented design**
   - Recommendation: Escalate to Knowledge Architect to identify and preserve conflict

5. **Decision rationale is unclear**
   - Recommendation: Escalate to Knowledge Architect + Research Analyst

6. **Change affects security, governance, or authority**
   - Recommendation: Escalate to Knowledge Architect + CCC + Security & Governance Auditor

7. **Multiple alternatives exist with different tradeoffs**
   - Recommendation: Escalate to Knowledge Architect to document alternatives

8. **Modification of interfaces or contracts**
   - Recommendation: Escalate to Knowledge Architect to preserve interface history

---

## Knowledge Architect Output Requirements

When Knowledge Architect is involved, output must include:

### For Architecture Decisions:
- [ ] Decision made (what was chosen?)
- [ ] Problem context (what problem existed?)
- [ ] Alternatives considered (what else was evaluated?)
- [ ] Rationale (why this choice?)
- [ ] Tradeoffs (what was gained/lost?)
- [ ] Dependencies (what depends on this?)
- [ ] Assumptions (what must be true for this to work?)
- [ ] Constraints (what limits existed?)
- [ ] Future considerations (what should future systems know?)

### For Functional Changes:
- [ ] What changed
- [ ] What was removed (if applicable)
- [ ] Why it changed
- [ ] Impact on other components
- [ ] Migration path (if applicable)
- [ ] Historical precedent (if any)

### For Contradictions:
- [ ] What contradicts what
- [ ] Which is authoritative (if known)
- [ ] Evidence for each position
- [ ] Historical context
- [ ] Recommended resolution (if applicable)

### For Unknown Rationale:
- [ ] What decision is unclear
- [ ] What evidence exists
- [ ] What could clarify it
- [ ] Recommendation for recovery

---

## Integration with Review Gates

Knowledge Architect information flows into:

1. **Triad-42 Green phase** — Validate that architectural decisions have been documented
2. **Governance Gateway** — Ensure governance rules are preserved in documentation
3. **Conservation Kernel** — Verify architectural invariants are maintained
4. **TIE handoff** — Feed architectural context into typed handoff

---

## Routing Decision Tree

```
Does this work involve:
├─ Removing, replacing, or modifying functionality? → YES → Knowledge Architect
├─ Changing interfaces or contracts? → YES → Knowledge Architect
├─ Affecting module relationships? → YES → Knowledge Architect
├─ Changing governance or authority? → YES → Knowledge Architect
├─ Connecting new systems? → YES → Knowledge Architect
├─ Unknown historical rationale? → YES → Knowledge Architect
├─ Contradictory documentation? → YES → Knowledge Architect
├─ Design alternatives? → YES → Knowledge Architect
├─ Multiple specialist domains? → YES → Knowledge Architect
└─ None of above → Knowledge Architect optional (recommended for all work)
```

**Note:** Knowledge Architect is optional for simple, isolated feature additions that do not affect existing interfaces, governance, or system design. However, even isolated work benefits from documentation, so escalation is recommended when in doubt.

---

## Knowledge Architect Responsibilities During Routing

1. **Before work begins:** Capture current state and context
2. **During work:** Track decisions and rationale
3. **After work:** Document change, impact, and historical context
4. **Continuously:** Identify contradictions, gaps, and missing rationale

---

## Non-Blocking Nature

**Important:** Knowledge Architect escalation does not block work completion.

- Knowledge Architect documents in parallel with specialist work
- Knowledge Architect does not have authority to approve/reject work
- Knowledge Architect does not have authority to authorize deletions
- Knowledge Architect preserves knowledge; it does not make decisions

**Exception:** If Knowledge Architect identifies a governance violation or security issue, escalation to CCC or Security & Governance Auditor is required (but still non-blocking).
