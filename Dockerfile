FROM ubuntu:18.04
MAINTAINER Anil <anilsalunke110@gmail.com>
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
 apt-get -y install wget curl git apache2 && \
 echo "test" > /var/www/test

EXPOSE 80
RUN a2enmod rewrite
