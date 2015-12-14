#!/bin/bash

rm -f test_file.cp

out=$(time -p ( (cp test_file test_file.cp && sync && sync) ) 2>&1)
[ $? -ne 0 ] && {
    echo -e "$out"
    exit 1
}

secs=$(echo -e "$out"|grep real|cut -d ' ' -f2)
size=$(stat -c%s test_file.cp)

result=$(echo "" |awk "{ print $size/$secs/1024/1024 }" )
echo $result > $RESULT_FILE
