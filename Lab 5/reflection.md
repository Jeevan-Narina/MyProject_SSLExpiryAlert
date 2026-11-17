# Reflection on Static Code Analysis

## 1. What is the importance of static code analysis?

Static code analysis helps identify programming errors, security vulnerabilities, unused variables, and coding-style violations without executing the program. Tools such as Pylint, Bandit, and Flake8 improve code quality, readability, maintainability, and security.

## 2. What issues did you identify in the original program?

The original program contained several issues, including the use of `eval()`, MD5 hashing, insecure random-number generation for the checkout PIN, shell command execution using `os.system()`, mutable default arguments, unused variables, missing docstrings, and formatting violations.

## 3. How did you resolve the identified issues?

I improved the program by replacing `eval()` with direct arithmetic and input validation, replacing MD5 with SHA-256, using the `secrets` module for PIN generation, and replacing shell command execution with safe file handling. I also improved naming conventions, removed unused code, added docstrings, corrected function behavior, and resolved formatting issues.

## 4. What did you learn from this experiment?

I learned that static analysis tools identify different categories of problems. Pylint helps improve code quality and maintainability, Bandit identifies potential security vulnerabilities, and Flake8 checks Python style and formatting. Using these tools together helps produce cleaner and more secure code.