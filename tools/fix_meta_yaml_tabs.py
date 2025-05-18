import glob
import os
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(sequence=2, offset=2)

def fix_tabs_and_indent(path):
    # Backup the original file
    backup_path = path + ".bak"
    if not os.path.exists(backup_path):
        os.rename(path, backup_path)
    else:
        # If backup exists, use it as the source
        os.remove(path)
        os.rename(backup_path, path)
        os.rename(path, backup_path)
    # Read, replace tabs, and reformat
    with open(backup_path, 'r') as f:
        content = f.read().replace('\t', '  ')  # Replace tabs with 2 spaces
    try:
        data = yaml.load(content)
    except Exception as e:
        print(f"SKIPPING {path}: YAML parse error after tab fix: {e}")
        # Restore original if parse fails
        os.rename(backup_path, path)
        return
    with open(path, 'w') as f:
        yaml.dump(data, f)
    print(f"Fixed tabs and reformatted: {path} (backup at {backup_path})")

if __name__ == "__main__":
    for path in glob.glob('**/**/*.meta.yaml', recursive=True):
        fix_tabs_and_indent(path)