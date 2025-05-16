import os
import json
import yaml
from copy import deepcopy

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

index = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file == 'package.json':
            pkg_path = os.path.join(root, file)
            with open(pkg_path) as f:
                try:
                    pkg = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error parsing {pkg_path}: {e}")
                    continue
                    
            bundle_name = pkg.get('name', os.path.basename(root))
            bundle_version = pkg.get('version', '')
            bundle_author = pkg.get('author', '')
            bundle_display_name = pkg.get('displayName', '')
            bundle_description = pkg.get('description', '')
            bundle_tags = pkg.get('tags', [])
            
            for tmpl in pkg.get('templates', []):
                template_file = tmpl.get('file', '')
                
                # Check if the file exists at the specified path
                full_path = os.path.join(root, template_file)
                if not os.path.exists(full_path):
                    print(f"Warning: Template file not found: {full_path}")
                    continue
                    
                entry = {
                    'bundle': bundle_name,
                    'bundle_display_name': bundle_display_name,
                    'bundle_version': bundle_version,
                    'bundle_author': bundle_author,
                    'bundle_description': bundle_description,
                    'bundle_tags': bundle_tags,
                    'file': full_path.lstrip('./'),
                    'name': tmpl.get('name', os.path.splitext(os.path.basename(template_file))[0]),
                    'description': tmpl.get('description', ''),
                    'log_type': tmpl.get('log_type', ''),
                    'template_version': tmpl.get('version', ''),
                }
                index.append(entry)

# Sort by bundle name and template name for consistent output
index.sort(key=lambda x: (x['bundle'], x.get('name', '')))

with open('TEMPLATES.yaml', 'w') as f:
    # Use CleanDumper for better readability and proper list indentation
    yaml.dump(index, f, Dumper=CleanDumper, sort_keys=False, default_flow_style=False, 
              width=80, indent=2, allow_unicode=True, canonical=False, 
              explicit_start=True, explicit_end=True, version=(1, 2))