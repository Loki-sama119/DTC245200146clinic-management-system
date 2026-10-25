import { api } from '../../services/api.js';

export async function renderAppointmentsPage() {
  let appointments = [];
  let doctors = [];
  let patients = [];
  let specialties = [];

  try {
    const [aptRes, docRes, patRes, specRes] = await Promise.all([
      api.get('/appointments/'),
      api.get('/doctors/'),
      api.get('/patients/'),
      api.get('/specialties/')
    ]);
    appointments = aptRes.results || aptRes;
    doctors = docRes.results || docRes;
    patients = patRes.results || patRes;
    specialties = specRes.results || specRes;
  } catch (err) {
    console.error('Lỗi tải dữ liệu lịch hẹn:', err);
  }

  const statusMap = {
    'PENDING': { label: 'Chờ xác nhận', class: 'badge-pending' },
    'CONFIRMED': { label: 'Đã xác nhận', class: 'badge-confirmed' },
    'IN_PROGRESS': { label: 'Đang khám', class: 'badge-in_progress' },
    'COMPLETED': { label: 'Đã hoàn thành', class: 'badge-completed' },
    'CANCELLED': { label: 'Đã hủy', class: 'badge-cancelled' },
    'NO_SHOW': { label: 'Bỏ hẹn', class: 'badge-no_show' },
  };

  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Quản lý Lịch hẹn Khám bệnh</h1>
          <p class="page-subtitle">Theo dõi tiếp nhận, điều phối phòng khám và chống đặt trùng lịch của Bác sĩ</p>
        </div>
        <button id="btn-open-modal-apt" class="btn btn-primary">➕ Đặt lịch khám mới</button>
      </div>

      <div class="card-table">
        <div class="table-toolbar">
          <div class="search-box">
            <span>🔍</span>
            <input type="text" id="apt-search" placeholder="Tìm theo mã lịch, tên BN, bác sĩ...">
          </div>
          <div style="display: flex; gap: 8px;">
            <select id="filter-apt-status" class="form-control" style="width: 180px; padding: 6px 12px;">
              <option value="">Tất cả trạng thái</option>
              <option value="PENDING">Chờ xác nhận</option>
              <option value="CONFIRMED">Đã xác nhận</option>
              <option value="IN_PROGRESS">Đang khám</option>
              <option value="COMPLETED">Đã hoàn thành</option>
              <option value="CANCELLED">Đã hủy</option>
            </select>
          </div>
        </div>

        <table id="table-appointments">
          <thead>
            <tr>
              <th>Mã lịch</th>
              <th>Bệnh nhân</th>
              <th>Bác sĩ phụ trách</th>
              <th>Chuyên khoa</th>
              <th>Ngày & Giờ</th>
              <th>Trạng thái</th>
              <th>Lý do khám</th>
              <th>Thao tác</th>
            </tr>
          </thead>
          <tbody>
            ${appointments.map(apt => {
              const st = statusMap[apt.status] || { label: apt.status, class: 'badge-pending' };
              const patName = apt.patient_details?.full_name || 'BN-' + apt.patient;
              const docName = apt.doctor_details?.full_name || 'BS-' + apt.doctor;
              return `
                <tr data-search="${apt.code} ${patName} ${docName} ${apt.reason}" data-status="${apt.status}">
                  <td><strong style="color: var(--primary);">${apt.code}</strong></td>
                  <td><strong>${patName}</strong><br><small style="color: var(--text-muted);">${apt.patient_details?.phone || ''}</small></td>
                  <td>${docName}<br><small style="color: var(--text-muted);">${apt.doctor_details?.room_number || ''}</small></td>
                  <td><span class="badge badge-confirmed">${apt.specialty_name || ''}</span></td>
                  <td>
                    <strong>${apt.appointment_date}</strong><br>
                    <span style="color: var(--primary);">${apt.start_time.slice(0, 5)} - ${apt.end_time.slice(0, 5)}</span>
                  </td>
                  <td><span class="badge ${st.class}">${st.label}</span></td>
                  <td style="max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${apt.reason}</td>
                  <td>
                    <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                      ${apt.status === 'PENDING' ? `
                        <button class="btn btn-primary btn-sm btn-action-apt" data-action="confirm" data-id="${apt.id}">Duyệt</button>
                      ` : ''}
                      ${apt.status === 'CONFIRMED' ? `
                        <button class="btn btn-secondary btn-sm btn-action-apt" data-action="check-in" data-id="${apt.id}">Tiếp nhận</button>
                      ` : ''}
                      ${apt.status === 'IN_PROGRESS' ? `
                        <a href="#/medical-records?appointment_id=${apt.id}&patient_id=${apt.patient}&doctor_id=${apt.doctor}" class="btn btn-primary btn-sm">🩺 Vào khám</a>
                      ` : ''}
                      ${['PENDING', 'CONFIRMED'].includes(apt.status) ? `
                        <button class="btn btn-danger btn-sm btn-action-apt" data-action="cancel" data-id="${apt.id}">Hủy</button>
                      ` : ''}
                    </div>
                  </td>
                </tr>
              `;
            }).join('') || '<tr><td colspan="8" style="text-align: center;">Chưa có lịch hẹn nào.</td></tr>'}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Đặt Lịch Hẹn -->
    <div id="modal-apt" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Đặt Lịch Hẹn Khám Bệnh Mới</h3>
          <button class="modal-close" id="modal-apt-close">&times;</button>
        </div>
        <form id="form-create-apt">
          <div class="modal-body">
            <div id="apt-form-error" style="display: none; background: #fee2e2; color: #dc2626; padding: 12px; border-radius: 8px; margin-bottom: 16px; font-size: 13px; border-left: 4px solid #dc2626;"></div>

            <div class="form-group">
              <label>Bệnh nhân *</label>
              <select id="apt-patient" class="form-control" required>
                <option value="">-- Chọn bệnh nhân --</option>
                ${patients.map(p => `<option value="${p.id}">${p.full_name} (${p.code}) - ${p.phone}</option>`).join('')}
              </select>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Chuyên khoa *</label>
                <select id="apt-specialty" class="form-control" required>
                  <option value="">-- Chọn chuyên khoa --</option>
                  ${specialties.map(s => `<option value="${s.id}">${s.name}</option>`).join('')}
                </select>
              </div>

              <div class="form-group">
                <label>Bác sĩ phụ trách *</label>
                <select id="apt-doctor" class="form-control" required>
                  <option value="">-- Chọn bác sĩ --</option>
                  ${doctors.map(d => `<option value="${d.id}" data-spec="${d.specialty}">${d.full_name} (${d.specialty_name})</option>`).join('')}
                </select>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Ngày khám *</label>
                <input type="date" id="apt-date" class="form-control" required value="${new Date().toISOString().split('T')[0]}">
              </div>
              <div class="form-group">
                <label>Khung giờ khám *</label>
                <select id="apt-time" class="form-control" required>
                  <option value="08:00:00">08:00 - 08:30</option>
                  <option value="08:30:00">08:30 - 09:00</option>
                  <option value="09:00:00">09:00 - 09:30</option>
                  <option value="09:30:00">09:30 - 10:00</option>
                  <option value="10:00:00">10:00 - 10:30</option>
                  <option value="10:30:00">10:30 - 11:00</option>
                  <option value="13:30:00">13:30 - 14:00</option>
                  <option value="14:00:00">14:00 - 14:30</option>
                  <option value="14:30:00">14:30 - 15:00</option>
                  <option value="15:00:00">15:00 - 15:30</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>Lý do khám / Triệu chứng ban đầu *</label>
              <textarea id="apt-reason" class="form-control" rows="3" required placeholder="Mô tả lý do khám hoặc triệu chứng của bệnh nhân..."></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" id="btn-cancel-apt">Hủy</button>
            <button type="submit" class="btn btn-primary" id="btn-save-apt">Xác nhận đặt lịch</button>
          </div>
        </form>
      </div>
    </div>
  `;
}

export function initAppointmentsEvents() {
  const modal = document.getElementById('modal-apt');
  const btnOpen = document.getElementById('btn-open-modal-apt');
  const btnClose = document.getElementById('modal-apt-close');
  const btnCancel = document.getElementById('btn-cancel-apt');
  const form = document.getElementById('form-create-apt');
  const searchInput = document.getElementById('apt-search');
  const statusFilter = document.getElementById('filter-apt-status');

  if (btnOpen) btnOpen.onclick = () => modal.classList.add('open');
  if (btnClose) btnClose.onclick = () => modal.classList.remove('open');
  if (btnCancel) btnCancel.onclick = () => modal.classList.remove('open');

  // Search & Status filters
  const applyFilters = () => {
    const q = (searchInput?.value || '').toLowerCase();
    const st = statusFilter?.value || '';
    document.querySelectorAll('#table-appointments tbody tr').forEach(tr => {
      const textMatch = (tr.dataset.search || '').toLowerCase().includes(q);
      const statusMatch = !st || tr.dataset.status === st;
      tr.style.display = (textMatch && statusMatch) ? '' : 'none';
    });
  };

  if (searchInput) searchInput.oninput = applyFilters;
  if (statusFilter) statusFilter.onchange = applyFilters;

  // Actions: confirm, check-in, cancel
  document.querySelectorAll('.btn-action-apt').forEach(btn => {
    btn.onclick = async () => {
      const action = btn.dataset.action;
      const id = btn.dataset.id;
      if (action === 'cancel' && !confirm('Bạn có chắc chắn muốn hủy lịch hẹn này?')) return;

      try {
        btn.disabled = true;
        await api.post(`/appointments/${id}/${action}/`);
        window.location.reload();
      } catch (err) {
        alert(err.message || 'Lỗi thao tác.');
        btn.disabled = false;
      }
    };
  });

  // Submit appointment
  if (form) {
    form.onsubmit = async (e) => {
      e.preventDefault();
      const errBox = document.getElementById('apt-form-error');
      errBox.style.display = 'none';

      const data = {
        patient: document.getElementById('apt-patient').value,
        specialty: document.getElementById('apt-specialty').value,
        doctor: document.getElementById('apt-doctor').value,
        appointment_date: document.getElementById('apt-date').value,
        start_time: document.getElementById('apt-time').value,
        reason: document.getElementById('apt-reason').value.trim()
      };

      try {
        const btnSave = document.getElementById('btn-save-apt');
        btnSave.disabled = true;
        btnSave.innerText = 'Đang kiểm tra & đặt lịch...';
        await api.post('/appointments/', data);
        modal.classList.remove('open');
        window.location.reload();
      } catch (err) {
        errBox.innerText = err.message || 'Lỗi đặt lịch hẹn.';
        errBox.style.display = 'block';
      } finally {
        const btnSave = document.getElementById('btn-save-apt');
        btnSave.disabled = false;
        btnSave.innerText = 'Xác nhận đặt lịch';
      }
    };
  }
}
