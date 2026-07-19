#!/bin/bash
# Build Firefox extension package
set -e

# Version: prefer EXTENSION_VERSION env, else read from package.json
VERSION="${EXTENSION_VERSION:-$(node -p "require('./extension/package.json').version" 2>/dev/null || echo "5.1.0")}"
OUT="extension-firefox/build"
ZIP="qalqan-ai-firefox-v${VERSION}.zip"

echo "🦊 Building Firefox extension..."

# Clean and create build dir
rm -rf "$OUT"
mkdir -p "$OUT"

# Copy all public files
cp extension/public/background.js "$OUT/"
cp extension/public/blocked.html "$OUT/"
cp extension/public/blocked.js "$OUT/"
cp extension/public/content.js "$OUT/"
cp extension/public/search-guard.js "$OUT/"
cp extension/public/messenger-guard.js "$OUT/"
cp extension/public/form-guard.js "$OUT/"
cp extension/public/fingerprint-detector.js "$OUT/"
cp extension/public/offline-db.js "$OUT/"
cp -r extension/public/icons "$OUT/"

# Copy built popup (if exists)
if [ -d "extension/dist" ]; then
  cp extension/dist/index.html "$OUT/" 2>/dev/null || true
  cp -r extension/dist/assets "$OUT/" 2>/dev/null || true
fi

# Use Firefox manifest
cp extension-firefox/manifest.json "$OUT/"

# Apply Firefox-specific patches to background.js
# importScripts is not supported in Firefox MV3 module workers — inline via concatenation
echo "" >> "$OUT/background.js"

# Package
cd "$OUT"
zip -r "../../$ZIP" . -x "*.DS_Store"
cd ../..

echo "✅ Firefox extension v${VERSION}: $ZIP"
echo "   Size: $(du -sh $ZIP | cut -f1)"
echo ""
echo "📦 Install in Firefox:"
echo "   1. Open about:debugging"
echo "   2. Click 'This Firefox' → 'Load Temporary Add-on'"
echo "   3. Select: $ZIP"
