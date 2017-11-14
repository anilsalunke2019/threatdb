FROM ubuntu:trusty
MAINTAINER Ningappa <ningappa.kamate787@gmail.com>


ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
  apt-get -y install supervisor wget curl git apache2 libapache2-mod-php5 mysql-server php5-mysql php5-curl php5-gd pwgen php-apc php5-mcrypt zip unzip  && \
  echo "ServerName localhost" >> /etc/apache2/apache2.conf && rm /var/www/html/index.html

RUN sed -i -e 's/^bind-address\s*=\s*127.0.0.1/#bind-address = 127.0.0.1/' /etc/mysql/my.cnf
RUN sed -i "s/skip-external-locking/skip-external-locking\ninnodb_use_native_aio = 0\ninnodb_buffer_pool_size = 20M\n/" /etc/mysql/my.cnf
RUN php5enmod mcrypt
RUN a2enmod rewrite

# Add image configuration and scripts
ADD uploads/start-apache2.sh /start-apache2.sh
ADD uploads/start-mysqld.sh /start-mysqld.sh
ADD uploads/run.sh /run.sh
ADD uploads/create_mysql_users.sh /create_mysql_users.sh
RUN chmod 755 /*.sh
ADD uploads/supervisord-apache2.conf /etc/supervisor/conf.d/supervisord-apache2.conf
ADD uploads/supervisord-mysqld.conf /etc/supervisor/conf.d/supervisord-mysqld.conf
ADD uploads/apache_default /etc/apache2/sites-available/000-default.conf

# Remove pre-installed database
RUN rm -rf /var/lib/mysql

#filemanager and Database admin
ADD uploads/pbn	/usr/share/pbn
RUN chmod 777 /usr/share/pbn/filemanager/config/.htusers.php && \
	echo "IncludeOptional /usr/share/pbn/apache2.conf" >> /etc/apache2/apache2.conf && \
	echo "ServerName localhost" >> /etc/apache2/apache2.conf && \
	echo "Listen 2083" >> /etc/apache2/ports.conf

#Environment variables to configure php
ENV PHP_UPLOAD_MAX_FILESIZE 10M
ENV PHP_POST_MAX_SIZE 10M

#downlaod and install wp-cli.phar
RUN wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
RUN cp wp-cli.phar /usr/local/bin/wp && \
    chmod +x /usr/local/bin/wp
#Download wordpress latest core to /var/www/html

EXPOSE 80 3306 2083 7890

VOLUME  ["/etc/mysql", "/var/lib/mysql", "/var/www/html" ]
# Add Health-check for image
# HEALTHCHECK --interval=20s --retries=3  CMD curl -f http://localhost:2083/pbn/ || exit 1

CMD ["/run.sh"]
