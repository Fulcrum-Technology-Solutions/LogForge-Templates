# LogForge Templates

This repository contains community-contributed templates for [LogForge](https://github.com/Fulcrum-Technology-Solutions/LogForge), a synthetic event log generator.

> **Note:** LLM-powered (AI-assisted) template creation, analysis, and metadata generation are only available in the Enterprise version (future separate repository), and only via the web UI (not CLI). The open-source version does not include any Enterprise-only features.

---

## LogForge Template Hierarchy: 4-Tier System

LogForge Templates are organized in a strict 4-level hierarchy, which is reflected in both the directory structure and the API/UI:

1. **Vendor**: The organization or company that produces the product (e.g., `paloalto`, `microsoft`, `acme`).
   - Directory: `vendor/`
   - Metadata: `vendor.meta.yaml`
2. **Product**: The specific product or application from the vendor (e.g., `firewall`, `windows`, `secureapp-pro`).
   - Directory: `vendor/product/`
   - Metadata: `product.meta.yaml`, `collection.json`
3. **Data Source**: The subsystem, log type, or event source within the product (e.g., `network`, `security`, `user-authentication`).
   - Directory: `vendor/product/data_source/`
4. **Event Type (Template)**: The specific event type or log template (e.g., `traffic`, `vpn`, `user_login`).
   - Files: `template_name.j2` (Jinja2 template), `template_name.meta.yaml` (metadata)

**Example Path:**
```
paloalto/firewall/network/traffic.j2
paloalto/firewall/network/traffic.meta.yaml
```

Each level has its own metadata file (see `schemas/`), and the template-level meta.yaml must conform to `template.schema.json`.

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
- The `archive/` and `examples/` directories are excluded from validation (see [Template Validation & Automation](#template-validation--automation)).

---

## Template Metadata Schema (`template.schema.json`)

All template-level `meta.yaml` files must conform to the JSON schema defined in [`schemas/template.schema.json`](schemas/template.schema.json). This schema enforces the required structure, field types, and allowed values for template metadata, including:

- Basic identification fields (vendor, product, data_source, description, format)
- Event generation frequency and time pattern fields
- Detailed documentation and field definitions for UI and developer guidance
- External resources and tools

**Location:** `schemas/template.schema.json`

**Validation:**
You can validate any `meta.yaml` file against the schema using a Python script with `pyyaml` and `jsonschema`. Example script:

```python
import yaml
import json
import jsonschema
from pathlib import Path

SCHEMA_PATH = Path("schemas/template.schema.json")

def validate_meta_yaml(yaml_path):
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    jsonschema.validate(instance=data, schema=schema)
    print(f"{yaml_path} is valid.")

# Usage:
# python validate_meta_yaml.py path/to/meta.yaml
```

**Required fields and structure:**
See the schema file for the full list of required and optional fields, types, and nested objects. Key required fields include:
- `vendor`, `product`, `data_source` (must match directory structure)
- `description` (10-500 characters)
- `format` (enum: JSON, XML, CSV, Syslog, CEF, LEEF, Plain Text, Custom)

Optional fields include:
- `frequency` (enum: critical, high, medium, low)
- `is_generator` (boolean, default: false)
- `base_frequency`, `time_patterns`, and multiplier fields (for generator templates)

**Contributing:**
All new or updated template-level `meta.yaml` files must pass schema validation before being merged. See [CONTRIBUTING.md](./CONTRIBUTING.md) for more details.

---

## Template Authoring & Contribution

To contribute a new template:
- Place your `.j2` template and its `.meta.yaml` metadata file as described in the [Template Structure & Requirements](#template-structure--requirements) section (e.g., `paloalto/firewall/network/`).
- All metadata files must conform to their respective schemas (see [Schema Validation](#schema-validation)).
- Use realistic field names and reference entities using the `registry` object (e.g., `{{ registry.get_random_user().username }}` or `{{ fake.email() }}`).
- Test your template with sample entity files and run validation:
  ```bash
  # Validate metadata files
  python .github/scripts/validate_templates.py
  
  # Test template rendering (requires LogForge CLI)
  logforge templates info <vendor>/<product>/<data_source>/<template_name>
  ```

**Minimal Example:**

Template (`example_log.j2`):
```jinja2
{{ now() | iso8601 }} {{ fake.email() }} {{ random_hostname() }} {{ registry.get_random_user().username }}
```

Metadata (`example_log.meta.yaml`):
```yaml
vendor: paloalto
product: firewall
data_source: network
description: Example log template for demonstration
format: Syslog
frequency: medium  # Valid values: critical, high, medium, low
is_generator: true
base_frequency: 10
time_patterns:
  - business_hours
documentation:
  display:
    title: "Example Log Event"
    subtitle: "Demonstration of LogForge Template Structure"
    icon: "📝"
    color_scheme: "info"
    tags:
      - "demo"
      - "example"
  overview:
    summary: "This event is generated for demonstration purposes."
    when_generated:
      - "When running LogForge in demo mode."
    security_relevance: "Low"
    compliance_frameworks:
      - "N/A"
    frequency_notes: "This is a low-frequency, demo-only event."
  fields:
    - name: "timestamp"
      type: "DateTime"
      required: true
      description: "Event timestamp in ISO8601 format."
      example_value: "2025-01-01T00:00:00Z"
      format: "ISO 8601"
      template_source: "now() | iso8601"
    - name: "device_id"
      type: "String"
      required: true
      description: "Unique identifier for the device."
      example_value: "device-1234"
      template_source: "device_id"
  resources:
    documentation:
      - title: "LogForge Template Authoring Guide"
        url: "https://github.com/Fulcrum-Technology-Solutions/LogForge"
        type: "official"
    tools:
      - name: "LogForge CLI"
        description: "Command-line tool for template validation and log generation."
        url: "https://github.com/Fulcrum-Technology-Solutions/LogForge"
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

If a template references a registry function (e.g., `registry.get_random_user()`) and no users are defined in your `entities.yaml`, LogForge will return an empty dict `{}` and print a warning. Ensure your `entities.yaml` file includes the required entities (users, devices, services) for your templates to work correctly.

---

## Template Validation & Automation

- The `TEMPLATES.yaml` file is auto-generated and provides a complete index of all templates in the repository.
- **Do not edit `TEMPLATES.yaml` manually.**
- **Do not use generate_template_index.py; it is deprecated and has been removed.**
- The only supported script for index generation is `.github/scripts/update_templates_index.py`.
- GitHub Actions automatically validate all metadata and update the index on every push and pull request.
- **Note:** The `archive/` and `examples/` directories are excluded from validation and indexing.
- You can also run the scripts locally:

```bash
# Validate all metadata and templates (excludes archive/ and examples/)
python .github/scripts/validate_templates.py

# Update the TEMPLATES.yaml index
python .github/scripts/update_templates_index.py
```

**Validation Failures:**
If validation fails, GitHub Actions will report the errors. Common issues:
- Missing required fields in metadata files
- Invalid enum values (e.g., `frequency` must be one of: critical, high, medium, low)
- Schema structure mismatches
- Directory name mismatches with metadata fields (vendor/product/data_source must match directory names)

---

## Using Templates with LogForge CLI

### Search for Templates
```bash
# Search all templates
logforge templates search "windows"

# Search by vendor
logforge templates search --vendor paloalto "firewall"

# Browse templates interactively
logforge templates browse
```

### Install Templates
```bash
# Install entire vendor package
logforge templates install paloalto

# Install specific product
logforge templates install aws/cloudtrail

# List available vendors
logforge templates install --list-vendors
```

### View Template Information
```bash
# Get template details
logforge templates info paloalto/wildfire/threats/wildfire_threat_detected

# List all local templates
logforge templates list

# Compare local vs remote templates
logforge templates compare
```

### Generate Logs
Templates are used via LogForge generators configured in `config.yaml`. See the [main LogForge documentation](https://github.com/Fulcrum-Technology-Solutions/LogForge) for generator configuration.

---

## Advanced Template Helpers

LogForge provides a rich set of helper functions for use in your Jinja2 templates. These helpers make it easy to generate realistic, randomized data for your synthetic logs.

**Available Helpers:**

**Random Generation:**
- `random_public_ip()` — Generate a random public (non-reserved) IP address
- `random_private_ip()` — Generate a random private IP address (RFC 1918 ranges)
- `random_port([min], [max])` — Generate a random port number (default: 1024-65535)
- `random_hostname()` — Generate a random hostname (e.g., DESKTOP-XXXXX)
- `random_int(min, max)` — Generate a random integer (both parameters required)
- `random_string([length], [chars])` — Generate a random string (default length 10, alphanumeric)
- `random_guid()` — Generate a random GUID/UUID
- `random_hex(min, max)` — Generate a random hexadecimal value with '0x' prefix
- `random_choice(choices)` — Choose random item from list
- `random_weighted(choices, weights)` — Choose random item based on weights

**DateTime:**
- `now()` — Get current datetime (timezone-aware, returns DateTimeWrapper)
- `current_timestamp()` — Alias for `now()` (returns DateTimeWrapper, not Unix timestamp)
- `format_datetime(dt, format)` — Format datetime with strftime format string
- `iso8601(dt, [include_microseconds])` — Format as ISO 8601
- `iso8601_utc(dt, [include_microseconds])` — Format as ISO 8601 with UTC Z suffix
- `rfc3339(dt)` — Format as RFC 3339
- `unix_timestamp(dt)` — Convert to Unix timestamp
- `add_seconds(dt, seconds)` — Add seconds to datetime
- `subtract_seconds(dt, seconds)` — Subtract seconds from datetime

**Registry Functions:**
- `registry.get_random_user()` — Get a random user dict (e.g., `{{ registry.get_random_user().username }}`)
- `registry.get_random_device()` — Get a random device dict (e.g., `{{ registry.get_random_device().ip_address }}`)
- `registry.get_random_service()` — Get a random service dict
- `registry.get_user(username)` — Get specific user by username
- `registry.get_device(hostname)` — Get specific device by hostname
- `registry.get_service(name)` — Get specific service by name
- `registry.get_all_users()` — Get all users as list
- `registry.get_all_devices()` — Get all devices as list
- `registry.get_all_services()` — Get all services as list
- `registry.get_organization()` — Get organization dict
- `registry.get_organization_field(field)` — Get specific organization field (supports dot notation)
- `registry.get_organization_contact(role)` — Get organization contact for role (e.g., 'security', 'admin')
- `registry.get_network_ranges()` — Get network ranges configuration

**Faker Library:**
- `fake.email()` — Random email address
- `fake.mac_address()` — Random MAC address
- `fake.name()` — Random person name
- `fake.ipv4()` — Random IPv4 address
- `fake.ipv6()` — Random IPv6 address
- `fake.url()` — Random URL
- `fake.user_agent()` — Random user agent string
- `fake.file_path()` — Random file path
- `fake.uuid4()` — Random UUID
- (See Faker documentation for full list of available methods)

**Usage Example:**
```jinja2
User: {{ registry.get_random_user().username }} ({{ registry.get_random_user().email }})
Host: {{ registry.get_random_device().hostname }} ({{ registry.get_random_device().ip_address }})
Public IP: {{ random_public_ip() }}
Internal IP: {{ random_private_ip() }}
Random Port: {{ random_port() }}
Random MAC: {{ fake.mac_address() }}
Random Int: {{ random_int(1000, 9999) }}
Random GUID: {{ random_guid() }}
Random String: {{ random_string(12) }}
Timestamp: {{ now() | iso8601 }}
Organization: {{ registry.get_organization().name }}
Domain: {{ registry.get_organization_field('domain') }}
Security Contact: {{ registry.get_organization_contact('security') }}
Email: {{ fake.email() }}
```

---

## Event Generation Frequency and Time Patterns

LogForge uses metadata fields in each template's `.meta.yaml` to control how often events are generated. **Time calculations use the organization's timezone (from `entities.yaml`), defaulting to UTC if not specified.**

**Key Fields for Event Generation Frequency:**

- `frequency` — General categorization (enum: `critical`, `high`, `medium`, `low`)
- `base_frequency` — Number of events per hour (e.g., `60` = 60 events/hour = 1 per minute)
- `time_patterns` — List of time periods to apply multipliers to. Standard values:
  - `business_hours` (Mon–Fri, 9am–5pm)
  - `night_hours` (Mon–Fri, 5pm–9am next day)
  - `weekend` (all day Saturday and Sunday)
- Multipliers for each period:
  - `business_hours_multiplier` — Multiplier for event rate during business hours (default: 1.0)
  - `night_hours_multiplier` — Multiplier for event rate during night hours (default: 1.0)
  - `weekend_multiplier` — Multiplier for event rate during weekends (default: 1.0)

**Pattern Priority:**
Time patterns are evaluated in priority order: `business_hours` > `weekend` > `night_hours`. If no pattern matches, the base rate is used without any multiplier.

**Example:**
```yaml
base_frequency: 120   # 120 events per hour (2 per minute)
time_patterns:
  - business_hours
  - night_hours
  - weekend
business_hours_multiplier: 2.0    # 2x during business hours (240 events/hour)
night_hours_multiplier: 0.5       # 0.5x during night hours (60 events/hour)
weekend_multiplier: 0.1           # 0.1x during weekends (12 events/hour)
```

---

## Template Helper Functions

LogForge templates support a wide range of **helper functions** to make your synthetic logs more realistic and dynamic. These helpers allow you to easily generate random data, look up entities, and simulate real-world log patterns—without writing custom Python code.

### Why Use Helper Functions?

- **Alex (Technical Advisor):**  
  Helper functions abstract away common randomization and entity lookup logic, so you can focus on the structure and intent of your log events, not the mechanics of data generation.

- **Maya (Implementation Guide):**  
  Use helpers like `fake.email()`, `random_private_ip()`, or `registry.get_random_user()` directly in your Jinja2 templates to inject realistic, varied data with a single line of code.

- **Ethan (Quality Coach):**  
  Helper functions are tested and standardized, reducing the risk of errors and ensuring your templates work consistently across different environments.

### Types of Helpers

- **Entity Lookup Helpers:**  
  Access your defined entities (users, devices, services) from the registry.
  - `registry.get_random_user()`, `registry.get_random_device()`, `registry.get_random_service()`, etc. for entity lookups
  - `registry.get_user(username)`, `registry.get_device(hostname)`, `registry.get_service(name)` for specific entity lookups

- **Randomization Helpers:**  
  Generate realistic values for common log fields.
  - `fake.email()`, `random_hostname()`, `random_private_ip()`, `random_public_ip()`, etc. for randomization
  - See [Advanced Template Helpers](#advanced-template-helpers) section above for complete list

- **Time and Utility Helpers:**  
  - `now()` — Current datetime (timezone-aware, returns DateTimeWrapper)
  - `current_timestamp()` — Alias for `now()` (returns DateTimeWrapper, not Unix timestamp)
  - Use filters like `iso8601`, `format_datetime` to format datetime values

### Example Usage

```jinja2
{
  "user": "{{ registry.get_random_user().username }}",
  "email": "{{ fake.email() }}",
  "src_ip": "{{ random_private_ip() }}",
  "dst_ip": "{{ random_public_ip() }}",
  "hostname": "{{ random_hostname() }}",
  "event_time": "{{ now() | iso8601 }}",
  "session_id": "{{ random_guid() }}"
}
```

### Best Practices

- **Sara (Solution Architect):**  
  Use helpers to keep your templates portable and maintainable—no need to hardcode values or write custom logic for each template.

- **Nina (Project Organizer):**  
  For a full, always up-to-date list of available helpers (including advanced and registry helpers), see the [Advanced Template Helpers](#advanced-template-helpers) section above.

> **Tip:** If you're unsure which helper to use, check the [Advanced Template Helpers](#advanced-template-helpers) section above or look at examples in the `examples/` directory.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to add or modify templates, metadata, and collections.
- Follow the structure and metadata requirements in the `examples/` and `schemas/` directories.
- Validate your files before submitting a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## LogForge Template Package Format (.forge)

When you download a vendor package from the registry, you will receive a file with the `.forge` extension (e.g., `crowdstrike.forge`). This is a **LogForge Template package**—a gzipped tar archive containing all templates, metadata, and subfolders for the vendor.

- `.forge` files are fully compatible with standard archive tools (e.g., `tar`, `7-Zip`, `WinRAR`).
- To extract on the command line:
  ```bash
  tar -xzf crowdstrike.forge
  # or rename to .tar.gz and extract as usual
  mv crowdstrike.forge crowdstrike.tar.gz
  tar -xzf crowdstrike.tar.gz
  ```
- The `.forge` extension helps users and tools recognize LogForge Template packages.

> **Tip:** You can import `.forge` files directly into LogForge or extract them manually for inspection.