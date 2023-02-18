#! /bin/bash
git --version
git config --global user.name "metamorrphosis"
git config --global user.password "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"
git add *
git stash
git pull https://github.com/metamorrphosis/death-gun.git main
git stash apply --index
