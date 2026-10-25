# BÁO CÁO KẾT THÚC HỌC PHẦN
## TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM

- **Tên đề tài**: Đề 8 — Hệ thống Quản lý Phòng khám / Bệnh viện (Clinic Management System)
- **Sinh viên thực hiện**: Nguyễn Văn Thắng
- **Mã sinh viên**: DTC245200146
- **Giảng viên hướng dẫn**: Bộ môn Công nghệ Phần mềm & Hệ thống thông tin

---

## 1. LÝ DO CHỌN ĐỀ TÀI VÀ MỤC TIÊU NGHIÊN CỨU
Trong chuyển đổi số y tế, việc điều phối phòng khám, chống trùng lịch khám của bác sĩ và quản trị tập trung hồ sơ bệnh án, đơn thuốc điện tử là bài toán tối quan trọng.
Mục tiêu của đồ án:
1. Xây dựng ứng dụng quản lý y tế thực tế, đáp ứng đầy đủ các quy trình nghiệp vụ: Tiếp nhận, đặt lịch hẹn, khám bệnh, kê đơn thuốc và in ấn.
2. Triển khai theo mô hình Container hóa hoàn chỉnh bằng **Docker Compose** với tính sẵn sàng cao.
3. Thiết lập hệ thống giám sát toàn diện (**Prometheus & Grafana**) và quản trị nhật ký tập trung (**Loki & Promtail**).
4. Áp dụng các biện pháp Hardening bảo mật hệ thống theo tiêu chuẩn an toàn thông tin.

---

## 2. PHÂN TÍCH CHỨC NĂNG NGHIỆP VỤ HỆ THỐNG
1. **Xác thực và Phân quyền RBAC**:
   - `ADMIN`: Quản trị toàn bộ danh mục bác sĩ, chuyên khoa, người dùng và tra cứu nhật ký audit.
   - `DOCTOR`: Bác sĩ trực tiếp vào lượt khám, chẩn đoán bệnh án, kê đơn thuốc và in phiếu khám.
   - `RECEPTIONIST`: Lễ tân tạo hồ sơ bệnh nhân, điều phối lịch hẹn, check-in và hủy lịch.
2. **Quản lý Hồ sơ Bệnh nhân**:
   - Mã bệnh nhân duy nhất dạng `BN-XXXXX`, kiểm tra trùng số điện thoại, quản lý nhóm máu, tiền sử dị ứng.
3. **Quản lý Lịch hẹn & Chống trùng lịch (Anti-conflict)**:
   - Ngăn chặn triệt để tình trạng 2 bệnh nhân đặt cùng 1 bác sĩ trong cùng khung giờ.
   - Chặn đặt lịch trong quá khứ.
4. **Hồ sơ Bệnh án & Kê đơn thuốc điện tử**:
   - Chỉ số sinh tồn (huyết áp, mạch, nhiệt độ, cân nặng).
   - Đơn thuốc và phác đồ điều trị, tích hợp mẫu in đạt chuẩn Bộ Y tế.
5. **Báo cáo & Thống kê**:
   - Tỷ lệ lịch khám theo chuyên khoa, trạng thái và xuất báo cáo dữ liệu định dạng CSV.

---

## 3. ĐÁNH GIÁ KẾT QUẢ THỰC HIỆN
- **Mức độ hoàn thiện**: 100% chức năng theo yêu cầu đề cương.
- **Tính thực tế**: 11 containers phối hợp nhịp nhàng, dữ liệu lưu trữ bền vững trên PostgreSQL 16.
- **Kiểm thử tự động**: Đầy đủ ca kiểm thử Pytest kiểm tra từ xác thực, CRUD bệnh nhân, chống trùng lịch tới phân quyền y tế.
