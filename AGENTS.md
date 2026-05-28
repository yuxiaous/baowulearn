# API Captures Documentation Workflow

When a request involves adding, updating, renaming, or reorganizing files under `doc/api-captures/`, you must read `doc/api-captures/README.md` before making changes.

Treat `doc/api-captures/README.md` as the single source of truth for:

- file naming
- document structure
- title and subtitle format
- sanitization rules
- README index update rules
- workflow grouping and ordering

For new single-API documents:

1. Infer a business-oriented filename from the API purpose and group rules in `doc/api-captures/README.md`.
2. Use the standard document skeleton embedded in `doc/api-captures/README.md`.
3. Keep the title format as a business title plus the original API name subtitle.
4. Sanitize all sensitive values before writing examples.
5. Update `doc/api-captures/README.md` in the correct interface group, and update the workflow description when the new API changes the reading path.

If the user only provides API basics such as URL, method, request body, and response body, you should still complete the document using the README rules and infer the missing narrative fields from the existing documentation style.