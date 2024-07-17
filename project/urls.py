from django.contrib import admin
from django.conf.urls import handler404
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.site.site_title = "PORTFOLIO WEBSITE"
admin.site.site_header = "Administration PORTFOLIO"
admin.site.index_title = "PORTFOLIO WEBSITE ADMIN"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("application.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
