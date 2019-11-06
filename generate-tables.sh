#!/bin/bash

set -e

for D in ./resource_families/*/; do 
	[ -d "$D" ] && ./run.py -i "$D" -o "$D" -r ./rules.json
	echo "Generates table from $D corpora"
done
for D in ./tables/*; do echo $D; done
