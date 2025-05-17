import glob
import yaml

for path in glob.glob('*/*.meta.yaml', recursive=True):
    with open(path) as f:
        meta = yaml.safe_load(f)
    if 'base_frequency' in meta:
        old = meta['base_frequency']
        new = round(float(old) * 60, 6)
        meta['base_frequency'] = new
        print(f"{path}: {old} -> {new}")
        with open(path, 'w') as f:
            yaml.dump(meta, f, sort_keys=False)