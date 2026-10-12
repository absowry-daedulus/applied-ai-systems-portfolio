# Shared Workspace MCP V0 — Acceptance Summary

**Result:** PASS  
**Regression suite:** 24 tests passed  
**Integration:** Real streamable-HTTP MCP smoke test passed  
**Reference implementation:** Private, personally owned AI-systems project

## Acceptance Matrix

| Area | Acceptance condition | Result |
|---|---|---|
| Workspace boundary | Resolved paths cannot escape the approved root | PASS |
| Git protection | Writes into `.git` are refused | PASS |
| Listing | Root and nested directories list deterministically | PASS |
| Listing failures | Missing, file-target, and traversal requests refuse | PASS |
| Read metadata | Content, byte count, and SHA-256 are returned | PASS |
| Read size | 64 KiB + 1 byte is refused | PASS |
| Read encoding | Invalid UTF-8 is refused | PASS |
| Create | Missing target with no expected hash creates | PASS |
| Duplicate create | Existing target cannot be overwritten as create | PASS |
| Update | Matching expected SHA-256 updates | PASS |
| Stale update | Wrong/stale hash refuses and preserves newer content | PASS |
| Missing update target | Supplied hash against missing file refuses | PASS |
| Missing parent | Write refuses rather than creating directories implicitly | PASS |
| Directory target | Directory cannot be replaced by file write | PASS |
| Write size | 64 KiB + 1 byte is refused | PASS |
| File mode | Existing permission mode survives update | PASS |
| Staging | Proposed bytes are staged, flushed, and fsync'd before commit | PASS |
| Integration transport | MCP server/client path runs successfully | PASS |
| Tool discovery | All four expected tools are exposed | PASS |
| Negative integration checks | Traversal, directory-read, and missing-read failures are observed through MCP | PASS |
| Canonical reproduction | Published source was fetched and reproduced on the working host | PASS |

## Regression Test Distribution

```text
test_read_file.py        6 tests
test_workspace_tools.py  6 tests
test_write_file.py      12 tests
--------------------------------
total                   24 tests
```

## Final Smoke Marker

```text
SHARED_WORKSPACE_MCP_V0_SMOKE_PASS
```

## Accepted Boundaries

The V0 acceptance does **not** claim:

- arbitrary filesystem access;
- generic shell authority;
- Git mutation or publication authority;
- binary-file support;
- directory creation;
- automatic merge/conflict resolution;
- general filesystem locking;
- multi-workspace policy enforcement.

## Evidence Discipline

Acceptance was not based only on the implementation existing.

The project was considered complete only after:

1. intended behavior had been converted into automated regression tests;
2. the full suite passed after final source cleanup;
3. the real MCP transport passed a non-mutating smoke test;
4. the exact published source was positively read back;
5. the working host reconciled to the published source;
6. regression and integration tests passed again from that reconciled state.

This public summary is sanitized. Private repository paths and unrelated project state are intentionally excluded.
