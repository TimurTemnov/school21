#!/bin/sh

INPUT_JSON="$1"

if ! [ -f "$INPUT_JSON" ]; then
    echo "Ошибка: Файл '$INPUT_JSON' не найден."
    exit 1
fi

if ! jq empty "$INPUT_JSON" 2>/dev/null; then
    echo "Ошибка: '$INPUT_JSON' не является валибным JSON."
    exit 1
fi

jq -r -f filter.jq "$INPUT_JSON" > hh.csv
