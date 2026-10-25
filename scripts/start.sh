#!/usr/bin/env bash
# Khởi động toàn bộ dịch vụ Docker Compose
set -e

echo "==> Đang khởi động hệ thống Clinic Management System qua Docker Compose..."
docker compose up -d --build

echo "==> Kiểm tra trạng thái các container sau khởi động:"
docker compose ps
