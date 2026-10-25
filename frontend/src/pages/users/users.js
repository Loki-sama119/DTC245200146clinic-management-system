import { api } from '../../services/api.js';

export async function renderUsersPage() {
  let users = [];
  try {
    const res = await api.get('/auth/users/');
    users = res.results || res;
  } catch (err) {
    console.error('Lỗi tải danh sách người dùng:', err);
  }

  const roleBadge = {
    'ADMIN': '<span class="badge" style="background:#ede9fe; color:#6d28d9;">Quản trị viên</span>',
    'DOCTOR': '<span class="badge badge-confirmed">Bác sĩ</span>',
    'RECEPTIONIST': '<span class="badge badge-completed">Lễ tân / Tiếp đón</span>'
  };

  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Quản lý Nhân viên & Tài khoản</h1>
          <p class="page-subtitle">Phân quyền, cấp tài khoản và quản trị nhân sự phòng khám</p>
        </div>
        <button id="btn-add-user" class="btn btn-primary">➕ Thêm Nhân viên mới</button>
      </div>

      <div class="card-table">
        <div class="table-toolbar">
          <div class="search-box">
            <span>🔍</span>
            <input type="text" id="user-search" placeholder="Tìm theo tên đăng nhập, họ tên hoặc vai trò...">
          </div>
          <span style="font-size: 13px; color: var(--text-muted);">Tổng cộng: <strong>${users.length}</strong> tài khoản</span>
        </div>

        <table id="table-users">
          <thead>
            <tr>
              <th>ID</th>
              <th>Tên đăng nhập</th>
              <th>Họ và tên</th>
              <th>Vai trò</th>
              <th>Số điện thoại / Email</th>
              <th>Trạng thái</th>
              <th>Thao tác</th>
            </tr>
          </thead>
          <tbody>
            ${users.map(u => `
              <tr data-search="${u.username} ${u.first_name} ${u.last_name} ${u.role}">
                <td>#${u.id}</td>
                <td><strong style="color: var(--primary); font-family: monospace; font-size: 14px;">${u.username}</strong></td>
                <td><strong>${u.last_name || ''} ${u.first_name || ''}</strong></td>
                <td>${roleBadge[u.role] || u.role}</td>
                <td>${u.phone || '—'}<br><small style="color: var(--text-muted);">${u.email || ''}</small></td>
                <td>
                  <span class="badge ${u.is_active ? 'badge-completed' : 'badge-cancelled'}">
                    ${u.is_active ? '🟢 Hoạt động' : '🔴 Đã khóa'}
                  </span>
                </td>
                <td>
                  <div style="display: flex; gap: 6px; align-items: center;">
                    ${u.username !== 'admin' && u.role !== 'ADMIN' ? `
                      <button class="btn btn-secondary btn-sm btn-toggle-user" data-id="${u.id}" data-active="${u.is_active}">
                        ${u.is_active ? '🔒 Khóa' : '🔓 Mở khóa'}
                      </button>
                      <button class="btn btn-danger btn-sm btn-del-user" data-id="${u.id}" data-username="${u.username}">
                        🗑️ Xóa
                      </button>
                    ` : `
                      <span class="badge" style="background: #f1f5f9; color: #64748b; font-size: 11px;">🛡️ Tài khoản gốc (Bảo vệ)</span>
                    `}
                  </div>
                </td>
              </tr>
            `).join('') || '<tr><td colspan="7" style="text-align: center;">Chưa có tài khoản nào.</td></tr>'}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Thêm Nhân Viên Mới -->
    <div id="modal-user" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Thêm Mới Nhân Viên & Cấp Tài Khoản</h3>
          <button class="modal-close" id="modal-user-close">&times;</button>
        </div>
        <form id="form-create-user">
          <div class="modal-body">
            <div id="user-form-error" style="display: none; background: #fee2e2; color: #dc2626; padding: 10px; border-radius: 6px; margin-bottom: 14px; font-size: 13px;"></div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Tên đăng nhập (Username) *</label>
                <input type="text" id="u-username" class="form-control" required placeholder="Ví dụ: letan.mai">
              </div>
              <div class="form-group">
                <label>Mật khẩu khởi tạo *</label>
                <input type="text" id="u-password" class="form-control" required value="Staff@123" placeholder="Mật khẩu ban đầu">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Họ đệm</label>
                <input type="text" id="u-lastname" class="form-control" placeholder="Ví dụ: Nguyễn Thị">
              </div>
              <div class="form-group">
                <label>Tên nhân viên *</label>
                <input type="text" id="u-firstname" class="form-control" required placeholder="Ví dụ: Mai">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div class="form-group">
                <label>Vai trò hệ thống (Role) *</label>
                <select id="u-role" class="form-control" required>
                  <option value="RECEPTIONIST">👩‍💼 Lễ tân / Tiếp đón bệnh nhân</option>
                  <option value="DOCTOR">🩺 Bác sĩ khám chữa bệnh</option>
                  <option value="ADMIN">🛡️ Quản trị viên (Toàn quyền)</option>
                </select>
              </div>
              <div class="form-group">
                <label>Số điện thoại</label>
                <input type="tel" id="u-phone" class="form-control" placeholder="09xxxxxxxx">
              </div>
            </div>

            <div class="form-group">
              <label>Địa chỉ Email</label>
              <input type="email" id="u-email" class="form-control" placeholder="nhanvien@phucanclinic.vn">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" id="btn-cancel-user">Hủy</button>
            <button type="submit" class="btn btn-primary" id="btn-save-user">Tạo tài khoản</button>
          </div>
        </form>
      </div>
    </div>
  `;
}

export function initUsersEvents() {
  const modal = document.getElementById('modal-user');
  const btnAdd = document.getElementById('btn-add-user');
  const btnClose = document.getElementById('modal-user-close');
  const btnCancel = document.getElementById('btn-cancel-user');
  const form = document.getElementById('form-create-user');
  const searchInput = document.getElementById('user-search');

  if (btnAdd) btnAdd.onclick = () => modal.classList.add('open');
  if (btnClose) btnClose.onclick = () => modal.classList.remove('open');
  if (btnCancel) btnCancel.onclick = () => modal.classList.remove('open');

  if (searchInput) {
    searchInput.oninput = (e) => {
      const q = e.target.value.toLowerCase();
      document.querySelectorAll('#table-users tbody tr').forEach(tr => {
        const text = (tr.dataset.search || '').toLowerCase();
        tr.style.display = text.includes(q) ? '' : 'none';
      });
    };
  }

  // Khóa / Mở khóa tài khoản
  document.querySelectorAll('.btn-toggle-user').forEach(btn => {
    btn.onclick = async () => {
      const id = btn.dataset.id;
      const isActive = btn.dataset.active === 'true';
      const action = isActive ? 'khóa' : 'mở khóa';
      if (!confirm(`Bạn có chắc muốn ${action} tài khoản này không?`)) return;

      try {
        await api.put(`/auth/users/${id}/`, { is_active: !isActive });
        window.location.reload();
      } catch (err) {
        alert('Lỗi cập nhật trạng thái tài khoản: ' + err.message);
      }
    };
  });

  // Xóa tài khoản
  document.querySelectorAll('.btn-del-user').forEach(btn => {
    btn.onclick = async () => {
      const id = btn.dataset.id;
      const uname = btn.dataset.username;
      if (!confirm(`Bạn có chắc chắn muốn xóa vĩnh viễn tài khoản '${uname}' không?`)) return;

      try {
        await api.delete(`/auth/users/${id}/`);
        window.location.reload();
      } catch (err) {
        alert('Lỗi khi xóa tài khoản: ' + err.message);
      }
    };
  });

  // Submit form tạo user
  if (form) {
    form.onsubmit = async (e) => {
      e.preventDefault();
      const errBox = document.getElementById('user-form-error');
      errBox.style.display = 'none';

      const data = {
        username: document.getElementById('u-username').value.trim(),
        password: document.getElementById('u-password').value.trim(),
        first_name: document.getElementById('u-firstname').value.trim(),
        last_name: document.getElementById('u-lastname').value.trim(),
        role: document.getElementById('u-role').value,
        phone: document.getElementById('u-phone').value.trim(),
        email: document.getElementById('u-email').value.trim()
      };

      try {
        const btnSave = document.getElementById('btn-save-user');
        btnSave.disabled = true;
        btnSave.innerText = 'Đang tạo...';
        await api.post('/auth/users/', data);
        modal.classList.remove('open');
        window.location.reload();
      } catch (err) {
        errBox.innerText = err.message || 'Lỗi khi tạo tài khoản.';
        errBox.style.display = 'block';
      } finally {
        const btnSave = document.getElementById('btn-save-user');
        if (btnSave) {
          btnSave.disabled = false;
          btnSave.innerText = 'Tạo tài khoản';
        }
      }
    };
  }
}
