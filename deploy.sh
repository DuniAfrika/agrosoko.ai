#!/bin/bash

# AgroGhala Render Deployment Script
# Usage: ./deploy.sh

set -e  # Exit on error

echo "🚀 AgroGhala Render Deployment"
echo "================================"
echo ""

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "❌ Render CLI not found!"
    echo ""
    echo "Install it with:"
    echo "  macOS: brew tap render-oss/render && brew install render"
    echo "  Linux: curl -fsSL https://render.com/install-cli | sh"
    echo ""
    exit 1
fi

echo "✅ Render CLI found: $(render version)"
echo ""

# Check if logged in
echo "🔐 Checking Render authentication..."
if ! render services list &> /dev/null; then
    echo "❌ Not logged in to Render"
    echo ""
    echo "Please login first:"
    echo "  render login"
    echo ""
    exit 1
fi

echo "✅ Authenticated with Render"
echo ""

# Check if git repo exists
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
fi

# Check for remote
if ! git remote get-url origin &> /dev/null; then
    echo "⚠️  No git remote found!"
    echo ""
    echo "Please add a remote first:"
    echo "  git remote add origin https://github.com/yourusername/agrosoko-ai.git"
    echo ""
    read -p "Enter your GitHub repository URL: " repo_url
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote added"
    else
        echo "❌ No remote URL provided"
        exit 1
    fi
    echo ""
fi

# Add and commit all changes
echo "📝 Committing changes..."
git add .
git commit -m "Deploy to Render - $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
echo ""

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main || git push -u origin master
echo "✅ Pushed to remote"
echo ""

# Deploy to Render
echo "🚀 Deploying to Render..."
echo ""
echo "Choose deployment method:"
echo "  1) Create new service from render.yaml (first time)"
echo "  2) Redeploy existing service"
echo "  3) Open Render dashboard"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📋 Creating service from render.yaml..."
        render blueprint launch
        ;;
    2)
        echo ""
        read -p "Enter service name (default: agrosoko-api): " service_name
        service_name=${service_name:-agrosoko-api}
        echo "🔄 Redeploying $service_name..."
        render services redeploy "$service_name"
        ;;
    3)
        echo ""
        echo "🌐 Opening Render dashboard..."
        open https://dashboard.render.com || xdg-open https://dashboard.render.com
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📊 Monitor deployment:"
echo "  render logs --service agrosoko-api --tail --follow"
echo ""
echo "🌐 View dashboard:"
echo "  open https://dashboard.render.com"
echo ""
echo "🧪 Test API (after deployment completes):"
echo "  curl https://agrosoko-api.onrender.com/"
echo ""
echo "🎉 Done!"

