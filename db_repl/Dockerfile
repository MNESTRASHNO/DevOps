FROM postgres:latest

RUN apt-get update && apt-get install -y gettext-base

RUN mkdir -p /oracle/pg_data/archive/ 
RUN chown postgres:postgres /oracle/pg_data/archive/ 

ENTRYPOINT [ "bash", "-c", "\
cat <<EOF > /etc/postgresql/postgresql.conf \n\
listen_addresses = '*' \n\
port = ${DB_REPL_PORT} \n\
EOF\n\
rm -rf /var/lib/postgresql/data/* \n\
until pg_basebackup --pgdata=/var/lib/postgresql/data -R --host=${DB_HOST} --port=${DB_PORT}; do \n\
  echo 'Waiting for primary to connect...' \n\
  sleep 3s \n\
done \n\
chmod 0700 /var/lib/postgresql/data \n\
docker-entrypoint.sh $@"]

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
