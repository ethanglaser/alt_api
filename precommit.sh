#!/bin/bash

# abort on errors
set -e

check_changes() {
  if git diff --stat --cached -- "$1" | grep -E "$1"; then
    echo "run precommit for $1"
    return 0
  else
    echo "no changes found for $1"
    return 1
  fi
}

force_run_command="-f"

node_paths=("frontend")

for path in "${node_paths[@]}"
do
  if [ "$1" = "$force_run_command" ] || check_changes "$path" ; then
    npm run precommit --prefix $path
  fi
done

script_paths=("api")

for path in "${script_paths[@]}"; do
  if [ "$1" = "$force_run_command" ] || check_changes "$path"; then
    cd "$path"
    ./precommit.sh
    cd -
  fi
done

if [ "$(expr substr $(uname -s) 1 10)" != "MINGW64_NT" ]; then
  git secrets --scan
fi

# run check for tabs precommit
cd scripts/precommit
./spaces.sh
# ./line_endings.sh
./check_symlinks.sh
cd -

git add -A

exit 0
