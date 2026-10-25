# ==============================================================================
# CLINIC MANAGEMENT FRONTEND DOCKERFILE — NGINX ALPINE
# ==============================================================================

FROM nginx:1.25-alpine

# Copy cấu hình Nginx riêng cho Frontend container
RUN rm -rf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy toàn bộ mã nguồn Frontend tĩnh vào thư mục phục vụ
COPY . /usr/share/nginx/html

# Hardening: Phân quyền an toàn
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
