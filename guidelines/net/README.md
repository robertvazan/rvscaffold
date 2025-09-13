# .NET Project Guidelines

These are guidelines for structuring .NET projects, building upon the [general project guidelines](../README.md).

## Directory Structure

A typical .NET solution is organized as follows:

-   `{ProjectName}.sln`: The solution file in the root directory.
-   `{ProjectName}/`: A directory containing the main project's source code and `.csproj` file.
-   `{ProjectName}.Tests/`: A directory for the test project, if applicable.

## Solution File (`.sln`)

The solution file lists all projects in the solution. It is managed by Visual Studio or the `dotnet` CLI and should contain references to all `csproj` files.

## Project File (`.csproj`)

The `.csproj` file defines the project's properties, dependencies, and build configuration.

### Main Project

The main project's `.csproj` file should contain:

-   A `<PropertyGroup>` section with:
    -   `<TargetFrameworks>` or `<TargetFramework>`: Specifies the target .NET version(s).
    -   `<LangVersion>`: Specifies the C# language version.
    -   `<Version>`: The package version, following semantic versioning.
    -   `<Title>`: A human-readable name for the package.
    -   `<Authors>`, `<RepositoryUrl>`, `<PackageProjectUrl>`: Project metadata.
    -   `<Description>`, `<PackageTags>`: NuGet package information.
    -   `<PackageLicenseExpression>`: The license identifier (e.g., `Apache-2.0`).
    -   `<PackageReadmeFile>` and `<PackageIcon>`: For NuGet packages.
    -   `<GenerateDocumentationFile>`: Should be `true` for libraries to generate XML documentation comments.
-   An `<ItemGroup>` for `PackageReference` items, listing NuGet dependencies.
-   For libraries with tests, an `<ItemGroup>` with an `<InternalsVisibleTo>` attribute to make internal types visible to the test project.

### Test Project

The test project's `.csproj` file is simpler:

-   It targets a specific .NET version (e.g., `net6.0`).
-   It has `<IsPackable>false</IsPackable>`.
-   It includes a `ProjectReference` to the main project.
-   It includes `PackageReference` items for testing frameworks like NUnit and MSTest.

## GitHub Actions

Projects use GitHub Actions for Continuous Integration (CI) and releases.

-   **Build workflow:** A `build.yml` file in `.github/workflows/` should define a job that runs on every push and pull request. This job should use the `dotnet` CLI to:
    -   `dotnet build`
    -   `dotnet test`
    -   `dotnet pack` (for libraries)

-   **Release workflow:** For libraries published to NuGet, a `release.yml` file should define a manually triggered job to:
    -   `dotnet pack --configuration Release`
    -   `dotnet nuget push` to publish the package to nuget.org.

## Special Project Types

-   [FVC Project Guidelines](fvc.md): For projects that are submissions to the FVC-onGoing competition.
