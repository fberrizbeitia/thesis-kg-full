FROM httpd:2.4

COPY apache-vhost.conf /usr/local/apache2/conf/extra/httpd-default.conf
RUN echo "Include /usr/local/apache2/conf/extra/httpd-default.conf" >> /usr/local/apache2/conf/httpd.conf

