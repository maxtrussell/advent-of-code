#!/bin/env bash

date=$1
input="${2:-input}"

echo .env/bin/python3 -m ${date}.main ${input}.txt
time .env/bin/python3 -m ${date}.main ${input}.txt
