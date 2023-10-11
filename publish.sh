#!/bin/bash
git switch gh-pages && git fetch origin && git merge origin/main && git push && git switch main