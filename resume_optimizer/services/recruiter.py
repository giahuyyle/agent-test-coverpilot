from resume_optimizer.services.llm import llm
from resume_optimizer.schemas.optimizer import ResumeOptimizerInput
from resume_optimizer.schemas.outputs import RecruiterAnalysis
from resume_optimizer.prompts.recruiter import RECRUITER_PROMPT


def recruiter_review(data: ResumeOptimizerInput) -> RecruiterAnalysis:
    structured_llm = llm.with_structured_output(RecruiterAnalysis)

    prompt = RECRUITER_PROMPT.format(
        target_role=data.target_role,
        industry=data.industry,
        seniority=data.seniority,
        target_companies=data.target_companies or "Any",
        resume_json=data.resume.model_dump_json(indent=2),
    )

    return structured_llm.invoke(prompt)