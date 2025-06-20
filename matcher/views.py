from django.http import JsonResponse
from .services import get_top_matches

def match_question(request):
    question = request.GET.get("q", "").strip()
    if not question:
        return JsonResponse({"error": "Missing required query param '?q=...'"}, status=400)

    top_docs = get_top_matches(question)
    return JsonResponse({"results": top_docs})
