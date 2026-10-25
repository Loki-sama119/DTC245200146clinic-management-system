# ==============================================================================
# CLINIC MANAGEMENT BACKEND DOCKERFILE — PYTHON 3.12 SLIM
# ==============================================================================

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cài đặt thư viện hệ thống cần thiết cho PostgreSQL & build
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng
COPY . .

# Tạo thư mục staticfiles, logs và cấp quyền cho non-root user
RUN useradd -m -u 1000 clinicuser && \
    mkdir -p /app/staticfiles /app/logs && \
    chown -R clinicuser:clinicuser /app

# Cấp quyền thực thi cho entrypoint script
RUN chmod +x /app/entrypoint.sh

USER clinicuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
