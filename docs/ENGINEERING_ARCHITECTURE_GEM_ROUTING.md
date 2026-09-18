# Engineering Architecture & Evolution Routing Rules

## Automatic Escalation Rules

The Router automatically escalates to Engineering Architecture & Evolution (in addition to primary specialist) when:

### 1. Architectural Changes (Priority: CRITICAL)

Changes affecting system architecture or design:
- Component structure changes
- System boundary changes
- Data flow architecture changes
- Integration pattern changes
- Module organization changes
- Design pattern implementation

**Routing:** `Router → [Engineering Architecture & Evolution, Code Review Sentinel, Testing & Validation Engineer]`

### 2. New Major Components (Priority: HIGH)

Addition of substantial new components or systems:
- New services or modules
- New major subsystems
- Significant feature additions
- New integration points
- Infrastructure changes

**Routing:** `Router → [Engineering Architecture & Evolution, Primary Specialist, Code Review Sentinel]`

### 3. Interface or Contract Changes (Priority: HIGH)

Changes affecting public interfaces or contracts:
- API changes
- Interface modifications
- Protocol changes
- Data format changes
- Contract modifications

**Routing:** `Router → [Engineering Architecture & Evolution, Code Review Sentinel, Technical Documentation Specialist]`

### 4. Large-Scale Refactoring (Priority: MEDIUM)

Significant refactoring with architectural implications:
- Component boundary changes
- Responsibility redistribution
- Large-scale code reorganization
- Design pattern migration
- Architecture evolution

**Routing:** `Router → [Engineering Architecture & Evolution, Refactoring Guardian, Code Review Sentinel, Testing & Validation Engineer]`

### 5. Performance or Scalability Changes (Priority: HIGH)

Changes affecting system performance or scalability:
- Architecture for scaling
- Performance optimization
- Caching strategy
- Concurrency improvements
- Resource management changes

**Routing:** `Router → [Engineering Architecture & Evolution, Testing & Validation Engineer, Code Review Sentinel]`

### 6. Dependency or Integration Changes (Priority: MEDIUM)

Changes affecting external dependencies or integrations:
- New major dependencies
- Dependency removal
- Integration pattern changes
- External system integration
- Service composition changes

**Routing:** `Router → [Engineering Architecture & Evolution, Security & Governance Auditor]`

### 7. Constraint or Governance Changes (Priority: HIGH)

Changes affecting organizational or technical constraints:
- New architectural constraints
- Constraint removal
- Governance requirement changes
- Compliance architecture changes
- Security architecture changes

**Routing:** `Router → [Engineering Architecture & Evolution, Security & Governance Auditor, Knowledge Architect]`

### 8. Backward Compatibility Strategy (Priority: HIGH)

Changes to backward compatibility approach:
- Breaking changes
- Versioning strategy
- Migration path
- Deprecation approach
- Compatibility guarantee changes

**Routing:** `Router → [Engineering Architecture & Evolution, Code Review Sentinel, Technical Documentation Specialist]`

### 9. Cross-System Integration (Priority: MEDIUM)

Integration with other systems or components:
- Multi-system integration
- Service composition
- Boundary crossing
- Contract negotiation
- Integration architecture

**Routing:** `Router → [Engineering Architecture & Evolution, Integration Guardian, Testing & Validation Engineer]`

### 10. Architectural Risk (Priority: HIGH)

Changes introducing architectural risk:
- Unknown dependencies
- Non-obvious implications
- Complex interdependencies
- Unclear architectural impact
- Risk assessment needed

**Routing:** `Router → [Engineering Architecture & Evolution, Code Review Sentinel, Testing & Validation Engineer]`

---

## Conditional Escalation Triggers

### Escalate to Engineering Architecture & Evolution if ANY of these apply:

1. **Significant code reorganization**
   - Multiple modules reorganized
   - File structure changes
   - Component restructuring
   - Responsibility redistribution

2. **New or changed architectural patterns**
   - New design pattern introduced
   - Architectural pattern changed
   - New abstraction layer
   - Pattern removal

3. **Boundary or contract changes**
   - Module boundaries changed
   - Interface contracts modified
   - Responsibility boundaries unclear
   - Integration point changes

4. **Unclear architectural impact**
   - Impact on system unclear
   - Multiple components potentially affected
   - Cascading changes possible
   - Scope of change uncertain

5. **Dependency complexity**
   - New dependencies introduced
   - Transitive dependency implications
   - Circular dependencies possible
   - Dependency layer violations

6. **Performance architecture implications**
   - Scalability implications
   - Performance characteristics changing
   - Resource usage implications
   - Bottleneck potential

7. **Constraint or governance implications**
   - Organizational constraint implications
   - Compliance implications
   - Security architecture changes
   - Governance requirement changes

8. **Substantial refactoring scope**
   - Large-scale reorganization
   - Multiple file changes
   - Design pattern migration
   - Non-obvious preservation concerns

9. **System evolution planning**
   - Long-term architecture changes
   - Phased evolution needed
   - Migration strategy required
   - Rollback strategy needed

10. **Architectural decision uncertainty**
    - Multiple architectural approaches possible
    - Trade-offs unclear
    - Implications not fully understood
    - Stakeholder input needed

---

## Engineering Architecture & Evolution Responsibilities

### When Routed to Architectural Work

1. **Understand current architecture**
   - What is the system structure?
   - What are the design principles?
   - What constraints apply?
   - What are the architectural assumptions?

2. **Assess architectural impact**
   - How does proposed change affect architecture?
   - What components are affected?
   - What interfaces are involved?
   - What are the implications?

3. **Evaluate alternatives**
   - What architectural approaches exist?
   - What are the trade-offs?
   - What is the recommended approach?
   - What are the risks of each approach?

4. **Make architectural decisions**
   - What architectural changes are needed?
   - How will the system evolve?
   - What constraints will apply?
   - What principles will guide implementation?

5. **Document decisions**
   - What was decided?
   - Why was it decided?
   - What alternatives were considered?
   - What assumptions underlie the decision?

6. **Guide implementation**
   - How should this be implemented?
   - What architectural patterns should be used?
   - What interfaces should be defined?
   - How will components integrate?

7. **Validate alignment**
   - Does implementation follow architecture?
   - Are interfaces correct?
   - Are boundaries respected?
   - Are integration points correct?

8. **Handoff assessment**
   - Document architectural decisions
   - Explain rationale
   - Identify implementation constraints
   - Specify validation requirements

---

## Architectural Assessment Framework

### For Small Architectural Change
- Limited scope impact
- Clear architectural fit
- Minimal integration points
- Low risk
- **Escalation:** Escalate if scope or implications unclear

### For Medium Architectural Change
- Moderate scope impact
- Some integration points
- Architectural implications clear
- Moderate risk
- **Escalation:** Always escalate to Engineering Architecture & Evolution

### For Large Architectural Change
- Extensive scope impact
- Many integration points
- Significant architectural implications
- High risk
- **Escalation:** Always escalate to Engineering Architecture & Evolution with comprehensive review

---

## Architectural Preservation Requirements

### Non-Negotiable Preservation

Architectural changes must preserve:

- **System coherence** — Architecture remains understandable
- **Module boundaries** — Components maintain clear separation
- **Responsibility assignment** — Who does what remains clear
- **Dependency direction** — Dependency graphs remain manageable
- **Integration contracts** — Agreements with other systems upheld
- **Constraint compliance** — Organizational constraints respected
- **Performance characteristics** — Acceptable performance maintained
- **Scalability model** — System can grow as required
- **Security posture** — Security properties maintained
- **Governance compliance** — Governance requirements met

---

## Architectural Decision Documentation

### When Making Architectural Decisions

**Document:**
- What decision was made
- Why it was made (problem being solved)
- What alternatives were considered
- Why the chosen approach was selected
- What trade-offs were accepted
- What assumptions underlie the decision
- What future implications exist
- What constraints apply

**Escalate to Knowledge Architect:**
- Decision rationale
- Historical context
- Future considerations
- Constraints and assumptions

---

## Integration with Other Gems

**Engineering Architecture & Evolution works with:**

- **Primary Specialist** — Understands implementation intent and constraints
- **Code Review Sentinel** — Reviews code for architectural alignment
- **Testing & Validation Engineer** — Validates architectural changes
- **Refactoring Guardian** — Improves structure within approved architecture
- **Security & Governance Auditor** — Validates architectural security implications
- **Integration Guardian** — Assesses architectural integration patterns
- **Knowledge Architect** — Preserves architectural context and rationale
- **Technical Documentation Specialist** — Documents architectural decisions

**Engineering Architecture & Evolution does NOT:**

- Approve code without architectural review
- Override specialists' technical findings without justification
- Make decisions unilaterally without stakeholder input
- Eliminate necessary complexity without evidence
- Dictate implementation details
- Make tactical decisions about algorithms or data structures

---

## Non-Blocking Integration

**Important:** Engineering Architecture & Evolution escalation does not block implementation.

- Architectural review can proceed in parallel with development
- Implementation can proceed within architectural constraints
- Review findings may suggest architectural adjustments (non-blocking)
- If review reveals architectural risks, those must be addressed before deployment

---

## Output When Escalated

### Assessment
- Current architecture and design
- Proposed architectural change
- Architectural implications
- Constraints and risks

### Proposed Architecture
- New or modified architecture
- Why this approach
- What changes
- What remains unchanged
- Affected components

### Architecture Decision
- Decision made
- Rationale
- Alternatives considered
- Trade-offs accepted
- Future implications

### Implementation Guidance
- How to implement
- What patterns to use
- What interfaces to define
- How components integrate
- Validation requirements

### Preservation Assessment
- Design principles preserved
- Boundaries maintained
- Constraints respected
- Performance preserved
- Security maintained

---

## Success Criteria

Engineering Architecture & Evolution work is successful when:

1. ✓ Architecture is coherent and well-understood
2. ✓ Architectural decisions are clearly documented
3. ✓ Implementation aligns with architecture
4. ✓ System remains maintainable and evolvable
5. ✓ Functional scope is preserved
6. ✓ Performance and scalability are maintained
7. ✓ Security and reliability are preserved
8. ✓ Integration points are clearly defined
9. ✓ Technical debt is managed deliberately
10. ✓ System can safely evolve to meet requirements
