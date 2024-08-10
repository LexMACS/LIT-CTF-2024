FROM nginx:stable

COPY index.html /var/www/index.html
COPY revsite2.js /var/www/revsite2.js
COPY revsite2.wasm /var/www/revsite2.wasm

# add other files as needed

COPY nginx.conf /etc/nginx/conf.d/default.conf
