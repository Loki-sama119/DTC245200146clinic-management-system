import os
from PIL import Image, ImageDraw, ImageFont

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

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def generate_system_architecture_diagram():
    w, h = 1680, 1080
    img = Image.new('RGB', (w, h), color='#0b0f19')
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_subtitle = get_font(13, bold=False)
    f_col_title = get_font(15, bold=True)
    f_card_title = get_font(14, bold=True)
    f_badge = get_font(11, bold=True)
    f_body = get_font(12, bold=False)
    f_body_bold = get_font(12, bold=True)
    f_flow = get_font(11, bold=True)
    f_net = get_font(11, bold=True)

    # 1. Header Banner
    draw.rounded_rectangle([35, 20, w - 35, 95], radius=12, fill='#111827', outline='#1f2937', width=1)
    title_text = "KIẾN TRÚC TỔNG THỂ HỆ THỐNG QUẢN LÝ PHÒNG KHÁM PHÚC AN"
    draw.text((w // 2, 45), title_text, fill='#38bdf8', font=f_title, anchor="mm")
    sub_text = "Mô hình điều phối 11 Container Docker Compose, phân tách 3 mạng ảo biệt lập (Defense in Depth) & Giám sát tập trung"
    draw.text((w // 2, 75), sub_text, fill='#94a3b8', font=f_subtitle, anchor="mm")

    # 3 Zone Columns
    col_w = 510
    gap = 25
    start_x = 40
    top_y = 115
    col_h = 790

    zones = [
        {
            "tag": "ZONE 1: GATEWAY & WEB CLIENT",
            "net": "Docker Network: frontend_net",
            "theme": "#38bdf8",
            "border": "#0284c7",
            "cards": [
                {
                    "title": "Người Dùng (Bác Sĩ / Lễ Tân / Admin)",
                    "badges": [("Clients", "#3b82f6"), ("Browsers", "#0284c7")],
                    "container": "Web Browser (Chrome, Edge, Safari, Firefox)",
                    "desc": "Truy cập giao diện quản lý khám chữa bệnh, đặt lịch hẹn, quản lý hồ sơ bệnh án điện tử và đơn thuốc qua giao thức HTTP/HTTPS.",
                    "notes": "Xác thực JWT Token, phân quyền chặt chẽ RBAC (Admin, Doctor, Receptionist)."
                },
                {
                    "title": "Nginx Reverse Proxy & Gateway",
                    "badges": [("Port :80", "#0284c7"), ("clinic_nginx", "#0369a1")],
                    "container": "Nginx 1.25 Alpine Linux Container",
                    "desc": "Điểm tiếp nhận lưu lượng duy nhất từ bên ngoài. Phân luồng: '/' phục vụ Frontend SPA, '/api/' chuyển tiếp Django Backend.",
                    "notes": "Bảo mật với Security Headers (X-Frame, CSP, HSTS, XSS), Rate Limiting, Nginx Logs."
                },
                {
                    "title": "React Frontend SPA Application",
                    "badges": [("SPA Web", "#0284c7"), ("clinic_frontend", "#0891b2")],
                    "container": "React 18 + Vite SPA, Nginx Web Server",
                    "desc": "Giao diện Single Page Application tối ưu trải nghiệm y tế: đặt lịch thông minh, biểu đồ thống kê, tra cứu lịch sử khám bệnh.",
                    "notes": "Giao tiếp Backend qua REST API, quản lý token phiên làm việc an toàn."
                }
            ],
            "flows": ["⬇ HTTP:80 Gửi yêu cầu truy cập", "⬇ Phân luồng URL: / (Frontend) & /api/ (Backend)"]
        },
        {
            "tag": "ZONE 2: BACKEND & CƠ SỞ DỮ LIỆU",
            "net": "Docker Network: backend_net (Cô lập dữ liệu)",
            "theme": "#4ade80",
            "border": "#16a34a",
            "cards": [
                {
                    "title": "Django REST Backend Core API",
                    "badges": [("Port :8000", "#16a34a"), ("clinic_backend", "#15803d")],
                    "container": "Django 5.0 + Gunicorn WSGI Server (Python 3.11)",
                    "desc": "Xử lý toàn bộ logic nghiệp vụ y tế: xác thực JWT, RBAC, kiểm tra chống trùng lịch khám, quản lý đơn thuốc, OpenAPI/Swagger docs.",
                    "notes": "Chạy tài khoản không đặc quyền clinicuser (UID 1000). Xuất metrics tại /api/metrics."
                },
                {
                    "title": "PostgreSQL 16 Database Server",
                    "badges": [("Port :5432", "#dc2626"), ("clinic_postgres", "#991b1b")],
                    "container": "PostgreSQL 16 Alpine Database Container",
                    "desc": "Lưu trữ bền vững toàn bộ dữ liệu hệ thống: Users, Patients, Doctors, Appointments, Medical Records và Audit Logs.",
                    "notes": "Gắn Named Volume clinic_pgdata. KHÔNG mở cổng ra Internet (Cô lập mạng an toàn)."
                },
                {
                    "title": "pgAdmin 4 Web Database Manager",
                    "badges": [("Port :5050", "#16a34a"), ("clinic_pgadmin", "#15803d")],
                    "container": "pgAdmin 4 Web GUI Management Tool v8.4",
                    "desc": "Giao diện quản trị CSDL trực quan cho Admin: quản lý bảng, kiểm tra ràng buộc khóa ngoại, truy vấn SQL và sao lưu định kỳ.",
                    "notes": "Kết nối nội bộ trực tiếp đến container postgres qua backend_net an toàn."
                }
            ],
            "flows": ["⬇ Truy vấn ORM / SQL qua cổng nội bộ 5432", "⬇ Quản trị CSDL & kiểm tra schema"]
        },
        {
            "tag": "ZONE 3: GIÁM SÁT & NHẬT KÝ TẬP TRUNG",
            "net": "Docker Network: monitoring_net (Giám sát)",
            "theme": "#c084fc",
            "border": "#9333ea",
            "cards": [
                {
                    "title": "Grafana Observability Dashboard",
                    "badges": [("Port :3000", "#9333ea"), ("clinic_grafana", "#7e22ce")],
                    "container": "Grafana 10.4.0 (Tự động nạp cấu hình Dashboards)",
                    "desc": "Trực quan hóa thời gian thực: tải CPU/RAM container, QPS Nginx, thời gian phản hồi Backend API và phân tích LogQL thời gian thực.",
                    "notes": "Provisioning tự động các Data Sources (Prometheus, Loki) và dashboard y tế."
                },
                {
                    "title": "Prometheus Metrics Time-Series DB",
                    "badges": [("Port :9090", "#9333ea"), ("clinic_prometheus", "#6b21a8")],
                    "container": "Prometheus Server v2.51.0 (Pull Model TSDB)",
                    "desc": "Định kỳ cào (scrape) chỉ số từ Django /metrics, cAdvisor và postgres-exporter theo chu kỳ 10 giây; lưu trữ TSDB bền vững.",
                    "notes": "Hỗ trợ ngôn ngữ truy vấn PromQL linh hoạt cho giám sát và cảnh báo sự cố."
                },
                {
                    "title": "Loki, Promtail & Container Exporters",
                    "badges": [("Port :3100", "#7e22ce"), ("Loki & Exporters", "#581c87")],
                    "container": "Loki 2.9, Promtail 2.9, cAdvisor v0.49, pg-exporter",
                    "desc": "Promtail đọc log Nginx & Backend gửi về Loki để tìm kiếm LogQL tập trung; cAdvisor & pg-exporter thu thập tài nguyên container & DB.",
                    "notes": "Giúp truy vết sự cố hệ thống tức thì không cần SSH vào từng container."
                }
            ],
            "flows": ["⬇ Truy vấn dữ liệu PromQL & LogQL", "⬇ Thu thập log stream & metrics exporters"]
        }
    ]

    for col_idx, z in enumerate(zones):
        zx = start_x + col_idx * (col_w + gap)
        zy = top_y

        # Draw Zone Box
        draw.rounded_rectangle([zx, zy, zx + col_w, zy + col_h], radius=12, fill='#111827', outline=z["border"], width=2)

        # Zone Header
        draw.rounded_rectangle([zx, zy, zx + col_w, zy + 50], radius=10, fill='#1e293b')
        draw.text((zx + 18, zy + 15), z["tag"], fill=z["theme"], font=f_col_title)
        draw.line([zx, zy + 50, zx + col_w, zy + 50], fill=z["border"], width=1)

        # Network sub-header
        draw.text((zx + 18, zy + 60), z["net"], fill='#94a3b8', font=f_badge)

        # Cards inside Zone
        card_y = zy + 82
        card_h = 188

        for c_idx, card in enumerate(z["cards"]):
            cx = zx + 14
            cw = col_w - 28

            # Draw Card
            draw.rounded_rectangle([cx, card_y, cx + cw, card_y + card_h], radius=8, fill='#0f172a', outline='#334155', width=1)

            # Draw Badges on the right
            bx = cx + cw - 12
            for b_text, b_color in reversed(card["badges"]):
                p_bbox = draw.textbbox((0, 0), b_text, font=f_badge)
                p_w = p_bbox[2] - p_bbox[0] + 14
                bx -= p_w
                draw.rounded_rectangle([bx, card_y + 11, bx + p_w, card_y + 29], radius=4, fill=b_color)
                draw.text((bx + 7, card_y + 13), b_text, fill='#ffffff', font=f_badge)
                bx -= 6

            # Available width for Title
            max_title_w = bx - (cx + 14) - 8
            title_text = card["title"]
            draw.text((cx + 14, card_y + 12), title_text, fill='#ffffff', font=f_card_title)

            # Container line
            draw.text((cx + 14, card_y + 36), "Container: " + card["container"], fill='#38bdf8', font=f_body_bold)

            # Description (wrapped)
            desc_lines = wrap_text(draw, card["desc"], f_body, cw - 28)
            dy = card_y + 58
            for line in desc_lines[:2]:
                draw.text((cx + 14, dy), line, fill='#cbd5e1', font=f_body)
                dy += 18

            # Note
            draw.line([cx + 14, card_y + 104, cx + cw - 14, card_y + 104], fill='#1e293b', width=1)
            draw.text((cx + 14, card_y + 113), "Đặc điểm: ", fill='#f59e0b', font=f_badge)
            note_lines = wrap_text(draw, card["notes"], f_body, cw - 95)
            ny = card_y + 112
            for nline in note_lines[:3]:
                draw.text((cx + 85, ny), nline, fill='#94a3b8', font=f_body)
                ny += 18

            card_y += card_h

            # If there's an arrow to next card
            if c_idx < len(z["flows"]):
                flow_text = z["flows"][c_idx]
                draw.text((zx + col_w // 2, card_y + 16), flow_text, fill=z["theme"], font=f_flow, anchor="mm")
                card_y += 32

    # 4. Bottom Summary / Legend (Defense in Depth)
    foot_y = 920
    draw.rounded_rectangle([35, foot_y, w - 35, foot_y + 135], radius=10, fill='#111827', outline='#374151', width=1)
    
    # Legend Title
    draw.text((50, foot_y + 16), "QUY HOẠCH MẠNG DOCKER & NGUYÊN TẮC BẢO MẬT HỆ THỐNG (DEFENSE IN DEPTH):", fill='#f8fafc', font=f_card_title)

    # Row 1 (y: foot_y + 45)
    # frontend_net
    draw.rounded_rectangle([50, foot_y + 45, 180, foot_y + 71], radius=6, fill='#0284c7')
    draw.text((60, foot_y + 50), "frontend_net", fill='#ffffff', font=f_net)
    f_desc = "Giao tiếp Client -> Nginx Gateway -> React Frontend & Django Backend. Chỉ mở duy nhất cổng 80."
    draw.text((195, foot_y + 51), f_desc, fill='#cbd5e1', font=f_body)

    # monitoring_net
    draw.rounded_rectangle([880, foot_y + 45, 1020, foot_y + 71], radius=6, fill='#7e22ce')
    draw.text((890, foot_y + 50), "monitoring_net", fill='#ffffff', font=f_net)
    m_desc = "Mạng nội bộ riêng biệt thu thập metrics & logs qua Prometheus, Loki & Grafana, không nghẽn nghiệp vụ."
    draw.text((1035, foot_y + 51), m_desc, fill='#cbd5e1', font=f_body)

    # Row 2 (y: foot_y + 85)
    # backend_net
    draw.rounded_rectangle([50, foot_y + 85, 180, foot_y + 111], radius=6, fill='#16a34a')
    draw.text((62, foot_y + 90), "backend_net", fill='#ffffff', font=f_net)
    b_desc = "Vùng mạng CÔ LẬP CSDL PostgreSQL 16 & pgAdmin. Ngăn chặn triệt để tấn công trực tiếp từ Internet."
    draw.text((195, foot_y + 91), b_desc, fill='#cbd5e1', font=f_body)

    # Non-Root UID
    draw.rounded_rectangle([880, foot_y + 85, 1020, foot_y + 111], radius=6, fill='#b45309')
    draw.text((895, foot_y + 90), "Non-Root UID", fill='#ffffff', font=f_net)
    u_desc = "Toàn bộ container chạy người dùng clinicuser (UID 1000) nhằm triệt tiêu nguy cơ container breakout."
    draw.text((1035, foot_y + 91), u_desc, fill='#cbd5e1', font=f_body)

    os.makedirs('docs/images', exist_ok=True)
    img_path = 'docs/images/arch_diagram.png'
    img.save(img_path, quality=95)
    print(f"Successfully generated {img_path} ({w}x{h})")

if __name__ == '__main__':
    generate_system_architecture_diagram()
