# HƯỚNG DẪN BẢO MẬT VÀ HARDENING HỆ THỐNG (SECURITY REPORT)

- **Hệ thống**: Clinic Management System
- **Sinh viên**: Nguyễn Văn Thắng (MSV: DTC245200146)

---

## 1. CÁC BIỆN PHÁP BẢO MẬT ĐÃ TRIỂN KHAI VÀ XÁC MINH

| STT | Biện pháp bảo mật | Cơ chế áp dụng | Cách thức xác minh thực tế |
| :---: | :--- | :--- | :--- |
| **1** | **Non-root Container** | User `clinicuser` (UID 1000) và `nginx` | Kiểm tra lệnh `docker compose exec backend whoami` -> trả về `clinicuser` |
| **2** | **Network Isolation** | 3 mạng bridge độc lập (`frontend_net`, `backend_net`, `monitoring_net`) | Cổng 5432 của PostgreSQL không bị expose ra máy chủ bên ngoài |
| **3** | **Security Headers** | Nginx gán `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy` | `curl -s -I http://localhost/` hiển thị đầy đủ headers |
| **4** | **Phân quyền Secret File** | File `.env` chứa mật khẩu CSDL phân quyền `chmod 600`, không commit vào Git | Kiểm tra `ls -l .env` trả về `-rw-------`, lệnh `git status` không thấy file `.env` |
| **5** | **Mã hóa Mật khẩu** | Thuật toán băm PBKDF2:SHA256 có Salt | Mật khẩu trong PostgreSQL được lưu dưới dạng băm `pbkdf2_sha256$...` |
| **6** | **Chống SQLi & XSS** | Sử dụng Django ORM Parameterized Query & Jinja/SPA sanitization | Không thể chèn mã SQL hoặc script độc hại qua các input form |
| **7** | **Nhật ký Kiểm toán (Audit)**| Bảng `audit_logs` tự động ghi vết hành động, người dùng và địa chỉ IP | Tra cứu bảng `audit_logs` có đầy đủ nhật ký các hành động nhạy cảm |
