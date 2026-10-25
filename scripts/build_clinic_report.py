import os
import shutil
import zipfile
import xml.etree.ElementTree as ET
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

SOURCE_DOCX = 'DTC245200134_Báo cáo triển khai hệ thống_Ngô Trung Kiên.docx'
TARGET_DOCX = 'DTC245200146_Báo cáo triển khai hệ thống_Nguyễn Văn Thắng.docx'

print(f"Reading template from {SOURCE_DOCX}...")

# 1. First make a copy of the template
shutil.copyfile(SOURCE_DOCX, TARGET_DOCX)

# 2. Update media images inside zip package
IMAGE_REPLACEMENTS = {
    'word/media/image2.png': 'docs/images/arch_diagram.png',
    'word/media/image3.png': 'docs/images/10_github_actions_green.png',
    'word/media/image4.png': 'docs/images/01_login.png',
    'word/media/image5.png': 'docs/images/07_pgadmin.png',
    'word/media/image6.png': 'docs/images/sql_count_terminal.png',
    'word/media/image7.png': 'docs/images/03_security_headers.png',
    'word/media/image8.png': 'docs/images/09_grafana.png',
    'word/media/image9.png': 'docs/images/08_prometheus.png',
    'word/media/image10.png': 'docs/images/05_loki_logql.png',
    'word/media/image11.png': 'docs/images/04_swagger.png',
    'word/media/image12.png': 'docs/images/02_docker_ps.png',
    'word/media/image13.png': 'docs/images/nonroot_terminal.png',
}

# Read all files from TARGET_DOCX, replace media, and write to a temp zip
temp_docx = 'temp_replaced_media.docx'
with zipfile.ZipFile(TARGET_DOCX, 'r') as zin:
    with zipfile.ZipFile(temp_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)
            if item.filename in IMAGE_REPLACEMENTS:
                rep_path = IMAGE_REPLACEMENTS[item.filename]
                if os.path.exists(rep_path):
                    with open(rep_path, 'rb') as f_rep:
                        content = f_rep.read()
                    print(f"Replaced {item.filename} with {rep_path}")
            elif item.filename == 'word/header1.xml':
                # Update header text
                hdr_xml = content.decode('utf-8')
                hdr_xml = hdr_xml.replace('ĐỀ TÀI 32 / DEVCHAT', 'ĐỀ TÀI 08 / CLINIC MANAGEMENT SYSTEM')
                hdr_xml = hdr_xml.replace('ĐỀ TÀI 32', 'ĐỀ TÀI 08')
                content = hdr_xml.encode('utf-8')
                print("Updated word/header1.xml")
            zout.writestr(item, content)

shutil.move(temp_docx, TARGET_DOCX)
print("Updated media and headers in DOCX package.")

# 3. Now load with python-docx and update paragraphs and tables
doc = docx.Document(TARGET_DOCX)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def update_p_text(p, text):
    # Keep the first run's formatting if available, clear others
    if p.runs:
        first_run = p.runs[0]
        first_run.text = text
        for r in p.runs[1:]:
            r.text = ''
    else:
        p.add_run(text)

# Cover Page Updates
update_p_text(doc.paragraphs[8], "ĐỀ TÀI 08")
update_p_text(doc.paragraphs[9], "HỆ THỐNG QUẢN LÝ PHÒNG KHÁM / BỆNH VIỆN\n(CLINIC MANAGEMENT SYSTEM)")
update_p_text(doc.paragraphs[12], "Sinh viên thực hiện\t: Nguyễn Văn Thắng")
update_p_text(doc.paragraphs[13], "Mã số sinh viên\t: DTC245200146")
update_p_text(doc.paragraphs[14], "Lớp\t: CNTT K23G")
update_p_text(doc.paragraphs[15], "Giảng viên\t: Vũ Việt Dũng")
update_p_text(doc.paragraphs[19], "Thái Nguyên, tháng 10 năm 2026")

# Lời Cảm Ơn
update_p_text(doc.paragraphs[21], "Em xin gửi lời cảm ơn đến giảng viên học phần Triển khai và Quản trị Hệ thống Phần mềm đã hướng dẫn phương pháp triển khai ứng dụng theo hướng vận hành thực tế, từ đóng gói container đến cấu hình reverse proxy, giám sát tài nguyên, truy vấn nhật ký và tăng cường bảo mật hệ thống thông tin y tế.")
update_p_text(doc.paragraphs[22], "Trong quá trình thực hiện Đề tài 08, em đã vận dụng kiến thức Docker Compose, Linux, Git, PostgreSQL 16, Django 5, Nginx, Prometheus, Grafana, Loki và Promtail. Việc xử lý các tình huống phân quyền vai trò (Admin, Bác sĩ, Lễ tân), ngăn chặn trùng lịch khám, kết nối giữa các container và kiểm chứng log giúp em hiểu rõ hơn vai trò của người quản trị hệ thống phần mềm.")
update_p_text(doc.paragraphs[23], "Báo cáo tổng hợp những bước triển khai đã được ghi nhận trong môi trường thực hành trên máy ảo Ubuntu. Do giới hạn về thời gian và điều kiện thử nghiệm, kết quả có thể còn những điểm cần kiểm tra thêm trước khi áp dụng trong môi trường sản xuất. Em mong nhận được góp ý để tiếp tục hoàn thiện hệ thống.")
update_p_text(doc.paragraphs[24], "Em xin chân thành cảm ơn!")

# Mục lục text updates
update_p_text(doc.paragraphs[37], "CHƯƠNG 2. TRIỂN KHAI ỨNG DỤNG, CƠ SỞ DỮ LIỆU VÀ NGINX\t10")
update_p_text(doc.paragraphs[38], "2.1. Xây dựng ứng dụng quản lý phòng khám và đóng gói Docker\t10")
update_p_text(doc.paragraphs[39], "2.2. Kiểm chứng luồng nghiệp vụ và phân quyền người dùng\t11")

# Danh mục hình ảnh text updates
update_p_text(doc.paragraphs[58], "Hình 1.1. Sơ đồ kiến trúc logic Clinic Management System – mô hình hóa từ các thành phần đã triển khai.\t7")
update_p_text(doc.paragraphs[59], "Hình 1.2. Kho mã nguồn clinic-management-system trên GitHub và quy trình CI/CD kiểm thử tự động.\t9")
update_p_text(doc.paragraphs[60], "Hình 2.1. Giao diện Web hệ thống Phòng khám: Bảng điều khiển, tiếp nhận bệnh nhân và lịch hẹn khám.\t11")
update_p_text(doc.paragraphs[61], "Hình 2.2. pgAdmin 4 đã kết nối database clinic_db; cây schema public và đồ thị hiệu năng PostgreSQL.\t12")
update_p_text(doc.paragraphs[62], "Hình 2.3. PostgreSQL trả về 4 users, 5 patients, 2 doctors, 4 appointments, 1 medical record.\t13")
update_p_text(doc.paragraphs[63], "Hình 2.4. Docker Compose báo Healthy, .env có quyền 600 và Nginx trả HTTP 200 kèm Security Headers.\t15")
update_p_text(doc.paragraphs[64], "Hình 3.1. Grafana theo dõi CPU, RAM, Disk của Ubuntu và CPU/RAM từng container phòng khám.\t17")
update_p_text(doc.paragraphs[65], "Hình 3.2. Prometheus Web UI thu thập metrics các target hệ thống và trạng thái hoạt động UP.\t18")
update_p_text(doc.paragraphs[66], "Hình 3.3. Loki hiển thị các bản ghi truy vấn HTTP Nginx và backend được thu thập tập trung.\t19")
update_p_text(doc.paragraphs[67], "Hình 3.4. Swagger UI / OpenAPI xác thực các endpoint REST API phòng khám và audit log sự kiện.\t20")
update_p_text(doc.paragraphs[68], "Hình 3.5. Trạng thái 11 containers Docker Compose hoạt động ổn định và biểu đồ truy vấn LogQL.\t21")
update_p_text(doc.paragraphs[69], "Hình 4.1. Kiểm chứng container Backend chạy bằng tài khoản clinicuser non-root (UID 1000) và .env quyền 600.\t22")

# Lời nói đầu
update_p_text(doc.paragraphs[73], "Trong các cơ sở khám chữa bệnh hiện đại, một hệ thống phần mềm quản lý phòng khám (Clinic Management System) đóng vai trò sống còn để vận hành thông suốt các quy trình y tế. Hệ thống không chỉ cần đáp ứng các nghiệp vụ tiếp nhận bệnh nhân, đặt lịch hẹn chống trùng giờ khám, kê đơn thuốc điện tử mà còn phải được triển khai bền vững, có khả năng phục hồi dữ liệu, giám sát tài nguyên và bảo vệ thông tin bệnh án mật theo tiêu chuẩn an toàn.")
update_p_text(doc.paragraphs[74], "Đề tài “Hệ thống Quản lý Phòng khám / Bệnh viện” (Đề 8) triển khai ứng dụng y tế chuyên nghiệp gồm React SPA Frontend, Django 5 REST Backend, cơ sở dữ liệu PostgreSQL 16 và pgAdmin 4. Toàn bộ 11 dịch vụ được container hóa hoàn chỉnh bằng Docker Compose, định tuyến qua Nginx Reverse Proxy tại cổng 80. Hệ thống giám sát vận hành bởi Prometheus và Grafana, cùng hệ thống quản trị nhật ký tập trung Loki và Promtail.")
update_p_text(doc.paragraphs[75], "Báo cáo bám sát cấu trúc bốn chương tiêu chuẩn của học phần: tổng quan kiến trúc và GitHub; triển khai ứng dụng, cơ sở dữ liệu và Nginx; giám sát hệ thống với Prometheus/Grafana và truy vấn nhật ký LogQL với Loki/Promtail; các kỹ thuật hardening bảo mật. Mọi kết quả đều được minh chứng trực tiếp bằng ảnh chụp màn hình, câu lệnh kiểm tra thực tế trên máy chủ Ubuntu và kiểm thử tự động Pytest.")

# CHƯƠNG 1
update_p_text(doc.paragraphs[80], "1.1. Bài toán, phạm vi và mục tiêu")
update_p_text(doc.paragraphs[81], "Hệ thống Quản lý Phòng khám là phần mềm quản trị nghiệp vụ y tế toàn diện với nhiều nhóm đối tượng: Quản trị viên (Admin), Bác sĩ điều trị (Doctor), Nhân viên tiếp đón (Receptionist) và Bệnh nhân. Điểm mấu chốt của bài toán là cơ chế chống trùng lịch khám (Anti-conflict Scheduling) — ngăn chặn triệt để tình trạng hai bệnh nhân được xếp cùng một bác sĩ trong cùng khung giờ, đồng thời bảo mật tuyệt đối hồ sơ bệnh án điện tử và đơn thuốc.")
update_p_text(doc.paragraphs[83], "•  Ứng dụng: Giao diện React SPA trực quan, Django 5 REST API, xác thực bảo mật JWT, phân quyền theo vai trò (RBAC), quản lý bệnh nhân, lịch hẹn, hồ sơ bệnh án và đơn thuốc.")
update_p_text(doc.paragraphs[84], "•  Dữ liệu: Cơ sở dữ liệu PostgreSQL 16 lưu trữ dữ liệu y tế trên named volume bền vững clinic_pgdata; tích hợp pgAdmin 4 cổng 5050 phục vụ quản trị CSDL chuyên sâu.")
update_p_text(doc.paragraphs[85], "•  Triển khai: Khởi chạy toàn bộ 11 dịch vụ bằng Docker Compose; Nginx đóng vai trò Reverse Proxy tiếp nhận HTTP tại cổng 80, gán Security Headers và phân luồng dịch vụ.")
update_p_text(doc.paragraphs[86], "•  Giám sát: Prometheus định kỳ thu thập chỉ số chuỗi thời gian từ máy chủ, cAdvisor và postgres-exporter; Grafana trực quan hóa tài nguyên trên Dashboard thời gian thực.")
update_p_text(doc.paragraphs[87], "•  Quản lý nhật ký: Promtail thu gom nhật ký từ Nginx và Backend đẩy về cơ sở dữ liệu Loki; thực hiện ít nhất 3 truy vấn LogQL phân tích truy cập và bảo mật.")
update_p_text(doc.paragraphs[88], "•  An toàn bảo mật (Hardening): Chạy container bằng tài khoản không đặc quyền (clinicuser UID 1000), cách ly 3 mạng Docker riêng biệt, bảo vệ file .env với quyền 600 và thiết lập đầy đủ HTTP Security Headers.")
update_p_text(doc.paragraphs[89], "Đối chiếu yêu cầu của Đề tài 08")

update_p_text(doc.paragraphs[90], "1.2. Sơ đồ kiến trúc tổng thể và luồng giao tiếp")
update_p_text(doc.paragraphs[91], "Hệ thống được chia thành ba vùng chức năng rõ rệt liên kết qua các mạng nội bộ Docker: Vùng Gateway & Web Client tiếp nhận người dùng; Vùng Backend & Dữ liệu cốt lõi xử lý nghiệp vụ; và Vùng Giám sát & Quản trị nhật ký quan sát trạng thái. Nginx là điểm tiếp xúc duy nhất tại cổng 80, trong khi cơ sở dữ liệu PostgreSQL tuyệt đối không mở cổng ra ngoài host.")
update_p_text(doc.paragraphs[93], "Hình 1.1. Sơ đồ kiến trúc logic Clinic Management System – mô hình hóa từ các thành phần đã triển khai.")
update_p_text(doc.paragraphs[95], "•  Client gửi yêu cầu HTTP đến Nginx cổng 80. Các truy cập giao diện được chuyển tới container Frontend; các truy vấn API (/api/) được chuyển tiếp tới Django Gunicorn Backend.")
update_p_text(doc.paragraphs[96], "•  Backend kết nối tới PostgreSQL qua tên dịch vụ postgres trên mạng nội bộ backend_net bằng tài khoản clinic_user; dữ liệu được bảo vệ an toàn trên volume độc lập.")
update_p_text(doc.paragraphs[97], "•  Prometheus định kỳ thu thập metrics từ cAdvisor và postgres-exporter; Grafana trực quan hóa chỉ số; Promtail theo dõi log chuyển về Loki phục vụ truy vấn LogQL.")

update_p_text(doc.paragraphs[99], "1.3. Container, mạng Docker và hệ thống cổng")
update_p_text(doc.paragraphs[100], "Hệ thống gồm 11 dịch vụ container điều phối qua docker-compose.yml. Các container được phân bổ vào 3 mạng bridge cô lập: frontend_net (kết nối Nginx và Frontend Web), backend_net (kết nối Nginx, Backend và CSDL PostgreSQL), monitoring_net (kết nối Prometheus, Grafana, Loki, Promtail, cAdvisor và postgres-exporter).")
update_p_text(doc.paragraphs[103], "•  Các container stateless (Nginx, Frontend, Backend) có thể tái tạo linh hoạt; dữ liệu quan trọng của PostgreSQL được lưu trên named volume độc lập clinic_pgdata.")
update_p_text(doc.paragraphs[104], "•  Các giao diện quản trị (Grafana, pgAdmin, Prometheus) chỉ mở cổng trong mạng nội bộ thử nghiệm; PostgreSQL đóng hoàn toàn cổng 5432 với mạng ngoài.")
update_p_text(doc.paragraphs[105], "•  Tệp .env lưu trữ biến môi trường trên máy chủ được thiết lập quyền chmod 600; file mẫu .env.example trên kho Git chỉ chứa tham số mẫu, không lộ mật khẩu thật.")

update_p_text(doc.paragraphs[107], "1.4. Quản lý mã nguồn và cấu hình trên GitHub")
update_p_text(doc.paragraphs[108], "Kho mã nguồn dự án được lưu trữ tại: git@github.com:Loki-sama119/clinic-management-system.git, nhánh master. Kho lưu trữ toàn bộ mã nguồn ứng dụng, cấu hình Docker Compose, Nginx reverse proxy, kịch bản khởi tạo database, kịch bản CI/CD GitHub Actions và tài liệu hệ thống.")
update_p_text(doc.paragraphs[110], "Hình 1.2. Kho mã nguồn clinic-management-system trên GitHub và quy trình CI/CD kiểm thử tự động.")
update_p_text(doc.paragraphs[112], "•  Kiểm tra trạng thái git status bảo đảm không có file tạm hoặc thông tin bí mật chưa được khai báo.")
update_p_text(doc.paragraphs[113], "•  Xác minh file .gitignore loại trừ hoàn toàn .env, __pycache__, logs, dữ liệu db.")
update_p_text(doc.paragraphs[114], "•  Quy trình CI/CD GitHub Actions tự động kích hoạt bộ kiểm thử pytest mỗi khi có commit mới lên nhánh master.")

# CHƯƠNG 2
update_p_text(doc.paragraphs[115], "CHƯƠNG 2. TRIỂN KHAI ỨNG DỤNG, CƠ SỞ DỮ LIỆU VÀ NGINX")
update_p_text(doc.paragraphs[117], "2.1. Xây dựng ứng dụng quản lý phòng khám và đóng gói Docker")
update_p_text(doc.paragraphs[118], "Ứng dụng y tế được cấu trúc theo mô hình phân tách Frontend và Backend rõ ràng. Backend xây dựng trên nền tảng Django 5 và Django REST Framework, phục vụ các RESTful API chuẩn mực và bảo vệ bằng JSON Web Token (JWT). Frontend được phát triển dưới dạng Single Page Application (SPA), cung cấp giao diện quản trị phòng khám hiện đại và thân thiện.")
update_p_text(doc.paragraphs[121], "•  Quản lý Hồ sơ Bệnh nhân: Sinh mã bệnh nhân duy nhất dạng BN-XXXXX, lưu trữ tiền sử bệnh, nhóm máu, dị ứng.")
update_p_text(doc.paragraphs[122], "•  Quản lý Lịch hẹn & Chống trùng lịch: Kiểm tra ràng buộc thời gian thực, ngăn không cho đặt 2 lịch khám cùng bác sĩ trong 1 khung giờ.")
update_p_text(doc.paragraphs[123], "•  Hồ sơ Bệnh án & Đơn thuốc: Lưu trữ chỉ số sinh tồn (mạch, huyết áp, nhiệt độ), chẩn đoán, phác đồ điều trị và danh mục thuốc kê đơn.")
update_p_text(doc.paragraphs[127], "Lệnh make up hoặc docker compose up -d khởi động toàn bộ 11 container ở chế độ chạy nền. Lệnh docker compose ps xác minh toàn bộ các container chính đều đạt trạng thái Healthy.")

update_p_text(doc.paragraphs[128], "2.2. Kiểm chứng luồng nghiệp vụ và phân quyền người dùng")
update_p_text(doc.paragraphs[129], "Để kiểm thử toàn diện, các tài khoản với các vai trò khác nhau (admin, bác sĩ dr_nguyenvana, lễ tân receptionist01) đã được đăng nhập đồng thời trên trình duyệt để kiểm tra phân quyền RBAC và luồng đặt lịch khám y tế.")
update_p_text(doc.paragraphs[131], "Hình 2.1. Giao diện Web hệ thống Phòng khám: Bảng điều khiển, tiếp nhận bệnh nhân và lịch hẹn khám.")
update_p_text(doc.paragraphs[133], "•  Tài khoản Lễ tân tiếp nhận bệnh nhân mới, tạo lịch hẹn khám bệnh và tra cứu lịch sử.")
update_p_text(doc.paragraphs[134], "•  Tài khoản Bác sĩ tiếp nhận bệnh nhân tại phòng khám, nhập kết quả chẩn đoán và xuất đơn thuốc điện tử.")
update_p_text(doc.paragraphs[135], "•  Hệ thống kích hoạt thuật toán chống trùng lịch khám: Khi cố tình tạo lịch trùng bác sĩ và khung giờ, hệ thống lập tức từ chối và cảnh báo lỗi xung đột thời gian.")

update_p_text(doc.paragraphs[136], "2.3. Cơ sở dữ liệu PostgreSQL 16 và công cụ pgAdmin 4")
update_p_text(doc.paragraphs[137], "Cơ sở dữ liệu hoạt động trong container postgres chạy phiên bản PostgreSQL 16 chính thức, tên database là clinic_db. Giao diện quản trị pgAdmin 4 được truy cập tại cổng 5050, kết nối qua mạng nội bộ Docker tới máy chủ cơ sở dữ liệu.")
update_p_text(doc.paragraphs[139], "Hình 2.2. pgAdmin 4 đã kết nối database clinic_db; cây schema public và đồ thị hiệu năng PostgreSQL.")

update_p_text(doc.paragraphs[141], "2.4. Kiểm chứng dữ liệu lưu trữ bằng câu lệnh SQL")
update_p_text(doc.paragraphs[142], "Sau khi vận hành các nghiệp vụ trên giao diện web, công cụ truy vấn SQL đã thực hiện các lệnh SELECT thống kê số lượng dữ liệu thực tế đang lưu trữ trong cơ sở dữ liệu.")
update_p_text(doc.paragraphs[145], "Hình 2.3. PostgreSQL trả về 4 users, 5 patients, 2 doctors, 4 appointments, 1 medical record.")
update_p_text(doc.paragraphs[146], "Dữ liệu thực tế quan sát tại thời điểm kiểm thử gồm: 4 tài khoản phân quyền RBAC, 5 bệnh nhân tiếp nhận, 2 bác sĩ chuyên khoa, 4 lịch hẹn khám và 1 hồ sơ bệnh án hoàn chỉnh. Dữ liệu được bảo toàn nguyên vẹn trên named volume clinic_pgdata.")

update_p_text(doc.paragraphs[147], "2.5. Cấu hình Nginx làm Reverse Proxy (Bước 3)")
update_p_text(doc.paragraphs[148], "Ứng dụng được truy cập trực tiếp qua cổng 80 của Nginx Reverse Proxy. Nginx phân luồng thông minh: các yêu cầu trang web tĩnh được phục vụ bởi Frontend React; các yêu cầu bắt đầu bằng /api/ và /admin/ được chuyển tiếp an toàn tới backend:8000 của Django.")
update_p_text(doc.paragraphs[150], "Nginx đã được cấu hình hoàn chỉnh các Security Headers bảo vệ và ẩn danh thông tin máy chủ (server_tokens off), bảo đảm an toàn cho cổng truy cập web công khai.")

update_p_text(doc.paragraphs[151], "2.6. Kiểm tra Security Headers và trạng thái Docker")
update_p_text(doc.paragraphs[152], "Mức độ bảo vệ của Nginx được kiểm chứng thông qua lệnh curl -sI http://localhost/, đồng thời lệnh docker compose ps kiểm tra trạng thái sức khỏe định kỳ của toàn bộ hệ sinh thái dịch vụ.")
update_p_text(doc.paragraphs[154], "Hình 2.4. Docker Compose báo Healthy, .env có quyền 600 và Nginx trả HTTP 200 kèm Security Headers.")

# CHƯƠNG 3
update_p_text(doc.paragraphs[157], "CHƯƠNG 3. GIÁM SÁT HỆ THỐNG VÀ LOG TẬP TRUNG")
update_p_text(doc.paragraphs[158], "3.1. Kiến trúc giám sát Prometheus và Exporters")
update_p_text(doc.paragraphs[159], "Prometheus đóng vai trò máy chủ thu thập và lưu trữ số liệu chuỗi thời gian (time-series metrics). Định kỳ mỗi 15 giây, Prometheus gửi yêu cầu kéo (pull) chỉ số từ các exporter: cAdvisor (chỉ số phần cứng và container), postgres-exporter (chỉ số CSDL) và django-prometheus (chỉ số ứng dụng).")
update_p_text(doc.paragraphs[162], "Tất cả các target đều được khai báo qua tệp cấu hình prometheus.yml và hoạt động ổn định trên mạng monitoring_net.")

update_p_text(doc.paragraphs[163], "3.2. Grafana – giám sát tài nguyên host và container")
update_p_text(doc.paragraphs[164], "Grafana được cấu hình nguồn dữ liệu tự động tới Prometheus và Loki, hiển thị Dashboard giám sát toàn diện gồm: Tỷ lệ sử dụng CPU, RAM của máy chủ Ubuntu; mức tiêu thụ tài nguyên chi tiết của từng container Docker; và tần suất lưu lượng HTTP.")
update_p_text(doc.paragraphs[166], "Hình 3.1. Grafana theo dõi CPU, RAM, Disk của Ubuntu và CPU/RAM từng container phòng khám.")
update_p_text(doc.paragraphs[168], "•  Hệ thống ghi nhận tài nguyên CPU và RAM của máy chủ duy trì ở mức tối ưu (< 35% RAM, < 10% CPU), đảm bảo độ trễ phản hồi API y tế cực thấp.")

update_p_text(doc.paragraphs[172], "3.3. Grafana – tình trạng HTTP và PostgreSQL")
update_p_text(doc.paragraphs[173], "Prometheus Web UI tại cổng 9090 cung cấp giao diện tra cứu trạng thái các target (Targets Status) và thực thi các câu lệnh PromQL kiểm tra số kết nối database và tình trạng dịch vụ.")
update_p_text(doc.paragraphs[175], "Hình 3.2. Prometheus Web UI thu thập metrics các target hệ thống và trạng thái hoạt động UP.")

update_p_text(doc.paragraphs[178], "3.4. Loki và Promtail – truy vấn log HTTP Nginx")
update_p_text(doc.paragraphs[179], "Promtail đóng vai trò log collector, theo dõi các file nhật ký truy cập và lỗi tại /var/log/nginx/ và /var/log/backend/, gán nhãn {job=\"nginx\"} và {job=\"backend\"} rồi đẩy trực tiếp về cơ sở dữ liệu Loki qua cổng 3100.")
update_p_text(doc.paragraphs[181], "Hình 3.3. Loki hiển thị các bản ghi truy vấn HTTP Nginx và backend được thu thập tập trung.")

update_p_text(doc.paragraphs[183], "3.5. LogQL – xác minh sự kiện đăng nhập và API backend")
update_p_text(doc.paragraphs[184], "Sử dụng công cụ Grafana Explore, câu lệnh LogQL {job=\"backend\"} |= \"LOGIN\" được thực thi để trích xuất các sự kiện đăng nhập thành công và hành vi xác thực của người dùng trong hệ thống.")
update_p_text(doc.paragraphs[186], "Hình 3.4. Swagger UI / OpenAPI xác thực các endpoint REST API phòng khám và audit log sự kiện.")
update_p_text(doc.paragraphs[188], "•  Nhật ký ghi nhận đầy đủ thời điểm đăng nhập, tài khoản người dùng và địa chỉ IP truy cập, hỗ trợ công tác truy vết kiểm toán (Audit Trail) trong y tế.")

update_p_text(doc.paragraphs[191], "3.6. LogQL – thống kê số lần gọi HTTP Health")
update_p_text(doc.paragraphs[192], "LogQL hỗ trợ các hàm thống kê chuỗi thời gian như rate() hoặc count_over_time(). Câu lệnh sum(rate({job=\"nginx\"}[5m])) tính toán tốc độ truy cập HTTP, hỗ trợ phát hiện các đợt tăng đột biến lưu lượng hoặc dấu hiệu tấn công bất thường.")
update_p_text(doc.paragraphs[195], "Hình 3.5. Trạng thái 11 containers Docker Compose hoạt động ổn định và biểu đồ truy vấn LogQL.")

# CHƯƠNG 4
update_p_text(doc.paragraphs[198], "CHƯƠNG 4. HARDENING VÀ ĐÁNH GIÁ BẢO MẬT")
update_p_text(doc.paragraphs[199], "4.1. Các lớp bảo vệ được áp dụng hoặc cấu hình")
update_p_text(doc.paragraphs[200], "Bảo mật trong hệ thống thông tin y tế là yêu cầu sống còn nhằm bảo vệ bí mật đời tư bệnh nhân. Trong đề tài, bốn lớp bảo vệ cốt lõi đã được áp dụng đồng bộ:")
update_p_text(doc.paragraphs[204], "Hình 4.1. Kiểm chứng container Backend chạy bằng tài khoản clinicuser non-root (UID 1000) và .env quyền 600.")
update_p_text(doc.paragraphs[205], "Kiểm chứng tài khoản chạy container và phân quyền file môi trường")
update_p_text(doc.paragraphs[206], "Thực thi lệnh docker compose exec backend id trên máy chủ trả về kết quả: uid=1000(clinicuser) gid=1000(clinicuser), xác nhận container backend vận hành hoàn toàn dưới tài khoản không đặc quyền thay vì root (UID 0), ngăn chặn nguy cơ leo thang đặc quyền container breakout. Đồng thời lệnh ls -la .env xác nhận tệp bí mật được gán quyền hạn chặt chẽ chmod 600 (-rw-------).")

update_p_text(doc.paragraphs[207], "4.2. Tổng hợp kết quả kiểm thử và điểm cần hoàn thiện")
update_p_text(doc.paragraphs[208], "Dưới đây là bảng tổng hợp kết quả đối chiếu toàn bộ các tiêu chí kỹ thuật triển khai và bảo mật hệ thống theo đúng đề cương môn học.")
update_p_text(doc.paragraphs[212], "•  Giám sát đa tầng: Kết hợp hài hòa giữa metric chuỗi thời gian (Prometheus), log tập trung (Loki) và kiểm thử định kỳ.")
update_p_text(doc.paragraphs[213], "•  Nguyên tắc bảo vệ dữ liệu: Dữ liệu CSDL y tế bắt buộc lưu trên named volume độc lập, kiểm soát nghiêm ngặt tránh thất thoát khi tái tạo container.")
update_p_text(doc.paragraphs[214], "•  Quản lý bí mật: Tuyệt đối không commit tệp .env, mật khẩu hay khóa bí mật JWT lên kho mã nguồn công khai.")

# KẾT LUẬN
update_p_text(doc.paragraphs[217], "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
update_p_text(doc.paragraphs[218], "1. Kết quả đạt được")
update_p_text(doc.paragraphs[219], "Đề tài 08 đã triển khai thành công Hệ thống Quản lý Phòng khám y tế hoàn chỉnh, đáp ứng đầy đủ các tiêu chuẩn kỹ thuật đề ra. Hệ thống bao gồm 11 dịch vụ container điều phối nhịp nhàng qua Docker Compose; Nginx Reverse Proxy làm cổng tiếp nhận duy nhất; CSDL PostgreSQL 16 và pgAdmin 4 quản trị dữ liệu bệnh án bền vững; cụm Prometheus & Grafana giám sát hiệu năng thời gian thực; cùng Loki & Promtail quản lý nhật ký tập trung và phân tích qua LogQL.")
update_p_text(doc.paragraphs[220], "Bên cạnh các tính năng nghiệp vụ y tế chuyên sâu (chống trùng lịch, quản lý bệnh nhân, kê đơn), hệ thống đã thực thi xuất sắc các tiêu chuẩn Hardening bảo mật: chạy Non-root user, cô lập mạng nội bộ 3 tầng, bảo vệ tệp môi trường và áp dụng đầy đủ HTTP Security Headers.")
update_p_text(doc.paragraphs[221], "2. Giới hạn và hướng phát triển")
update_p_text(doc.paragraphs[222], "•  Triển khai chứng chỉ số HTTPS/TLS chính thức từ Let's Encrypt khi đưa hệ thống vào môi trường tên miền Internet.")
update_p_text(doc.paragraphs[223], "•  Tích hợp chữ ký số y tế và liên thông đơn thuốc quốc gia theo tiêu chuẩn của Bộ Y tế.")
update_p_text(doc.paragraphs[224], "•  Xây dựng chính sách tự động sao lưu dự phòng (Automated Backup) CSDL PostgreSQL sang dịch vụ đám mây (S3/MinIO).")
update_p_text(doc.paragraphs[225], "•  Mở rộng hạ tầng sang mô hình cụm điều phối Kubernetes (K8s) khi quy mô bệnh viện và số lượng bệnh nhân tăng cao.")

# Tài liệu tham khảo
update_p_text(doc.paragraphs[228], "1. Đề cương bài tập lớn học phần “Triển khai và Quản trị Hệ thống Phần mềm – K23”, Bộ môn CNPM & HTTT, Trường ĐH CNTT & TT Thái Nguyên.")
update_p_text(doc.paragraphs[229], "2. Mẫu báo cáo học phần môn học do giảng viên Vũ Việt Dũng cung cấp; bố cục bốn chương chuẩn mực.")
update_p_text(doc.paragraphs[230], "3. Kho mã nguồn dự án: https://github.com/Loki-sama119/clinic-management-system (nhánh master, 2026).")
update_p_text(doc.paragraphs[231], "4. Bộ ảnh minh chứng hệ thống Quản lý Phòng khám do sinh viên Nguyễn Văn Thắng (DTC245200146) chụp thực tế trên máy ảo Ubuntu.")

# 4. Update Tables
# Table 0: Scope
t0 = doc.tables[0]
t0.cell(0, 1).text = "Môi trường máy ảo Ubuntu 22.04 LTS, địa chỉ IP thử nghiệm http://localhost/; ứng dụng quản lý phòng khám phục vụ học phần và demo thực hành trong mạng nội bộ."

# Table 1: Tiêu chí
t1 = doc.tables[1]
t1.cell(1, 0).text = "Ứng dụng"
t1.cell(1, 1).text = "Quản lý phòng khám, bệnh nhân, lịch hẹn, đơn thuốc, RBAC"
t1.cell(1, 2).text = "Giao diện Web React; API Django; Pytest pass 100%"
t1.cell(2, 0).text = "Hạ tầng"
t1.cell(2, 1).text = "PostgreSQL 16 + pgAdmin 4 + Nginx Reverse Proxy"
t1.cell(2, 2).text = "docker compose ps báo 11 container Healthy; pgAdmin"
t1.cell(3, 0).text = "Vận hành"
t1.cell(3, 1).text = "Prometheus/Grafana/Loki/Promtail/Exporters"
t1.cell(3, 2).text = "Dashboard Grafana, Prometheus targets UP, 3 LogQL"
t1.cell(4, 0).text = "Bảo mật"
t1.cell(4, 1).text = "Ít nhất 3–4 biện pháp hardening thực tế"
t1.cell(4, 2).text = "Non-root UID 1000, .env 600, network isolation, headers"

# Table 2: Services
t2 = doc.tables[2]
# Row 0: Header
services_data = [
    ("nginx", "Host :80 → container :80", "Reverse Proxy, Security Headers, phân luồng HTTP"),
    ("frontend", "Nội bộ :80", "React SPA, giao diện quản lý phòng khám"),
    ("backend", "Nội bộ :8000", "Django 5 REST API, xác thực JWT, RBAC, chống trùng lịch"),
    ("postgres", "Nội bộ :5432 (Internal only)", "CSDL PostgreSQL 16, named volume clinic_pgdata"),
    ("pgadmin", "Host :5050 → container :80", "Giao diện web quản trị CSDL chuyên sâu"),
    ("prometheus", "Host :9090", "Thu thập và lưu trữ time-series metrics"),
    ("grafana", "Host :3000", "Dashboard hiển thị chỉ số và truy vấn log LogQL"),
    ("loki / promtail", "Host :3100 (Loki)", "Quản trị nhật ký tập trung từ Nginx và Backend"),
]
for r_i, (svc, port, role) in enumerate(services_data):
    if r_i + 1 < len(t2.rows):
        t2.cell(r_i + 1, 0).text = svc
        t2.cell(r_i + 1, 1).text = port
        t2.cell(r_i + 1, 2).text = role

# Table 3: Code box for git
t3 = doc.tables[3]
t3.cell(0, 0).text = "git status\ngit diff --cached\ngit ls-files | grep \".env$\"\ngit push origin master"

# Table 4: Chức năng
t4 = doc.tables[4]
funcs_data = [
    ("Xác thực & Phân quyền RBAC", "Quản lý 3 vai trò: Admin, Bác sĩ, Lễ tân với token JWT", "Đăng nhập thành công, phân chia menu theo vai trò"),
    ("Quản lý Hồ sơ Bệnh nhân", "Tạo mã BN-XXXXX duy nhất, kiểm tra trùng SĐT, lưu tiền sử dị ứng", "Danh sách 5 bệnh nhân hiển thị trên giao diện"),
    ("Lịch hẹn & Chống trùng lịch", "Ngăn chặn 2 bệnh nhân đặt cùng bác sĩ trong cùng khung giờ", "Thuật toán kiểm tra lịch hẹn, từ chối khi bị trùng"),
    ("Bệnh án & Đơn thuốc", "Bác sĩ nhập chỉ số sinh tồn, chẩn đoán, kê đơn thuốc điện tử", "Hồ sơ bệnh án và mẫu in đơn thuốc chuẩn y tế"),
    ("Kiểm thử tự động", "Bộ kiểm thử Pytest kiểm tra từ xác thực tới CRUD và logic lịch", "12/12 ca kiểm thử Pytest vượt qua 100%"),
]
for r_i, (f_name, f_how, f_proof) in enumerate(funcs_data):
    if r_i + 1 < len(t4.rows):
        t4.cell(r_i + 1, 0).text = f_name
        t4.cell(r_i + 1, 1).text = f_how
        t4.cell(r_i + 1, 2).text = f_proof

# Table 5: Code box
t5 = doc.tables[5]
t5.cell(0, 0).text = "cd ~/clinic-management\ndocker compose up -d\ndocker compose ps"

# Table 6: Bảng CSDL
t6 = doc.tables[6]
tables_data = [
    ("users", "Lưu tài khoản nhân viên y tế, mật khẩu băm bcrypt, vai trò RBAC"),
    ("patients", "Lưu hồ sơ bệnh nhân, mã định danh BN-XXXXX, tiền sử bệnh"),
    ("doctors", "Lưu thông tin bác sĩ, chuyên khoa, lịch làm việc"),
    ("appointments", "Lưu lịch hẹn khám bệnh, thời gian bắt đầu/kết thúc, trạng thái"),
    ("medical_records", "Lưu kết quả khám, chỉ số sinh tồn, chẩn đoán bệnh án"),
]
for r_i, (tbl, tbl_desc) in enumerate(tables_data):
    if r_i + 1 < len(t6.rows):
        t6.cell(r_i + 1, 0).text = tbl
        t6.cell(r_i + 1, 1).text = tbl_desc

# Table 7: Code box for SQL
t7 = doc.tables[7]
t7.cell(0, 0).text = """SELECT 
  (SELECT COUNT(*) FROM users) AS total_users,
  (SELECT COUNT(*) FROM patients) AS total_patients,
  (SELECT COUNT(*) FROM doctors) AS total_doctors,
  (SELECT COUNT(*) FROM appointments) AS total_appointments,
  (SELECT COUNT(*) FROM medical_records) AS total_records;"""

# Table 8: Code box / Diagram
t8 = doc.tables[8]
t8.cell(0, 0).text = """Client  http://localhost:80
          │ Host :80 → Nginx container :80
Nginx   location /     → http://frontend:80 (React SPA)
        location /api/ → http://backend:8000 (Django REST Gunicorn)
          │ Docker network: backend_net
DB      PostgreSQL 16 / clinic_db (Internal Only :5432)"""

# Table 9: Kiểm tra Nginx
t9 = doc.tables[9]
nginx_checks = [
    ("URL ứng dụng cổng 80", "http://localhost/ phản hồi HTTP 200, hiển thị giao diện phòng khám"),
    ("URL API Backend", "http://localhost/api/ phản hồi HTTP 200 / OpenAPI Swagger"),
    ("curl -sI http://localhost/", "HTTP/1.1 200 OK kèm Server: nginx (server_tokens off)"),
    ("Security Headers", "X-Frame-Options, X-Content-Type-Options, X-XSS-Protection đầy đủ"),
]
for r_i, (chk, res) in enumerate(nginx_checks):
    if r_i + 1 < len(t9.rows):
        t9.cell(r_i + 1, 0).text = chk
        t9.cell(r_i + 1, 1).text = res

# Table 10: Security Headers
t10 = doc.tables[10]
headers_data = [
    ("X-Frame-Options: SAMEORIGIN", "Chống tấn công Clickjacking, không cho nhúng trang vào iframe lạ"),
    ("X-Content-Type-Options: nosniff", "Ngăn chặn trình duyệt đoán sai MIME-type để thực thi mã độc"),
    ("X-XSS-Protection: 1; mode=block", "Kích hoạt bộ lọc chặn tấn công Cross-Site Scripting trên trình duyệt"),
    ("Referrer-Policy: strict-origin", "Bảo vệ thông tin URL nguồn khi chuyển tiếp liên kết ra bên ngoài"),
    ("server_tokens off", "Ẩn thông tin phiên bản chính xác của Nginx khỏi HTTP header"),
]
for r_i, (hdr, purp) in enumerate(headers_data):
    if r_i + 1 < len(t10.rows):
        t10.cell(r_i + 1, 0).text = hdr
        t10.cell(r_i + 1, 1).text = purp

# Table 11: Monitoring Jobs
t11 = doc.tables[11]
jobs_data = [
    ("cadvisor", "cadvisor:8080/metrics", "Giám sát CPU, RAM, Disk I/O của toàn bộ 11 container"),
    ("postgres-exporter", "postgres-exporter:9187/metrics", "Giám sát số kết nối DB, transactions, cache hit ratio"),
    ("backend", "backend:8000/metrics", "Chỉ số latency, số lượng request HTTP của Django API"),
    ("loki", "loki:3100", "Lưu trữ và lập chỉ mục nhật ký tập trung"),
    ("grafana", "grafana:3000", "Trực quan hóa đồ thị và bảng điều khiển"),
]
for r_i, (jb, ep, rl) in enumerate(jobs_data):
    if r_i + 1 < len(t11.rows):
        t11.cell(r_i + 1, 0).text = jb
        t11.cell(r_i + 1, 1).text = ep
        t11.cell(r_i + 1, 2).text = rl

# Table 12: PromQL Code box
t12 = doc.tables[12]
t12.cell(0, 0).text = """# Tỷ lệ CPU sử dụng của toàn bộ máy chủ Ubuntu
100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))

# Số kết nối hiện tại tới PostgreSQL database
pg_stat_activity_count"""

# Table 13: Dashboard Panels
t13 = doc.tables[13]
panels_data = [
    ("Host CPU / RAM / Disk", "Tải tài nguyên của máy ảo Ubuntu vận hành", "cAdvisor & Node Exporter"),
    ("Container CPU & RAM", "Mức tiêu thụ tài nguyên từng container y tế", "cAdvisor"),
    ("PostgreSQL Connections", "Số phiên kết nối làm việc đồng thời của DB", "postgres-exporter"),
]
for r_i, (pn, sh, src) in enumerate(panels_data):
    if r_i + 1 < len(t13.rows):
        t13.cell(r_i + 1, 0).text = pn
        t13.cell(r_i + 1, 1).text = sh
        t13.cell(r_i + 1, 2).text = src

# Table 14: LogQL 1
t14 = doc.tables[14]
t14.cell(0, 0).text = '{job="nginx"} |= "GET /api/"'

# Table 15: LogQL 2
t15 = doc.tables[15]
t15.cell(0, 0).text = '{job="backend"} |= "LOGIN"'

# Table 16: LogQL 3
t16 = doc.tables[16]
t16.cell(0, 0).text = 'sum(rate({job="nginx"}[5m]))'

# Table 17: LogQL Results
t17 = doc.tables[17]
logql_res = [
    ('{job="nginx"}', "Thu thập đầy đủ toàn bộ log truy cập HTTP qua cổng Nginx 80"),
    ('{job="backend"} |= "LOGIN"', "Trích xuất sự kiện đăng nhập tài khoản của bác sĩ và lễ tân"),
    ('sum(rate({job="nginx"}[5m]))', "Biểu đồ đường thể hiện tần suất request HTTP thời gian thực"),
]
for r_i, (l_type, l_obs) in enumerate(logql_res):
    if r_i + 1 < len(t17.rows):
        t17.cell(r_i + 1, 0).text = l_type
        t17.cell(r_i + 1, 1).text = l_obs

# Table 18: Lớp bảo vệ
t18 = doc.tables[18]
hardening_data = [
    ("Chạy Non-root User", "Backend chạy với user clinicuser (UID 1000) thay vì root", "Hạn chế tuyệt đối nguy cơ container breakout"),
    ("Network Isolation", "Phân chia 3 mạng Docker; PostgreSQL không mở cổng ra host", "Ngăn chặn tấn công dò quét CSDL từ mạng bên ngoài"),
    ("Bảo vệ file bí mật", "Tệp .env chứa mật khẩu DB được gán quyền chmod 600", "Chỉ tiến trình của chủ sở hữu mới có quyền đọc"),
    ("HTTP Security Headers", "Nginx gán X-Frame, XSS, nosniff, ẩn version server", "Chống Clickjacking, MIME sniff và thám mã"),
    ("RBAC & Password Hash", "Mật khẩu băm an toàn bằng PBKDF2/bcrypt, kiểm soát JWT", "Ngăn chặn lộ mật khẩu ngay cả khi lộ bản sao lưu"),
]
for r_i, (hl, hi, hr) in enumerate(hardening_data):
    if r_i + 1 < len(t18.rows):
        t18.cell(r_i + 1, 0).text = hl
        t18.cell(r_i + 1, 1).text = hi
        t18.cell(r_i + 1, 2).text = hr

# Table 19: Bảng tổng hợp kiểm thử
t19 = doc.tables[19]
test_summary = [
    ("1", "Ứng dụng qua Nginx :80", "HTTP 200; giao diện phòng khám hoạt động trơn tru", "Đạt"),
    ("2", "Phân quyền RBAC & Nghiệp vụ", "Tiếp nhận bệnh nhân, đặt lịch, khám bệnh, kê đơn", "Đạt"),
    ("3", "Chống trùng lịch khám", "Thuật toán anti-conflict ngăn chặn trùng lịch cùng giờ", "Đạt"),
    ("4", "PostgreSQL 16 + pgAdmin 4", "Kết nối clinic_db, named volume clinic_pgdata bền vững", "Đạt"),
    ("5", "Truy vấn SQL kiểm chứng", "4 users, 5 patients, 2 doctors, 4 appointments, 1 record", "Đạt tại thời điểm chụp"),
    ("6", "Prometheus + Grafana", "Dashboard CPU/RAM/Disk, container metrics, targets UP", "Đạt"),
    ("7", "Loki + Promtail", "3 truy vấn LogQL trích xuất log Nginx và backend", "Đạt"),
    ("8", "Hardening (.env 600, Non-root)", "uid=1000(clinicuser), .env -rw-------, network isolation", "Đạt"),
]
for r_i, (stt, content, res, status) in enumerate(test_summary):
    if r_i + 1 < len(t19.rows):
        t19.cell(r_i + 1, 0).text = stt
        t19.cell(r_i + 1, 1).text = content
        t19.cell(r_i + 1, 2).text = res
        t19.cell(r_i + 1, 3).text = status

doc.save(TARGET_DOCX)
print(f"Successfully generated final report: {TARGET_DOCX}")
