#!/bin/bash
cd /var/www/html/; svn co --non-interactive  --username anilleo --password alpha@1234 http://svn.leosys.net/p2pword .;find  -type d -exec chmod 755 {} + ;find -type f -exec chmod 644 {} +;chown -R www-data:www-data *;
exec supervisord -n
