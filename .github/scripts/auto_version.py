#!/usr/bin/env python3
"""
Auto-version collection.json files based on changes detected.

Rules:
- New vendor or product → minor update
- Add/remove/edit templates → patch update
- Quarterly major release (handled by separate workflow)
"""

import os
import json
import sys
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Set

REPO_ROOT = Path(os.getcwd())

def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse semantic version string into (major, minor, patch)."""
    parts = version.split('.')
    major = int(parts[0]) if len(parts) > 0 else 0
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    return (major, minor, patch)

def increment_version(version: str, bump_type: str) -> str:
    """Increment version based on bump type."""
    major, minor, patch = parse_version(version)
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        return version

def get_git_diff_files() -> Set[str]:
    """Get list of files changed in the current commit compared to previous commit."""
    try:
        # Get files changed in this commit
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()
    except subprocess.CalledProcessError:
        # If HEAD~1 doesn't exist (first commit), return empty set
        return set()

def is_new_vendor_or_product(collection_path: Path, changed_files: Set[str]) -> bool:
    """Check if this is a new vendor or product."""
    # Check if vendor.meta.yaml or product.meta.yaml was added
    vendor_dir = collection_path.parent.parent
    vendor_meta = vendor_dir / "vendor.meta.yaml"
    product_meta = collection_path.parent / "product.meta.yaml"
    
    # Check if collection.json itself is new
    collection_str = str(collection_path.relative_to(REPO_ROOT))
    if collection_str in changed_files:
        # Check if it's a new file (wasn't in previous commit)
        try:
            result = subprocess.run(
                ["git", "diff", "--name-status", "HEAD~1", "HEAD", collection_str],
                capture_output=True,
                text=True,
                check=True
            )
            # If it starts with 'A' (Added), it's new
            if result.stdout.strip().startswith('A'):
                return True
        except subprocess.CalledProcessError:
            pass
    
    # Check if vendor or product metadata files are new
    vendor_meta_str = str(vendor_meta.relative_to(REPO_ROOT)) if vendor_meta.exists() else None
    product_meta_str = str(product_meta.relative_to(REPO_ROOT)) if product_meta.exists() else None
    
    if vendor_meta_str and vendor_meta_str in changed_files:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-status", "HEAD~1", "HEAD", vendor_meta_str],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip().startswith('A'):
                return True
        except subprocess.CalledProcessError:
            pass
    
    if product_meta_str and product_meta_str in changed_files:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-status", "HEAD~1", "HEAD", product_meta_str],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip().startswith('A'):
                return True
        except subprocess.CalledProcessError:
            pass
    
    return False

def get_template_changes(collection_path: Path) -> Tuple[Set[str], Set[str]]:
    """Get added and removed templates by comparing with previous commit."""
    try:
        # Get previous version of collection.json
        result = subprocess.run(
            ["git", "show", f"HEAD~1:{collection_path.relative_to(REPO_ROOT)}"],
            capture_output=True,
            text=True,
            check=True
        )
        old_data = json.loads(result.stdout)
        old_templates = set(old_data.get("templates", []))
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        # File didn't exist in previous commit or couldn't be parsed
        old_templates = set()
    
    # Get current templates
    with open(collection_path) as f:
        current_data = json.load(f)
    current_templates = set(current_data.get("templates", []))
    
    added = current_templates - old_templates
    removed = old_templates - current_templates
    
    return added, removed

def has_template_file_changes(collection_path: Path, changed_files: Set[str]) -> bool:
    """Check if any template files (.j2 or .meta.yaml) changed in this product."""
    product_dir = collection_path.parent
    product_dir_str = str(product_dir.relative_to(REPO_ROOT))
    
    for changed_file in changed_files:
        if changed_file.startswith(product_dir_str):
            if changed_file.endswith('.j2') or changed_file.endswith('.meta.yaml'):
                return True
    return False

def determine_bump_type(collection_path: Path, changed_files: Set[str], force_major: bool = False) -> Optional[str]:
    """Determine version bump type based on changes."""
    if force_major:
        return "major"
    
    # Check if new vendor/product
    if is_new_vendor_or_product(collection_path, changed_files):
        return "minor"
    
    # Check template changes
    added, removed = get_template_changes(collection_path)
    
    # If templates were added/removed or template files changed, it's a patch
    if added or removed or has_template_file_changes(collection_path, changed_files):
        return "patch"
    
    # No changes detected
    return None

def update_collection_version(collection_path: Path, bump_type: str) -> bool:
    """Update version in collection.json file."""
    with open(collection_path) as f:
        data = json.load(f)
    
    current_version = data.get("version", "1.0.0")
    new_version = increment_version(current_version, bump_type)
    
    if new_version == current_version:
        return False
    
    data["version"] = new_version
    
    with open(collection_path, 'w') as f:
        json.dump(data, f, indent=4)
        f.write('\n')
    
    print(f"  {collection_path.relative_to(REPO_ROOT)}: {current_version} → {new_version} ({bump_type})")
    return True

def main():
    """Main function to auto-version all changed collection.json files."""
    force_major = os.getenv("FORCE_MAJOR_RELEASE", "false").lower() == "true"
    
    if force_major:
        print("Quarterly major release: forcing major version bumps")
    
    changed_files = get_git_diff_files()
    
    if not changed_files:
        print("No files changed, skipping version updates")
        return
    
    # Find all collection.json files that were changed
    changed_collections = []
    for root, dirs, files in os.walk(REPO_ROOT / "templates"):
        if "collection.json" in files:
            collection_path = Path(root) / "collection.json"
            rel_path = str(collection_path.relative_to(REPO_ROOT))
            
            # Check if this collection.json or related files changed
            if (rel_path in changed_files or 
                has_template_file_changes(collection_path, changed_files) or
                is_new_vendor_or_product(collection_path, changed_files)):
                changed_collections.append(collection_path)
    
    if not changed_collections:
        print("No collection.json files affected by changes")
        return
    
    print(f"Auto-versioning {len(changed_collections)} collection(s)...")
    
    updated_count = 0
    for collection_path in changed_collections:
        bump_type = determine_bump_type(collection_path, changed_files, force_major)
        if bump_type:
            if update_collection_version(collection_path, bump_type):
                updated_count += 1
    
    if updated_count > 0:
        print(f"\nUpdated {updated_count} collection version(s)")
        sys.exit(0)
    else:
        print("No version updates needed")
        sys.exit(0)

if __name__ == "__main__":
    main()

