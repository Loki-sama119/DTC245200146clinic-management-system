# BÁO CÁO TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG
## HẠ TẦNG DEVOPS, MONITORING, LOGGING VÀ SECURITY

- **Đề tài**: Đề 8 — Hệ thống Quản lý Phòng khám / Bệnh viện
- **Sinh viên**: Nguyễn Văn Thắng (MSV: DTC245200146)

---

## 1. DANH SÁCH 11 DỊCH VỤ TRONG DOCKER COMPOSE

1. `postgres` (PostgreSQL 16): Database chính, lưu trữ trên named volume `clinic_pgdata`.
2. `pgadmin` (pgAdmin 4): Giao diện web quản trị CSDL trên cổng 5050.
3. `backend` (Django 5 + Gunicorn): Xử lý API nghiệp vụ, phân quyền JWT.
4. `frontend` (React SPA + Nginx Alpine): Phục vụ giao diện người dùng.
5. `nginx` (Reverse Proxy): Điểm tiếp nhận cổng 80, gán Security Headers và phân luồng.
6. `prometheus`: Thu thập metrics từ cAdvisor, postgres-exporter và backend.
7. `grafana`: Hiển thị dashboard giám sát container, DB connections và live logs.
8. `loki`: Cơ sở dữ liệu lưu trữ nhật ký tập trung.
9. `promtail`: Đọc file log từ Nginx và Backend đẩy về Loki.
10. `postgres-exporter`: Thu thập chỉ số nội tại của PostgreSQL.
11. `cadvisor`: Thu thập chỉ số CPU, RAM, Disk của các container Docker.

---

## 2. QUẢN TRỊ NHẬT KÝ TẬP TRUNG VỚI LOKI & PROMTAIL

Promtail thu thập log từ `/var/log/nginx/*.log` và `/var/log/backend/*.log`, gắn nhãn `{job="nginx"}` và `{job="backend"}`.

### 3 Truy vấn LogQL cơ bản phục vụ chấm thi:
1. **Truy vấn toàn bộ log truy cập Nginx Reverse Proxy**:
   ```logql
   {job="nginx"}
   ```
2. **Truy vấn log lỗi HTTP 4xx hoặc 5xx của hệ thống**:
   ```logql
   {job="nginx"} |~ " (4[0-9]{2}|5[0-9]{2}) "
   ```
3. **Truy vấn log nghiệp vụ từ Backend**:
   ```logql
   {job="backend"} |= "LOGIN"
   ```

---

## 3. CÁC BIỆN PHÁP BẢO MẬT & LINUX HARDENING ĐÃ ÁP DỤNG

1. **Chạy ứng dụng với Non-root User**: Container `backend` và `frontend` đều tạo và sử dụng user không đặc quyền (`clinicuser` UID 1000 và `nginx`).
2. **Cô lập mạng nội bộ (Network Isolation)**: Thiết lập 3 mạng Docker (`frontend_net`, `backend_net`, `monitoring_net`). Cơ sở dữ liệu PostgreSQL **tuyệt đối không mở port 5432** ra mạng ngoài.
3. **Phân quyền và bảo vệ bí mật**: File `.env` chứa mật khẩu CSDL được gán quyền `chmod 600`, loại trừ khỏi Git qua `.gitignore`. Chỉ commit file mẫu `.env.example`.
4. **Áp dụng Security Headers trên Nginx**: Cấu hình đầy đủ `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy` và ẩn phiên bản `server_tokens off`.
5. **Mật khẩu an toàn & RBAC**: Mật khẩu người dùng được băm an toàn bằng PBKDF2:SHA256, kiểm soát quyền truy cập API nghiêm ngặt theo 3 vai trò.
