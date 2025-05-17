# Contributing to LogForge

Thank you for your interest in contributing to LogForge! We welcome both code and template contributions. Please follow these guidelines to help us maintain a high-quality, user-friendly project.

## Table of Contents
- [How to Contribute](#how-to-contribute)
- [Code Contributions](#code-contributions)
- [Template Contributions](#template-contributions)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Schema Validation](#schema-validation)
- [Pull Request Process](#pull-request-process)
- [Community Standards](#community-standards)

---

## How to Contribute
1. **Check [Issues.md](./Issues.md) and [Tasks.md](./Tasks.md)** for open tasks or bugs.
2. **Fork the repository** and create a new branch for your changes.
3. **Make your changes** (see below for details).
4. **Test your changes** locally.
5. **Update documentation** as needed.
6. **Submit a pull request** (or share your patch if not using GitHub).

---

## Code Contributions
- Follow the existing project structure (`core/`, `cli/`, `entities/`, `templates/`, `configs/`, `tests/`).
- Use clear, descriptive commit messages.
- Add or update unit tests for new features or bug fixes.
- Run all tests with `pytest` before submitting.
- Ensure your code passes schema validation (see below).
- Add docstrings and comments for clarity.

---

## Template Contributions
- Place new templates in the correct vendor/product/data_source directory (e.g., `templates/microsoft/windows/security/`).
- Each template (`.j2` file) **must** have a corresponding `.meta.yaml` file with required metadata fields:
  - `name`: Template name
  - `description`: Short description
  - `log_type`: e.g., security, application, network
  - `author`: Your name or handle
  - `version`: Template version (e.g., 1.0.0)
- Use realistic field names and values in your templates.
- Reference entities using the `entities` object (e.g., `{{ entities.users[0] }}` or `{{ random_email() }}`).
- Test your template with sample entity files and run validation:
  ```bash
  logforge validate-template --template <path-to-template> --entities <path-to-entities.yaml>
  ```
- See the [README.md](./README.md) for advanced helpers and authoring tips.

### Example Template and Metadata
**Template:**
```jinja2
{{ current_timestamp() }} {{ random_email() }} {{ random_hostname() }} {{ registry.get_random_user() }}
```
**Metadata (`.meta.yaml`):**
```yaml
name: Example Log
description: Example log template for demonstration
log_type: application
author: Your Name
version: 1.0.0
```

---

## Coding Standards
- Use 4 spaces for indentation (no tabs).
- Follow PEP8 style guidelines for Python code.
- Use descriptive variable and function names.
- Add comments explaining "why" for non-obvious logic.

---

## Testing
- All new code should include unit tests (see `tests/` directory).
- Use `pytest` for all tests.
- For templates, add sample entity files and test rendering.
- Run all tests before submitting:
  ```bash
  pytest
  ```

---

## Schema Validation
- LogForge uses [Pydantic](https://docs.pydantic.dev/) to validate entity and metadata files.
- Ensure your entity YAML and template metadata files conform to the documented schema (see README).
- Validation errors will be shown in the CLI if your files are invalid.

---

## Pull Request Process
1. Fork the repository and create a new branch.
2. Make your changes and commit them with clear messages.
3. Run all tests and validation scripts.
4. Open a pull request and describe your changes.
5. Reference any related issues or tasks.
6. Respond to feedback and make any requested changes.

---

## Community Standards
- Be respectful and constructive in all communications.
- Help others by reviewing pull requests and answering questions.
- Report bugs and suggest improvements in [Issues.md](./Issues.md).

Thank you for helping make LogForge better! 