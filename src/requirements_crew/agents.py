from __future__ import annotations
from crewai import Agent
from .llm import make_llm

def make_agents(model_name: str = "gpt-5-mini-2025-08-07"):
    # Build a LangChain ChatOpenAI so LangSmith can trace LLM calls
    llm = make_llm()

    policy_clarifier = Agent(
        role="Policy & Clarification Analyst",
        goal="Define house policy and resolve ambiguities with proposed answers.",
        backstory="Senior BA who anticipates gaps early.",
        llm=llm,
        verbose=True,
    )

    drafter = Agent(
        role="Requirements Drafter",
        goal="Write unambiguous, testable functional requirements with acceptance tests.",
        backstory="Seasoned analyst producing crisp, testable specs.",
        llm=llm,
        verbose=True,
    )

    validator = Agent(
        role="Requirements Auditor",
        goal="Detect contradictions, unverifiable language, passive voice, missing tests, and numbering issues.",
        backstory="Warn-only quality gate enforcing style rules and testability.",
        llm=llm,
        verbose=True,
    )

    return policy_clarifier, drafter, validator
