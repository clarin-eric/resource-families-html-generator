#/bin/bash

set -e

for D in ./resource_families/*/; do 
	[ -d "$D" ] && ./run.py -i "$D" -o "$D" -r ./rules.json
	trap "echo Corpora that failed to process: $D" 1 
done
