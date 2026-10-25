import { api } from '../../services/api.js';

export async function renderSpecialtiesPage() {
  let list = [];
  try {
    const res = await api.get('/specialties/');
    list = res.results || res;
  } catch (err) {
    console.error('Lỗi tải chuyên khoa:', err);
  }

  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Danh mục Chuyên khoa Phòng khám</h1>
          <p class="page-subtitle">Phân bổ chuyên môn và dịch vụ y tế của phòng khám Phúc An</p>
        </div>
        <button id="btn-add-spec" class="btn btn-primary">➕ Thêm Chuyên khoa mới</button>
      </div>

      <div class="card-table">
        <div class="table-toolbar">
          <div class="search-box">
            <span>🔍</span>
            <input type="text" id="spec-search" placeholder="Tìm kiếm chuyên khoa...">
          </div>
          <span style="font-size: 13px; color: var(--text-muted);">Tổng cộng: <strong>${list.length}</strong> chuyên khoa</span>
        </div>

        <table id="table-specs">
          <thead>
            <tr>
              <th>Mã CK</th>
              <th>Tên chuyên khoa</th>
              <th>Mô tả chuyên môn</th>
              <th>Số lượng bác sĩ</th>
              <th>Trạng thái</th>
            </tr>
          </thead>
          <tbody>
            ${list.map(s => `
              <tr data-search="${s.code} ${s.name} ${s.description}">
                <td><strong style="color: var(--primary);">${s.code}</strong></td>
                <td><strong>${s.name}</strong></td>
                <td style="max-width: 300px;">${s.description || 'Chưa cập nhật'}</td>
                <td><span class="badge badge-confirmed">${s.doctors_count || 0} bác sĩ</span></td>
                <td>
                  <span class="badge ${s.is_active ? 'badge-completed' : 'badge-cancelled'}">
                    ${s.is_active ? 'Hoạt động' : 'Tạm dừng'}
                  </span>
                </td>
              </tr>
            `).join('') || '<tr><td colspan="5" style="text-align: center;">Chưa có chuyên khoa nào.</td></tr>'}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Thêm Chuyên Khoa -->
    <div id="modal-spec" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Thêm Mới Chuyên Khoa</h3>
          <button class="modal-close" id="modal-spec-close">&times;</button>
        </div>
        <form id="form-create-spec">
          <div class="modal-body">
            <div id="spec-form-error" style="display: none; background: #fee2e2; color: #dc2626; padding: 10px; border-radius: 6px; margin-bottom: 14px; font-size: 13px;"></div>

            <div class="form-group">
              <label>Mã chuyên khoa *</label>
              <input type="text" id="spec-code" class="form-control" required placeholder="Ví dụ: CK-TIMMACH">
            </div>

            <div class="form-group">
              <label>Tên chuyên khoa *</label>
              <input type="text" id="spec-name" class="form-control" required placeholder="Ví dụ: Khoa Tim Mạch">
            </div>

            <div class="form-group">
              <label>Mô tả chuyên môn</label>
              <textarea id="spec-desc" class="form-control" rows="3" placeholder="Mô tả phạm vi khám và chẩn đoán..."></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" id="btn-cancel-spec">Hủy</button>
            <button type="submit" class="btn btn-primary" id="btn-save-spec">Lưu chuyên khoa</button>
          </div>
        </form>
      </div>
    </div>
  `;
}

export function initSpecialtiesEvents() {
  const modal = document.getElementById('modal-spec');
  const btnAdd = document.getElementById('btn-add-spec');
  const btnClose = document.getElementById('modal-spec-close');
  const btnCancel = document.getElementById('btn-cancel-spec');
  const form = document.getElementById('form-create-spec');
  const searchInput = document.getElementById('spec-search');

  if (btnAdd) btnAdd.onclick = () => modal.classList.add('open');
  if (btnClose) btnClose.onclick = () => modal.classList.remove('open');
  if (btnCancel) btnCancel.onclick = () => modal.classList.remove('open');

  if (searchInput) {
    searchInput.oninput = (e) => {
      const q = e.target.value.toLowerCase();
      document.querySelectorAll('#table-specs tbody tr').forEach(tr => {
        const text = (tr.dataset.search || '').toLowerCase();
        tr.style.display = text.includes(q) ? '' : 'none';
      });
    };
  }

  if (form) {
    form.onsubmit = async (e) => {
      e.preventDefault();
      const errBox = document.getElementById('spec-form-error');
      errBox.style.display = 'none';

      const data = {
        code: document.getElementById('spec-code').value.trim(),
        name: document.getElementById('spec-name').value.trim(),
        description: document.getElementById('spec-desc').value.trim()
      };

      try {
        const btnSave = document.getElementById('btn-save-spec');
        btnSave.disabled = true;
        btnSave.innerText = 'Đang lưu...';
        await api.post('/specialties/', data);
        modal.classList.remove('open');
        window.location.reload();
      } catch (err) {
        errBox.innerText = err.message || 'Lỗi khi lưu chuyên khoa.';
        errBox.style.display = 'block';
      } finally {
        const btnSave = document.getElementById('btn-save-spec');
        btnSave.disabled = false;
        btnSave.innerText = 'Lưu chuyên khoa';
      }
    };
  }
}
