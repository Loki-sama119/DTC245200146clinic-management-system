#!/usr/bin/env bash
set -e
if [ -z "$1" ]; then
    echo "Sử dụng: $0 <duong_dan_file_backup.sql>"
    exit 1
fi
BACKUP_FILE="$1"
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Lỗi: Không tìm thấy file backup $BACKUP_FILE"
    exit 1
fi
echo "==> Đang phục hồi cơ sở dữ liệu từ: $BACKUP_FILE"
docker compose exec -T postgres psql -U "${POSTGRES_USER:-clinic_user}" -d "${POSTGRES_DB:-clinic_db}" < "$BACKUP_FILE"
echo "==> Phục hồi cơ sở dữ liệu hoàn tất thành công!"
