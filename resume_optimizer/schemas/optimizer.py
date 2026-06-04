from typing import Literal
from pydantic import BaseModel

from resume_optimizer.schemas.resume import ResumeJSON


class ResumeOptimizerInput(BaseModel):
    target_role: str
    industry: str
    seniority: Literal["intern", "junior", "mid", "senior", "lead"]
    resume: ResumeJSON
    target_companies: list[str] | None = None