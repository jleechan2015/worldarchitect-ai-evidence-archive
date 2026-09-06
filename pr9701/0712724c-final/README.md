# PR9701 legacy-helper ordering and exploratory baseline evidence

Current review head: `0712724c81144dd97029a91182dfea6bfd984635`.
Actual A/B control: `54b3a564624c9a7b3bc63f7ddc039ff9e93ab9a1`;
treatment: `5bc8d1b9be2801068980e614de37de8c23ae538f`.
The complete capture-to-current diff changes only test/evidence files, not
application runtime or prompt bytes. Capture SHAs are never relabeled.

## Incremental claim and direct proof

Against the current stacked base, active PlanningAgent/LevelUpAgent tuples were
already aligned. The executable application change is ordering consistency in
the legacy `PromptBuilder.build_think_mode_instructions` helper. No production
caller was found. This PR does not claim an active-route prompt migration or
causal cache improvement from that helper change.

`legacy-helper/red.cast` and `green.cast` record the IDENTICAL current test
`test_prompt_builder_think_mode_instructions_starts_with_canonical_base_prefix`.
Base `30dbaeee` fails one assertion, treatment `6b47a736` passes. Source blobs
and identical test hashes are recorded. This is deterministic unit-contract
evidence, not real-provider RED/GREEN. RED's unrelated modified CI fixture was
not imported; actual helper bytes equal the declared Git blob.

## Supporting real-service evidence

All five predeclared matched blocks completed: ten arms, 100 native HTTP
exchanges, 90 streaming request IDs, 60 measured turns. Independent BQ/model
review verified the raw identity and token receipts. PlanningAgent delta is
-0.226968 percentage points, BCa95% [-1.248640, 0.813026], p=0.8125.
LevelUpAgent delta is +0.968236 points, BCa95% [-0.823266, 4.475794], p=0.5625.
Five blocks are exploratory; the predeclared confirmatory minimum is24.
No statistically significant improvement, confirmatory no-harm, equivalence,
population economics or deployed-service result is claimed. This active-route
A/B is supporting exploratory baseline evidence, not execution of the changed
legacy helper. No further provider experiment was performed for publication.

## Public projection and media

Original captures remain immutable. This current package discloses host-path-only
redaction in `publication-projection.json`, with original/published hashes for
every source file. JSON string escaping is preserved. The projected capture
manifest and checksum sidecars are regenerated for projected bytes; historical
original manifests are explicitly retained for provenance, not current checks.
Native response payload bodies and base64 transport content are not replaced.

Historical unsanitized terminal media remains in the older immutable packet and
is not the current visual claim. Current terminal GIF/MP4 derives from the actual
same-test RED/GREEN casts after disclosed host-path projection, with a separate
caption strip. No test output is invented or replaced. The older offline cast
records validation at eb95 and is historical, not a current-head runtime run.

`REPRODUCIBILITY.md` supplies literal clone/checkout/setup and fresh-output
commands. `verify_offline.py` checks all686 projected original-manifest entries
and all10 native transport contracts. `reproduce-helper.py` runs the identical
current test against an explicitly chosen checkout. Neither makes model calls.

This packet does not claim browser UI, active-route performance improvement,
whole-fleet approval, /ready or merge authorization. Independent re-review of
this offline correction is pending.
