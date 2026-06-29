
FROM nginx:1.29.0-alpine

COPY ./web_server/nginx.conf /etc/nginx/nginx.conf
COPY ./web_server/server.conf /etc/nginx/conf.d/server.conf
COPY index.html /usr/share/nginx/html/index.html

COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 80 443

ENTRYPOINT ["./run.sh"]