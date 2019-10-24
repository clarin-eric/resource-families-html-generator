#!/bin/bash

set -o errexit

# config
git config --global user.email "nobody@nobody.org"
git config --global user.name "Travis CI"

# generate tables
for D in ./resource_families/*/; do [ -d "$D" ] && ./run.py -i "$D" -o "$D" -r ./rules.json; done

# deploy to tables branch
cd tables
git init
git add .
git commit -m "Generate tables"
git push --force --quiet "https://${GITHUB_TOKEN}@$github.com/${GITHUB_REPO}" master:gh-pages > /dev/null 2>&1
