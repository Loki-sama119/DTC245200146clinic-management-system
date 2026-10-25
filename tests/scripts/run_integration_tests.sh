#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "  CLINIC MANAGEMENT SYSTEM — AUTOMATED INTEGRATION TESTS"
echo "=========================================================="

echo "==> 1. Kiểm tra trạng thái container backend..."
if docker compose ps backend | grep -q "Up"; then
    echo "    Backend container đang chạy. Thực thi pytest bên trong container..."
    docker compose exec -T backend pytest -v /app/../tests/integration/ || docker compose exec -T backend pytest -v
else
    echo "    Backend container chưa chạy. Thử chạy pytest trực tiếp với biến môi trường cục bộ..."
    pytest -v tests/integration/
fi

echo "==> Hoàn tất kiểm thử!"
