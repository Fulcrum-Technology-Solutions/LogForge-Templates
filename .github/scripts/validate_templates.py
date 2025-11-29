#!/usr/bin/env python3
import os
import sys
import json
import yaml
from jsonschema import validate, ValidationError

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), '../../schemas')

SCHEMAS = {
    'vendor.meta.yaml': 'vendor.schema.json',
    'product.meta.yaml': 'product.schema.json',
    'collection.json': 'collection.schema.json',
    'template.meta.yaml': 'template.schema.json',
}

def load_schema(schema_name):
    with open(os.path.join(SCHEMA_DIR, schema_name)) as f:
        return json.load(f)

def validate_file(filepath, schema_name):
    schema = load_schema(schema_name)
    with open(filepath) as f:
        if filepath.endswith('.json'):
            data = json.load(f)
        else:
            data = yaml.safe_load(f)
    try:
        validate(instance=data, schema=schema)
        print(f"[OK] {filepath}")
        return True
    except ValidationError as e:
        print(f"[FAIL] {filepath}: {e.message}")
        return False

def main():
    root = os.getcwd()
    success = True
    
    # Directories to skip (archived/old templates, examples)
    skip_dirs = {'archive', 'examples', '.git', '__pycache__', 'node_modules'}
    
    for dirpath, dirs, files in os.walk(root):
        # Skip excluded directories
        rel_path = os.path.relpath(dirpath, root)
        path_parts = rel_path.split(os.sep)
        if any(skip_dir in path_parts for skip_dir in skip_dirs):
            continue
        
        for filename in files:
            filepath = os.path.join(dirpath, filename)
            if filename.endswith('vendor.meta.yaml'):
                if not validate_file(filepath, 'vendor.schema.json'):
                    success = False
            elif filename.endswith('product.meta.yaml'):
                if not validate_file(filepath, 'product.schema.json'):
                    success = False
            elif filename.endswith('collection.json'):
                if not validate_file(filepath, 'collection.schema.json'):
                    success = False
            elif filename.endswith('.meta.yaml') and not (
                filename.endswith('vendor.meta.yaml') or filename.endswith('product.meta.yaml')):
                if not validate_file(filepath, 'template.schema.json'):
                    success = False
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 