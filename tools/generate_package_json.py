import os
import yaml
import json

TEMPLATES_ROOT = "../"

def find_product_dirs(root):
    """Yield all product directories (vendor/product) under the templates root."""
    for vendor in os.listdir(root):
        vendor_path = os.path.join(root, vendor)
        if not os.path.isdir(vendor_path):
            continue
        for product in os.listdir(vendor_path):
            product_path = os.path.join(vendor_path, product)
            if os.path.isdir(product_path):
                yield vendor, product, product_path

def collect_templates(product_path, vendor, product):
    """Collect all templates and their metadata under a product directory."""
    templates = []
    for dirpath, _, files in os.walk(product_path):
        for file in files:
            if file.endswith(".j2"):
                rel_path = os.path.relpath(os.path.join(dirpath, file), TEMPLATES_ROOT)
                meta_path = os.path.splitext(os.path.join(dirpath, file))[0] + ".meta.yaml"
                meta = {}
                if os.path.exists(meta_path):
                    with open(meta_path) as f:
                        try:
                            meta = yaml.safe_load(f) or {}
                        except Exception:
                            meta = {}
                templates.append({
                    "file": rel_path.replace("\\", "/"),
                    "name": meta.get("data_source", os.path.splitext(file)[0]),
                    "description": meta.get("description", ""),
                    "vendor": meta.get("vendor", vendor),
                    "product": meta.get("product", product),
                    "format": meta.get("format", ""),
                })
    return templates

def main():
    for vendor, product, product_path in find_product_dirs(TEMPLATES_ROOT):
        templates = collect_templates(product_path, vendor, product)
        if not templates:
            continue
        package_json = {
            "vendor": vendor,
            "product": product,
            "templates": templates
        }
        out_path = os.path.join(product_path, "package.json")
        with open(out_path, "w") as f:
            json.dump(package_json, f, indent=2)
        print(f"Generated {out_path} with {len(templates)} templates.")

if __name__ == "__main__":
    main()