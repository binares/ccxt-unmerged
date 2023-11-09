"""
Async versions of exchanges that are not present in ccxt
"""
import ccxt.async_support

from .bitclude import bitclude
from .bitforexfu import bitforexfu
from .bitkub import bitkub
from .btse import btse
from .changellypro import changellypro
from .coindcx import coindcx
from .felixo import felixo
from .foblgate import foblgate
from .gateiofu import gateiofu
from .krakenfu import krakenfu
from .nominex import nominex
from .primexbt import primexbt
from .remitano import remitano
from .slicex import slicex
from .tokenomy import tokenomy
from .tradeogre import tradeogre
from .vitex import vitex
from .yunex import yunex

# Add the custom-defined exchanges to ccxt.async_support
for attr, value in list(globals().items()):
    if isinstance(value, type) and issubclass(value, ccxt.async_support.Exchange):
        if not hasattr(ccxt.async_support, attr):
            setattr(ccxt.async_support, attr, value)
