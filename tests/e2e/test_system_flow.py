"""
End-to-End System Flow Test via HTTP Gateway (Nginx / API Gateway)
Kiểm thử toàn trình từ cổng Nginx reverse proxy qua HTTP REST API thực tế.
"""
import pytest
import os
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost")

def test_gateway_health():
    """Kiểm tra Nginx reverse proxy định tuyến đến Health API"""
    res = requests.get(f"{BASE_URL}/api/health/", timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert data.get("status") == "healthy"
    assert data.get("database") == "healthy"

def test_login_flow():
    """Kiểm tra luồng đăng nhập cấp phát JWT Token"""
    res = requests.post(f"{BASE_URL}/api/accounts/login/", json={
        "username": "admin",
        "password": "Admin@123"
    }, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert "token" in data or "access" in data
    assert data["user"]["role"] == "ADMIN"

def test_conflict_prevention_flow():
    """Kiểm tra Nginx chặn đặt trùng lịch khám ở cấp độ API"""
    # 1. Login lễ tân
    login_res = requests.post(f"{BASE_URL}/api/accounts/login/", json={
        "username": "receptionist",
        "password": "Rec@123"
    }, timeout=5)
    token = login_res.json().get("token") or login_res.json().get("access")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Thử đặt lịch trùng vào khung giờ 08:30 - 09:00 của BS-1001 hôm nay
    from datetime import date
    today_str = date.today().isoformat()
    conflict_res = requests.post(f"{BASE_URL}/api/appointments/", json={
        "patient": 1,
        "doctor": 1,
        "appointment_date": today_str,
        "start_time": "08:30",
        "end_time": "09:00",
        "reason": "Thử nghiệm đặt trùng lịch hẹn"
    }, headers=headers, timeout=5)

    # API phải trả về HTTP 400 Bad Request
    assert conflict_res.status_code == 400
    assert "trùng" in str(conflict_res.json()).lower() or "conflict" in str(conflict_res.json()).lower()
