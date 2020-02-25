FROM ubuntu:18.04
MAINTAINER Anil <anilsalunke110@gmail.com>
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
 apt-get -y install supervisor wget curl git apache2 && \ 
EXPOSE 80
RUN a2enmod rewrite
