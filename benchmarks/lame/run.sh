#!/bin/bash

out=$(time -p ( (./lame/bin/lame -h pts-trondheim.wav ) ) 2>&1)
[ $? -ne 0 ] && {
    echo -e "$out"
    exit 1
}

result=$(echo -e "$out"|grep real|cut -d ' ' -f2)
echo $result > $RESULT_FILE
