# base image
FROM postgres:11.2-alpine

WORKDIR /usr/src/app/postgres

# run init scripts on start up
COPY ./init/jeopardy201908021145.sql /docker-entrypoint-initdb.d
COPY ./init/create.sql /docker-entrypoint-initdb.d
