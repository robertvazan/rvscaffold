# Project Guidelines

This document is the main entry point to a set of guidelines for structuring projects. These guidelines are intended to be interpreted by Large Language Models (LLMs) to assist with software development, but they are also human-readable.

## General Files

All projects, regardless of language, should contain some standard files in their root directory.

### `README.md`

The `README.md` file is the front page of the project. It should include:

-   A Stand with Ukraine banner. You can use this Markdown snippet:
    ```markdown
    [![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md)
    ```
-   The project's short name as a level 1 heading (e.g., "SourceAFIS for Java").
-   Badges for build status, package registry versions, and test coverage. Examples:
    -   **Build Status (GitHub Actions):** `[![Build status](https://github.com/{user}/{repo}/actions/workflows/build.yml/badge.svg)](https://github.com/{user}/{repo}/actions/workflows/build.yml)`
    -   **Maven Central:** `[![Maven Central](https://img.shields.io/maven-central/v/{group}/{artifact})](https://central.sonatype.com/artifact/{group}/{artifact})`
    -   **NuGet:** `[![NuGet](https://img.shields.io/nuget/v/{package})](https://www.nuget.org/packages/{package}/)`
    -   **Test Coverage (Codecov):** `[![Test coverage](https://codecov.io/gh/{user}/{repo}/branch/master/graph/badge.svg)](https://codecov.io/gh/{user}/{repo})`
-   A short description of the project.
-   A "Status" section describing the project's maturity (e.g., experimental, stable, obsolete).
-   A "Getting started" or "Documentation" section with links to the project's homepage, API documentation (like Javadoc or XML doc comments), and other relevant resources.
-   For open-source projects, "Feedback" and "License" sections pointing to `CONTRIBUTING.md` and `LICENSE` files.

### `LICENSE`

For open-source projects, a `LICENSE` file containing the Apache License 2.0 is required. It should be a copy of the [LICENSE file from the `rvscaffold` repository](../../LICENSE).

### `COPYRIGHT`

A `COPYRIGHT` file should be present to state copyright information clearly. It should use the project's long legal name (e.g., "Robert Važan's SourceAFIS for Java"). See the [COPYRIGHT example](example-copyright.txt) for the recommended format.

### `CONTRIBUTING.md`

This file provides guidance for contributors. It should cover:

-   Links to authoritative repositories (GitHub, Bitbucket).
-   How to submit issues and pull requests.
-   A statement that contributions will be licensed under the project's license.
-   Any project-specific exceptions to the guidelines in this repository.

### `.gitignore`

Every project must have a `.gitignore` file. It should start with the contents of the [base .gitignore from `rvscaffold`](../../.gitignore), followed by language-specific patterns.

## Language-Specific Guidelines

For detailed instructions on setting up projects in a specific language, see the documents below:

-   [Java Project Guidelines](java/README.md)
-   [.NET Project Guidelines](dotnet/README.md)

## Migration from the Old Scaffolding Tool

If you are familiar with the previous Python-based scaffolding tool, please read the [Migration Guide](migration.md) to understand the changes.
