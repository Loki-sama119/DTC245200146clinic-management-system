-- ==========================================================
-- CLINIC MANAGEMENT SYSTEM — SAMPLE SEED SQL DATA (REFERENCE)
-- Thư viện dữ liệu mẫu tham chiếu chuẩn cho PostgreSQL 16
-- ==========================================================

-- 1. Chuyên khoa
INSERT INTO specialties (code, name, description, is_active, created_at, updated_at)
VALUES 
('CK-NOI', 'Khoa Nội Tổng Quát', 'Khám, chẩn đoán và điều trị bệnh lý nội khoa, tim mạch, tiêu hóa', true, NOW(), NOW()),
('CK-NHI', 'Khoa Nhi', 'Chăm sóc sức khỏe, tiêm chủng và điều trị bệnh lý cho trẻ nhỏ', true, NOW(), NOW()),
('CK-TMH', 'Khoa Tai Mũi Họng', 'Nội soi, điều trị viêm xoang, viêm họng, viêm amidan', true, NOW(), NOW()),
('CK-NGOAI', 'Khoa Ngoại Tổng Quát', 'Tiểu phẫu, sơ cứu vết thương, tư vấn can thiệp ngoại khoa', true, NOW(), NOW()),
('CK-MAT', 'Khoa Mắt', 'Khám tật khúc xạ, đo thị lực, điều trị bệnh lý về mắt', true, NOW(), NOW())
ON CONFLICT (code) DO NOTHING;
