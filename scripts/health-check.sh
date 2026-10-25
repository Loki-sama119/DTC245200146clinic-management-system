#!/usr/bin/env bash
# ==============================================================================
# CLINIC MANAGEMENT SYSTEM — HEALTH CHECK SCRIPT
# ==============================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}     KIỂM TRA SỨC KHỎE HỆ THỐNG CLINIC MANAGEMENT (DOCKER COMPOSE)    ${NC}"
echo -e "${BLUE}======================================================================${NC}"

# 1. Kiểm tra trạng thái containers
echo -e "\n${YELLOW}1. Trạng thái các Docker Containers:${NC}"
docker compose ps

# 2. Kiểm tra Health Endpoint Backend
echo -e "\n${YELLOW}2. Kiểm tra Backend API Health Endpoint (/api/health/):${NC}"
HEALTH_JSON=$(curl -s http://127.0.0.1/api/health/ || true)
if [[ "$HEALTH_JSON" == *"healthy"* ]]; then
  echo -e "${GREEN}[PASS] Backend API & Database: $HEALTH_JSON${NC}"
else
  echo -e "${RED}[FAIL] Backend API không phản hồi hoặc Database mất kết nối: $HEALTH_JSON${NC}"
fi

# 3. Kiểm tra Nginx Security Headers
echo -e "\n${YELLOW}3. Kiểm tra Nginx Reverse Proxy & Security Headers:${NC}"
HEADERS=$(curl -s -I http://127.0.0.1/ | grep -iE "X-Frame-Options|X-Content-Type-Options|X-XSS-Protection" || true)
if [[ -n "$HEADERS" ]]; then
  echo -e "${GREEN}[PASS] Nginx Security Headers được áp dụng đầy đủ:${NC}"
  echo "$HEADERS"
else
  echo -e "${RED}[FAIL] Thiếu Security Headers trên Nginx!${NC}"
fi

# 4. Kiểm tra pgAdmin 4
echo -e "\n${YELLOW}4. Kiểm tra pgAdmin 4 Web GUI (Port 5050):${NC}"
PG_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5050/ || true)
if [[ "$PG_CODE" == "200" || "$PG_CODE" == "302" ]]; then
  echo -e "${GREEN}[PASS] pgAdmin 4 đang hoạt động (HTTP Status: $PG_CODE)${NC}"
else
  echo -e "${RED}[FAIL] pgAdmin 4 không phản hồi (HTTP Status: $PG_CODE)${NC}"
fi

# 5. Kiểm tra Prometheus
echo -e "\n${YELLOW}5. Kiểm tra Prometheus Server (Port 9090):${NC}"
PROM_READY=$(curl -s http://127.0.0.1:9090/-/ready || true)
if [[ "$PROM_READY" == *"Prometheus Server is Ready"* ]]; then
  echo -e "${GREEN}[PASS] Prometheus Server sẵn sàng thu thập metrics${NC}"
else
  echo -e "${RED}[FAIL] Prometheus Server chưa sẵn sàng: $PROM_READY${NC}"
fi

# 6. Kiểm tra Grafana
echo -e "\n${YELLOW}6. Kiểm tra Grafana Server (Port 3000):${NC}"
GRAFANA_HEALTH=$(curl -s http://127.0.0.1:3000/api/health || true)
if [[ "$GRAFANA_HEALTH" == *"ok"* ]]; then
  echo -e "${GREEN}[PASS] Grafana Server: $GRAFANA_HEALTH${NC}"
else
  echo -e "${RED}[FAIL] Grafana Server lỗi: $GRAFANA_HEALTH${NC}"
fi

# 7. Kiểm tra Loki
echo -e "\n${YELLOW}7. Kiểm tra Grafana Loki (Port 3100):${NC}"
LOKI_READY=$(curl -s http://127.0.0.1:3100/ready || true)
if [[ "$LOKI_READY" == *"ready"* ]]; then
  echo -e "${GREEN}[PASS] Grafana Loki Ingester sẵn sàng${NC}"
else
  echo -e "${RED}[FAIL] Grafana Loki chưa sẵn sàng: $LOKI_READY${NC}"
fi

echo -e "\n${BLUE}======================================================================${NC}"
echo -e "${GREEN}             HOÀN TẤT KIỂM TRA SỨC KHỎE HỆ THỐNG!                     ${NC}"
echo -e "${BLUE}======================================================================${NC}"
