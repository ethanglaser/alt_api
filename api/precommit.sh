#!/bin/bash

# abort on errors
set -e

BASEDIR=$(dirname $0)

$BASEDIR/../scripts/precommit/python_poetry.sh api
