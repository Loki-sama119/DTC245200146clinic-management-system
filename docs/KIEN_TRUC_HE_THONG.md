# TÀI LIỆU KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

- **Hệ thống**: Clinic Management System (Phòng khám Đa khoa Phúc An)
- **Sinh viên thực hiện**: Nguyễn Văn Thắng (MSV: DTC245200146)

---

## 1. MÔ HÌNH KIẾN TRÚC TỔNG THỂ (CONTAINER ORCHESTRATION)

```mermaid
flowchart TD
    Client["Client Browser (Máy tính / Điện thoại)"] -->|Cổng 80 HTTP| Nginx["clinic_nginx (Reverse Proxy & Gateway)"]

    subgraph FrontendNet ["Docker Network: frontend_net"]
        Nginx -->|/ route| FrontSPA["clinic_frontend (React/Vite SPA)"]
        Nginx -->|/api/ route| BackAPI["clinic_backend (Django + Gunicorn WSGI)"]
    end

    subgraph BackendNet ["Docker Network: backend_net (Cô lập dữ liệu)"]
        BackAPI -->|Port 5432 nội bộ| DB["clinic_postgres (PostgreSQL 16)"]
        PGAdmin["clinic_pgadmin (pgAdmin 4 :5050)"] --> DB
        PGExp["clinic_postgres_exporter (:9187)"] --> DB
    end

    subgraph MonitoringNet ["Docker Network: monitoring_net (Giám sát & Logs)"]
        Prom["clinic_prometheus (:9090)"] -->|Scrape metrics| BackAPI
        Prom -->|Scrape metrics| PGExp
        Prom -->|Scrape metrics| CAdvisor["clinic_cadvisor (:8080)"]
        Promtail["clinic_promtail"] -->|Tail Log files| Nginx
        Promtail -->|Tail Log files| BackAPI
        Promtail -->|Push Log Stream| Loki["clinic_loki (:3100)"]
        Grafana["clinic_grafana (:3000)"] -->|Query PromQL| Prom
        Grafana -->|Query LogQL| Loki
    end
```

---

## 2. PHÂN TÁCH VÙNG MẠNG BẢO MẬT (NETWORK ISOLATION)
Hệ thống thiết lập 3 mạng ảo biệt lập theo nguyên tắc **Defense in Depth**:
1. `frontend_net`: Cho phép `nginx`, `frontend` và `backend` giao tiếp phục vụ người dùng.
2. `backend_net`: Cô lập hoàn toàn cơ sở dữ liệu `postgres`, `pgadmin` và `postgres-exporter`. Người dùng từ mạng ngoài không thể kết nối trực tiếp đến cổng 5432 của PostgreSQL.
3. `monitoring_net`: Mạng riêng để `prometheus`, `grafana`, `loki` và `promtail` thu thập dữ liệu giám sát và logs mà không làm ảnh hưởng đến lưu lượng nghiệp vụ chính.
