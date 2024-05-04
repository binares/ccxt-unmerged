"""
Exchanges that are not present in ccxt
"""

__version__ = "4.0"
__author__ = "binares"

import ccxt
import sys
import warnings

from ._ccxtUnmergedExchange import ccxtUnmergedExchange
from .bitkub import bitkub
from .btse import btse
from .changellypro import changellypro
from .coindcx import coindcx
from .foblgate import foblgate
from .gateiofutures import gateiofutures
from .nominex import nominex
from .remitano import remitano


_ALREADY_MERGED = []

# Add the custom-defined exchanges to ccxt
for attr, value in list(globals().items()):
    if isinstance(value, type) and issubclass(value, ccxt.Exchange):
        if not hasattr(ccxt, attr):
            newCls = type(attr, (ccxtUnmergedExchange, value), {})
            setattr(ccxt, attr, newCls)
            globals()[attr] = newCls
        else:
            _ALREADY_MERGED.append(attr)

if sys.version_info >= (3, 5, 3):
    from . import async_support  # initialize async exchanges


def warn_duplicated():
    """Warn the user that the new exchange version in ccxt (that we'll be using now)
    might differ from the one previously defined here"""
    if _ALREADY_MERGED:
        merged_exchanges = "'" + "', '".join(_ALREADY_MERGED) + "'"
        warnings.warn(
            "Exchanges %s have been added to ccxt. If you were using the old version (in ccxt_unmerged), there might be some differences."
            % merged_exchanges
        )


warn_duplicated()
