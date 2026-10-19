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

The design was exercised against the actual GitHub repository rather than assessed only from source code or test descriptions.

| Test | Observed result |
|---|---|
| Ordinary connection attempts to change the protected branch | Rejected; the branch remained unchanged |
| Authorized publishing service submits an accepted update | Completed successfully through GitHub Actions |
| Published commit and file contents are checked after publication | Matched the submitted change |
| Ordinary development continues on a separate working branch | Succeeded without changing the protected branch |
| Fresh-session state recovery | Read-only reconstruction was demonstrated with repository evidence; hosted execution of the deterministic boot checker is not yet consistently available |

These results establish the tested permission and publishing behavior. They do not constitute a general security audit or proof that every interruption and failure mode has been covered.

### Findings and Remaining Limitations

An infrastructure change during the transition did not satisfy the existing prepublication review sequence. The failed checks were preserved, and a one-time, operator-reviewed deviation was recorded. Later checks were not treated as retroactive evidence that the original procedure passed. A compliant process for future protected-infrastructure changes remains to be completed and tested.

The project includes code for deterministic, read-only startup verification. However, making that checker available consistently in hosted AI environments remains an integration problem. A model's claim that it has recovered project state is not accepted as a substitute for the required evidence.

Additional controlled failure testing is also needed for the live publishing and recovery process. Earlier isolated fault tests remain useful, but they do not establish how every live failure will behave.

### Current Outcome

Persistence V3 is the active method used to preserve authoritative project changes. Verified updates no longer depend on ending a conversation, and the next session can retrieve the current state and work handoff without a required startup write.

The engineering objective is **reliable, auditable project continuity**. This is not a claim of uninterrupted model operation, complete conversational recall, or production-ready deployment.

## October 2026 — Cross-Model Recovery Investigation

**Status:** Experimental; full recovery using a different AI provider has not been demonstrated.

A related test asks whether another AI model can recover the same project state without access to previous conversations.

In an initial trial, a different model received only the repository locator and the instruction to verify canonical state. Its repository import did not expose enough readable information to complete verification. The model returned the required failure message rather than claiming a successful recovery.

That is a positive result for the **fail-closed requirement**, not a successful cross-model boot.

A second provider's integration requested broader repository permissions than the read-only experiment required. Access to the protected project repository was not granted, so no recovery test was completed through that integration.

These trials exposed two practical issues: models need a dependable way to retrieve verification evidence, and connector permissions must match the intended task. The next test must demonstrate actual retrieval, verification, and correct state reconstruction—not merely a convincing summary.

## Related Development

The persistence work is part of a wider personal AI project. Related components are at different stages of development and are **not presented as completed V3 integrations**.

- **Local AI orchestration service:** intended to coordinate models, tools, and approved access to project information without tying the supporting software to one AI provider.
- **Conversation capture and archival:** preserves conversation material separately from the smaller verified state needed to resume a project. Full historical reconciliation remains unfinished.
- **Append-only event history:** a proposed durable record of events in sequence, to support future reconstruction and review without rewriting earlier records.

These components will receive their own engineering records as their implementations and test evidence develop.

## Next Work

The next steps are to establish and test the protected-infrastructure change procedure, make deterministic startup verification available through a consistent read-only interface, complete a verified cross-model recovery test, and continue integration with local orchestration and archival tools.

Future updates will be added to this log as work is completed. Failed tests and design corrections will remain visible rather than being rewritten into a more convenient development history.

## Publication Boundary

This public account describes tested behavior and known limitations without releasing the private canonical repository, its operating data, credentials, or protected implementation details. The [original case study](README.md) and its [sanitized example](demo/) remain available for readers who want to examine the underlying engineering approach.
