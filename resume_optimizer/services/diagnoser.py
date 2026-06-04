from resume_optimizer.services.llm import llm
from resume_optimizer.schemas.optimizer import ResumeOptimizerInput
from resume_optimizer.schemas.outputs import ResumeDiagnosis
from resume_optimizer.prompts.diagnoser import DIAGNOSER_PROMPT


def diagnose_resume(data: ResumeOptimizerInput) -> ResumeDiagnosis:
    structured_llm = llm.with_structured_output(ResumeDiagnosis)

    prompt = DIAGNOSER_PROMPT.format(
        target_role=data.target_role,
        industry=data.industry,
        seniority=data.seniority,
        resume_json=data.resume.model_dump_json(indent=2),
    )

    return structured_llm.invoke(prompt)