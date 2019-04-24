#!/bin/bash
mkdir -p $1/s16
for file in $1/wavs/*.wav; do
    echo $file
    c=${file}
    c1=${file%%.wav*}
    c2=${c1##*wavs/}
    # echo $c
    sox $c -r 16000 -c 1 -t sw - > $1/s16/$c2.s16
done