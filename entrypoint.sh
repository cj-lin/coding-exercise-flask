#!/bin/bash

until mysql -e '\q'; do
    sleep 1
done

if [ "$(mysql -Ne "SELECT count(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'myapi'")" == "0" ]; then
    flask db migrate
    flask db upgrade
    flask myapi init
fi

exec "$@"
