#!/bin/bash
# Build the frontend and deploy to GitHub Pages

# Build the frontend
npm run build

# Navigate to the build output directory
cd dist

# Initialize a new git repo
git init
git add -A
git commit -m "Deploy to GitHub Pages"

# Push to the gh-pages branch
git push -f git@github.com:YOUR_USERNAME/YOUR_REPOSITORY.git master:gh-pages

# Go back to the root directory
cd ..
