# Contributing to Project Scaffolding Guidelines

This is a personal repository of Robert Važan, so contributions are unlikely. This file contains meta-guidelines for writing the guideline documents contained in this repository. This file is mainly intended to be read by LLMs, but it also serves as the author's persistent memory for meta-guidelines.

## Why LLMs and not scripts?

This project was originally a collection of scripts that enforced a standard structure in all of my projects. This approach did not work well, because many projects have special requirements and exceptions. The scaffolding project was growing into unmaintainable complexity trying to accommodate them. On top of that, most project files need some manual editing, which interferes with scaffolding scripts.

The current approach is different. This repository contains instructions for Large Language Models (LLMs) to enforce the standard project structure. These instructions are written in plain language, as if they were for humans to read. And humans might read them sometimes, but they are primarily for LLMs. Since LLMs are smart, they can adapt to project-specific requirements and exceptions, which can be described in the target project's `CONTRIBUTING.md` file. They can also make targeted edits that coexist with manually written code. Because edits are targeted, the scaffolding does not have to address content that every project can maintain on its own, for example the list of dependencies and their versions.

## Inclusion criteria

What to include in and exclude from the guidelines:

- Provide human-readable guidelines that can be interpreted and softly enforced instead of encoding hard requirements in scripts.
- Provide justification for non-obvious guidelines. Justification should be sufficiently detailed to support later review, so that outdated guidelines can be updated or removed.
- If a guideline is motivated by a well-known issue, document it with an external link to the relevant bug report or article.
- Prefer concrete examples over lengthy descriptions.
- Be specific. If only one value makes sense, say so instead of trying to be unnecessarily general.
- Do not prescribe specific versions for dependencies unless some minimal version is necessary to address an issue.

## Structure

This repository is organized as follows:

- `guidelines/`: The core content. It contains a main [`README.md`](guidelines/README.md) that serves as an entry point, with language-specific guidelines in subdirectories (e.g., `java/`, `dotnet/`).
- `CONTRIBUTING.md`: Meta-guidelines for maintaining this repository, which you are currently reading.
- `README.md`: Introduction, usage, basic information.

How to organize the guidelines:

- Break down complex topics into separate files and directories.
- Use a `README.md` file in each directory to serve as an index and introduction.
- All documents should link to their parent document to aid navigation.
- Place lengthy code blocks or file templates (e.g., `pom.xml` content) in separate example files (e.g., `example-pom.xml`) in the same directory as the guideline that references them.

## Formatting

- Maintain consistent formatting and style across all guideline documents.
- Structure the content logically. Use headings and lists to make the information easy to read.
- Link to other Markdown files and content files instead of just mentioning them.
