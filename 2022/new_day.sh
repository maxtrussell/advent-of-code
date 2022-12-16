#!/bin/bash

os=$(uname)
cd ~/dev/advent-of-code/2022/

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
url="https://adventofcode.com/2022/day/"$(echo $day | sed 's/^0*//')"/input"
cookies="session=$cookie"
status_code=$(curl -sb $cookies $url -o ${day}/input.txt -w "%{http_code}")
cat > "${day}/__init__.py" <<EOF
import sys

sys.path.append('../aoc.py')
EOF

cat > "${day}/main.py" <<EOF
import aoc

aoc.input_lines()
EOF

cat > "${day}/main.cpp" <<EOF
#include <string>
#include <vector>

#include "../aoc.cpp"

using namespace std;

int main(int, char* argv[]) {
  vector<string> lines = aoc::input_lines(argv[1]);
}
echo $status_code
