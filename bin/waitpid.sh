#!/bin/bash

if [[ $# -lt 1 ]]; then
	echo "usage: $0 <pid>"
fi

PID=$1

while [[ $(ps -p $PID | wc -l) -gt 1 ]]; do
	sleep 0.5
done;

notify-me
