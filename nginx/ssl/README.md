# HƯỚNG DẪN CẤU HÌNH SSL/TLS CHO NGINX

Môi trường demo tại phòng Lab/Máy ảo hiện đang sử dụng giao thức HTTP (cổng 80) nhằm phục vụ chấm thi và kết nối nội bộ nhanh chóng.

## Để kích hoạt HTTPS trên môi trường Production:
1. Đặt chứng chỉ SSL (`clinic.crt`) và khóa riêng (`clinic.key`) vào thư mục `nginx/ssl/`.
2. Mở file `nginx/conf.d/default.conf` và thêm cấu hình:
```nginx
listen 443 ssl http2;
ssl_certificate /etc/nginx/ssl/clinic.crt;
ssl_certificate_key /etc/nginx/ssl/clinic.key;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
```
3. Mở cổng 443 trên firewall UFW: `sudo ufw allow 443/tcp`.
