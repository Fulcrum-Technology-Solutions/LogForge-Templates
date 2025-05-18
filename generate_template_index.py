import os
import json
import yaml

# Custom YAML dumper with improved formatting
class CleanDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True
    
    # Better indentation for lists
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

# Custom string formatter
def represent_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, represent_str, Dumper=CleanDumper)

REQUIRED_FIELDS = [
    'name', 'display_name', 'version', 'author',
    'description', 'tags', 'path', 'template_count'
]

index = []
root_dir = '.'
for vendor in os.listdir(root_dir):
    if vendor == 'samples':
        continue  # Skip the 'samples' directory
    vendor_path = os.path.join(root_dir, vendor)
    if not os.path.isdir(vendor_path) or vendor.startswith('.'):
        continue
    for product in os.listdir(vendor_path):
        product_path = os.path.join(vendor_path, product)
        if not os.path.isdir(product_path):
            continue
        pkg_path = os.path.join(product_path, 'package.json')
        if not os.path.isfile(pkg_path):
            continue
        with open(pkg_path) as f:
            try:
                pkg = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing {pkg_path}: {e}")
                continue
        # Validate required fields
        missing = [k for k in REQUIRED_FIELDS if k not in pkg]
        if missing:
            print(f"{pkg_path} missing fields: {missing}")
            continue
        # Validate path field matches actual location
        rel_path = os.path.relpath(product_path, start=root_dir)
        if pkg['path'] != rel_path.replace('\\', '/').replace('./', ''):
            print(f"Warning: path field in {pkg_path} does not match actual location. Should be '{rel_path}'.")
        entry = {field: pkg[field] for field in REQUIRED_FIELDS}
        index.append(entry)

# Sort by name for consistent output
index.sort(key=lambda x: x['name'])

with open('TEMPLATES.yaml', 'w') as f:
    yaml.dump(index, f, Dumper=CleanDumper, sort_keys=False, default_flow_style=False, 
              width=80, indent=2, allow_unicode=True, canonical=False, 
              explicit_start=True, explicit_end=False)