#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres... " $DB_HOST $DB_PORT

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

alembic upgrade head

exec "$@"
