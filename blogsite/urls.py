from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.accounts.api_password_reset import PasswordResetRequest, PasswordResetConfirm
from django.views.generic import TemplateView
from blog.pages.views import landing

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", TemplateView.as_view(template_name="landing.html"), name="home"),
    path("", landing, name="home"),
    path("", include(("blog.urls", "blog"), namespace="blog")),
    path("api/", include("rest_framework.urls")),
    path("api/auth/password/reset/",  PasswordResetRequest.as_view(),  name="password-reset"),
    path("api/auth/password/confirm/", PasswordResetConfirm.as_view(), name="password-reset-confirm"),
] + (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.DEBUG else [])
