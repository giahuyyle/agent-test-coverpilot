import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError

from resume_optimizer.schemas.optimizer import ResumeOptimizerInput
from resume_optimizer.services.optimizer import run_resume_optimizer
from resume_optimizer.utils.validators import validate_optimizer_input


@csrf_exempt
def optimize_resume_view(request):
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

        return JsonResponse(
            result.model_dump(),
            status=200,
        )

    except Exception as e:
        return JsonResponse(
            {"error": "Resume optimization failed.", "details": str(e)},
            status=500,
        )