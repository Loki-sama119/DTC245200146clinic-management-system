# ==============================================================================
# CLINIC MANAGEMENT NGINX REVERSE PROXY DOCKERFILE
# ==============================================================================

FROM nginx:1.25-alpine

# Gỡ cấu hình mặc định
RUN rm -rf /etc/nginx/conf.d/default.conf /etc/nginx/nginx.conf

# Sao chép cấu hình tối ưu và bảo mật
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
