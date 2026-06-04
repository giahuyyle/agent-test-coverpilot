from resume_optimizer.schemas.optimizer import ResumeOptimizerInput


def validate_optimizer_input(data: ResumeOptimizerInput) -> list[str]:
    errors = []

    if not data.target_role.strip():
        errors.append("target_role is required.")

    if not data.industry.strip():
        errors.append("industry is required.")

    if not data.seniority:
        errors.append("seniority is required.")

    if not data.resume.full_name.strip():
        errors.append("resume.full_name is required.")

    has_resume_content = (
        bool(data.resume.experience)
        or bool(data.resume.projects)
        or bool(data.resume.education)
    )

    if not has_resume_content:
        errors.append("Resume must include experience, projects, or education.")

    return errors