import { api } from '../../services/api.js';

export async function renderDoctorsPage() {
  const user = api.getUser();
  const isAdmin = user && user.role === 'ADMIN';

  let doctors = [];
  let specialties = [];
  try {
    const resDocs = await api.get('/doctors/');
    doctors = resDocs.results || resDocs;

    const resSpecs = await api.get('/specialties/');
    specialties = resSpecs.results || resSpecs;
  } catch (err) {
    console.error('Lỗi tải danh mục bác sĩ / chuyên khoa:', err);
  }

  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Danh mục Bác sĩ Chuyên khoa</h1>
          <p class="page-subtitle">Quản lý đội ngũ y bác sĩ, cấp tài khoản đăng nhập và phân công phòng khám</p>
        </div>
        ${isAdmin ? `<button id="btn-add-doctor" class="btn btn-primary">➕ Thêm Bác sĩ mới</button>` : ''}
      </div>

      <div class="card-table">
        <div class="table-toolbar">
          <div class="search-box">
            <span>🔍</span>
            <input type="text" id="doc-search" placeholder="Tìm theo tên bác sĩ, mã BS, chuyên khoa...">
          </div>
          <span style="font-size: 13px; color: var(--text-muted);">Tổng cộng: <strong>${doctors.length}</strong> bác sĩ</span>
        </div>

        <table id="table-doctors">
          <thead>
            <tr>
              <th>Mã BS</th>
              <th>Tài khoản</th>
              <th>Họ và tên bác sĩ</th>
              <th>Chuyên khoa</th>
              <th>Phòng khám</th>
              <th>Số điện thoại</th>
              <th>Giá khám</th>
              <th>Trạng thái</th>
              ${isAdmin ? `<th>Thao tác</th>` : ''}
            </tr>
          </thead>
          <tbody>
            ${doctors.map(d => `
              <tr data-search="${d.code} ${d.full_name} ${d.specialty_name} ${d.room_number} ${d.user_details?.username || ''}">
                <td><strong style="color: var(--primary);">${d.code}</strong></td>
                <td><code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-weight: 600;">${d.user_details?.username || 'N/A'}</code></td>
                <td><strong>${d.full_name}</strong><br><small style="color: var(--text-muted);">${d.email || ''}</small></td>
                <td><span class="badge badge-confirmed">${d.specialty_name}</span></td>
                <td>${d.room_number}</td>
                <td>${d.phone}</td>
                <td><strong>${Number(d.consultation_fee).toLocaleString('vi-VN')} đ</strong></td>
                <td>
                  <span class="badge ${d.is_active ? 'badge-completed' : 'badge-cancelled'}">
                    ${d.is_active ? 'Đang công tác' : 'Tạm nghỉ'}
                  </span>
                </td>
                ${isAdmin ? `
                  <td>
                    <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                      <button class="btn btn-secondary btn-sm btn-edit-doc" data-doc='${JSON.stringify(d).replace(/'/g, "&apos;")}'>✏️ Sửa</button>
                      <button class="btn btn-secondary btn-sm btn-toggle-doc" data-id="${d.id}" data-active="${d.is_active}">
                        ${d.is_active ? '🔒 Khóa' : '🔓 Mở'}
                      </button>
                      <button class="btn btn-danger btn-sm btn-del-doc" data-id="${d.id}" data-code="${d.code}">🗑️</button>
                    </div>
                  </td>
                ` : ''}
              </tr>
            `).join('') || `<tr><td colspan="${isAdmin ? 9 : 8}" style="text-align: center;">Chưa có bác sĩ nào.</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Thêm Bác Sĩ Mới & Tạo Tài Khoản -->
    <div id="modal-doctor" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3 id="modal-doc-title">Thêm Mới Bác Sĩ & Tạo Tài Khoản</h3>
          <button class="modal-close" id="modal-doctor-close">&times;</button>
        </div>
        <form id="form-create-doctor">
          <input type="hidden" id="edit-doc-id">
          <div class="modal-body">
            <div id="doc-form-error" style="display: none; background: #fee2e2; color: #dc2626; padding: 10px; border-radius: 6px; margin-bottom: 14px; font-size: 13px;"></div>

            <div id="account-section">
              <h4 style="font-size: 14px; color: var(--primary); margin-bottom: 12px; border-bottom: 1px dashed var(--border); padding-bottom: 6px;">1. Thông tin Tài khoản Đăng nhập</h4>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                <div class="form-group">
                  <label>Tên đăng nhập (Username) *</label>
                  <input type="text" id="doc-username" class="form-control" placeholder="Ví dụ: doctor_nam">
                </div>
                <div class="form-group">
                  <label>Mật khẩu khởi tạo *</label>
                  <input type="text" id="doc-password" class="form-control" value="Doc@123" placeholder="Mật khẩu ban đầu">
                </div>
              </div>
            </div>

            <h4 style="font-size: 14px; color: var(--primary); margin-top: 14px; margin-bottom: 12px; border-bottom: 1px dashed var(--border); padding-bottom: 6px;">2. Thông tin Hồ sơ Chuyên môn</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Họ và học hàm *</label>
                <input type="text" id="doc-lastname" class="form-control" required placeholder="Ví dụ: ThS.BS Nguyễn">
              </div>
              <div class="form-group">
                <label>Tên bác sĩ *</label>
                <input type="text" id="doc-firstname" class="form-control" required placeholder="Ví dụ: Thành Nam">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Chuyên khoa công tác *</label>
                <select id="doc-specialty" class="form-control" required>
                  <option value="">-- Chọn chuyên khoa --</option>
                  ${specialties.map(s => `<option value="${s.id}">${s.name} (${s.code})</option>`).join('')}
                </select>
              </div>
              <div class="form-group">
                <label>Phòng khám tiếp nhận *</label>
                <input type="text" id="doc-room" class="form-control" required placeholder="Ví dụ: Phòng 302 - Tầng 3">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Số điện thoại *</label>
                <input type="tel" id="doc-phone" class="form-control" required placeholder="09xxxxxxxx">
              </div>
              <div class="form-group">
                <label>Email công tác</label>
                <input type="email" id="doc-email" class="form-control" placeholder="bacsi@phucanclinic.vn">
              </div>
            </div>

            <div class="form-group">
              <label>Giá khám bệnh (VNĐ) *</label>
              <input type="number" id="doc-fee" class="form-control" required value="200000" min="50000" step="10000">
            </div>

            <div class="form-group">
              <label>Tiểu sử / Quá trình công tác</label>
              <textarea id="doc-bio" class="form-control" rows="2" placeholder="Kinh nghiệm khám chữa bệnh, chứng chỉ hành nghề..."></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" id="btn-cancel-doc">Hủy</button>
            <button type="submit" class="btn btn-primary" id="btn-save-doc">Lưu thông tin Bác sĩ</button>
          </div>
        </form>
      </div>
    </div>
  `;
}

export function initDoctorsEvents() {
  const modal = document.getElementById('modal-doctor');
  const btnAdd = document.getElementById('btn-add-doctor');
  const btnClose = document.getElementById('modal-doctor-close');
  const btnCancel = document.getElementById('btn-cancel-doc');
  const form = document.getElementById('form-create-doctor');
  const searchInput = document.getElementById('doc-search');
  const modalTitle = document.getElementById('modal-doc-title');
  const accountSection = document.getElementById('account-section');
  const editIdInput = document.getElementById('edit-doc-id');

  if (btnAdd) {
    btnAdd.onclick = () => {
      editIdInput.value = '';
      modalTitle.innerText = 'Thêm Mới Bác Sĩ & Tạo Tài Khoản';
      accountSection.style.display = 'block';
      document.getElementById('doc-username').required = true;
      form.reset();
      document.getElementById('doc-fee').value = '200000';
      modal.classList.add('open');
    };
  }

  if (btnClose) btnClose.onclick = () => modal.classList.remove('open');
  if (btnCancel) btnCancel.onclick = () => modal.classList.remove('open');

  // Search filter
  if (searchInput) {
    searchInput.oninput = (e) => {
      const q = e.target.value.toLowerCase();
      document.querySelectorAll('#table-doctors tbody tr').forEach(tr => {
        const text = (tr.dataset.search || '').toLowerCase();
        tr.style.display = text.includes(q) ? '' : 'none';
      });
    };
  }

  // Khóa / Mở khóa bác sĩ
  document.querySelectorAll('.btn-toggle-doc').forEach(btn => {
    btn.onclick = async () => {
      const id = btn.dataset.id;
      const isActive = btn.dataset.active === 'true';
      const action = isActive ? 'tạm ngưng công tác' : 'kích hoạt hoạt động lại';
      if (!confirm(`Bạn có chắc chắn muốn ${action} cho bác sĩ này không?`)) return;

      try {
        await api.put(`/doctors/${id}/`, { is_active: !isActive });
        window.location.reload();
      } catch (err) {
        alert('Lỗi cập nhật trạng thái bác sĩ: ' + err.message);
      }
    };
  });

  // Xóa bác sĩ
  document.querySelectorAll('.btn-del-doc').forEach(btn => {
    btn.onclick = async () => {
      const id = btn.dataset.id;
      const code = btn.dataset.code;
      if (!confirm(`Bạn có chắc chắn muốn xóa bác sĩ ${code} không?`)) return;

      try {
        await api.delete(`/doctors/${id}/`);
        window.location.reload();
      } catch (err) {
        alert('Lỗi khi xóa bác sĩ: ' + err.message);
      }
    };
  });

  // Sửa bác sĩ
  document.querySelectorAll('.btn-edit-doc').forEach(btn => {
    btn.onclick = () => {
      const d = JSON.parse(btn.dataset.doc);
      editIdInput.value = d.id;
      modalTitle.innerText = `Chỉnh Sửa Thông Tin Bác Sĩ: ${d.code}`;
      accountSection.style.display = 'none'; // Không sửa username ở đây
      document.getElementById('doc-username').required = false;

      document.getElementById('doc-lastname').value = d.user_details?.last_name || '';
      document.getElementById('doc-firstname').value = d.user_details?.first_name || '';
      document.getElementById('doc-specialty').value = d.specialty;
      document.getElementById('doc-room').value = d.room_number;
      document.getElementById('doc-phone').value = d.phone;
      document.getElementById('doc-email').value = d.email || '';
      document.getElementById('doc-fee').value = d.consultation_fee;
      document.getElementById('doc-bio').value = d.bio || '';

      modal.classList.add('open');
    };
  });

  // Submit form
  if (form) {
    form.onsubmit = async (e) => {
      e.preventDefault();
      const errBox = document.getElementById('doc-form-error');
      errBox.style.display = 'none';

      const isEdit = !!editIdInput.value;
      const data = {
        first_name: document.getElementById('doc-firstname').value.trim(),
        last_name: document.getElementById('doc-lastname').value.trim(),
        specialty: parseInt(document.getElementById('doc-specialty').value),
        room_number: document.getElementById('doc-room').value.trim(),
        phone: document.getElementById('doc-phone').value.trim(),
        email: document.getElementById('doc-email').value.trim(),
        consultation_fee: parseInt(document.getElementById('doc-fee').value),
        bio: document.getElementById('doc-bio').value.trim()
      };

      if (!isEdit) {
        data.username = document.getElementById('doc-username').value.trim();
        data.password = document.getElementById('doc-password').value.trim();
        data.is_active = true;
      }

      try {
        const btnSave = document.getElementById('btn-save-doc');
        btnSave.disabled = true;
        btnSave.innerText = 'Đang lưu...';

        if (isEdit) {
          await api.put(`/doctors/${editIdInput.value}/`, data);
        } else {
          await api.post('/doctors/', data);
        }
        modal.classList.remove('open');
        window.location.reload();
      } catch (err) {
        errBox.innerText = err.message || 'Lỗi khi lưu thông tin bác sĩ.';
        errBox.style.display = 'block';
      } finally {
        const btnSave = document.getElementById('btn-save-doc');
        if (btnSave) {
          btnSave.disabled = false;
          btnSave.innerText = 'Lưu thông tin Bác sĩ';
        }
      }
    };
  }
}
