# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import base64
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InvalidOrder


class foblgate(Exchange):

    def describe(self):
        return self.deep_extend(super(foblgate, self).describe(), {
            'id': 'foblgate',
            'name': 'FOBLGATE',
            'countries': ['KR'],  # South Korea
            'rateLimit': 500,
            'has': {
                'CORS': True,
                'createOrder': True,
                'cancelOrder': True,
                'createMarketOrder': True,
                'fetchTicker': False,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchOrder': True,
                'fetchTrades': True,
                'fetchMyTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/69025125/89286704-a5495200-d68d-11ea-8486-fe3fa693e4a6.jpg',
                'api': {
                    'public': 'https://api2.foblgate.com',
                    'private': 'https://api2.foblgate.com',
                },
                'www': 'https://www.foblgate.com',
                'doc': 'https://api-document.foblgate.com',
                'fees': 'https://www.foblgate.com/fees',
            },
            'api': {
                'public': {
                    'post': [
                        'ccxt/marketList',
                        'ccxt/orderBook',
                        'ccxt/trades',
                    ],
                },
                'private': {
                    'post': [
                        'ccxt/balance',
                        'ccxt/myTrades',
                        'ccxt/createOrder',
                        'ccxt/cancelOrder',
                        'ccxt/orderDetail',
                        'ccxt/openOrders',
                        'ccxt/closedOrders',
                    ],
                },
            },
            'requiredCredentials': {
                'uid': True,
            },
            'exceptions': {
                '400': BadRequest,
                '401': AuthenticationError,
                '403': AuthenticationError,
                '500': ExchangeError,
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicPostCcxtMarketList(params)
        marketList = self.safe_value(response, 'marketList')
        # {
        #     'ETH/BTC': {
        #         limits: {amount: [Object], price: [Object], cost: [Object]},
        #         precision: {amount: 8, price: 8},
        #         tierBased: False,
        #             percentage: True,
        #             taker: 0.03,
        #             maker: 0.03,
        #             symbol: 'ETH/BTC',
        #             active: True,
        #             baseId: 'ETH',
        #             quoteId: 'BTC',
        #             quote: 'BTC',
        #             id: 'ETH-BTC',
        #             base: 'ETH',
        #             info: {market: 'ETH/BTC', coinName: 'ETH', coinNameKo: '이더리움'}
        #     }
        # }
        return marketList

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'pairName': symbol,
        }
        if limit is not None:
            request['count'] = limit
        response = await self.publicPostCcxtOrderBook(self.extend(request, params))
        # {
        #     bids: [
        #         [303100, 11.68805904],
        #         [303000, 0.61282982],
        #         [302900, 0.59681086]
        #     ],
        #     asks: [
        #         [303700, 0.99953148],
        #         [303800, 0.66825562],
        #         [303900, 1.47346607],
        #     ],
        #     timestamp: None,
        #     datetime: None,
        #     nonce: None
        # }
        return self.parse_order_book(response, symbol, None, 'bids', 'asks', 'price', 'amount')

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         "transaction_date":"2020-04-23 22:21:46",
        #         "type":"ask",
        #         "units_traded":"0.0125",
        #         "price":"8667000",
        #         "total":"108337"
        #     }
        #
        # fetchOrder(private)
        #
        #     {
        #         "transaction_date": "1572497603902030",
        #         "price": "8601000",
        #         "units": "0.005",
        #         "fee_currency": "KRW",
        #         "fee": "107.51",
        #         "total": "43005"
        #     }
        #
        # a workaround for their bug in date format, hours are not 0-padded
        timestamp = None
        transactionDatetime = self.safe_string(trade, 'transaction_date')
        if transactionDatetime is not None:
            parts = transactionDatetime.split(' ')
            numParts = len(parts)
            if numParts > 1:
                transactionDate = parts[0]
                transactionTime = parts[1]
                if len(transactionTime) < 8:
                    transactionTime = '0' + transactionTime
                timestamp = self.parse8601(transactionDate + ' ' + transactionTime)
            else:
                timestamp = self.safe_integer_product(trade, 'transaction_date', 0.001)
        if timestamp is not None:
            timestamp -= 9 * 3600000  # they report UTC + 9 hours, server in Korean timezone
        type = None
        side = self.safe_string(trade, 'type')
        side = 'sell' if (side == 'ask') else 'buy'
        id = self.safe_string(trade, 'cont_no')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'units_traded')
        cost = self.safe_float(trade, 'total')
        if cost is None:
            if amount is not None:
                if price is not None:
                    cost = price * amount
        fee = None
        feeCost = self.safe_float(trade, 'fee')
        if feeCost is not None:
            feeCurrencyId = self.safe_string(trade, 'fee_currency')
            feeCurrencyCode = self.common_currency_code(feeCurrencyId)
            fee = {
                'cost': feeCost,
                'currency': feeCurrencyCode,
            }
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pairName': symbol,
            'since': since,
            'cnt': limit,
        }
        response = await self.publicPostCcxtTrades(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        return self.parse_trades(data, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pairName': symbol,
            'cnt': limit,
            'since': since,
        }
        response = await self.privatePostCcxtMyTrades(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        return self.parse_trades(data, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostCcxtBalance(params)
        # {
        #     BTC: {total: 0, used: 0, free: 0},
        #     ETH: {total: 0, used: 0, free: 0},
        #     info: {}
        # }
        return self.parse_balance(response)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise InvalidOrder(self.id + ' createOrder type = market, currently not supported.')
        action = None
        if side == 'buy':
            action = 'bid'
        elif side == 'sell':
            action = 'ask'
        else:
            raise InvalidOrder(self.id + ' createOrder allows buy or sell side only!')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pairName': market['symbol'],
            'type': type,
            'action': action,
            'amount': self.amount_to_precision(symbol, amount),
            'price': self.price_to_precision(symbol, price),
        }
        response = await self.privatePostCcxtCreateOrder(self.extend(request, params))
        # {
        #     info: {data: '2008042'},
        #     id: '2008042',
        #     symbol: 'BTC/KRW',
        #     type: 'limit',
        #     side: 'buy',
        #     amount: 0.1,
        #     price: 9000000
        # }
        return response

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'ordNo': id,
        }
        response = await self.privatePostCcxtCancelOrder(self.extend(request, params))
        # {status: '0'}
        return response

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        timestamp = self.safe_value(order, 'timestamp')
        lastTradeTimestamp = self.safe_value(order, 'lastTradeTimestamp')
        symbol = self.safe_string(order, 'symbol')
        type = self.safe_string(order, 'type')
        side = self.safe_string(order, 'side')
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        cost = self.safe_float(order, 'cost')
        average = self.safe_float(order, 'average')
        filled = self.safe_float(order, 'filled')
        remaining = self.safe_float(order, 'remaining')
        status = self.safe_string(order, 'status')
        fee = self.safe_value(order, 'fee')
        trades = self.safe_value(order, 'trades', [])
        trades = self.parse_trades(trades, market, None, None, {
            'order': id,
            'type': type,
        })
        return {
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': trades,
        }

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'ordNo': id,
        }
        response = await self.privatePostCcxtOrderDetail(self.extend(request, params))
        order = self.safe_value(response, 'order')
        return self.parse_order(order)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pairName': market['symbol'],
            'since': since,
            'cnt': limit,
        }
        response = await self.privatePostCcxtOpenOrders(self.extend(request, params))
        orderList = self.safe_value(response, 'orderList', [])
        return self.parse_orders(orderList, market, since, limit)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pairName': market['symbol'],
            'since': since,
            'cnt': limit,
        }
        response = await self.privatePostCcxtClosedOrders(self.extend(request, params))
        orderList = self.safe_value(response, 'orderList', [])
        return self.parse_orders(orderList, market, since, limit)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        endpoint = '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + endpoint
        query = self.omit(params, self.extract_params(path))
        if method != 'POST':
            if query:
                url += '?' + self.urlencode(query)
        else:
            if api == 'private':
                self.check_required_credentials()
                body = self.urlencode(query)
                nonce = str(self.nonce())
                auth = self.urlencode(self.extend({
                    'apiKey': self.apiKey,
                    'mbId': self.uid,
                    'nonce': nonce,
                }, query))
                signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512)
                signature64 = self.decode(base64.b64encode(self.encode(signature)))
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Api-Key': self.apiKey,
                    'Api-Uid': self.uid,
                    'Api-Sign': str(signature64),
                    'Api-Nonce': nonce,
                }
            else:
                body = self.urlencode(query)
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        code = self.safe_value(response, 'code')
        if code is not None:
            if code == '0':
                return
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions, code, feedback)
            raise ExchangeError(feedback)  # unknown message
