FROM nginx:latest
RUN rm -f /etc/nginx/nginx.conf && \
rm -f /etc/nginx/conf.d/default.conf
# COPY config_nginx/nginx.conf /etc/nginx/nginx.conf
# COPY config_nginx/available.conf /etc/nginx/conf.d/available.conf
# COPY config_nginx/blaclist.txt /app
# COPY config_nginx/blaclist.conf /app
WORKDIR /app
CMD ["nginx", "-g", "daemon off;"]