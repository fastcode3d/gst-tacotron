#!/bin/bash
mkdir -p $1/lpcf
for file in $1/s16/*.s16; do
    c=${file}
    c1=${file%%.s16*}
    c2=${c1##*s16/}
    # echo $c
    # echo $c2
    ./src/dump_data -test $c $1/lpcf/$c2.f32
done