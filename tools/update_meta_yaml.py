from ruamel.yaml import YAML
import glob

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(sequence=2, offset=2)

for path in glob.glob('**/**/*.meta.yaml', recursive=True):
    try:
        with open(path, 'r') as f:
            data = yaml.load(f)
    except Exception as e:
        print(f"SKIPPING {path}: YAML parse error: {e}")
        continue
    if data and 'base_frequency' in data:
        old = data['base_frequency']
        new = round(float(old) * 60, 6)
        data['base_frequency'] = new
        print(f"{path}: {old} -> {new}")
        with open(path, 'w') as f:
            yaml.dump(data, f)