#!/bin/sh

INPUT_CSV="$1"

if ! [ -f "$INPUT_CSV" ]; then
    echo "Ошибка: Файл '$INPUT_CSV' не найден."
    exit 1
fi

head --lines=1 "$INPUT_CSV" > hh_sorted.csv

tail -n+2 "$INPUT_CSV" | sort -t',' -k2,2 -k1,1 >> hh_sorted.csv
