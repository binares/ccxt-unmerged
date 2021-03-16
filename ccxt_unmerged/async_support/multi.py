# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable


class multi(Exchange):

    def describe(self):
        return self.deep_extend(super(multi, self).describe(), {
            'id': 'multi',
            'name': 'multi',
            'countries': ['SG'],
            'version': 'v1',
            'rateLimit': 1000,
            'has': {
                'fetchMarkets': True,
                'fetchCurrencies': True,
                'fetchTradingLimits': False,
                'fetchTradingFees': True,
                'fetchFundingLimits': False,
                'fetchTicker': True,
                'fetchOrderBook': True,
                'fetchTrades': True,
                'fetchOHLCV': True,
                'fetchBalance': True,
                'fetchAccounts': False,
                'createOrder': True,
                'cancelOrder': True,
                'editOrder': False,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchOrders': True,
                'fetchMyTrades': True,
                'fetchDepositAddress': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'fetchTransactions': True,
                'fetchLedger': True,
                'withdraw': True,
                'transfer': False,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '10m': '10m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '4h': '4h',
                '6h': '6h',
                '8h': '8h',
                '12h': '12h',
                '1d': '1d',
                '1w': '1w',
                '1M': '1M',
            },
            'urls': {
                'logo': 'https://multi.io/en/static/img/icons/logo_white.svg',
                'api': 'https://api.multi.io/api',
                'www': 'https://multi.io/',
                'doc': 'https://docs.multi.io/',
            },
            'api': {
                'public': {
                    'get': [
                        'market/list',
                        'asset/list',
                        'order/depth',
                        'market/kline',
                        'fee_schedules',
                        'market/trade',
                        'market/status/all',
                    ],
                },
                'private': {
                    'get': [
                        'asset/balance',
                        'order/pending/detail',
                        'order/completed/detail',
                        'order/pending',
                        'order/pending/stoplimit',
                        'order/completed',
                        'order/completed/detail',
                        'market/user/trade',
                        'asset/transactions/withdraw',
                        'asset/transactions/deposit',
                        'asset/transactions/all',
                    ],
                    'post': [
                        'asset/deposit',
                        'order',
                        'order/cancel',
                        'asset/withdraw',
                    ],
                },
            },
            'exceptions': {
                'exact': {
                    '1': BadRequest,
                    '701': ArgumentsRequired,
                    '603': AuthenticationError,
                    '10': InvalidOrder,
                    '600': ArgumentsRequired,
                },
            },
            'whitelistErrorsAPIs': ['order/pending/detail', 'order/completed/detail'],
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetMarketList(params)
        return self.parse_markets(response)

    def parse_markets(self, markets):
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            base = self.safe_currency_code(market['base'])
            quote = self.safe_currency_code(market['quote'])
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'basePrec'),
                'price': self.safe_integer(market, 'quotePrec'),
            }
            result.append({
                'id': market['name'],
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': base.lower(),
                'quoteId': quote.lower(),
                'active': True,
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
                },
                'info': market,
            })
        return result

    async def fetch_currencies(self, params={}):
        response = await self.publicGetAssetList(params)
        return self.parse_currencies(response)

    def parse_currencies(self, currencies):
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            currencyCode = self.safe_string(currency, 'name')
            id = currencyCode.lower()
            numericId = self.safe_integer(currency, 'id')
            code = self.safe_currency_code(currencyCode)
            name = self.safe_string(currency, 'displayName')
            active = self.safe_value(currency, 'status')
            fee = self.safe_float(currency, 'withdrawFee')
            precision = self.safe_float(currency, 'precWithdraw')
            result[code] = {
                'id': id,
                'numericId': numericId,
                'code': code,
                'info': currency,
                'name': name,
                'active': active,
                'fee': fee,
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
                        'min': self.safe_float(currency, 'minWithdrawAmount'),
                        'max': None,
                    },
                },
            }
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 20
        response = await self.publicGetOrderDepth(self.extend(request, params))
        timestamp = self.safe_integer(response, 'timestamp')
        return self.parse_order_book(response, timestamp * 1000)

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        period = self.safe_string(self.timeframes, timeframe)
        intervalInSeconds = self.parse_timeframe(period)
        request['interval'] = intervalInSeconds
        now = self.seconds()
        if since is None:
            if limit is not None:
                start = now - limit * intervalInSeconds
                request['start'] = int(start)
        else:
            start = int(since / 1000)
            request['start'] = start
            if limit is not None:
                request['end'] = int(self.sum(start, limit * intervalInSeconds))
        response = await self.publicGetMarketKline(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        timestamp = self.safe_integer(ohlcv, 0) * 1000
        return [
            timestamp,
            self.safe_float(ohlcv, 1),
            self.safe_float(ohlcv, 3),
            self.safe_float(ohlcv, 4),
            self.safe_float(ohlcv, 2),
            self.safe_float(ohlcv, 5),
        ]

    async def fetch_trading_fees(self, params={}):
        await self.load_markets()
        response = await self.publicGetFeeSchedules(params)
        fees = []
        for i in range(0, len(response)):
            fee = response[i]
            fees.append({
                'minVolume': fee['minVolume'],
                'maker': fee['makerFee'],
                'taker': fee['takerFee'],
            })
        return {
            'info': response,
            'fees': fees,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = await self.publicGetMarketTrade(self.extend(request, params))
        return self.parse_trades(response['result'], market, since, limit)

    def parse_trade(self, trade, market):
        symbol = market['symbol']
        timestamp = self.safe_timestamp(trade, 'time')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        role = self.safe_string(trade, 'role')
        takerOrMaker = 'maker' if (role == '1') else 'taker'
        side = self.safe_string(trade, 'side')
        type = self.safe_value(trade, 'type')
        fee = {}
        fee['cost'] = self.safe_float(trade, 'fee')
        if side == '1' or type == 'sell':  # sell
            fee['currency'] = market['quote']
            side = 'sell'
        if side == '2' or type == 'buy':  # buy
            fee['currency'] = market['quote']
            side = 'buy'
        return {
            'info': trade,
            'id': self.safe_string(trade, 'id'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': float(price * amount),
            'order': self.safe_string(trade, 'id'),
            'takerOrMaker': takerOrMaker,
            'type': None,
            'fee': fee,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        response = await self.publicGetMarketStatusAll(params)
        marketTicket = self.get_market_ticket(response, marketId)
        return self.parse_ticker(marketTicket['result'], symbol)

    def get_market_ticket(self, response, marketId):
        marketTicker = {}
        for i in range(0, len(response)):
            if response[i]['market'] == marketId:
                marketTicker['result'] = response[i]
                break
        return marketTicker

    def parse_ticker(self, ticker, symbol):
        return {
            'symbol': symbol,
            'info': ticker,
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'open': self.safe_float(ticker, 'open'),
            'close': self.safe_float(ticker, 'close'),
            'last': self.safe_float(ticker, 'close'),
            'baseVolume': self.safe_float(ticker, 'baseVolume'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume'),
            'askVolume': None,
            'average': None,
            'change': None,
            'datetime': None,
            'percentage': None,
            'previousClose': None,
            'timestamp': None,
            'vwap': None,
        }

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetAssetBalance(params)
        exchange = response['exchange']
        keys = list(exchange.keys())
        result = {'info': exchange}
        for i in range(0, len(keys)):
            code = keys[i]
            result[code] = {
                'free': float(exchange[code]['available']),
                'used': float(exchange[code]['freeze']),
            }
        return self.parse_balance(result)

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'symbol': currency['code'],
        }
        response = await self.privatePostAssetDeposit(self.extend(request, params))
        currencyObject = self.safe_value(response, code)
        return {
            'currency': code,
            'address': currencyObject['address'],
            'tag': self.safe_value(currencyObject, 'memo'),
            'info': currencyObject,
        }

    def parse_order(self, order, market):
        timestamp = self.safe_timestamp(order, 'cTime')
        orderType = self.safe_string(order, 'type')
        orderSide = self.safe_string(order, 'side')
        type = 'limit' if (orderType == '1') else 'market'
        side = 'sell' if (orderSide == '1') else 'buy'
        amount = self.safe_float(order, 'amount')
        filled = amount - self.safe_float(order, 'left', 0)
        fee = {}
        if side == 'buy':
            fee['cost'] = self.safe_value(order, 'takerFee')
        else:
            fee['cost'] = self.safe_value(order, 'makerFee')
        fee['currency'] = market['quote']
        return {
            'id': self.safe_string(order, 'id'),
            'clientOrderId': None,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': None,
            'symbol': market['symbol'],
            'type': type,
            'side': side,
            'price': self.safe_float(order, 'price'),
            'average': None,
            'amount': amount,
            'filled': filled,
            'remaining': self.safe_float(order, 'left'),
            'cost': float(filled * self.safe_float(order, 'price')),
            'trades': None,
            'fee': fee,
            'info': order,
        }

    async def fetch_open_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'orderId': id,
            'type': 'limit',
        }
        fetchLimitOrderResponse = await self.privateGetOrderPendingDetail(self.extend(request, params))
        if fetchLimitOrderResponse:
            return self.parse_order(fetchLimitOrderResponse, market)
        request['type'] = 'stoplimit'
        fetchStopLimitOrderResponse = await self.privateGetOrderPendingDetail(self.extend(request, params))
        if fetchStopLimitOrderResponse:
            return self.parse_order(fetchStopLimitOrderResponse, market)
        return None

    async def fetch_complete_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'orderId': id,
        }
        response = await self.privateGetOrderCompletedDetail(self.extend(request, params))
        return self.parse_order(response, market)

    async def fetch_order(self, id, symbol=None, params={}):
        openOrder = await self.fetch_open_order(id, symbol, params)
        if openOrder:
            return openOrder
        completeOrder = await self.fetch_complete_order(id, symbol)
        if completeOrder:
            return completeOrder
        raise OrderNotFound(self.id + ' order ' + id + ' not found')

    async def fetch_limit_pending_orders(self, marketId, limit=None, params={}):
        request = {
            'market': marketId,
            'limit': limit,
        }
        response = await self.privateGetOrderPending(self.extend(request, params))
        return self.safe_value(response, 'records')

    async def fetch_stop_limit_pending_orders(self, marketId, limit=None, params={}):
        request = {
            'market': marketId,
            'limit': limit,
        }
        response = await self.privateGetOrderPendingStoplimit(self.extend(request, params))
        return self.safe_value(response, 'records')

    async def fetch_complete_orders(self, marketId, limit=None, params={}):
        request = {
            'market': marketId,
            'limit': limit,
        }
        response = await self.privateGetOrderCompleted(self.extend(request, params))
        return self.safe_value(response, 'records')

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        pendingLimitOrdersPromise = self.fetch_limit_pending_orders(marketId, limit, params)
        pendingStopLimitOrdersPromise = self.fetch_stop_limit_pending_orders(marketId, limit, params)
        limitOrders = await pendingLimitOrdersPromise
        stopLimitOrders = await pendingStopLimitOrdersPromise
        return self.parse_orders(limitOrders.concat(stopLimitOrders), market, since, limit, params)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        pendingLimitOrdersPromise = self.fetch_limit_pending_orders(marketId, limit, params)
        pendingStopLimitOrdersPromise = self.fetch_stop_limit_pending_orders(marketId, limit, params)
        completeOrdersPromise = self.fetch_complete_orders(marketId, limit, params)
        limitOrders = await pendingLimitOrdersPromise
        stopLimitOrders = await pendingStopLimitOrdersPromise
        completeOrders = await completeOrdersPromise
        allOrders = limitOrders.concat(stopLimitOrders, completeOrders)
        return self.parse_orders(allOrders, market, since, limit, params)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if since:
            request['since'] = int(since / 1000)
        if limit:
            request['limit'] = limit
        response = await self.privateGetMarketUserTrade(self.extend(request, params))
        return self.parse_trades(response['records'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'side': 1 if (side == 'sell') else 2,
            'amount': amount,
            'price': price,
            'type': type,
        }
        if self.safe_value(params, 'type') == 'stopLimit':
            request['type'] = 'stoplimit'
            request['stop'] = self.safe_value(params, 'stopPrice')
            request['gtlt'] = self.safe_value(params, 'gtlt', 1)
            params = self.omit(params, ['type', 'stopPrice', 'gtlt'])
        response = await self.privatePostOrder(self.extend(request, params))
        return self.parse_order(response, market)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'orderId': id,
            'type': 'limit',  # TODO support cancelling stop limit order
        }
        response = await self.privatePostOrderCancel(self.extend(request, params))
        return {'success': True, 'info': response}

    async def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'symbol': currency['code'],
        }
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetAssetTransactionsWithdraw(self.extend(request, params))
        return self.parse_transactions(response['result'], currency, since, limit, params)

    async def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'symbol': currency['code'],
        }
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetAssetTransactionsDeposit(self.extend(request, params))
        return self.parse_transactions(response['result'], currency, since, limit, params)

    async def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'symbol': currency['code'],
        }
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetAssetTransactionsAll(self.extend(request, params))
        return self.parse_transactions(response['result'], currency, since, limit, params)

    def parse_transaction(self, transaction, currency):
        addressFrom = None
        addressTo = None
        tagFrom = None
        tagTo = None
        address = self.safe_value(transaction, 'address')
        tag = self.safe_value(transaction, 'memo')
        type = self.safe_value(transaction, 'type')
        if type == 'WITHDRAW':
            addressTo = address
            tagTo = tag
        if type == 'DEPOSIT':
            addressFrom = address
            tagFrom = tag
        return {
            'info': transaction,
            'id': self.safe_value(transaction, 'id'),
            'txid': self.safe_value(transaction, 'txhash'),
            'timestamp': self.safe_timestamp(transaction, 'nonce'),
            'datetime': self.safe_value(transaction, 'createdAt'),
            'addressFrom': addressFrom,
            'address': address,
            'addressTo': addressTo,
            'tagFrom': tagFrom,
            'tag': tag,
            'tagTo': tagTo,
            'type': type.lower(),
            'amount': self.safe_float(transaction, 'amount'),
            'currency': self.safe_value(transaction, 'symbol'),
            'status': self.safe_value(transaction, 'status'),
            'fee': None,
        }

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'amount': amount,
            'symbol': currency['code'],
            'address': address,
        }
        if tag is not None:
            request['memo'] = tag
        response = await self.privatePostAssetWithdraw(self.extend(request, params))
        return {
            'info': self.extend({'status': 'ok'}, response),
        }

    def sign(self, path, api='public', method='GET', params=None, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + path
        query = self.omit(params, self.extract_params(path))
        if method == 'GET':
            if params:
                url += '?' + self.urlencode(params)
        if api == 'private':
            self.check_required_credentials()
            timestamp = int(math.floor(self.milliseconds()) / 1000)
            payloadToSign = {}
            if method == 'GET' and params:
                payloadToSign = {}
            if method == 'POST':
                body = self.json(query)
                payloadToSign = query
            message = self._make_query_string(self.extend({}, payloadToSign, {timestamp, method, path})).substr(1)
            signature = self.hmac(self.encode(message), self.encode(self.secret), hashlib.sha256, 'hex')
            headers = {
                'Content-Type': 'application/json',
                'X-MULTI-API-KEY': self.apiKey,
                'X-MULTI-API-SIGNATURE': signature,
                'X-MULTI-API-TIMESTAMP': timestamp,
                'X-MULTI-API-SIGNED-PATH': path,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def _make_query_string(self, q):
        arr = []
        if q:
            sortedParams = self.keysort(q)
            keys = list(sortedParams.keys())
            for i in range(0, len(keys)):
                key = keys[i]
                arr.append(self.encode_uri_component(key) + '=' + self.encode_uri_component(q[key]))
            return '?' + '&'.join(arr)
        else:
            return ''

    def check_if_whitelisted_path(self, url):
        whitelistedUrl = False
        for i in range(0, len(self.whitelistErrorsAPIs)):
            path = self.whitelistErrorsAPIs[i]
            if url.find(path) != -1:
                whitelistedUrl = True
                break
        return whitelistedUrl

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        status = self.safe_string(response, 'status')
        if code >= 200 and code < 300:
            return
        if self.check_if_whitelisted_path(url):
            return  # default to defaultErrorHandler
        if code == 429:
            raise DDoSProtection(self.id + ' ' + body)
        if status == 'error':
            errors = self.safe_value(response, 'errors')
            errorCode = self.safe_string(errors[0], 'code')
            message = self.safe_string(errors[0], 'message')
            self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, message)

    def default_error_handler(self, code, reason, url, method, headers, body, response):
        if (code >= 200) and (code <= 299):
            return
        details = body
        codeAsString = str(code)
        ErrorClass = None
        if self.check_if_whitelisted_path(url):
            return
        if self.httpExceptions.find(codeAsString) != -1:
            ErrorClass = self.httpExceptions[codeAsString]
        if ErrorClass == ExchangeNotAvailable:
            details += '(possible reasons: ' + ', '.join([
                'invalid API keys',
                'bad or old nonce',
                'exchange is down or offline',
                'on maintenance',
                'DDoS protection',
                'rate-limiting',
            ]) + ')'
        if ErrorClass is not None:
            raise ErrorClass(' '.join([self.id, method, url, code, reason, details]))

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        return self.safe_value(response, 'data')
