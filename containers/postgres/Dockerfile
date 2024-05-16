FROM postgres:16.2

# init.sqlをコンテナの/docker-entrypoint-init.db.dと共有
COPY containers/postgres/init.sql /docker-entrypoint-initdb.d
