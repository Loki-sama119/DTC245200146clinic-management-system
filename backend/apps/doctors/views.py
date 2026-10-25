from rest_framework import viewsets, permissions
from .models import Doctor
from .serializers import DoctorSerializer
from apps.accounts.permissions import IsAdminRole
from apps.audit.utils import record_audit

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('user', 'specialty').all().order_by('code')
    serializer_class = DoctorSerializer
    filterset_fields = ['specialty', 'is_active']
    search_fields = ['code', 'user__first_name', 'user__last_name', 'phone', 'specialty__name', 'room_number']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        instance = serializer.save()
        record_audit(self.request, "CREATE", "Doctor", instance.id, f"Thêm bác sĩ mới: {instance.code}")

    def perform_update(self, serializer):
        instance = serializer.save()
        record_audit(self.request, "UPDATE", "Doctor", instance.id, f"Cập nhật bác sĩ: {instance.code}")

    def perform_destroy(self, instance):
        code = instance.code
        idx = instance.id
        instance.delete()
        record_audit(self.request, "DELETE", "Doctor", idx, f"Xóa bác sĩ: {code}")
