from django.db import models

class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Nam'
        FEMALE = 'FEMALE', 'Nữ'
        OTHER = 'OTHER', 'Khác'

    code = models.CharField(max_length=50, unique=True, verbose_name="Mã bệnh nhân")
    full_name = models.CharField(max_length=150, verbose_name="Họ và tên")
    date_of_birth = models.DateField(verbose_name="Ngày sinh")
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE, verbose_name="Giới tính")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    identity_number = models.CharField(max_length=30, blank=True, null=True, verbose_name="CCCD / CMND")
    address = models.CharField(max_length=255, verbose_name="Địa chỉ thường trú")
    blood_type = models.CharField(max_length=10, blank=True, null=True, verbose_name="Nhóm máu")
    allergies = models.TextField(blank=True, null=True, verbose_name="Dị ứng thuốc/thực phẩm")
    medical_history = models.TextField(blank=True, null=True, verbose_name="Tiền sử bệnh lý")
    is_active = models.BooleanField(default=True, verbose_name="Trạng thái hồ sơ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patients'
        ordering = ['-id']
        verbose_name = 'Bệnh nhân'
        verbose_name_plural = 'Danh sách bệnh nhân'

    def __str__(self):
        return f"{self.full_name} ({self.code}) - {self.phone}"
