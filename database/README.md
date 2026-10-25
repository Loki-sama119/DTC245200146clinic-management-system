# QUẢN TRỊ CƠ SỞ DỮ LIỆU POSTGRESQL (CLINIC DATABASE)

## 1. Thông tin kết nối nội bộ
- **Database Name**: `clinic_db`
- **User**: `clinic_user`
- **Host**: `postgres` (hoặc `127.0.0.1` nếu qua pgAdmin)
- **Port**: `5432` (cô lập nội bộ trong Docker network `backend_net`)
- **Timezone**: `Asia/Ho_Chi_Minh`

## 2. Quản lý bản sao lưu (Backup & Restore)
- Script sao lưu tự động: `bash scripts/backup-db.sh`
- Script phục hồi dữ liệu: `bash scripts/restore-db.sh <backup_file.sql>`
- Thư mục lưu trữ: `database/backups/`
