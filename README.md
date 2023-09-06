`flake8-no-pytest-mark-only`
============================

A [Flake8](https://flake8.pycqa.org/) plugin to check for the usage of the `@pytest.mark.only` decorator.

Rationale
---------

The `@pytest.mark.only` decorator, coming from the [`pytest-only`](https://pypi.org/project/pytest-only/) plugin, is great.
It's super useful when developing your tests, so that you can run just the test (or set of tests) that you're working on,
without having to run your whole test suite.

The only problem with it is that when you forget to remove it after you've finished developing your tests,
and you accidentally commit it to your repository,
it's hard to notice that only a subset of tests are running in CI instead of the whole test suite.

This Flake8 plugin prevents that, by raising a lint error on usages of the `@pytest.mark.only` decorator,
so that you notice that you've committed changes with the decorator in them.

Usage
-----

Just install the `flake8-no-pytest-mark-only` package, and when you run Flake8,
it will automatically find the plugin and use it.

If you want to override the reporting from this plugin, you can filter for the error code `PNO001`:

```bash
# Turn on the errors from this plugin
flake8 --select PNO001 ...

# Turn off the errors from this plugin
flake8 --extend-ignore PNO001 ...
```
