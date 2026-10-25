#!/usr/bin/env bash
# Sao lưu cơ sở dữ liệu PostgreSQL từ container
set -e

BACKUP_DIR="database/backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/clinic_db_backup_${TIMESTAMP}.sql"

echo "==> Đang tiến hành sao lưu CSDL clinic_db ra file ${BACKUP_FILE}..."
docker compose exec -T postgres pg_dump -U clinic_user clinic_db > "$BACKUP_FILE"

echo "==> Sao lưu thành công! Kích thước file: $(du -sh "$BACKUP_FILE" | cut -f1)"
