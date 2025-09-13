# FVC Project Guidelines

This document describes special guidelines for .NET projects that are submissions to the [FVC-onGoing](https://biolab.csr.unibo.it/FVCOnGoing/UI/Form/Home.aspx) fingerprint verification competition. These guidelines extend the general [.NET Project Guidelines](README.md).

These projects are typically command-line applications that wrap the SourceAFIS library for a specific FVC benchmark.

## Naming Conventions

-   **Root Namespace and Project Name:** `SourceAFIS.FVC.{BenchmarkAbbreviation}{Suffix}`, where:
    -   `{BenchmarkAbbreviation}` is the short name of the benchmark (e.g., `FV-STD-1.0`).
    -   `{Suffix}` is `.Extractor` for the enrollment part and `.Matcher` for the matching part if they are submitted separately.
-   **Assembly Name:** `enroll` for the extractor, `match` for the matcher.
-   **Pretty Name:** `SourceAFIS {extractor|matcher} for FVC {BenchmarkAbbreviation}`.

## Project Structure

-   The project is a console application (`<OutputType>Exe</OutputType>` in `.csproj`), not a library.
-   It has a dependency on the `SourceAFIS` NuGet package.

## `README.md` Content

The `README.md` file should explicitly state that the project is a SourceAFIS submission to the specific FVC benchmark, with links to both the SourceAFIS homepage and the benchmark's page on the FVC-onGoing website.

## Publishing Script

A `scripts/publish.sh` script should be included to prepare the submission package. This script should:
1.  Run `dotnet publish` to create a self-contained executable.
2.  Create a `submission` directory.
3.  Copy the published files into the `submission` directory.
4.  If the submission consists of multiple parts (e.g., extractor and matcher), it should bundle files from sister projects.
5.  Create a ZIP archive from the contents of the `submission` directory, ready for upload to the FVC-onGoing website.
