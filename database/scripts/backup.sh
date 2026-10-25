#!/usr/bin/env bash
set -e
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$(dirname "$0")/../backups"
BACKUP_FILE="${BACKUP_DIR}/clinic_db_backup_${TIMESTAMP}.sql"

mkdir -p "${BACKUP_DIR}"
echo "==> Đang tiến hành sao lưu cơ sở dữ liệu PostgreSQL..."
docker compose exec -T postgres pg_dump -U "${POSTGRES_USER:-clinic_user}" -d "${POSTGRES_DB:-clinic_db}" > "${BACKUP_FILE}"
echo "==> Sao lưu thành công: ${BACKUP_FILE} ($(du -h "${BACKUP_FILE}" | cut -f1))"
