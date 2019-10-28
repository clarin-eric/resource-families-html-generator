#!/bin/bash

git config --global user.email "CI-Bot@travis.com"
git config --global user.name "Travis Bot"

git init
git branch -a
git status
git add .
git status
git commit -m "Deploy tables"
git push --force https://$GITHUB_TOKEN:x-oauth-basic@github.com/clarin-eric/resource-families-html-generator.git travis:gh-pages

