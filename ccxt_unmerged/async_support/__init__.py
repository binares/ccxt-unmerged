"""
Async versions of exchanges that are not present in ccxt
"""
import ccxt.async_support

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

# Add the custom-defined exchanges to ccxt.async_support
for attr,value in list(globals().items()):
    if isinstance(value, type) and issubclass(value, ccxt.async_support.Exchange):
        if not hasattr(ccxt.async_support, attr):
            setattr(ccxt.async_support, attr, value)
