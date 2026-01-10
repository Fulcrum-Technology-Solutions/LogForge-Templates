# Examples Directory

This directory contains example templates and metadata files to help you get started with creating your own LogForge templates.

## Structure
- Example vendor, product, and data source directories
- Example template files (.j2) and metadata files (.meta.yaml)
- Example collection.json and meta files

## Example Structure

```
examples/
  acme/
    vendor.meta.yaml
    widget/
      product.meta.yaml
      collection.json
      telemetry/
        device_online.j2
        device_online.meta.yaml
```

Use these examples as a reference for formatting and required fields when contributing new templates to the repository. 