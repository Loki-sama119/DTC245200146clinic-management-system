import { api } from '../../services/api.js';

export async function renderMedicalRecordsPage() {
  let records = [];
  let inProgressApts = [];

  try {
    const [recRes, aptRes] = await Promise.all([
      api.get('/medical-records/'),
      api.get('/appointments/', { status: 'IN_PROGRESS' })
    ]);
    records = recRes.results || recRes;
    inProgressApts = aptRes.results || aptRes;
  } catch (err) {
    console.error('Lỗi tải bệnh án:', err);
  }

  // Check query params if directed from appointment
  const urlParams = new URLSearchParams(window.location.hash.split('?')[1] || '');
  const targetAptId = urlParams.get('appointment_id');
  const targetPatId = urlParams.get('patient_id');
  const targetDocId = urlParams.get('doctor_id');

  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Hồ sơ Bệnh án & Kê đơn thuốc</h1>
          <p class="page-subtitle">Khám bệnh, chẩn đoán, lưu trữ phác đồ điều trị và in đơn thuốc điện tử</p>
        </div>
        ${inProgressApts.length > 0 ? `
          <button id="btn-open-examine" class="btn btn-primary">🩺 Khám cho bệnh nhân chờ (${inProgressApts.length})</button>
        ` : ''}
      </div>

      <div class="card-table">
        <div class="table-toolbar">
          <div class="search-box">
            <span>🔍</span>
            <input type="text" id="record-search" placeholder="Tìm theo mã bệnh án, tên BN, chẩn đoán...">
          </div>
          <span style="font-size: 13px; color: var(--text-muted);">Tổng số: <strong>${records.length}</strong> bệnh án</span>
        </div>

        <table id="table-records">
          <thead>
            <tr>
              <th>Mã BA</th>
              <th>Bệnh nhân</th>
              <th>Bác sĩ khám</th>
              <th>Triệu chứng</th>
              <th>Chẩn đoán xác định</th>
              <th>Ngày khám</th>
              <th>Thao tác</th>
            </tr>
          </thead>
          <tbody>
            ${records.map(r => `
              <tr data-search="${r.code} ${r.patient_details?.full_name} ${r.diagnosis} ${r.symptoms}">
                <td><strong style="color: var(--primary);">${r.code}</strong></td>
                <td><strong>${r.patient_details?.full_name || ''}</strong><br><small style="color: var(--text-muted);">${r.patient_details?.code || ''}</small></td>
                <td>${r.doctor_details?.full_name || ''}</td>
                <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${r.symptoms}</td>
                <td><strong style="color: #0369a1;">${r.diagnosis}</strong></td>
                <td>${new Date(r.created_at).toLocaleDateString('vi-VN')}</td>
                <td>
                  <button class="btn btn-secondary btn-sm btn-view-print" data-record='${JSON.stringify(r)}'>🖨️ In phiếu khám</button>
                </td>
              </tr>
            `).join('') || '<tr><td colspan="7" style="text-align: center;">Chưa có hồ sơ bệnh án nào.</td></tr>'}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Khám Bệnh & Kê Đơn -->
    <div id="modal-examine" class="modal-overlay ${targetAptId ? 'open' : ''}">
      <div class="modal-content" style="max-width: 700px;">
        <div class="modal-header">
          <h3>Thực hiện Khám bệnh & Lập Bệnh án</h3>
          <button class="modal-close" id="modal-examine-close">&times;</button>
        </div>
        <form id="form-create-record">
          <div class="modal-body">
            <div id="record-form-error" style="display: none; background: #fee2e2; color: #dc2626; padding: 12px; border-radius: 8px; margin-bottom: 14px; font-size: 13px;"></div>

            <div class="form-group">
              <label>Lượt khám tiếp nhận (Đang chờ) *</label>
              <select id="rec-apt" class="form-control" required>
                <option value="">-- Chọn bệnh nhân đang chờ khám --</option>
                ${inProgressApts.map(a => `
                  <option value="${a.id}" data-pat="${a.patient}" data-doc="${a.doctor}" ${String(a.id) === targetAptId ? 'selected' : ''}>
                    [${a.code}] ${a.patient_details?.full_name} - BS: ${a.doctor_details?.full_name} (${a.reason})
                  </option>
                `).join('')}
              </select>
            </div>

            <div class="form-group">
              <label>Triệu chứng lâm sàng *</label>
              <textarea id="rec-symptoms" class="form-control" rows="2" required placeholder="Ghi nhận triệu chứng, mô tả của bệnh nhân..."></textarea>
            </div>

            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; background: #f8fafc; padding: 14px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 16px;">
              <div>
                <label style="font-size: 11px;">Huyết áp</label>
                <input type="text" id="rec-bp" class="form-control" placeholder="120/80">
              </div>
              <div>
                <label style="font-size: 11px;">Mạch (bpm)</label>
                <input type="text" id="rec-pulse" class="form-control" placeholder="75">
              </div>
              <div>
                <label style="font-size: 11px;">Nhiệt độ (°C)</label>
                <input type="text" id="rec-temp" class="form-control" placeholder="36.8">
              </div>
              <div>
                <label style="font-size: 11px;">Cân nặng (kg)</label>
                <input type="text" id="rec-weight" class="form-control" placeholder="65">
              </div>
            </div>

            <div class="form-group">
              <label>Chẩn đoán xác định *</label>
              <input type="text" id="rec-diagnosis" class="form-control" required placeholder="Tên bệnh lý theo mã ICD-10...">
            </div>

            <div class="form-group">
              <label>Phác đồ & Hướng điều trị *</label>
              <textarea id="rec-treatment" class="form-control" rows="2" required placeholder="Nghỉ ngơi, ăn uống, theo dõi..."></textarea>
            </div>

            <div class="form-group">
              <label>Kê đơn thuốc điện tử (Tên thuốc, số lượng, cách dùng)</label>
              <textarea id="rec-prescription" class="form-control" rows="3" placeholder="Ví dụ: 1. Paracetamol 500mg x 10 viên (Uống 1v khi sốt > 38.5)\n2. Vitamin C 500mg x 10 viên (Uống 1v/ngày sau ăn)"></textarea>
            </div>

            <div class="form-group">
              <label>Lời dặn của Bác sĩ</label>
              <input type="text" id="rec-notes" class="form-control" placeholder="Tái khám sau 7 ngày nếu không đỡ...">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" id="btn-cancel-examine">Hủy</button>
            <button type="submit" class="btn btn-primary" id="btn-save-record">Hoàn thành khám & Lưu bệnh án</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Bản In Phiếu Khám Bệnh -->
    <div id="modal-print" class="modal-overlay">
      <div class="modal-content" style="max-width: 650px;">
        <div class="modal-header">
          <h3>Phiếu Khám Bệnh & Đơn Thuốc</h3>
          <button class="modal-close" id="modal-print-close">&times;</button>
        </div>
        <div class="modal-body" id="print-content" style="background: white; color: black; line-height: 1.6;">
          <!-- Nạp động qua JS -->
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" id="btn-close-print">Đóng</button>
          <button type="button" class="btn btn-primary" onclick="window.print()">🖨️ In ra máy in</button>
        </div>
      </div>
    </div>
  `;
}

export function initMedicalRecordsEvents() {
  const modalExamine = document.getElementById('modal-examine');
  const btnOpenExamine = document.getElementById('btn-open-examine');
  const btnCloseExamine = document.getElementById('modal-examine-close');
  const btnCancelExamine = document.getElementById('btn-cancel-examine');
  const formRecord = document.getElementById('form-create-record');

  const modalPrint = document.getElementById('modal-print');
  const btnClosePrint = document.getElementById('modal-print-close');
  const btnClosePrint2 = document.getElementById('btn-close-print');

  if (btnOpenExamine) btnOpenExamine.onclick = () => modalExamine.classList.add('open');
  if (btnCloseExamine) btnCloseExamine.onclick = () => modalExamine.classList.remove('open');
  if (btnCancelExamine) btnCancelExamine.onclick = () => modalExamine.classList.remove('open');

  if (btnClosePrint) btnClosePrint.onclick = () => modalPrint.classList.remove('open');
  if (btnClosePrint2) btnClosePrint2.onclick = () => modalPrint.classList.remove('open');

  // Print view
  document.querySelectorAll('.btn-view-print').forEach(btn => {
    btn.onclick = () => {
      const r = JSON.parse(btn.dataset.record);
      const printBox = document.getElementById('print-content');
      printBox.innerHTML = `
        <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 16px;">
          <h2 style="font-size: 20px; font-weight: bold; text-transform: uppercase;">PHÒNG KHÁM ĐA KHOA PHÚC AN</h2>
          <p style="font-size: 12px;">Địa chỉ: 123 Cầu Giấy, Hà Nội — Hotline: 1900 6868</p>
          <h3 style="font-size: 16px; font-weight: bold; margin-top: 8px;">PHIẾU KHÁM BỆNH VÀ ĐƠN THUỐC</h3>
          <p style="font-size: 12px;">Mã bệnh án: <strong>${r.code}</strong> — Ngày: ${new Date(r.created_at).toLocaleDateString('vi-VN')}</p>
        </div>

        <div style="margin-bottom: 14px;">
          <p><strong>Họ và tên bệnh nhân:</strong> ${r.patient_details?.full_name} (${r.patient_details?.gender === 'MALE' ? 'Nam' : 'Nữ'}) — Ngày sinh: ${r.patient_details?.date_of_birth}</p>
          <p><strong>Số điện thoại:</strong> ${r.patient_details?.phone} — <strong>Địa chỉ:</strong> ${r.patient_details?.address}</p>
        </div>

        <div style="border: 1px solid #ccc; padding: 12px; border-radius: 6px; margin-bottom: 14px;">
          <p><strong>Triệu chứng:</strong> ${r.symptoms}</p>
          <p><strong>Chẩn đoán:</strong> <span style="font-size: 15px; font-weight: bold;">${r.diagnosis}</span></p>
          <p><strong>Phác đồ điều trị:</strong> ${r.treatment_plan}</p>
        </div>

        <div style="margin-bottom: 14px;">
          <h4 style="font-weight: bold; text-decoration: underline; margin-bottom: 6px;">ĐƠN THUỐC ĐIỆN TỬ:</h4>
          <pre style="white-space: pre-wrap; font-family: inherit; font-size: 13px; background: #f8fafc; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">${Array.isArray(r.prescription) ? r.prescription.map(p => `- ${p.medicine}: ${p.quantity} (${p.dosage})`).join('\n') : r.prescription}</pre>
        </div>

        <p><strong>Lời dặn bác sĩ:</strong> ${r.doctor_notes || 'Uống thuốc đúng liều lượng theo đơn.'}</p>

        <div style="display: flex; justify-content: space-between; margin-top: 30px; text-align: center;">
          <div>
            <p style="font-size: 12px;">Bệnh nhân / Người nhà</p>
            <p style="margin-top: 40px;">(Ký và ghi rõ họ tên)</p>
          </div>
          <div>
            <p style="font-size: 12px;">Bác sĩ khám bệnh</p>
            <p style="font-weight: bold; margin-top: 40px;">${r.doctor_details?.full_name || 'Bác sĩ điều trị'}</p>
          </div>
        </div>
      `;
      modalPrint.classList.add('open');
    };
  });

  // Submit record
  if (formRecord) {
    formRecord.onsubmit = async (e) => {
      e.preventDefault();
      const errBox = document.getElementById('record-form-error');
      errBox.style.display = 'none';

      const aptSelect = document.getElementById('rec-apt');
      const selectedOption = aptSelect.options[aptSelect.selectedIndex];

      const data = {
        appointment: aptSelect.value,
        patient: selectedOption.dataset.pat,
        doctor: selectedOption.dataset.doc,
        symptoms: document.getElementById('rec-symptoms').value.trim(),
        vital_signs: {
          blood_pressure: document.getElementById('rec-bp').value.trim(),
          pulse: document.getElementById('rec-pulse').value.trim(),
          temperature: document.getElementById('rec-temp').value.trim(),
          weight: document.getElementById('rec-weight').value.trim()
        },
        diagnosis: document.getElementById('rec-diagnosis').value.trim(),
        treatment_plan: document.getElementById('rec-treatment').value.trim(),
        prescription: document.getElementById('rec-prescription').value.trim(),
        doctor_notes: document.getElementById('rec-notes').value.trim()
      };

      try {
        const btnSave = document.getElementById('btn-save-record');
        btnSave.disabled = true;
        btnSave.innerText = 'Đang lưu bệnh án...';
        await api.post('/medical-records/', data);
        modalExamine.classList.remove('open');
        window.location.hash = '#/medical-records';
        window.location.reload();
      } catch (err) {
        errBox.innerText = err.message || 'Lỗi khi lưu bệnh án.';
        errBox.style.display = 'block';
      } finally {
        const btnSave = document.getElementById('btn-save-record');
        btnSave.disabled = false;
        btnSave.innerText = 'Hoàn thành khám & Lưu bệnh án';
      }
    };
  }
}
