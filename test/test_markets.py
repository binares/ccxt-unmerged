# import pytest
import ccxt_unmerged
import ccxt
import traceback


def get_exchange_classes():
    exchange_classes = []
    for name in dir(ccxt_unmerged):
        obj = getattr(ccxt_unmerged, name)
        if isinstance(obj, type) and issubclass(obj, ccxt.Exchange):
            exchange_classes.append(obj)
    return exchange_classes


def get_exchanges():
    return [xc() for xc in get_exchange_classes()]


def test_load_markets():
    for xc_cls in get_exchange_classes():
        print("Loading {}'s markets".format(xc_cls.__name__))
        try:
            xc = xc_cls()
            xc.load_markets()
            if not xc.markets:
                print("No markets were loaded!")
        except Exception as e:
            traceback.print_exc()
