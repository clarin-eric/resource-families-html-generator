#!/bin/bash

set -o errexit

# config
git config --global user.email "nobody@nobody.org"
git config --global user.name "Travis CI"

# deploy to tables branch
git add .
git commit -m "Generate tables"
git push --force "https://github-ci-token:${GITHUB_TOKEN}@github.org/${GITHUB_REPO}" travis
# > /dev/null 2>&1
