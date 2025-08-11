from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Clarification(BaseModel):
    question: str
    proposed_answer: str
    confidence: float = Field(ge=0.0, le=1.0)

class Policy(BaseModel):
    id_prefix: str = "FR"
    style_rules: List[str] = []
    banned_phrases: List[str] = ["TBD", "etc.", "and so on"]
    acceptance_test_format: str = "GIVEN-WHEN-THEN"
    wording_tone: str = "imperative, unambiguous, testable"

class PolicyClarifications(BaseModel):
    policy: Policy
    clarifications: List[Clarification]

class AcceptanceTest(BaseModel):
    id: str
    given: str
    when: str
    then: str

class FunctionalRequirement(BaseModel):
    id: str
    statement: str
    rationale: Optional[str] = None
    acceptance_tests: List[AcceptanceTest]
    priority: Literal["MUST","SHOULD","COULD"] = "MUST"
    dependencies: List[str] = []

class NonFunctional(BaseModel):
    performance: Optional[str] = None
    security: Optional[str] = None
    reliability: Optional[str] = None
    usability: Optional[str] = None
    compliance: Optional[str] = None

class Context(BaseModel):
    business_goal: Optional[str] = None
    stakeholders: List[str] = []
    assumptions: List[str] = []
    out_of_scope: List[str] = []
    non_functional: NonFunctional = NonFunctional()

class RequirementsModel(BaseModel):
    meta: dict
    context: Context = Context()
    functional_requirements: List[FunctionalRequirement]
    risks: List[dict] = []
    open_questions: List[str] = []

class Finding(BaseModel):
    severity: Literal["low","medium","high"]
    message: str
    location: Optional[str] = None
    suggestion: Optional[str] = None

class ValidationResult(BaseModel):
    findings: List[Finding]
    repaired_requirements: Optional[RequirementsModel] = None

class DraftOutput(BaseModel):
    requirements: RequirementsModel
    analysis_report_md: str
