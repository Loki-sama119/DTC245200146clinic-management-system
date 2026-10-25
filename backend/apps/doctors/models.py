from django.db import models
from django.conf import settings
from apps.specialties.models import Specialty

class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name="Tài khoản liên kết"
    )
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã bác sĩ")
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name='doctors',
        verbose_name="Chuyên khoa"
    )
    room_number = models.CharField(max_length=50, verbose_name="Phòng khám")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại liên hệ")
    email = models.EmailField(blank=True, null=True, verbose_name="Email công tác")
    consultation_fee = models.DecimalField(max_digits=12, decimal_places=0, default=150000, verbose_name="Giá khám (VNĐ)")
    bio = models.TextField(blank=True, null=True, verbose_name="Tiểu sử chuyên môn")
    is_active = models.BooleanField(default=True, verbose_name="Đang công tác")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doctors'
        ordering = ['code']
        verbose_name = 'Bác sĩ'
        verbose_name_plural = 'Danh sách bác sĩ'

    def __str__(self):
        full_name = f"{self.user.last_name} {self.user.first_name}".strip()
        name = full_name if full_name else self.user.username
        return f"BS. {name} ({self.code}) - {self.specialty.name}"
