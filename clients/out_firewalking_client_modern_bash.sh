#!/bin/bash
for i in $(seq 1 65535); do cat < /dev/null > /dev/tcp/$1/$i; done
echo "DONE"
