#!/bin/bash

os=$(uname)
cd ~/dev/advent-of-code/2024/

cookie=''
if [ -f "cookie.txt" ]; then
	cookie=$(cat cookie.txt)
else
	[[ -z "$2" ]] && echo "Usage: new_day.sh [day] [cookie]" && exit
	cookie=$2
fi

day=$(date +%d)
if [ -n "$1" ]; then
	day="$1"
fi
mkdir -p "$day"
url="https://adventofcode.com/2024/day/"$(echo $day | sed 's/^0*//')"/input"
cookies="session=$cookie"
status_code=$(curl -sb $cookies $url -o ${day}/input.txt -w "%{http_code}")

cat > "${day}/main.py" <<EOF
import lib.aoc as aoc

aoc.input_lines()
EOF

echo $status_code
