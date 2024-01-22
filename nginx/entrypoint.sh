#!/bin/sh

echo "Certbot entrypoint is running."

crontab scheduler.txt
crontab -l

nginx -g 'daemon off;'
