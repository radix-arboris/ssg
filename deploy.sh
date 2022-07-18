#!/bin/bash
systemctl stop ssg
git clean
git reset --hard HEAD
git pull
chmod -R 777 $PWD
chown -R www-data:www-data $PWD
systemctl start ssg