# Shared Workspace MCP V0 — Bounded AI Collaboration Interface

> **Status: Complete / validated reference implementation**

## Problem

An AI system that can only discuss code is useful, but an AI system that can modify files directly can become dangerous very quickly if the interface is simply "give the model a shell."

The goal of this project was to create a small collaboration layer that lets an AI participant inspect and update files inside one approved workspace while deliberately withholding broad filesystem and shell authority.

The design question was:

> What is the smallest useful file-collaboration interface that supports real engineering work while still failing closed when the caller is stale, out of bounds, or asking for more authority than the tool should have?

## Requirements and Constraints

The V0 interface had to:

1. expose only a bounded workspace rather than the host filesystem;
2. support status, directory listing, text reads, and text writes;
3. limit reads and writes to 64 KiB UTF-8 text;
4. prevent path traversal outside the workspace;
5. prohibit writes into `.git`;
6. distinguish file creation from file update;
7. refuse updates when the caller is working from stale content;
8. stage writes before commit;
9. preserve existing file permission mode during updates;
10. avoid generic shell execution, Git operations, directory creation, and automatic conflict resolution.

The design intentionally treats file-version identity and execution authority as different concepts. A correct hash can prove which version the caller read; it does not grant permission by itself.

## Interface

The MCP server exposes four tools:

```text
workspace_status
list_files
read_file
write_file
```

### Bounded path resolution

Every requested path is resolved against one configured workspace root.

If the resolved path falls outside that root, the request fails.

Write paths receive an additional restriction: any real `.git` path component is rejected.

### Read contract

`read_file(relative_path)`:

- rejects missing targets;
- rejects directories;
- rejects path traversal;
- reads at most 64 KiB + 1 byte from the underlying file;
- refuses the request when the result exceeds the 64 KiB limit;
- decodes UTF-8 and rejects invalid text;
- returns the exact byte count and SHA-256 with the content.

The bounded I/O detail matters. An earlier implementation checked the file size first and then read the file. Review identified the small time-of-check/time-of-use gap between those operations. The accepted version instead bounds the read itself.

### Write contract

The write interface uses explicit create/update semantics:

```text
missing target + no expected hash
    -> CREATE

existing target + matching expected hash
    -> UPDATE

existing target + no expected hash
    -> REFUSE

existing target + stale/wrong expected hash
    -> REFUSE

missing target + supplied expected hash
    -> REFUSE
```

For updates, the supplied SHA-256 is an optimistic-concurrency precondition. If another actor changes the file after the caller reads it, the stale update is refused rather than silently overwriting newer work.

### Staged commit behavior

Proposed content is:

1. UTF-8 encoded;
2. checked against the write-size limit;
3. written to a temporary file beside the target;
4. flushed and `fsync`'d;
5. committed using a create or update path.

New-file creation uses a same-filesystem hard link so an existing target cannot be overwritten.

Updates re-check the current SHA-256, preserve the current file mode, and then use atomic replacement.

## Verification and Validation

The final regression suite contains **24 pytest tests** covering the intended contract.

The suite verifies:

- exact status response;
- deterministic directory listing;
- missing-path, file-target, and traversal rejection for listing;
- read content, byte count, and SHA-256 metadata;
- missing, directory, traversal, oversized, and non-UTF-8 read rejection;
- successful create;
- duplicate-create refusal;
- successful correct-hash update;
- stale-hash refusal with newer content preserved;
- missing-target-with-hash refusal;
- `.git` write refusal;
- write path-traversal refusal;
- missing-parent refusal;
- directory-target refusal;
- 64 KiB + 1 write refusal;
- existing permission-mode preservation;
- returned write metadata.

Final local regression result:

```text
24 passed
```

The accepted implementation was then exercised through the real streamable-HTTP MCP transport with a non-mutating smoke client.

Successful completion ended with:

```text
SHARED_WORKSPACE_MCP_V0_SMOKE_PASS
```

The smoke test verified transport, tool registration, successful bounded operations, and expected rejection behavior.

See [acceptance evidence](evidence/acceptance-summary.md) for the validation record.

## Failure Handling and Review Findings

Several small defects were deliberately treated as useful engineering evidence rather than hidden:

- The initial read design used a size check followed by a separate read. Review replaced it with bounded I/O.
- During final test packaging, a duplicate pytest function name was found. Python had silently rebound the later definition, so the suite still passed. The duplicate was removed and the complete 24-test suite was rerun before the acceptance snapshot.
- A publication read-back caught a mismatch between one prepared source blob and the tested source. The mismatch was corrected using normal forward history, followed by exact positive read-back and a full Core-side reproduction test.

These were not reasons to discard the project. They were evidence that layered review, regression testing, and positive read-back were doing their jobs.

## Reproducibility

Validated dependency versions:

```text
mcp==2.3.0
pytest==9.1.1
```

The private reference implementation includes a setup/run/test README and was reproduced from the published source before final acceptance.

## What It Demonstrates

This project is small by design, but it exercises several concepts that matter in larger AI systems:

- **least-authority interface design** instead of defaulting to a shell;
- **optimistic concurrency control** to protect human and machine collaborators from stale overwrites;
- **atomic file-update mechanics**;
- **failure-closed path handling**;
- **explicit capability boundaries**;
- **regression-driven development** once behavioral contracts stabilize;
- **real transport-level integration testing**, not only direct function tests;
- **positive publication verification** rather than assuming a write succeeded because a tool returned success;
- **AI-assisted implementation with human review and operator control**.

## Limitations and Next-Level Questions

V0 intentionally does not solve everything.

Open extensions include:

- named multiple workspaces;
- actor/object/right policy rules;
- stronger multi-writer coordination;
- directory creation;
- binary-file handling;
- editor integration;
- Git workflow integration;
- broader communication and routing layers.

Those are separate architectural problems rather than features silently smuggled into the V0 authority surface.

## Portfolio Disclosure

The production reference implementation is part of a larger private personal AI-systems project. This public case study preserves the engineering method, interface contract, failure history, and acceptance evidence while omitting private project state, internal paths, credentials, and unrelated system details.
