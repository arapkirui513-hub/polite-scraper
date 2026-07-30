# Lessons Learned

## Purpose

This document captures the key technical and engineering lessons learned while developing the Polite Scraper. It focuses on architectural thinking, software design, and the practical experience gained throughout the project.

The goal is not only to document what was built, but also to record the reasoning and insights that can inform future projects.

---

# 1. Separation of Concerns Improves Maintainability

One of the most important lessons from this project was the value of assigning a single responsibility to each component.

Initially, responsibilities such as networking and application orchestration were more tightly coupled. Refactoring the application into dedicated modules made the codebase easier to understand and maintain.

Clear boundaries between modules also reduce the risk of unintended side effects when introducing new features.

---

# 2. Configuration Should Be External

Moving application settings into `config.yaml` demonstrated the benefits of separating configuration from implementation.

Configuration values such as timeouts, retry counts, and output locations can now be changed without modifying source code.

This approach improves flexibility and reduces maintenance effort.

---

# 3. Small Refactorings Are Safer Than Large Rewrites

Rather than redesigning the application all at once, improvements were introduced incrementally.

Each change focused on a single concern—for example:

- centralising configuration,
- improving storage,
- reorganising networking,
- expanding documentation.

This made it easier to verify changes and reduced the likelihood of introducing new issues.

---

# 4. Documentation Is Part of the Software

Writing documentation after the implementation highlighted how documentation supports long-term maintainability.

Architecture diagrams, design decisions, and review notes explain *why* the project is structured the way it is, making it easier for future contributors—or your future self—to understand the system.

Good documentation complements the code rather than repeating it.

---

# 5. Designing for Extension

Building the scraper as a collection of independent modules makes future enhancements more straightforward.

Potential improvements such as database storage, search indexing, or Retrieval-Augmented Generation (RAG) can be added without major changes to the existing architecture.

Designing for extension from the beginning reduces the cost of future development.

---

# 6. Testing Is an Ongoing Process

The project includes automated tests for configuration loading and robots.txt behaviour.

Additional automated tests for the parser, extractor, cleaner, fetcher, storage, and full pipeline remain future work.

Expanding test coverage will improve confidence when introducing new functionality and refactoring existing components.

---

# 7. Software Evolves Through Review

Many improvements in this project were driven by reviewing the implementation rather than adding new features.

Reviewing the code led to improvements such as:

- clearer module responsibilities,
- centralised configuration,
- duplicate detection,
- cleaner documentation,
- simplified project structure.

Regular review proved to be an effective way of improving software quality incrementally.

---

# What I Would Do Differently

If starting the project again, I would:

- write more automated tests earlier,
- define module boundaries before implementation,
- document design decisions throughout development instead of after major milestones,
- establish logging and configuration management from the beginning.

These changes would reduce the amount of refactoring required later in the project.

---

# Final Reflection

This project reinforced that good software engineering is about more than writing working code.

Maintainability, documentation, modular design, and thoughtful review all contribute to software that is easier to understand, extend, and support over time.

The Polite Scraper provided valuable experience in building a structured application while balancing functionality with code quality and long-term maintainability.