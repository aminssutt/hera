#!/bin/bash
# Deployment Script for Hera AI Coloring Books
# Run this script to deploy all changes to production

echo "🚀 HERA AI DEPLOYMENT SCRIPT"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Not in project root directory"
    exit 1
fi

echo "📋 Pre-deployment checks..."
echo ""

# Check for test files that shouldn't be committed
if git diff --cached --name-only | grep -E "test_.*\.py$"; then
    echo "⚠️  WARNING: Test files found in staging area:"
    git diff --cached --name-only | grep -E "test_.*\.py$"
    echo ""
    read -p "Remove test files from commit? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git reset HEAD aipart/test_*.py 2>/dev/null || true
        echo "✅ Test files unstaged"
    fi
fi

# Check for .env file
if git diff --cached --name-only | grep "\.env"; then
    echo "❌ ERROR: .env file in staging area!"
    echo "   Remove it immediately:"
    echo "   git reset HEAD .env"
    exit 1
fi

echo "✅ Pre-checks passed"
echo ""

# Show files to be committed
echo "📦 Files to be deployed:"
echo "------------------------"
git diff --cached --name-only
echo ""

# Ask for confirmation
read -p "Deploy these changes? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

# Commit
echo ""
echo "📝 Committing changes..."
git commit -m "feat: Migrate to Gemini 2.5 Flash Image + UX improvements

Major Changes:
- Switched from Imagen 4.0 to Gemini 2.5 Flash Image API
- Improved prompt structure with 3-part format
- Enhanced PDF page coverage from 54.6% to 72.8%
- Organized color selection into 4 themed palettes (28 colors)
- Added Success page with real-time PDF viewer
- Fixed email sender to verified address (hera.work.noreply@gmail.com)
- Improved email subjects for better deliverability
- Added 'Coming Soon: Markers' feature banner

Technical Details:
- Backend: generated_image.py, book_generator.py use Gemini 2.5 Flash Image
- Frontend: StepThree.jsx (color palettes), StepFour.jsx (markers), Success.jsx (PDF viewer)
- PDF: Reduced padding from 72pt to 36pt for better A4 coverage
- Email: Anti-spam improvements, professional subjects
- Queue: Background processing with session tracking

Testing:
- Local generation tested (12 pages B&W)
- Email delivery verified (Status 202)
- Success page polling works
- PDF viewer functional"

if [ $? -eq 0 ]; then
    echo "✅ Commit successful"
else
    echo "❌ Commit failed"
    exit 1
fi

# Push
echo ""
echo "🚀 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo ""
    echo "📊 Next steps:"
    echo "   1. Check Render logs: https://dashboard.render.com"
    echo "   2. Verify Vercel deployment: https://vercel.com/dashboard"
    echo "   3. Test production: https://hera-seven.vercel.app"
    echo "   4. Monitor emails in SendGrid dashboard"
    echo ""
    echo "🎯 Expected deployment time: 5-10 minutes"
else
    echo ""
    echo "❌ Push failed"
    echo "   Check your internet connection and GitHub credentials"
    exit 1
fi
