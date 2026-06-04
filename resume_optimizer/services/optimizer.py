from resume_optimizer.schemas.optimizer import ResumeOptimizerInput
from resume_optimizer.schemas.outputs import FullOptimizationResult
from resume_optimizer.services.diagnoser import diagnose_resume
from resume_optimizer.services.recruiter import recruiter_review
from resume_optimizer.services.rewriter import rewrite_resume


def run_resume_optimizer(data: ResumeOptimizerInput) -> FullOptimizationResult:
    diagnosis = diagnose_resume(data)
    recruiter_analysis = recruiter_review(data)

    rewrite = rewrite_resume(
        data=data,
        diagnosis=diagnosis,
        recruiter_analysis=recruiter_analysis,
    )

    return FullOptimizationResult(
        diagnosis=diagnosis,
        recruiter_analysis=recruiter_analysis,
        rewrite=rewrite,
    )