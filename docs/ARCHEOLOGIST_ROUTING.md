# Archeologist Routing Rules

## Automatic Escalation Rules

The Router automatically escalates to Archeologist when:

### 1. Workflow Completion Data Analysis (Priority: MEDIUM)

Completed workflows with collected metrics that should be analyzed for patterns:
- Workflow has executed with full instrumentation
- Metrics have been collected on specialist participation
- Want to identify patterns across multiple workflows
- Want to discover if gaps are emerging

**Routing:** `Router → [Archeologist, Test Track]`

**Timing:** AFTER multiple workflows (minimum 5-10) have been executed

### 2. Recurring Issue Pattern (Priority: HIGH)

Same type of issue has appeared multiple times across different workflows:
- Issue appears in 3+ workflows
- Issue appears to indicate capability gap
- Current workarounds are ad-hoc
- Pattern might justify new Gem

**Routing:** `Router → [Archeologist, BP]`

**Trigger Examples:**
- "We keep needing to validate that requirements are correct" (5+ workflows)
- "Integration repeatedly struggles with semantic conflicts" (4+ workflows)
- "Specialists frequently wait for unavailable peer" (6+ workflows)
- "Context loss happens between certain handoffs" (3+ workflows)

### 3. Specialist Workload Analysis (Priority: MEDIUM)

Specialist is consistently overloaded or certain work doesn't fit current specialists:
- One specialist is bottleneck across many workflows
- Work keeps getting assigned to "wrong" specialist (with workarounds)
- Specialist load could be reduced by extracting domain to new Gem
- Pattern appears in 20%+ of workflows

**Routing:** `Router → [Archeologist, Workflow Coordinator]`

### 4. Test Track Expansion Signal (Priority: MEDIUM)

Test harness is repeatedly expanding to cover new scenarios:
- New test combinations are being added frequently
- New failure modes are being discovered regularly
- Test coverage growth suggests gaps in specification
- Want to know if gaps indicate missing Gems

**Routing:** `Router → [Archeologist, BP, Test Track]`

### 5. BP Finding Pattern (Priority: HIGH)

BP has discovered recurring failure modes across multiple tests:
- Same failure appears in 3+ test scenarios
- Failure mode appears to reflect missing capability
- BP recommends investigating whether new Gem needed
- Pattern suggests systematic gap, not edge case

**Routing:** `Router → [Archeologist, BP]`

**Example:**
- "Reversibility isn't being checked; decision made that can't be undone" (3+ BP tests)
- "No one validates requirements before architecture; causes rework" (4+ BP tests)
- "Authority ambiguous on this type of decision; escalated repeatedly" (5+ BP tests)

### 6. Framework Evolution Point (Priority: CRITICAL)

GEMS ecosystem is being considered for expansion:
- Want to evolve to next version
- Want to identify what new Gems would improve system
- Have collected enough workflow data to analyze patterns
- Ready to make evidence-based decisions on expansion

**Routing:** `Router → [Archeologist, Systems Architect, Workflow Coordinator]`

**Timing:** Conducted after 20+ diverse workflows executed

### 7. Specialist Feedback Indicates Gap (Priority: MEDIUM)

Specialists report that work doesn't fit existing roles:
- Specialist says "someone else should handle this"
- Specialist says "I'm overloaded on this particular work type"
- Specialist says "workflows always need X and no one owns X"
- Multiple specialists independently report similar gap

**Routing:** `Router → [Archeologist, Workflow Coordinator]`

### 8. Domain Emergence Signal (Priority: MEDIUM)

New workflows reveal work in areas not previously encountered:
- Workflows start touching new subject domain
- New type of decision appearing that no Gem was designed for
- New integration pattern appearing repeatedly
- New risk type emerging that security alone can't handle

**Routing:** `Router → [Archeologist, Test Track]`

### 9. Specialist Interaction Problem (Priority: MEDIUM)

Certain Gem pairings consistently have friction:
- Two Gems that should work together have handoff problems
- Two Gems have conflicting authority
- Two Gems can't communicate effectively
- Pattern suggests missing intermediary or specialized role

**Routing:** `Router → [Archeologist, Workflow Coordinator]`

### 10. Efficiency Plateau Detection (Priority: MEDIUM)

Workflow efficiency isn't improving despite optimizations:
- Optimizations hit diminishing returns
- Workflow duration hitting floor despite parallelization
- Efficiency gains are being masked by systematic gaps
- May indicate need for new Gem rather than optimization of existing

**Routing:** `Router → [Archeologist, Sequence Optimizer]`

---

## Conditional Escalation Triggers

### Escalate to Archeologist if ANY of these apply:

1. **Multiple workflows report similar problem**
   - Same issue appearing in 3+ workflows
   - Issue appears ad-hoc in current workflows
   - Pattern suggests systematic gap, not edge case

2. **Current Gem is consistently overloaded**
   - One specialist is bottleneck
   - Workload could be distributed if domain extracted
   - Specialist load reduction would improve overall efficiency

3. **Work doesn't fit any current Gem well**
   - Task is assigned to "least wrong" specialist
   - Multiple workarounds exist
   - Work appears in many workflows but no good home for it

4. **New workflow domain has emerged**
   - Workflows now include work type not previously seen
   - No current Gem has expertise in this domain
   - Type appears in multiple workflows, not just one

5. **Test coverage is expanding rapidly**
   - New test cases added frequently
   - New failure modes discovered regularly
   - May indicate specification gaps that new Gem could address

6. **BP finds recurring failure mode**
   - Same failure induced in multiple test scenarios
   - Failure seems to reflect missing capability
   - Pattern appears systematic, not edge case

7. **Authority boundaries are unclear at certain point**
   - Multiple workflows have same authority conflict
   - Conflict resolution requires escalation repeatedly
   - May indicate missing specialist to own that decision

8. **Specialist feedback indicates frustration**
   - Specialist says "I shouldn't have to do this"
   - Specialist says "this work should be specialized"
   - Multiple specialists report similar gap

9. **Framework evolution is being considered**
   - Collecting workflow data to understand gaps
   - Want to make evidence-based decisions on system expansion
   - Ready to analyze patterns for strategic improvements

10. **New metrics reveal systematic issue**
    - Efficiency analysis shows consistent bottleneck
    - Error analysis shows repeated problem type
    - Load analysis shows uneven specialist utilization

---

## Archeologist Responsibilities When Escalated

### When Routed to Pattern Analysis

1. **Analyze Workflow Data**
   - Identify which specialists are involved
   - Map handoff patterns
   - Measure durations and wait times
   - Identify where work gets stuck

2. **Recognize Patterns**
   - Which issues appear repeatedly?
   - Which specialist pairings are problematic?
   - Which decision types lack clear ownership?
   - Which work doesn't fit existing Gems?

3. **Quantify Impact**
   - How many workflows affected?
   - How much time/effort is lost?
   - How many rework cycles traced to this?
   - What percentage of workflows experience this?

4. **Document Findings**
   - Present evidence of pattern
   - Show frequency and impact
   - Identify current workarounds
   - Make case for gap

### When Routed to Gap Characterization

1. **Define the Gap**
   - What work is needed that no Gem does?
   - What decisions lack clear ownership?
   - What expertise is missing?
   - What integration is missing?

2. **Assess Necessity**
   - Does gap meet frequency threshold (20%+ workflows)?
   - Does gap meet impact threshold (10%+ improvement)?
   - Can existing Gem be extended instead?
   - Is gap truly distinct from existing Gems?

3. **Characterize Required Gem**
   - What would new Gem do?
   - What authority would it have?
   - Which Gems would it work with?
   - What would success look like?

### When Routed to Gem Recommendation

1. **Propose New Gem**
   - Full Gem specification
   - Integration with existing Gems
   - Success metrics
   - Risk assessment

2. **Justify Recommendation**
   - Show evidence of gap
   - Show impact improvement potential
   - Show necessity threshold met
   - Show risk is acceptable

3. **Plan Implementation**
   - When should Gem be implemented?
   - What must be prepared?
   - How would existing workflows transition?
   - How would it be tested?

### When Routed to Evolution Roadmap

1. **Synthesize Recommendations**
   - Collect all identified gaps
   - Prioritize by impact and frequency
   - Identify dependencies
   - Create logical sequence

2. **Create Roadmap**
   - Short-term additions (critical gaps)
   - Medium-term additions (high-value gaps)
   - Long-term vision (emerging domains)
   - Implementation timeline

3. **Validate with System**
   - Will new Gems interact well?
   - Are there conflicts?
   - Does system remain coherent?
   - Are there second-order effects?

---

## Success Criteria for Archeologist Escalation

### Pattern Analysis Successful When:

- ✓ Recurring patterns are identified with data
- ✓ Frequency of pattern is quantified
- ✓ Impact of gap is measured
- ✓ Current workarounds are documented
- ✓ Pattern is shown to be systematic, not anecdotal
- ✓ Recommendation for investigation is clear

### Gap Characterization Successful When:

- ✓ Gap is clearly defined
- ✓ Necessity thresholds are met
- ✓ Existing Gems evaluated for extension
- ✓ Potential new Gem is characterized
- ✓ Success metrics are measurable
- ✓ Risk assessment is complete

### Gem Recommendation Successful When:

- ✓ Gem specification is complete and actionable
- ✓ Impact justification is data-driven
- ✓ Necessity is demonstrated
- ✓ Integration with existing Gems is clear
- ✓ Implementation roadmap is provided
- ✓ Validation plan is specified

### Evolution Roadmap Successful When:

- ✓ All identified gaps are prioritized
- ✓ Implementation sequence is logical
- ✓ Dependencies are resolved
- ✓ Timeline is realistic
- ✓ System remains coherent
- ✓ Roadmap is actionable

---

## Integration with Test Track and BP

**Continuous Improvement Loop:**

```
Workflows Execute
    ↓
Test Track Collects Metrics
    ↓
BP Tests for Failure Modes
    ↓
BP Discovers Recurring Failures
    ↓
Archeologist Analyzes Patterns
    ↓
Archeologist Recommends New Gems
    ↓
New Gems Implemented
    ↓
Workflows Execute with New Gems
    ↓
[Loop continues]
```

**Data Flow:**
- Test Track provides execution metrics
- BP provides failure mode data
- Archeologist synthesizes both into gap analysis
- Recommendations feed into evolution planning
- New Gems fill gaps discovered by previous cycle

---

## Output Format When Escalated to Archeologist

### Pattern Analysis Report

**Identified Patterns**
- Pattern description
- Workflows affected (count and examples)
- Frequency (appears in X% of workflows)
- Current workaround
- Impact if gap not filled

**Evidence**
- Data supporting pattern
- Examples from specific workflows
- Quantified impact
- Necessity threshold assessment

### Gap Characterization Report

**Gap Definition**
- What work is needed
- Which workflows need it
- Why current Gems can't handle it
- What would filling gap accomplish

**Necessity Assessment**
- Frequency threshold: Met/Not met (show data)
- Impact threshold: Met/Not met (show data)
- Can existing Gem handle it? (analysis)
- Is this distinct enough for new Gem? (assessment)

**Recommendation**
- Strong recommendation / Recommend / Consider for future

### Gem Recommendation Report

**Gem Proposal**
- Gem name and role
- Purpose and problem solved
- Capabilities required (specific list)
- Authority and boundaries
- Integration points with existing Gems

**Impact Justification**
- Workflows affected (list and counts)
- Efficiency improvement (quantified)
- Quality improvement (quantified)
- Specialist load impact (quantified)
- Necessity thresholds met (with data)

**Risk Assessment**
- Integration risks with existing Gems
- Potential authority conflicts
- Scope creep risks
- Mitigation strategies

**Implementation Plan**
- Timeline recommendation
- Dependencies (what must be done first)
- Testing requirements
- Transition plan for existing workflows

### Evolution Roadmap Report

**Prioritized Recommendations**
1. [Gem] — Critical
   - Justification (frequency, impact)
   - Effort estimate
   - Timeline

2. [Gem] — High Priority
   - Justification
   - Effort estimate
   - Timeline

3. [Gem] — Medium Priority
   - Justification
   - Effort estimate
   - Timeline

**System Evolution Vision**
- Short-term (1-2 years): Core gaps filled
- Medium-term (2-4 years): Emerging domains addressed
- Long-term (4+ years): Mature ecosystem vision

**Monitoring Plan**
- How to track if recommendations are effective
- What metrics to collect
- How to validate gap analysis was correct
- How to iterate if needed

---

## Non-Responsibilities of Archeologist

**Archeologist does NOT:**

- Create new Gems (that's for Gem specification authors)
- Modify existing Gems (that's for existing Gem specifications)
- Make decisions about which Gems to implement (that's for humans)
- Implement recommendations (that's for engineering teams)
- Test new Gems (that's for Test Track)
- Validate that new Gems work (that's for validation teams)

Archeologist is analytical and advisory. Findings drive decisions, not execution.
