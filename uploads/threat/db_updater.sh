#!/usr/bin/env bash

echo "Welcome to GeoLite2 City database updater"
sleep 2s
echo "Downloading database..."
URL="https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=OwnUnMrcnORi86z8&suffix=tar.gz"
wget $URL
DIR="GeoLite2*"
sleep 2s
echo "Extracting database..."
tar -xzvf geoip_download*
mv $DIR/GeoLite2-City.mmdb resource/GeoLite2-City.mmdb
rm -r $DIR
rm geoip_download*