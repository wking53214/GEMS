# Workflow Coordinator Routing Rules

## Automatic Escalation Rules

The Router automatically escalates to Workflow Coordinator when:

### 1. Multiple Specialists Required (Priority: CRITICAL)

Work that requires coordination between multiple Gems:
- Objective needs multiple perspectives
- Different specialized expertise required
- Work spans multiple domains
- Complex dependencies between specialists
- Handoffs required between stages

**Routing:** `Router → [Workflow Coordinator, Primary Specialists]`

### 2. Complex Workflow Sequencing (Priority: HIGH)

Work requiring careful ordering and dependency management:
- Multiple phases that must occur in sequence
- Dependencies between specialist work
- Evidence must be gathered before decisions
- Validation must occur before proceeding
- Clear prerequisites and dependencies

**Routing:** `Router → [Workflow Coordinator, Domain Specialists]`

### 3. Critical Context Preservation (Priority: CRITICAL)

Work where context loss between stages would cause failure:
- Continuity is essential to avoid duplication
- Each specialist builds on prior specialist's work
- Material changes must be traceable
- Baseline integrity is critical
- Authority or authorization chains must be preserved

**Routing:** `Router → [Workflow Coordinator, Primary Specialists]`

### 4. Large or Complex Workflow (Priority: HIGH)

Substantial work involving many steps or multiple specialists:
- More than two specialists involved
- More than three workflow stages
- Complex decision points and branches
- Multiple validation and review stages
- Significant coordination overhead

**Routing:** `Router → [Workflow Coordinator, Domain Specialists]`

### 5. Workflow with Deletion Components (Priority: CRITICAL)

Work involving deletion or removal of material:
- Deletion candidates identified
- Deletion analysis required
- Authorized deletion execution
- Preservation-relevant workflows
- Recoverability assessment needed

**Routing:** `Router → [Workflow Coordinator, Deletion Authority, Primary Specialist]`

### 6. Integration Across Multiple Systems (Priority: HIGH)

Workflow requiring coordination across multiple codebases or systems:
- Multi-source integration required
- Multiple teams or components involved
- Integration strategy needed
- Conflict resolution required
- Component preservation critical

**Routing:** `Router → [Workflow Coordinator, Integration Guardian, Primary Specialists]`

### 7. Architectural or Strategic Decision (Priority: CRITICAL)

Complex decision requiring multiple specialist inputs:
- Architecture and implementation perspectives needed
- Strategic and tactical considerations
- Research and domain expertise required
- Risk assessment and validation needed
- Long-term implications matter

**Routing:** `Router → [Workflow Coordinator, Systems Architect, Engineering Architecture & Evolution, Research Analyst]`

### 8. Workflow with Validation Dependencies (Priority: HIGH)

Work where validation must occur at specific points:
- Testing strategy must precede implementation
- Code review must occur before merge
- Security assessment must occur before deployment
- Compliance validation required
- Validation results gate advancement

**Routing:** `Router → [Workflow Coordinator, Testing & Validation Engineer, Code Review Sentinel, Domain Specialists]`

### 9. Conflict Resolution Required (Priority: HIGH)

Workflow where specialist recommendations conflict:
- Multiple specialists have different recommendations
- Evidence supporting conflicting positions
- Requires resolution before proceeding
- Human decision or additional research needed
- Impact of conflict on system is material

**Routing:** `Router → [Workflow Coordinator, Research Analyst, Primary Specialists]`

### 10. Knowledge Preservation and Documentation (Priority: MEDIUM)

Work requiring documentation of decisions, architecture, or knowledge:
- Decision records must be created
- Architecture documentation needed
- Institutional knowledge must be preserved
- Rationale for choices must be documented
- Future reference and learning required

**Routing:** `Router → [Workflow Coordinator, Knowledge Architect, Technical Documentation Specialist, Domain Specialists]`

---

## Conditional Escalation Triggers

### Escalate to Workflow Coordinator if ANY of these apply:

1. **More than one specialist is required**
   - Multiple perspectives needed
   - Different expertise domains involved
   - Coordination between stages necessary

2. **Handoffs between specialists are required**
   - Work transfers from one specialist to another
   - Context must be preserved between stages
   - Dependencies span multiple specialists

3. **Workflow dependencies are complex**
   - Multiple work items with dependencies
   - Evidence must be gathered before decisions
   - Validation must occur before proceeding
   - Clear prerequisite relationships exist

4. **Context loss between stages would cause problems**
   - Restarting analysis would be wasteful
   - Prior work must inform later stages
   - Continuity is essential to correctness

5. **Authority or scope boundaries need active management**
   - Clear delineation between specialist responsibilities
   - Scope expansion risk exists
   - Authority boundaries must be preserved
   - Boundary violations must be detected

6. **Workflow state tracking is necessary**
   - Workflow has more than three stages
   - Progress must be tracked through multiple phases
   - Completion criteria are complex
   - Multiple decision points exist

7. **Specialist conflict is possible**
   - Different specialists might have different opinions
   - Evidence might support multiple approaches
   - Tradeoffs need to be surfaced

8. **Deletion or material removal is involved**
   - Deletion candidates identified
   - Authorization verification required
   - Scope control necessary
   - Recoverability documentation needed

9. **Integration across multiple sources**
   - Multiple codebases or systems
   - Coordination across teams
   - Component preservation critical
   - Conflict resolution needed

10. **Validation at specific workflow points is critical**
    - Testing must inform implementation decisions
    - Review findings must be addressed
    - Compliance validation gates advancement
    - Results determine workflow direction

---

## Workflow Coordinator Responsibilities

### When Routed to Workflow Coordination

1. **Establish Workflow Context**
   - Define primary objective and desired outcome
   - Identify baseline and source material
   - Establish active constraints and known decisions
   - Document accepted assumptions and unresolved questions

2. **Determine Required Specialists and Sequence**
   - Identify which specialists are needed
   - Determine correct sequence based on dependencies
   - Identify parallel work opportunities
   - Establish critical path

3. **Coordinate First Specialist**
   - Provide complete workflow context
   - Establish their scope and responsibilities
   - Identify required inputs and expected outputs
   - Clarify authority boundaries

4. **Receive First Specialist Output**
   - Evaluate completeness and quality
   - Identify any gaps or issues
   - Update workflow state
   - Prepare handoff to next specialist

5. **Manage Subsequent Handoffs**
   - Transfer context and evidence to next specialist
   - Ensure prior work is understood and not duplicated
   - Maintain continuity through all stages
   - Update workflow state after each stage

6. **Detect and Resolve Conflicts**
   - Identify when specialist recommendations conflict
   - Surface both positions with supporting evidence
   - Determine resolution approach
   - Escalate if human decision required

7. **Manage Deletion Workflows**
   - Route deletion candidates to Deletion Authority Alpha
   - When authorized, route to Deletion Authority Omega
   - Maintain recoverability documentation
   - Preserve audit trail

8. **Monitor for Workflow Failures**
   - Watch for context loss, duplicated analysis, missing dependencies
   - Identify incomplete handoffs or authority violations
   - Surface unresolved questions being treated as settled
   - Stop workflow if blockers cannot be resolved

9. **Establish Workflow Completion**
   - Confirm all specialists completed their work
   - Verify required validation occurred
   - Document final artifact and its status
   - Record open questions and limitations

---

## Workflow State Management Framework

### Track Throughout Workflow

**Baseline Identity**
- Original material or source
- Version at workflow start
- What should remain unchanged

**Current Artifact Version**
- Where workflow currently stands
- What has changed
- Latest version of working material

**Completed Work**
- What specialists have finished
- What stages are complete
- What has been validated

**Open Items**
- What remains unresolved
- What decisions are pending
- What questions are open

**Decisions Reached**
- What has been decided
- Why it was decided
- What evidence supports it

**Authority and Constraints**
- What each specialist is permitted to do
- What boundaries cannot be crossed
- What requires external approval

**Validation Status**
- What has been validated
- What remains unvalidated
- What validation is pending

**Pending Actions**
- What work is coming next
- What specialist is next
- What must happen before next stage

---

## Specialist Coordination Framework

### When Establishing Specialist Role

**Communicate to Specialist:**

1. Assigned responsibility (what they're doing)
2. Workflow objective they support
3. Relevant context and background
4. Decisions already made (don't reconsider these)
5. Work already completed (don't redo this)
6. Required inputs they'll receive
7. Expected outputs they should produce
8. Constraints and authority boundaries
9. What remains unresolved
10. How their work enables the next stage

**When Receiving Specialist Output:**

1. Evaluate completeness and quality
2. Identify gaps or unclear points
3. Document what was produced
4. Update workflow state
5. Determine readiness for next stage
6. Identify any blockers or issues

---

## Handoff Integrity Framework

### Handoff Must Include

- **Objective** - What must be accomplished
- **Baseline** - Source material and version
- **Context** - Relevant background
- **Decisions** - What has been decided
- **Completed Work** - What doesn't need to be repeated
- **Open Items** - What remains unresolved
- **Required Evidence** - What must be established
- **Authority** - What the specialist can do
- **Expected Output** - What should be produced
- **Next Action** - Recommended continuation

### Handoff Integrity Checks

- Is information sufficient for next specialist to work without repeating prior analysis?
- Are decisions clearly marked so they're not reconsidered?
- Is context preserved so dependencies are understood?
- Is scope clear so boundaries are not violated?
- Are constraints documented so they're respected?

---

## Integration with Other Gems

**Workflow Coordinator works with:**

- **All Other Gems** — Routes work, maintains continuity
- **Router** — Uses routing determinations to establish workflow
- **Requirements Analyst** — Clarifies objectives and scope
- **Research Analyst** — Provides evidence for decisions
- **Systems Architect** — Provides strategic direction
- **Engineering Architecture & Evolution** — Validates architectural feasibility
- **Code Review Sentinel** — Quality gate before integration
- **Integration Guardian** — Coordinates multi-source work
- **Security & Governance Auditor** — Validates security/compliance
- **Testing & Validation Engineer** — Validation gating
- **Technical Documentation Specialist** — Workflow documentation
- **Knowledge Architect** — Preserves decisions and rationale
- **Refactoring Guardian** — Evaluates improvements
- **Deletion Authority** — Routes and manages deletions

**Workflow Coordinator does NOT:**

- Perform specialist work
- Make decisions belonging to specialists
- Override specialist judgment
- Create authority or authorization

---

## Output When Escalated to Coordination

### Workflow Establishment Produces

**Workflow Context**
- Objective and desired outcome
- Baseline and source material
- Active constraints and known decisions
- Unresolved questions

**Specialist Sequence**
- Identified specialists
- Correct sequence based on dependencies
- Parallel work opportunities if any
- Critical path

**Initial Handoff**
- Complete context for first specialist
- Clear scope and responsibilities
- Required inputs and expected outputs
- Authority boundaries

### Workflow Completion Produces

**Final Artifact**
- Complete result of workflow
- All changes documented
- Current version identified
- Status clearly established

**Workflow History**
- All specialists who participated
- Work completed by each
- Decisions made
- Changes from baseline

**Validation Status**
- What was validated
- What remains unvalidated
- Outstanding validation requirements

**Open Items**
- Unresolved questions
- Assumptions made
- Information gaps
- What would change recommendations

**Knowledge Preservation**
- Decision records
- Rationale for choices
- Important insights
- Lessons learned

---

## Success Criteria

Workflow Coordinator work is successful when:

1. ✓ Workflow context is clearly established
2. ✓ Specialists are correctly sequenced
3. ✓ Context transfers correctly between stages
4. ✓ No completed work is unnecessarily repeated
5. ✓ Responsibility boundaries are maintained
6. ✓ Specialist scope is clearly understood
7. ✓ Changes are traceable from baseline to result
8. ✓ Conflicts are surfaced and resolved
9. ✓ Workflow completion is clearly established
10. ✓ Final artifact status is clear
