from rest_framework import viewsets, permissions
from .models import Specialty
from .serializers import SpecialtySerializer
from apps.accounts.permissions import IsAdminRole
from apps.audit.utils import record_audit

class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all().order_by('name')
    serializer_class = SpecialtySerializer
    search_fields = ['name', 'code', 'description']
    filterset_fields = ['is_active']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        instance = serializer.save()
        record_audit(self.request, "CREATE", "Specialty", instance.id, f"Tạo chuyên khoa mới: {instance.name}")

    def perform_update(self, serializer):
        instance = serializer.save()
        record_audit(self.request, "UPDATE", "Specialty", instance.id, f"Cập nhật chuyên khoa: {instance.name}")

    def perform_destroy(self, instance):
        name = instance.name
        idx = instance.id
        instance.delete()
        record_audit(self.request, "DELETE", "Specialty", idx, f"Xóa chuyên khoa: {name}")
