#!/bin/sh
set -e

echo "==> Đang chờ PostgreSQL khởi động hoàn tất..."
until python -c "
import psycopg2, os
try:
    psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB', 'clinic_db'),
        user=os.environ.get('POSTGRES_USER', 'clinic_user'),
        password=os.environ.get('POSTGRES_PASSWORD', 'clinic_secure_password_2026'),
        host=os.environ.get('POSTGRES_HOST', 'postgres'),
        port=os.environ.get('POSTGRES_PORT', '5432')
    )
    exit(0)
except Exception:
    exit(1)
"; do
  echo "    PostgreSQL chưa sẵn sàng, thử lại sau 2 giây..."
  sleep 2
done

echo "==> PostgreSQL đã sẵn sàng!"

echo "==> Tạo Database Migrations nếu chưa có..."
python manage.py makemigrations accounts specialties doctors patients appointments medical_records audit --noinput

echo "==> Thực hiện Database Migrations..."
python manage.py migrate --noinput

echo "==> Thu thập Static Files..."
python manage.py collectstatic --noinput

echo "==> Khởi tạo dữ liệu mẫu phòng khám & tài khoản demo..."
python manage.py seed_data

echo "==> Khởi động máy chủ ứng dụng Gunicorn..."
exec "$@"
