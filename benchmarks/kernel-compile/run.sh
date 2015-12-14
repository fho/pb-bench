#!/bin/bash -x

cd linux-4.3
make V=0 distclean
make V=0 defconfig

out=$(time -p ( (make V=0 -j $CPU_THREADS ) ) 2>&1)
[ $? -ne 0 ] && {
    echo -e "$out"
    exit 1
}

result=$(echo -e "$out"|grep real|cut -d ' ' -f2)
echo $result > $RESULT_FILE
