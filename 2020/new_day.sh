#!/bin/bash

[[ -z "$1" ]] && echo "Usage: new_day.sh <session cookie val>" && exit

cd ~/dev/github/maxtrussell/advent-of-code/2020

day=$(date +%d)
mkdir $day
url="https://adventofcode.com/2020/day/${day}/input"
cookies="session=$1"
curl -sb $cookies $url > ${day}/input.txt
