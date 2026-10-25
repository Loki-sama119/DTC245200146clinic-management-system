from django.db import models
from django.conf import settings
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.specialties.models import Specialty

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Chờ xác nhận'
        CONFIRMED = 'CONFIRMED', 'Đã xác nhận'
        IN_PROGRESS = 'IN_PROGRESS', 'Đang khám'
        COMPLETED = 'COMPLETED', 'Đã khám xong'
        CANCELLED = 'CANCELLED', 'Đã hủy'
        NO_SHOW = 'NO_SHOW', 'Bỏ hẹn'

    code = models.CharField(max_length=50, unique=True, verbose_name="Mã lịch hẹn")
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='appointments', verbose_name="Bệnh nhân")
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='appointments', verbose_name="Bác sĩ phụ trách")
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name='appointments', verbose_name="Chuyên khoa")
    appointment_date = models.DateField(verbose_name="Ngày khám")
    start_time = models.TimeField(verbose_name="Giờ bắt đầu")
    end_time = models.TimeField(verbose_name="Giờ kết thúc")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name="Trạng thái")
    reason = models.CharField(max_length=255, verbose_name="Lý do khám")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú thêm")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Người tạo lịch")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['appointment_date', 'start_time']
        verbose_name = 'Lịch hẹn khám'
        verbose_name_plural = 'Danh sách lịch hẹn'
        indexes = [
            models.Index(fields=['doctor', 'appointment_date', 'status']),
            models.Index(fields=['patient', 'appointment_date']),
        ]

    def __str__(self):
        return f"[{self.code}] {self.patient.full_name} - {self.doctor.code} ({self.appointment_date} {self.start_time.strftime('%H:%M')})"
