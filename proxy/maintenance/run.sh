#!/bin/sh

echo "Starting Nginx web server for maintenance mode..."

exec nginx -g 'daemon off;'