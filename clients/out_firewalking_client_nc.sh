#!/bin/bash
for i in $(seq 1 65535); do nc $1 $i; done
echo "DONE"
