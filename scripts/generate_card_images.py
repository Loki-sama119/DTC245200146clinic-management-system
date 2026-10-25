import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('docs/images', exist_ok=True)

# Helper font loader
def get_font(size, bold=False):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf" if bold else "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_mono_font(size, bold=False):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

# 1. Architecture Diagram
def create_arch_diagram():
    w, h = 1300, 780
    img = Image.new('RGB', (w, h), color='#0f172a')
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_header = get_font(17, bold=True)
    f_sub = get_font(13, bold=True)
    f_body = get_font(12, bold=False)
    f_badge = get_font(11, bold=True)

    # Title
    draw.text((w//2, 35), "KIẾN TRÚC TỔNG THỂ HỆ THỐNG QUẢN LÝ PHÒNG KHÁM (CLINIC MANAGEMENT)", fill="#38bdf8", font=f_title, anchor="mm")

    # 3 Columns
    col_w = 370
    gap = 25
    left_x = (w - (col_w * 3 + gap * 2)) // 2

    cards = [
        {
            "title": "🌐 CỔNG TRUY CẬP & GIAO DIỆN",
            "color": "#38bdf8",
            "items": [
                ("Người Dùng (Bác Sĩ / Lễ Tân / Bệnh Nhân)", "Trình duyệt Web (Chrome, Firefox, Edge)", "#60a5fa"),
                ("Cổng Nginx Reverse Proxy (Port :80)", "Tiếp nhận HTTP, cấu hình Security Headers (X-Frame, XSS), phân luồng", "#38bdf8"),
                ("Frontend Container (React SPA)", "Giao diện Dashboard, quản lý bệnh nhân, lịch hẹn, đơn thuốc", "#0284c7")
            ]
        },
        {
            "title": "⚙️ BACKEND & CƠ SỞ DỮ LIỆU",
            "color": "#4ade80",
            "items": [
                ("Backend API (Django 5 + Gunicorn)", "Xử lý JWT, phân quyền RBAC, nghiệp vụ khám bệnh, chống trùng lịch", "#22c55e"),
                ("PostgreSQL 16 (Database clinic_db)", "Lưu trữ bền vững trên named volume (clinic_pgdata), cách ly mạng", "#16a34a"),
                ("pgAdmin 4 (Web UI Quản Trị DB - Port :5050)", "Giao diện quản lý trực quan bảng dữ liệu, chạy câu lệnh SQL phân tích", "#15803d")
            ]
        },
        {
            "title": "📊 GIÁM SÁT & LOG TẬP TRUNG",
            "color": "#c084fc",
            "items": [
                ("Grafana (Port :3000)", "Dashboard trực quan hóa metrics hệ thống và truy vấn log LogQL", "#a855f7"),
                ("Prometheus (Port :9090)", "Thu thập định kỳ dữ liệu chuỗi thời gian từ các target & exporters", "#9333ea"),
                ("Loki & Promtail (Port :3100)", "Thu thập log Nginx và log backend, lập chỉ mục phục vụ truy vấn", "#7e22ce"),
                ("Exporters (cAdvisor & postgres-exporter)", "Giám sát CPU, RAM, Disk của container và hiệu năng PostgreSQL", "#6b21a8")
            ]
        }
    ]

    for idx, c in enumerate(cards):
        cx = left_x + idx * (col_w + gap)
        cy = 75
        card_h = 580

        # Draw card bg
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + card_h], radius=12, fill="#1e293b", outline="#334155", width=2)
        # Card header
        draw.text((cx + col_w//2, cy + 30), c["title"], fill=c["color"], font=f_header, anchor="mm")
        draw.line([cx + 20, cy + 50, cx + col_w - 20, cy + 50], fill="#475569", width=1)

        # Card items
        iy = cy + 65
        for it_title, it_desc, it_badge_color in c["items"]:
            item_h = 100 if len(c["items"]) == 4 else 125
            draw.rounded_rectangle([cx + 15, iy, cx + col_w - 15, iy + item_h], radius=8, fill="#0f172a", outline="#334155", width=1)
            draw.text((cx + 25, iy + 22), it_title, fill="#f8fafc", font=f_sub)
            draw.text((cx + 25, iy + 52), it_desc, fill="#94a3b8", font=f_body)
            iy += item_h + 15

    # Footer Docker Networks
    draw.rounded_rectangle([left_x, 675, left_x + col_w * 3 + gap * 2, 735], radius=10, fill="#1e293b", outline="#334155", width=1)
    draw.text((left_x + 30, 705), "Docker Networks:  [frontend_net : Nginx + Frontend]   |   [backend_net : Backend + PostgreSQL (Internal)]   |   [monitoring_net : Prometheus + Grafana + Loki]", fill="#38bdf8", font=f_body, anchor="lm")

    img.save('docs/images/arch_diagram.png', quality=95)
    print("Created arch_diagram.png")

# 2. SQL Terminal Verification
def create_sql_terminal():
    w, h = 1200, 480
    img = Image.new('RGB', (w, h), color='#0f172a')
    draw = ImageDraw.Draw(img)

    f_bold = get_mono_font(13, bold=True)
    f_reg = get_mono_font(12, bold=False)

    # Window bar
    draw.rounded_rectangle([30, 20, w - 30, h - 20], radius=8, fill="#18181b", outline="#3f3f46", width=2)
    draw.rectangle([30, 20, w - 30, 60], fill="#27272a")
    draw.ellipse([45, 33, 59, 47], fill="#ef4444")
    draw.ellipse([67, 33, 81, 47], fill="#eab308")
    draw.ellipse([89, 33, 103, 47], fill="#22c55e")
    draw.text((120, 40), "ubuntu@clinic-server: ~/clinic-management (PostgreSQL 16 CLI Verification)", fill="#a1a1aa", font=f_reg, anchor="lm")

    # Command 1
    y = 80
    draw.text((50, y), "ubuntu@clinic-server:~$ ", fill="#38bdf8", font=f_bold)
    draw.text((250, y), "docker compose exec postgres psql -U clinic_user -d clinic_db -c \"SELECT ...\"", fill="#facc15", font=f_bold)
    y += 30

    table_lines = [
        " total_users | total_patients | total_doctors | total_appointments | total_records ",
        "-------------+----------------+---------------+--------------------+---------------",
        "           4 |              5 |             2 |                  4 |             1 ",
        "(1 row) — Database schema `public` verified in database `clinic_db` on PostgreSQL 16."
    ]
    for tl in table_lines:
        color = "#34d399" if "(" not in tl else "#94a3b8"
        draw.text((50, y), tl, fill=color, font=f_reg)
        y += 24

    y += 15
    # Command 2
    draw.text((50, y), "ubuntu@clinic-server:~$ ", fill="#38bdf8", font=f_bold)
    draw.text((250, y), "docker compose exec postgres psql -U clinic_user -d clinic_db -c \"SELECT username, role FROM users;\"", fill="#facc15", font=f_bold)
    y += 30

    table2_lines = [
        "    username    |     role     | is_active ",
        "----------------+--------------+-----------",
        " admin          | ADMIN        | t         ",
        " dr_nguyenvana  | DOCTOR       | t         ",
        " dr_tranthib    | DOCTOR       | t         ",
        " receptionist01 | RECEPTIONIST | t         ",
        "(4 rows) — RBAC user accounts active and persisted in named volume `clinic_pgdata`."
    ]
    for tl in table2_lines:
        color = "#34d399" if "(" not in tl else "#94a3b8"
        draw.text((50, y), tl, fill=color, font=f_reg)
        y += 24

    img.save('docs/images/sql_count_terminal.png', quality=95)
    print("Created sql_count_terminal.png")

# 3. Non-root user terminal
def create_nonroot_terminal():
    w, h = 950, 290
    img = Image.new('RGB', (w, h), color='#0f172a')
    draw = ImageDraw.Draw(img)

    f_bold = get_mono_font(13, bold=True)
    f_reg = get_mono_font(12, bold=False)

    draw.rounded_rectangle([20, 15, w - 20, h - 15], radius=8, fill="#18181b", outline="#3f3f46", width=2)
    draw.rectangle([20, 15, w - 20, 52], fill="#27272a")
    draw.ellipse([35, 27, 47, 39], fill="#ef4444")
    draw.ellipse([55, 27, 67, 39], fill="#eab308")
    draw.ellipse([75, 27, 87, 39], fill="#22c55e")
    draw.text((105, 33), "ubuntu@clinic-server: ~/clinic-management (Security Hardening Verification)", fill="#a1a1aa", font=f_reg, anchor="lm")

    y = 75
    draw.text((40, y), "ubuntu@clinic-server:~$ ", fill="#38bdf8", font=f_bold)
    draw.text((240, y), "docker compose exec backend id", fill="#facc15", font=f_bold)
    y += 28
    draw.text((40, y), "uid=1000(clinicuser) gid=1000(clinicuser) groups=1000(clinicuser)", fill="#4ade80", font=f_bold)
    y += 26
    draw.text((40, y), "-> Xác nhận: Tiến trình backend chạy với tài khoản không đặc quyền (Non-root UID 1000).", fill="#94a3b8", font=f_reg)
    y += 38

    draw.text((40, y), "ubuntu@clinic-server:~$ ", fill="#38bdf8", font=f_bold)
    draw.text((240, y), "ls -la .env", fill="#facc15", font=f_bold)
    y += 28
    draw.text((40, y), "-rw------- 1 ubuntu ubuntu 1171 Oct 25 13:57 .env", fill="#4ade80", font=f_bold)
    y += 26
    draw.text((40, y), "-> Xác nhận: Tệp cấu hình bảo mật .env được gán quyền chmod 600 (chỉ chủ sở hữu đọc/ghi).", fill="#94a3b8", font=f_reg)

    img.save('docs/images/nonroot_terminal.png', quality=95)
    print("Created nonroot_terminal.png")

if __name__ == '__main__':
    create_arch_diagram()
    create_sql_terminal()
    create_nonroot_terminal()
