FROM postgres:15.2

# init.sqlをコンテナの/docker-entrypoint-init.db.dと共有
COPY containers/mysql/init.sql /docker-entrypoint-initdb.d
