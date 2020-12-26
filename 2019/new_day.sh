#!/bin/bash

year=2019

os=$(uname)
if [ "$os" == "Linux" ]; then
	cd ~/dev/advent-of-code/${year}/
else
	cd ~/dev/github/maxtrussell/advent-of-code/${year}/
fi

cookie=''
if [ -f "cookie.txt" ]; then
	cookie=$(cat cookie.txt)
else
	echo "ERROR: Put session cookie in cookie.txt" && exit
fi

[[ -z "$1" ]] && echo "Usage: new_day <day>" && exit

day=$1
mkdir $day
url="https://adventofcode.com/${year}/day/${day}/input"
cookies="session=$cookie"
curl -sb $cookies $url > ${day}/input.txt
