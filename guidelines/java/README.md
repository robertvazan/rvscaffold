# Java Project Guidelines

These are guidelines for structuring Java projects, building upon the [general project guidelines](../README.md).

## Project Structure

- **Source Code:** Java projects are expected to be structured as [Java Platform Module System (JPMS)](https://en.wikipedia.org/wiki/Java_Platform_Module_System) modules.
  - A `module-info.java` file must be present in the root source package directory (e.g., `src/main/java/com/example/project/module-info.java`).
  - The module name should follow the reverse-DNS convention (e.g., `com.machinezoo.projectname`).
  - The main package of the project should be the same as the module name.
- **Build System:** All Java projects use [Apache Maven](https://maven.apache.org/). The configuration is defined in a `pom.xml` file. See the [Maven Guidelines](maven.md) for details.
- **Version:** The recommended minimum Java version is 11 (LTS) for open-source libraries. For executable applications and closed-source libraries, Java 21 (LTS) or later is recommended.

## Standard Files

- **`.gitignore`:** Add Java-specific patterns to the project's `.gitignore` file. See the [Java .gitignore example](example-gitignore.txt) for a minimal set of patterns to include.
- **GitHub Actions:** Projects use GitHub Actions for Continuous Integration (CI) and releases.
  - See the example [build workflow](example-build.yml).
  - For libraries published to Maven Central, see the example [release workflow](example-release.yml).

## Example Project

For a real-world application of these guidelines, see the [sourceafis-java](https://github.com/robertvazan/sourceafis-java) project.
