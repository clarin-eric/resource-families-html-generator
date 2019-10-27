#!/bin/bash

set -o errexit

# config
git config --global user.email "nobody@nobody.org"
git config --global user.name "Travis CI"

# deploy to tables branch
cd tables
git init
git add .
git commit -m "Generate tables"
git push --force --quiet "https://${GITHUB_TOKEN}@$github.com/${GITHUB_REPO}" master:gh-pages > /dev/null 2>&1
