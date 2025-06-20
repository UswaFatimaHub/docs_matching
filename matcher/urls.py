from django.urls import path
from .views import match_question

urlpatterns = [
    path("match/", match_question, name="match-question"),
]
