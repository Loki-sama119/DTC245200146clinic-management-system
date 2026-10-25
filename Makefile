.PHONY: help up down restart logs build migrate seed test health clean

help:
	@echo "=========================================================="
	@echo "CLINIC MANAGEMENT SYSTEM — LỆNH QUẢN TRỊ DOCKER COMPOSE"
	@echo "=========================================================="
	@echo "  make up        : Khởi động toàn bộ dịch vụ (chạy nền)"
	@echo "  make down      : Dừng và gỡ bỏ các container"
	@echo "  make restart   : Khởi động lại toàn bộ dịch vụ"
	@echo "  make logs      : Xem log thời gian thực của toàn bộ hệ thống"
	@echo "  make build     : Build lại các Docker images"
	@echo "  make migrate   : Chạy database migrations cho Django"
	@echo "  make seed      : Nạp dữ liệu tài khoản và bệnh nhân mẫu"
	@echo "  make test      : Chạy bộ kiểm thử tự động pytest"
	@echo "  make health    : Kiểm tra sức khỏe toàn bộ các container"
	@echo "  make clean     : Dọn dẹp volumes và cache docker thừa"
	@echo "=========================================================="

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

build:
	docker compose build

migrate:
	docker compose exec backend python manage.py migrate

seed:
	docker compose exec backend python manage.py seed_data

test:
	docker compose exec backend pytest

health:
	@bash scripts/health-check.sh

clean:
	docker compose down -v --remove-orphans
