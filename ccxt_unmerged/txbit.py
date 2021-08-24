# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.bittrex import bittrex
import math
from ccxt.base.errors import ExchangeError


class txbit (bittrex):

    def describe(self):
        timeframes = {
            '5m': '5m',
            '15m': '15m',
            '30m': '30m',
            '1h': '1h',
            '6h': '6h',
            '1d': '1d',
            '1w': '1w',
            '2w': '2w',
        }
        result = self.deep_extend(super(txbit, self).describe(), {
            'id': 'txbit',
            'name': 'Txbit.io',
            'countries': ['NL'],  # Netherlands
            'rateLimit': 1000,
            'certified': False,
            'version': '',
            'timeframes': timeframes,
            'has': {
                'CORS': True,
                'createMarketOrder': False,
                'fetchDepositAddress': True,
                'fetchClosedOrders': True,
                'fetchCurrencies': True,
                'fetchMyTrades': 'emulated',
                'fetchOHLCV': False,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchTickers': True,
                'withdraw': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'fetchTransactions': False,
            },
            'hostname': 'api.txbit.io',
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/2078175/66576388-ee1ca100-eb77-11e9-89e8-75808e4389eb.jpg',
                'api': {
                    'public': 'https://{hostname}/api',
                    'account': 'https://{hostname}/api',
                    'market': 'https://{hostname}/api',
                },
                'www': 'https://txbit.io',
                'doc': [
                    'https://apidocs.txbit.io',
                ],
                'fees': 'https://txbit.io/Fee',
            },
            'api': {
                'account': {
                    'get': [
                        'balance',
                        'balances',
                        'depositaddress',
                        'deposithistory',
                        'order',
                        'orderhistory',
                        'withdrawhistory',
                        'withdraw',
                    ],
                },
                'public': {
                    'get': [
                        'currencies',
                        'markethistory',
                        'markets',
                        'marketsummaries',
                        'marketsummary',
                        'orderbook',
                        'ticker',
                        'systemstatus',
                        'currencyinformation',
                        'currencybalancesheet',
                    ],
                },
                'market': {
                    'get': [
                        'buylimit',
                        'selllimit',
                        'cancel',
                        'openorders',
                    ],
                },
            },
            'fees': {
                'funding': {
                    'withdraw': {
                        'BTC': 0.001,
                    },
                },
            },
            'options': {
                # price precision by quote currency code
                'pricePrecisionByCode': {
                    'USD': 3,
                    'BTC': 8,
                },
                'parseOrderStatus': True,
                'disableNonce': False,
                'symbolSeparator': '/',
            },
            # 'verbose': True,
        })
        return result

    def fetch_markets(self, params={}):
        # https://github.com/ccxt/ccxt/issues/5668
        response = self.publicGetMarkets(params)
        result = []
        markets = self.safe_value(response, 'result')
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'MarketName')
            baseId = self.safe_string(market, 'MarketCurrency')
            quoteId = self.safe_string(market, 'BaseCurrency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            pricePrecision = 8
            if quote in self.options['pricePrecisionByCode']:
                pricePrecision = self.options['pricePrecisionByCode'][quote]
            precision = {
                'amount': 8,
                'price': pricePrecision,
            }
            # bittrex uses boolean values, bleutrade uses strings
            active = self.safe_value(market, 'IsActive', False)
            if (active != 'false') and active:
                active = True
            else:
                active = False
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'info': market,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': self.safe_float(market, 'MinTradeSize'),
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                },
            })
        return result

    def parse_order_status(self, status):
        statuses = {
            'OK': 'closed',
            'OPEN': 'open',
            'CANCELED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        # Possible params
        # orderstatus(ALL, OK, OPEN, CANCELED)
        # ordertype(ALL, BUY, SELL)
        # depth(optional, default is 500, max is 20000)
        self.load_markets()
        market = None
        marketId = 'ALL'
        if symbol is not None:
            market = self.market(symbol)
            marketId = market['id']
        request = {
            'market': marketId,
            'orderstatus': 'ALL',
        }
        response = self.accountGetOrders(self.extend(request, params))
        return self.parse_orders(response['result'], market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        response = self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(response, 'status', 'closed')

    def get_order_id_field(self):
        return 'orderid'

    def parse_symbol(self, id):
        base, quote = id.split(self.options['symbolSeparator'])
        base = self.safe_currency_code(base)
        quote = self.safe_currency_code(quote)
        return base + '/' + quote

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'market': self.market_id(symbol),
            'type': 'both',
        }
        if limit is not None:
            request['depth'] = limit  # 50
        response = self.publicGetOrderbook(self.extend(request, params))
        orderbook = self.safe_value(response, 'result')
        if not orderbook:
            raise ExchangeError(self.id + ' publicGetOrderbook() returneded no result ' + self.json(response))
        return self.parse_order_book(orderbook, symbol, None, 'buy', 'sell', 'Rate', 'Quantity')

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        # Currently we can't set the makerOrTaker field, but if the user knows the order side then it can be
        # determined(if the side of the trade is different to the side of the order, then the trade is maker).
        # Similarly, the correct 'side' for the trade is that of the order.
        # The trade fee can be set by the user, it is always 0.25% and is taken in the quote currency.
        self.load_markets()
        request = {
            'orderid': id,
        }
        response = self.accountGetOrderhistory(self.extend(request, params))
        return self.parse_trades(response['result'], None, since, limit, {
            'order': id,
        })

    def fetch_transactions_by_type(self, type, code=None, since=None, limit=None, params={}):
        self.load_markets()
        method = 'accountGetDeposithistory' if (type == 'deposit') else 'accountGetWithdrawhistory'
        response = getattr(self, method)(params)
        result = self.parse_transactions(response['result'])
        return self.filterByCurrencySinceLimit(result, code, since, limit)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        return self.fetch_transactions_by_type('deposit', code, since, limit, params)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        return self.fetch_transactions_by_type('withdrawal', code, since, limit, params)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['TimeStamp'] + '+00:00')
        side = None
        if trade['OrderType'] == 'BUY':
            side = 'buy'
        elif trade['OrderType'] == 'SELL':
            side = 'sell'
        id = self.safe_string_2(trade, 'Id', 'ID')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        cost = None
        price = self.safe_float(trade, 'Price')
        amount = self.safe_float(trade, 'Quantity')
        if amount is not None:
            if price is not None:
                cost = price * amount
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'order': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = self.publicGetMarkethistory(self.extend(request, params))
        if 'result' in response:
            if response['result'] is not None:
                return self.parse_trades(response['result'], market, since, limit)
        raise ExchangeError(self.id + ' fetchTrades() returned None response')

    def parse_order(self, order, market=None):
        #
        # fetchOrders
        #
        #     {
        #         OrderId: '107220258',
        #         Exchange: 'LTC_BTC',
        #         Type: 'SELL',
        #         Quantity: '2.13040000',
        #         QuantityRemaining: '0.00000000',
        #         Price: '0.01332672',
        #         Status: 'OK',
        #         Created: '2018-06-30 04:55:50',
        #         QuantityBaseTraded: '0.02839125',
        #         Comments: ''
        #     }
        #
        side = self.safe_string_2(order, 'OrderType', 'Type')
        isBuyOrder = (side == 'LIMIT_BUY') or (side == 'BUY')
        isSellOrder = (side == 'LIMIT_SELL') or (side == 'SELL')
        if isBuyOrder:
            side = 'buy'
        if isSellOrder:
            side = 'sell'
        # We parse different fields in a very specific order.
        # Order might well be closed and then canceled.
        status = None
        if ('Opened' in list(order.keys())) and order['Opened']:
            status = 'open'
        if ('Closed' in list(order.keys())) and order['Closed']:
            status = 'closed'
        if ('CancelInitiated' in list(order.keys())) and order['CancelInitiated']:
            status = 'canceled'
        if ('Status' in list(order.keys())) and self.options['parseOrderStatus']:
            status = self.parse_order_status(self.safe_string(order, 'Status'))
        symbol = None
        marketId = self.safe_string(order, 'Exchange')
        if marketId is None:
            if market is not None:
                symbol = market['symbol']
        else:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            else:
                symbol = self.parse_symbol(marketId)
        timestamp = None
        if 'Opened' in order:
            timestamp = self.parse8601(order['Opened'] + '+00:00')
        if 'Created' in order:
            timestamp = self.parse8601(order['Created'] + '+00:00')
        lastTradeTimestamp = None
        if ('TimeStamp' in list(order.keys())) and (order['TimeStamp'] is not None):
            lastTradeTimestamp = self.parse8601(order['TimeStamp'] + '+00:00')
        if ('Closed' in list(order.keys())) and (order['Closed'] is not None):
            lastTradeTimestamp = self.parse8601(order['Closed'] + '+00:00')
        if timestamp is None:
            timestamp = lastTradeTimestamp
        fee = None
        commission = None
        if 'Commission' in order:
            commission = 'Commission'
        elif 'CommissionPaid' in order:
            commission = 'CommissionPaid'
        if commission:
            fee = {
                'cost': self.safe_float(order, commission),
            }
            if market is not None:
                fee['currency'] = market['quote']
            elif symbol is not None:
                currencyIds = symbol.split('/')
                quoteCurrencyId = currencyIds[1]
                fee['currency'] = self.safe_currency_code(quoteCurrencyId)
        price = self.safe_float(order, 'Price')
        cost = None
        amount = self.safe_float(order, 'Quantity')
        remaining = self.safe_float(order, 'QuantityRemaining')
        filled = None
        if amount is not None and remaining is not None:
            filled = amount - remaining
        if not cost:
            if price and filled:
                cost = price * filled
        if not price:
            if cost and filled:
                price = cost / filled
        average = self.safe_float(order, 'PricePerUnit')
        id = self.safe_string_2(order, 'OrderUuid', 'OrderId')
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': 'limit',
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

    def parse_transaction(self, transaction, currency=None):
        #
        #  deposit:
        #
        #     {
        #         Id: '96974373',
        #         Coin: 'DOGE',
        #         Amount: '12.05752192',
        #         TimeStamp: '2017-09-29 08:10:09',
        #         Label: 'DQqSjjhzCm3ozT4vAevMUHgv4vsi9LBkoE',
        #     }
        #
        # withdrawal:
        #
        #     {
        #         Id: '98009125',
        #         Coin: 'DOGE',
        #         Amount: '-483858.64312050',
        #         TimeStamp: '2017-11-22 22:29:05',
        #         Label: '483848.64312050;DJVJZ58tJC8UeUv9Tqcdtn6uhWobouxFLT;10.00000000',
        #         TransactionId: '8563105276cf798385fee7e5a563c620fea639ab132b089ea880d4d1f4309432',
        #     }
        #
        #     {
        #         "Id": "95820181",
        #         "Coin": "BTC",
        #         "Amount": "-0.71300000",
        #         "TimeStamp": "2017-07-19 17:14:24",
        #         "Label": "0.71200000;PER9VM2txt4BTdfyWgvv3GziECRdVEPN63;0.00100000",
        #         "TransactionId": "CANCELED"
        #     }
        #
        id = self.safe_string(transaction, 'Id')
        amount = self.safe_float(transaction, 'Amount')
        type = 'deposit'
        if amount < 0:
            amount = abs(amount)
            type = 'withdrawal'
        currencyId = self.safe_string(transaction, 'Coin')
        code = self.safe_currency_code(currencyId, currency)
        label = self.safe_string(transaction, 'Label')
        timestamp = self.parse8601(self.safe_string(transaction, 'TimeStamp'))
        txid = self.safe_string(transaction, 'TransactionId')
        address = None
        feeCost = None
        labelParts = label.split(';')
        if len(labelParts) == 3:
            amount = float(labelParts[0])
            address = labelParts[1]
            feeCost = float(labelParts[2])
        else:
            address = label
        fee = None
        if feeCost is not None:
            fee = {
                'currency': code,
                'cost': feeCost,
            }
        status = 'ok'
        if txid == 'CANCELED':
            txid = None
            status = 'canceled'
        return {
            'info': transaction,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'id': id,
            'currency': code,
            'amount': amount,
            'address': address,
            'tag': None,
            'status': status,
            'type': type,
            'updated': None,
            'txid': txid,
            'fee': fee,
        }

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "MarketName":"BTC-ETH",
        #         "High":0.02127099,
        #         "Low":0.02035064,
        #         "Volume":10288.40271571,
        #         "Last":0.02070510,
        #         "BaseVolume":214.64663206,
        #         "TimeStamp":"2019-09-18T21:03:59.897",
        #         "Bid":0.02070509,
        #         "Ask":0.02070510,
        #         "OpenBuyOrders":1228,
        #         "OpenSellOrders":5899,
        #         "PrevDay":0.02082823,
        #         "Created":"2015-08-14T09:02:24.817"
        #     }
        #
        timestamp = self.parse8601(self.safe_string(ticker, 'TimeStamp'))
        symbol = None
        marketId = self.safe_string(ticker, 'MarketName')
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                symbol = self.parse_symbol(marketId)
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        previous = self.safe_float(ticker, 'PrevDay')
        last = self.safe_float(ticker, 'Last')
        change = None
        percentage = None
        if last is not None:
            if previous is not None:
                change = last - previous
                if previous > 0:
                    percentage = (change / previous) * 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'High'),
            'low': self.safe_float(ticker, 'Low'),
            'bid': self.safe_float(ticker, 'Bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'Ask'),
            'askVolume': None,
            'vwap': None,
            'open': previous,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'Volume'),
            'quoteVolume': self.safe_float(ticker, 'BaseVolume'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = self.publicGetMarketsummary(self.extend(request, params))
        #
        #     {
        #         "success":true,
        #         "message":"",
        #         "result": {
        #                 "MarketName":"BTC-ETH",
        #                 "High":0.02127099,
        #                 "Low":0.02035064,
        #                 "Volume":10288.40271571,
        #                 "Last":0.02070510,
        #                 "BaseVolume":214.64663206,
        #                 "TimeStamp":"2019-09-18T21:03:59.897",
        #                 "Bid":0.02070509,
        #                 "Ask":0.02070510,
        #                 "OpenBuyOrders":1228,
        #                 "OpenSellOrders":5899,
        #                 "PrevDay":0.02082823,
        #                 "Created":"2015-08-14T09:02:24.817"
        #             }
        #     }
        #
        ticker = response['result']
        return self.parse_ticker(ticker, market)
