FROM ubuntu:18.04
MAINTAINER Anil <anilsalunke110@gmail.com>
RUN apt-get update && \
    apt-get install -y supervisor wget curl git apache2 && \
    apt-get install -y php7.2 php7.2-cli php7.2-common && \
    apt-get install -y php7.2-bcmath php7.2-bz2 php7.2-calendar php7.2-Core php7.2-ctype php7.2-curl php7.2-date php7.2-dba php7.2-dom php7.2-exif php7.2-fileinfo php7.2-filter php7.2-ftp php7.2-gd php7.2-gettext php7.2-gmp php7.2-gnupg php7.2-hash php7.2-iconv php7.2-imagick php7.2-imap php7.2-intl php7.2-json php7.2-ldap php7.2-libxml php7.2-mbstring php7.2-mcrypt php7.2-mongodb php7.2-mysqli php7.2-mysqlnd php7.2-odbc php7.2-openssl php7.2-pcntl php7.2-pcre php7.2-PDO php7.2-pdo_mysql php7.2-PDO_ODBC php7.2-pdo_pgsql php7.2-pdo_sqlite php7.2-pgsql php7.2-Phar php7.2-posix php7.2-readline php7.2-recode php7.2-Reflection php7.2-session php7.2-shmop php7.2-SimpleXML php7.2-snmp php7.2-soap php7.2-sockets php7.2-SPL php7.2-sqlite3 php7.2-standard php7.2-sysvmsg php7.2-sysvsem php7.2-sysvshm php7.2-tidy php7.2-tokenizer php7.2-wddx php7.2-xml php7.2-xmlreader php7.2-xmlrpc php7.2-xmlwriter php7.2-xsl php7.2-Zend OPcache php7.2-zip php7.2-zlib && \
   RUN a2enmod rewrite
