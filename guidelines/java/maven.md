# Maven Guidelines

This document provides guidelines for structuring the `pom.xml` file in Java projects, as mentioned in the [Java Project Guidelines](README.md).

The `pom.xml` file is the core of a Maven project. It should be well-structured and contain all necessary information to build, test, and distribute the project.

## Project Coordinates

The `pom.xml` must define the project's coordinates:

-   `<groupId>`: Follows the reverse-DNS convention, typically `com.machinezoo.subgroup`.
-   `<artifactId>`: The name of the project, e.g., `projectname`.
-   `<version>`: The project's version, following semantic versioning.

## Metadata

The POM should include the following metadata:

-   `<name>`: A human-readable name for the project.
-   `<description>`: A short description of the project.
-   `<url>`: A link to the project's homepage or repository.
-   `<inceptionYear>`: The year the project was created.
-   `<licenses>`: An entry for the Apache License 2.0 for open-source projects.
-   `<organization>` and `<developers>`: Information about the author.
-   `<scm>`: Source Control Management information, pointing to the Git repository.

## Properties

Define the following properties:

-   `<project.build.sourceEncoding>`: Should be `UTF-8`.
-   `<maven.compiler.release>`: The target Java language level (e.g., `11`, `17`).

## Dependencies

Dependencies are listed in the `<dependencies>` section. This section should be managed manually for each project. The guidelines do not prescribe specific dependencies or versions.

## Build Configuration

The `<build>` section configures the build process, primarily through plugins.

### Standard Plugins

-   `maven-compiler-plugin`: To compile Java source code. Ensure its version is up-to-date.
-   `maven-surefire-plugin`: To run unit tests. Ensure its version is up-to-date.

### Plugins for Publishing to Maven Central

For libraries distributed via Maven Central, the following plugins are required:

-   `jacoco-maven-plugin`: To generate test coverage reports.
-   `maven-javadoc-plugin`: To generate Javadoc. It should be configured to attach the javadoc JAR to the build.
-   `maven-source-plugin`: To bundle the source code into a source JAR.
--   `central-publishing-maven-plugin`: To handle the release process to Sonatype OSSRH and Maven Central.
-   `maven-gpg-plugin`: To sign the artifacts before release.
