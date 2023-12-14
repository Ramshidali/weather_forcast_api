from django.contrib import admin
from django.views.static import serve
from django.urls import path, re_path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/weather_report/', include(('api.v1.weather_report.urls','weather_report'))),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
