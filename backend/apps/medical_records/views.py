from rest_framework import viewsets, permissions, exceptions
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from apps.accounts.permissions import IsDoctorRole, IsAdminRole
from apps.audit.utils import record_audit

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.select_related('patient', 'doctor', 'doctor__user', 'appointment').all().order_by('-created_at')
    serializer_class = MedicalRecordSerializer
    filterset_fields = ['patient', 'doctor', 'appointment']
    search_fields = ['code', 'patient__full_name', 'patient__phone', 'diagnosis', 'symptoms']

    def get_permissions(self):
        # Bác sĩ hoặc Admin mới có quyền tạo/sửa bệnh án
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), (IsDoctorRole | IsAdminRole)()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role not in ['DOCTOR', 'ADMIN'] and not user.is_superuser:
            raise exceptions.PermissionDenied("Chỉ có Bác sĩ hoặc Quản trị viên mới được lập bệnh án và kê đơn thuốc.")

        instance = serializer.save()
        record_audit(self.request, "CREATE", "MedicalRecord", instance.id, f"Lập bệnh án: {instance.code} cho BN {instance.patient.code}")

    def perform_update(self, serializer):
        user = self.request.user
        if user.role not in ['DOCTOR', 'ADMIN'] and not user.is_superuser:
            raise exceptions.PermissionDenied("Bạn không có quyền chỉnh sửa hồ sơ bệnh án.")

        instance = serializer.save()
        record_audit(self.request, "UPDATE", "MedicalRecord", instance.id, f"Cập nhật bệnh án: {instance.code}")
