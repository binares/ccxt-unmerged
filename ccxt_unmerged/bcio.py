# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import ROUND


class bcio (Exchange):

    def describe(self):
        return self.deep_extend(super(bcio, self).describe(), {
            'id': 'bcio',
            'name': 'Blockchain.io',
            'countries': ['FR'],
            'rateLimit': 500,
            'certified': False,
            'has': {
                'fetchDepositAddress': False,
                'CORS': False,
                'fetchBidsAsks': True,
                'fetchTickers': True,
                'fetchOHLCV': True,
                'fetchMyTrades': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'withdraw': True,
                'fetchFundingFees': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'fetchTransactions': False,
            },
            'timeframes': {
                '1m': '1m',
                '3m': '3m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '4h': '4h',
                '6h': '6h',
                '8h': '8h',
                '12h': '12h',
                '1d': '1d',
                '3d': '3d',
                '1w': '1w',
                '1M': '1M',
            },
            'urls': {
                'logo': 'https://journalducoin.com/wp-content/uploads/2018/08/BCIO_logo_square_256px.png',
                'api': {
                    'web': 'https://www.trade.blockchain.io',
                    'public': 'https://api.blockchain.io/v1',
                    'private': 'https://api.blockchain.io/v1',
                },
                'www': 'https://www.blockchain.io',
                'doc': [
                    'https://github.com/bcio/api-documentation/blob/master/README.md',
                ],
                'fees': 'https://www.blockchain.io/fees',
            },
            'api': {
                'public': {
                    'get': [
                        'ping',
                        'time',
                        'depth',
                        'trades',
                        'aggTrades',
                        'klines',
                        'ticker/24hr',
                        'ticker/price',
                        'ticker/bookTicker',
                        'exchangeInfo',
                    ],
                },
                'private': {
                    'get': [
                        'order',
                        'openOrders',
                        'allOrders',
                        'account',
                        'myTrades',
                    ],
                    'post': [
                        'order',
                        'order/test',
                    ],
                    'delete': [
                        'order',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.01,
                    'maker': 0.01,
                },
            },
            'options': {
                'fetchTradesMethod': 'publicGetAggTrades',
                'fetchTickersMethod': 'publicGetTicker24hr',
                'defaultTimeInForce': 'GTC',
                'defaultLimitOrderType': 'limit',
                'hasAlreadyAuthenticatedSuccessfully': False,
                'warnOnFetchOpenOrdersWithoutSymbol': True,
                'recvWindow': 5 * 1000,
                'timeDifference': 0,
                'adjustForTimeDifference': False,
                'parseOrderToPrecision': False,
                'newOrderRespType': {
                    'market': 'FULL',
                    'limit': 'RESULT',
                },
            },
            'exceptions': {
                'API key does not exist': AuthenticationError,
                'Order would trigger immediately.': InvalidOrder,
                'Account has insufficient balance for requested action.': InsufficientFunds,
                'Rest API trading is not enabled.': ExchangeNotAvailable,
                '-1000': ExchangeNotAvailable,
                '-1013': InvalidOrder,
                '-1021': InvalidNonce,
                '-1022': AuthenticationError,
                '-1100': InvalidOrder,
                '-1104': ExchangeError,
                '-1128': ExchangeError,
                '-2010': ExchangeError,
                '-2011': OrderNotFound,
                '-2013': OrderNotFound,
                '-2014': AuthenticationError,
                '-2015': AuthenticationError,
            },
        })

    def nonce(self):
        return self.milliseconds() - self.options['timeDifference']

    def load_time_difference(self):
        response = self.publicGetTime()
        after = self.milliseconds()
        self.options['timeDifference'] = int(after - response['serverTime'])
        return self.options['timeDifference']

    def fetch_markets(self, params={}):
        response = self.publicGetExchangeInfo(params)
        if self.options['adjustForTimeDifference']:
            self.load_time_difference()
        markets = self.safe_value(response, 'symbols')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'symbol')
            if id == '123456':
                continue
            baseId = market['baseAsset']
            quoteId = market['quoteAsset']
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            filters = self.index_by(market['filters'], 'filterType')
            precision = {
                'base': market['baseAssetPrecision'],
                'quote': market['quotePrecision'],
                'amount': market['baseAssetPrecision'],
                'price': market['quotePrecision'],
            }
            status = self.safe_string(market, 'status')
            active = (status == 'TRADING')
            entry = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': -1 * math.log10(precision['amount']),
                        'max': None,
                    },
                },
            }
            if 'PRICE_FILTER' in filters:
                filter = filters['PRICE_FILTER']
                entry['limits']['price'] = {
                    'min': self.safe_float(filter, 'minPrice'),
                    'max': None,
                }
                maxPrice = self.safe_float(filter, 'maxPrice')
                if (maxPrice is not None) and (maxPrice > 0):
                    entry['limits']['price']['max'] = maxPrice
                entry['precision']['price'] = self.precision_from_string(filter['tickSize'])
            if 'LOT_SIZE' in filters:
                filter = self.safe_value(filters, 'LOT_SIZE', {})
                stepSize = self.safe_string(filter, 'stepSize')
                entry['precision']['amount'] = self.precision_from_string(stepSize)
                entry['limits']['amount'] = {
                    'min': self.safe_float(filter, 'minQty'),
                    'max': self.safe_float(filter, 'maxQty'),
                }
            if 'MIN_NOTIONAL' in filters:
                entry['limits']['cost']['min'] = self.safe_float(filters['MIN_NOTIONAL'], 'minNotional')
            result.append(entry)
        return result

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        key = 'quote'
        rate = market[takerOrMaker]
        cost = amount * rate
        precision = market['precision']['price']
        if side == 'sell':
            cost *= price
        else:
            key = 'base'
            precision = market['precision']['amount']
        cost = self.decimal_to_precision(cost, ROUND, precision, self.precisionMode)
        return {
            'type': takerOrMaker,
            'currency': market[key],
            'rate': rate,
            'cost': float(cost),
        }

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetAccount(params)
        result = {'info': response}
        balances = self.safe_value(response, 'balances', [])
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = balance['asset']
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'free')
            account['used'] = self.safe_float(balance, 'locked')
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetDepth(self.extend(request, params))
        orderbook = self.parse_order_book(response, symbol)
        orderbook['nonce'] = self.safe_integer(response, 'lastUpdateId')
        return orderbook

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_integer(ticker, 'closeTime')
        symbolId = self.safe_string(ticker, 'symbol')
        symbol = None
        if market is None and symbolId in self.marketsById:
            market = self.marketsById[symbolId]
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'lastPrice')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'highPrice'),
            'low': self.safe_float(ticker, 'lowPrice'),
            'bid': self.safe_float(ticker, 'bidPrice'),
            'bidVolume': self.safe_float(ticker, 'bidQty'),
            'ask': self.safe_float(ticker, 'askPrice'),
            'askVolume': self.safe_float(ticker, 'askQty'),
            'vwap': self.safe_float(ticker, 'weightedAvgPrice'),
            'open': self.safe_float(ticker, 'openPrice'),
            'close': last,
            'last': last,
            'previousClose': self.safe_float(ticker, 'prevClosePrice'),
            'change': self.safe_float(ticker, 'priceChange'),
            'percentage': self.safe_float(ticker, 'priceChangePercent'),
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume'),
            'info': ticker,
        }

    def fetch_status(self, params={}):
        systemStatus = self.wapiGetSystemStatus()
        status = self.safe_value(systemStatus, 'status')
        if status is not None:
            self.status = self.extend(self.status, {
                'status': status == 'ok' if 0 else 'maintenance',
                'updated': self.milliseconds(),
            })
        return self.status

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetTicker24hr(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_tickers(self, rawTickers, symbols=None):
        tickers = []
        for i in range(0, len(rawTickers)):
            tickers.append(self.parse_ticker(rawTickers[i]))
        return self.filter_by_array(tickers, 'symbol', symbols)

    def fetch_bids_asks(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetTickerBookTicker(params)
        return self.parse_tickers(response, symbols)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        method = self.options['fetchTickersMethod']
        response = getattr(self, method)(params)
        return self.parse_tickers(response, symbols)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv[0],
            float(ohlcv[1]),
            float(ohlcv[2]),
            float(ohlcv[3]),
            float(ohlcv[4]),
            float(ohlcv[5]),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'interval': self.timeframes[timeframe],
        }
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetKlines(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        if 'isDustTrade' in trade:
            return self.parse_dust_trade(trade, market)
        timestamp = self.safe_integer_2(trade, 'T', 'time')
        price = self.safe_float_2(trade, 'p', 'price')
        amount = self.safe_float_2(trade, 'q', 'qty')
        id = self.safe_string_2(trade, 'a', 'id')
        side = None
        orderId = self.safe_string(trade, 'orderId')
        if 'm' in trade:
            side = 'sell' if trade['m'] else 'buy'
        elif 'isBuyerMaker' in trade:
            side = 'sell' if trade['isBuyerMaker'] else 'buy'
        else:
            if 'isBuyer' in trade:
                side = 'buy' if (trade['isBuyer']) else 'sell'
        fee = None
        if 'commission' in trade:
            fee = {
                'cost': self.safe_float(trade, 'commission'),
                'currency': self.safe_currency_code(self.safe_string(trade, 'commissionAsset')),
            }
        takerOrMaker = None
        if 'isMaker' in trade:
            takerOrMaker = 'maker' if trade['isMaker'] else 'taker'
        symbol = None
        if market is None:
            marketId = self.safe_string(trade, 'symbol')
            market = self.safe_value(self.markets_by_id, marketId)
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': orderId,
            'type': None,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': price * amount,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if self.options['fetchTradesMethod'] == 'publicGetAggTrades':
            if since is not None:
                request['startTime'] = since
                request['endTime'] = self.sum(since, 3600000)
        if limit is not None:
            request['limit'] = limit
        method = self.safe_value(self.options, 'fetchTradesMethod', 'publicGetTrades')
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            'NEW': 'open',
            'PARTIALLY_FILLED': 'open',
            'FILLED': 'closed',
            'CANCELED': 'canceled',
            'PENDING_CANCEL': 'canceling',
            'REJECTED': 'rejected',
            'EXPIRED': 'expired',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        status = self.parse_order_status(self.safe_string(order, 'status'))
        symbolId = self.safe_string(order, 'symbol')
        symbol = None
        if market is None and symbolId in self.marketsById:
            market = self.marketsById[symbolId]
        if market is not None:
            symbol = market['symbol']
        timestamp = None
        if 'time' in order:
            timestamp = self.safe_integer(order, 'time')
        elif 'transactTime' in order:
            timestamp = self.safe_integer(order, 'transactTime')
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'origQty')
        filled = self.safe_float(order, 'executedQty')
        remaining = None
        cost = self.safe_float(order, 'cummulativeQuoteQty')
        if filled is not None:
            if amount is not None:
                remaining = amount - filled
                if self.options['parseOrderToPrecision']:
                    remaining = float(self.amount_to_precision(symbol, remaining))
                remaining = max(remaining, 0.0)
            if price is not None:
                if cost is None:
                    cost = price * filled
        id = self.safe_string(order, 'orderId')
        type = self.safe_string_lower(order, 'type')
        if type == 'market':
            if price == 0.0:
                if (cost is not None) and (filled is not None):
                    if (cost > 0) and (filled > 0):
                        price = cost / filled
        side = self.safe_string_lower(order, 'side')
        fee = None
        trades = None
        fills = self.safe_value(order, 'fills')
        if fills is not None:
            trades = self.parse_trades(fills, market)
            numTrades = len(trades)
            if numTrades > 0:
                cost = trades[0]['cost']
                fee = {
                    'cost': trades[0]['fee']['cost'],
                    'currency': trades[0]['fee']['currency'],
                }
                for i in range(1, len(trades)):
                    cost = self.sum(cost, trades[i]['cost'])
                    fee['cost'] = self.sum(fee['cost'], trades[i]['fee']['cost'])
        average = None
        if cost is not None:
            if filled:
                average = cost / filled
            if self.options['parseOrderToPrecision']:
                cost = float(self.cost_to_precision(symbol, cost))
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
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

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePostOrder'
        test = self.safe_value(params, 'test', False)
        if test:
            method += 'Test'
            params = self.omit(params, 'test')
        uppercaseType = type.upper()
        newOrderRespType = self.safe_value(self.options['newOrderRespType'], type, 'RESULT')
        request = {
            'symbol': market['id'],
            'quantity': self.amount_to_precision(symbol, amount),
            'type': uppercaseType,
            'side': side.upper(),
            'newOrderRespType': newOrderRespType,
        }
        timeInForceIsRequired = False
        priceIsRequired = False
        stopPriceIsRequired = False
        if uppercaseType == 'LIMIT':
            priceIsRequired = True
            timeInForceIsRequired = True
        elif (uppercaseType == 'STOP_LOSS') or (uppercaseType == 'TAKE_PROFIT'):
            stopPriceIsRequired = True
        elif (uppercaseType == 'STOP_LOSS_LIMIT') or (uppercaseType == 'TAKE_PROFIT_LIMIT'):
            stopPriceIsRequired = True
            priceIsRequired = True
            timeInForceIsRequired = True
        elif uppercaseType == 'LIMIT_MAKER':
            priceIsRequired = True
        if priceIsRequired:
            if price is None:
                raise InvalidOrder(self.id + ' createOrder method requires a price argument for a ' + type + ' order')
            request['price'] = self.price_to_precision(symbol, price)
        if timeInForceIsRequired:
            request['timeInForce'] = self.options['defaultTimeInForce']
        if stopPriceIsRequired:
            stopPrice = self.safe_float(params, 'stopPrice')
            if stopPrice is None:
                raise InvalidOrder(self.id + ' createOrder method requires a stopPrice extra param for a ' + type + ' order')
            else:
                params = self.omit(params, 'stopPrice')
                request['stopPrice'] = self.price_to_precision(symbol, stopPrice)
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_order(response, market)

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        origClientOrderId = self.safe_value(params, 'origClientOrderId')
        request = {
            'symbol': market['id'],
        }
        if origClientOrderId is not None:
            request['origClientOrderId'] = origClientOrderId
        else:
            request['orderId'] = int(id)
        response = self.privateGetOrder(self.extend(request, params))
        return self.parse_order(response, market)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetAllOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        elif self.options['warnOnFetchOpenOrdersWithoutSymbol']:
            symbols = self.symbols
            numSymbols = len(symbols)
            fetchOpenOrdersRateLimit = int(numSymbols / 2)
            raise ExchangeError(self.id + ' fetchOpenOrders WARNING: fetching open orders without specifying a symbol is rate-limited to one call per ' + str(fetchOpenOrdersRateLimit) + ' seconds. Do not call self method frequently to avoid ban. Set ' + self.id + '.options["warnOnFetchOpenOrdersWithoutSymbol"] = False to suppress self warning message.')
        response = self.privateGetOpenOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'orderId': int(id),
        }
        response = self.privateDeleteOrder(self.extend(request, params))
        return self.parse_order(response)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetMyTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_my_dust_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        response = self.wapiGetUserAssetDribbletLog(params)
        results = self.safe_value(response, 'results', {})
        rows = self.safe_value(results, 'rows', [])
        data = []
        for i in range(0, len(rows)):
            logs = rows[i]['logs']
            for j in range(0, len(logs)):
                logs[j]['isDustTrade'] = True
                data.append(logs[j])
        trades = self.parse_trades(data, None, since, limit)
        return self.filter_by_since_limit(trades, since, limit)

    def parse_dust_trade(self, trade, market=None):
        orderId = self.safe_string(trade, 'tranId')
        timestamp = self.parse8601(self.safe_string(trade, 'operateTime'))
        tradedCurrency = self.safe_currency_code(self.safe_string(trade, 'fromAsset'))
        earnedCurrency = self.currency('BNB')['code']
        applicantSymbol = earnedCurrency + '/' + tradedCurrency
        tradedCurrencyIsQuote = False
        if applicantSymbol in self.markets:
            tradedCurrencyIsQuote = True
        fee = {
            'currency': earnedCurrency,
            'cost': self.safe_float(trade, 'serviceChargeAmount'),
        }
        symbol = None
        amount = None
        cost = None
        side = None
        if tradedCurrencyIsQuote:
            symbol = applicantSymbol
            amount = self.sum(self.safe_float(trade, 'transferedAmount'), fee['cost'])
            cost = self.safe_float(trade, 'amount')
            side = 'buy'
        else:
            symbol = tradedCurrency + '/' + earnedCurrency
            amount = self.safe_float(trade, 'amount')
            cost = self.sum(self.safe_float(trade, 'transferedAmount'), fee['cost'])
            side = 'sell'
        price = None
        if cost is not None:
            if amount:
                price = cost / amount
        id = None
        type = None
        takerOrMaker = None
        return {
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': orderId,
            'type': type,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'amount': amount,
            'price': price,
            'cost': cost,
            'fee': fee,
            'info': trade,
        }

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        currency = None
        request = {}
        if code is not None:
            currency = self.currency(code)
            request['asset'] = currency['id']
        if since is not None:
            request['startTime'] = since
        response = self.wapiGetDepositHistory(self.extend(request, params))
        return self.parse_transactions(response['depositList'], currency, since, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        currency = None
        request = {}
        if code is not None:
            currency = self.currency(code)
            request['asset'] = currency['id']
        if since is not None:
            request['startTime'] = since
        response = self.wapiGetWithdrawHistory(self.extend(request, params))
        return self.parse_transactions(response['withdrawList'], currency, since, limit)

    def parse_transaction_status_by_type(self, status, type=None):
        if type is None:
            return status
        statuses = {
            'deposit': {
                '0': 'pending',
                '1': 'ok',
            },
            'withdrawal': {
                '0': 'pending',
                '1': 'canceled',
                '2': 'pending',
                '3': 'failed',
                '4': 'pending',
                '5': 'failed',
                '6': 'ok',
            },
        }
        return statuses[type][status] if (status in list(statuses[type].keys())) else status

    def parse_transaction(self, transaction, currency=None):
        id = self.safe_string(transaction, 'id')
        address = self.safe_string(transaction, 'address')
        tag = self.safe_string(transaction, 'addressTag')
        if tag is not None:
            if len(tag) < 1:
                tag = None
        txid = self.safe_value(transaction, 'txId')
        currencyId = self.safe_string(transaction, 'asset')
        code = self.safe_currency_code(currencyId, currency)
        timestamp = None
        insertTime = self.safe_integer(transaction, 'insertTime')
        applyTime = self.safe_integer(transaction, 'applyTime')
        type = self.safe_string(transaction, 'type')
        if type is None:
            if (insertTime is not None) and (applyTime is None):
                type = 'deposit'
                timestamp = insertTime
            elif (insertTime is None) and (applyTime is not None):
                type = 'withdrawal'
                timestamp = applyTime
        status = self.parse_transaction_status_by_type(self.safe_string(transaction, 'status'), type)
        amount = self.safe_float(transaction, 'amount')
        return {
            'info': transaction,
            'id': id,
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': address,
            'tag': tag,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': None,
            'fee': None,
        }

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'asset': currency['id'],
        }
        response = self.wapiGetDepositAddress(self.extend(request, params))
        success = self.safe_value(response, 'success')
        if (success is None) or not success:
            raise InvalidAddress(self.id + ' fetchDepositAddress returned an empty response – create the deposit address in the user settings first.')
        address = self.safe_string(response, 'address')
        tag = self.safe_string(response, 'addressTag')
        self.check_address(address)
        return {
            'currency': code,
            'address': self.check_address(address),
            'tag': tag,
            'info': response,
        }

    def fetch_funding_fees(self, codes=None, params={}):
        response = self.wapiGetAssetDetail(params)
        detail = self.safe_value(response, 'assetDetail', {})
        ids = list(detail.keys())
        withdrawFees = {}
        for i in range(0, len(ids)):
            id = ids[i]
            code = self.safe_currency_code(id)
            withdrawFees[code] = self.safe_float(detail[id], 'withdrawFee')
        return {
            'withdraw': withdrawFees,
            'deposit': {},
            'info': response,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        name = address[0:20]
        request = {
            'asset': currency['id'],
            'address': address,
            'amount': float(amount),
            'name': name,
        }
        if tag is not None:
            request['addressTag'] = tag
        response = self.wapiPostWithdraw(self.extend(request, params))
        return {
            'info': response,
            'id': self.safe_string(response, 'id'),
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        url += '/' + path
        if api == 'wapi':
            url += '.html'
        userDataStream = (path == 'userDataStream')
        if path == 'historicalTrades':
            headers = {
                'X-BCIO-APIKEY': self.apiKey,
            }
        elif userDataStream:
            body = self.urlencode(params)
            headers = {
                'X-BCIO-APIKEY': self.apiKey,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        if (api == 'private') or (api == 'sapi') or (api == 'wapi' and path != 'systemStatus'):
            self.check_required_credentials()
            query = self.urlencode(self.extend({
                'timestamp': self.nonce(),
                'recvWindow': self.options['recvWindow'],
            }, params))
            signature = self.hmac(self.encode(query), self.encode(self.secret))
            query += '&' + 'signature=' + signature
            headers = {
                'X-BCIO-APIKEY': self.apiKey,
            }
            if (method == 'GET') or (method == 'DELETE') or (api == 'wapi'):
                url += '?' + query
            else:
                body = query
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
        else:
            if not userDataStream:
                if params:
                    url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if (code == 418) or (code == 429):
            raise DDoSProtection(self.id + ' ' + str(code) + ' ' + reason + ' ' + body)
        if code >= 400:
            if body.find('Price * QTY is zero or less') >= 0:
                raise InvalidOrder(self.id + ' order cost = amount * price is zero or less ' + body)
            if body.find('LOT_SIZE') >= 0:
                raise InvalidOrder(self.id + ' order amount should be evenly divisible by lot size ' + body)
            if body.find('PRICE_FILTER') >= 0:
                raise InvalidOrder(self.id + ' order price is invalid, i.e. exceeds allowed price precision, exceeds min price or max price limits or is invalid float value in general, use self.price_to_precision(symbol, amount) ' + body)
        if len(body) > 0:
            if body[0] == '{':
                success = self.safe_value(response, 'success', True)
                if not success:
                    message = self.safe_string(response, 'msg')
                    parsedMessage = None
                    if message is not None:
                        try:
                            parsedMessage = json.loads(message)
                        except Exception as e:
                            parsedMessage = None
                        if parsedMessage is not None:
                            response = parsedMessage
                exceptions = self.exceptions
                message = self.safe_string(response, 'msg')
                if message in exceptions:
                    ExceptionClass = exceptions[message]
                    raise ExceptionClass(self.id + ' ' + message)
                error = self.safe_string(response, 'code')
                if error is not None:
                    if error in exceptions:
                        if (error == '-2015') and self.options['hasAlreadyAuthenticatedSuccessfully']:
                            raise DDoSProtection(self.id + ' temporary banned: ' + body)
                        raise exceptions[error](self.id + ' ' + body)
                    else:
                        raise ExchangeError(self.id + ' ' + body)
                if not success:
                    raise ExchangeError(self.id + ' ' + body)

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if (api == 'private') or (api == 'wapi'):
            self.options['hasAlreadyAuthenticatedSuccessfully'] = True
        return response
