from importlib import metadata

from .plugin import Flake8NoPytestMarkOnly

__all__ = ['Flake8NoPytestMarkOnly']

__version__ = metadata.version('flake8-no-pytest-mark-only')
