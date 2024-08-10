FROM nginx:stable

COPY index.html /var/www/index.html
COPY revsite1.js /var/www/revsite1.js
COPY revsite1.wasm /var/www/revsite1.wasm

# add other files as needed

COPY nginx.conf /etc/nginx/conf.d/default.conf
