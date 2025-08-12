Analysis and mapping to policy and clarifications

Summary
- This requirements document defines an SPB (Smart Prompt Booster) that ingests a user-selected image and generates labeled base_prompt and negative_prompt outputs, plus modular Style Packs (cinematic, analog film, anime, product, portrait). The system supports user-defined packs, deterministic pack merging with deduplication, Safe/Bold/Experimental variants with recommended CFG/steps/sampler ranges and defaults, and platform-ready exports for A1111, SDXL, and ComfyUI.

Mapping to policy/style rules
- ID prefix: All acceptance test IDs use the configured prefix 'SPB' per policy.
- base_prompt and negative_prompt: Every requirement and test uses exactly these field names as required.
- Style Packs: Default five packs are required and shipped; user-defined packs supported with same schema and validation.
- Pack toggles: Implemented at pack-level and required; subcomponent toggles are optional (documented as future work).
- Variant guidance: Safe/Bold/Experimental each include ranges and defaults for CFG and steps and ordered sampler lists; defaults lie within ranges.
- Exports: Provided three exports per variant with platform-expected wrappers and explicit model-sensitive token marking for SDXL.
- Merging: Deterministic concatenation algorithm is defined (base first, default pack order, then user packs in registration order) with exact-string deduplication and documented precedence.
- Rationales: Each FR includes short rationales where the choice may be non-obvious.
- Safety: Safety-by-default is enforced: Safe variant sanitizes disallowed content; all variants run a safety scan and reject disallowed content.
- Test format: Acceptance tests follow the policy-specified given/when/then strings with machine-checkable pass_criteria assertions (presence/absence substrings, numeric range checks, metadata flags). Tests use SPB-0001.. numbering.

Design choices and justifications
- Pack order: Default pack order chosen to be [cinematic, analog film, anime, product, portrait] for deterministic behavior. User packs appended in registration order to avoid ambiguous sorting and to preserve user intent.
- Merge precedence: Base prompt tokens first to preserve image-specific descriptions; packs add style tokens while not overwriting base semantics.
- Deduplication: Exact-string deduplication is simple and deterministic; semantic deduplication is error-prone, so initial implementation is exact-string only; future versions may add optional semantic merging.
- CFG/steps ranges: Ranges chosen to provide conservative Safe defaults (lower CFG, fewer steps) and broader Experimental ranges to support creative exploration; defaults chosen near midpoints or slightly higher for quality.
- Export formats: We provide commonly-accepted, copy-paste-friendly formats. SDXL includes explicit marking for SDXL-only tokens to avoid misapplication across engines.

Testing coverage
- Each functional requirement includes at least one acceptance test. Tests check: correct field names, pack toggles respected, tokens merged in required order, exact-string deduplication, presence of model-sensitive markers, safety sanitization, export correctness (presence of required flags, JSON-like structure for ComfyUI), warning flags for long prompts, and user pack registration/validation.

Security and safety considerations
- All user-provided content (packs, tokens, metadata) must be sanitized. The Safe variant removes or neutralizes disallowed descriptors. Experimental variants may include advanced or 'hack' tokens only when not disallowed and are clearly labeled.

Implementation notes for engineers (concise)
- Provide deterministic string concatenation function: output = join_nonempty([base_tokens, tokens_from_packs_in_order]) with exact-string deduplication preserving first occurrence.
- Maintain pack registry with metadata: {name, description, tokens[], subcomponents?, model_sensitive_markers[]}.
- Safety scanner: run on pack registration and on every variant generation. Block and log disallowed tokens, and return sanitized outputs plus evidence of removal in metadata.
- Exports: produce three strings per variant using the patterns in the tests; include model-sensitive token annotations for SDXL exports.

Remaining clarifications
- Confirm whether SDXL export single-line JSON or comment-style suffix is preferred by integration partners; current spec uses JSON-like suffix for compatibility.
- Decide whether user-defined packs require admin approval before being visible to other users in shared deployments.

This analysis report documents choices influenced by the provided policy and clarifications and highlights how the acceptance tests and functional requirements implement the mandated behaviors and safety constraints.