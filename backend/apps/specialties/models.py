from django.db import models

class Specialty(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Tên chuyên khoa")
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã chuyên khoa")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả chuyên môn")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'specialties'
        ordering = ['name']
        verbose_name = 'Chuyên khoa'
        verbose_name_plural = 'Danh mục chuyên khoa'

    def __str__(self):
        return f"{self.name} ({self.code})"
