from pydantic import BaseModel, Field


class BasicInfo(BaseModel):
    phone_country_code: str = "+1"
    phone: str = ""
    contact_email: str = ""
    location: str = ""
    headline: str = ""
    github_url: str = ""
    linkedin_url: str = ""
    portfolio_url: str = ""
    summary: str = ""


class ExperienceItem(BaseModel):
    company: str = ""
    role: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    is_current: bool = False
    description: list[str] = Field(default_factory=list)


class ProjectItem(BaseModel):
    name: str = ""
    label: str = ""
    stack: list[str] = Field(default_factory=list)
    description: list[str] = Field(default_factory=list)
    live_url: str = ""
    github_url: str = ""
    start_date: str = ""
    end_date: str = ""


class EducationItem(BaseModel):
    school: str = ""
    degree: str = ""
    major: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    gpa: str = ""
    awards: list[str] = Field(default_factory=list)
    relevant_coursework: list[str] = Field(default_factory=list)


class CertificateItem(BaseModel):
    name: str = ""
    issuer: str = ""
    issue_date: str = ""
    expiration_date: str = ""
    credential_id: str = ""
    credential_url: str = ""


class SkillItem(BaseModel):
    name: str = ""
    category: str = ""


class ResumeJSON(BaseModel):
    full_name: str = ""
    display_name: str = ""
    basic: BasicInfo = Field(default_factory=BasicInfo)
    experience: list[ExperienceItem] = Field(default_factory=list)
    projects: list[ProjectItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    certificates: list[CertificateItem] = Field(default_factory=list)
    skills: list[SkillItem] = Field(default_factory=list)