# Push to GitHub Instructions

## Step 1: Create the Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `holywar-bot` (or `holywar bot` - GitHub will convert spaces to hyphens)
3. Description: "Automated bot for Holy War browser game - handles plundering, training, and player attacks"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/tucker-green/holywar-bot.git
git branch -M main
git push -u origin main
```

Or if you prefer SSH:
```bash
git remote add origin git@github.com:tucker-green/holywar-bot.git
git branch -M main
git push -u origin main
```

## Alternative: Use the Helper Script

I've created `push_to_github.bat` which will do this automatically. Just run it after creating the repo on GitHub!

