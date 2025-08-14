# Analysis Report

## Summary
This draft specifies a testable Smart Prompt Booster (SPB) that converts user-selected images into a Base Prompt and Negative Prompt, supports additive Style Packs (Cinematic, Analog Film, Anime, Product, Portrait) with deterministic merging order, recommends numeric CFG/Steps/sampler ranges, exports syntactically-valid strings for A1111, SDXL, and ComfyUI, and generates Safe/Bold/Experimental variants. The specification emphasizes deterministic outputs, explicit tokens, and automated acceptance tests suitable for QA automation.

## Key design decisions
- Additive Style Packs: Packs are additive by default to allow flexible combinations. Deterministic merge order is Cinematic -> Analog Film -> Anime -> Product -> Portrait. A 'pack priority' override is supported for advanced users.
- Canonical tokens: Each pack has a canonical token set (human-readable) to make automated tests deterministic and simple (string containment checks). These tokens were chosen to be explicit about lighting, composition, camera, and material where relevant.
- Numeric recommendations: Use the ranges provided in clarifications with defaults. Ranges are explicit to allow automated checks for validity.
- Export formats: Chosen per clarifications: A1111 single-line with --neg separator; SDXL pipe-delimited string; ComfyUI with human-readable prompt block plus minimal JSON snippet. Exports are labeled and must be parseable according to specified simple regex/patterns.
- Variants: Safe, Bold, Experimental each have precise rules. Experimental tokens must be flagged with rationales to enable traceability and compliance checks.

## Testability
- Each functional requirement contains at least one GIVEN-WHEN-THEN acceptance test. System-level requirement SPB-0011 mandates generation of at least 9 structured acceptance test artifacts mirroring the policy acceptance_test_format and SPB- prefix, enabling automated QA ingestion.
- For export parseability tests, simple regex patterns and delimiter parsing are specified so automated parsers can verify correctness.
- Negative prompt constraints (non-empty, <2000 chars, >=3 tokens) are specified to enable deterministic checks.

## Safety and compliance
- The system must avoid banned phrases and explicit real-person/celebrity likenesses. The Safe variant includes explicit negative tokens for 'real person likeness' and 'celebrity'. User attempts to request exact celebrity likeness must be sanitized or refused.
- Experimental tokens must be clearly labeled and accompanied by rationale to ensure reviewers can understand deviations from standard tokens.

## Implementation notes for engineers
- Image ingestion must return an image reference id and metadata for traceability.
- Image analysis should return confidence scores; if confidence < threshold, default to user text and mark analysis unavailable.
- Implement canonical pack metadata as part of API (tokens, cfg defaults and ranges, steps defaults and ranges, samplers) to allow clients and QA to fetch and assert values.
- Exports should include adjacent metadata block (JSON) listing allowed min/max for CFG and Steps for transparency; users may override with explicit warnings.
- Implement deterministic merging and de-duplication; include 'merge_trace' in output showing source pack for each token and any override events.

## How acceptance tests map to requirements
- SPB-1001..1003 map to image ingestion (SPB-0001).
- SPB-2001..2002 map to image analysis (SPB-0002).
- SPB-3001..3002 validate Base Prompt generation (SPB-0003).
- SPB-4001..4002 validate Negative Prompt constraints and celebrity sanitization (SPB-0004).
- SPB-5001..5003, SPB-6001..6002, SPB-7001..7002 validate Style Pack behavior, tokens, numeric ranges and deterministic merging (SPB-0005, SPB-0006, SPB-0007).
- SPB-8001..8003 validate Export formats and parseability (SPB-0008).
- SPB-9001..9003 validate variant behaviors and experimental token rationale (SPB-0009).
- SPB-11001 validates that the system emits structured acceptance test artifacts per policy.

## Trace to policy and clarifications
- ID prefix SPB- applied consistently to requirement IDs and acceptance test IDs.
- Outputs structured per policy ordering preference where applicable.
- Negative prompt constraints and banned-phrases handling follow policy.
- Numeric ranges for packs reflect clarification suggestions and are explicitly documented.
- Additive behavior and deterministic pack order follow clarification answers.

## Remaining decisions / open items
See 'open_questions' in requirements for items requiring stakeholder decisions prior to implementation.

## Final notes
This draft strikes a balance between safety, usability, and testability: all token sets and numeric ranges are explicit to enable automated tests; exports are syntactically constrained (regex/delimiter rules) to allow parsers to validate them; variants are clearly defined with safety and traceability rules. Implementers should ensure logs and merge_traces are available to debug rare composition edge-cases and to satisfy compliance review requests.