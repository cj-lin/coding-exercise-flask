#!/bin/bash

until mysql -h db -e '\q'; do
    sleep 1
done

if [ "$(mysql -Nh db -e "SELECT count(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'myapi'")" == "0" ]; then
    flask db upgrade
    flask myapi init
fi

exec "$@"
