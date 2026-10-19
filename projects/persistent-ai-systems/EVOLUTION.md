# Persistent AI Systems — Engineering Evolution

> **Project status:** Active development  
> **Latest update:** October 2026 — Persistence V3  
> **Scope:** Personal, AI-assisted engineering project. The canonical implementation and operational records remain private.

This log records changes to the system after the [original case study](README.md). The earlier design, its tests, and its limitations remain part of the record. New entries document what prompted a change, what was implemented, what was tested, and what still needs work.

## October 2026 — Persistence V3: Incremental State Updates and Controlled Publishing

**Status:** Implemented and tested in the current GitHub environment. Broader integration and recovery testing remain open.

### Background

The earlier system established verified state recovery between AI conversations. It used Git-backed records, coordinated session closeouts, and an independent verification process to confirm continuity between sessions.

As the project developed, the session-based approach became a limitation. Important findings and decisions could remain provisional until the conversation was closed. Long sessions also made the final review and reconciliation process more difficult to manage.

With V3, important information can be saved and verified as work progresses rather than waiting until a conversation ends. This reduces the amount of information that must be reconciled at closeout while retaining the verification and recovery controls established in the earlier system.

### Implementation

The updated process separates decisions about what information to save from the tools responsible for saving it.

1. **Prepare the update.** The AI and project operator identify information that needs to be preserved and determine where it belongs, using the project's existing approval rules.
2. **Check the proposed change.** The update is submitted through GitHub. Automated checks verify the requested file locations, information-handling restrictions, and expected repository state before publication.
3. **Control who can publish.** The main project branch is protected against direct changes from ordinary development connections. A dedicated GitHub App is authorized to publish changes that pass the required checks.
4. **Verify the result.** The publishing workflow checks the resulting commit and saved file contents. An update is not considered complete until the workflow finishes successfully and the published information is confirmed.
5. **Recover the current state.** A new AI session retrieves the project information and supporting verification records before resuming work. Startup does not require creating a new session transaction.

The earlier process depended on reconciling project information at the end of a conversation. V3 allows important changes to be saved throughout the session instead.

Session closeout remains useful for reviewing anything that may have been missed, but it is no longer required to make individual updates permanent.

The result is a separation between **deciding what should be saved, controlling how it is published, and verifying that publication succeeded.**

### Verification Results

Persistence V3 was tested using the actual GitHub repository, including successful operations and deliberate attempts to perform actions that should be rejected.

The tests focused on three requirements: preventing unauthorized changes, confirming that approved changes are published correctly, and recovering project information in a new AI session.

| Test | Observed result |
|---|---|
| Attempt a direct update to the protected main branch using an ordinary development connection | GitHub rejected the update. The branch remained unchanged. |
| Publish an approved change using the dedicated GitHub App | The publishing workflow completed successfully and updated the protected branch. |
| Compare the completed publication with the original request | The resulting commit, changed files, and saved contents matched the submitted update. |
| Make an authorized change on an unprotected development branch | The change succeeded without modifying the protected main branch. |
| Recover project state in a fresh AI conversation | A read-only reconstruction was completed using repository records and GitHub verification evidence. The existing automated boot checker was not executed directly in that hosted environment. |

These results confirm that the tested permission controls and publishing process behaved as intended. The repository also retains the underlying test records for further review.

The tests do not establish that every possible failure has been addressed. In particular, additional live recovery testing and consistent access to automated startup verification remain outstanding.

The distinction is important: **a completed software operation is not necessarily a verified result.** The system requires evidence that the expected change occurred before accepting it as part of the project's current state.

### Findings and Remaining Limitations

Testing and implementation identified several areas requiring further work.

**Protected Infrastructure Changes**

During the V3 transition, one infrastructure change did not satisfy the required prepublication review procedure. The failed checks were retained in the engineering record, and the operator approved a one-time exception for that specific change.

Subsequent testing confirmed the implemented publishing controls, but those results do not change the outcome of the original review.

A revised procedure for future changes to protected infrastructure still needs to be developed and tested.

**Startup Verification**

The project includes an automated checker designed to verify repository identity, publishing history, and the current project state without modifying the repository.

The verification requirements have been exercised through direct inspection of GitHub records. However, the automated checker has not been consistently executable from the hosted AI environments used during development.

Providing a dependable way for different AI environments to run or consume those checks remains an integration priority.

**Failure and Recovery Testing**

Earlier development included isolated tests for interrupted operations, outdated repository state, ambiguous publication results, and duplicate requests.

Those tests informed the current design, but additional fault testing against the live V3 publishing and recovery process is still needed.

Until that testing is completed, the documented results are limited to the conditions actually exercised.

These are known engineering limitations, not accepted assumptions about how the system will behave under every condition.

### Current Outcome

Persistence V3 is now the active method for maintaining authoritative project information.

Important updates can be saved and verified throughout a conversation rather than waiting for a session closeout. A new session can recover the current project state and work handoff using GitHub records without creating a new startup transaction.

This process has been demonstrated within the tested GitHub environment. Further work is needed to simplify verification across different AI services and to expand live failure and recovery testing.

The goal is **reliable, verifiable project continuity**, not uninterrupted AI operation or complete recall of every conversation.

## October 2026 — Cross-Model Recovery Investigation

**Status:** In progress. Full recovery using a different AI provider has not yet been demonstrated.

An important design goal is to allow the reasoning model to be replaced without losing the project's verified information or operating constraints.

To evaluate this, we began testing whether an unfamiliar AI model could locate and recover the project's authoritative state using only a small repository configuration file and the documented startup procedure.

### Initial Tests

**Test 1 — Missing Verification Evidence**

The first external model received the repository location and startup requirements without previous project history.

Its repository import did not provide enough readable information to complete verification. The model correctly returned the required failure response rather than claiming it had recovered the project.

**Result:** The failure behavior worked in this test. Project recovery was not achieved.

**Test 2 — Repository Permission Review**

A second AI provider was evaluated for the same recovery test. Its GitHub integration requested write permissions to repository resources that were not necessary for read-only recovery.

The authorization was declined before access to the protected repository was granted.

**Result:** The intended permission boundary was maintained. No recovery test was completed with this provider.

### Findings and Next Test

These experiments highlighted two requirements for model portability.

First, each AI environment needs access to readable project records and the evidence required to verify them. Second, that access must be limited to the operations needed for the task.

The next test will use a consistent read-only interface to provide the required GitHub evidence. Success will require the model to verify the current project state, identify the correct work handoff, and recognize any restrictions or unresolved issues.

Until that test succeeds, **cross-model recovery remains an engineering objective rather than a demonstrated capability.**

## Related Development

Persistence V3 is part of a larger personal AI engineering project. Several supporting components are being developed separately and are not yet fully integrated with the persistence system.

**Local AI Orchestration**

Development is underway on a local service intended to coordinate AI models, tools, and access to project information.

The goal is to reduce dependence on any one AI provider and give the supporting software a consistent way to exchange information with different models.

**Conversation Recording and Archival**

A separate recording and archival process is being developed to preserve conversation records independently of the AI's working context.

This serves a different purpose from the verified project state: conversation archives preserve historical material, while persistence records identify the information needed to continue current work.

Complete historical reconciliation and automated integration remain unfinished.

**Append-Only Event History**

A longer-term development objective is an append-only record of project events. This would provide a historical record for reconstruction and review without modifying earlier entries.

The event-history design and its integration with local orchestration are still under development.

These components will be documented separately as implementation and testing progress.

## Next Work

The next development priorities are:

1. Complete and test the procedure for modifying protected publishing infrastructure.
2. Provide a consistent read-only interface for automated startup verification.
3. Demonstrate successful project recovery using a different AI model.
4. Continue integrating persistence with local orchestration and conversation archival.
5. Expand failure and recovery testing under live operating conditions.

Future updates will document completed work, observed results, and design changes. Unsuccessful tests and unresolved problems will remain part of the engineering record.

## Publication and Project Scope

This is a personal, AI-assisted engineering project developed using established engineering practices for requirements, testing, failure investigation, and verification.

The public portfolio documents the engineering approach, observed results, and known limitations. The underlying system, its operational records, and private project information remain outside the public repository.

The [original case study](README.md) and [sanitized demonstration](demo/) provide additional technical background without releasing the private implementation.
