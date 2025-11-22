@echo off
echo ========================================
echo Holy War Bot - GitHub Push Helper
echo ========================================
echo.
echo This script will help you push your code to GitHub.
echo.
echo IMPORTANT: You must create the repository on GitHub first!
echo Go to: https://github.com/new
echo Repository name: holywar-bot
echo (Don't initialize with README/gitignore)
echo.
pause

echo.
echo Adding remote repository...
git remote add origin https://github.com/tucker-green/holywar-bot.git

if %errorlevel% neq 0 (
    echo.
    echo Remote might already exist. Trying to update...
    git remote set-url origin https://github.com/tucker-green/holywar-bot.git
)

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Your code has been pushed!
    echo ========================================
    echo.
    echo View your repository at:
    echo https://github.com/tucker-green/holywar-bot
) else (
    echo.
    echo ========================================
    echo ERROR: Push failed!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Repository doesn't exist yet - create it at https://github.com/new
    echo 2. Authentication required - you may need to enter credentials
    echo 3. Repository name might be different
    echo.
    echo Check the error message above for details.
)

pause

