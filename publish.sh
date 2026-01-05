#!/bin/bash
# Publishing script for chpy-orm
# Usage: ./publish.sh <tag>
# Example: ./publish.sh v0.1.1

set -e  # Exit on error

if [ -z "$1" ]; then
    echo "Error: Tag is required"
    echo "Usage: $0 <tag>"
    echo "Example: $0 v0.1.1"
    exit 1
fi

TAG="$1"
VERSION="${TAG#v}"  # Remove 'v' prefix if present

echo "Publishing version $VERSION with tag $TAG"

# Check if setup.py exists
if [ ! -f "setup.py" ]; then
    echo "Error: setup.py not found"
    exit 1
fi

# Update version in setup.py
echo "Updating version in setup.py..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/version=\"[^\"]*\"/version=\"$VERSION\"/" setup.py
else
    # Linux
    sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" setup.py
fi

# Verify the version was updated
if ! grep -q "version=\"$VERSION\"" setup.py; then
    echo "Error: Failed to update version in setup.py"
    exit 1
fi

echo "Version updated to $VERSION in setup.py"

# Check if there are uncommitted changes (excluding setup.py changes we just made)
if ! git diff --quiet setup.py; then
    echo "Staging setup.py changes..."
    git add setup.py
    
    echo "Committing version update..."
    git commit -m "Bump version to $VERSION"
else
    echo "No changes to commit in setup.py"
fi

# Check if tag already exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "Warning: Tag $TAG already exists"
    read -p "Do you want to delete and recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d "$TAG"
        git push origin ":refs/tags/$TAG" 2>/dev/null || true
    else
        echo "Aborting..."
        exit 1
    fi
fi

# Create tag
echo "Creating tag $TAG..."
git tag -a "$TAG" -m "Release $TAG"

# Push changes
echo "Pushing commits and tags..."
BRANCH=$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD)
git push origin "$BRANCH"
git push origin "$TAG"

echo "Successfully published version $VERSION with tag $TAG"
echo "You can now publish to PyPI with: python -m build && python -m twine upload dist/*"

