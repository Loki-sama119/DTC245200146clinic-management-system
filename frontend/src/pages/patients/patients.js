import { api } from '../../services/api.js';

export async function renderPatientsPage() {
  let patients = [];
  try {
    const res = await api.get('/patients/');
    patients = res.results || res;
  } catch (err) {
    console.error('Lỗi tải danh sách bệnh nhân:', err);
  }

  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Quản lý Hồ sơ Bệnh nhân</h1>
          <p class="page-subtitle">Danh bạ, thông tin liên lạc và lịch sử bệnh lý của bệnh nhân</p>
        </div>
        <button id="btn-add-patient" class="btn btn-primary">➕ Thêm Bệnh nhân mới</button>
      </div>

      <div class="card-table">
        <div class="table-toolbar">
          <div class="search-box">
            <span>🔍</span>
            <input type="text" id="patient-search" placeholder="Tìm theo mã BN, họ tên hoặc SĐT...">
          </div>
          <span style="font-size: 13px; color: var(--text-muted);">Tổng cộng: <strong>${patients.length}</strong> bệnh nhân</span>
        </div>

        <table id="table-patients">
          <thead>
            <tr>
              <th>Mã BN</th>
              <th>Họ và tên</th>
              <th>Ngày sinh</th>
              <th>Giới tính</th>
              <th>Số điện thoại</th>
              <th>Địa chỉ</th>
              <th>Nhóm máu</th>
              <th>Thao tác</th>
            </tr>
          </thead>
          <tbody>
            ${patients.map(p => `
              <tr data-search="${p.code} ${p.full_name} ${p.phone}">
                <td><strong style="color: var(--primary);">${p.code}</strong></td>
                <td><strong>${p.full_name}</strong></td>
                <td>${p.date_of_birth}</td>
                <td>${p.gender === 'MALE' ? 'Nam' : (p.gender === 'FEMALE' ? 'Nữ' : 'Khác')}</td>
                <td>${p.phone}</td>
                <td>${p.address}</td>
                <td><span class="badge badge-confirmed">${p.blood_type || 'N/A'}</span></td>
                <td>
                  <a href="#/appointments?patient_id=${p.id}" class="btn btn-secondary btn-sm">📅 Đặt lịch</a>
                </td>
              </tr>
            `).join('') || '<tr><td colspan="8" style="text-align: center;">Chưa có bệnh nhân nào.</td></tr>'}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Thêm Bệnh Nhân -->
    <div id="modal-patient" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Thêm Mới Hồ Sơ Bệnh Nhân</h3>
          <button class="modal-close" id="modal-patient-close">&times;</button>
        </div>
        <form id="form-create-patient">
          <div class="modal-body">
            <div id="patient-form-error" style="display: none; background: #fee2e2; color: #dc2626; padding: 10px; border-radius: 6px; margin-bottom: 14px; font-size: 13px;"></div>

            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Họ và tên *</label>
                <input type="text" id="p-name" class="form-control" required placeholder="Ví dụ: Nguyễn Văn An">
              </div>
              <div class="form-group">
                <label>Giới tính *</label>
                <select id="p-gender" class="form-control" required>
                  <option value="MALE">Nam</option>
                  <option value="FEMALE">Nữ</option>
                  <option value="OTHER">Khác</option>
                </select>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Ngày sinh *</label>
                <input type="date" id="p-dob" class="form-control" required>
              </div>
              <div class="form-group">
                <label>Số điện thoại *</label>
                <input type="tel" id="p-phone" class="form-control" required placeholder="09xxxxxxxx">
              </div>
            </div>

            <div class="form-group">
              <label>Địa chỉ thường trú *</label>
              <input type="text" id="p-address" class="form-control" required placeholder="Số nhà, đường, quận/huyện...">
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Số CCCD / CMND</label>
                <input type="text" id="p-identity" class="form-control" placeholder="001xxxxxxxxx">
              </div>
              <div class="form-group">
                <label>Nhóm máu</label>
                <select id="p-blood" class="form-control">
                  <option value="">Chưa xác định</option>
                  <option value="A+">A+</option>
                  <option value="B+">B+</option>
                  <option value="AB+">AB+</option>
                  <option value="O+">O+</option>
                </select>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" id="btn-cancel-patient">Hủy</button>
            <button type="submit" class="btn btn-primary" id="btn-save-patient">Lưu hồ sơ</button>
          </div>
        </form>
      </div>
    </div>
  `;
}

export function initPatientsEvents() {
  const modal = document.getElementById('modal-patient');
  const btnAdd = document.getElementById('btn-add-patient');
  const btnClose = document.getElementById('modal-patient-close');
  const btnCancel = document.getElementById('btn-cancel-patient');
  const form = document.getElementById('form-create-patient');
  const searchInput = document.getElementById('patient-search');

  if (btnAdd) btnAdd.onclick = () => modal.classList.add('open');
  if (btnClose) btnClose.onclick = () => modal.classList.remove('open');
  if (btnCancel) btnCancel.onclick = () => modal.classList.remove('open');

  // Search filter
  if (searchInput) {
    searchInput.oninput = (e) => {
      const q = e.target.value.toLowerCase();
      document.querySelectorAll('#table-patients tbody tr').forEach(tr => {
        const text = (tr.dataset.search || '').toLowerCase();
        tr.style.display = text.includes(q) ? '' : 'none';
      });
    };
  }

  // Submit patient form
  if (form) {
    form.onsubmit = async (e) => {
      e.preventDefault();
      const errBox = document.getElementById('patient-form-error');
      errBox.style.display = 'none';

      const data = {
        full_name: document.getElementById('p-name').value.trim(),
        gender: document.getElementById('p-gender').value,
        date_of_birth: document.getElementById('p-dob').value,
        phone: document.getElementById('p-phone').value.trim(),
        address: document.getElementById('p-address').value.trim(),
        identity_number: document.getElementById('p-identity').value.trim(),
        blood_type: document.getElementById('p-blood').value
      };

      try {
        const btnSave = document.getElementById('btn-save-patient');
        btnSave.disabled = true;
        btnSave.innerText = 'Đang lưu...';
        await api.post('/patients/', data);
        modal.classList.remove('open');
        window.location.reload();
      } catch (err) {
        errBox.innerText = err.message || 'Lỗi khi lưu bệnh nhân.';
        errBox.style.display = 'block';
      } finally {
        const btnSave = document.getElementById('btn-save-patient');
        btnSave.disabled = false;
        btnSave.innerText = 'Lưu hồ sơ';
      }
    };
  }
}
