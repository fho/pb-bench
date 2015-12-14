#!/bin/sh

out=$(./dbench/bin/dbench -c dbench/client.txt 48 2>&1)
[ $? -ne 0 ] && {
    echo -e "$out"
    exit 1
}

result=$(echo -e "$out"|grep -i "Throughput" |awk '{print $2}' 2>&1)
echo $result > $RESULT_FILE

[ -z "$result" ] && {
    echo "$out"
    echo "result is empty"
    exit 1
}
exit 0
