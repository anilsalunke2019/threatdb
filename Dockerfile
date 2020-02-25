FROM ubuntu:18.04
MAINTAINER Anil <anilsalunke110@gmail.com>
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
 apt-get -y install wget curl git apache2 && \
 echo "test" > /var/www/

EXPOSE 80
RUN a2enmod rewrite
