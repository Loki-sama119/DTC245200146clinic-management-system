from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Quản trị viên'
        DOCTOR = 'DOCTOR', 'Bác sĩ'
        RECEPTIONIST = 'RECEPTIONIST', 'Lễ tân / Tiếp đón'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.RECEPTIONIST,
        verbose_name="Vai trò"
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Địa chỉ")

    class Meta:
        db_table = 'users'
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Danh sách người dùng'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_doctor_role(self):
        return self.role == self.Role.DOCTOR

    @property
    def is_receptionist_role(self):
        return self.role == self.Role.RECEPTIONIST
