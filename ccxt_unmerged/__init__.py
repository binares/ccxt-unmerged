"""
Exchanges that are not present in ccxt
"""
__version__ = '2.2'
__author__ = 'binares'

import ccxt
import sys
import warnings

from ._58coin import _58coin
from .bcio import bcio
from .beaxy import beaxy
from .biki import biki
from .bitclude import bitclude
from .bitforexfu import bitforexfu
from .bitkub import bitkub
from .bitopro import bitopro
from .bitrue import bitrue
from .bkex import bkex
from .btse import btse
from .ceo import ceo
from .changellypro import changellypro
from .coinbene import coinbene
from .coindcx import coindcx
from .coinsuper import coinsuper
from .cossdex import cossdex
from .cryptocom import cryptocom
from .dragonex import dragonex
from .duedex import duedex
from .felixo import felixo
from .foblgate import foblgate
from .gateiofu import gateiofu
from .krakenfu import krakenfu
from .multi import multi
from .mxc import mxc
from .nominex import nominex
from .primexbt import primexbt
from .remitano import remitano
from .silgonex import silgonex
from .slicex import slicex
from .tokenomy import tokenomy
from .tokensnet import tokensnet
from .tradeogre import tradeogre
from .txbit import txbit
from .vinex import vinex
from .vitex import vitex
from .wazirx import wazirx
from .yunex import yunex

_ALREADY_MERGED = []

# Add the custom-defined exchanges to ccxt
for attr,value in list(globals().items()):
    if isinstance(value, type) and issubclass(value, ccxt.Exchange):
        if not hasattr(ccxt, attr):
            setattr(ccxt, attr, value)
        else:
            _ALREADY_MERGED.append(attr)

if sys.version_info >= (3, 5, 3):
    from . import async_support # initialize async exchanges


def warn_duplicated():
    """Warn the user that the new exchange version in ccxt (that we'll be using now)
    might differ from the one previously defined here"""
    if _ALREADY_MERGED:
        merged_exchanges = "'" + "', '".join(_ALREADY_MERGED) + "'"
        warnings.warn("Exchanges %s have been added to ccxt. If you were using the old version (in ccxt_unmerged), there might be some differences." % merged_exchanges)

warn_duplicated()
