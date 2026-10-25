import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import time, timedelta
from apps.specialties.models import Specialty
from apps.doctors.models import Doctor
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.medical_records.models import MedicalRecord
from apps.audit.models import AuditLog

User = get_user_model()

class Command(BaseCommand):
    help = 'Khởi tạo dữ liệu mẫu phong phú và tài khoản demo cho phòng khám'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('==> Bắt đầu nạp dữ liệu mẫu cho Clinic Management System...'))

        admin_pass = os.environ.get('ADMIN_PASSWORD', 'Admin@123')
        doc_pass = os.environ.get('DOCTOR_PASSWORD', 'Doc@123')
        rec_pass = os.environ.get('RECEPTIONIST_PASSWORD', 'Rec@123')

        # 1. Tạo Tài khoản
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@phucanclinic.vn',
                'first_name': 'Văn Thắng',
                'last_name': 'Nguyễn',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'phone': '0912345678'
            }
        )
        admin_user.set_password(admin_pass)
        admin_user.save()

        doc_user_1, _ = User.objects.get_or_create(
            username='doctor_thang',
            defaults={
                'email': 'thang.nguyen@phucanclinic.vn',
                'first_name': 'Văn Thắng',
                'last_name': 'BS.CKII Nguyễn',
                'role': User.Role.DOCTOR,
                'phone': '0988776655'
            }
        )
        doc_user_1.set_password(doc_pass)
        doc_user_1.save()

        doc_user_2, _ = User.objects.get_or_create(
            username='doctor_lan',
            defaults={
                'email': 'lan.tran@phucanclinic.vn',
                'first_name': 'Thị Lan',
                'last_name': 'ThS.BS Trần',
                'role': User.Role.DOCTOR,
                'phone': '0977665544'
            }
        )
        doc_user_2.set_password(doc_pass)
        doc_user_2.save()

        rec_user, _ = User.objects.get_or_create(
            username='receptionist',
            defaults={
                'email': 'receptionist@phucanclinic.vn',
                'first_name': 'Thu Hương',
                'last_name': 'Lê',
                'role': User.Role.RECEPTIONIST,
                'phone': '0933221100'
            }
        )
        rec_user.set_password(rec_pass)
        rec_user.save()

        # 2. Tạo Chuyên khoa
        specs_data = [
            ("CK-NOI", "Khoa Nội Tổng Quát", "Khám, chẩn đoán và điều trị bệnh lý nội khoa, tim mạch, tiêu hóa"),
            ("CK-NHI", "Khoa Nhi", "Chăm sóc sức khỏe, tiêm chủng và điều trị bệnh lý cho trẻ nhỏ"),
            ("CK-TMH", "Khoa Tai Mũi Họng", "Nội soi, điều trị viêm xoang, viêm họng, viêm amidan"),
            ("CK-NGOAI", "Khoa Ngoại Tổng Quát", "Tiểu phẫu, sơ cứu vết thương, tư vấn can thiệp ngoại khoa"),
            ("CK-MAT", "Khoa Mắt", "Khám tật khúc xạ, đo thị lực, điều trị bệnh lý về mắt")
        ]
        specialties = {}
        for code, name, desc in specs_data:
            s, _ = Specialty.objects.get_or_create(code=code, defaults={'name': name, 'description': desc})
            specialties[code] = s

        # 3. Tạo Bác sĩ
        doc1, _ = Doctor.objects.get_or_create(
            code="BS-1001",
            defaults={
                'user': doc_user_1,
                'specialty': specialties["CK-NOI"],
                'room_number': "Phòng 102 - Tầng 1",
                'phone': "0988776655",
                'email': "thang.nguyen@phucanclinic.vn",
                'consultation_fee': 200000,
                'bio': "Hơn 15 năm kinh nghiệm chẩn đoán tim mạch và nội khoa tổng quát."
            }
        )

        doc2, _ = Doctor.objects.get_or_create(
            code="BS-1002",
            defaults={
                'user': doc_user_2,
                'specialty': specialties["CK-NHI"],
                'room_number': "Phòng 205 - Tầng 2",
                'phone': "0977665544",
                'email': "lan.tran@phucanclinic.vn",
                'consultation_fee': 180000,
                'bio': "Tốt nghiệp ĐH Y Hà Nội, chuyên gia tâm lý và bệnh lý nhi khoa."
            }
        )

        # 4. Tạo Bệnh nhân
        patients_data = [
            ("BN-10001", "Trần Đình Trọng", "1990-05-12", "MALE", "0912111222", "Quận Cầu Giấy, Hà Nội", "O+"),
            ("BN-10002", "Phạm Thị Ngọc Ánh", "1995-08-24", "FEMALE", "0982333444", "Quận Đống Đa, Hà Nội", "A+"),
            ("BN-10003", "Vũ Hoàng Nam", "2018-03-15", "MALE", "0973555666", "Quận Ba Đình, Hà Nội", "B+"),
            ("BN-10004", "Hoàng Thu Thủy", "1988-11-09", "FEMALE", "0964777888", "Quận Thanh Xuân, Hà Nội", "AB+"),
            ("BN-10005", "Đỗ Minh Quân", "2001-07-02", "MALE", "0945999000", "Quận Hoàn Kiếm, Hà Nội", "O+")
        ]
        patients = []
        for code, name, dob, gender, phone, addr, blood in patients_data:
            p, _ = Patient.objects.get_or_create(
                code=code,
                defaults={
                    'full_name': name,
                    'date_of_birth': dob,
                    'gender': gender,
                    'phone': phone,
                    'address': addr,
                    'blood_type': blood
                }
            )
            patients.append(p)

        # 5. Tạo Lịch hẹn
        today = timezone.localdate()
        apt1, _ = Appointment.objects.get_or_create(
            code="LH-50001",
            defaults={
                'patient': patients[0],
                'doctor': doc1,
                'specialty': doc1.specialty,
                'appointment_date': today,
                'start_time': time(8, 30),
                'end_time': time(9, 0),
                'status': Appointment.Status.COMPLETED,
                'reason': "Đau tức ngực và mệt mỏi khi vận động mạnh",
                'created_by': rec_user
            }
        )

        apt2, _ = Appointment.objects.get_or_create(
            code="LH-50002",
            defaults={
                'patient': patients[1],
                'doctor': doc1,
                'specialty': doc1.specialty,
                'appointment_date': today,
                'start_time': time(9, 30),
                'end_time': time(10, 0),
                'status': Appointment.Status.IN_PROGRESS,
                'reason': "Tái khám theo dõi huyết áp định kỳ",
                'created_by': rec_user
            }
        )

        apt3, _ = Appointment.objects.get_or_create(
            code="LH-50003",
            defaults={
                'patient': patients[2],
                'doctor': doc2,
                'specialty': doc2.specialty,
                'appointment_date': today,
                'start_time': time(10, 0),
                'end_time': time(10, 30),
                'status': Appointment.Status.CONFIRMED,
                'reason': "Ho sốt 2 ngày, biếng ăn",
                'created_by': rec_user
            }
        )

        apt4, _ = Appointment.objects.get_or_create(
            code="LH-50004",
            defaults={
                'patient': patients[3],
                'doctor': doc1,
                'specialty': doc1.specialty,
                'appointment_date': today + timedelta(days=1),
                'start_time': time(14, 0),
                'end_time': time(14, 30),
                'status': Appointment.Status.PENDING,
                'reason': "Khám sức khỏe tổng quát",
                'created_by': rec_user
            }
        )

        # 6. Tạo Bệnh án cho lịch hẹn COMPLETED
        MedicalRecord.objects.get_or_create(
            code="BA-90001",
            defaults={
                'appointment': apt1,
                'patient': patients[0],
                'doctor': doc1,
                'symptoms': "Khó thở nhẹ, tức ngực trái khi leo cầu thang, mạch 85 bpm",
                'vital_signs': {
                    "blood_pressure": "135/85 mmHg",
                    "pulse": "85 bpm",
                    "temperature": "36.8 C",
                    "weight": "68 kg"
                },
                'diagnosis': "Tăng huyết áp giai đoạn 1, nghi ngờ thiếu máu cơ tim cục bộ",
                'treatment_plan': "Nghỉ ngơi, giảm ăn mặn, tập thể dục nhẹ, dùng thuốc theo đơn và tái khám sau 2 tuần.",
                'prescription': [
                    {"medicine": "Amlodipine 5mg", "quantity": "30 viên", "dosage": "Uống 1 viên vào buổi sáng sau ăn"},
                    {"medicine": "Aspirin 81mg", "quantity": "30 viên", "dosage": "Uống 1 viên vào buổi trưa sau ăn"}
                ],
                'doctor_notes': "Nếu có cơn đau thắt ngực dữ dội cần vào viện cấp cứu ngay.",
                'follow_up_date': today + timedelta(days=14)
            }
        )

        # 7. Ghi Audit Log mẫu
        AuditLog.objects.create(
            user=admin_user,
            action="SYSTEM_INIT",
            model_name="System",
            details="Khởi tạo thành công CSDL và nạp dữ liệu mẫu ban đầu."
        )

        self.stdout.write(self.style.SUCCESS('==> Hoàn tất nạp dữ liệu mẫu thành công 100%!'))
