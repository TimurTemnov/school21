#!/bin/sh

INPUT_CSV="$1"

if ! [ -f "$INPUT_CSV" ]; then
    echo "Ошибка: Файл '$INPUT_CSV' не найден."
    exit 1
fi

awk -F',' '
BEGIN {
    print "\"name\",\"count\""  
}

NR > 1 {
    gsub(/"/, "", $3)

    if ($3 == "-") next

    split($3, parts, "/")
    for (i in parts) {
        if (parts[i] == "Junior" || parts[i] == "Middle" || parts[i] == "Senior") {
            counts[parts[i]]++
        }
    }
}

END {
    for (name in counts) {
        sorted[++idx] = counts[name] ":" name
    }

    n = asort(sorted, sorted, "@val_num_desc")

    for (i = 1; i <=n; i++) {
        split(sorted[i], parts, ":")
        name = parts[2]
        count = parts[1]
        printf "\"%s\",%s\n", name, count
    }
}
' "$INPUT_CSV" > hh_uniq_positions.csv