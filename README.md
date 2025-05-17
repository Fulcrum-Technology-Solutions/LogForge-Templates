# LogForge Templates

A comprehensive collection of log templates for generating realistic log data across various vendors, products, and data sources.

## Overview

LogForge Templates provides a standardized repository of Jinja2 templates for generating realistic logs that mimic many popular security and infrastructure products. These templates can be used with log generation tools to create sample data for testing, demos, and development.

## Repository Structure

Templates are organized in a consistent four-level directory structure:

```
/vendor/product/data_source/template_name.j2
```

For example:
- `/microsoft/windows/security/login/login_success.j2`
- `/paloalto/globalprotect/vpn/globalprotect.j2`

Each template has a corresponding metadata file (`.meta.yaml`) with the same name, containing information about the template, parameters, and generation settings.

Package metadata at the vendor/product level is stored in `package.json` files.

## Available Templates

The repository includes templates for logs from:

- **Cloud Providers**: Microsoft Azure (Active Directory)
- **Operating Systems**: Microsoft Windows (Security, System, Application logs)
- **Network Security**: Palo Alto Networks (GlobalProtect, Traffic, WildFire)
- **Identity**: Microsoft Azure AD
- **Email Security**: Microsoft Office 365

See the [TEMPLATES.yaml](TEMPLATES.yaml) file for a complete index of all templates.

## Getting Started

### Using Templates

1. Clone this repository:
   ```
   git clone https://github.com/Fulcrum-Technology-Solutions/LogForge-Templates.git
   ```

2. Browse available templates in the directory structure or refer to `TEMPLATES.yaml` for a complete index.

3. Use the templates with your log generation tool or framework. Each template is designed to be used with Jinja2 templating.

### Template Structure

Each template has two components:

1. **Template File (`.j2`)**: Jinja2 template that defines the log format and structure
2. **Metadata File (`.meta.yaml`)**: YAML file containing metadata about the template

### Example Template & Metadata

Example template (`microsoft/windows/security/login/login_success.j2`):
```jinja2
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
  <System>
    <Provider Name="Microsoft-Windows-Security-Auditing" Guid="{54849625-5478-4994-A5BA-3E3B0328C30D}" />
    <EventID>{{ event_id }}</EventID>
    <TimeCreated SystemTime="{{ timestamp }}" />
    <Computer>{{ hostname }}</Computer>
  </System>
  <EventData>
    <Data Name="TargetUserName">{{ username }}</Data>
    <Data Name="TargetDomainName">{{ domain }}</Data>
    <Data Name="LogonType">{{ logon_type }}</Data>
    <Data Name="WorkstationName">{{ hostname }}</Data>
    <Data Name="IpAddress">{{ ip_address }}</Data>
    <Data Name="IpPort">{{ random_port() }}</Data>
  </EventData>
</Event>
```

Example metadata (`microsoft/windows/security/login/login_success.meta.yaml`):
```yaml
name: Security Login Success
description: Windows Security successful login events (EventID 4624)
log_type: security
author: Fulcrum Technology Solutions
version: 1.0.0
product: Windows
vendor: Microsoft
tags:
  - microsoft
  - windows
  - security
  - login
  - success
date_created: '2025-05-16'
last_updated: '2025-05-16'
fields:
  - field: username
    description: The username of the user logging in
  - field: domain
    description: The domain of the user
  - field: hostname
    description: The hostname of the machine
  - field: ip_address
    description: Source IP address of the login
```

## Template Index

Use the `generate_template_index.py` script to generate or update the `TEMPLATES.yaml` file, which provides a complete index of all templates in the repository.

```bash
# Activate your virtual environment if needed
source .venv/bin/activate

# Generate the template index
python generate_template_index.py
```

## Contributing

Contributions to LogForge Templates are welcome\! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b my-new-template`)
3. Add your templates following the repository structure
4. Update `TEMPLATES.yaml` by running the generate script
5. Commit your changes (`git commit -am 'Add new template for XYZ'`)
6. Push to the branch (`git push origin my-new-template`)
7. Create a new Pull Request

### Template Guidelines

When creating new templates, follow these guidelines:

1. Follow the established directory structure: `/vendor/product/data_source/template_name.j2`
2. Create a metadata file (`.meta.yaml`) for each template
3. Update or create a `package.json` file in the product directory
4. Ensure the template renders valid logs when provided with appropriate parameters
5. Include example parameters in the metadata file

## License

This project is licensed under the MIT License - see the LICENSE file for details.
