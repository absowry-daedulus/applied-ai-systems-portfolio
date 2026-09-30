# Fresh-Session Discovery Failure and Recovery

**Status:** Completed regression sequence — sanitized public record

## Goal

Test whether a fresh AI session could reconstruct project state from an external canonical source without relying on prior conversational context.

## Failure

The first isolated session could not deterministically locate the canonical source. It stopped instead of substituting remembered or inferred state.

The failure exposed a circular dependency: the reconstruction instructions lived inside the source that had not yet been located.

## Correction

A small Stage 0 locator was separated from project state. It identifies the expected canonical source and requires positive identity verification before the bootstrap contract or current state can be trusted. The locator contains no project state.

## Retest

A second isolated session resolved and verified the canonical source, retrieved the bootstrap contract and current state, checked event-ledger agreement, reconstructed the active operating constraints and resume target, and completed a cross-session read/write handoff.

## Boundary

This result supports the tested hosted-session workflow. It does not establish continuity across arbitrary models, providers, or runtimes.
