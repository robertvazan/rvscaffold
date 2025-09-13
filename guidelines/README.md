# Project Guidelines

This document is the main entry point to a set of guidelines for structuring projects. These guidelines are intended to be interpreted by Large Language Models (LLMs) to assist with software development, but they are also human-readable.

## General Files

All projects, regardless of language, should contain some standard files in their root directory.

### `README.md`

The `README.md` file is the front page of the project. It should include:

-   A Stand with Ukraine banner.
-   The project's pretty name as a level 1 heading.
-   Badges for build status, package registry versions, test coverage, etc.
-   A short description of the project.
-   A "Status" section describing the project's maturity (e.g., experimental, stable, obsolete).
-   A "Getting started" or "Documentation" section with links to the project's homepage, API documentation (like Javadoc or XML doc comments), and other relevant resources.
-   For open-source projects, "Feedback" and "License" sections pointing to `CONTRIBUTING.md` and `LICENSE` files.

### `LICENSE`

For open-source projects, a `LICENSE` file containing the [Apache License 2.0](templates/apache-2.0-license.txt) is required.

### `COPYRIGHT`

A `COPYRIGHT` file should be present to state copyright information clearly. It should follow the format in the [COPYRIGHT template](templates/COPYRIGHT.txt).

### `CONTRIBUTING.md`

This file provides guidance for contributors. It should cover:

-   Links to authoritative repositories (GitHub, Bitbucket).
-   How to submit issues and pull requests.
-   A note about generated code if applicable.
-   A statement that contributions will be licensed under the project's license.

### `.gitignore`

Every project must have a `.gitignore` file. Use the appropriate template as a starting point:

-   [Java .gitignore](templates/gitignore-java.txt)
-   [.NET .gitignore](templates/gitignore-net.txt)

## Language-Specific Guidelines

For detailed instructions on setting up projects in a specific language, see the documents below:

-   [Java Project Guidelines](java/README.md)
-   [.NET Project Guidelines](net/README.md)

## Migration from the Old Scaffolding Tool

If you are familiar with the previous Python-based scaffolding tool, please read the [Migration Guide](migration.md) to understand the changes.
