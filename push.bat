@echo off

set /p input= commit:
git add .
git commit -m "%input%"
git push heroku master
