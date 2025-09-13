# Java Project Guidelines

These are guidelines for structuring Java projects, building upon the [general project guidelines](../README.md).

## Directory Structure

Java projects follow the standard Maven directory layout:

-   `src/main/java`: For Java source code.
-   `src/main/resources`: For resource files.
-   `src/test/java`: For test source code.
-   `src/test/resources`: For test resource files.

## JPMS Modules

Projects are expected to be structured as [Java Platform Module System (JPMS)](https://en.wikipedia.org/wiki/Java_Platform_Module_System) modules.

-   A `module-info.java` file must be present in the root source package directory (e.g., `src/main/java/module-info.java`).
-   The module name should follow the reverse-DNS convention (e.g., `com.machinezoo.projectname`).
-   The main package of the project should be the same as the module name.
-   All exported packages must be listed in `module-info.java`.

## Maven Build System

All Java projects use [Apache Maven](https://maven.apache.org/) as their build system. The project's configuration is defined in a `pom.xml` file in the root directory.

For detailed instructions on how to structure the `pom.xml` file, see the [Maven Guidelines](maven.md).

## GitHub Actions

Projects use GitHub Actions for Continuous Integration (CI) and releases.

-   **Build workflow:** A `build.yml` file in `.github/workflows/` should define a job that runs on every push and pull request to the `master` branch. This job should:
    -   Check out the source code.
    -   Set up the correct JDK version.
    -   Run `mvn install`.
    -   For projects that publish to Maven Central, generate a test coverage report with JaCoCo and upload it to a code coverage service.

-   **Release workflow:** For libraries that are published to Maven Central, a `release.yml` file in `.github/workflows/` should define a manually triggered job. This job should:
    -   Check out the source code.
    -   Set up the JDK, Maven, and GPG for signing.
    -   Run `mvn deploy` to publish the artifact to Maven Central.
