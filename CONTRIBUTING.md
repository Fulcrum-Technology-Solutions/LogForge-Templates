# Contributing to LogForge Templates

Thank you for your interest in contributing to LogForge Templates! This document provides guidelines for creating and submitting new templates.

## Table of Contents
- [Repository Structure](#repository-structure)
- [Adding a New Template](#adding-a-new-template)
- [Metadata Files](#metadata-files)
- [Template Testing & Validation](#template-testing--validation)
- [Updating collection.json](#updating-collectionjson)
- [Archive Directory Policy](#archive-directory-policy)
- [Template Naming Conventions](#template-naming-conventions)
- [Field Documentation Requirements](#field-documentation-requirements)
- [Pull Request Process](#pull-request-process)
- [PR Checklist](#pr-checklist)
- [Community Standards](#community-standards)

---

## Repository Structure

Templates are organized in a 4-tier structure:
- Vendor (e.g., `microsoft`)
- Product (e.g., `windows`)
- Data Source (e.g., `security`)
- Template files (e.g., `account_locked.j2`, `account_locked.meta.yaml`)

See the `examples/` directory for a complete sample structure and files.

## Adding a New Template

### To an Existing Vendor/Product

1. Navigate to the appropriate `vendor/product/data_source` directory
2. Create your template file (`.j2`) and its metadata file (`.meta.yaml`)
3. Update the product's `collection.json` to include your new template

### For a New Vendor/Product

1. Create the directory structure: `vendor/product/data_source/`
2. Create a `vendor.meta.yaml` in the vendor directory
3. Create a `product.meta.yaml` in the product directory
4. Create a `collection.json` in the product directory
5. Add your template `.j2` and `.meta.yaml` files in the data source directory

## Metadata Files

Each level has its own metadata file:

1. Vendor level: `vendor.meta.yaml`
2. Product level: `product.meta.yaml`
3. Package level: `collection.json`
4. Template level: `template_name.meta.yaml`

See the `schemas/` directory for the required fields for each file.

## Template Testing & Validation

### Local Validation

Before submitting a PR, validate your metadata files:

```bash
# Run validation script (excludes archive/ and examples/)
python .github/scripts/validate_templates.py
```

This will check:
- All metadata files conform to their schemas
- Required fields are present
- Enum values are valid (e.g., `frequency` must be: critical, high, medium, low)
- Directory names match metadata fields (vendor/product/data_source)

### Testing Template Rendering

1. **Install LogForge CLI** (if not already installed):
   ```bash
   pip install logforge
   ```

2. **Create a test entity file** (`test_entities.yaml`):
   ```yaml
   organization:
     name: "Test Organization"
     domain: "test.example.com"
   users:
     - username: "alice"
       email: "alice@test.example.com"
     - username: "bob"
       email: "bob@test.example.com"
   devices:
     - hostname: "workstation-01"
       ip_address: "192.168.1.10"
   ```

3. **Test your template**:
   ```bash
   # View template info
   logforge templates info <vendor>/<product>/<data_source>/<template_name>
   
   # Generate sample output (if LogForge supports direct generation)
   # Check main LogForge documentation for current CLI commands
   ```

4. **Verify output format**:
   - JSON templates should produce valid JSON
   - Syslog templates should follow RFC 5424 or RFC 3164 format
   - CSV templates should have consistent column structure
   - All timestamps should be valid
   - All IP addresses should be valid format

### Common Validation Errors

- **Missing required field**: Check schema for required fields
- **Invalid enum value**: `frequency` must be one of: `critical`, `high`, `medium`, `low`
- **Directory mismatch**: `vendor`, `product`, `data_source` in metadata must match directory names
- **Invalid format**: `format` must be one of: JSON, XML, CSV, Syslog, CEF, LEEF, Plain Text, Custom
- **Schema structure**: Ensure nested objects (like `documentation.resources`) match schema exactly

GitHub Actions will automatically validate your templates and update the `TEMPLATES.yaml` index file on every push and pull request. Validation failures will block merging.

## Updating collection.json

When adding or removing templates, you must update the product's `collection.json` file.

### Required Fields

- `name`: Collection name in format `{vendor}-{product}` (e.g., `paloalto-wildfire`)
- `version`: Semantic version (e.g., `1.0.0`, `1.1.0`)
- `templates`: Array of template paths in format `{data_source}/{template_name}` (without `.j2` extension)
- `maintainers`: Array of maintainer objects with `name` and `email` (required), `github` (optional)

### Template Path Format

Template paths in `collection.json` must be relative to the product directory:
- Format: `{data_source}/{template_name}` (no `.j2` extension)
- Example: `threats/wildfire_threat_detected` (not `threats/wildfire_threat_detected.j2`)

### Versioning Guidelines

- **Patch version** (1.0.0 → 1.0.1): Bug fixes, minor template updates
- **Minor version** (1.0.0 → 1.1.0): New templates added, non-breaking changes
- **Major version** (1.0.0 → 2.0.0): Breaking changes, major template restructures

### Example collection.json

```json
{
  "name": "paloalto-wildfire",
  "version": "1.0.0",
  "description": "Palo Alto WildFire threat detection templates",
  "maintainers": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "github": "johndoe"
    }
  ],
  "tags": ["wildfire", "threat", "malware", "security"],
  "templates": [
    "threats/wildfire_threat_detected"
  ]
}
```

## Archive Directory Policy

The `archive/` directory contains deprecated or legacy templates that are no longer actively maintained but preserved for reference.

### When to Archive

- Templates that are superseded by newer versions
- Templates for deprecated product versions
- Templates that no longer match current log formats
- Templates with known issues that won't be fixed

### How to Archive

1. Move the entire vendor/product directory to `archive/`
2. **Do not** update `collection.json` for archived templates
3. **Do not** include archived templates in `TEMPLATES.yaml` (automatically excluded)
4. Add a note in your PR explaining why templates were archived

### Archive Structure

```
archive/
  vendor/
    product/
      [templates...]
```

**Note:** Archived templates are excluded from:
- Validation scripts
- Template indexing
- Community API sync
- Package downloads

## Template Naming Conventions

### File Names

- **Template files**: Use lowercase with underscores (e.g., `user_login.j2`, `threat_detected.j2`)
- **Metadata files**: Match template name (e.g., `user_login.meta.yaml`)
- **Avoid**: Spaces, special characters (except underscores and hyphens), mixed case

### Directory Names

- **Vendor**: Lowercase, alphanumeric, hyphens only (e.g., `paloalto`, `microsoft`, `acme-health`)
- **Product**: Lowercase, alphanumeric, hyphens only (e.g., `wildfire`, `windows-server`, `pan-os`)
- **Data Source**: Lowercase, alphanumeric, underscores and hyphens (e.g., `user_activity`, `network-security`)

### Metadata Fields

- `vendor`: Must match vendor directory name exactly
- `product`: Must match product directory name exactly
- `data_source`: Must match data source directory name exactly
- Use lowercase, alphanumeric, hyphens/underscores only

## Field Documentation Requirements

Template metadata should include comprehensive field documentation for UI rendering and user understanding.

### Required Documentation Sections

1. **display** (under `documentation.display`):
   - `title`: Clear, descriptive title
   - `subtitle`: Brief subtitle (optional but recommended)
   - `icon`: Emoji or icon identifier
   - `color_scheme`: One of: success, warning, error, info
   - `tags`: Array of searchable tags

2. **overview** (under `documentation.overview`):
   - `summary`: Brief description of what the template generates
   - `when_generated`: Array of scenarios when this event occurs
   - `security_relevance`: One of: Critical, High, Medium, Low, Informational
   - `compliance_frameworks`: Array of relevant frameworks (e.g., "SOC 2", "PCI DSS")
   - `frequency_notes`: Notes about frequency patterns

3. **fields** (under `documentation.fields`):
   - Each significant field in the template output should be documented
   - Required fields: `name`, `type`, `description`
   - Recommended: `example_value`, `format`, `template_source`
   - Optional: `possible_values` for enum-like fields

4. **resources** (under `documentation.resources`):
   - `documentation`: Array of documentation links
   - `tools`: Array of related tools

### Field Documentation Example

```yaml
documentation:
  fields:
    - name: "user_id"
      type: "String"
      required: true
      description: "Unique identifier for the user"
      example_value: "alice@example.com"
      format: "Email address"
      template_source: "registry.get_random_user().email"
    - name: "severity"
      type: "String"
      required: true
      description: "Event severity level"
      example_value: "high"
      possible_values:
        - value: "low"
          description: "Low severity event"
        - value: "medium"
          description: "Medium severity event"
        - value: "high"
          description: "High severity event"
```

## Pull Request Process

1. **Fork the repository**
2. **Create your feature branch**:
   ```bash
   git checkout -b feature/add-new-template
   ```
3. **Make your changes**:
   - Add/modify templates and metadata
   - Update `collection.json` if adding new templates
   - Follow naming conventions and structure requirements
4. **Test locally**:
   - Run validation: `python .github/scripts/validate_templates.py`
   - Test template rendering if possible
5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add new template: vendor/product/data_source/template_name"
   ```
6. **Push to your branch**:
   ```bash
   git push origin feature/add-new-template
   ```
7. **Submit a Pull Request**:
   - Use a clear, descriptive title
   - Describe what templates were added/modified
   - Reference any related issues
   - Ensure all checks pass (validation, indexing)

## PR Checklist

Before submitting your PR, ensure:

- [ ] All metadata files pass validation (`python .github/scripts/validate_templates.py`)
- [ ] Template files (`.j2`) are syntactically correct Jinja2
- [ ] Metadata fields match directory structure (vendor/product/data_source)
- [ ] `collection.json` is updated if adding/removing templates
- [ ] `collection.json` version is incremented appropriately
- [ ] Template naming follows conventions (lowercase, underscores)
- [ ] Field documentation is complete (at minimum: name, type, description)
- [ ] Required metadata fields are present (vendor, product, data_source, description, format)
- [ ] Frequency enum value is valid (critical, high, medium, low)
- [ ] Format enum value is valid (JSON, XML, CSV, Syslog, CEF, LEEF, Plain Text, Custom)
- [ ] Resources are properly nested under `documentation.resources`
- [ ] No references to deprecated `meta.schema.json` (use `template.schema.json`)
- [ ] Template has been tested locally (if possible)
- [ ] PR description explains what was added/changed

## Community Standards

- **Be respectful and constructive** in all communications
- **Help others** by reviewing pull requests and answering questions
- **Report bugs** and suggest improvements using GitHub Issues
- **Follow the code of conduct** and maintain a welcoming environment
- **Document your changes** clearly in PR descriptions

## Getting Help

- **Questions?** Open a GitHub Discussion or Issue
- **Found a bug?** Report it with steps to reproduce
- **Need clarification?** Ask in your PR and maintainers will help

Thank you for helping make LogForge Templates better! 