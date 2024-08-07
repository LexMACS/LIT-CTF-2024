FROM nginx:stable

COPY index.html /var/www/index.html
COPY assets /var/www/assets
COPY vite.svg /var/www/vite.svg

# add other files as needed

COPY nginx.conf /etc/nginx/conf.d/default.conf
