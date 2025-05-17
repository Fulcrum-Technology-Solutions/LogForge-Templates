#!/usr/bin/env python3
import os
import yaml
import datetime
from pathlib import Path

def update_meta_yaml(file_path):
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            if data is None:
                data = {}
        
        # Save original data for reference
        original_data = data.copy()
        
        # Create new data structure according to the schema
        new_data = {}
        
        # Set required fields
        new_data['name'] = original_data.get('data_source', 
                                            os.path.basename(file_path).replace('.meta.yaml', ''))
        new_data['description'] = original_data.get('description', 'No description available')
        
        # Set log_type based on best guess from existing fields
        if 'data_source' in original_data and 'security' in original_data['data_source'].lower():
            new_data['log_type'] = 'security'
        elif 'product' in original_data and any(x in original_data['product'].lower() for x in ['firewall', 'threat']):
            new_data['log_type'] = 'threat'
        else:
            new_data['log_type'] = original_data.get('product', 'general').lower()
        
        new_data['author'] = 'Fulcrum Technology Solutions'
        new_data['version'] = '1.0.0'
        
        # Set optional fields if they exist in the original
        if 'product' in original_data:
            new_data['product'] = original_data['product']
        
        if 'vendor' in original_data:
            new_data['vendor'] = original_data['vendor']
        
        # Create tags from existing data
        tags = []
        if 'vendor' in original_data:
            tags.append(original_data['vendor'].lower().replace(' ', '-'))
        if 'product' in original_data:
            tags.append(original_data['product'].lower().replace(' ', '-'))
        if 'data_source' in original_data:
            parts = original_data['data_source'].lower().split()
            for part in parts:
                if len(part) > 3 and part not in tags:  # Avoid short words
                    tags.append(part)
        
        if tags:
            new_data['tags'] = tags
        
        # Set dates
        today = datetime.date.today().isoformat()
        new_data['date_created'] = today
        new_data['last_updated'] = today
        
        # Copy fields if they exist
        if 'parameters' in original_data:
            fields = []
            for param in original_data['parameters']:
                if 'name' in param and 'description' in param:
                    fields.append({
                        'field': param['name'],
                        'description': param['description']
                    })
            if fields:
                new_data['fields'] = fields
        
        # Copy documentation to notes if it exists
        if 'documentation' in original_data:
            new_data['notes'] = original_data['documentation']
        
        # Write updated data back to file
        with open(file_path, 'w') as f:
            yaml.dump(new_data, f, default_flow_style=False, sort_keys=False)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

# Find all meta.yaml files in the repository
count = 0
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.meta.yaml'):
            file_path = os.path.join(root, file)
            if update_meta_yaml(file_path):
                count += 1
                print(f"Updated: {file_path}")

print(f"\nTotal files updated: {count}")