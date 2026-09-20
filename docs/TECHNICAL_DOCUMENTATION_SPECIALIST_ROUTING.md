# Technical Documentation Specialist Routing Rules

## Automatic Escalation Rules

The Router automatically escalates to Technical Documentation Specialist (in addition to primary specialist) when:

### 1. Public API or Interface Changes (Priority: HIGH)

- New public interfaces created
- Existing interfaces modified
- Interfaces deprecated
- Interface contracts changing
- Breaking changes to signatures

**Routing:** `Router → [Primary Specialist, Technical Documentation Specialist, Knowledge Architect]`

### 2. Architecture Documentation (Priority: HIGH)

- System architecture changes
- Major design changes
- New major components
- Changed component relationships
- New external dependencies

**Routing:** `Router → [Engineering Architecture & Evolution, Technical Documentation Specialist, Knowledge Architect]`

### 3. README or Getting Started Docs (Priority: MEDIUM)

- Project setup changes
- Installation procedure changes
- Configuration options added/removed/changed
- First-time user experience changes
- Dependency updates that affect users

**Routing:** `Router → [Primary Specialist, Technical Documentation Specialist]`

### 4. Feature Documentation (Priority: MEDIUM)

- New features added
- Feature behavior changed
- New configuration options
- New capabilities exposed
- Feature removal

**Routing:** `Router → [Primary Specialist, Technical Documentation Specialist]`

### 5. Developer Documentation (Priority: MEDIUM)

- Code structure changes
- Development workflow changes
- Extension points added/removed
- Build or test process changes
- Development environment setup changes

**Routing:** `Router → [Primary Specialist, Technical Documentation Specialist]`

### 6. Troubleshooting or Operations (Priority: MEDIUM)

- Known failure modes discovered
- Common errors and resolutions
- Operational procedures changed
- Configuration pitfalls identified
- Performance characteristics change

**Routing:** `Router → [Primary Specialist, Technical Documentation Specialist]`

### 7. Complex Decision Documentation (Priority: MEDIUM)

When a decision has complex tradeoffs, alternatives, or constraints:
- Document the decision comprehensively
- Explain why alternatives were rejected
- Preserve the rationale for future reference

**Routing:** `Router → [Primary Specialist, Technical Documentation Specialist, Knowledge Architect]`

### 8. Documentation/Implementation Drift Discovery (Priority: HIGH)

When documentation contradicts implementation:
- Identify the contradiction
- Determine which is authoritative
- Update as needed
- Preserve the reason for the discrepancy

**Routing:** `Router → [Primary Specialist, Technical Documentation Specialist, Knowledge Architect]`

### 9. Security, Governance, or Authority Documentation (Priority: HIGH)

- Security decisions that affect users
- Governance rules that affect operations
- Authority boundaries
- Permission or access control changes

**Routing:** `Router → [Security & Governance Auditor, Technical Documentation Specialist, Knowledge Architect]`

### 10. Integration with Other Systems (Priority: MEDIUM)

- New system integration
- Changed integration points
- New external APIs used
- Changed dependencies

**Routing:** `Router → [Integration Guardian, Technical Documentation Specialist]`

---

## Conditional Escalation Triggers

### Escalate to Technical Documentation Specialist if ANY of these apply:

1. **Change affects how users interact with the system**
   - Users need to understand this change
   - Documentation must be updated

2. **Change removes capability or functionality**
   - Users affected by removal must be informed
   - Migration path should be documented

3. **Change introduces new terminology**
   - New terms must be defined consistently
   - Terminology guide should be updated

4. **Behavior changes in non-obvious ways**
   - Users might misunderstand the new behavior
   - Examples or explanation needed

5. **Performance characteristics change**
   - Users care about performance implications
   - Documentation should reflect new characteristics

6. **Error messages or failures change**
   - Troubleshooting documentation affected
   - New error handling documentation needed

7. **Configuration options change**
   - Configuration guide must be updated
   - Examples may need adjustment

8. **Development workflow changes**
   - Contributor documentation must be updated
   - New developers affected

9. **Dependencies or setup changes**
   - Installation/setup documentation affected
   - Getting started guide needs update

10. **Contradictions discovered**
    - Documentation contradicts implementation
    - Requires investigation and update

---

## Technical Documentation Specialist Responsibilities

### When Routed to Documentation Work

1. **Analyze the change**
   - What is changing?
   - Who needs to know about it?
   - What questions might they have?

2. **Identify documentation needs**
   - What documentation should be created or updated?
   - What examples are needed?
   - What terminology must be explained?

3. **Audit existing documentation**
   - Is related documentation stale?
   - Are there contradictions with current docs?
   - What documentation exists but is outdated?

4. **Create or update documentation**
   - Write clear, accurate documentation
   - Include examples where helpful
   - Follow established structure and terminology

5. **Identify for Knowledge Architect**
   - What knowledge should be preserved?
   - What decisions underlie this change?
   - What should future systems understand?

6. **Escalate contradictions**
   - If documentation contradicts implementation, escalate to Knowledge Architect
   - Do not guess what is correct
   - Identify evidence for both positions

---

## Documentation Audit Process

When auditing documentation, identify and document:

### Content Issues
- **Missing information** — What should be there but isn't?
- **Outdated sections** — What is no longer accurate?
- **Contradictions** — What statements conflict with each other or with implementation?
- **Inaccurate statements** — What is factually wrong?
- **Unclear explanations** — What is confusing?

### Knowledge Issues
- **Undocumented assumptions** — What is assumed but not stated?
- **Terminology inconsistencies** — Are terms used consistently?
- **Missing rationale** — Why is something done this way?
- **Usability problems** — Is information easy to find?

### Synchronization Issues
- **Documentation/implementation drift** — Does documentation match implementation?
- **Removed but documented capabilities** — What no longer exists?
- **Implemented but undocumented capabilities** — What exists but isn't documented?
- **Incorrect interfaces or workflows** — Are examples wrong?
- **Stale configuration** — Are examples out of date?
- **Outdated dependencies** — Do examples use old versions?

### Report Format

For each significant issue provide:

**Issue:** What is wrong.

**Evidence:** Quote, reference, or location.

**Impact:** Why it matters. Who is affected? What could break?

**Recommendation:** What should change.

**Priority:** High / Medium / Low.

---

## Integration with Knowledge Architect

**Technical Documentation Specialist escalates to Knowledge Architect when:**

1. Documentation contradicts implementation and authoritative source is unclear
2. Reason for a documented decision is unknown
3. Historical context is missing
4. Assumption vs. fact is unclear
5. Important knowledge might be lost
6. Change reverses a previous documented decision

**Knowledge Architect escalates to Technical Documentation Specialist:**

1. When knowledge should be documented
2. When documentation needs to be created or updated
3. When documentation structure needs improvement
4. When documentation should be audited for drift

---

## Default Output When Documentation Escalated

### Purpose
- What documentation is needed
- Why it is needed
- Who is the audience

### Current Knowledge
- What is confirmed
- What is assumed
- What is unknown

### Structure
- Recommended documentation organization
- Sections needed
- Integration with existing documentation

### Audit Results (if applicable)
- Documentation issues found
- Contradictions identified
- Gaps discovered
- Recommendations for improvement

### Draft Documentation
- Documentation content
- Examples
- Diagrams if needed

### Knowledge Preservation
- Decisions documented
- Rationale preserved
- Constraints captured
- Dependencies noted
- Lessons learned recorded

### Validation
- Accuracy review
- Completeness check
- Consistency verification
- Usability assessment

---

## Non-Blocking Integration

**Important:** Technical Documentation Specialist escalation does not block work completion.

- Documentation is created in parallel with specialist work
- Documentation should be timely but does not delay feature completion
- Documentation can be updated incrementally as implementation becomes stable

**Exception:** If documentation contradicts implementation and authoritative source is genuinely unclear, escalation to Knowledge Architect is required before documenting (but still non-blocking to implementation).

---

## Collaboration Model with Knowledge Architect

```
PRIMARY SPECIALIST
    ↓
MAKES DECISION
    ↓
┌───────────────────────────────┐
│  Routes to:                   │
│  - Knowledge Architect        │
│  - Technical Documentation    │
│    Specialist                 │
└───────────────────────────────┘
    ↓                        ↓
KNOWLEDGE ARCHITECT      TECHNICAL DOCUMENTATION
    ↓                        SPECIALIST
Preserves:                   ↓
- Rationale           Creates:
- Context             - Documentation
- History             - Examples
- Constraints         - Architecture diagrams
- Assumptions         - README updates
- Lessons learned     - Troubleshooting guides
    ↓                        ↓
    └───────────────────────┬──────────────────────┘
                            ↓
                    DOCUMENTED KNOWLEDGE
                    + PRESERVED RATIONALE
```

---

## Success Criteria

Technical Documentation Specialist work is successful when:

1. ✓ Documentation accurately reflects implementation
2. ✓ Intended audience can understand the change
3. ✓ Examples work and are appropriate
4. ✓ Rationale for decisions is preserved
5. ✓ Contradictions with existing documentation are resolved
6. ✓ Terminology is consistent
7. ✓ Documentation is easy to find and navigate
8. ✓ Future developers can understand from documentation alone
9. ✓ AI systems can understand the system intent from documentation
10. ✓ Documentation remains useful and accurate 6+ months later
