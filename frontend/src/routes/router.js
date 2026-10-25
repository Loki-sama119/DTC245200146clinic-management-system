import { api } from '../services/api.js';
import { renderSidebar } from '../components/Sidebar.js';
import { renderNavbar } from '../components/Navbar.js';
import { renderLoginPage, initLoginEvents } from '../pages/auth/login.js';
import { renderDashboardPage } from '../pages/dashboard/dashboard.js';
import { renderPatientsPage, initPatientsEvents } from '../pages/patients/patients.js';
import { renderDoctorsPage, initDoctorsEvents } from '../pages/doctors/doctors.js';
import { renderSpecialtiesPage, initSpecialtiesEvents } from '../pages/specialties/specialties.js';
import { renderAppointmentsPage, initAppointmentsEvents } from '../pages/appointments/appointments.js';
import { renderMedicalRecordsPage, initMedicalRecordsEvents } from '../pages/medical-records/medical-records.js';
import { renderReportsPage, initReportsEvents } from '../pages/reports/reports.js';
import { renderUsersPage, initUsersEvents } from '../pages/users/users.js';

export async function navigate() {
  const app = document.getElementById('app');
  let hash = window.location.hash || '#/dashboard';
  const cleanPath = hash.split('?')[0];

  // Auth Guard
  if (!api.isAuthenticated()) {
    if (cleanPath !== '#/login') {
      window.location.hash = '#/login';
      return;
    }
    app.innerHTML = renderLoginPage();
    initLoginEvents();
    return;
  }

  // Nếu đã đăng nhập mà vào #/login thì đưa về dashboard
  if (cleanPath === '#/login') {
    window.location.hash = '#/dashboard';
    return;
  }

  let pageContent = '';
  let pageTitle = 'Phòng khám Phúc An';
  let initEvents = null;

  switch (cleanPath) {
    case '#/dashboard':
      pageTitle = 'Bảng điều khiển Tổng quan';
      pageContent = await renderDashboardPage();
      break;
    case '#/patients':
      pageTitle = 'Quản lý Hồ sơ Bệnh nhân';
      pageContent = await renderPatientsPage();
      initEvents = initPatientsEvents;
      break;
    case '#/doctors':
      pageTitle = 'Danh mục Bác sĩ';
      pageContent = await renderDoctorsPage();
      initEvents = initDoctorsEvents;
      break;
    case '#/specialties':
      pageTitle = 'Quản lý Chuyên khoa';
      pageContent = await renderSpecialtiesPage();
      initEvents = initSpecialtiesEvents;
      break;
    case '#/appointments':
      pageTitle = 'Quản lý Lịch hẹn Khám';
      pageContent = await renderAppointmentsPage();
      initEvents = initAppointmentsEvents;
      break;
    case '#/medical-records':
      pageTitle = 'Hồ sơ Bệnh án & Đơn thuốc';
      pageContent = await renderMedicalRecordsPage();
      initEvents = initMedicalRecordsEvents;
      break;
    case '#/users':
      pageTitle = 'Quản lý Nhân viên & Phân quyền';
      pageContent = await renderUsersPage();
      initEvents = initUsersEvents;
      break;
    case '#/reports':
      pageTitle = 'Báo cáo & Thống kê Y tế';
      pageContent = await renderReportsPage();
      initEvents = initReportsEvents;
      break;
    default:
      pageTitle = 'Bảng điều khiển';
      pageContent = await renderDashboardPage();
  }

  app.innerHTML = `
    <div id="app-layout">
      ${renderSidebar(cleanPath)}
      <div class="main-wrapper">
        ${renderNavbar(pageTitle)}
        ${pageContent}
      </div>
    </div>
  `;

  // Gắn sự kiện nút Logout trên sidebar và navbar
  const logoutBtn = document.getElementById('btn-logout');
  if (logoutBtn) {
    logoutBtn.onclick = () => api.logout();
  }
  const topLogoutBtn = document.getElementById('btn-top-logout');
  if (topLogoutBtn) {
    topLogoutBtn.onclick = () => api.logout();
  }

  // Khởi tạo sự kiện cho trang hiện tại
  if (initEvents) {
    initEvents();
  }
}
