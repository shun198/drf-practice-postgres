FROM postgres:15.5

# init.sqlをコンテナの/docker-entrypoint-init.db.dと共有
COPY containers/postgres/init.sql /docker-entrypoint-initdb.d
