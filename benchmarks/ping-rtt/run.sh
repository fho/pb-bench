#!/bin/bash

ping_host="google-public-dns-a.google.com."
max_tries=3
tries=0
rv=1

# To prevent that the benchmark is aborted when a single ICMP echo packet is
# lost, retry pinging up to 3 times when it failed
while [ $rv -ne 0 -a $tries -lt $max_tries ]; do
    out=$(ping -q -c1 $ping_host)
    rv=$?
done

result=$(echo $out |grep rtt| cut -d'/' -f 6)
echo $result > $RESULT_FILE
