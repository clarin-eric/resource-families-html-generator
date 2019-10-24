#!/bin/bash

set -o errexit

# config
git config --global user.email "nobody@nobody.org"
git config --global user.name "Travis CI"

# deploy
for D in ./resource_families/*/; do [ -d "$D" ] && ./run.py -i "$D" -o "$D" -r ./rules.json; done

