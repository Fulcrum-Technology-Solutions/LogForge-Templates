# LogForge Templates

This repository contains community-contributed templates for [LogForge](https://github.com/Fulcrum-Technology-Solutions/LogForge), a synthetic event log generator.

> **Note:** LLM-powered (AI-assisted) template creation, analysis, and metadata generation are only available in the Enterprise version (future separate repository), and only via the web UI (not CLI). The open-source version does not include any Enterprise-only features.

---

## Overview
LogForge Templates is a community-driven collection of Jinja2-based templates and metadata for generating realistic synthetic logs from a variety of systems (e.g., Windows Event Log, Palo Alto Firewall, Azure AD). Templates are designed for use with the LogForge CLI and entity registry, enabling customizable, high-fidelity log generation for testing, demos, and development.

---

## Template Structure & Requirements

Templates and metadata are organized in a strict hierarchy:

```
vendor/
  vendor.meta.yaml           # Vendor metadata (see schemas/vendor.schema.json)
  product/
    product.meta.yaml        # Product metadata (see schemas/product.schema.json)
    collection.json          # Product's template collection index (see schemas/collection.schema.json)
    data_source/
      template_name.j2       # Jinja2 template
      template_name.meta.yaml # Template metadata (see schemas/template.schema.json)
```

- **Vendor**: Top-level directory (e.g., `paloalto/`, `microsoft/`).
  - `vendor.meta.yaml`: Contains vendor info (machine ID, display name, website, description, logo).
- **Product**: Subdirectory for each product (e.g., `firewall/`, `windows/`).
  - `product.meta.yaml`: Contains product info (vendor, product name, description, version, documentation URL).
  - `collection.json`: Lists all templates for the product, with metadata for maintainers, tags, and template paths.
- **Data Source**: Subdirectory for each data source or log type (e.g., `network/`, `security/`).
- **Template**: Each template consists of:
  - `template_name.j2`: The Jinja2 template file.
  - `template_name.meta.yaml`: Metadata describing the template (vendor, product, data_source, description, format, parameters, etc.).

See the `examples/` directory for a complete, working sample.

---

## Schema Validation

All metadata files must conform to their respective JSON schemas in the `schemas/` directory:

- `schemas/vendor.schema.json` → `vendor.meta.yaml`
- `schemas/product.schema.json` → `product.meta.yaml`
- `schemas/collection.schema.json` → `collection.json`
- `schemas/template.schema.json` → `template_name.meta.yaml`

**Key Points:**
- Only template-level `.meta.yaml` files require a `data_source` property.
- Vendor and product metadata do **not** require `data_source`.
- All fields and structure must match the schema for validation to pass.

---

## Template Authoring & Contribution

To contribute a new template:
- Place your `.j2` template and its `.meta.yaml` metadata file as described in the [Template Structure & Requirements](#template-structure--requirements) section (e.g., `paloalto/firewall/network/`).
- All metadata files must conform to their respective schemas (see [Schema Validation](#schema-validation)).
- Use realistic field names and reference entities using the `entities` object (e.g., `{{ entities.users[0] }}` or `{{ random_email() }}`).
- Test your template with sample entity files and run validation:
  ```bash
  logforge validate-template --template <path-to-template> --entities <path-to-entities.yaml>
  ```

**Minimal Example:**

Template (`example_log.j2`):
```jinja2
{{ current_timestamp() }} {{ random_email() }} {{ random_hostname() }} {{ registry.get_random_user() }}
```

Metadata (`example_log.meta.yaml`):
```yaml
vendor: Palo Alto Networks
product: Firewall
data_source: network
description: Example log template for demonstration
format: Syslog
frequency: medium
is_generator: true
base_frequency: 10
time_patterns:
  - business_hours
context:
  device_id: "device-1234"
  timestamp: "2025-01-01T00:00:00Z"
parameters:
  - name: device_id
    description: Unique identifier for the device.
    required: true
    default: device-1234
  - name: timestamp
    description: Event timestamp in ISO8601 format.
    required: true
    default: 2025-01-01T00:00:00Z
```

For more details and advanced authoring tips, see [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Entity Files & Dynamic Fallbacks

Templates reference fields from an entity YAML file (e.g., `entities/entities.yaml`). LogForge will automatically fill in missing entity fields with standard values for common fields, making template rendering more robust and user-friendly.

**Example entity file:**
```yaml
users:
  - alice
  - bob
source_ip:
  - 192.168.1.10
  - 10.0.0.5
```

If a template references a field (e.g., `entities.registry`) that is missing from your `entities.yaml`, LogForge will inject a standard value and print a warning. You can override defaults by creating a `standard_entities.yaml` in your project root.

---

## Template Validation & Automation

- The `TEMPLATES.yaml` file is auto-generated and provides a complete index of all templates in the repository.
- **Do not edit `TEMPLATES.yaml` manually.**
- **Do not use generate_template_index.py; it is deprecated and has been removed.**
- The only supported script for index generation is `.github/scripts/update_templates_index.py`.
- GitHub Actions automatically validate all metadata and update the index on every push and pull request.
- You can also run the scripts locally:

```bash
# Validate all metadata and templates
python .github/scripts/validate_templates.py

# Update the TEMPLATES.yaml index
python .github/scripts/update_templates_index.py
```

---

## Using Templates with LogForge CLI

### Install a Template Bundle
```bash
logforge install-template paloalto/firewall
```

### Validate a Template and Entities
```bash
logforge validate-template --template paloalto/firewall/network/traffic.j2 --entities entities/entities.yaml
```

### Generate Logs
```bash
logforge generate \
  --template paloalto/firewall/network/traffic.j2 \
  --entities entities/entities.yaml \
  --output-type file --output logs/traffic.log
```

---

## Advanced Template Helpers

LogForge provides a rich set of helper functions for use in your Jinja2 templates. These helpers make it easy to generate realistic, randomized data for your synthetic logs.

**Available Helpers:**

- `random_private_ip([range_name])` — Generate a random private IP address (optionally specify a named range)
- `random_public_ip()` — Generate a random public (non-reserved) IP address
- `random_port([min], [max])` — Generate a random port number (optionally specify min/max)
- `random_mac()` — Generate a random MAC address
- `current_timestamp()` — Get the current Unix timestamp
- `random_email()` — Generate a random email address from your users or fallback
- `random_hostname()` — Generate a random hostname from your devices or fallback
- `random_user()` — Get a random user dict (e.g., `{{ random_user().username }}`)
- `random_device()` — Get a random device dict (e.g., `{{ random_device().ip_address }}`)
- `random_int([min], [max])` — Generate a random integer (default 0–1000)
- `random_guid()` — Generate a random GUID/UUID
- `random_string([length], [chars])` — Generate a random string (default length 10, alphanumeric)
- `registry.get_organization()`, `registry.get_organization_field('domain')`, `registry.get_organization_contact('security')` for organization lookups

**Usage Example:**
```jinja2
User: {{ random_user().username }} ({{ random_user().email }})
Host: {{ random_device().hostname }} ({{ random_device().ip_address }})
Public IP: {{ random_public_ip() }}
Internal IP: {{ random_private_ip('office') }}
Random Port: {{ random_port() }}
Random MAC: {{ random_mac() }}
Random Int: {{ random_int(1000, 9999) }}
Random GUID: {{ random_guid() }}
Random String: {{ random_string(12) }}
Organization: {{ registry.get_organization().name }}
Domain: {{ registry.get_organization_field('domain') }}
Security Contact: {{ registry.get_organization_contact('security') }}
```

---

## Event Generation Frequency and Time Patterns

LogForge uses metadata fields in each template's `.meta.yaml` to control how often events are generated. **All time calculations are in UTC.**

**Key Fields for Event Generation Frequency:**

- `base_frequency` — Number of events per hour (e.g., `60` = 60 events/hour = 1 per minute)
- `time_patterns` — List of time periods to apply multipliers to. Standard values:
  - `business_hours` (Mon–Fri, 9am–5pm UTC)
  - `night_hours` (Mon–Fri, 5pm–9am UTC)
  - `weekend` (all day Saturday and Sunday UTC)
- Multipliers for each period:
  - `business_hours_multiplier` — Multiplier for event rate during business hours
  - `night_hours_multiplier` — Multiplier for event rate during night hours
  - `weekend_multiplier` — Multiplier for event rate during weekends

**Example:**
```yaml
base_frequency: 120   # 120 events per hour (2 per minute)
time_patterns:
  - business_hours
  - night_hours
  - weekend
business_hours_multiplier: 2.0    # 2x during business hours
night_hours_multiplier: 0.5       # 0.5x during night hours
weekend_multiplier: 0.1           # 0.1x during weekends
```

---

## Template Helper Functions

LogForge templates support a wide range of **helper functions** to make your synthetic logs more realistic and dynamic. These helpers allow you to easily generate random data, look up entities, and simulate real-world log patterns—without writing custom Python code.

### Why Use Helper Functions?

- **Alex (Technical Advisor):**  
  Helper functions abstract away common randomization and entity lookup logic, so you can focus on the structure and intent of your log events, not the mechanics of data generation.

- **Maya (Implementation Guide):**  
  Use helpers like `random_email()`, `random_private_ip()`, or `registry.get_random_user()` directly in your Jinja2 templates to inject realistic, varied data with a single line of code.

- **Ethan (Quality Coach):**  
  Helper functions are tested and standardized, reducing the risk of errors and ensuring your templates work consistently across different environments.

### Types of Helpers

- **Entity Lookup Helpers:**  
  Access your defined entities (users, devices, etc.) or use built-in defaults.
  - `registry.get_random_user()`, `registry.get_random_device()`, etc. for entity lookups

- **Randomization Helpers:**  
  Generate realistic values for common log fields.
  - `random_email()`, `random_hostname()`, `random_private_ip()`, etc. for randomization

- **Time and Utility Helpers:**  
  - `current_timestamp()` — Current Unix timestamp

### Example Usage

```jinja2
{
  "user": "{{ registry.get_random_user().username }}",
  "email": "{{ random_email() }}",
  "src_ip": "{{ random_private_ip('office') }}",
  "dst_ip": "{{ random_public_ip() }}",
  "hostname": "{{ random_hostname() }}",
  "event_time": "{{ current_timestamp() }}",
  "session_id": "{{ random_guid() }}"
}
```

### Best Practices

- **Sara (Solution Architect):**  
  Use helpers to keep your templates portable and maintainable—no need to hardcode values or write custom logic for each template.

- **Nina (Project Organizer):**  
  For a full, always up-to-date list of available helpers (including advanced and registry helpers), see the [main LogForge README](https://github.com/Fulcrum-Technology-Solutions/LogForge/blob/main/README.md#advanced-template-helpers).

> **Tip:** If you're unsure which helper to use, check the main LogForge documentation or look at examples in the `examples/` directory.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to add or modify templates, metadata, and collections.
- Follow the structure and metadata requirements in the `examples/` and `schemas/` directories.
- Validate your files before submitting a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
