from rest_framework import viewsets, permissions
from .models import Patient
from .serializers import PatientSerializer
from apps.accounts.permissions import IsStaffOrAdmin
from apps.audit.utils import record_audit

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('-id')
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['code', 'full_name', 'phone', 'identity_number', 'address']
    filterset_fields = ['gender', 'is_active', 'blood_type']

    def perform_create(self, serializer):
        instance = serializer.save()
        record_audit(self.request, "CREATE", "Patient", instance.id, f"Thêm mới bệnh nhân: {instance.full_name} ({instance.code})")

    def perform_update(self, serializer):
        instance = serializer.save()
        record_audit(self.request, "UPDATE", "Patient", instance.id, f"Cập nhật hồ sơ bệnh nhân: {instance.code}")

    def perform_destroy(self, instance):
        code = instance.code
        name = instance.full_name
        idx = instance.id
        instance.delete()
        record_audit(self.request, "DELETE", "Patient", idx, f"Xóa hồ sơ bệnh nhân: {name} ({code})")
