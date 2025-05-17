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
            
            # Skip node_modules or other unwanted directories
            if 'node_modules' in pkg_path or '.git' in pkg_path:
                continue
                
            with open(pkg_path) as f:
                try:
                    pkg = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error parsing {pkg_path}: {e}")
                    continue
                    
            # Count template files in the package
            template_count = len(pkg.get('templates', []))
            if template_count == 0:
                continue  # Skip packages with no templates
                
            # Verify template files exist
            templates_exist = False
            for tmpl in pkg.get('templates', []):
                template_file = tmpl.get('file', '')
                full_path = os.path.join(root, template_file)
                if os.path.exists(full_path):
                    templates_exist = True
                    break
                    
            if not templates_exist:
                continue  # Skip if no template files exist
            
            # Create an entry for the package
            bundle_path = '/'.join(root.split('/')[1:])  # Remove leading './'
            
            entry = {
                'name': pkg.get('name', os.path.basename(root)),
                'display_name': pkg.get('displayName', ''),
                'version': pkg.get('version', ''),
                'author': pkg.get('author', ''),
                'description': pkg.get('description', ''),
                'tags': pkg.get('tags', []),
                'path': bundle_path,
                'template_count': template_count
            }
            
            # Add entry if it has all required fields
            if entry['name'] and entry['path']:
                index.append(entry)

# Sort by name for consistent output
index.sort(key=lambda x: x['name'])

with open('TEMPLATES.yaml', 'w') as f:
    # Use CleanDumper for better readability and proper list indentation
    f.write('%YAML 1.2\n---\n')
    yaml.dump(index, f, Dumper=CleanDumper, sort_keys=False, default_flow_style=False, 
              width=80, indent=2, allow_unicode=True, canonical=False, 
              explicit_start=False, explicit_end=False)