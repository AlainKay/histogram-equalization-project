# GitHub Push Guide - Complete Reference

This guide documents all the steps used to push the histogram equalization project to GitHub.

## Prerequisites

- Git installed on your system
- GitHub account
- GitHub Personal Access Token with `repo` scope

---

## Step 1: Create GitHub Personal Access Token

1. Go to [GitHub](https://github.com) and log in
2. Click your profile picture → **Settings**
3. Scroll down to **Developer settings** (bottom of left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Configure the token:
   - **Note:** "Repository Push Access" (or any descriptive name)
   - **Expiration:** Choose your preference
   - **Scopes:** Check `repo` (this is critical for creating/pushing to repositories)
7. Click **Generate token**
8. **Copy the token immediately** (format: `ghp_xxxxxxxxxxxxx`)
9. Store it securely (you won't be able to see it again)

---

## Step 2: Create .gitignore File

Create a `.gitignore` file to exclude unnecessary files:

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# LaTeX
*.aux
*.log
*.out
*.toc
*.pdf
*.synctex.gz
*.fls
*.fdb_latexmk

# OS
.DS_Store
Thumbs.db

# Project specific
*.tar.gz
data_and_results.tar.gz
EOF
```

---

## Step 3: Initialize Git Repository

```bash
# Initialize git repository
git init

# Configure git user (local to this repository)
git config user.email "your-email@example.com"
git config user.name "YourUsername"

# Check status
git status
```

---

## Step 4: Stage and Commit Files

```bash
# Add all files to staging
git add .

# Verify what will be committed
git status

# Create initial commit
git commit -m "Initial commit: Histogram Equalization Project

- Implemented GHE and CLAHE algorithms for image enhancement
- Comprehensive evaluation with PSNR, SSIM, entropy, contrast, naturalness metrics
- 22 test images across 11 challenging categories
- Complete LaTeX report with experimental results
- Python source code with modular architecture"
```

---

## Step 5: Create GitHub Repository via API

**Method 1: Using curl (no sudo required)**

```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{
    "name": "your-repo-name",
    "description": "Your repository description",
    "private": false
  }'
```

**Method 2: Manual (via browser)**

1. Go to https://github.com/new
2. Enter repository name
3. Add description (optional)
4. Choose Public or Private
5. **Do NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

---

## Step 6: Add Remote and Push

```bash
# Rename branch to main (if needed)
git branch -M main

# Add remote repository (replace with your username and repo name)
git remote add origin https://github.com/YOUR_USERNAME/your-repo-name.git

# Verify remote was added
git remote -v

# Set remote URL with token for authentication
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/your-repo-name.git

# Push to GitHub
git push -u origin main

# Clean up: Remove token from remote URL for security
git remote set-url origin https://github.com/YOUR_USERNAME/your-repo-name.git
```

---

## Step 7: Verify Success

Visit your repository URL:
```
https://github.com/YOUR_USERNAME/your-repo-name
```

Check that all files are present.

---

## Alternative: Using GitHub CLI (if installed)

If you have sudo access and can install GitHub CLI:

```bash
# Install GitHub CLI (requires sudo)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
  sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
  sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y

# Authenticate with GitHub
gh auth login

# Create repository and push
gh repo create your-repo-name --public --source=. --remote=origin --push
```

---

## Troubleshooting

### "Not a git repository" Error
```bash
# Make sure you're in the correct directory
pwd

# Navigate to your project directory
cd /path/to/your/project

# Verify .git folder exists
ls -la .git
```

### "Permission denied" for sudo
If you don't have sudo access, use the curl/API method instead of installing GitHub CLI.

### "Not Found" when creating repository via API
Your token doesn't have the `repo` scope. Create a new token with proper permissions.

### Authentication failed during push
- Verify your token is correct
- Ensure the token has `repo` scope
- Use token as password, not your GitHub password

### Token in remote URL
After pushing, always clean up the token from the remote URL:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/your-repo-name.git
```

---

## Security Best Practices

1. **Never share your Personal Access Token** in chat, code, or documentation
2. **Revoke exposed tokens immediately** at: Settings → Developer settings → Personal access tokens
3. **Use token expiration** - set reasonable expiration dates
4. **Minimize token scopes** - only grant necessary permissions
5. **Remove tokens from git remote URLs** after use
6. **Store tokens securely** - use password managers or environment variables

---

## Future Pushes

After initial setup, pushing updates is simple:

```bash
# Make changes to your code
# ...

# Stage changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

You'll be prompted for credentials. Use:
- **Username:** Your GitHub username
- **Password:** Your Personal Access Token (not your GitHub password)

---

## Additional Git Commands

### Check repository status
```bash
git status
```

### View commit history
```bash
git log --oneline
```

### Create a new branch
```bash
git checkout -b new-branch-name
```

### Pull latest changes
```bash
git pull origin main
```

### Clone repository to another machine
```bash
git clone https://github.com/YOUR_USERNAME/your-repo-name.git
```

---

## Example: Complete Workflow for This Project

```bash
# Navigate to project directory
cd /mnt/bst/achoi13A100/ptuemler/alain_llm_project/mACHINEVision_Project/histogram_equalization_project

# Create .gitignore
cat > .gitignore << 'EOF'
[content as shown in Step 2]
EOF

# Initialize git
git init
git config user.email "kayiranga37@gmail.com"
git config user.name "AlainKay"

# Stage and commit
git add .
git commit -m "Initial commit: Histogram Equalization Project

- Implemented GHE and CLAHE algorithms for image enhancement
- Comprehensive evaluation with PSNR, SSIM, entropy, contrast, naturalness metrics
- 22 test images across 11 challenging categories
- Complete LaTeX report with experimental results
- Python source code with modular architecture"

# Create repository on GitHub via API
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"histogram-equalization-project","description":"Comparative analysis of GHE and CLAHE for image enhancement","private":false}'

# Add remote and push
git branch -M main
git remote add origin https://github.com/AlainKay/histogram-equalization-project.git
git remote set-url origin https://AlainKay:YOUR_TOKEN@github.com/AlainKay/histogram-equalization-project.git
git push -u origin main

# Clean up token from URL
git remote set-url origin https://github.com/AlainKay/histogram-equalization-project.git
```

**Result:** https://github.com/AlainKay/histogram-equalization-project

---

## Summary

This guide covered:
- ✅ Creating GitHub Personal Access Tokens
- ✅ Initializing git repositories
- ✅ Creating .gitignore files
- ✅ Making commits
- ✅ Creating GitHub repositories via API
- ✅ Adding remotes and pushing code
- ✅ Security best practices
- ✅ Troubleshooting common issues

Keep this guide for future reference when working with Git and GitHub!
