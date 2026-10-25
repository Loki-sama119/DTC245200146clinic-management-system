-- ==============================================================================
-- DATABASE INITIALIZATION SCRIPT — POSTGRESQL 16
-- Học phần: Triển khai và Quản trị Hệ thống Phần mềm
-- ==============================================================================

-- Thiết lập Timezone chuẩn Việt Nam
SET timezone = 'Asia/Ho_Chi_Minh';
ALTER DATABASE clinic_db SET timezone TO 'Asia/Ho_Chi_Minh';

-- Kích hoạt các Extensions cần thiết
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Gán quyền cho user quản trị ứng dụng
GRANT ALL PRIVILEGES ON DATABASE clinic_db TO clinic_user;
GRANT ALL ON SCHEMA public TO clinic_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO clinic_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO clinic_user;
