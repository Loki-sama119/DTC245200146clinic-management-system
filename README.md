# HỆ THỐNG QUẢN LÝ PHÒNG KHÁM / BỆNH VIỆN (CLINIC MANAGEMENT SYSTEM)

[![CI](https://github.com/Loki-sama119/DTC245200146clinic-management-system/actions/workflows/ci.yml/badge.svg)](https://github.com/Loki-sama119/DTC245200146clinic-management-system/actions)
- **Học phần**: Triển khai và Quản trị Hệ thống Phần mềm
- **Đề tài**: Đề 8 — Hệ thống Quản lý Phòng khám / Bệnh viện
- **Sinh viên thực hiện**: Nguyễn Văn Thắng (MSV: DTC245200146)
- **Công nghệ chính**: Django 5 + DRF, React SPA, PostgreSQL 16, pgAdmin 4, Nginx, Prometheus, Grafana, Loki, Promtail, cAdvisor, postgres-exporter, Docker Compose.

---

## 1. KIẾN TRÚC TỔNG THỂ HỆ THỐNG

Hệ thống được đóng gói hoàn chỉnh bằng **Docker Compose** bao gồm 11 dịch vụ phối hợp qua 3 mạng ảo biệt lập (`frontend_net`, `backend_net`, `monitoring_net`):

| Tầng kiến trúc | Dịch vụ Container | Cổng công khai | Vai trò & Trách nhiệm |
| :--- | :--- | :---: | :--- |
| **Gateway / Proxy** | `clinic_nginx` | `80` | Điểm truy cập duy nhất, reverse proxy frontend/backend, security headers |
| **Frontend** | `clinic_frontend` | Nội bộ | Giao diện Single Page Application (SPA) chuẩn y tế, Fetch API |
| **Backend API** | `clinic_backend` | Nội bộ | Django 5 + DRF, xử lý nghiệp vụ y tế, RBAC, Gunicorn WSGI |
| **Database** | `clinic_postgres` | Nội bộ (`5432`) | Cơ sở dữ liệu quan hệ PostgreSQL 16 lưu trữ dữ liệu bền vững |
| **DB Admin** | `clinic_pgadmin` | `5050` | Giao diện quản trị PostgreSQL pgAdmin 4 trực quan |
| **Monitoring** | `clinic_prometheus` | `9090` | Thu thập metrics từ Backend, PostgreSQL, Container và Nginx |
| **Dashboard** | `clinic_grafana` | `3000` | Bảng điều khiển trực quan hóa thời gian thực (Provisioned) |
| **Centralized Log**| `clinic_loki` | `3100` | Lưu trữ nhật ký tập trung và hỗ trợ truy vấn LogQL |
| **Log Shipper** | `clinic_promtail` | Nội bộ | Đọc và chuyển log thời gian thực từ Nginx và Backend về Loki |
| **DB Exporter** | `clinic_postgres_exporter`| Nội bộ | Thu thập chỉ số hiệu năng PostgreSQL (Connections, Commits) |
| **Container Metric**| `clinic_cadvisor` | Nội bộ | Thu thập metrics tài nguyên phần cứng container (CPU, RAM, Disk) |

---

## 2. TÀI KHOẢN TRUY CẬP HỆ THỐNG DEMO

Khi khởi động hệ thống lần đầu, script `seed_data` tự động nạp các tài khoản chuẩn phân quyền:

| Vai trò | Tên đăng nhập | Mật khẩu | Quyền hạn chính |
| :--- | :--- | :--- | :--- |
| **ADMIN (Quản trị)** | `admin` | `Admin@123` | Toàn quyền cấu hình bác sĩ, chuyên khoa, người dùng, xem audit logs |
| **DOCTOR (Bác sĩ)** | `doctor_thang` | `Doc@123` | Khám bệnh, chẩn đoán, xem lịch sử bệnh lý, kê đơn thuốc điện tử |
| **RECEPTIONIST (Lễ tân)**| `receptionist` | `Rec@123` | Thêm hồ sơ bệnh nhân, điều phối lịch hẹn, check-in, hủy lịch |
| **pgAdmin 4 Web** | `admin@phucanclinic.vn` | `Admin@Clinic2026` | Đăng nhập pgAdmin 4 trên cổng `http://localhost:5050` |
| **Grafana Dashboard** | `admin` | `Admin@Grafana2026` | Bảng điều khiển giám sát hiệu năng trên cổng `http://localhost:3000` |

---

## 3. HƯỚNG DẪN KHỞI CHẠY BẰNG DOCKER COMPOSE

### Bước 1: Sao chép file cấu hình môi trường
```bash
cp .env.example .env
```

### Bước 2: Khởi động toàn bộ 11 container
```bash
docker compose up -d --build
# Hoặc sử dụng Makefile:
make up
```

### Bước 3: Kiểm tra trạng thái hệ thống
```bash
bash scripts/health-check.sh
# Hoặc:
make health
```

---

## 4. DANH MỤC ĐỊA CHỈ TRUY CẬP DỊCH VỤ

- **Ứng dụng Phòng Khám Phúc An**: `http://localhost/` hoặc `http://192.168.220.131/`
- **Swagger / OpenAPI Documentation**: `http://localhost/api/docs/`
- **pgAdmin 4 Database Management**: `http://localhost:5050/`
- **Prometheus Server**: `http://localhost:9090/`
- **Grafana Monitoring Dashboard**: `http://localhost:3000/`
- **Health Check Endpoint**: `http://localhost/api/health/`
- **Prometheus Metrics Endpoint**: `http://localhost/api/metrics/`

---

## 5. CHẠY BỘ KIỂM THỬ TỰ ĐỘNG (PYTEST)
```bash
docker compose exec backend pytest
# Hoặc:
make test
```

---

## 6. SAO LƯU VÀ KHÔI PHỤC CƠ SỞ DỮ LIỆU
- **Sao lưu**: `bash scripts/backup-db.sh` (File lưu tại `database/backups/`)
- **Khôi phục**: `bash scripts/restore-db.sh <path_to_backup.sql>`

---

## 7. LIÊN KẾT TÀI LIỆU BÁO CÁO HỌC PHẦN
Toàn bộ tài liệu chi tiết được lưu trong thư mục `docs/`:
- [Báo cáo Học phần Môn học](file:///home/ubuntu/clinic-management/docs/BAO_CAO_MON_HOC.md)
- [Báo cáo Triển khai Hệ thống](file:///home/ubuntu/clinic-management/docs/BAO_CAO_TRIEN_KHAI_HE_THONG.md)
- [Kịch bản Trình diễn Demo 10 bước](file:///home/ubuntu/clinic-management/docs/KICH_BAN_DEMO.md)
- [Kiến trúc Hệ thống & Network Flow](file:///home/ubuntu/clinic-management/docs/KIEN_TRUC_HE_THONG.md)
- [Thiết kế Cơ sở Dữ liệu & ERD](file:///home/ubuntu/clinic-management/docs/THIET_KE_CO_SO_DU_LIEU.md)
- [Hướng dẫn An toàn & Hardening](file:///home/ubuntu/clinic-management/docs/HUONG_DAN_BAO_MAT.md)
- [Hướng dẫn Vận hành & Truy cập](file:///home/ubuntu/clinic-management/docs/HUONG_DAN_TRUY_CAP_VA_VAN_HANH.md)
- [Báo cáo Kết quả Kiểm thử](file:///home/ubuntu/clinic-management/docs/KIEM_THU.md)
- [Phân công Công việc](file:///home/ubuntu/clinic-management/docs/PHAN_CONG_CONG_VIEC.md)
