import { api } from '../../services/api.js';

export async function renderDashboardPage() {
  let stats = {
    metrics: {
      total_patients: 0,
      total_doctors: 0,
      today_appointments: 0,
      pending_appointments: 0,
      completed_appointments: 0,
      total_medical_records: 0
    },
    specialty_distribution: [],
    recent_7_days: []
  };

  try {
    stats = await api.get('/reports/dashboard/');
  } catch (err) {
    console.error('Lỗi tải dữ liệu dashboard:', err);
  }

  const m = stats.metrics;

  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Tổng quan Hoạt động Phòng khám</h1>
          <p class="page-subtitle">Thống kê dữ liệu thời gian thực truy xuất từ cơ sở dữ liệu PostgreSQL</p>
        </div>
        <a href="#/appointments" class="btn btn-primary">➕ Đặt lịch khám mới</a>
      </div>

      <div class="grid-cards">
        <div class="stat-card">
          <div class="stat-icon teal">👥</div>
          <div class="stat-info">
            <h4>Tổng bệnh nhân</h4>
            <div class="stat-value">${m.total_patients}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon blue">👨‍⚕️</div>
          <div class="stat-info">
            <h4>Bác sĩ công tác</h4>
            <div class="stat-value">${m.total_doctors}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon amber">📅</div>
          <div class="stat-info">
            <h4>Lịch khám hôm nay</h4>
            <div class="stat-value">${m.today_appointments}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon green">✅</div>
          <div class="stat-info">
            <h4>Đã hoàn thành</h4>
            <div class="stat-value">${m.completed_appointments}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon purple">🩺</div>
          <div class="stat-info">
            <h4>Hồ sơ bệnh án</h4>
            <div class="stat-value">${m.total_medical_records}</div>
          </div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;">
        <div class="card-table">
          <div class="table-toolbar">
            <h3 style="font-size: 16px; font-weight: 600;">Lượt khám theo Chuyên khoa</h3>
            <span class="badge badge-confirmed">PostgreSQL Real-time</span>
          </div>
          <table>
            <thead>
              <tr>
                <th>Tên chuyên khoa</th>
                <th>Tổng số lượt khám</th>
                <th>Tỷ trọng</th>
              </tr>
            </thead>
            <tbody>
              ${(stats.specialty_distribution || []).map(s => {
                const total = m.completed_appointments + m.pending_appointments || 1;
                const percent = Math.round((s.appointment_count / total) * 100);
                return `
                  <tr>
                    <td><strong>${s.name}</strong></td>
                    <td>${s.appointment_count} lượt</td>
                    <td>
                      <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="flex: 1; height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
                          <div style="width: ${percent}%; height: 100%; background: var(--primary);"></div>
                        </div>
                        <span style="font-size: 12px; color: var(--text-muted);">${percent}%</span>
                      </div>
                    </td>
                  </tr>
                `;
              }).join('') || '<tr><td colspan="3" style="text-align: center; color: var(--text-muted);">Chưa có dữ liệu</td></tr>'}
            </tbody>
          </table>
        </div>

        <div class="card-table">
          <div class="table-toolbar">
            <h3 style="font-size: 16px; font-weight: 600;">Lịch khám 7 ngày qua</h3>
          </div>
          <div style="padding: 20px;">
            ${(stats.recent_7_days || []).map(d => `
              <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px dashed var(--border);">
                <span style="font-size: 14px; font-weight: 500;">Ngày ${d.date}</span>
                <span class="badge badge-confirmed">${d.count} lịch</span>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    </div>
  `;
}
