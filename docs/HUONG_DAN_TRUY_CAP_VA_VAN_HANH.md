# HƯỚNG DẪN TRUY CẬP VÀ VẬN HÀNH HỆ THỐNG

- **Đề tài**: Đề 8 — Hệ thống Quản lý Phòng khám / Bệnh viện
- **Sinh viên**: Nguyễn Văn Thắng (MSV: DTC245200146)

---

## 1. CÁC ĐỊA CHỈ TRUY CẬP (ENDPOINTS)

| Dịch vụ | Địa chỉ URL | Tài khoản / Thông tin |
| :--- | :--- | :--- |
| **Website Phòng Khám** | `http://localhost/` hoặc `http://192.168.220.131/` | `admin` / `Admin@123`<br>`doctor_thang` / `Doc@123`<br>`receptionist` / `Rec@123` |
| **Tài liệu Swagger API** | `http://localhost/api/docs/` | Xem và thử nghiệm trực tiếp toàn bộ REST API |
| **pgAdmin 4 Web GUI** | `http://localhost:5050/` | `admin@phucanclinic.vn` / `Admin@Clinic2026` |
| **Prometheus Server** | `http://localhost:9090/` | Xem danh sách target cào metrics |
| **Grafana Dashboard** | `http://localhost:3000/` | `admin` / `Admin@Grafana2026` |
| **Health Check API** | `http://localhost/api/health/` | Kiểm tra kết nối CSDL và tình trạng backend |
| **Prometheus Metrics**| `http://localhost/api/metrics/` | Dữ liệu metrics dạng văn bản chuẩn Prometheus |

---

## 2. CÁC LỆNH VẬN HÀNH HỆ THỐNG (MAKEFILE COMMANDS)

```bash
# Khởi động toàn bộ hệ thống
make up

# Xem log thời gian thực của toàn bộ hệ thống
make logs

# Kiểm tra sức khỏe toàn bộ dịch vụ
make health

# Chạy bộ kiểm thử tự động
make test

# Nạp lại dữ liệu mẫu
make seed

# Dừng hệ thống
make down
```
