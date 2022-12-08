#!/bin/bash

git config user.name "GITACTIONS CI"
git config user.email "$COMMIT_AUTHOR_EMAIL"

# set -e

# generate tables
mkdir tables || true
bash ./generate-tables.sh

if [ "$GITHUB.BASE_REF" != "false" -o "$GIHUB.REF_NAME" != "master" ]; then exit 0; fi
echo Tables generated
# deploy
cd tables
git init
git add .
git commit -m "Deploy tables"
git push --force https://${GITHUB_TOKEN}:x-oauth-basic@github.com/clarin-eric/resource-families-html-generator.git HEAD:gh-pages
