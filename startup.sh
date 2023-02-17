#! /bin/bash
git config --global user.name "metamorrphosis"
git config --global user.password "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"
git init
git branch --set-upstream-to=origin/main main
git pull 
python bot.py
