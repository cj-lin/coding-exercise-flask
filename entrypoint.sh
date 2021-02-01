#!/bin/bash

until mysql -e '\q'; do
    sleep 1
done

flask db init
flask myapi init
flask db migrate
flask db upgrade

exec "$@"
