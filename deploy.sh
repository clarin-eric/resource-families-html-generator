#!/bin/bash

git config --global user.email "CI-Bot@travis.com"
git config --global user.name "Travis Bot"

set -e

# generate tables
mkdir tables || true
bash ./generate-tables.sh

if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "master" ]; then exit 0; fi
echo Tables generated
# deploy
cd tables
git init
git add .
git commit -m "Deploy tables"
git push --force https://${GITHUB_TOKEN}:x-oauth-basic@github.com/clarin-eric/resource-families-html-generator.git HEAD:gh-pages
