# Tests policy.

## Purpose

Tests should:
- Help maintain the code.
- Be easy to follow.
- Short, self-explanatory, and meaningful.

Tests should NOT:
- Exist to satisfy coverage numbers.
- Be mandatory, sometimes, less is more.
- Cause complexity bloat.

## Principles

1. **Clarity over coverage**

* A small, clear test is better than a big, unreadable one.
* Do not write tests “just because the rule says so.”

2. **Self-explanatory**

* Every test must be understandable without extra context.
* Add step-by-step comments describing *what* is happening and *why*.

3. **Multiple values, not single traps**

* Avoid tests that check only one arbitrary number/string.
* Use parameterization or small sets of inputs so tests fail if logic changes.

4. **Focus on behavior, not implementation**

* Test **what the code should do**, not *how* it does it.
* Avoid locking tests to internals that might reasonably change.

5. **No redundancy**

* Don’t test trivial assignments, constants, or one-line pass-throughs.
* Remove tests that only duplicate coverage from another test.

6. **Fail usefully**

* A failing test should point to a real problem, not a contrived one.
* Prefer meaningful assertions over “is not None” or “equals 1”.

7. **Minimal scaffolding**

* Use dummy/test doubles only for what is required to exercise the code.
* Keep helpers inside the test file unless reused often.

## Examples

* ✅ **Good**: Test that a window mover repositions correctly for positive, negative, and zero cursor movement.
* ❌ **Bad**: Test that `tooltip.delay == 123` for one hardcoded config value.

## Tools & Running

* Use **pytest** as the default runner.
* Run with `pytest -v` for readable output.
* Show debug prints only when needed with `pytest -s`.
