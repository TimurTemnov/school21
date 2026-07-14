#!/bin/sh

vacancy_name="Data Scientist"
OUTPUT_FILE="hh.json"

if [ ! -z "$1" ]; then
    vacancy_name="$1"
fi

encoded_vacancy=$(echo "$vacancy_name" | sed 's/ /+/g')


curl -s "https://api.hh.ru/vacancies?text=$encoded_vacancy&per_page=100" | \
    jq --arg query "$vacancy_name" '
        .items |
        map(select(.name | test($query; "i"))) |
        .[0:20]
    ' > "$OUTPUT_FILE"