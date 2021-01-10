"""Generates a weekly bullet-point list of all the work done by ASF's Tools Team"""

from importlib.metadata import PackageNotFoundError, version

from bullets.__main__ import generate_bullets
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    print(f'{__name__} package is not installed!\n'
          f'Install in editable/develop mode via (from the top of this repo):\n'
          f'   python -m pip install -e .[develop]\n'
          f'Or, to just get the version number use:\n'
          f'   python setup.py --version')

__all__ = [
    '__version__',
    'generate_bullets',
]
