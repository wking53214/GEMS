# Deletion Authority Routing Rules

## Automatic Escalation Rules

The Router automatically escalates to Deletion Authority (in addition to primary specialist) when:

### 1. Proposed Deletion of Significant Material (Priority: CRITICAL)

Any proposed deletion of material that has importance or dependencies:
- Code removal affecting functionality
- Data deletion affecting system state
- Documentation deletion affecting knowledge
- Configuration deletion affecting behavior
- Archive or historical material deletion
- User or workflow data deletion

**Routing:** `Router → [Deletion Authority Alpha, Primary Specialist]`

### 2. Permanent Information Removal (Priority: CRITICAL)

Operations that would destroy information irreversibly:
- Deletion of records with no backup
- Permanent removal of design decisions
- Destruction of audit trails or logs
- Removal of knowledge that exists nowhere else
- Archive discard without preservation

**Routing:** `Router → [Deletion Authority Alpha, Security & Governance Auditor]`

### 3. Deletion with Regulatory or Compliance Impact (Priority: CRITICAL)

Deletions affecting compliance or governance:
- Personal data deletion (privacy/GDPR/regulatory)
- Deletion with legal hold or litigation implications
- Audit trail deletion affecting accountability
- Compliance record deletion
- Regulatory requirement deletions

**Routing:** `Router → [Deletion Authority Alpha, Security & Governance Auditor]`

### 4. Refactoring or Code Evolution with Deletion (Priority: HIGH)

Structural improvements involving removal:
- Large code deletion or removal
- Module or component deletion
- Interface or API deletion
- Dependency removal
- Technical debt removal through deletion

**Routing:** `Router → [Deletion Authority Alpha, Refactoring Guardian, Engineering Architecture & Evolution]`

### 5. Data Migration or Transformation with Discard (Priority: HIGH)

Data operations that discard material:
- Deletion during data migration
- Discarding old format data in favor of new
- Removal of deprecated data structures
- Archive purge operations
- Retention policy enforcement deletions

**Routing:** `Router → [Deletion Authority Alpha, Testing & Validation Engineer, Integration Guardian]`

### 6. Knowledge or Documentation Deletion (Priority: MEDIUM)

Removal of institutional knowledge:
- Documentation deletion
- Decision record deletion
- Architecture documentation removal
- Knowledge base deletion
- Historical information removal

**Routing:** `Router → [Deletion Authority Alpha, Knowledge Architect]`

### 7. User or Workflow Data Deletion (Priority: CRITICAL)

Deletion affecting user-facing data or workflow:
- User account data deletion
- User-generated content removal
- Workflow history deletion
- Transaction record deletion
- User preference or configuration deletion

**Routing:** `Router → [Deletion Authority Alpha, Security & Governance Auditor, Testing & Validation Engineer]`

### 8. Authorized Deletion Execution (Priority: CRITICAL)

When valid deletion authorization has been established:
- Execute authorized deletion with verification
- Verify authorization status and scope
- Execute deletion within authorized scope
- Document deletion and maintain audit trail
- Report execution to authorization source

**Routing:** `Router → [Deletion Authority Omega]`

### 9. Deletion Candidate with Uncertain Authorization (Priority: HIGH)

Proposed deletion where authorization status is unclear:
- Authorization is unverified or conflicting
- Multiple parties claiming authority
- Scope boundaries are unclear
- Authorization chain is unclear
- No documented authorization exists

**Routing:** `Router → [Deletion Authority Alpha, Workflow Coordinator]`

### 10. Deletion with Dependency or Impact Uncertainty (Priority: HIGH)

Proposed deletion where dependencies or downstream impact is unclear:
- Scope of deletion impact is unknown
- Dependencies on deleted material are unidentified
- Recoverability status is uncertain
- Alternative approaches have not been evaluated
- Risk assessment is incomplete

**Routing:** `Router → [Deletion Authority Alpha, Primary Specialist, Code Review Sentinel]`

---

## Conditional Escalation Triggers

### Escalate to Deletion Authority Alpha if ANY of these apply:

1. **Material being deleted has dependencies**
   - Other systems depend on it
   - Downstream processes reference it
   - Documentation or records depend on it
   - Recoverability concerns exist

2. **Deletion would remove important context or history**
   - Historical information would be lost
   - Decision rationale would be destroyed
   - Audit trail would be affected
   - Knowledge preservation risk exists

3. **Authorization for deletion is not clearly established**
   - No authorization document exists
   - Multiple conflicting authorizations exist
   - Authorization scope is unclear
   - Authorization chain cannot be verified

4. **Deletion has regulatory or compliance implications**
   - Data protection requirements
   - Retention policy concerns
   - Legal hold implications
   - Audit or regulatory risk

5. **Proposed deletion would be difficult to reverse**
   - No backup or alternative source exists
   - Recoverability cost is high
   - Deletion is effectively permanent
   - Alternative approaches exist

6. **Deletion scope is ambiguous or disputed**
   - Unclear exactly what should be deleted
   - Multiple interpretations of scope
   - Scope boundaries are vague
   - Disagreement about what qualifies

7. **Material could be archived instead of deleted**
   - Preservation alternative exists
   - Non-destructive approach possible
   - Archival meets the actual need
   - Deletion is premature or unnecessary

8. **Deletion is proposed as a side effect rather than explicit decision**
   - Deletion would occur as consequence of other work
   - No explicit deletion authorization
   - Not independently decided to delete
   - Scope of deletion side effects unclear

9. **Material has historical, compliance, or knowledge value**
   - Decision records with rationale
   - Historical information for future reference
   - Compliance or audit requirements
   - Knowledge preservation need

10. **Uncertainty exists about whether deletion is necessary**
    - Alternative solutions not fully explored
    - Assumption that deletion is required but not verified
    - Refactoring or alternative approach might be better
    - Deletion would solve the problem but at unknown cost

---

## Authorization Verification Framework

### ALPHA Decision Framework

**When Alpha receives a deletion candidate, determine:**

**SITUATION: Clear Authorization Exists**
- Authorization is documented
- Scope is clearly defined
- Justification is provided
- → Route to Omega for execution verification

**SITUATION: Authorization is Ambiguous**
- Authorization is claimed but not clearly documented
- Scope boundaries are unclear
- Multiple interpretations exist
- → Request authorization clarification before proceeding

**SITUATION: No Authorization Exists**
- Deletion is proposed without authorization
- No authorized party has approved removal
- Support for deletion is informal
- → Identify who should authorize and obtain authorization

**SITUATION: Authorization is Conflicting**
- Multiple authorizations conflict
- Different parties claim different scope
- Priorities are unclear
- → Escalate to resolve conflict before proceeding

**SITUATION: Deletion Alternative Exists**
- Archive instead of delete
- Redact instead of delete
- Deprecate instead of delete
- → Recommend alternative if preservation is possible

---

### OMEGA Decision Framework

**When Omega receives an authorized deletion, verify:**

**AUTHORIZATION VERIFICATION:**
- Is authorization status VERIFIED or ATTESTED?
- Can authorization be traced to authorized source?
- Is authorization still valid (not revoked/expired)?
- → If VERIFIED or ATTESTED and valid: PROCEED
- → If UNVERIFIED, ABSENT, or CONFLICTING: STOP

**SCOPE VERIFICATION:**
- Is requested deletion within authorized scope?
- Has scope been clearly defined?
- Are scope boundaries unambiguous?
- → If within scope: PROCEED
- → If unclear or outside scope: REQUEST CLARIFICATION

**PRE-EXECUTION CHECKS:**
- Has recoverability status been documented?
- Have dependencies been identified?
- Has impact been assessed?
- Has documentation been updated to reflect deletion?
- → If all complete: EXECUTE
- → If incomplete: REQUEST COMPLETION

**EXECUTION:**
- Execute deletion precisely as authorized
- Do not expand scope beyond authorization
- Document execution with authorization reference
- Preserve audit trail
- Report execution completion

---

## Special Cases

### Deletion of Deletion Candidates

If Alpha identifies material that should not be deleted after analysis:

**Alpha Output:** "Deletion not recommended"

**Supporting Evidence:**
- Why deletion is not justified
- What would be preserved by not deleting
- Alternative approaches
- Recommendation to retain or archive instead

**Scope:** Deletion candidate is preserved, not removed

---

### Deletion with Compliance Hold

If deletion is requested but material is subject to legal hold or compliance retention:

**Authorization Status:** CONSTRAINED

**Omega Action:**
- Cannot execute deletion while hold is active
- Preserve material under compliance restriction
- Document hold and its implications
- Alert authorized parties to hold status

---

### Partial Deletions and Scope Creep

If authorized deletion is for subset of material but request expands to additional scope:

**Omega Action:**
- Execute only explicitly authorized portion
- Preserve material outside authorized scope
- Document scope limitation
- Request separate authorization for expanded scope

---

## Integration with Other Gems

**Deletion Authority works with:**

- **Primary Specialist** — Provides deletion context and justification
- **Code Review Sentinel** — Analyzes deletion impact on code integrity
- **Refactoring Guardian** — Evaluates deletion as refactoring approach
- **Security & Governance Auditor** — Validates compliance and governance implications
- **Testing & Validation Engineer** — Assesses deletion testing requirements
- **Knowledge Architect** — Evaluates knowledge preservation before deletion
- **Workflow Coordinator** — Routes deletion authorization through proper workflow
- **Research Analyst** — Researches implications and alternatives

**Deletion Authority does NOT:**

- Create authorization (only verifies)
- Override authorized scope (only executes within scope)
- Expand deletion beyond authorized material
- Make authorization decisions (only verifies them)
- Establish canonical status of deleted material

---

## Output When Routed to Deletion Work

### Alpha Deletion Analysis Includes:

**Deletion Candidate Identification**
- What material is proposed for deletion
- Why deletion is proposed
- Supporting evidence or justification

**Dependency Analysis**
- What systems or workflows depend on this material
- What downstream processes would be affected
- Documentation or records that reference it

**Risk Assessment**
- Information that would be lost
- Compliance or regulatory implications
- Audit trail implications
- Business continuity impact

**Recoverability Evaluation**
- Can material be recovered if decision changes
- Backup or alternative source availability
- Cost of recovery
- Cost of permanent loss

**Alternative Approaches**
- Could archival serve instead of deletion
- Could redaction serve instead of deletion
- Could deprecation serve instead of deletion
- When non-destructive alternatives are preferable

**Recommendation**
- Delete/archive/redact/preserve
- If delete: conditions and required authorization
- Scope boundaries
- Required documentation

### Omega Deletion Execution Includes:

**Authorization Verification**
- Authorization status (VERIFIED/ATTESTED/UNVERIFIED/ABSENT/CONFLICTING)
- Authorization source and authority
- Scope verified against authorization

**Execution Documentation**
- Material deleted
- Scope of deletion
- Authorization reference
- Date, time, responsible party
- Justification and supporting evidence

**Execution Confirmation**
- Deletion completed as authorized
- Scope limitations encountered if any
- Material that could not be deleted as requested
- Audit trail recorded

---

## Success Criteria

Deletion Authority work is successful when:

1. ✓ All proposed deletions are analyzed before authorization
2. ✓ Dependencies and risks are identified
3. ✓ Non-destructive alternatives are considered
4. ✓ Authorization is clearly verified before execution
5. ✓ Execution occurs only within authorized scope
6. ✓ Every deletion is fully documented
7. ✓ Audit trail is complete and preserved
8. ✓ Recoverability status is established
9. ✓ No deletion occurs without clear authorization
10. ✓ Uncertain authorizations result in preservation, not deletion
