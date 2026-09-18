# BP (Banana Peel) Routing Rules

## Automatic Escalation Rules

The Router automatically escalates to BP (Banana Peel) when:

### 1. Post-Workflow Chaos Testing (Priority: HIGH)

Work that has completed and is ready for robustness validation:
- Workflow has completed successfully
- All specialists have finished their work
- Artifact is ready for testing
- Need to validate against edge cases and failure modes

**Routing:** `Router → [BP, Workflow Coordinator]`

**Timing:** AFTER primary workflow completion, BEFORE deployment or production use

### 2. Specification Validation (Priority: MEDIUM)

New or updated GEMS specifications that need testing:
- New Gem specification created
- Specification significantly modified
- Routing rules updated
- Integration patterns changed
- Need to validate specifications against edge cases

**Routing:** `Router → [BP, Specification Review]`

### 3. Framework Evolution Decision (Priority: MEDIUM)

Major changes to GEMS framework that need chaos testing:
- Adding new Gem to ecosystem
- Modifying authority boundaries
- Changing routing logic
- Altering handoff requirements
- Need to validate impact on existing workflows

**Routing:** `Router → [BP, Archeologist, Systems Architect]`

### 4. High-Risk Workflow (Priority: CRITICAL)

Workflows with significant consequences if they fail:
- Security-critical decisions
- Compliance-sensitive work
- High-impact architecture changes
- Large-scale refactoring
- Deletion or removal of material
- Need extensive failure mode analysis

**Routing:** `Router → [Workflow Coordinator, Primary Specialists, BP]`

**Timing:** PARALLEL with primary workflow execution

### 5. Assumption-Heavy Specification (Priority: MEDIUM)

Specifications that rely heavily on unstated assumptions:
- Specifications with many implicit dependencies
- Specifications that assume specialist availability
- Specifications relying on context always being sufficient
- Specifications assuming no conflicting constraints
- Need explicit assumption validation

**Routing:** `Router → [BP, Specification Author]`

### 6. System Stress Testing (Priority: LOW)

Operational testing under extreme load or constraint:
- Testing system under high throughput
- Testing under extreme time pressure
- Testing with minimal resources
- Testing with conflicting constraints
- Need stress testing and scalability validation

**Routing:** `Router → [BP, Test Track]`

### 7. Recovery Path Validation (Priority: HIGH)

Validating that recovery procedures actually work:
- Recovery procedures have been specified
- Need to validate they work in practice
- Need to identify recovery gaps
- Need to measure recovery effectiveness

**Routing:** `Router → [BP, Workflow Coordinator]`

### 8. Edge Case Discovery for Workflow Type (Priority: MEDIUM)

First instance of a new workflow type that needs edge case identification:
- New workflow pattern not previously tested
- New specialist combination not previously validated
- New variant not previously executed
- New context constraint not previously experienced

**Routing:** `Router → [BP, Test Track]`

### 9. Contradiction Detection (Priority: CRITICAL)

Specifications or workflows that appear to have contradictions:
- Two specifications seem to require incompatible behaviors
- Routing rules seem to conflict
- Authority definitions seem to create deadlock
- Success criteria seem impossible to achieve simultaneously

**Routing:** `Router → [BP, Specification Review]`

### 10. Pre-Optimization Analysis (Priority: MEDIUM)

Before optimizing GEMS framework based on trends:
- Optimization recommendations identified
- Need to validate they don't introduce fragility
- Need to test across varied workflows
- Need to ensure no regressions

**Routing:** `Router → [BP, Sequence Optimizer]`

---

## Conditional Escalation Triggers

### Escalate to BP if ANY of these apply:

1. **Workflow completed successfully but feels fragile**
   - Success achieved but path felt precarious
   - Many assumptions were made
   - Edge cases were navigated ad-hoc
   - Need to validate specification or process

2. **Specification is new or significantly changed**
   - Want to validate before deploying
   - Want to identify holes before they cause issues
   - Want to test edge cases proactively

3. **Similar workflows have failed previously**
   - This workflow type has historical failures
   - Want to identify why and validate fix
   - Want to prevent recurrence

4. **Workflow involves high-risk activities**
   - Security-critical work
   - Deletion or removal
   - Compliance-sensitive decisions
   - High-impact architectural changes

5. **System behavior seems incorrect**
   - Specialist did something unexpected
   - Workflow took an unusual path
   - Results don't match expectations
   - Need to validate specification vs reality

6. **Assumptions are being made about specialist behavior**
   - "Specialists will always understand their role"
   - "Context will always be sufficient"
   - "Validation will always catch errors"
   - "Specialists will stay within boundaries"

7. **Authority boundaries seem unclear**
   - Multiple specialists seem to have overlapping authority
   - Conflict resolution path is unclear
   - Blocking authority seems ambiguous

8. **Workflow completion is uncertain**
   - Unclear whether workflow is actually complete
   - Outstanding questions about artifact status
   - Validation results are inconclusive

9. **Performance seems suboptimal**
   - Workflow took longer than expected
   - Multiple rework cycles occurred
   - Parallelization wasn't fully utilized
   - Need to identify bottlenecks or failures

10. **Framework changes are being considered**
    - New Gem under consideration
    - Routing rules being modified
    - Authority boundaries being changed
    - Need to validate impact

---

## BP Responsibilities When Escalated

### When Routed to Chaos Testing

1. **Identify Edge Cases**
   - Document what could go wrong
   - Design scenarios that violate assumptions
   - Test boundary conditions
   - Identify unusual sequences

2. **Attempt Failure Induction**
   - Create scenarios designed to fail
   - Violate constraints intentionally
   - Test recovery paths
   - Measure system resilience

3. **Document Findings**
   - Record each failure discovered
   - Classify by severity
   - Assess impact and recovery
   - Recommend improvements

4. **Validate Assumptions**
   - Test critical assumptions
   - Document which hold and which break
   - Surface implicit dependencies
   - Recommend explicit documentation

### When Routed to Specification Validation

1. **Test Specification Completeness**
   - Does specification cover edge cases?
   - Are assumptions explicit?
   - Are recovery procedures documented?
   - Are boundary conditions addressed?

2. **Identify Ambiguities**
   - What terms are unclear?
   - What responsibilities are fuzzy?
   - What success criteria are subjective?
   - What authority boundaries need clarification?

3. **Expose Contradictions**
   - Are there internal contradictions?
   - Do related specifications conflict?
   - Do routing rules contradict requirements?
   - Are authority definitions circular?

### When Routed to Framework Evolution

1. **Test Impact of Changes**
   - How does new Gem interact with existing Gems?
   - Does change break existing workflows?
   - Does change introduce new failure modes?
   - Does change resolve identified issues?

2. **Validate Backward Compatibility**
   - Do existing workflows still work?
   - Are there edge cases that now fail?
   - Is recovery still possible?
   - Are performance characteristics affected?

---

## Success Criteria for BP Escalation

### Chaos Testing Successful When:

- ✓ Edge cases are systematically identified
- ✓ Assumptions are tested and validated or violated
- ✓ Failure modes are discovered
- ✓ Recovery capabilities are assessed
- ✓ Recommendations are prioritized by severity
- ✓ Specification improvements are identified

### Specification Validation Successful When:

- ✓ Completeness gaps are identified
- ✓ Ambiguities are documented
- ✓ Contradictions are exposed
- ✓ Recommendations are actionable
- ✓ Specification author can address findings
- ✓ Framework robustness is improved

### Framework Evolution Successful When:

- ✓ Impact of changes is understood
- ✓ Backward compatibility is validated
- ✓ New failure modes are identified
- ✓ Existing workflows are protected
- ✓ Change benefits outweigh costs
- ✓ System robustness is maintained or improved

---

## Integration with Test Track

**BP + Test Track Collaboration:**

1. **Test Track executes workflows** → collects metrics
2. **BP analyzes test results** → identifies failure modes
3. **BP designs chaos tests** → extends test harness
4. **Test Track executes chaos tests** → discovers failures
5. **Results feed back to Archeologist** → identifies missing Gems

**Continuous Improvement Loop:**
- Workflow execution → Metrics collection → BP analysis → Chaos test design → Test execution → Finding documentation → Specification improvement → Repeat

---

## Output Format When Escalated to BP

### Edge Case Analysis Report

**Identified Edge Cases**
- Case description
- How it can occur
- Specification coverage (yes/no)
- Potential impact if not handled
- Severity (Critical/High/Medium/Low)

**Assumption Testing Results**
- Assumption statement
- Test method
- Outcome (holds/breaks)
- Impact if assumption is wrong
- Recommendation

### Failure Mode Analysis Report

**Discovered Failures**
- Failure description
- How it was induced
- System behavior during failure
- Recovery attempted (success/failure)
- Impact assessment
- Specification gap identified

**Severity Summary**
- Critical findings (must address)
- High priority (strongly recommend addressing)
- Medium priority (consider addressing)
- Low priority (nice-to-have improvements)

### Recommendations

**Specification Improvements**
- Recommendation 1: [specific change needed]
- Recommendation 2: [specific change needed]
- ...

**Process Improvements**
- Recommendation 1: [add validation gate / safeguard / monitoring]
- Recommendation 2: [add recovery procedure]
- ...

**System Improvements**
- Recommendation 1: [design change to prevent failure]
- Recommendation 2: [add redundancy / safeguard]
- ...

---

## Non-Responsibilities of BP

**BP does NOT:**

- Fix identified failures (that's for specification refinement)
- Make decisions about what to change (that's for humans)
- Enforce compliance with recommendations (that's for governance)
- Override specialist judgment (BP is observer, not authority)
- Deploy changes (BP identifies needs, doesn't implement)

BP is diagnostic and advisory. Findings feed into decision-making, not into automatic system changes.
