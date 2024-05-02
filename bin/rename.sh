#!/bin/bash

repo_name=$1
export LANG=C

sed -i '' "s/clean-architecture/${repo_name}/g" app/app.py
grep 'clean-architecture' -rl .* --exclude=README.md --exclude-dir={.idea,.git,bin} | xargs sed -i '' "s/clean-architecture/${repo_name}/g"
