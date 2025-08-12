from __future__ import annotations
from crewai import Task
from textwrap import dedent
from .models import PolicyClarifications, DraftOutput, ValidationResult

def build_policy_task(agent, spec: str) -> Task:
    return Task(
        description=dedent(f"""
            You receive the following raw spec:
            ---
            {spec}
            ---
            1) Derive a house policy (tone, style rules, banned phrases, acceptance test format, ID prefix).
            2) List top uncertainties as clarification questions; propose an answer and confidence for each.
            Output MUST be a valid PolicyClarifications (JSON only).
        """).strip(),
        expected_output="JSON only policy+clarifications per pydantic model.",
        agent=agent,
        output_pydantic=PolicyClarifications,
    )

def build_draft_task(agent, spec: str) -> Task:
    return Task(
        description=dedent(f"""
            Use the approved policy and clarifications to write a requirements document for the spec:
            ---
            {spec}
            ---
            Requirements MUST be unambiguous, imperative, and testable with GIVEN-WHEN-THEN tests.
            Output MUST be a valid DraftOutput JSON (requirements + analysis_report_md).
        """).strip(),
        expected_output="JSON only DraftOutput (requirements + analysis_report_md).",
        agent=agent,
        output_pydantic=DraftOutput,
        depends_on=[],
    )

def build_validate_task(agent) -> Task:
    return Task(
        description=dedent(f"""
            Validate the provided requirements against the policy.
            Severity: low|medium|high. WARN-ONLY: never block.

            IMPORTANT OUTPUT RULES:
            - Only include "repaired_requirements" if you can return a COMPLETE RequirementsModel,
              including a non-empty "functional_requirements" array AND a "meta" object.
            - If you cannot produce a COMPLETE repair, set "repaired_requirements": null.
            - Never emit partial or placeholder objects for "repaired_requirements".
            - Output MUST be valid JSON for ValidationResult. No commentary outside JSON.
        """).strip(),
        expected_output="JSON only ValidationResult with findings and optional repaired_requirements.",
        agent=agent,
        output_pydantic=ValidationResult,
    )
