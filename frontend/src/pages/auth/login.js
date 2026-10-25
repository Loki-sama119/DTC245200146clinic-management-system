import { api } from '../../services/api.js';

export function renderLoginPage() {
  return `
    <div style="display: flex; align-items: center; justify-content: center; min-height: 100vh; width: 100%; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);">
      <div style="width: 100%; max-width: 440px; background: white; border-radius: 16px; padding: 36px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);">
        <div style="text-align: center; margin-bottom: 28px;">
          <div style="font-size: 40px; margin-bottom: 8px;">🏥</div>
          <h2 style="font-size: 24px; font-weight: 700; color: #0f172a;">PHÚC AN CLINIC</h2>
          <p style="font-size: 13px; color: #64748b; margin-top: 4px;">Hệ thống Quản lý Phòng khám / Bệnh viện</p>
        </div>

        <div id="login-error" style="display: none; background: #fee2e2; color: #dc2626; padding: 12px; border-radius: 8px; font-size: 13px; margin-bottom: 16px;"></div>

        <form id="form-login">
          <div class="form-group">
            <label>Tên đăng nhập</label>
            <input type="text" id="username" class="form-control" placeholder="Nhập username..." required autofocus>
          </div>

          <div class="form-group" style="margin-bottom: 24px;">
            <label>Mật khẩu</label>
            <input type="password" id="password" class="form-control" placeholder="Nhập mật khẩu..." required>
          </div>

          <button type="submit" id="btn-submit-login" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 12px; font-weight: 600;">
            Đăng nhập hệ thống ➔
          </button>
        </form>

        <div style="margin-top: 28px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
          <div style="font-size: 12px; font-weight: 600; color: #64748b; margin-bottom: 10px; text-transform: uppercase;">
            Tài khoản Demo nhanh:
          </div>
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">
            <button type="button" class="btn btn-secondary btn-sm btn-quick-login" data-user="admin" data-pass="Admin@123">
              👑 Admin
            </button>
            <button type="button" class="btn btn-secondary btn-sm btn-quick-login" data-user="doctor_thang" data-pass="Doc@123">
              👨‍⚕️ Bác sĩ
            </button>
            <button type="button" class="btn btn-secondary btn-sm btn-quick-login" data-user="receptionist" data-pass="Rec@123">
              👩‍💼 Lễ tân
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
}

export function initLoginEvents() {
  const form = document.getElementById('form-login');
  const errBox = document.getElementById('login-error');

  // Quick login buttons
  document.querySelectorAll('.btn-quick-login').forEach(btn => {
    btn.addEventListener('click', () => {
      document.getElementById('username').value = btn.dataset.user;
      document.getElementById('password').value = btn.dataset.pass;
      form.dispatchEvent(new Event('submit'));
    });
  });

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      errBox.style.display = 'none';

      const username = document.getElementById('username').value.trim();
      const password = document.getElementById('password').value;
      const btn = document.getElementById('btn-submit-login');

      try {
        btn.disabled = true;
        btn.innerText = 'Đang xử lý...';
        await api.login(username, password);
        window.location.hash = '#/dashboard';
      } catch (err) {
        errBox.innerText = err.message || 'Đăng nhập không thành công.';
        errBox.style.display = 'block';
      } finally {
        btn.disabled = false;
        btn.innerText = 'Đăng nhập hệ thống ➔';
      }
    });
  }
}
