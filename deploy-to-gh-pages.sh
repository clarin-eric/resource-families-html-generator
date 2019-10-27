#!/bin/bash

set -o errexit

# config
git config --global user.email "nobody@nobody.org"
git config --global user.name "Travis CI"

# deploy to tables branch
git add .
git commit -m "Generate tables"
echo "https://github-ci-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git"
echo "___"
git push --force "https://github-ci-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}" travis:gh-pages > /dev/null 2>&1
