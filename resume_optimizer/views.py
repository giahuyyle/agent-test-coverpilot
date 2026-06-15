import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError

from resume_optimizer.schemas.optimizer import ResumeOptimizerInput
from resume_optimizer.services.optimizer import run_resume_optimizer
from resume_optimizer.utils.validators import validate_optimizer_input


SAMPLE_RESUME_JSON = {
    "full_name": "Huy Le",
    "display_name": "Huy",
    "basic": {
        "phone_country_code": "+1",
        "phone": "",
        "contact_email": "huy@example.com",
        "location": "Edmonton, AB",
        "headline": "",
        "github_url": "",
        "linkedin_url": "",
        "portfolio_url": "",
        "summary": ""
    },
    "experience": [
        {
            "company": "FarmTracker",
            "role": "Software Developer",
            "location": "Remote",
            "start_date": "2026-05",
            "end_date": "",
            "is_current": True,
            "description": [
                "Built a farm tracking app using Node.js and Express.",
                "Worked on livestock records.",
                "Used GitHub."
            ]
        }
    ],
    "projects": [],
    "education": [],
    "certificates": [],
    "skills": [
        {"name": "Python", "category": "Programming"},
        {"name": "JavaScript", "category": "Programming"},
        {"name": "Git", "category": "Tools"}
    ]
}


@csrf_exempt
def optimize_resume_view(request):
    """
    JSON API endpoint.

    POST /api/resume/optimize/
    """
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405,
        )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON body."},
            status=400,
        )

    try:
        data = ResumeOptimizerInput.model_validate(body)
    except ValidationError as e:
        return JsonResponse(
            {"error": "Invalid request schema.", "details": e.errors()},
            status=400,
        )

    validation_errors = validate_optimizer_input(data)
    if validation_errors:
        return JsonResponse(
            {"error": "Validation failed.", "details": validation_errors},
            status=400,
        )

    try:
        result = run_resume_optimizer(data)
        return JsonResponse(result.model_dump(), status=200)
    except Exception as e:
        return JsonResponse(
            {"error": "Resume optimization failed.", "details": str(e)},
            status=500,
        )


def optimize_resume_ui_view(request):
    """
    Simple browser interface.

    GET  /api/resume/optimize-ui/
    POST /api/resume/optimize-ui/
    """
    if request.method == "GET":
        return render(
            request,
            "resume_optimizer/optimize_form.html",
            {
                "sample_resume_json": json.dumps(SAMPLE_RESUME_JSON, indent=2),
            },
        )

    target_role = request.POST.get("target_role", "").strip()
    industry = request.POST.get("industry", "").strip()
    seniority = request.POST.get("seniority", "").strip()
    target_companies_raw = request.POST.get("target_companies", "").strip()
    resume_json_raw = request.POST.get("resume_json", "").strip()

    errors = []

    if not target_role:
        errors.append("Target role is required.")

    if not industry:
        errors.append("Industry is required.")

    if seniority not in ["junior", "mid", "senior", "lead"]:
        errors.append("Seniority must be junior, mid, senior, or lead.")

    try:
        resume_dict = json.loads(resume_json_raw)
    except json.JSONDecodeError:
        resume_dict = None
        errors.append("Resume JSON is invalid.")

    target_companies = None
    if target_companies_raw:
        target_companies = [
            company.strip()
            for company in target_companies_raw.split(",")
            if company.strip()
        ]

    if errors:
        return render(
            request,
            "resume_optimizer/optimize_form.html",
            {
                "errors": errors,
                "target_role": target_role,
                "industry": industry,
                "seniority": seniority,
                "target_companies": target_companies_raw,
                "sample_resume_json": resume_json_raw or json.dumps(SAMPLE_RESUME_JSON, indent=2),
            },
        )

    request_data = {
        "target_role": target_role,
        "industry": industry,
        "seniority": seniority,
        "resume": resume_dict,
        "target_companies": target_companies,
    }

    try:
        data = ResumeOptimizerInput.model_validate(request_data)
    except ValidationError as e:
        return render(
            request,
            "resume_optimizer/optimize_form.html",
            {
                "errors": ["Invalid request schema.", str(e)],
                "target_role": target_role,
                "industry": industry,
                "seniority": seniority,
                "target_companies": target_companies_raw,
                "sample_resume_json": resume_json_raw,
            },
        )

    validation_errors = validate_optimizer_input(data)
    if validation_errors:
        return render(
            request,
            "resume_optimizer/optimize_form.html",
            {
                "errors": validation_errors,
                "target_role": target_role,
                "industry": industry,
                "seniority": seniority,
                "target_companies": target_companies_raw,
                "sample_resume_json": resume_json_raw,
            },
        )

    try:
        result = run_resume_optimizer(data)
        result_dict = result.model_dump()

        return render(
            request,
            "resume_optimizer/optimize_result.html",
            {
                "result": result_dict,
                "result_json": json.dumps(result_dict, indent=2),
            },
        )

    except Exception as e:
        return render(
            request,
            "resume_optimizer/optimize_form.html",
            {
                "errors": [f"Resume optimization failed: {str(e)}"],
                "target_role": target_role,
                "industry": industry,
                "seniority": seniority,
                "target_companies": target_companies_raw,
                "sample_resume_json": resume_json_raw,
            },
        )