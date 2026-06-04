from resume_optimizer.services.llm import llm
from resume_optimizer.schemas.optimizer import ResumeOptimizerInput
from resume_optimizer.schemas.outputs import (
    ResumeDiagnosis,
    RecruiterAnalysis,
    ResumeRewriteResult,
)
from resume_optimizer.prompts.rewriter import REWRITER_PROMPT


def rewrite_resume(
    data: ResumeOptimizerInput,
    diagnosis: ResumeDiagnosis,
    recruiter_analysis: RecruiterAnalysis,
) -> ResumeRewriteResult:
    structured_llm = llm.with_structured_output(ResumeRewriteResult)

    prompt = REWRITER_PROMPT.format(
        target_role=data.target_role,
        industry=data.industry,
        seniority=data.seniority,
        resume_json=data.resume.model_dump_json(indent=2),
        diagnosis_json=diagnosis.model_dump_json(indent=2),
        recruiter_json=recruiter_analysis.model_dump_json(indent=2),
    )

    return structured_llm.invoke(prompt)