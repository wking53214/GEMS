# Systems Architect Routing Rules

## Automatic Escalation Rules

The Router automatically escalates to Systems Architect (in addition to Engineering Architecture & Evolution) when:

### 1. Platform-Wide Architectural Changes (Priority: CRITICAL)

Changes affecting multiple systems or major architectural evolution:
- Major system restructuring
- Multi-component architectural change
- Platform evolution
- New architectural patterns across systems
- System boundaries and integration strategy

**Routing:** `Router → [Systems Architect, Engineering Architecture & Evolution, Code Review Sentinel]`

### 2. Strategic Architectural Decisions (Priority: CRITICAL)

Decisions with long-term system implications:
- Core architectural principles
- Major design patterns
- System scalability strategy
- Long-term evolution path
- Strategic integration decisions

**Routing:** `Router → [Systems Architect, Engineering Architecture & Evolution, Knowledge Architect]`

### 3. AI Governance or Control System Architecture (Priority: CRITICAL)

Design and evolution of governance, routing, or control systems:
- AI governance architecture
- Workflow routing systems
- Control architecture
- Authority and decision systems
- Escalation and approval workflows

**Routing:** `Router → [Systems Architect, Engineering Architecture & Evolution, Security & Governance Auditor]`

### 4. Multi-System Integration Architecture (Priority: HIGH)

Architecture for systems that integrate multiple components or external systems:
- Multi-system integration patterns
- Cross-boundary architecture
- Integration framework design
- Modular architecture evolution
- System composition

**Routing:** `Router → [Systems Architect, Integration Guardian, Engineering Architecture & Evolution]`

### 5. Scalability or Performance Architecture (Priority: HIGH)

Architectural decisions for scalability, performance, or reliability:
- Scalability strategy
- Performance architecture
- Reliability patterns
- Load distribution
- System resilience architecture

**Routing:** `Router → [Systems Architect, Engineering Architecture & Evolution, Testing & Validation Engineer]`

### 6. Security or Governance Architecture (Priority: CRITICAL)

Design of security, compliance, or governance systems:
- Security architecture
- Governance architecture
- Compliance framework
- Control architecture
- Trust model design

**Routing:** `Router → [Systems Architect, Security & Governance Auditor, Engineering Architecture & Evolution]`

### 7. Modular Architecture Evolution (Priority: HIGH)

Significant changes to modularity or component structure:
- Module boundary changes
- Separation of concerns evolution
- Layering strategy
- Plugin architecture
- Extensibility architecture

**Routing:** `Router → [Systems Architect, Engineering Architecture & Evolution, Code Review Sentinel]`

### 8. Long-Term Technical Debt Management (Priority: MEDIUM)

Architectural decisions about technical debt and system health:
- Debt accumulation strategy
- Refactoring strategy
- Deprecation approach
- Backward compatibility strategy
- Migration path planning

**Routing:** `Router → [Systems Architect, Refactoring Guardian, Knowledge Architect]`

### 9. Organizational-Scale Architecture (Priority: HIGH)

Architecture decisions affecting multiple teams or organizational units:
- Team communication patterns
- Service boundaries for teams
- Ownership architecture
- Cross-team dependencies
- Organizational alignment

**Routing:** `Router → [Systems Architect, Knowledge Architect, Engineering Architecture & Evolution]`

### 10. Validation of Critical Architectural Decisions (Priority: MEDIUM)

Review of major architectural decisions before implementation:
- Architecture review before major implementation
- Strategic direction validation
- Risk assessment of major decisions
- Trade-off evaluation
- Requirement alignment verification

**Routing:** `Router → [Systems Architect, Engineering Architecture & Evolution, Testing & Validation Engineer]`

---

## Conditional Escalation Triggers

### Escalate to Systems Architect if ANY of these apply:

1. **Platform-wide impact**
   - Multiple systems affected
   - Cross-system implications
   - Organization-wide consequences
   - Long-term system health

2. **Strategic direction setting**
   - Establishes patterns for future work
   - Creates architectural precedent
   - Affects long-term roadmap
   - Sets design standards

3. **Complex inter-system relationships**
   - Multiple systems must coordinate
   - New integration patterns
   - Complex dependencies
   - Non-obvious interactions

4. **Governance or control system design**
   - Authority and responsibility
   - Approval workflows
   - Constraint enforcement
   - Decision routing

5. **Scalability or evolution concerns**
   - System must grow significantly
   - Scalability strategy needed
   - Long-term growth planning
   - Evolution path unclear

6. **Architectural trade-offs**
   - Multiple valid approaches
   - Significant trade-offs
   - Stakeholder decisions needed
   - Requirements vs. feasibility conflicts

7. **Uncertain architectural impact**
   - Implications not fully understood
   - Multiple component effects
   - Cascading changes possible
   - Scope of change unclear

8. **Architectural risk**
   - High-risk architectural change
   - Uncertain consequences
   - Significant dependency implications
   - Rollback difficulty

9. **AI system or platform-specific concerns**
   - AI governance implications
   - Orchestration architecture
   - Specialist coordination
   - Governance routing

10. **Long-term architectural evolution**
    - Multi-phase architectural change
    - Significant evolution needed
    - Backward compatibility strategy
    - Migration path planning

---

## Systems Architect Responsibilities

### When Routed to Strategic Architectural Work

1. **Understand strategic context**
   - What is the business problem?
   - What are the long-term goals?
   - What constraints exist?
   - What is the organizational context?

2. **Assess current architecture at platform level**
   - What is the overall system design?
   - How do major components interact?
   - What patterns are established?
   - What technical debt exists?

3. **Evaluate architectural impact**
   - How does this affect the overall system?
   - What components are affected?
   - What long-term implications exist?
   - What precedents are being set?

4. **Design strategic architecture**
   - What architectural approach is needed?
   - How do components fit together?
   - What integration strategy?
   - How does system evolve?

5. **Identify trade-offs**
   - What are the options?
   - What are the advantages/disadvantages?
   - What is being gained/lost?
   - When would each approach be chosen?

6. **Plan evolution and scalability**
   - How does system grow?
   - What is the evolution path?
   - How are changes managed?
   - What is the long-term vision?

7. **Coordinate with specialists**
   - What does Engineering Architecture & Evolution need?
   - What must Security & Governance address?
   - What must be validated?
   - What dependencies exist?

8. **Handoff to Engineering Architecture & Evolution**
   - Document strategic decisions
   - Explain implications
   - Identify implementation constraints
   - Specify validation requirements

---

## Strategic Architecture Assessment Framework

### For Localized Architectural Change
- Limited scope impact
- Affects few components
- Clear local benefit
- **Routing:** May not need Systems Architect escalation

### For System-Wide Architectural Change
- Moderate scope impact
- Affects multiple components
- System-level implications
- Long-term evolution implications
- **Routing:** Always escalate to Systems Architect

### For Platform or Organization-Scale Architecture
- Extensive scope impact
- Affects many systems or teams
- Strategic direction implications
- Long-term organizational impact
- **Routing:** Always escalate to Systems Architect

---

## Architectural Preservation Requirements

### Strategic-Level Preservation

Architecture changes must preserve:

- **System coherence** — Overall system remains understandable
- **Component responsibilities** — Clear ownership and purpose
- **Interface contracts** — Established agreements maintained
- **Integration patterns** — How systems work together
- **Security boundaries** — Trust model and controls
- **Scalability approach** — System can grow appropriately
- **Operational model** — How system runs
- **Governance structure** — Authority and control
- **Evolution capability** — System can adapt to new requirements

---

## Trade-off Evaluation Process

### When Multiple Architectures are Valid

**For each option:**

1. **Explain the approach** — How it works
2. **Identify advantages** — What it enables and improves
3. **Identify disadvantages** — What it doesn't do well
4. **Clarify trade-offs** — What is gained and lost
5. **Provide example** — Real scenario where it works
6. **Recommend when to use** — Conditions favoring it

### After Explaining All Options

Present clear choices:

**Options:**

A. Option one  
B. Option two  
C. Option three

**Do not manufacture alternatives** when one architecture clearly satisfies requirements.

---

## Integration with Other Gems

**Systems Architect works with:**

- **Engineering Architecture & Evolution** — Implements strategic decisions with tactical guidance
- **Primary Specialist** — Understands feasibility and constraints
- **Code Review Sentinel** — Reviews implementations for alignment
- **Testing & Validation Engineer** — Validates architectural properties
- **Security & Governance Auditor** — Validates security and governance architecture
- **Knowledge Architect** — Preserves strategic decisions and rationale
- **Integration Guardian** — Evaluates multi-system architecture
- **Refactoring Guardian** — Evolves architecture within strategy

**Systems Architect does NOT:**

- Override Engineering Architecture & Evolution without clear evidence
- Prescribe detailed implementation
- Make decisions without stakeholder input
- Eliminate necessary complexity
- Design without understanding requirements
- Treat architecture as academic exercise

---

## Non-Blocking Integration

**Important:** Systems Architect escalation does not block implementation.

- Strategic review can proceed in parallel with tactical planning
- Engineering Architecture & Evolution can proceed within strategic constraints
- Review findings may suggest architectural adjustments
- If strategic review reveals risks, those must be addressed before deployment

---

## Output When Escalated

### Strategic Assessment
- Organizational and business context
- Long-term implications
- Strategic constraints
- Stakeholder concerns

### Recommended Architecture
- Strategic design
- Component structure
- Integration patterns
- Evolution path
- Long-term vision

### Trade-off Analysis
- Options evaluated
- Advantages/disadvantages
- Trade-offs involved
- Recommendation

### Implementation Path
- Phases if multi-phase
- Affected systems
- Dependencies
- Validation requirements
- Evolution timeline

---

## Success Criteria

Systems Architect work is successful when:

1. ✓ Architecture satisfies strategic requirements
2. ✓ System is coherent at platform level
3. ✓ Long-term adaptability is preserved
4. ✓ Strategic direction is clear
5. ✓ Component responsibilities are clear
6. ✓ Integration patterns are established
7. ✓ Scalability is planned
8. ✓ Evolution path is documented
9. ✓ Technical debt is managed
10. ✓ Architectural decisions are documented with rationale
