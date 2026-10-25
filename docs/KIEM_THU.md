# BÁO CÁO KIỂM THỬ HỆ THỐNG (TESTING REPORT)

- **Học phần**: Triển khai và Quản trị Hệ thống Phần mềm
- **Sinh viên**: Nguyễn Văn Thắng (MSV: DTC245200146)
- **Công cụ kiểm thử**: Pytest, Pytest-Django, Bash Health Check

---

## 1. KẾT QUẢ KIỂM THỬ ĐƠN VỊ & TÍCH HỢP (PYTEST)

| STT | Tập tin kiểm thử | Số ca kiểm thử | Nội dung kiểm tra | Kết quả |
| :---: | :--- | :---: | :--- | :---: |
| **1** | `test_auth_api.py` | 4 | Đăng nhập thành công, từ chối sai pass, lấy profile, chặn unauth | **PASS (100%)** |
| **2** | `test_patients_api.py` | 3 | Thêm mới bệnh nhân tự sinh mã, chặn trùng SĐT, tìm kiếm bệnh nhân | **PASS (100%)** |
| **3** | `test_appointments_api.py` | 4 | Đặt lịch mới, phát hiện trùng giờ bác sĩ (anti-conflict), chặn đặt ngày quá khứ, chuyển trạng thái | **PASS (100%)** |
| **4** | `test_medical_records_api.py` | 2 | Bác sĩ khám và lập bệnh án, chặn lễ tân không có quyền truy cập bệnh án | **PASS (100%)** |
| **5** | `test_health_metrics_api.py` | 2 | Kiểm tra `/api/health/` kết nối DB, kiểm tra `/api/metrics/` trả về metrics | **PASS (100%)** |

**Tổng số ca kiểm thử:** 15 ca kiểm thử — **Tỷ lệ vượt qua: 15 / 15 (100% PASS)**.

---

## 2. KẾT QUẢ KIỂM THỬ HẠ TẦNG DOCKER & OBSERVABILITY

| Dịch vụ kiểm tra | Lệnh xác minh | Kết quả thực tế ghi nhận | Đánh giá |
| :--- | :--- | :--- | :---: |
| **PostgreSQL 16** | `pg_isready -U clinic_user` | `accepting connections` | **PASS** |
| **Backend API** | `curl -s http://localhost/api/health/` | `{"database": "healthy", "status": "healthy"}` | **PASS** |
| **Nginx Reverse Proxy** | `curl -s -I http://localhost/` | Trả về 200 OK kèm Security Headers | **PASS** |
| **pgAdmin 4** | `curl -s http://localhost:5050/` | Trả về 200 OK / 302 Found | **PASS** |
| **Prometheus Targets** | `curl -s http://localhost:9090/-/ready` | `Prometheus Server is Ready` | **PASS** |
| **Grafana Health** | `curl -s http://localhost:3000/api/health` | `{"database": "ok"}` | **PASS** |
| **Loki Log Ingester** | `curl -s http://localhost:3100/ready` | `ready` | **PASS** |
