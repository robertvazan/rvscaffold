# Python Project Guidelines

These are guidelines for structuring Python projects, building upon the [general project guidelines](../README.md).

## Project Structure

A typical Python project is organized as follows:

- `{projectname}/`: A directory containing the main Python package.
- `tests/`: A directory for the test project. The directory structure within `tests/` should mirror the main package.
- `requirements.txt`: A file listing the project's dependencies.
- The root directory also contains standard files like `README.md`, `CONTRIBUTING.md`, `LICENSE`, and `COPYRIGHT`.

## Dependencies

Project dependencies are managed in a `requirements.txt` file. This includes both application dependencies and development dependencies like `pytest`.

## Coding Conventions

- **Docstrings**: All modules, classes, and functions should have Google-style docstrings.
- **Imports**: Use fully qualified module names in imports and import individual symbols rather than whole modules (e.g., `from projectname.utils.config import REQUEST_TIMEOUT`).
- **Multiline Strings**: Use `textwrap.dedent()` to clean up indentation in multiline strings.

## Unit Tests

- Unit tests should be written using the [pytest](https://docs.pytest.org/) framework.
- Tests should be placed in the `tests/` directory.
- Pytest tests should usually be plain global functions rather than classes.

## Standard Files

- **`.gitignore`:** Add Python-specific patterns to the project's `.gitignore` file. See the [Python .gitignore example](example-gitignore.txt) for a minimal set of patterns to include.
- **GitHub Actions:** Projects use GitHub Actions for Continuous Integration (CI). See the example [build workflow](example-build.yml).

## Example Project

For example project applying these guidelines, see [llobot](https://github.com/robertvazan/llobot).
