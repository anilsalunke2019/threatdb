FROM ubuntu:18.04
MAINTAINER Anil <anilsalunke110@gmail.com>
RUN apt-get update && \
    apt-get install -y supervisor wget curl git apache2 && \
    apt-get install -y php7.2 php7.2-cli php7.2-common && \
    apt-get install -y  php7.2-curl  php7.2-gd php7.2-imagick php7.2-intl php7.2-json php7.2-mbstring php7.2-mcrypt  php7.2-mysqli php7.2-mysqlnd php7.2-PDO php7.2-pdo_mysql php7.2-xml  php7.2-xmlrpc php7.2-xsl php7.2-Zend OPcache php7.2-zip php7.2-zlib && \
   RUN a2enmod rewrite
