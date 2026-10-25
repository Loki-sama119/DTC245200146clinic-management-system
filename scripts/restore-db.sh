#!/usr/bin/env bash
# Khôi phục cơ sở dữ liệu PostgreSQL từ file backup
set -e

if [ -z "$1" ]; then
  echo "Cách dùng: bash scripts/restore-db.sh <đường_dẫn_file_backup.sql>"
  exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Lỗi: Không tìm thấy file sao lưu tại $BACKUP_FILE"
  exit 1
fi

echo "==> Đang khôi phục dữ liệu từ $BACKUP_FILE vào container postgres..."
cat "$BACKUP_FILE" | docker compose exec -T postgres psql -U clinic_user -d clinic_db

echo "==> Khôi phục cơ sở dữ liệu thành công!"
