from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts endpoints (register, login, profile)
    path("api/accounts/", include("accounts.urls")),

    # Posts & comments endpoints
    path("api/", include("posts.urls")),

    # Notifications endpoints

    path("api/notifications/", include("notifications.urls")),

]

# Serve media files (profile pictures) in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
