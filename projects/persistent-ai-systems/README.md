# Persistent AI Systems — Canonical State & Recovery

## Problem
While working with a frontier LLM, I noticed that during long sessions or between chat instances the LLM could lose its place in projects we had previously been working on. This caused friction when moving from one project or instance to another and then returning to the original place where we left off. So we began working on a system that would establish persistence and provenance for the multiple projects we had going.

## Requirements and Constraints
1. A system that was capable of storing the place where we left off previously.
2. Enough detail to know what we had already learned or discovered, reasoned over, decided, and implemented.
3. A set of instructions that could be called when we were finished working on a project for the time being that would have the LLM durably save to GitHub.
4. A set of instructions that could direct the LLM to the correct GitHub repo and that had checks to make sure the persistence system was healthy and could be trusted.
   
## Architecture
 The persistence architecture is separated into several layers, each with a specific responsibility:

1. **Stage 0 Locator**  
   A small external pointer identifies the expected canonical repository, branch, and location of the bootstrap instructions. It contains no project state itself.

2. **Bootstrap Instructions**  
   A fresh LLM instance follows a defined startup procedure that verifies the canonical source before attempting to reconstruct the project. If the source cannot be verified, the boot process stops rather than substituting remembered or inferred information.

3. **Canonical State**  
   A compact state record contains the information required to continue the project correctly, including the current operating state, important constraints, and the next intended resume point.

4. **Event History and Durable Artifacts**  
   Decisions, failures, experiments, architectural changes, and other consequential work are preserved as durable records. An event ledger maintains the chronological history of significant changes while more detailed artifacts contain the supporting evidence.

5. **Open and Closeout Process**  
   At the beginning of a session, the system reconstructs the current project state from the verified canonical source. At the end of a session, consequential work is reconciled into the persistent records and a new resume point is established.

6. **Deterministic Verification**  
   Scripts and integrity checks independently verify important relationships between the stored records. This allows some persistence checks to be performed without depending on the LLM's interpretation of the data.

## Why It Was Designed This Way
1. This persistennce system was designed in such a way as to prevent the LLM from becoming the governing authority of the persistence system, but rather a participant.
2. LLM agnosticism was also a targeted design so that the persistence system could be utilized across multiple models.

## Failure History and Design Changes

The persistence architecture was not designed all at once. Several failures exposed assumptions in the original design and resulted in changes to how state is discovered, written, and verified.

### Canonical Source Discovery Failure

During the first clean-session boot test, a new LLM instance was unable to reliably locate the repository containing the persistence system.

The system behaved as intended by stopping rather than substituting conversational memory or guessing where the authoritative state was stored. However, the test exposed a circular dependency: the instructions explaining how to reconstruct the project were stored inside the repository that the new instance first needed to locate.

**Design change:** A small Stage 0 locator was introduced outside the canonical project state. Its purpose is only to identify the expected canonical source and allow its identity to be positively verified. It contains no project state itself.

### Incomplete Closeout and Continuity Rollback

In a later session, a closeout was reported as complete even though the current state, event history, and session record had not all been reconciled.

When a fresh instance started afterward, it correctly trusted the canonical records but reconstructed an older project state and an outdated resume point. The stored information was internally plausible, but it was stale.

This demonstrated that successfully writing some information was not enough. The system needed a defined point at which the stored state could be considered sufficiently complete for another instance to inherit.

**Design change:** Persistence was divided into durability levels, with explicit checkpoints at continuity boundaries. Closeout became a reconciliation process rather than simply a summary, requiring the important state, event history, and next resume point to agree before the session is considered durably closed.

### Event Ledger Truncation

A persistence write later replaced part of the historical event ledger with only its recent tail.

The remaining records appeared valid, but part of the project history had been lost from the current version of the ledger. A deterministic continuity check detected the inconsistency, and the missing records were recovered from Git history.

The failure demonstrated that an "append-only" design intention does not guarantee an append-only result.

**Design change:** Positive read-back and deterministic verification were strengthened. Related persistence changes were increasingly treated as a single guarded logical publication rather than independent writes, and historical corrections were recorded as new events rather than rewriting the meaning of previous records.

## Verification and Validation

## What It Demonstrates

## Limitations and Open Questions

## Project Files
