# LogForge Templates

This repository contains community-contributed templates for [LogForge](https://github.com/Fulcrum-Technology-Solutions/LogForge), a synthetic event log generator.

## Template Structure

Templates are organized in a 4-tier hierarchy:
- Vendor (e.g., microsoft)
- Product (e.g., windows)
- Data Source (e.g., security)
- Template files (e.g., account_locked.j2, account_locked.meta.yaml)

Example structure:
```
vendor/
  product/
    data_source/
      template_name.j2
      template_name.meta.yaml
```

See the `examples/` directory for a complete sample structure and files.

## Using Templates

To use these templates with LogForge:

```bash
# Install templates from the command line
logforge templates install microsoft/windows/security/account_locked

# Or install all templates for a product
logforge templates install microsoft/windows --all
```

## Template Metadata

Each template must have a corresponding `.meta.yaml` file with required fields. See the `schemas/` directory for JSON schema definitions.

## Example Template & Metadata

Example template (`examples/acme/widget/telemetry/device_online.j2`):
```jinja2
{
  "event": "device_online",
  "device_id": "{{ device_id }}",
  "timestamp": "{{ timestamp }}",
  "status": "online"
}
```

Example metadata (`examples/acme/widget/telemetry/device_online.meta.yaml`):
```yaml
vendor: "Acme"
product: "Widget"
data_source: "telemetry"
description: "Indicates that a device has come online."
format: "JSON"
frequency: "medium"
is_generator: true
base_frequency: 10
time_patterns:
  - business_hours
context:
  device_id: "device-1234"
  timestamp: "2025-01-01T00:00:00Z"
parameters:
  - name: "device_id"
    description: "Unique identifier for the device."
    required: true
    default: "device-1234"
  - name: "timestamp"
    description: "Event timestamp in ISO8601 format."
    required: true
    default: "2025-01-01T00:00:00Z"
```

## Template Index & Automation

- The `TEMPLATES.yaml` file is auto-generated and provides a complete index of all templates in the repository.
- **Do not edit `TEMPLATES.yaml` manually.**
- GitHub Actions automatically validate all metadata and update the index on every push and pull request.
- You can also run the scripts locally:

```bash
# Validate all metadata and templates
python .github/scripts/validate_templates.py

# Update the TEMPLATES.yaml index
python .github/scripts/update_templates_index.py
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to add or modify templates, metadata, and collections.

- Follow the structure and metadata requirements in the `examples/` and `schemas/` directories.
- Validate your files before submitting a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
