FROM ubuntu:18.04
MAINTAINER Anil <anilsalunke110@gmail.com>
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
 apt-get -y install wget curl git apache2 zip unzip php7.2 php7.2-curl  php7.2-gd php7.2-json php7.2-mbstring php7.2-mysqli && \
 echo "ServerName localhost" >> /etc/apache2/apache2.conf && rm /var/www/html/index.html

EXPOSE 80
RUN a2enmod rewrite
