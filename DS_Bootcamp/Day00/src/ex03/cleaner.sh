#!/bin/sh

INPUT_CSV="$1"

if ! [ -f "$INPUT_CSV" ]; then
    echo "Ошибка: Файл '$INPUT_CSV' не найден." >&2
    exit 1
fi

awk '
function process_third_column(field) {
    gsub(/"/, "", field)
    split(field, words, /[ ,\/()\[\]+-]+/)
    result = "-"
    found = 0
    
    for (i in words) {
        word = words[i]
        if (word == "Junior" || word == "Middle" || word == "Senior") {
            if (!found) {
                result = word
                found = 1
            } else if (!index(result, word)) {
                result = result "/" word
            }
        }
    }
    return "\"" result "\""
}

BEGIN {
    FPAT = "([^,]*)|(\"([^\"]|\"\")+\")"  # Шаблон для полей CSV
    OFS = ","
}
{
    if (NR == 1) {
        print $0
        next
    }

    new_third = process_third_column($3)
    
    printf "%s,%s,%s,%s,%s\n", $1, $2, new_third, $4, $5
}
' "$INPUT_CSV" > hh_positions.csv