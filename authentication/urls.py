from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("users.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
