import { api } from '../services/api.js';

export function renderNavbar(title = 'Bảng điều khiển') {
  const user = api.getUser();
  const today = new Date().toLocaleDateString('vi-VN', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  const roleName = {
    'ADMIN': 'Quản trị viên',
    'DOCTOR': 'Bác sĩ',
    'RECEPTIONIST': 'Lễ tân'
  }[user?.role] || user?.role || '';

  return `
    <header class="top-navbar">
      <div class="navbar-brand">
        <span>${title}</span>
      </div>
      <div class="navbar-actions">
        <span style="font-size: 13px; color: #64748b;">📅 ${today}</span>
        <span class="badge badge-confirmed">🟢 Máy chủ: Hoạt động</span>
        <div style="display: flex; align-items: center; gap: 8px; margin-left: 12px; border-left: 1px solid #e2e8f0; padding-left: 16px;">
          <span style="font-size: 13px; font-weight: 600; color: #1e293b;">👤 ${user ? ((user.last_name ? user.last_name + ' ' : '') + (user.first_name || user.username)) : ''} (${roleName})</span>
          <button id="btn-top-logout" class="btn btn-danger btn-sm" style="font-weight: 600; cursor: pointer;">Đăng xuất 🚪</button>
        </div>
      </div>
    </header>
  `;
}
