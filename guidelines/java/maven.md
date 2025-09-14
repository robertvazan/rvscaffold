# Maven Guidelines

This document provides guidelines for structuring the `pom.xml` file in Java projects, as mentioned in the [Java Project Guidelines](README.md). An [example `pom.xml`](example-pom.xml) is available for reference.

The `pom.xml` file is the core of a Maven project. It should be well-structured and contain all necessary information to build, test, and distribute the project.

## Project Coordinates

The `pom.xml` must define the project's coordinates:

- `<groupId>`: Follows reverse-DNS convention, typically `com.machinezoo.subgroup`.
  - For a standalone project like `my-project`, the subgroup is `myproject`.
  - For a project that is part of a larger group, like `project-core` and `project-extension`, the subgroup is `project`. The groupId is shared, and the artifactId distinguishes the modules.
- `<artifactId>`: The name of the project, e.g., `project-name`.
- `<version>`: The project's version, following semantic versioning.

## Metadata

The POM should include standard metadata for identification and for publication to Maven Central:

- `<name>`: A human-readable name for the project (short name).
- `<description>`: A short description of the project.
- `<url>`: A link to the project's homepage or repository.
- `<inceptionYear>`: The year the project was created.
- `<licenses>`: An entry for the Apache License 2.0.
- `<organization>` and `<developers>`: Information about the author. This should be consistent across projects. See the example `pom.xml` for the correct structure.
- `<scm>`: Source Control Management information, pointing to the Git repository.

## Properties

Define the following properties:

- `<project.build.sourceEncoding>`: Should be `UTF-8`.
- `<maven.compiler.release>`: The target Java language level (e.g., `11`).
- For executable applications, an `<exec.mainClass>` property should be defined to specify the main class for `exec-maven-plugin`. The format should be `{module-name}/{fully.qualified.ClassName}`.

## Build Configuration

The `<build>` section configures the build process, primarily through plugins. It is important to use up-to-date plugin versions to support modern Java versions and to ensure reproducible builds.

### Standard Plugins

- `maven-compiler-plugin` (3.11.0+): To compile Java source code.
- `maven-surefire-plugin` (3.2.2+): To run unit tests.

### Plugins for Publishing to Maven Central

For libraries distributed via Maven Central, a specific set of plugins is required to meet the publication requirements.

- `jacoco-maven-plugin` (0.8.11+): To generate test coverage reports, which are often required by quality gates and for reporting to services like Codecov.
- `maven-javadoc-plugin` (3.6.2+): To generate Javadoc. Maven Central requires a `javadoc.jar` artifact.
  - To enable cross-linking to Javadoc of dependency libraries, add a `<links>` section to the plugin configuration with URLs to the Javadoc of all dependencies. This is preferred over `<detectLinks>`, which can be unreliable in CI environments.
  - For projects with incomplete Javadoc, the `<doclint>` option can be configured to ignore missing comments (e.g., `<doclint>all,-missing</doclint>`) to avoid build failures, especially on newer JDKs.
- `maven-source-plugin` (3.3.0+): To bundle the source code. A `sources.jar` artifact is also a requirement.
- `central-publishing-maven-plugin` (0.6.0+): A modern plugin to handle the release process to Sonatype OSSRH and Maven Central. It simplifies what used to be a complex process involving `maven-deploy-plugin` and `nexus-staging-maven-plugin`.
- `maven-gpg-plugin` (3.1.0+): To sign the artifacts, a security requirement for publishing.

### Plugins for JMH Benchmarks

For projects that include [Java Microbenchmark Harness (JMH)](https://openjdk.java.net/projects/code-tools/jmh/) benchmarks, additional configuration is needed.

- Add JMH dependencies (`jmh-core` and `jmh-generator-annprocess`).
- Configure `maven-compiler-plugin` to use the JMH annotation processor by adding an `<annotationProcessorPaths>` section.
- Add and configure `maven-shade-plugin` (3.5.1+) to create an executable JAR for the benchmarks. This JAR should include all dependencies and have `org.openjdk.jmh.Main` as its main class.
