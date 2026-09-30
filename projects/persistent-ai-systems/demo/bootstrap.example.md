# Bootstrap Contract — Sanitized Demonstrator

This file is a reduced, public example of a reconstruction contract used for a persistent AI workspace.

## Reconstruction rules

1. Begin from an externally supplied locator.
2. Positively verify the canonical repository identity before reading project state.
3. Read the bootstrap contract and current state only from that verified source.
4. Verify the expected snapshot hashes before trusting the example artifacts.
5. Parse the event ledger and require the state's `last_event_id` to match the ledger tail.
6. Reconstruct current operating state only from verified canonical artifacts.
7. Treat conversational context or model memory as supplemental information only after canonical verification succeeds.
8. If required identity, state, or integrity checks fail, stop rather than infer or manufacture missing state.

The public demonstrator intentionally omits private project content, production repository identifiers, personal data, and implementation-specific governance records.
