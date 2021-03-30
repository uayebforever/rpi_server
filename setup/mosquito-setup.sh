# This is for debian buster based builds!
# Based on https://hackaday.com/2016/05/09/minimal-mqtt-building-a-broker/

curl -O http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
apt-key add mosquitto-repo.gpg.key
rm mosquitto-repo.gpg.key
cd /etc/apt/sources.list.d/ || exit 1
curl -O http://repo.mosquitto.org/debian/mosquitto-jessie.list
apt-get update
apt-get install mosquitto mosquitto-clients
