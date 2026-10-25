# KỊCH BẢN TRÌNH DIỄN BẢO VỆ ĐỒ ÁN (DEMO SCRIPT)
## THỜI LƯỢNG TRÌNH DIỄN: 7 — 10 PHÚT

- **Sinh viên**: Nguyễn Văn Thắng (MSV: DTC245200146)
- **Đề tài**: Đề 8 — Hệ thống Quản lý Phòng khám / Bệnh viện

---

### BƯỚC 1: KHỞI ĐỘNG HỆ THỐNG DOCKER COMPOSE
- **Thao tác**: Mở Terminal, gõ lệnh:
  ```bash
  docker compose up -d
  docker compose ps
  ```
- **Mục tiêu**: Chứng minh toàn bộ 11 container đang ở trạng thái `running` hoặc `healthy`.

---

### BƯỚC 2: ĐĂNG NHẬP VỚI TÀI KHOẢN LỄ TÂN
- **Thao tác**: Mở trình duyệt truy cập `http://localhost/`. Bấm nút chọn nhanh tài khoản `👩‍💼 Lễ tân` (Username: `receptionist`, Password: `Rec@123`).
- **Mục tiêu**: Chứng minh cơ chế xác thực JWT, bảo vệ trang đăng nhập và giao diện responsive tiếng Việt.

---

### BƯỚC 3: TẠO HỒ SƠ BỆNH NHÂN MỚI
- **Thao tác**: Vào menu **Hồ sơ bệnh nhân** -> Bấm **➕ Thêm Bệnh nhân mới**. Nhập:
  - Tên: `Nguyễn Hoàng Long`
  - Ngày sinh: `2000-01-15`
  - Số điện thoại: `0987654321`
  - Địa chỉ: `Hà Nội`
- **Mục tiêu**: Hệ thống tự sinh mã `BN-XXXXX`, kiểm tra số điện thoại duy nhất và lưu vào PostgreSQL.

---

### BƯỚC 4: ĐẶT LỊCH HẸN KHÁM BỆNH
- **Thao tác**: Vào menu **Lịch hẹn khám** -> Bấm **➕ Đặt lịch khám mới**.
  - Chọn bệnh nhân vừa tạo: `Nguyễn Hoàng Long`.
  - Chọn chuyên khoa: `Khoa Nội Tổng Quát`.
  - Chọn bác sĩ: `BS.CKII Nguyễn Văn Thắng (BS-1001)`.
  - Chọn ngày: Hôm nay. Khung giờ: `09:00 - 09:30`.
- **Mục tiêu**: Tạo lịch hẹn thành công với trạng thái `PENDING`.

---

### BƯỚC 5: MINH CHỨNG NGĂN CHẶN ĐẶT TRÙNG LỊCH (ANTI-CONFLICT)
- **Thao tác**: Tiếp tục bấm **➕ Đặt lịch khám mới**:
  - Chọn bệnh nhân khác.
  - Chọn cùng bác sĩ: `BS.CKII Nguyễn Văn Thắng (BS-1001)`.
  - Chọn cùng ngày và cùng khung giờ: `09:00 - 09:30`.
  - Bấm **Xác nhận đặt lịch**.
- **Kết quả mong đợi**: Hệ thống hiển thị hộp cảnh báo màu đỏ: *"Bác sĩ BS-1001 đã có lịch khám khác trong khung giờ 09:00 - 09:30... Vui lòng chọn khung giờ khác!"*.
- **Mục tiêu**: Chứng minh thuật toán kiểm tra xung đột thời gian (Interval Overlap Prevention) hoạt động 100%.

---

### BƯỚC 6: CHUYỂN ĐỔI TRẠNG THÁI & CHỨNG MINH PHÂN QUYỀN
- **Thao tác**:
  1. Lễ tân bấm nút **Duyệt** -> Lịch chuyển sang `CONFIRMED`.
  2. Bệnh nhân có mặt tại phòng khám -> Lễ tân bấm **Tiếp nhận** -> Lịch chuyển sang `IN_PROGRESS`.
  3. Đăng xuất và đăng nhập bằng tài khoản Bác sĩ `doctor_thang` (Pass: `Doc@123`).
  4. Bác sĩ thấy bệnh nhân đang chờ -> Bấm **🩺 Vào khám**.
- **Mục tiêu**: Chứng minh luồng y tế thực tế và phân quyền RBAC (Lễ tân không được khám/sửa bệnh án).

---

### BƯỚC 7: BÁC SĨ KHÁM BỆNH, KÊ ĐƠN & IN PHIẾU KHÁM
- **Thao tác**:
  1. Nhập chỉ số sinh tồn (Huyết áp: `125/80`, Mạch: `80`, Nhiệt độ: `37.0°C`).
  2. Chẩn đoán: `Viêm dạ dày cấp tính`. Phác đồ: `Dùng thuốc giảm tiết acid, kiêng đồ chua cay`.
  3. Đơn thuốc: `1. Nexium 40mg x 14 viên (Uống 1v trước ăn sáng)`.
  4. Bấm **Hoàn thành khám & Lưu bệnh án**.
  5. Bấm nút **🖨️ In phiếu khám**: Hiển thị phiếu khám bệnh chuẩn Bộ Y tế.
- **Mục tiêu**: Dữ liệu lưu vĩnh viễn vào PostgreSQL, trạng thái lịch chuyển sang `COMPLETED`.

---

### BƯỚC 8: MỞ PGADMIN 4 XÁC MINH DỮ LIỆU THỰC TẾ
- **Thao tác**: Truy cập `http://localhost:5050/`. Đăng nhập tài khoản `admin@phucanclinic.vn` / `Admin@Clinic2026`.
- **Mục tiêu**: Mở bảng `patients`, `appointments`, `medical_records` để giảng viên thấy dữ liệu vừa tạo đã nằm trong database PostgreSQL 16.

---

### BƯỚC 9: MỞ GRAFANA DASHBOARD XEM CHỈ SỐ GIÁM SÁT
- **Thao tác**: Truy cập `http://localhost:3000/`. Mở Dashboard **Clinic Management — System Observability Dashboard**.
- **Mục tiêu**:
  - Xem biểu đồ Container CPU/RAM từ cAdvisor.
  - Xem số lượng kết nối `PostgreSQL Active Connections` và `Commits/sec` từ postgres_exporter.

---

### BƯỚC 10: TRUY VẤN NHẬT KÝ BẰNG LOGQL TRÊN GRAFANA LOKI
- **Thao tác**: Vào menu **Explore** -> Chọn datasource **Loki** -> Nhập câu query:
  ```logql
  {job="nginx"}
  ```
  Bấm **Run query**. Thấy toàn bộ log các request vừa bấm trên giao diện xuất hiện theo thời gian thực.
- **Mục tiêu**: Đáp ứng trọn vẹn tiêu chí Giám sát và Quản trị nhật ký tập trung.
