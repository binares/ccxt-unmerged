# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound


class bitrue(Exchange):

    def describe(self):
        return self.deep_extend(super(bitrue, self).describe(), {
            'id': 'bitrue',
            'name': 'Bitrue',
            'countries': ['US'],
            'version': 'v1',
            'rateLimit': 3000,
            'urls': {
                'logo': 'https://www.bitrue.com/includes/assets/346c710f38975f71fa8ea90f9f7457a3.svg',
                'api': 'https://www.bitrue.com/api',
                'www': 'https://bitrue.com',
                'doc': 'https://github.com/Bitrue/bitrue-official-api-docs',
                'referral': 'https://www.bitrue.com/activity/task/task-landing?inviteCode=TAEZWW&cn=900000',
            },
            'has': {
                'fetchMarkets': True,
                'fetchCurrencies': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchOrderBook': True,
                'fetchOrderBooks': False,
                'fetchTrades': True,
                'fetchTradingLimits': False,
                'fetchTradingFees': False,
                'fetchAllTradingFees': False,
                'fetchFundingFees': False,
                'fetchTime': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchBalance': True,
                'createMarketOrder': True,
                'createOrder': True,
                'cancelOrder': True,
                'cancelOrders': False,
                'cancelAllOrders': False,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '4h': '4h',
                '12h': '12h',
                '1d': '1d',
                '1w': '1w',
            },
            'api': {
                'public': {
                    'get': [
                        'exchangeInfo',
                        'ticker/24hr',
                        'ticker/24hr',
                        'depth',
                        'trades',
                        'time',
                    ],
                },
                'private': {
                    'get': [
                        'account',
                        'order',
                        'openOrders',
                        'myTrades',
                        'allOrders',
                    ],
                    'post': [
                        'order',
                    ],
                    'delete':[
                        'order',
                    ]
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.1 / 100,
                    'taker': 0.1 / 100,
                },
            },
            'commonCurrencies': {
                'PLA': 'Plair',
            },
            'options': {
                'timeDifference': None,  # the difference between system clock and Bitrue clock, normally about 57 seconds
                'adjustForTimeDifference': True,
            },
            'exceptions': {
                'codes': {
                    '-1': BadRequest,
                    '-2': BadRequest,
                    '1001': BadRequest,
                    '1004': ArgumentsRequired,
                    '1006': AuthenticationError,
                    '1008': AuthenticationError,
                    '1010': AuthenticationError,
                    '1011': PermissionDenied,
                    '2001': AuthenticationError,
                    '2002': InvalidOrder,
                    '2004': OrderNotFound,
                    '9003': PermissionDenied,
                },
                'exact': {
                    'market does not have a valid value': BadRequest,
                    'side does not have a valid value': BadRequest,
                    'Account::AccountError: Cannot lock funds': InsufficientFunds,
                    'The account does not exist': AuthenticationError,
                },
            },
        })

    def fetch_markets(self, params={}):
        if self.options['adjustForTimeDifference']:
            self.load_time_difference()
        request = {'show_details': True}
        response = self.publicGetExchangeInfo(self.extend(request, params))
        result = []
        # symbols = self.safe_value(response, 'symbols')
        markets = self.safe_value(response, 'symbols')
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string_lower(market, 'symbol')
            base = self.safe_string_upper(market, 'baseAsset')
            quote = self.safe_string_upper(market, 'quoteAsset')
            baseId = base.lower()
            quoteId = quote.lower()
            symbol = base + '/' + quote
            filters = self.safe_value(market, 'filters')
            price_filter = self.safe_value(filters, 0)
            volume_filter = self.safe_value(filters, 1)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'info': market,
                'precision': {
                    'amount': self.safe_value(volume_filter, 'volumeScale'),
                    'price': self.safe_value(price_filter, 'priceScale'),
                    'base': self.safe_value(volume_filter, 'volumeScale'),
                    'quote': self.safe_value(price_filter, 'priceScale'),
                },
                'limits': {
                    'amount': {
                        'min': self.safe_value(volume_filter, 'minQty'),
                        'max': self.safe_value(volume_filter, 'maxQty'),
                    },
                    'price': {
                        'min': self.safe_value(price_filter, 'minPrice'),
                        'max': self.safe_value(price_filter, 'maxPrice'),
                    },
                    'cost': {
                        'min': self.safe_value(volume_filter, 'minQty'),
                        'max': self.safe_value(volume_filter, 'maxQty')
                    },
                },
            })
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetTicker24hr(self.extend(request, params))
        data = self.safe_value(response, 0)
        return self.parse_ticker(data, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetTicker24hr(params)
        # data = self.safe_value(response, 0, [])
        result = {}
        return self.parse_tickers(response, symbols)

    def parse_tickers(self, rawTickers, symbols=None):
        tickers = []
        for i in range(0, len(rawTickers)):
            tickers.append(self.parse_ticker(rawTickers[i]))
        return self.filter_by_array(tickers, 'symbol', symbols)

    def parse_ticker(self, ticker, market=None):
        symbol = None
        marketId = self.safe_string_lower(ticker, 'symbol')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_timestamp(ticker, 'closeTime')
        if timestamp is None or timestamp == 0:
            timestamp = self.milliseconds()
        vwap = self.safe_float(ticker, 'weightedAvgPrice')
        # response includes `volume`, but it is equal to `quoteVolume`
        # since e.g. BTC/USDT volume = quoteVolume ~ 30000000, we can assume it is quoteVolume 
        baseVolume = None
        quoteVolume = self.safe_float(ticker, 'quoteVolume')
        if (quoteVolume is not None) and (vwap is not None) and (vwap > 0):
            baseVolume = quoteVolume / vwap
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'highPrice'),
            'low': self.safe_float(ticker, 'lowPrice'),
            'bid': self.safe_float(ticker, 'bidPrice'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'askPrice'),
            'askVolume': None,
            'vwap': vwap,
            'open': self.safe_float(ticker, 'openPrice'),
            'close': self.safe_float(ticker, 'lastPrice'),
            'last': self.safe_float(ticker, 'lastPrice'),
            'previousClose': self.safe_float(ticker, 'prevClosePrice'),
            'change': self.safe_float(ticker, 'priceChange'),
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetDepth(self.extend(request, params))
        orderbook = response if response else {}
        timestamp = self.safe_integer(orderbook, 'lastUpdateId')
        return self.parse_order_book(orderbook, timestamp)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetTrades(self.extend(request, params))
        data = response if isinstance(response, list) else []
        return self.parse_trades(data, market, since, limit)

    def parse_trade(self, trade, market=None):
        isBuyMaker = self.safe_value(trade, 'isBuyerMaker')
        isBestMatch = self.safe_value(trade, 'isBestMatch')
        side = None
        if not isBuyMaker and isBestMatch:
            side = 'buy'
        elif isBuyMaker and isBestMatch:
            side = 'sell'
        symbol = None
        if market is not None:
            symbol = market['symbol']
        if symbol is None:
            if market is None:
                market = self.markets_by_id[self.safe_string_lower(trade, 'symbol')]
            symbol = market['symbol']
        timestamp = self.safe_integer(trade, 'time')
        if timestamp is None:
            timestamp = self.parse8601(self.safe_string(trade, 'time'))
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': self.safe_string(trade, 'id'),
            'order': None,
            'type': 'limit',
            'takerOrMaker': None,
            'side': side,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'qty'),
            'cost': None,
            'fee': None,
        }

    def fetch_time(self, params={}):
        response = self.publicGetTime(params)
        return self.safe_integer(response, 'serverTime')

    def load_time_difference(self, params={}):
        serverTime = self.fetch_time(params)
        after = self.milliseconds()
        self.options['timeDifference'] = after - serverTime
        return self.options['timeDifference']

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'private':
            self.check_required_credentials()
            timestamp = (self.milliseconds() - self.options['timeDifference']) if (self.options['timeDifference'] is not None) else 0
            query = self.extend({'timestamp': timestamp}, query)
            # Does it have to be sorted?
            # signStr = "&".join(["%s=%s" %(key, query[key]) for key in sorted(query.keys())])
            signStr = self.urlencode(query)
            signature = self.hmac(self.encode(signStr), self.encode(self.secret))
            query = self.extend({'signature': signature}, query)
            if method == 'GET':
                url += '?' + signStr + '&signature=' + signature
            else:
                body = signStr + '&signature=' + signature
        headers = {'Content-Type': 'application/json', 'X-MBX-APIKEY': self.apiKey}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        #
        #     {"code":1011,"message":"This IP '5.228.233.138' is not allowed","data":{}}
        #
        if response is None:
            return
        errorCode = self.safe_string(response, 'code')
        message = self.safe_string(response, 'message')
        if (errorCode is not None) and (errorCode != '0'):
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions['codes'], errorCode, feedback)
            self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
            raise ExchangeError(response)
