import ast
import textwrap

from flake8_no_pytest_mark_only import Flake8NoPytestMarkOnly


def test_class_with_decorator() -> None:
    """Test a class with a decorator."""
    src = """
        import pytest

        @pytest.mark.only
        class TestClassWithDecorator:
            @pytest.mark.only
            class TestNestedClass:
                pass

            @pytest.mark.only
            def test_function_with_decorator():
                pass

            @pytest.mark.only
            async def test_async_function_with_decorator():
                pass

            def test_function_without_decorator():
                pass

        class TestClassWithoutDecorator:
            @pytest.mark.only
            def test_function_with_decorator():
                pass

            def test_function_without_decorator():
                pass

        @pytest.mark.only
        def test_function_with_decorator():
            pass

        @pytest.mark.only()
        def test_function_with_decorator_as_function_call():
            pass

        @pytest.mark.other_mark
        def test_function_with_different_decorator():
            pass

        def test_function_without_decorator():
            pass

        # test that non-decorator use is not detected
        print(pytest.mark.only)
    """
    src = textwrap.dedent(src)
    tree = ast.parse(src)
    plugin = Flake8NoPytestMarkOnly(tree)
    errors = list(plugin.run())

    # Find all positions of @pytest.mark.only decorators in the source
    expected_errors = []
    for lineno, line in enumerate(src.splitlines(), start=1):
        if '@pytest.mark.only' in line:
            expected_errors.append((lineno, line.index('@pytest.mark.only') + len('@pytest.mark.'), 'PNO001 do not commit @pytest.mark.only', plugin))

    # Check that the expected errors were found
    assert len(errors) == len(expected_errors)
    for error, expected_error in zip(errors, expected_errors):
        try:
            assert error == expected_error
        finally:
            print(error)
            print(src.splitlines()[error[0] + 1])
