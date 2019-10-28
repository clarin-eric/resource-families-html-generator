#!/bin/bash

git config --global user.email "CI-Bot@travis.com"
git config --global user.name "Travis Bot"


git checkout gh-pages
git branch -a
git status
git add .
git status
git commit -m "Deploy tables"
git status
git push --force https://$GITHUB_TOKEN:x-oauth-basic@github.com/clarin-eric/resource-families-html-generator.git travis:gh-pages

