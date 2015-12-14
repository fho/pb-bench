#!/bin/sh

tar Jxf apache.tar.xz
apache_path="$(pwd)/apache"
quoted_apache_path=$(echo $apache_path| sed 's/\//\\\//g')
sed -i "s/<path>/$quoted_apache_path/g" "$apache_path/conf/httpd.conf"
sed -i "s/<path>/$quoted_apache_path/g" "$apache_path/bin/apachectl"
sed -i "s/<path>/$quoted_apache_path/g" "$apache_path/include/ap_config_layout.h"
