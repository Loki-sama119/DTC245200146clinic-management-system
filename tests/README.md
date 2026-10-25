# BỘ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)

Hệ thống được kiểm thử toàn diện với **Pytest & Pytest-Django**, kiểm tra:
1. Xác thực & Phân quyền RBAC (`test_auth_api.py`)
2. Quản lý hồ sơ bệnh nhân (`test_patients_api.py`)
3. Đặt lịch khám, chống trùng khung giờ Bác sĩ & chuyển trạng thái (`test_appointments_api.py`)
4. Bác sĩ khám bệnh, kê đơn thuốc & bảo vệ quyền riêng tư y tế (`test_medical_records_api.py`)
5. Healthcheck & Prometheus Metrics Endpoint (`test_health_metrics_api.py`)

## Lệnh thực thi:
```bash
docker compose exec backend pytest
# hoặc chạy trực tiếp trong môi trường backend:
pytest
```
