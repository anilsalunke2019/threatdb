FROM ubuntu:18.04
MAINTAINER Anil <anilsalunke110@gmail.com>
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
 apt-get -y install subversion wget curl git zip unzip apache2 nano python3.6 python3-pip php7.2 php7.2-curl  php7.2-gd php7.2-json php7.2-mbstring php7.2-mysqli && \
 echo "ServerName localhost" >> /etc/apache2/apache2.conf && echo "vm.nr_hugepages=128" >> /etc/sysctl.conf && rm /var/www/html/index.html
ADD uploads/run.sh /run.sh
ADD uploads/requirements.txt /requirements.txt
RUN chmod 755 /*.sh
ENV PHP_UPLOAD_MAX_FILESIZE 10M
ENV PHP_POST_MAX_SIZE 10M
EXPOSE 80
VOLUME  [ "/var/www/html" ]
CMD ["/run.sh"]
