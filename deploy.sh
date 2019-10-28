#!/bin/bash

git config --global user.email "CI-Bot@travis.com"
git config --global user.name "Travis Bot"


git checkout gh-pages > /dev/null 2>&1
git branch -a > /dev/null 2>&1
git status > /dev/null 2>&1
git add . > /dev/null 2>&1
git status > /dev/null 2>&1
git commit -m "Deploy tables" > /dev/null 2>&1
git status > /dev/null 2>&1
git push --force https://$GITHUB_TOKEN:x-oauth-basic@github.com/clarin-eric/resource-families-html-generator.git travis:gh-pages > /dev/null 2>&1

