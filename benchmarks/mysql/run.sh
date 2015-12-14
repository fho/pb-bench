#!/bin/bash

rm -rf mysql/data/*

trap _cleanup EXIT

_cleanup() {
    pid=$(cat /tmp/mysql.pid)
    kill $pid
    sleep 3
    kill -9 $pid >/dev/null
}

mysql/bin/mysqld --defaults-file=./my.cnf --thread-concurrency=$CPU_THREADS --skip-grant --datadir=data --pid-file=/tmp/mysql.pid  -b ./mysql --lc-messages-dir=./mysql/share/ &

# wait 120sec for mysqld startup
i=0
while [ ! -S /tmp/mysql.sock -a $i -le 10 ]; do
    sleep 2;
done

echo 'create database test;' | mysql/bin/mysql --socket=/tmp/mysql.sock
cd mysql/sql-bench
out=$(perl run-all-tests --small-test --socket=/tmp/mysql.sock 2>&1)
result=$(echo -e "$out"|grep "TOTALS" |awk '{print $2}')
echo $result > $RESULT_FILE
