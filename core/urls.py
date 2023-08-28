from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("posts/", include("apps.posts.urls")),
    path('admin/', admin.site.urls),
]
