#!/bin/bash

repo_name=$1

grep 'clean-architecture' -rl * --exclude=README.md --exclude-dir=venv | xargs sed -i "s/clean-architecture/${repo_name}/g"
grep 'clean-architecture' -rl .* --exclude-dir={.idea,.git} | xargs sed -i "s/clean-architecture/${repo_name}/g"
