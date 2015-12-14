#!/bin/sh

trap _cleanup 0

_cleanup() {
    ./apache/bin/apachectl -d apache -k stop || sleep 3
}


export LD_LIBRARY_PATH="apache/lib/"

./apache/bin/apachectl -d apache -k stop  || sleep 3 # make sure apache isnt running
# start apache
./apache/bin/apachectl -d apache -k start || {
    echo "apache start failed" 
    exit 1
}
sleep 3


# benchmark!
out=$(./apache/bin/ab -n 700000 -c 100 http://localhost:8088/test.html)
[ $? -ne 0 ] && {
    echo -e "$out"
    exit 1
}

result=$(echo -e "$out"|grep "Requests per second:" |awk '{print $4}')
echo $result > $RESULT_FILE
