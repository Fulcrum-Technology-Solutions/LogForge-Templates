# Contributing to LogForge Templates

Thank you for your interest in contributing to LogForge Templates! This document provides guidelines for creating and submitting new templates.

## Table of Contents
- [Repository Structure](#repository-structure)
- [Adding a New Template](#adding-a-new-template)
- [Metadata Files](#metadata-files)
- [Template Testing & Validation](#template-testing--validation)
- [Pull Request Process](#pull-request-process)
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

Before submitting a PR:
1. Validate your metadata files using:
   ```bash
   python .github/scripts/validate_templates.py
   ```
2. Test your template with LogForge to ensure it generates valid logs

GitHub Actions will automatically validate your templates and update the `TEMPLATES.yaml` index file on every push and pull request.

## Pull Request Process

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to your branch
5. Submit a Pull Request

## Community Standards
- Be respectful and constructive in all communications.
- Help others by reviewing pull requests and answering questions.
- Report bugs and suggest improvements using GitHub Issues.

Thank you for helping make LogForge Templates better! 