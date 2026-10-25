import { api } from '../services/api.js';

export function renderSidebar(currentPath) {
  const user = api.getUser();
  if (!user) return '';

  const roleDisplay = {
    'ADMIN': 'Quản trị viên',
    'DOCTOR': 'Bác sĩ chuyên khoa',
    'RECEPTIONIST': 'Lễ tân / Tiếp đón'
  }[user.role] || user.role;

  const menuItems = [
    { path: '#/dashboard', label: 'Tổng quan (Dashboard)', icon: '📊', roles: ['ADMIN', 'DOCTOR', 'RECEPTIONIST'] },
    { path: '#/appointments', label: 'Lịch hẹn khám', icon: '📅', roles: ['ADMIN', 'DOCTOR', 'RECEPTIONIST'] },
    { path: '#/patients', label: 'Hồ sơ bệnh nhân', icon: '👥', roles: ['ADMIN', 'DOCTOR', 'RECEPTIONIST'] },
    { path: '#/medical-records', label: 'Bệnh án & Đơn thuốc', icon: '🩺', roles: ['ADMIN', 'DOCTOR'] },
    { path: '#/doctors', label: 'Danh mục bác sĩ', icon: '👨‍⚕️', roles: ['ADMIN', 'RECEPTIONIST'] },
    { path: '#/specialties', label: 'Chuyên khoa', icon: '🏥', roles: ['ADMIN'] },
    { path: '#/users', label: 'Quản lý Nhân viên', icon: '🛡️', roles: ['ADMIN'] },
    { path: '#/reports', label: 'Báo cáo & Thống kê', icon: '📈', roles: ['ADMIN', 'RECEPTIONIST'] },
  ];

  const filteredItems = menuItems.filter(item => item.roles.includes(user.role));

  return `
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">🏥</div>
        <div>
          <div class="sidebar-title">PHÚC AN CLINIC</div>
          <div class="sidebar-sub">Clinic Management System</div>
        </div>
      </div>

      <ul class="sidebar-menu">
        ${filteredItems.map(item => `
          <li class="sidebar-item">
            <a href="${item.path}" class="sidebar-link ${currentPath === item.path ? 'active' : ''}">
              <span>${item.icon}</span>
              <span>${item.label}</span>
            </a>
          </li>
        `).join('')}
      </ul>

      <div class="sidebar-footer">
        <div class="user-badge">
          <div class="user-badge-name">${user.last_name || ''} ${user.first_name || user.username}</div>
          <div class="user-badge-role">${roleDisplay}</div>
        </div>
        <button id="btn-logout" class="btn btn-secondary btn-sm" title="Đăng xuất">Đăng xuất 🚪</button>
      </div>
    </aside>
  `;
}
