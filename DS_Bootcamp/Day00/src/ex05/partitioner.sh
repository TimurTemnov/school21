#!/bin/sh

INPUT_CSV="$1"
OUTPUT_PREFIX="hh_positions_"

if ! [ -f "$INPUT_CSV" ]; then
    echo "Ошибка: Файл '$INPUT_CSV' не найден." >&2
    exit 1
fi

awk -F',' -v output_prefix="$OUTPUT_PREFIX" '
BEGIN {
    getline header
    split(header, header_fields, ",")
    date_field = 2
}

{
    split($date_field, dtparts, "T")
    filedate = dtparts[1]

    filename = output_prefix "_" filedate ".csv"
    if (!(filename in files)) {
        print header > filename
        files[filename] = 1
    }

    print $0 >> filename
    close(filename)
}
' "$INPUT_CSV"