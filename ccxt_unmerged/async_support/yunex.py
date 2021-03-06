# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange


class yunex(Exchange):

    def describe(self):
        return self.deep_extend(super(yunex, self).describe(), {
            'id': 'yunex',
            'name': 'Yunex',
            'countries': ['Hong Kong'],
            'version': 'v1',
            'accounts': None,
            'accountsById': None,
            'has': {
                'CORS': True,
                'fetchMarkets': True,
                'fetchBalance': True,
                'createOrder': True,
                'cancelOrder': True,
                'fetchOHLCV': True,
                'fetchTicker': True,
                'fetchTickers': False,
                'fetchMyTrades': False,
                'fetchTrades': False,
                'fetchOrder': True,
                'fetchOrders': False,
                'fetchOrderBook': True,
                'fetchOpenOrders': False,
                'fetchClosedOrders': False,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '4h': '1hour',
                '1d': '1day',
            },
            'urls': {
                'logo': 'https://theme.zdassets.com/theme_assets/2289273/fdd2e3bf9e40a9751d199a337c48d8a48194ff7c.png',
                'api': 'https://a.yunex.io',
                'www': 'https://yunex.io/',
                'referral': 'https://yunex.io/user/register?inviter=16609',
                'doc': 'https://github.com/yunexio/openAPI',
                'fees': 'https://support.yunex.io/hc/en-us/articles/360003486391-Fees',
            },
            'api': {
                'public': {
                    'get': [
                        'api/v1/base/coins/tradepair',
                        'api/market/depth',
                        'api/market/trade/kline',
                        'api/market/trade/info',
                    ],
                },
                'private': {
                    'get': [
                        'api/v1/coin/balance',
                    ],
                    'post': [
                        'api/v1/order/buy',
                        'api/v1/order/sell',
                        'api/v1/order/cancel',
                        'api/v1/order/query',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.002,
                    'taker': 0.002,
                },
            },
            'funding': {
                'tierBased': False,
                'percentage': False,
                'deposit': {},
                'withdraw': {
                    'BTC': 0.001,
                    'ETH': 0.01,
                    'BCH': 0.001,
                    'LTC': 0.01,
                    'ETC': 0.01,
                    'USDT': 2,
                    'SNET': 20,
                    'KT': 20,
                    'YUN': 20,
                    'Rating': 20,
                    'YBT': 20,
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetApiV1BaseCoinsTradepair()
        data = response['data']
        result = []
        for i in range(0, len(data)):
            market = data[i]
            id = market['symbol']
            symbol = market['name']
            base = symbol.split('/')[0]
            quote = symbol.split('/')[1]
            baseId = market['base_coin_id']
            quoteId = market['coin_id']
            active = True
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'info': market,
            })
        return result

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
            'price': price,
            'volume': amount,
        }
        response = ''
        if side == 'buy':
            response = await self.privatePostApiV1OrderBuy(self.extend(request, params))
        elif side == 'sell':
            response = await self.privatePostApiV1OrderSell(self.extend(request, params))
        data = response['data']
        return {
            'info': response,
            'id': self.safe_string(data, 'order_id'),
        }

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        _symbol = self.market_id(symbol)
        request = {
            'symbol': _symbol,
            'order_id': id,
        }
        response = await self.privatePostApiV1OrderQuery(self.extend(request, params))
        order = self.parse_order(response['data'], _symbol)
        return order

    def parse_side(self, sideId):
        if sideId == 1:
            return 'buy'
        elif sideId == 2:
            return 'sell'
        else:
            return None

    def parse_order(self, order, symbol):
        id = self.safe_string(order, 'order_id')
        timestamp = self.safe_float(order, 'timestamp')
        sideId = self.safe_integer(order, 'type')
        side = self.parse_side(sideId)
        type = None
        price = self.safe_float(order, 'price')
        average = None
        amount = self.safe_float(order, 'volume')
        filled = self.safe_float(order, 'trade_volume')
        remaining = None
        if amount and filled:
            remaining = amount - filled
        status = self.parse_order_status(self.safe_string(order, 'status'))
        cost = None
        fee = None
        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
        }
        return result

    def parse_order_status(self, status):
        statuses = {
            '1': 'open',
            '2': 'closed',
            '3': 'canceled',
            '4': 'lose',
        }
        return statuses[status] if (status in statuses) else status

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'order_id': id,
        }
        if symbol is not None:
            request['symbol'] = self.market_id(symbol)
        results = await self.privatePostApiV1OrderCancel(self.extend(request, params))
        success = results['ok'] == 1
        returnVal = {'info': results, 'success': success}
        return returnVal

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        marketId = self.market_id(symbol)
        request = {
            'symbol': marketId,
        }
        if limit is not None:
            request['level'] = limit
        response = await self.publicGetApiMarketDepth(self.extend(request, params))
        return self.parse_order_book(response['data'], symbol)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv['ts'] * 1000,
            float(ohlcv['v'][0]),
            float(ohlcv['v'][3]),
            float(ohlcv['v'][2]),
            float(ohlcv['v'][1]),
            float(ohlcv['v'][4]),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=300, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'type': self.timeframes[timeframe],
        }
        if limit is not None:
            request['count'] = limit
        response = await self.publicGetApiMarketTradeKline(self.extend(request, params))
        # return response
        return self.parse_ohlcvs(response['data'], market, timeframe, since, limit)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.markets[symbol]
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetApiMarketTradeInfo(self.extend(request, params))
        data = response['data']
        timestamp = self.safe_integer(data, 'ts')
        timestamp = timestamp * 1000
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(data, 'max_price'),
            'low': self.safe_float(data, 'min_price'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': self.safe_float(data, 'open_price'),
            'close': self.safe_float(data, 'close_price'),
            'last': self.safe_float(data, 'close_price'),
            'previousClose': None,
            'change': self.safe_float(data, 'rate'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(data, 'volume'),
            'quoteVolume': None,
            'info': response,
        }

    async def fetch_balance(self, params={}):
        response = await self.privateGetApiV1CoinBalance()
        data = response['data']['coin']
        result = {'info': response}
        for i in range(0, len(data)):
            balance = data[i]
            currency = balance['name']
            account = None
            if currency in result:
                account = result[currency]
            else:
                account = self.account()
            result[currency] = account
            result[currency]['used'] = float(balance['freezed'])
            result[currency]['free'] = float(balance['usable'])
            result[currency]['total'] = float(balance['total'])
        return self.parse_balance(result)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
            headers = {
                'Content-Type': 'application/json',
            }
        else:
            self.check_required_credentials()
            ts = self.seconds()
            nonce = '308072f419'
            headers = {
                'Content-Type': 'application/json',
                '-x-ts': ts,
                '-x-nonce': nonce,
                '-x-key': self.apiKey,
            }
            str_parms = ''
            query = self.keysort(query)
            if method == 'POST':
                body = self.json(query)
                str_parms = body
            sign_str = str_parms + ts + nonce + self.secret
            sign = self.hash(self.encode(sign_str), 'sha256')
            headers['-x-sign'] = sign
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
