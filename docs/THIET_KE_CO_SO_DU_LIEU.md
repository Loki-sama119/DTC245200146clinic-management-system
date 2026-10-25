# THIẾT KẾ CƠ SỞ DỮ LIỆU POSTGRESQL (DATABASE DESIGN & ERD)

- **Hệ quản trị CSDL**: PostgreSQL 16
- **Database**: `clinic_db`
- **Timezone**: `Asia/Ho_Chi_Minh`

---

## 1. SƠ ĐỒ THỰC THỂ QUAN HỆ (ERD)

```mermaid
erDiagram
    USERS ||--o{ DOCTORS : "1:1 link"
    USERS ||--o{ APPOINTMENTS : "created_by"
    USERS ||--o{ AUDIT_LOGS : "logs action"
    SPECIALTIES ||--o{ DOCTORS : "specialty_id"
    SPECIALTIES ||--o{ APPOINTMENTS : "specialty_id"
    DOCTORS ||--o{ APPOINTMENTS : "doctor_id"
    DOCTORS ||--o{ MEDICAL_RECORDS : "doctor_id"
    PATIENTS ||--o{ APPOINTMENTS : "patient_id"
    PATIENTS ||--o{ MEDICAL_RECORDS : "patient_id"
    APPOINTMENTS ||--o| MEDICAL_RECORDS : "appointment_id (1:1)"

    USERS {
        int id PK
        string username UK
        string password
        string role "ADMIN, DOCTOR, RECEPTIONIST"
        string phone
        boolean is_active
    }

    SPECIALTIES {
        int id PK
        string code UK
        string name UK
        text description
        boolean is_active
    }

    DOCTORS {
        int id PK
        int user_id FK
        int specialty_id FK
        string code UK
        string room_number
        decimal consultation_fee
        boolean is_active
    }

    PATIENTS {
        int id PK
        string code UK
        string full_name
        date date_of_birth
        string gender "MALE, FEMALE, OTHER"
        string phone UK
        string address
        string blood_type
        boolean is_active
    }

    APPOINTMENTS {
        int id PK
        string code UK
        int patient_id FK
        int doctor_id FK
        int specialty_id FK
        date appointment_date
        time start_time
        time end_time
        string status "PENDING, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED, NO_SHOW"
        string reason
        int created_by_id FK
    }

    MEDICAL_RECORDS {
        int id PK
        string code UK
        int appointment_id FK "UNIQUE 1:1"
        int patient_id FK
        int doctor_id FK
        text symptoms
        json vital_signs
        text diagnosis
        text treatment_plan
        json prescription
        text doctor_notes
    }

    AUDIT_LOGS {
        int id PK
        int user_id FK
        string action
        string model_name
        string object_id
        string ip_address
        text details
        datetime timestamp
    }
```

---

## 2. RÀNG BUỘC CHỐNG TRÙNG LỊCH (ANTI-OVERLAP INTERVAL CHECK)
Thuật toán chống trùng lịch tại tầng nghiệp vụ và cơ sở dữ liệu:
```sql
SELECT id FROM appointments
WHERE doctor_id = :new_doctor_id
  AND appointment_date = :new_date
  AND status IN ('PENDING', 'CONFIRMED', 'IN_PROGRESS')
  AND start_time < :new_end_time
  AND end_time > :new_start_time;
```
Nếu có bất kỳ bản ghi nào trùng khớp, hệ thống từ chối tạo lịch và ném ngoại lệ Validation Error.
