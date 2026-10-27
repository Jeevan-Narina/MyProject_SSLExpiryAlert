# Static Code Analysis Issues

## Issue 1: Unsafe Use of eval()

- **Tool:** Bandit
- **Severity:** Medium
- **Problem:** The original program used `eval()` to calculate a discounted price. Evaluating arbitrary expressions can execute unintended code.
- **Fix:** Replaced `eval()` with direct arithmetic after validating the discount rate.
- **Result:** Discount calculations are performed without evaluating arbitrary expressions.

## Issue 2: Weak Hashing Algorithm

- **Tool:** Bandit
- **Severity:** High
- **Problem:** The original program used MD5 to generate an item hash. MD5 is not suitable for security-sensitive hashing.
- **Fix:** Replaced MD5 with SHA-256.
- **Result:** The program uses a stronger hashing algorithm.

## Issue 3: Insecure Checkout PIN Generation

- **Tool:** Bandit
- **Severity:** Low
- **Problem:** The original program used the `random` module to generate a checkout PIN. This module is not designed for security-sensitive random values.
- **Fix:** Replaced it with Python's `secrets` module.
- **Result:** The PIN is generated using a cryptographically secure random-number generator.

## Issue 4: Unsafe Shell Command Execution

- **Tool:** Bandit
- **Severity:** High
- **Problem:** The original program used `os.system()` to execute a shell command when exporting the receipt.
- **Fix:** Replaced shell execution with Python file handling using `open()` and a context manager.
- **Result:** Receipt export no longer requires shell command execution.

## Additional Issues Identified

### Mutable Default Argument

- **Tool:** Pylint
- **Problem:** The original function used a mutable list as a default argument.
- **Fix:** Changed the default to `None` and initialized the list inside the function.

### Code Formatting

- **Tool:** Flake8
- **Problem:** The original code contained unused imports, a bare `except`, unused variables, incorrect comparisons, and line-length issues.
- **Fix:** Removed unused code, improved exception handling, corrected comparisons, and reformatted the code.

## Conclusion

Static code analysis helped identify security, maintainability, and formatting problems. The revised implementation addresses the identified issues and was checked again using Pylint, Bandit, and Flake8.