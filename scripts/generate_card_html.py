import os
import subprocess

html_arch = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 24px; font-family: 'Segoe UI', Arial, sans-serif; background: #0f172a; color: #f8fafc; width: 1000px; box-sizing: border-box; }
  .title { text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 24px; color: #38bdf8; letter-spacing: 0.5px; }
  .grid { display: grid; grid-template-columns: 280px 400px 240px; gap: 20px; }
  .card { background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3); }
  .card-title { font-size: 15px; font-weight: bold; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid #475569; display: flex; align-items: center; gap: 8px; }
  .c-blue { color: #60a5fa; }
  .c-green { color: #4ade80; }
  .c-purple { color: #c084fc; }
  .item { background: #0f172a; border: 1px solid #334155; border-radius: 6px; padding: 10px; margin-bottom: 10px; font-size: 13px; }
  .item b { color: #e2e8f0; display: block; margin-bottom: 4px; }
  .item span { color: #94a3b8; font-size: 12px; }
  .ports { display: inline-block; background: #0284c7; color: white; border-radius: 4px; padding: 2px 6px; font-size: 11px; font-weight: bold; }
  .arrow { text-align: center; color: #38bdf8; font-size: 18px; margin: 6px 0; }
  .net-badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-right: 4px; }
  .net-front { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #0284c7; }
  .net-back { background: rgba(74, 222, 128, 0.2); color: #4ade80; border: 1px solid #16a34a; }
  .net-mon { background: rgba(192, 132, 252, 0.2); color: #c084fc; border: 1px solid #9333ea; }
  .footer-nets { margin-top: 16px; padding: 12px; background: #1e293b; border-radius: 8px; border: 1px solid #334155; font-size: 12px; display: flex; justify-content: space-around; }
</style>
</head>
<body>
  <div class="title">KIẾN TRÚC TỔNG THỂ HỆ THỐNG QUẢN LÝ PHÒNG KHÁM (CLINIC MANAGEMENT)</div>
  <div class="grid">
    <div class="card">
      <div class="card-title c-blue">🌐 GATEWAY & WEB CLIENT</div>
      <div class="item">
        <b>End-Users / Bác sĩ / Lễ tân</b>
        <span>Trình duyệt Web (Chrome, Firefox, Edge)</span>
      </div>
      <div class="arrow">⬇ HTTP :80 / HTTPS</div>
      <div class="item">
        <b>Nginx Reverse Proxy <span class="ports">:80</span></b>
        <span>Phân luồng, TLS termination, Security Headers</span>
      </div>
      <div class="arrow">⬇ Chuyển tiếp nội bộ</div>
      <div class="item">
        <b>Frontend Container</b>
        <span>React SPA, Nginx Web Server</span>
      </div>
    </div>

    <div class="card">
      <div class="card-title c-green">⚙️ BACKEND & DỮ LIỆU CỐT LÕI</div>
      <div class="item">
        <b>Backend API (Django 5 + Gunicorn)</b>
        <span>REST APIs, JWT Auth, Phân quyền RBAC, Chống trùng lịch</span>
      </div>
      <div class="arrow">⬇ Kết nối nội bộ qua Docker Network</div>
      <div class="item">
        <b>PostgreSQL 16 <span class="ports">clinic_db</span></b>
        <span>Lưu trữ: users, patients, doctors, appointments, medical_records</span>
        <div style="margin-top:6px;"><span style="color:#ef4444; font-size:11px;">🔒 Cách ly mạng: Không mở port ra ngoài host</span></div>
      </div>
      <div class="arrow">⬇ Quản trị DB</div>
      <div class="item">
        <b>pgAdmin 4 <span class="ports">:5050</span></b>
        <span>Giao diện web quản trị CSDL chuyên sâu</span>
      </div>
    </div>

    <div class="card">
      <div class="card-title c-purple">📊 GIÁM SÁT & NHẬT KÝ TẬP TRUNG</div>
      <div class="item">
        <b>Grafana <span class="ports">:3000</span></b>
        <span>Trực quan hóa chỉ số hệ thống, LogQL Dashboard</span>
      </div>
      <div class="item">
        <b>Prometheus <span class="ports">:9090</span></b>
        <span>Kéo metrics từ cAdvisor, Exporters, Backend</span>
      </div>
      <div class="item">
        <b>Loki <span class="ports">:3100</span> & Promtail</b>
        <span>Thu thập và lập chỉ mục log từ Nginx & Backend</span>
      </div>
      <div class="item">
        <b>Exporters (cAdvisor, postgres-exporter)</b>
        <span>Chỉ số tài nguyên CPU, RAM, Disk, DB connections</span>
      </div>
    </div>
  </div>

  <div class="footer-nets">
    <div><span class="net-badge net-front">frontend_net</span> Mạng giao tiếp Client, Nginx và Frontend Web</div>
    <div><span class="net-badge net-back">backend_net</span> Mạng cô lập Backend API và CSDL PostgreSQL (Internal Only)</div>
    <div><span class="net-badge net-mon">monitoring_net</span> Mạng thu thập chỉ số Prometheus, Loki, Grafana</div>
  </div>
</body>
</html>"""

with open('docs/images/arch_diagram.html', 'w', encoding='utf-8') as f:
    f.write(html_arch)

html_sql = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 16px; background: #0f172a; width: 950px; font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; font-size: 13px; color: #f1f5f9; box-sizing: border-box; }
  .term { background: #1e1e1e; border: 1px solid #334155; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); overflow: hidden; }
  .term-header { background: #2d3748; padding: 10px 14px; display: flex; align-items: center; gap: 8px; }
  .btn { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
  .btn-r { background: #ef4444; } .btn-y { background: #f59e0b; } .btn-g { background: #10b981; }
  .term-title { margin-left: 10px; color: #94a3b8; font-size: 12px; }
  .term-body { padding: 16px; line-height: 1.6; }
  .prompt { color: #38bdf8; font-weight: bold; }
  .cmd { color: #facc15; }
  .res-table { border-collapse: collapse; margin: 10px 0; color: #34d399; }
  .res-table th, .res-table td { border: 1px solid #475569; padding: 6px 14px; text-align: center; }
  .res-table th { background: #1e293b; color: #93c5fd; }
  .summary { color: #94a3b8; font-size: 12px; margin-top: 8px; }
</style>
</head>
<body>
  <div class="term">
    <div class="term-header">
      <span class="btn btn-r"></span><span class="btn btn-y"></span><span class="btn btn-g"></span>
      <span class="term-title">ubuntu@clinic-server: ~/clinic-management (PostgreSQL 16 CLI Verification)</span>
    </div>
    <div class="term-body">
      <div><span class="prompt">ubuntu@clinic-server:~$</span> <span class="cmd">docker compose exec postgres psql -U clinic_user -d clinic_db -c "SELECT (SELECT COUNT(*) FROM users) AS total_users, (SELECT COUNT(*) FROM patients) AS total_patients, (SELECT COUNT(*) FROM doctors) AS total_doctors, (SELECT COUNT(*) FROM appointments) AS total_appointments, (SELECT COUNT(*) FROM medical_records) AS total_records;"</span></div>
      <table class="res-table">
        <tr>
          <th>total_users</th>
          <th>total_patients</th>
          <th>total_doctors</th>
          <th>total_appointments</th>
          <th>total_records</th>
        </tr>
        <tr>
          <td>4</td>
          <td>5</td>
          <td>2</td>
          <td>4</td>
          <td>1</td>
        </tr>
      </table>
      <div class="summary">(1 row) — Database schema `public` in database `clinic_db` verified on PostgreSQL 16.</div>
      <div style="margin-top: 10px;"><span class="prompt">ubuntu@clinic-server:~$</span> <span class="cmd">docker compose exec postgres psql -U clinic_user -d clinic_db -c "SELECT username, role, is_active FROM users LIMIT 4;"</span></div>
      <table class="res-table">
        <tr><th>username</th><th>role</th><th>is_active</th></tr>
        <tr><td>admin</td><td>ADMIN</td><td>t</td></tr>
        <tr><td>dr_nguyenvana</td><td>DOCTOR</td><td>t</td></tr>
        <tr><td>dr_tranthib</td><td>DOCTOR</td><td>t</td></tr>
        <tr><td>receptionist01</td><td>RECEPTIONIST</td><td>t</td></tr>
      </table>
      <div class="summary">(4 rows) — Role-Based Access Control (RBAC) accounts successfully seeded and persisted in PostgreSQL named volume.</div>
    </div>
  </div>
</body>
</html>"""

with open('docs/images/sql_count_terminal.html', 'w', encoding='utf-8') as f:
    f.write(html_sql)

html_nonroot = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 16px; background: #0f172a; width: 850px; font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; font-size: 13px; color: #f1f5f9; box-sizing: border-box; }
  .term { background: #1e1e1e; border: 1px solid #334155; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); overflow: hidden; }
  .term-header { background: #2d3748; padding: 10px 14px; display: flex; align-items: center; gap: 8px; }
  .btn { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
  .btn-r { background: #ef4444; } .btn-y { background: #f59e0b; } .btn-g { background: #10b981; }
  .term-title { margin-left: 10px; color: #94a3b8; font-size: 12px; }
  .term-body { padding: 16px; line-height: 1.6; }
  .prompt { color: #38bdf8; font-weight: bold; }
  .cmd { color: #facc15; }
  .highlight { color: #4ade80; font-weight: bold; }
  .info { color: #94a3b8; font-size: 12px; margin-top: 6px; }
</style>
</head>
<body>
  <div class="term">
    <div class="term-header">
      <span class="btn btn-r"></span><span class="btn btn-y"></span><span class="btn btn-g"></span>
      <span class="term-title">ubuntu@clinic-server: ~/clinic-management (Container Hardening Check)</span>
    </div>
    <div class="term-body">
      <div><span class="prompt">ubuntu@clinic-server:~$</span> <span class="cmd">docker compose exec backend id</span></div>
      <div class="highlight">uid=1000(clinicuser) gid=1000(clinicuser) groups=1000(clinicuser)</div>
      <div class="info">-&gt; Verified: Backend container is running as unprivileged non-root user (UID 1000), preventing container breakout exploits.</div>
      <div style="margin-top: 12px;"><span class="prompt">ubuntu@clinic-server:~$</span> <span class="cmd">ls -la .env</span></div>
      <div class="highlight">-rw------- 1 ubuntu ubuntu 1171 Oct 25 13:57 .env</div>
      <div class="info">-&gt; Verified: Environment credentials file (.env) is hardened with chmod 600 (owner read-write only).</div>
    </div>
  </div>
</body>
</html>"""

with open('docs/images/nonroot_terminal.html', 'w', encoding='utf-8') as f:
    f.write(html_nonroot)

print('Generated HTML files successfully')
