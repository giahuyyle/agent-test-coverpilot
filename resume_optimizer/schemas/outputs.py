from typing import Literal
from pydantic import BaseModel

from resume_optimizer.schemas.resume import ResumeJSON


class ATSIssue(BaseModel):
    issue_type: str
    severity: Literal["low", "medium", "high"]
    resume_path: str
    quoted_line: str | None = None
    explanation: str
    fix: str


class SectionDiagnosis(BaseModel):
    section_name: str
    weakest_item_path: str | None = None
    weakest_line: str | None = None
    why_it_fails: str
    recommended_fix: str


class RankedFix(BaseModel):
    rank: int
    resume_path: str
    fix: str
    why_it_matters: str
    before: str | None = None
    after: str | None = None


class ResumeDiagnosis(BaseModel):
    ats_killers: list[ATSIssue]
    section_diagnosis: list[SectionDiagnosis]
    missing_signals: list[str]
    top_5_fixes: list[RankedFix]


class KeywordItem(BaseModel):
    keyword: str
    category: Literal["technical", "soft_skill", "tool", "domain", "other"]
    importance_rank: int
    status: Literal["present", "missing", "buried"]
    resume_path: str | None = None
    note: str


class RecruiterAnalysis(BaseModel):
    top_15_keywords: list[KeywordItem]
    missing_keywords: list[str]
    trending_skills: list[str]
    buzzwords_to_remove: list[str]
    ranked_action_list: list[str]


class BulletChange(BaseModel):
    resume_path: str
    before: str
    after: str
    keywords_added: list[str]
    needs_metric_from_user: bool = False
    metric_question: str | None = None
    why_stronger: str


class ResumeRewriteResult(BaseModel):
    optimized_resume: ResumeJSON
    bullet_changes: list[BulletChange]
    summary_of_changes: list[str]
    warnings: list[str]


class FullOptimizationResult(BaseModel):
    diagnosis: ResumeDiagnosis
    recruiter_analysis: RecruiterAnalysis
    rewrite: ResumeRewriteResult