# Contributing to Project Scaffolding Guidelines

This is a personal repository of Robert Važan, so contributions are unlikely. This file contains meta-guidelines for writing the guideline documents contained in this repository. It is mostly intended for LLMs, but it also serves as the author's persistent memory for meta-guidelines.

## Principles

The guidelines in this repository are meant to be read and interpreted by both humans and Large Language Models (LLMs). When writing or modifying them, please adhere to the following principles:

- **Clarity over code:** Write in plain, easy-to-understand language. The goal is to communicate conventions and principles, not to write a script. Provide justification for non-obvious guidelines.
- **LLM- and human-readable:** Structure the content logically. Use headings, lists, and links to make the information accessible and easy to parse.
- **Modularity:** Break down complex topics into separate files and directories. Use a `README.md` file in each directory to serve as an index and introduction to the topics within. All documents should link to their parent document to aid navigation.
- **Co-locate examples:** For lengthy code blocks or file templates (e.g., `pom.xml` content), place them in separate example files (e.g., `pom.xml.example`) in the same directory as the guideline document that references them. This keeps the guidelines concise and focused on principles.
- **Focus on conventions, not boilerplate:** The guidelines should describe *what* should be configured and *why*, but avoid prescribing specific versions for dependencies or other details that are better decided within the context of the target project. Essential plugin versions that are required for the build to work correctly are an exception.

## Formatting

- Use a single space between a list item marker (`-`) and the item's content.
- Indent nested lists by two spaces.
- Leave a blank line between a paragraph and a list that follows it.
