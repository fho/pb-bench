#!/bin/sh
out=$(p7zip_9.20.1/bin/7za -mmt=$CPU_THREADS b 2>&1)
[ $? -ne 0 ] && {
    echo -e "$out"
    exit 1
}

result=$(echo -e "$out"|grep "Tot:" |awk '{print $4}')
echo $result > $RESULT_FILE
