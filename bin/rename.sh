#!/bin/bash

repo_name=$1

sed -i '' "s/clean-architecture/${repo_name}/g" *.py
sed -i '' "s/clean-architecture/${repo_name}/g" *.yaml

grep 'clean-architecture' -rl .* --exclude-dir={.idea,.git} | xargs sed -i '' "s/clean-architecture/${repo_name}/g"
