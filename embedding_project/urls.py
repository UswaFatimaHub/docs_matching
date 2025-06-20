from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("matcher/", include("matcher.urls")),  # << This is essential
]
