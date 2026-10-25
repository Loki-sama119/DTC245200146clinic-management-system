from django.db import models
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.appointments.models import Appointment

class MedicalRecord(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã hồ sơ bệnh án")
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.PROTECT,
        related_name='medical_record',
        verbose_name="Lịch hẹn liên kết"
    )
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='medical_records', verbose_name="Bệnh nhân")
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='medical_records', verbose_name="Bác sĩ khám")
    symptoms = models.TextField(verbose_name="Triệu chứng lâm sàng")
    vital_signs = models.JSONField(default=dict, blank=True, verbose_name="Chỉ số sinh tồn (Huyết áp, mạch, nhiệt độ)")
    diagnosis = models.TextField(verbose_name="Chẩn đoán xác định")
    treatment_plan = models.TextField(verbose_name="Hướng điều trị")
    prescription = models.JSONField(default=list, blank=True, verbose_name="Đơn thuốc điện tử")
    doctor_notes = models.TextField(blank=True, null=True, verbose_name="Lời dặn của bác sĩ")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Hẹn ngày tái khám")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medical_records'
        ordering = ['-created_at']
        verbose_name = 'Hồ sơ bệnh án'
        verbose_name_plural = 'Danh sách bệnh án'

    def __str__(self):
        return f"[{self.code}] {self.patient.full_name} - Chẩn đoán: {self.diagnosis[:30]}"
