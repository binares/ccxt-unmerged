# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import BadRequest
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported


class remitano(Exchange):

    def describe(self):
        return self.deep_extend(super(remitano, self).describe(), {
            'id': 'remitano',
            'name': 'Remitano',
            'countries': ['VN', 'NG', 'MY', 'CN', 'KH'],
            'rateLimit': 500,  # milliseconds
            'has': {
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchCurrencies': True,
                'fetchMarkets': True,
                'fetchOHLCV': False,
                'fetchOrderBook': True,
                'fetchTicker': False,
                'fetchTrades': False,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/59945063/89111386-54fca500-d47f-11ea-9304-397e37c3ad72.png',
                'api': 'https://api.remitano.com/api/v1',
                'www': 'https://remitano.com/',
                'referral': 'https://remitano.com/btc/?utm_source=github&utm_medium=ccxt&utm_campaign=github-featured-exchange',
                'doc': 'https://developers.remitano.com/',
            },
            'api': {
                'public': {
                    'get': [
                        'altcoins',
                        'rates/ads',
                        'markets/{symbol}/order_book',
                    ],
                },
                'private': {
                    'get': [
                        'users/coin_accounts',
                    ],
                    'post': [
                        'offers',
                        'coin_withdrawals',
                    ],
                    'put': [
                        'my_offers/{id}/disable',
                    ],
                },
            },
            # guide to get key: https://developers.remitano.com/docs/guides/generate-new-key
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
            },
            'exceptions': {
                '400': BadRequest,
                '401': PermissionDenied,
                '404': OrderNotFound,
            },
        })

    def default_coins(self):
        return ['btc', 'eth', 'usdt', 'bch', 'ltc', 'xrp']

    def default_coin_currencies(self):
        result = {}
        defaultCoins = self.default_coins()
        defaultCoinsLength = len(defaultCoins)
        for i in range(0, defaultCoinsLength):
            coin = defaultCoins[i]
            code = self.safe_currency_code(coin)
            result[code] = {
                'id': coin,
                'code': code,
                'name': coin,
                'active': True,
                'fee': None,
                'precision': None,
                'type': 'crypto',
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': None,
                        'max': None,
                    },
                    'info': coin,
                },
            }
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = 50
        response = self.publicGetMarketsSymbolOrderBook(self.extend(request, params))
        # {
        #     "bids": [...],
        #     "asks": [...]
        # }
        return self.parse_order_book(response)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if type != 'limit':
            raise NotSupported(self.id + ' not supported type ' + type + 'for create order, please use type: limit')
        coinCurrency = self.currency(market['base'])
        fiatCurrency = self.currency(market['quote'])
        request = {
            'payment_method': 'fiat_wallet',
            'coin_currency': coinCurrency['id'].lower(),
            'currency': fiatCurrency['id'].upper(),
            'offer_type': side,
            'price': price,
            'total_amount': amount,
        }
        response = self.privatePostOffers(self.extend(request, params))
        return {
            'id': self.safe_string(response, 'id'),
            'clientOrderId': None,
            'info': response,
            'timestamp': None,
            'datetime': None,
            'lastTradeTimestamp': None,
            'status': self.safe_string(response, 'status'),
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': None,
            'average': None,
            'remaining': None,
            'fee': None,
            'trades': None,
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': int(id),
        }
        response = self.privatePutMyOffersIdDisable(self.extend(request, params))
        return {
            'id': id,
            'info': response,
            'status': 'canceled',
        }

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetUsersCoinAccounts(params)
        # [{
        #     user_id: 1860848,
        #     coin_address_channel: 'coin_address_channel_1860848',
        #     formatted_address: '3KDvouReT7nmKNuvhNoj9WfLWsPvXCxsN7',
        #     balance: 0,
        #     frozen_balance: 0,
        #     available_balance: 0,
        #     available_withdrawable_balance: 0,
        #     type: 'coin',
        #     coin_currency: 'btc',
        #     currency: 'btc',
        #     equivalent_btc_balance: 0,
        #     address_with_type_arr: [{type: 'btc', address: '3KDvouReT7nmKNuvhNoj9WfLWsPvXCxsN7'}]
        # },...]
        accountsLength = len(response)
        result = {'info': response}
        for i in range(0, accountsLength):
            data = response[i]
            account = self.account()
            currencyId = self.safe_string(data, 'currency')
            code = self.safe_currency_code(currencyId)
            account['free'] = self.safe_float(data, 'available_withdrawable_balance')
            account['used'] = self.safe_float(data, 'frozen_balance')
            account['total'] = self.safe_float(data, 'balance')
            result[code] = account
        return self.parse_balance(result)

    def fetch_currencies(self, params={}):
        # default coins
        result = self.default_coin_currencies()
        # alt coins
        altcoins = self.publicGetAltcoins(params)
        # [
        #     {
        #         "currency": "bnb",
        #         "name": "Binance Coin",
        #         "symbol": null,
        #         "default_exchange": "binance_BNBUSD",
        #         "close_prices_7_days": [],
        #         "one_day_volume": 1378092503.05929
        #     }
        # ]
        altcoinsLength = len(altcoins)
        for i in range(0, altcoinsLength):
            currency = altcoins[i]
            id = self.safe_string(currency, 'currency')
            code = self.safe_currency_code(id)
            result[code] = {
                'id': id,
                'code': code,
                'name': self.safe_string(currency, 'name'),
                'active': True,
                'fee': None,
                'precision': None,
                'type': 'crypto',
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': None,
                        'max': None,
                    },
                    'info': currency,
                },
            }
        # fiats
        fiats = self.publicGetRatesAds(params)
        # [{
        #     "ae": {
        #         "currency": "AED",
        #         "btc_bid": null,
        #         "btc_ask": null,
        #         "eth_bid": 1416.732669,
        #         "eth_ask": null,
        #         "usdt_bid": 3.6333,
        #         "usdt_ask": null,
        #         "bch_bid": null,
        #         "bch_ask": null,
        #         "ltc_bid": null,
        #         "ltc_ask": null,
        #         "xrp_bid": null,
        #         "xrp_ask": null
        #     }
        # },...]
        countryCodes = list(fiats.keys())
        countryCodesLength = len(countryCodes)
        for i in range(0, countryCodesLength):
            currency = fiats[countryCodes[i]]
            id = self.safe_string(currency, 'currency')
            code = self.safe_currency_code(id)
            result[code] = {
                'id': id,
                'code': code,
                'name': id,
                'active': True,
                'fee': None,
                'precision': None,
                'type': 'fiat',
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': None,
                        'max': None,
                    },
                    'info': currency,
                },
            }
        return result

    def fetch_markets(self, params={}):
        result = []
        defaults = self.default_coins()
        countries = self.publicGetRatesAds(params)
        # {
        #     "ae": {
        #         "currency": "AED",
        #         "btc_bid": null,
        #         "btc_ask": null,
        #         "eth_bid": 1416.732669,
        #         "eth_ask": null,
        #         "usdt_bid": 3.6333,
        #         "usdt_ask": null,
        #         "bch_bid": null,
        #         "bch_ask": null,
        #         "ltc_bid": null,
        #         "ltc_ask": null,
        #         "xrp_bid": null,
        #         "xrp_ask": null
        #     }
        # }
        countryKeys = list(countries.keys())
        for i in range(0, len(countryKeys)):
            country = countries[countryKeys[i]]
            for i in range(0, len(defaults)):
                # create order only have COIN/FIAT
                baseId = defaults[i]
                quoteId = self.safe_string(country, 'currency')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                id = base + quote
                symbol = base + '/' + quote
                active = True
                result.append({
                    'id': id,
                    'symbol': symbol,
                    'base': base,
                    'quote': quote,
                    'baseId': baseId,
                    'quoteId': quoteId,
                    'active': active,
                    'info': country,
                    'precision': None,
                    'limits': {
                        'amount': {
                            'min': None,
                            'max': None,
                        },
                        'price': {
                            'min': None,
                            'max': None,
                        },
                    },
                })
        return result

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'coin_withdrawal[coin_address]': address,
            'coin_withdrawal[coin_amount]': float(amount),
            'coin_withdrawal[coin_currency]': currency['id'],
        }
        if tag is not None:
            request['coin_withdrawal[destination_tag]'] = tag
        response = self.privatePostCoinWithdrawals(self.extend(request, params))
        return {
            'id': self.safe_string(response, 'id'),
            'info': {'withdraw': response, 'confirm': 'You need to click confirm on your trusted devices'},
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if query:
            request += '?' + self.urlencode(query)
        url = self.urls['api'] + '/' + request
        if api == 'private':
            self.check_required_credentials()
            date = self.rfc2616(self.milliseconds())
            hashedBody = ''
            if body:
                hashedBody = self.hash(self.json(body), 'md5', 'base64')
            raw = method.upper() + ',application/json,' + hashedBody + ',/api/v1/' + request + ',' + date
            signature = self.hmac(raw, self.secret, hashlib.sha1, 'base64')
            headers = {
                'Content-Type': 'application/json',
                'Content-MD5': hashedBody,
                'DATE': date,
                'Authorization': 'APIAuth ' + self.apiKey + ':' + signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
