from __future__ import annotations
import argparse, os, json, time, pathlib, sys
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from crewai import Crew, Process
from langsmith import traceable
from .agents import make_agents
from .tasks import build_policy_task, build_draft_task, build_validate_task
from .models import PolicyClarifications, DraftOutput, ValidationResult, RequirementsModel

console = Console()

def _artifacts_dir() -> str:
    ts = time.strftime("%Y%m%d-%H%M%S")
    out = pathlib.Path("artifacts") / ts
    out.mkdir(parents=True, exist_ok=True)
    return str(out)

@traceable(name="run_pipeline")
def run_pipeline(spec: str, model_name: str):
    p_agent, d_agent, v_agent = make_agents(model_name=model_name)
    task_policy = build_policy_task(p_agent, spec)
    task_draft  = build_draft_task(d_agent, spec)
    task_valid  = build_validate_task(v_agent)
    crew = Crew(agents=[p_agent, d_agent, v_agent], tasks=[task_policy, task_draft, task_valid], process=Process.sequential, verbose=True)
    console.rule("[bold cyan]Kicking off Crew")
    crew.kickoff(inputs={})
    pol_out: PolicyClarifications = task_policy.output.pydantic  # type: ignore
    draft_out: DraftOutput = task_draft.output.pydantic          # type: ignore
    val_out: ValidationResult = task_valid.output.pydantic       # type: ignore
    req: RequirementsModel = draft_out.requirements
    if val_out.repaired_requirements:
        req = val_out.repaired_requirements
    out_dir = _artifacts_dir()
    req_path = os.path.join(out_dir, "requirements.json")
    rep_path = os.path.join(out_dir, "analysis_report.md")
    fin_path = os.path.join(out_dir, "findings.json")
    pol_path = os.path.join(out_dir, "policy.json")
    clar_path = os.path.join(out_dir, "clarifications.json")
    with open(req_path, "w", encoding="utf-8") as f: json.dump(req.model_dump(), f, ensure_ascii=False, indent=2)
    with open(rep_path, "w", encoding="utf-8") as f: f.write(draft_out.analysis_report_md)
    with open(fin_path, "w", encoding="utf-8") as f: json.dump(val_out.model_dump(), f, ensure_ascii=False, indent=2)
    with open(pol_path, "w", encoding="utf-8") as f: json.dump(pol_out.policy.model_dump(), f, ensure_ascii=False, indent=2)
    with open(clar_path, "w", encoding="utf-8") as f: json.dump([c.model_dump() for c in pol_out.clarifications], f, ensure_ascii=False, indent=2)
    table = Table(title="Validator Findings (WARN only)")
    table.add_column("#", justify="right"); table.add_column("Severity"); table.add_column("Message"); table.add_column("Location")
    for idx, f in enumerate(val_out.findings, 1): table.add_row(str(idx), f.severity, f.message, f.location or "-")
    console.print(table)
    return {"artifacts_dir": out_dir, "paths": [req_path, rep_path, fin_path, pol_path, clar_path]}

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run Requirements Writer Crew")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--spec", type=str)
    src.add_argument("--spec-file", type=str)
    parser.add_argument("--model", type=str, default=os.getenv("OPENAI_MODEL_NAME", "gpt-5-mini-2025-08-07"))
    args = parser.parse_args()
    spec = args.spec
    if args.spec_file:
        with open(args.spec_file, "r", encoding="utf-8") as f: spec = f.read()
    if not spec or not spec.strip():
        print("Empty spec.", file=sys.stderr); sys.exit(2)
    res = run_pipeline(spec.strip(), args.model)
    console.print(f"[green]Artifacts written to:[/] {res['artifacts_dir']}")
    for p in res["paths"]: console.print(f"- {p}")
if __name__ == "__main__": main()
