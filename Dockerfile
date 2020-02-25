FROM ubuntu:18.04
MAINTAINER Anil <anilsalunke110@gmail.com>
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
 apt-get -y install supervisor wget curl git apache2 zip unzip php7.2 php7.2-curl  php7.2-gd php7.2-json php7.2-mbstring php7.2-mysqli && \
 echo "ServerName localhost" >> /etc/apache2/apache2.conf && rm /var/www/html/index.html

ADD uploads/start-apache2.sh /start-apache2.sh
RUN chmod 755 /*.sh
ADD uploads/supervisord-apache2.conf /etc/supervisor/conf.d/supervisord-apache2.conf
ADD uploads/apache_default /etc/apache2/sites-available/000-default.conf
RUN a2enmod rewrite

ENV PHP_UPLOAD_MAX_FILESIZE 10M
ENV PHP_POST_MAX_SIZE 10M

RUN wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
RUN cp wp-cli.phar /usr/local/bin/wp && \
    chmod +x /usr/local/bin/wp

EXPOSE 80
VOLUME  [ "/var/www/html" ]
