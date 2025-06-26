from rest_framework.decorators import api_view, schema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from matcher.services import get_top_matches
from matcher.db import get_collection

@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})

@extend_schema(
    parameters=[
        OpenApiParameter(name="q", required=True, type=str, description="Query string for matching"),
    ],
    responses={200: dict},  # Optional: you can add serializer later
)
@api_view(["GET"])
def match_question(request):
    question = request.GET.get("q", "").strip()
    if not question:
        return Response({"error": "Missing required query param '?q=...'"}, status=400)

    top_docs = get_top_matches(question=question, collection=get_collection())
    return Response({"results": top_docs})
