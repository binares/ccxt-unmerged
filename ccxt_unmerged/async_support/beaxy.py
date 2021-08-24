# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange


class beaxy(Exchange):

    def describe(self):
        return self.deep_extend(super(beaxy, self).describe(), {
            'id': 'beaxy',
            'name': 'Beaxy',
            'countries': ['US'],
            'rateLimit': 500,
            'userAgent': self.userAgents['chrome'],
            'has': {
                'CORS': False,
                'fetchMarkets': True,
                'fetchCurrencies': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchOrderBook': True,
                'fetchOHLCV': True,
            },
            'timeframes': {
                '1m': 'MINUTE',
                '5m': 'MINUTE5',
                '15m': 'MINUTE15',
                '30m': 'MINUTE30',
                '1h': 'HOUR',
                '4h': 'HOUR4',
                '8h': 'HOUR8',
                '1d': 'DAY',
                '1w': 'WEEK',
            },
            'urls': {
                'api': {
                    'public': 'https://services.beaxy.com/api/v2',
                },
                'www': 'https://beaxy.com',
                'doc': 'https://beaxyapiv2.docs.apiary.io',
            },
            'api': {
                'public': {
                    'get': [
                        'symbols',
                        'currencies',
                        'symbols/rates',
                        'symbols/{market}/rate',
                        'symbols/{market}/trades',
                        'symbols/{market}/chart',
                        'symbols/{market}/book',
                    ],
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetSymbols(params)
        #
        # [{
        #     symbol: "ETCBTC",
        #     name: "ETCBTC",
        #     minimumQuantity: 0.01,
        #     maximumQuantity: 2509.41,
        #     quantityIncrement: 1e-7,
        #     quantityPrecision: 7,
        #     tickSize: 1e-7,
        #     baseCurrency: "ETC",
        #     termCurrency: "BTC",
        #     pricePrecision: 7,
        #     suspendedForTrading: False
        # }]
        #
        result = []
        for i in range(0, len(response)):
            market = response[i]
            id = self.safe_string(market, 'name')
            uuid = self.safe_string(market, 'symbol')
            baseId = self.safe_string(market, 'baseCurrency')
            quoteId = self.safe_string(market, 'termCurrency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            suspended = self.safe_value(market, 'suspendedForTrading', False)
            precision = {
                'amount': self.safe_integer(market, 'quantityPrecision'),
                'price': self.safe_integer(market, 'pricePrecision'),
            }
            limits = {
                'price': {
                    'min': None,
                    'max': None,
                },
                'amount': {
                    'min': None,
                    'max': None,
                },
                'cost': {
                    'min': None,
                    'max': None,
                },
            }
            entry = {
                'id': id,
                'uuid': uuid,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
                'limits': limits,
                'active': not suspended,
            }
            result.append(entry)
        return result

    async def fetch_currencies(self, params={}):
        response = await self.publicGetCurrencies(params)
        #
        # [
        #     {
        #        "currency":"BXY",
        #        "name":"Beaxy Coin",
        #        "precision":8,
        #        "dailyDepositThreshold":1.0E9,
        #        "dailyWithdrawalThreshold":250000.0,
        #        "weeklyDepositThreshold":1.0E9,
        #        "weeklyWithdrawalThreshold":2.0E7,
        #        "monthlyDepositThreshold":1.0E9,
        #        "monthlyWithdrawalThreshold":5.0E7,
        #        "dailyDepositLimit":1.0E9,
        #        "dailyWithdrawalLimit":250000.0,
        #        "weeklyDepositLimit":1.0E9,
        #        "weeklyWithdrawalLimit":2.0E7,
        #        "monthlyDepositLimit":1.0E9,
        #        "monthlyWithdrawalLimit":5.0E7,
        #        "minimalWithdrawal":875.0,
        #        "type":"crypto"
        #     }
        # ]
        #
        result = {}
        for i in range(0, len(response)):
            currency = response[i]
            code = self.safe_string(currency, 'currency')
            precision = self.safe_integer(currency, 'precision')
            name = self.safe_string(currency, 'name')
            result[code] = {
                'id': code,
                'code': code,
                'name': name,
                'active': True,
                'fee': None,
                'precision': precision,
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
                },
            }
        return result

    def parse_trade(self, trade, market=None):
        side = self.safe_string(trade, 'side')
        timestamp = self.safe_integer(trade, 'timestamp')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'size')
        cost = None
        if (price is not None) and (amount is not None):
            cost = price * amount
        symbol = None
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': None,
            'order': None,
            'type': None,
            'takerOrMaker': None,
            'side': side.lower(),
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetSymbolsMarketTrades(self.extend(request, params))
        #
        # [
        #     {
        #        "price":8.3E-7,
        #        "size":27019.0,
        #        "side":"BUY",
        #        "timestamp":1593082296713
        #     }
        #  ]
        #
        return self.parse_trades(response, market, since, limit)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetSymbolsMarketRate(self.extend(request, params))
        return self.parse_ticker(response, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetSymbolsRates(params)
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            ticker = response[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return self.filter_by_array(result, 'symbol', symbols)

    def parse_ticker(self, ticker, market=None):
        #
        # {
        #    "ETCBTC":{
        #       "ask":6.67E-4,
        #       "bid":6.63E-4,
        #       "low24":6.57E-4,
        #       "high24":6.71E-4,
        #       "volume24":26.6879096,
        #       "change24":-0.4491017964071856,
        #       "price":6.62E-4,
        #       "volume":0.8439548,
        #       "timestamp":1593183000000
        #    }
        # }
        #
        timestamp = self.milliseconds()
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high24'),
            'low': self.safe_float(ticker, 'low24'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume24'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        #
        # {
        #    "symbol":"ETHBTC",
        #    "barType":"MINUTE5",
        #    "bars":[
        #       {
        #          "closeAsk":0.025308,
        #          "closeBid":0.025289,
        #          "highAsk":0.025319,
        #          "highBid":0.0253,
        #          "highMid":0.0253095,
        #          "lowAsk":0.025294,
        #          "lowBid":0.02527,
        #          "lowMid":0.025282,
        #          "openAsk":0.025294,
        #          "openBid":0.025274,
        #          "volume":0.0,
        #          "time":1593034200000
        #       }
        #    ]
        # }
        #
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'barType': self.timeframes[timeframe],
        }
        if limit is not None:
            request['count'] = limit
        response = await self.publicGetSymbolsMarketChart(self.extend(request, params))
        result = self.safe_value(response, 'bars', [])
        return self.parse_ohlcvs(result, market, timeframe, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #    {
        #       "closeAsk":0.025308,
        #       "closeBid":0.025289,
        #       "highAsk":0.025319,
        #       "highBid":0.0253,
        #       "highMid":0.0253095,
        #       "lowAsk":0.025294,
        #       "lowBid":0.02527,
        #       "lowMid":0.025282,
        #       "openAsk":0.025294,
        #       "openBid":0.025274,
        #       "volume":0.0,
        #       "time":1593034200000
        #    }
        #
        return [
            self.safe_integer(ohlcv, 'time'),
            self.safe_float(ohlcv, 'openBid'),
            self.safe_float(ohlcv, 'highBid'),
            self.safe_float(ohlcv, 'lowBid'),
            self.safe_float(ohlcv, 'closeBid'),
            self.safe_float(ohlcv, 'volume'),
        ]

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'depth': 20,
        }
        response = await self.publicGetSymbolsMarketBook(self.extend(request, params))
        #
        # {
        #    "type":"SNAPSHOT_FULL_REFRESH",
        #    "security":"BXYBTC",
        #    "timestamp":1593185579378,
        #    "sequenceNumber":11887,
        #    "entries":[
        #       {
        #          "action":"INSERT",
        #          "side":"ASK",
        #          "level":0,
        #          "numberOfOrders":null,
        #          "quantity":129541.0,
        #          "price":8.4E-7
        #       }]
        # }
        #
        result = self.safe_value(response, 'entries', [])
        timestamp = self.safe_integer(response, 'timestamp')
        return self.parse_order_book(result, symbol, timestamp, 'Buy', 'Sell', 'price', 'quantity')

    def parse_order_book(self, orderbook, symbol, timestamp=None, bidsKey='Buy', asksKey='Sell', priceKey='price', amountKey='size'):
        bids = []
        asks = []
        for i in range(0, len(orderbook)):
            bidask = orderbook[i]
            side = self.safe_string(bidask, 'side')
            if side == 'ASK':
                asks.append(self.parse_bid_ask(bidask, priceKey, amountKey))
            else:
                bids.append(self.parse_bid_ask(bidask, priceKey, amountKey))
        return {
            'symbol': symbol,
            'bids': self.sort_by(bids, 0, True),
            'asks': self.sort_by(asks, 0),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'nonce': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/'
        query = self.omit(params, self.extract_params(path))
        url += self.implode_params(path, params)
        if query:
            url += '?' + self.urlencode(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
