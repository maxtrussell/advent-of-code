#!/bin/bash

cookie=$(cat cookie.txt)
day=$(date +%d)
if [ -n "$1" ]; then
	day="$1"
fi
year=$(date +%Y)
if [ -n "$2" ]; then
	year="$2"
fi

mkdir -p "${year}/${day}"
url="https://adventofcode.com/${year}/day/"$(echo $day | sed 's/^0*//')"/input"
cookies="session=$cookie"
status_code=$(curl -sb $cookies $url -o ${year}/${day}/input.txt -w "%{http_code}")

cat > "${year}/${day}/main.py" <<EOF
import lib.aoc as aoc

aoc.input_lines()
EOF

echo Fetching ${url}...
echo $status_code
