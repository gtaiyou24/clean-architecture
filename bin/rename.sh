#!/bin/bash

repo_name=$1
export LANG=C

grep 'clean-architecture' -rl * --exclude-dir={venv,bin,doc} --exclude=README.md | xargs sed -i '' "s/clean-architecture/${repo_name}/g"
grep 'clean-architecture' -rl .* --exclude-dir={.idea,.git} | xargs sed -i '' "s/clean-architecture/${repo_name}/g"
