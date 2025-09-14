# .NET Project Guidelines

These are guidelines for structuring .NET projects, building upon the [general project guidelines](../README.md).

## Project Structure

A typical .NET solution is organized as follows:

- `{ProjectName}.sln`: The solution file in the root directory.
- `{ProjectName}/`: A directory containing the main project's source code and `.csproj` file.
  - For executable projects, the entry point should be in a `Program.cs` file in this directory.
- `{ProjectName}.Tests/`: A directory for the test project.
- An [example `.csproj` file](example.csproj) is available for reference.

The recommended minimum .NET version is .NET 8.0 (LTS).

## Project File (`.csproj`)

The main project's `.csproj` file should define the following properties:

- `<TargetFramework>` or `<TargetFrameworks>`: Specifies the target .NET version(s).
- `<LangVersion>`: Specifies the C# language version (e.g., `12.0`).
- `<EnableNETAnalyzers>`: Should be `true` to enable Roslyn code analysis.
- `<Version>`: The package version, following semantic versioning.
- `<Title>`: A human-readable name for the package.
- `<Authors>`: Should be `robertvazan`.
- `<RepositoryUrl>`, `<PackageProjectUrl>`: Project metadata.
- `<Description>`, `<PackageTags>`: NuGet package information.
- `<PackageLicenseExpression>`: The license identifier (`Apache-2.0`).
- `<PackageReadmeFile>` and `<PackageIcon>`: For NuGet packages.
- `<GenerateDocumentationFile>`: Should be `true` for libraries to generate XML documentation from comments.
- For libraries with tests, an `<InternalsVisibleTo>` attribute to make internal types visible to the test project.

For projects that are not intended to be published as a NuGet package (e.g., test projects, executables), the `.csproj` file should contain `<IsPackable>false</IsPackable>`.

## Standard Files

- **`.gitignore`:** Add .NET-specific patterns to the project's `.gitignore` file. See the [.NET .gitignore example](example-gitignore.txt) for a minimal set of patterns to include.
- **GitHub Actions:** Projects use GitHub Actions for Continuous Integration (CI) and releases.
  - See the example [build workflow](example-build.yml).
  - For libraries published to NuGet, see the example [release workflow](example-release.yml).

## Example Project

For a real-world application of these guidelines, see the [sourceafis-net](https://github.com/robertvazan/sourceafis-net) project.
