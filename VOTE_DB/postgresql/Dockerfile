FROM postgres:11.5-alpine
ENV POSTGRES_USER idugUser
ENV POSTGRES_PASSWORD idugPwd
ENV POSTGRES_DB vote_db
COPY init.sql /docker-entrypoint-initdb.d/