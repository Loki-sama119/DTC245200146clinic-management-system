import { api } from '../../services/api.js';

export async function renderReportsPage() {
  let stats = {
    metrics: {},
    status_distribution: {},
    specialty_distribution: [],
    recent_7_days: []
  };

  try {
    stats = await api.get('/reports/dashboard/');
  } catch (err) {
    console.error('Lỗi tải báo cáo:', err);
  }

  const m = stats.metrics || {};

  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Báo cáo & Thống kê Hoạt động Y tế</h1>
          <p class="page-subtitle">Xuất báo cáo, theo dõi hiệu năng phục vụ và lưu lượng bệnh nhân</p>
        </div>
        <button id="btn-export-csv" class="btn btn-primary">📥 Xuất Báo cáo CSV</button>
      </div>

      <div class="grid-cards">
        <div class="stat-card">
          <div class="stat-icon green">📊</div>
          <div class="stat-info">
            <h4>Tổng lượt khám hoàn tất</h4>
            <div class="stat-value">${m.completed_appointments || 0}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon amber">⏳</div>
          <div class="stat-info">
            <h4>Lượt khám đang chờ</h4>
            <div class="stat-value">${m.pending_appointments || 0}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon blue">🏥</div>
          <div class="stat-info">
            <h4>Tổng bệnh nhân đăng ký</h4>
            <div class="stat-value">${m.total_patients || 0}</div>
          </div>
        </div>
      </div>

      <div class="card-table">
        <div class="table-toolbar">
          <h3 style="font-size: 16px; font-weight: 600;">Bảng Phân Tích Lịch Khám Theo Trạng Thái</h3>
          <span class="badge badge-confirmed">PostgreSQL Aggregated</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Trạng thái lịch khám</th>
              <th>Số lượng ghi nhận</th>
              <th>Đánh giá vận hành</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="badge badge-completed">Đã hoàn thành (COMPLETED)</span></td>
              <td><strong>${stats.status_distribution['COMPLETED'] || 0}</strong> lượt</td>
              <td>Bệnh nhân đã hoàn tất quy trình khám và nhận đơn thuốc</td>
            </tr>
            <tr>
              <td><span class="badge badge-in_progress">Đang khám (IN_PROGRESS)</span></td>
              <td><strong>${stats.status_distribution['IN_PROGRESS'] || 0}</strong> lượt</td>
              <td>Bệnh nhân đang ở trong phòng khám với bác sĩ</td>
            </tr>
            <tr>
              <td><span class="badge badge-confirmed">Đã xác nhận (CONFIRMED)</span></td>
              <td><strong>${stats.status_distribution['CONFIRMED'] || 0}</strong> lượt</td>
              <td>Đã tiếp nhận hồ sơ, chờ vào lượt khám</td>
            </tr>
            <tr>
              <td><span class="badge badge-pending">Chờ xác nhận (PENDING)</span></td>
              <td><strong>${stats.status_distribution['PENDING'] || 0}</strong> lượt</td>
              <td>Lịch hẹn mới đăng ký qua hệ thống</td>
            </tr>
            <tr>
              <td><span class="badge badge-cancelled">Đã hủy (CANCELLED)</span></td>
              <td><strong>${stats.status_distribution['CANCELLED'] || 0}</strong> lượt</td>
              <td>Lịch hẹn bị hủy bởi bệnh nhân hoặc lễ tân</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;
}

export function initReportsEvents() {
  const btnExport = document.getElementById('btn-export-csv');
  if (btnExport) {
    btnExport.onclick = async () => {
      try {
        btnExport.disabled = true;
        btnExport.innerText = 'Đang trích xuất...';
        const res = await api.get('/appointments/');
        const apts = res.results || res;

        let csv = '\uFEFFMã Lịch,Bệnh Nhân,Bác Sĩ,Chuyên Khoa,Ngày Khám,Giờ Khám,Trạng Thái,Lý Do\n';
        apts.forEach(a => {
          csv += `"${a.code}","${a.patient_details?.full_name || ''}","${a.doctor_details?.full_name || ''}","${a.specialty_name || ''}","${a.appointment_date}","${a.start_time}","${a.status}","${(a.reason || '').replace(/"/g, '""')}"\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Bao_Cao_Lich_Kham_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } catch (err) {
        alert('Lỗi xuất CSV: ' + err.message);
      } finally {
        btnExport.disabled = false;
        btnExport.innerText = '📥 Xuất Báo cáo CSV';
      }
    };
  }
}
