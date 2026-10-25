#!/usr/bin/env bash
# Dừng toàn bộ dịch vụ Docker Compose
set -e

echo "==> Đang dừng hệ thống Clinic Management System..."
docker compose down
echo "==> Toàn bộ container đã được dừng và giải phóng an toàn."
