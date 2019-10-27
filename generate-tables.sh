#!/bin/bash

for D in ./resource_families/*/; do [ -d "$D" ] && ./run.py -i "$D" -o "$D" -r ./rules.json; done
