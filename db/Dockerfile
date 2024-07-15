FROM postgres:latest

RUN apt-get update && apt-get install -y gettext-base

RUN mkdir -p /oracle/pg_data/archive/ 
RUN chown -R postgres:postgres /oracle/pg_data/archive/ 

COPY ./init.sql /docker-entrypoint-initdb.d/init.sql.raw

ENTRYPOINT [ "bash", "-c", "\
mkdir -p /var/log/postgresql/ \n\
chown postgres:postgres /var/log/postgresql/ \n\
envsubst < /docker-entrypoint-initdb.d/init.sql.raw > /docker-entrypoint-initdb.d/init.sql \n\
cat <<EOF > /etc/postgresql/postgresql.conf \n\
listen_addresses = '*' \n\
port = ${DB_PORT} \n\
wal_level = replica \n\
wal_log_hints = on \n\
archive_mode = on \n\
archive_command = 'cp %p /oracle/pg_data/archive/%f' \n\
max_wal_senders = 10 \n\
hot_standby = on \n\
logging_collector = on \n\
log_replication_commands = on \n\
log_directory = '/var/log/postgresql' \n\
log_filename = 'postgresql.log' \n\
EOF\n\
cat <<EOF > /etc/postgresql/pg_hba.conf \n\
local all ${POSTGRES_USER} peer \n\
host all all 0.0.0.0/0 scram-sha-256 \n\
host replication ${DB_REPL_USER} ${DB_REPL_HOST}/32 scram-sha-256 \n\
EOF\n\
docker-entrypoint.sh $@"]

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf", "-c", "hba_file=/etc/postgresql/pg_hba.conf"]

