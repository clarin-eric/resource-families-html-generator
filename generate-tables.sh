#!/bin/bash

set -e

for D in ./resource_families/*/; do 
	echo "Currently processed corpora: $D"
	[ -d "$D" ] && ./run.py -i "$D" -o "$D" -r ./rules.json
	trap "echo Corpora that failed to process: $D" EXIT
done
for D in ./tables/*; do echo $D; done
