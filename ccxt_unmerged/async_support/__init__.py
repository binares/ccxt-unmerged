"""
Async versions of exchanges that are not present in ccxt
"""

import ccxt.async_support

from .._ccxtUnmergedExchange import ccxtUnmergedExchange
from .bitclude import bitclude
from .bitforexfu import bitforexfu
from .bitkub import bitkub
from .btse import btse
from .changellypro import changellypro
from .coindcx import coindcx
from .felixo import felixo
from .foblgate import foblgate
from .gateiofu import gateiofu
from .nominex import nominex
from .primexbt import primexbt
from .remitano import remitano
from .slicex import slicex

# Add the custom-defined exchanges to ccxt.async_support
for attr, value in list(globals().items()):
    if isinstance(value, type) and issubclass(value, ccxt.async_support.Exchange):
        if not hasattr(ccxt.async_support, attr):
            newCls = type(attr, (ccxtUnmergedExchange, value), {})
            setattr(ccxt.async_support, attr, newCls)
            globals()[attr] = newCls
