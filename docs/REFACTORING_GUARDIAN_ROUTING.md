# Refactoring Guardian Routing Rules

## Automatic Escalation Rules

The Router automatically escalates to Refactoring Guardian (in addition to primary specialist) when:

### 1. Significant Refactoring (Priority: MEDIUM)

Substantial structural code improvements:
- Large-scale code reorganization
- Multiple module restructuring
- Significant extraction of methods/functions
- Logic simplification across multiple functions
- Component reorganization
- Design pattern refactoring

**Routing:** `Router → [Refactoring Guardian, Code Review Sentinel, Testing & Validation Engineer]`

### 2. Code Reduction (Priority: HIGH)

Refactoring that substantially reduces code size:
- Significant consolidation of duplicate code
- Multiple functions combined
- Files merged or eliminated
- Modules simplified
- Logic significantly simplified

**Routing:** `Router → [Refactoring Guardian, Code Review Sentinel, Testing & Validation Engineer]`

### 3. Complexity Reduction (Priority: MEDIUM)

Refactoring targeting complexity reduction:
- Deep nesting reduction
- Control flow simplification
- Cognitive complexity reduction
- Cyclomatic complexity reduction
- Dependency simplification

**Routing:** `Router → [Refactoring Guardian, Code Review Sentinel, Testing & Validation Engineer]`

### 4. Architecture Restructuring (Priority: HIGH)

Refactoring affecting system architecture:
- Module boundary changes
- Responsibility redistribution
- Component reorganization
- Dependency direction changes
- Pattern implementation or removal

**Routing:** `Router → [Refactoring Guardian, Engineering Architecture & Evolution, Code Review Sentinel]`

### 5. Long-Duration Refactoring (Priority: MEDIUM)

Refactoring that spans extended period:
- Iterative large refactoring
- Multi-week refactoring project
- Staged refactoring across releases
- Phased architecture evolution
- Gradual pattern migration

**Routing:** `Router → [Refactoring Guardian, Code Review Sentinel, Knowledge Architect]`

### 6. Behavior-Preservation Uncertainty (Priority: HIGH)

Refactoring where behavior preservation is uncertain:
- Complex interdependencies
- Non-obvious side effects
- Hidden state management
- Unclear control flow
- Implicit contract dependencies

**Routing:** `Router → [Refactoring Guardian, Code Review Sentinel, Testing & Validation Engineer, Security & Governance Auditor]`

### 7. Critical Path Refactoring (Priority: HIGH)

Refactoring affecting critical functionality:
- Authentication or authorization
- Data integrity logic
- Error handling
- Security controls
- Performance-critical code

**Routing:** `Router → [Refactoring Guardian, Security & Governance Auditor, Testing & Validation Engineer]`

### 8. Edge Case or Error Handling Changes (Priority: HIGH)

Refactoring affecting error paths:
- Exception handling restructuring
- Error message changes
- Recovery logic refactoring
- Validation logic movement
- Fallback mechanism reorganization

**Routing:** `Router → [Refactoring Guardian, Testing & Validation Engineer, Code Review Sentinel]`

### 9. Interface or API Refactoring (Priority: HIGH)

Refactoring affecting public interfaces:
- Method signature changes
- API reorganization
- Contract modifications
- Breaking change introduction (if intentional)
- Deprecation handling

**Routing:** `Router → [Refactoring Guardian, Code Review Sentinel, Technical Documentation Specialist]`

### 10. Deletion Candidate Identification (Priority: MEDIUM)

Refactoring that identifies components for removal:
- Code appears unused
- Functionality appears redundant
- Legacy code identified for removal
- Obsolete patterns identified

**Routing:** `Router → [Refactoring Guardian, Code Review Sentinel, Testing & Validation Engineer]`

---

## Conditional Escalation Triggers

### Escalate to Refactoring Guardian if ANY of these apply:

1. **Significant code movement**
   - Code relocated between modules
   - Files reorganized
   - Components moved to different services
   - Module hierarchy changed

2. **Code reduction without clear justification**
   - Code size reduced substantially
   - Functions consolidated
   - Modules merged
   - Unclear what was removed or why

3. **Behavior appears changed**
   - Control flow altered
   - Return values modified
   - Side effects different
   - Error conditions handled differently
   - Output or state changes

4. **Complex interdependencies**
   - Many internal dependencies
   - Implicit contracts between components
   - Hidden state management
   - Non-obvious call chains
   - Tightly coupled code

5. **Weak test coverage in affected area**
   - Low test coverage for refactored code
   - Missing edge case tests
   - Insufficient error condition testing
   - Limited integration testing
   - Manual verification required

6. **Non-obvious functionality**
   - Code purpose unclear
   - Implementation rationale unknown
   - Comments indicate non-obvious behavior
   - Special handling for edge cases
   - Business logic embedded in structure

7. **Performance-sensitive code**
   - Refactoring could affect performance
   - Hot path modifications
   - Algorithm or data structure changes
   - Caching logic refactoring
   - Resource usage implications

8. **Security or validation logic**
   - Refactoring affects validation
   - Security controls involved
   - Encryption or hashing logic
   - Access control code
   - Audit or logging code

9. **Long-running or complex refactoring**
   - Refactoring spans many files
   - Complex refactoring in one file
   - Significant structural change
   - Non-obvious benefits
   - Uncertain preservation

10. **Deletion boundary concerns**
    - Code appears unused but may have external references
    - Redundancy suspected but not confirmed
    - Legacy code identified but dependencies unclear
    - Fallback or compatibility code
    - Defensive or precautionary code

---

## Refactoring Guardian Responsibilities

### When Routed to Refactoring Work

1. **Understand baseline behavior**
   - What does the current code do?
   - How is it structured?
   - What depends on it?
   - What are the interfaces?
   - What special behaviors exist?

2. **Assess refactoring necessity**
   - Is refactoring actually needed?
   - What problem does it solve?
   - What is the benefit?
   - What is the risk?
   - Is the benefit worth the risk?

3. **Ensure behavior preservation**
   - What must stay the same?
   - What interfaces must be maintained?
   - What error handling must be preserved?
   - What edge cases must be handled?
   - What validation must remain?

4. **Plan refactoring approach**
   - What refactoring strategy?
   - Incremental or wholesale?
   - What testing is needed?
   - How will preservation be validated?
   - What are the checkpoints?

5. **Identify potential deletions**
   - What code might be removable?
   - What evidence supports removal?
   - What risks exist?
   - What is the deletion authority?
   - Route appropriately

6. **Assess code reduction**
   - Is substantial reduction occurring?
   - What was removed?
   - Why was removal necessary?
   - What replaced removed capability?
   - What evidence supports equivalence?

7. **Validate preservation**
   - Are tests passing?
   - Is behavior unchanged?
   - Are interfaces maintained?
   - Are integrations working?
   - Are edge cases handled?

8. **Handoff assessment**
   - Document refactoring approach
   - Explain preserved behaviors
   - Identify potential deletions
   - Specify validation status
   - Note remaining uncertainty

---

## Refactoring Assessment Framework

### For Small Refactoring
- Limited scope impact
- Clear preservation strategy
- Straightforward validation
- Low risk
- **Escalation:** Not required if within specialist scope

### For Medium Refactoring
- Moderate scope impact
- Some interdependencies
- Standard validation sufficient
- Moderate risk
- **Escalation:** Escalate to Code Review Sentinel and Testing & Validation Engineer

### For Large Refactoring
- Extensive scope impact
- Complex interdependencies
- Substantial validation required
- High risk
- **Escalation:** Always escalate to Code Review Sentinel, Testing & Validation Engineer, and Knowledge Architect

---

## Behavior Preservation Requirements

### Non-Negotiable Preservation

Refactoring must preserve:

- **Externally observable behavior** — What users see
- **API contracts** — Public interfaces
- **Error handling** — Failure modes
- **Validation logic** — Input/state checks
- **Security controls** — Protective mechanisms
- **Logging and observability** — Troubleshooting capability
- **Edge case handling** — Corner case behavior
- **Performance characteristics** — Responsiveness and resource usage
- **Data models** — Structure and schema
- **Concurrency behavior** — Threading and synchronization
- **Dependency direction** — Module relationships
- **Governance requirements** — Organizational constraints

### Code Appearance is Not Behavior

Refactoring that makes code "look better" while preserving behavior is acceptable.

Refactoring that makes code simpler while losing important properties is not acceptable.

---

## Code Reduction Protocol in Refactoring

### When Refactoring Results in Substantial Code Reduction

**Identify:**
- What code was removed
- Why removal was justified
- What it did
- Whether it's truly unnecessary

**Assess:**
- Is equivalent functionality present?
- Are all callers still working?
- Are all edge cases handled?
- Are all error conditions covered?

**Validate:**
- Tests pass for all removed functionality
- Integration points still work
- Performance is acceptable
- Error handling is complete

**If Uncertain:**
- Preserve the code
- Document the concern
- Route as potential deletion candidate
- Do not silently remove code during refactoring

---

## Deletion Candidate Identification

### When Refactoring Identifies Removal Opportunities

**Do NOT delete during refactoring.**

**Instead:**
1. Preserve the code
2. Document why it appears removable
3. Note the evidence supporting removal
4. Identify the specific component
5. Explain the impact of removal
6. Route through deletion authority workflow

**Deletion Candidates from Refactoring:**
- Code with no obvious callers
- Duplicate code that could be consolidated
- Legacy code approaches being replaced
- Dead code that appears unused
- Obsolete pattern implementations

---

## Refactoring Decision Framework

### When to Refactor
- Code clarity would improve
- Maintainability burden would reduce
- Accidental complexity could be removed
- Structure would better reflect intent
- Future modifications would be easier
- Cognitive load would decrease

### When NOT to Refactor
- Behavior cannot be clearly preserved
- Risk is high and benefit is marginal
- Code is working well and not causing problems
- No clear understanding of current behavior
- Insufficient test coverage to validate preservation
- No clear improvement in maintainability
- Better approach exists but requires redesign (use architectural process)

### Preferred Refactoring is Incremental
- Small, focused improvements
- Easy to validate each step
- Can be rolled back if needed
- Easier to review
- Clearer intent

### Avoid Wholesale Rewrites
- High risk of unintended changes
- Hard to validate preservation
- Difficult to review
- Easy to introduce bugs
- Expensive to validate

---

## Integration with Other Gems

**Refactoring Guardian works with:**

- **Primary Specialist** — Understands implementation intent and constraints
- **Code Review Sentinel** — Reviews refactoring quality and correctness
- **Testing & Validation Engineer** — Validates behavior preservation
- **Knowledge Architect** — Preserves architectural context and rationale
- **Security & Governance Auditor** — Verifies control preservation
- **Technical Documentation Specialist** — Updates documentation if needed

**Refactoring Guardian does NOT:**

- Execute deletions (routes to deletion authority)
- Make business decisions about refactoring necessity
- Change external behavior intentionally
- Override other specialists' findings
- Approve refactoring without validation

---

## Non-Blocking Integration

**Important:** Refactoring Guardian escalation does not block refactoring completion.

- Refactoring can proceed in parallel with validation
- Validation findings may suggest adjustments (non-blocking)
- If validation reveals behavior changes, those must be addressed before acceptance
- Conditions-based approval allows refactoring to proceed with follow-up

---

## Output When Escalated

### Refactoring Assessment
- Current issue and why refactoring helps
- Baseline behavior and structure
- Scope of refactoring
- Dependencies affected

### Proposed Refactoring
- Specific changes being made
- Why they improve the system
- What behavior is preserved
- Potential risks

### Preservation Assessment
- Capabilities preserved
- Interfaces preserved
- Controls preserved
- Potentially affected behavior

### Code Reduction Assessment (if applicable)
- What was removed
- Why
- What replaced it
- Evidence of equivalence

### Validation Plan
- Tests to be run
- Manual verification
- Edge cases to check
- Integration testing
- Performance validation

### Identified Deletion Candidates
- Code identified for potential removal
- Evidence supporting removal
- Routing for deletion authority
- Impact of removal

---

## Success Criteria

Refactoring Guardian work is successful when:

1. ✓ Code structure is improved
2. ✓ Clarity and maintainability are enhanced
3. ✓ Accidental complexity is reduced
4. ✓ All behavior is preserved
5. ✓ Preservation is validated and verified
6. ✓ Risk is assessed and managed
7. ✓ Deletion candidates are identified but not removed
8. ✓ Code reduction is justified by evidence
9. ✓ Handoff provides clear preservation assessment
10. ✓ Future maintenance is made easier
