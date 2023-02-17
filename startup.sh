#! /bin/bash
git config --global user.name "metamorrphosis"
git config --global user.password "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"
cd death-gun
git branch --set-upstream-to=origin/main main
git fetch
git pull
python bot.py
