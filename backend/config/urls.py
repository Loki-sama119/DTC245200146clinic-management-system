from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connection
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
import prometheus_client
from django.http import HttpResponse

def health_check(request):
    """Healthcheck endpoint cho Docker, Nginx và Monitoring."""
    db_status = "healthy"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    status_code = 200 if "unhealthy" not in db_status else 503
    return JsonResponse({
        "status": "healthy" if status_code == 200 else "degraded",
        "service": "clinic-backend",
        "database": db_status,
        "version": "1.0.0"
    }, status=status_code)

def metrics_view(request):
    """Endpoint trả về Prometheus metrics chuẩn text/plain."""
    return HttpResponse(
        prometheus_client.generate_latest(),
        content_type=prometheus_client.CONTENT_TYPE_LATEST
    )

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health & Observability Endpoints
    path('api/health/', health_check, name='health-check'),
    path('api/metrics/', metrics_view, name='metrics'),

    # OpenAPI / Swagger Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Business Logic APIs
    path('api/auth/', include('apps.accounts.urls')),
    path('api/specialties/', include('apps.specialties.urls')),
    path('api/doctors/', include('apps.doctors.urls')),
    path('api/patients/', include('apps.patients.urls')),
    path('api/appointments/', include('apps.appointments.urls')),
    path('api/medical-records/', include('apps.medical_records.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/audit/', include('apps.audit.urls')),
]
