"""**openalea-meta**

openalea meta-package
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("openalea.openalea-meta")
except PackageNotFoundError:
    # package is not installed
    pass
