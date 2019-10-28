#!/bin/bash

git config --global user.email "CI-Bot@travis.com"
git config --global user.name "Travis Bot"

# generate tables
bash ./generate-tables.sh

# deploy
cd tables
git init
git add .
git commit -m "Deploy tables"
git push --force https://$GITHUB_TOKEN:x-oauth-basic@github.com/clarin-eric/resource-families-html-generator.git gh-pages > /dev/null 2>&1

