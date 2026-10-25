from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Người thực hiện"
    )
    action = models.CharField(max_length=50, verbose_name="Hành động")
    model_name = models.CharField(max_length=100, verbose_name="Bảng dữ liệu")
    object_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Mã đối tượng")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Địa chỉ IP")
    details = models.TextField(blank=True, null=True, verbose_name="Chi tiết hành động")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian")

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        verbose_name = 'Nhật ký kiểm toán'
        verbose_name_plural = 'Danh sách nhật ký kiểm toán'

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.user} - {self.action} on {self.model_name}"
