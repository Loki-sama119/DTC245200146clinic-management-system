from rest_framework import viewsets, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer
from apps.accounts.permissions import IsAdminRole

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().select_related('user').order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminRole]
    filterset_fields = ['action', 'model_name']
    search_fields = ['details', 'object_id', 'ip_address', 'user__username']
