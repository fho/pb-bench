#!/bin/bash

export OMP_NUM_THREADS=$CPU_THREADS
out=$(./stream)
[ $? -ne 0 ] && {
    echo -e "$out"
    exit 1
}
result=$(echo -e "$out"|grep "Copy:" |awk '{print $2}')
echo $result > $RESULT_FILE
