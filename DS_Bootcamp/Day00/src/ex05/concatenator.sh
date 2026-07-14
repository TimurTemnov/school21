#!/bin/sh

if [ $# -eq 0 ]; then
    echo "Использование: $0 file1.csv file2.csv ..."
    exit 1
fi

OUTPUT_FILE="hh_merged_sorted.csv"

head -n 1 "$1" > "$OUTPUT_FILE"

TMP_FILE=$(mktemp)

for file in "$@"; do
    if [ ! -f "$file" ]; then
        echo "Ошибка: Файл '$file' не найден, пропускаем" >&2
        continue
    fi
    
    tail -n +2 "$file" >> "$TMP_FILE"
done

sort -t',' -k2,2 "$TMP_FILE" >> "$OUTPUT_FILE"

rm "$TMP_FILE"