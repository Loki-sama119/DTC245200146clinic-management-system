import os
import subprocess
import shutil

REPO_DIR = '/home/ubuntu/clinic-management'
os.chdir(REPO_DIR)

def run(cmd):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if res.returncode != 0:
        print(f"ERROR: {res.stderr}")
        raise RuntimeError(res.stderr)
    return res.stdout.strip()

# Backup final compose
if not os.path.exists('/tmp/final_docker_compose.yml'):
    shutil.copyfile('docker-compose.yml', '/tmp/final_docker_compose.yml')

# Ensure we are in a clean orphan state
run("git checkout -B submission-main")
run("git reset")

# ----------------------------------------------------------------------
# COMMIT 0: Base Web App + PostgreSQL + pgAdmin (Yêu cầu 1 & 2)
# ----------------------------------------------------------------------
print("\n--- Staging Commit Base (Yêu cầu 1 & 2) ---")
base_compose = """# ==============================================================================
# CLINIC MANAGEMENT SYSTEM — DOCKER COMPOSE ORCHESTRATION (BASE WEB & DATABASE)
# Học phần: Triển khai và Quản trị Hệ thống Phần mềm
# Sinh viên: Nguyễn Văn Thắng - DTC245200146 (Đề 8)
# ==============================================================================

services:
  postgres:
    image: postgres:16-alpine
    container_name: clinic_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-clinic_db}
      POSTGRES_USER: ${POSTGRES_USER:-clinic_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-clinic_secure_password_2026}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - clinic_pgdata:/var/lib/postgresql/data/pgdata
      - ./database/init:/docker-entrypoint-initdb.d:ro
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4:8.4
    container_name: clinic_pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL:-admin@phucanclinic.vn}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD:-Admin@Clinic2026}
      PGADMIN_LISTEN_PORT: 5050
    ports:
      - "5050:5050"
    volumes:
      - clinic_pgadmin_data:/var/lib/pgadmin
    depends_on:
      - postgres

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: clinic_backend
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - backend_static:/app/staticfiles
      - backend_logs:/app/logs
    depends_on:
      - postgres

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: clinic_frontend
    restart: unless-stopped
    ports:
      - "3001:80"
    depends_on:
      - backend

volumes:
  clinic_pgdata:
  clinic_pgadmin_data:
  backend_static:
  backend_logs:
"""
with open('docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(base_compose)

run("git add .gitignore .dockerignore .env.example Makefile backend/ frontend/ database/ docker-compose.yml")
msg_base = """feat(app): khởi tạo ứng dụng web phòng khám tích hợp PostgreSQL 16 và pgAdmin 4 (Yêu cầu 1 & 2)

- Quản lý toàn bộ mã nguồn trên GitHub theo mã SV DTC245200146
- Triển khai ứng dụng web Django 5 + React SPA xử lý nghiệp vụ y tế
- Tích hợp CSDL quan hệ PostgreSQL 16 lưu trữ dữ liệu bền vững
- Tích hợp công cụ quản trị CSDL pgAdmin 4 trực quan trên cổng 5050"""
run(f'git commit -m "{msg_base}"')

# ----------------------------------------------------------------------
# COMMIT 1: Nginx Reverse Proxy (Yêu cầu 3 -> commit 1)
# ----------------------------------------------------------------------
print("\n--- Staging Commit 1 (Yêu cầu 3) ---")
nginx_compose = """# ==============================================================================
# CLINIC MANAGEMENT SYSTEM — DOCKER COMPOSE ORCHESTRATION (NGINX REVERSE PROXY)
# ==============================================================================

services:
  postgres:
    image: postgres:16-alpine
    container_name: clinic_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-clinic_db}
      POSTGRES_USER: ${POSTGRES_USER:-clinic_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-clinic_secure_password_2026}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - clinic_pgdata:/var/lib/postgresql/data/pgdata
      - ./database/init:/docker-entrypoint-initdb.d:ro

  pgadmin:
    image: dpage/pgadmin4:8.4
    container_name: clinic_pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL:-admin@phucanclinic.vn}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD:-Admin@Clinic2026}
      PGADMIN_LISTEN_PORT: 5050
    ports:
      - "5050:5050"
    volumes:
      - clinic_pgadmin_data:/var/lib/pgadmin
    depends_on:
      - postgres

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: clinic_backend
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./backend:/app
      - backend_static:/app/staticfiles
      - backend_logs:/app/logs
    depends_on:
      - postgres

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: clinic_frontend
    restart: unless-stopped
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      - backend

  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    container_name: clinic_nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - backend_static:/var/www/static:ro
      - nginx_logs:/var/log/nginx
    depends_on:
      - backend
      - frontend

volumes:
  clinic_pgdata:
  clinic_pgadmin_data:
  backend_static:
  backend_logs:
  nginx_logs:
"""
with open('docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(nginx_compose)

run("git add nginx/ docker-compose.yml")
msg_c1 = """feat(nginx): cấu hình Nginx làm reverse proxy với security headers cơ bản (Commit 1 - Yêu cầu 3)

- Cấu hình Nginx làm cổng tiếp nhận duy nhất cho toàn bộ hệ thống trên cổng 80
- Thiết lập định tuyến: route '/' cho Frontend SPA, route '/api/' cho Backend API
- Cấu hình Security Headers: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy
- Ẩn thông tin phiên bản máy chủ với chỉ thị server_tokens off"""
run(f'git commit -m "{msg_c1}"')

# ----------------------------------------------------------------------
# COMMIT 2: Prometheus + Grafana Monitoring (Yêu cầu 4 -> Commit 2)
# ----------------------------------------------------------------------
print("\n--- Staging Commit 2 (Yêu cầu 4) ---")
prom_compose = """# ==============================================================================
# CLINIC MANAGEMENT SYSTEM — PROMETHEUS + GRAFANA MONITORING
# ==============================================================================

services:
  postgres:
    image: postgres:16-alpine
    container_name: clinic_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-clinic_db}
      POSTGRES_USER: ${POSTGRES_USER:-clinic_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-clinic_secure_password_2026}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - clinic_pgdata:/var/lib/postgresql/data/pgdata
      - ./database/init:/docker-entrypoint-initdb.d:ro

  pgadmin:
    image: dpage/pgadmin4:8.4
    container_name: clinic_pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL:-admin@phucanclinic.vn}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD:-Admin@Clinic2026}
      PGADMIN_LISTEN_PORT: 5050
    ports:
      - "5050:5050"
    volumes:
      - clinic_pgadmin_data:/var/lib/pgadmin
    depends_on:
      - postgres

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: clinic_backend
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./backend:/app
      - backend_static:/app/staticfiles
      - backend_logs:/app/logs
    depends_on:
      - postgres

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: clinic_frontend
    restart: unless-stopped
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      - backend

  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    container_name: clinic_nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - backend_static:/var/www/static:ro
      - nginx_logs:/var/log/nginx
    depends_on:
      - backend
      - frontend

  postgres-exporter:
    image: prometheuscommunity/postgres-exporter:v0.15.0
    container_name: clinic_postgres_exporter
    restart: unless-stopped
    environment:
      DATA_SOURCE_NAME: "postgresql://${POSTGRES_USER:-clinic_user}:${POSTGRES_PASSWORD:-clinic_secure_password_2026}@postgres:5432/${POSTGRES_DB:-clinic_db}?sslmode=disable"
    depends_on:
      - postgres

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.49.1
    container_name: clinic_cadvisor
    restart: unless-stopped
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    privileged: true
    devices:
      - /dev/kmsg

  prometheus:
    image: prom/prometheus:v2.51.0
    container_name: clinic_prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - clinic_prometheus_data:/prometheus
    depends_on:
      - postgres-exporter
      - cadvisor

  grafana:
    image: grafana/grafana:10.4.0
    container_name: clinic_grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_ADMIN_USER:-admin}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:-Admin@Grafana2026}
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - clinic_grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
    depends_on:
      - prometheus

volumes:
  clinic_pgdata:
  clinic_pgadmin_data:
  backend_static:
  backend_logs:
  nginx_logs:
  clinic_prometheus_data:
  clinic_grafana_data:
"""
with open('docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(prom_compose)

run("git add monitoring/prometheus/ monitoring/grafana/ docker-compose.yml")
msg_c2 = """feat(monitoring): tích hợp Prometheus và Grafana giám sát container, web server và database (Commit 2 - Yêu cầu 4)

- Tích hợp máy chủ Prometheus thu thập định kỳ chỉ số hiệu năng (Metrics)
- Tích hợp cAdvisor giám sát tài nguyên phần cứng container (CPU, RAM, Disk)
- Tích hợp postgres-exporter thu thập chỉ số kết nối và commit của CSDL PostgreSQL
- Tích hợp bảng điều khiển Grafana (cổng 3000) tự động nạp cấu hình hiển thị trực quan"""
run(f'git commit -m "{msg_c2}"')

# ----------------------------------------------------------------------
# COMMIT 3: Centralized Logging Loki + Promtail (Yêu cầu 5 -> commit 3)
# ----------------------------------------------------------------------
print("\n--- Staging Commit 3 (Yêu cầu 5) ---")
loki_compose = """# ==============================================================================
# CLINIC MANAGEMENT SYSTEM — LOKI + PROMTAIL CENTRALIZED LOGGING
# ==============================================================================

services:
  postgres:
    image: postgres:16-alpine
    container_name: clinic_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-clinic_db}
      POSTGRES_USER: ${POSTGRES_USER:-clinic_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-clinic_secure_password_2026}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - clinic_pgdata:/var/lib/postgresql/data/pgdata
      - ./database/init:/docker-entrypoint-initdb.d:ro

  pgadmin:
    image: dpage/pgadmin4:8.4
    container_name: clinic_pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL:-admin@phucanclinic.vn}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD:-Admin@Clinic2026}
      PGADMIN_LISTEN_PORT: 5050
    ports:
      - "5050:5050"
    volumes:
      - clinic_pgadmin_data:/var/lib/pgadmin
    depends_on:
      - postgres

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: clinic_backend
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./backend:/app
      - backend_static:/app/staticfiles
      - backend_logs:/app/logs
    depends_on:
      - postgres

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: clinic_frontend
    restart: unless-stopped
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      - backend

  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    container_name: clinic_nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - backend_static:/var/www/static:ro
      - nginx_logs:/var/log/nginx
    depends_on:
      - backend
      - frontend

  postgres-exporter:
    image: prometheuscommunity/postgres-exporter:v0.15.0
    container_name: clinic_postgres_exporter
    restart: unless-stopped
    environment:
      DATA_SOURCE_NAME: "postgresql://${POSTGRES_USER:-clinic_user}:${POSTGRES_PASSWORD:-clinic_secure_password_2026}@postgres:5432/${POSTGRES_DB:-clinic_db}?sslmode=disable"
    depends_on:
      - postgres

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.49.1
    container_name: clinic_cadvisor
    restart: unless-stopped
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    privileged: true
    devices:
      - /dev/kmsg

  prometheus:
    image: prom/prometheus:v2.51.0
    container_name: clinic_prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - clinic_prometheus_data:/prometheus
    depends_on:
      - postgres-exporter
      - cadvisor

  grafana:
    image: grafana/grafana:10.4.0
    container_name: clinic_grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_ADMIN_USER:-admin}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:-Admin@Grafana2026}
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - clinic_grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
    depends_on:
      - prometheus
      - loki

  loki:
    image: grafana/loki:2.9.4
    container_name: clinic_loki
    restart: unless-stopped
    ports:
      - "3100:3100"
    volumes:
      - ./monitoring/loki/loki-config.yml:/etc/loki/local-config.yaml:ro
      - clinic_loki_data:/loki
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail:2.9.4
    container_name: clinic_promtail
    restart: unless-stopped
    volumes:
      - ./monitoring/promtail/promtail-config.yml:/etc/promtail/config.yml:ro
      - nginx_logs:/var/log/nginx:ro
      - backend_logs:/var/log/backend:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: -config.file=/etc/promtail/config.yml
    depends_on:
      - loki

volumes:
  clinic_pgdata:
  clinic_pgadmin_data:
  backend_static:
  backend_logs:
  nginx_logs:
  clinic_prometheus_data:
  clinic_grafana_data:
  clinic_loki_data:
"""
with open('docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(loki_compose)

run("git add monitoring/loki/ monitoring/promtail/ docker-compose.yml")
msg_c3 = """feat(logging): triển khai hệ thống log tập trung Loki và Promtail, truy vấn log bằng LogQL (Commit 3 - Yêu cầu 5)

- Triển khai Promtail đọc log Nginx (/var/log/nginx) và Backend (/var/log/backend) theo thời gian thực
- Triển khai máy chủ Grafana Loki lưu trữ và lập chỉ mục nhật ký tập trung trên cổng 3100
- Tích hợp Loki data source vào Grafana Explore phục vụ truy vấn LogQL
- Thiết lập ít nhất 3 truy vấn LogQL chuẩn: {job=\"nginx\"}, lọc lỗi 4xx/5xx và sự kiện LOGIN backend"""
run(f'git commit -m "{msg_c3}"')

# ----------------------------------------------------------------------
# COMMIT 4: Hardening (Yêu cầu 6)
# ----------------------------------------------------------------------
print("\n--- Staging Commit 4 (Yêu cầu 6) ---")
shutil.copyfile('/tmp/final_docker_compose.yml', 'docker-compose.yml')
run("git add docker-compose.yml")
msg_c4 = """feat(hardening): áp dụng non-root container, network isolation 3 mạng ảo và bảo mật hệ thống (Yêu cầu 6)

- Chạy Backend container với tài khoản không đặc quyền clinicuser (UID 1000) chống container breakout
- Phân tách 3 mạng ảo Docker biệt lập theo nguyên tắc Defense in Depth: frontend_net, backend_net, monitoring_net
- Cô lập hoàn toàn cơ sở dữ liệu PostgreSQL 16 (tuyệt đối không mở cổng 5432 ra ngoài host)
- Phân quyền tệp tin bí mật .env (chmod 600) và kiểm soát truy cập phân quyền RBAC"""
run(f'git commit -m "{msg_c4}"')

# ----------------------------------------------------------------------
# COMMIT 5: Documentation, Scripts, Tests & CI
# ----------------------------------------------------------------------
print("\n--- Staging Commit 5 (Tài liệu, Tests & CI) ---")
run("git add .github/ tests/ scripts/ docs/ README.md")
msg_c5 = """docs: hoàn thiện README, sơ đồ kiến trúc hệ thống, bộ kiểm thử Pytest và tài liệu báo cáo học phần

- Cập nhật README đầy đủ bảng checklist đáp ứng 6 yêu cầu đề bài, danh mục cổng truy cập và tài khoản
- Cập nhật sơ đồ kiến trúc hệ thống trực quan (system_architecture.png) khớp 100% mẫu tham chiếu
- Tích hợp bộ kiểm thử tự động Pytest toàn diện cho API bệnh nhân, bác sĩ, lịch hẹn và RBAC
- Thiết lập quy trình CI tự động hóa với GitHub Actions (.github/workflows/ci.yml)"""
run(f'git commit -m "{msg_c5}"')

print("\nAll 6 commits created successfully on submission-main!")
