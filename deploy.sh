#!/bin/bash
systemctl stop ssg
git config --global --add safe.directory $PWD
git config --global --add safe.user www-data
git config --global --add safe.group www-data

git fetch --all
git reset --hard origin/main

chmod -R 777 $PWD
chown -R www-data:www-data $PWD

cp server_stuff/ssg.conf /etc/nginx/sites-enabled/ssg.conf
cp server_stuff/ssg.service /etc/systemd/system/ssg.service

git pull
chmod -R 777 $PWD
chown -R www-data:www-data $PWD
systemctl start ssg