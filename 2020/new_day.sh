#!/bin/bash

os=$(uname)
if [ "$os" == "Linux" ]; then
	cd ~/dev/advent-of-code/2020/
else
	cd ~/dev/github/maxtrussell/advent-of-code/2020
fi

cookie=''
if [ -f "cookie.txt" ]; then
	cookie=$(cat cookie.txt)
else
	[[ -z "$1" ]] && echo "Usage: new_day.sh <session cookie val>" && exit
	cookie=$1
fi

day=$(date +%d)
mkdir $day
url="https://adventofcode.com/2020/day/${day}/input"
cookies="session=$cookie"
curl -sb $cookies $url > ${day}/input.txt
