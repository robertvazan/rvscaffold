# Contributing to Project Scaffolding Guidelines

This is a personal repository of Robert Važan, so contributions are unlikely. This file contains meta-guidelines for writing guideline documents contained in this repository. It is mostly intended for LLMs, but it also serves as author's persistent memory for meta-guidelines.

## Principles

The guidelines in this repository are meant to be read and interpreted by both humans and Large Language Models (LLMs). When writing or modifying them, please adhere to the following principles:

-   **Clarity over code:** Write in plain, easy-to-understand language. The goal is to communicate conventions and principles, not to write a script.
-   **LLM- and human-readable:** Structure the content logically. Use headings, lists, and links to make the information accessible and easy to parse.
-   **Modularity:** Break down complex topics into separate files and directories. Use a `README.md` file in each directory to serve as an index and introduction to the topics within. All documents should link to their parent document to aid navigation.
-   **Externalize templates:** For lengthy code blocks or file templates (e.g., `.gitignore` content), place them in separate files under `guidelines/templates/` and link to them from the relevant guideline document. This keeps the guidelines concise and focused on principles.
-   **Focus on conventions, not boilerplate:** The guidelines should describe *what* should be configured and *why*, but avoid prescribing specific versions for dependencies or other details that are better decided within the context of the target project.
