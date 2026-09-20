# Testing & Validation Engineer Routing Rules

## Automatic Escalation Rules

The Router automatically escalates to Testing & Validation Engineer (in addition to primary specialist) when:

### 1. Code Changes (Priority: HIGH)

Any change to implementation code:
- Bug fixes
- Feature implementations
- Performance optimizations
- Refactoring with behavioral changes
- Dependency updates

**Routing:** `Router → [Primary Specialist, Testing & Validation Engineer]`

### 2. Baseline Changes (Priority: HIGH)

When a baseline exists and it's being modified:
- Expected behavior changes
- Interface contracts change
- API signatures change
- Configuration defaults change

**Routing:** `Router → [Primary Specialist, Testing & Validation Engineer, Knowledge Architect]`

### 3. Critical Path Changes (Priority: HIGH)

Changes affecting critical or high-risk behaviors:
- Security-related code
- Data integrity logic
- Error handling
- Resource management
- Concurrency or synchronization

**Routing:** `Router → [Security & Governance Auditor, Testing & Validation Engineer]`

### 4. Architectural Changes (Priority: HIGH)

Changes to system architecture or design:
- Component interfaces
- System boundaries
- Data flows
- Trust or control relationships

**Routing:** `Router → [Engineering Architecture & Evolution, Testing & Validation Engineer]`

### 5. Integration Changes (Priority: MEDIUM)

Changes to integration points or inter-component communication:
- New component connections
- Changed interaction protocols
- Dependency changes
- Handoff modifications

**Routing:** `Router → [Integration Guardian, Testing & Validation Engineer]`

### 6. Test Suite Changes (Priority: HIGH)

Changes to test infrastructure:
- Test framework updates
- Test suite modifications
- Test environment changes
- Coverage-critical test additions/removals

**Routing:** `Router → [Testing & Validation Engineer]`

### 7. Regression Risk (Priority: HIGH)

When a change could affect existing functionality:
- Changes near untested code
- Changes affecting shared utilities
- Changes to widely-used interfaces
- Changes that touch many files

**Routing:** `Router → [Primary Specialist, Testing & Validation Engineer]`

### 8. Deletion or Removal (Priority: MEDIUM)

When code, tests, or features are being removed:
- Code removal
- Test removal
- Feature deprecation
- Component removal

**Routing:** `Router → [Testing & Validation Engineer, Alpha Deletion Demon]`

Note: Final deletion authority goes through Omega Deletion Demon.

### 9. Performance or Resource Changes (Priority: MEDIUM)

Changes affecting system performance or resource usage:
- Optimization
- Resource allocation
- Concurrency improvements
- Memory/CPU/I/O implications

**Routing:** `Router → [Primary Specialist, Testing & Validation Engineer]`

### 10. Security or Governance Changes (Priority: HIGH)

Changes affecting security or governance:
- Authentication/authorization changes
- Encryption approach changes
- Governance boundary changes
- Authority changes

**Routing:** `Router → [Security & Governance Auditor, Testing & Validation Engineer]`

---

## Conditional Escalation Triggers

### Escalate to Testing & Validation Engineer if ANY of these apply:

1. **Change is more complex than typical**
   - Multiple components affected
   - Non-obvious impact paths
   - High risk of unintended effects

2. **Change modifies untested or weakly tested code**
   - Existing tests are insufficient
   - Code coverage is low
   - Previous bugs in this area

3. **Change could break edge cases**
   - Edge case handling could be affected
   - Boundary conditions changed
   - Error paths affected

4. **Change affects error handling**
   - Exception handling modified
   - Error messages changed
   - Recovery behavior modified

5. **Change has environmental implications**
   - Behavior depends on external factors
   - Configuration sensitive
   - Timing or concurrency implications

6. **Change touches third-party interfaces**
   - External API calls modified
   - Library behavior assumptions changed
   - Version compatibility affected

7. **Integration point uncertainty**
   - Impact on callers is unclear
   - Integration testing coverage is weak
   - Dependency behavior could change

8. **High-risk area**
   - Security-sensitive code
   - Data integrity code
   - Shared utility code
   - Performance-critical code

9. **Deletion candidate without clear replacement**
   - Code appears unused
   - Test appears redundant
   - Component appears dead
   - Migration path unclear

10. **Test failure investigation needed**
    - Tests fail after the change
    - Test failure root cause unclear
    - Multiple tests affected
    - Test failure could indicate real problem

---

## Validation Strategy Decisions

### For Small, Low-Risk Changes

**Typical validation:**
- Smoke tests (basic functionality works)
- Existing test suite runs
- Manual spot-check of changed area
- No new test development required

**Escalation rule:** Can proceed with Primary Specialist validation alone

### For Medium-Risk Changes

**Typical validation:**
- Targeted unit tests for changes
- Integration tests with dependent components
- Existing test suite runs
- Regression testing of related areas
- New tests may be needed

**Escalation rule:** Always escalate to Testing & Validation Engineer

### For High-Risk Changes

**Typical validation:**
- Comprehensive unit tests
- Integration tests across system
- End-to-end tests
- Regression testing (full suite)
- Security/governance validation if applicable
- Performance validation if applicable
- Test plan and rationale documented
- Test code reviewed

**Escalation rule:** Always escalate to Testing & Validation Engineer

---

## Test Failure Resolution Process

When tests fail:

1. **Investigate the failure**
   - What test failed?
   - What is the actual failure?
   - Can it be reproduced?

2. **Determine root cause**
   - Is the test wrong?
   - Is the code wrong?
   - Is the environment wrong?

3. **Classify the failure**
   - Real bug found
   - Test environment issue
   - Test framework issue
   - Pre-existing failure

4. **Remediate**
   - Fix the code (if code is wrong)
   - Fix the test (if test is wrong)
   - Fix the environment (if environment is wrong)

5. **Verify resolution**
   - Test passes
   - Related tests pass
   - No new failures introduced

6. **Document the findings**
   - What was wrong
   - How it was fixed
   - What lessons apply

### What NOT to do

**Never recommend:**
- Suppressing a test without understanding why it fails
- Weakening a test to make it pass
- Deleting a test to make the problem go away
- Ignoring failures and hoping they resolve

---

## Baseline Verification

### When validating baseline preservation:

1. **Identify the baseline**
   - What behavior existed before?
   - What test coverage existed?

2. **Identify the change**
   - What is supposed to change?
   - What behavior is intentionally different?

3. **Identify unaffected areas**
   - What behavior should stay the same?
   - What tests should still pass?

4. **Validate the change**
   - Does the change work as intended?
   - Are the new behaviors correct?

5. **Validate preservation**
   - Do baseline tests still pass?
   - Is unaffected behavior unchanged?
   - Are there weak test areas?

6. **Assess completeness**
   - Is test coverage sufficient?
   - Are edge cases covered?
   - Could hidden regressions exist?

### Coverage Audit

When assessing whether baseline is preserved:

- **Direct testing** — Tests that explicitly test the behavior
- **Indirect testing** — Tests that exercise the behavior as side-effect
- **Weak coverage** — Areas with no tests or few tests
- **Integration gaps** — Behaviors not tested in integration

---

## Integration with Code Review and Knowledge Architect

**Code Review Sentinel examines:**
- Code quality
- Adherence to standards
- Readability and maintainability

**Testing & Validation Engineer examines:**
- Test quality and coverage
- Validation strategy appropriateness
- Baseline preservation
- Regression risk

**Knowledge Architect examines:**
- What knowledge should be preserved
- What decisions are documented
- Historical and architectural context

**Collaboration:** All three provide independent perspectives before change acceptance.

---

## Output Format When Escalated

When Testing & Validation Engineer is involved, provide:

### Validation Strategy
- What behaviors need validation
- Why those behaviors matter
- How validation will be performed
- Success criteria

### Baseline Assessment
- What baseline behavior exists
- What changes are intentional
- What behavior should be preserved
- What test coverage exists

### Change Impact Analysis
- What code changed
- What behaviors are affected
- What edge cases could be affected
- What integration points are impacted

### Test Plan
- What tests will be performed
- Why each test is necessary
- Coverage of edge cases
- Integration scenarios

### Risk Assessment
- What could go wrong
- What failure modes are possible
- What regression risks exist
- What remains untested

### Evidence and Recommendations
- What validation was performed
- What evidence was obtained
- Are results sufficient?
- What additional validation is needed
- Recommendation for acceptance or further work

---

## Non-Blocking Nature

**Important:** Testing & Validation Engineer escalation does not block work completion.

- Validation can proceed in parallel with implementation
- Validation findings may suggest implementation changes (non-blocking)
- If validation reveals problems, those must be addressed before acceptance

---

## Success Criteria

Testing & Validation Engineer work is successful when:

1. ✓ Validation approach is proportional to risk
2. ✓ Sufficient evidence exists to accept the change
3. ✓ Baseline behavior is verified preserved
4. ✓ Regression risks are identified
5. ✓ High-risk areas are thoroughly tested
6. ✓ Test failures are understood
7. ✓ Test quality is high
8. ✓ Edge cases and error handling validated
9. ✓ Documentation captures validation approach
10. ✓ Future developers can understand validation decisions
