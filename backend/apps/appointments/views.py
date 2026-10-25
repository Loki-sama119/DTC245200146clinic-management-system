from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Appointment
from .serializers import AppointmentSerializer
from apps.audit.utils import record_audit

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient', 'doctor', 'doctor__user', 'specialty', 'created_by').all().order_by('appointment_date', 'start_time')
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'doctor', 'specialty', 'patient', 'appointment_date']
    search_fields = ['code', 'patient__full_name', 'patient__phone', 'doctor__code', 'reason']

    def perform_create(self, serializer):
        with transaction.atomic():
            instance = serializer.save()
            record_audit(self.request, "CREATE", "Appointment", instance.id, f"Đặt lịch hẹn mới: {instance.code} cho BN {instance.patient.code}")

    def perform_update(self, serializer):
        with transaction.atomic():
            instance = serializer.save()
            record_audit(self.request, "UPDATE", "Appointment", instance.id, f"Cập nhật lịch hẹn: {instance.code}")

    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = Appointment.Status.CONFIRMED
        appointment.save()
        record_audit(request, "CONFIRM", "Appointment", appointment.id, f"Xác nhận lịch hẹn: {appointment.code}")
        return Response({"status": "success", "message": "Đã xác nhận lịch hẹn.", "data": AppointmentSerializer(appointment).data})

    @action(detail=True, methods=['post'], url_path='check-in')
    def check_in(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = Appointment.Status.IN_PROGRESS
        appointment.save()
        record_audit(request, "CHECK_IN", "Appointment", appointment.id, f"Bệnh nhân check-in: {appointment.code}")
        return Response({"status": "success", "message": "Bệnh nhân đã tiếp nhận vào phòng khám.", "data": AppointmentSerializer(appointment).data})

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        reason = request.data.get('reason', 'Lý do cá nhân')
        appointment.status = Appointment.Status.CANCELLED
        appointment.notes = f"{appointment.notes or ''} [HỦY: {reason}]".strip()
        appointment.save()
        record_audit(request, "CANCEL", "Appointment", appointment.id, f"Hủy lịch hẹn: {appointment.code} do {reason}")
        return Response({"status": "success", "message": "Đã hủy lịch hẹn.", "data": AppointmentSerializer(appointment).data})

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = Appointment.Status.COMPLETED
        appointment.save()
        record_audit(request, "COMPLETE", "Appointment", appointment.id, f"Hoàn thành khám bệnh: {appointment.code}")
        return Response({"status": "success", "message": "Đã hoàn thành lượt khám.", "data": AppointmentSerializer(appointment).data})
