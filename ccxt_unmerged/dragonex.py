# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import OrderNotFound
from ccxt.base.decimal_to_precision import ROUND


class dragonex(Exchange):

    def describe(self):
        return self.deep_extend(super(dragonex, self).describe(), {
            'id': 'dragonex',
            'name': 'DragonEx',
            'countries': ['CN'],
            'rateLimit': 500,  # up to 3000 requests per 5 minutes ≈ 600 requests per minute ≈ 10 requests per second ≈ 100 ms
            'has': {
                'fetchDepositAddress': True,
                'fetchTicker': True,
                'fetchTickers': False,
                'fetchOHLCV': True,
                'fetchMyTrades': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'withdraw': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'fetchTransactions': False,
            },
            'timeframes': {
                '1m': 1,
                '5m': 2,
                '15m': 3,
                '30m': 4,
                '1h': 5,
                '1d': 6,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/44139321/69334949-b9335c00-0c96-11ea-8e4d-cca246021d6f.png',
                'api': {
                    'public': 'https://openapi.dragonex.co/api/v1',
                    'private': 'https://openapi.dragonex.co',
                    'v1': 'https://openapi.dragonex.co/api/v1',
                    'aicoin': 'https://openapi.dragonex.co/api/aicoin',
                    'pal': 'https://openapi.dragonex.co/api/aicoin',
                },
                'www': 'https://dragonex.co',
                'referral': 'https://dragonex.co/account/register?inviteId=1248302',
                'doc': 'https://github.com/Dragonexio/OpenApi/blob/master/docs/English/1.interface_document_v1.md',
                'fees': 'https://dragonex.zendesk.com/hc/en-us/articles/115002431171-Fee',
            },
            'api': {
                'v1': {
                    'get': [
                        'market/kline/',  # 获取K线数据
                        'market/buy/',  # 获取买盘
                        'market/sell/',  # 获取卖盘
                        'market/real/',  # 获取实时行情
                        'market/depth/',  # 获取market depth数据
                    ],
                },
                'aicoin': {
                    'get': [
                        'market/real/',
                        'market/all_trade/',
                        'market/buy_sell/',
                    ],
                },
                'public': {
                    'get': [
                        'symbol/all/',  # 查询系统支持的所有交易对
                        'symbol/all2/',
                        'symbol/all3/',
                        'coin/all/',  # 查询系统支持的所有币种
                    ],
                },
                'private': {
                    'get': [
                        'user/own/',
                    ],
                    'post': [
                        'api/v1/token/new/',
                        'api/v1/token/status/',
                        'api/v1/user/own/',
                        'api/v1/user/fee/',
                        'api/v1/order/buy/',
                        'api/v1/order/sell/',
                        'api/v1/order/cancel/',
                        'api/v1/order/add/',
                        'api/v1/order/detail/',
                        'api/v1/order/detail2/',
                        'api/v1/order/history/',
                        'api/v1/order/history2/',
                        'api/v1/deal/history/',
                        'api/v1/user/detail/',
                        'api/pal/coin/withdraw/',
                        'api/v1/coin/withdraw/new/',
                        'api/v1/coin/prepay/history/',
                        'api/v1/coin/prepay/addr/',
                        'api/v1/coin/withdraw/history/',
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
            'exceptions': {
                # English
                # see https://github.com/Dragonexio/OpenApi/blob/master/docs/English/2.%20error_codes.md
                # Chinese
                # https://github.com/Dragonexio/OpenApi/blob/master/docs/%E4%B8%AD%E6%96%87/2.%20error_codes.md
                '1': 'ok',
                '2': 'Time Out',
                '3': 'Network Error',
                '4': 'Database Error',
                '5': 'Cache Error',
                '6': 'Server Error',
                '7': 'No Content',
                '8': 'Parameter Error',
                '5001': 'PriceLessThanLimit',
                '5002': 'VolumeLessThanLimit',
                '5003': 'MakeOrderIDFailed',
                '5004': 'DuplicateOrder',
                '5005': 'SellLessThanBuy',
                '5006': 'BuyGreaterThanSell',
                '5007': 'NotFindOrder',
                '5008': 'OrderCanceled',
                '5009': 'WriteTradeFailed',
                '5010': 'WrongPrice',
                '5011': 'WrongAmount',
                '5012': 'WrongUserID',
                '5013': 'OrderDone',
                '5014': 'OrderFailed',
                '5015': 'OrderNonTradable',
                '5016': 'AmountLessThanLimit',
                '5017': 'NewOrderDisabled',
                '5018': 'CancelOrderDisabled',
                '5019': 'TriggerPriceEqualClosePrice',
                '5020': 'OrderCountGreaterThanLimit',
                '9001': 'Key Already Exists',
                '9002': 'Key Not Exists',
                '9003': 'Invalid key',
                '9004': 'Signature Error',
                '9005': 'Invalid Token',
                '9006': 'Token Expires',
                '9007': 'Invalid User Credential',
                '9008': 'Frequent Operations',
                '9009': 'IP Disabled',
                '9010': 'Key Creation Fails',
                '9011': 'Unauthorized',
                '9014': 'Frequent Operations',
                '9015': 'Not in Binded IP',
                '9016': 'Exceed Maximum Times of Request Allowed in A Single Day',
                '9017': 'Fail to Obtain New Token',
                '9018': 'Key Expires',
                '9019': 'Date Field not Found in Headers',
                '9020': 'Improper Date Field Found in Headers',
                '9021': 'Incoming Time not within 15 Minutes',
                '9022': 'Token Kicked Off',
            },
            'options': {
                'change_quote': {
                    'USDT': 'USD',
                },
                'order_type': {
                    '0': '_',
                    '1': 'Buy',
                    '2': 'Sell',
                },
            },
        })

    def fetch_markets(self, params={}):
        result = []
        spotResponse = self.publicGetSymbolAll2()
        spotMarkets = self.safe_value(spotResponse, 'data', {})
        markets = self.safe_value(spotMarkets, 'list', [])
        for i in range(0, len(markets)):
            market = markets[i]
            id = market[1]
            parts = id.split('_')
            baseId = parts[0]
            quoteId = parts[1]
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            precision = {
                'amount': market[7],
                'price': market[5],
            }
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'symbol_id': market[0],
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': market[4],
                        'max': None,
                    },
                    'price': {
                        'min': market[2],
                        'max': None,
                    },
                    'cost': {
                        'min': float(market[4]) * float(market[2]),
                        'max': None,
                    },
                },
            })
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
        response = self.privatePostUserOwn(params)
        result = {'info': response}
        balances = self.safe_value(response, 'data', [])
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = balance['coin_id']
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['used'] = self.safe_float(balance, 'frozen')
            account['total'] = self.safe_float(balance, 'volume')
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol_id': market['symbol_id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = maximum = 100
        response = self.v1GetMarketDepth(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_order_book(data, symbol, None, 'buys', 'sells', 'price', 'volume')

    def parse_ticker(self, ticker, market=None):
        ticker = self.safe_value(self.safe_value(ticker, 'data', {}), 'list', [])[0]
        lastFourNum = 11
        timestamp = ticker[14]
        last = ticker[3]
        result = {
            'symbol': market['symbol'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': ticker[4],
            'low': ticker[5],
            'bid': ticker[6],
            'bidVolume': None,
            'ask': ticker[7],
            'askVolume': None,
            'vwap': None,
            'open': ticker[2],
            'close': last,
            'last': last,
            'previousClose': None,
            'change': ticker[8],
            'percentage': ticker[9],
            'average': None,
            'baseVolume': ticker[lastFourNum],
            'quoteVolume': None,
            'info': ticker,
        }
        keys = ['high', 'low', 'bid', 'ask', 'open', 'close', 'last', 'change', 'percentage', 'baseVolume']
        for i in range(0, len(keys)):
            key = keys[i]
            if result[key] is not None:
                result[key] = float(result[key])
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol_ids': market['symbol_id'],
        }
        response = self.aicoinGetMarketReal(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv[6],
            float(ohlcv[4]),
            float(ohlcv[2]),
            float(ohlcv[3]),
            float(ohlcv[1]),
            float(ohlcv[0]),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol_id': market['symbol_id'],
            'kline_type': self.timeframes[timeframe],
        }
        if since is not None:
            request['st'] = since
        if limit is not None:
            request['count'] = limit
        response = self.v1GetMarketKline(self.extend(request, params))
        lists = self.safe_value(self.safe_value(response, 'data'), 'lists', [])
        return self.parse_ohlcvs(lists, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_float(trade, 'timestamp')
        price = self.safe_float(trade, 'deal_price')
        amount = self.safe_float(trade, 'deal_volume')
        id = self.safe_string(trade, 'id')
        side = None
        cost = None
        order = None
        type = self.safe_string(trade, 'order_type')
        if type is not None:
            type = self.options['order_type'][type]
        if price is not None:
            if amount is not None:
                cost = amount * price
        feeCost = self.safe_float(trade, 'charge')
        fee = None
        feeCurrency = None
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
            }
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'info': trade,
            'order': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol_id': market['symbol_id'],
        }
        if limit is not None:
            request['count'] = limit
        response = self.aicoinGetMarketAllTrade(self.extend(request, params))
        data = self.safe_value(self.safe_value(response, 'data', {}), 'list', [])
        result = []
        for i in range(0, len(data)):
            dataDict = {
                'id': data[i][0],
                'order_type': data[i][1],
                'deal_type': data[i][2],
                'deal_price': data[i][3],
                'deal_volume': data[i][4],
                'charge': data[i][5],
                'price_base': data[i][6],
                'usdt_amount': data[i][7],
                'timestamp': data[i][8] / 1E6,
            }
            # trade = self.parse_trade(dataDict, market)
            # result.append(trade)
            result.append(dataDict)
        # result = self.sort_by(result, 'timestamp')
        # return self.filter_by_symbol_since_limit(result, market, since, limit)
        return self.parse_trades(result, market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            '0': 'Any',
            '1': 'Waiting',  # 等待成交
            '2': 'Done',  # 完成， 完全提交
            '3': 'Canceled',  # 取消+没有成交量
            '4': 'Failed',  # 失败
            '5': 'Cancelling',  # 正在取消订单
            '6': 'Partially_Filled',  # 部分成交+等待成交
            '7': 'Partially_Canceled',  # 部分成交+已撤销
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        status = self.parse_order_status(self.safe_string(order, 'status'))
        symbol = market['symbol']
        timestamp = self.safe_value(order, 'timestamp') / 1000000
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'volume')
        filled = self.safe_float(order, 'trade_volume')
        remaining = None
        average = None
        cost = self.safe_float(order, 'cummulativeQuoteQty', 0)
        if filled is not None:
            if amount is not None:
                remaining = amount - filled
                remaining = max(remaining, 0.0)
            if price is not None:
                if cost is None:
                    cost = price * filled
        id = self.safe_string(order, 'order_id')
        side = self.safe_string_lower(order, 'order_type', '0')
        side = self.options['order_type'][side]
        feeCost = self.safe_float(order, 'actual_fee', 0)
        fee = None
        if feeCost is not None:
            feeCurrency = None
            if market is not None:
                feeCurrency = market['quote'] if (side == 'sell') else market['base']
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
            }
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': 'market',
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol_id': market['symbol_id'],
            'volume': self.amount_to_precision(symbol, amount),
        }
        if type == 'limit':
            request['price'] = self.price_to_precision(symbol, price)
        response = None
        if side == 'buy':
            response = self.privatePostApiV1OrderBuy(self.extend(request, params))
        if side == 'sell':
            response = self.privatePostApiV1OrderSell(self.extend(request, params))
        timestamp = self.milliseconds()
        data = self.safe_value(response, 'data', {})
        return {
            'info': response,
            'id': data['order_id'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'cost': None,
            'trades': None,
            'fee': None,
        }

    def fetch_currencies(self, params={}):
        coinRes = self.publicGetCoinAll()
        response = self.safe_value(coinRes, 'data', [])
        result = {}
        for i in range(0, len(response)):
            currency = response[i]
            id = self.safe_integer(currency, 'coin_id', 0)
            code = self.safe_string(currency, 'code', '')
            result[code] = {
                'id': id,
            }
            result[id] = {
                'code': code,
            }
        return result

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol_id': market['symbol_id'],
            'order_id': id,
        }
        response = self.privatePostApiV1OrderDetail(self.extend(request, params))
        response_dict = self.safe_value(response, 'data', {})
        return self.parse_order(response_dict, market)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol_id': market['symbol_id'],
            'statuses': params['status'],
        }
        if since is not None:
            request['start'] = since
        if limit is not None:
            request['count'] = limit
        response = self.privatePostApiV1OrderHistory2(self.extend(request, params))
        data = self.safe_value(self.safe_value(response, 'data', {}), 'list', [])
        return self.parse_orders(data, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'statuses': '2',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'statuses': '3',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol_id': market['symbol_id'],
            'order_id': id,
        }
        response = self.privatePostApiV1OrderCancel(self.extend(request, params))
        response = self.safe_value(response, 'data')
        if response is None:
            raise OrderNotFound(self.id + ' cancelOrder() error ' + self.last_http_response)
        return self.parse_order(response, market)

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
        response = self.privatePostApiV1OrderDetail2(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        currency = None
        request = {}
        coinId = None
        if code is not None:
            coinId = self.currencies[code]['id']
            request['coin_id'] = coinId
        response = self.privatePostApiV1CoinPrepayHistory(self.extend(request, params))
        return self.parse_transactions(response['data']['list'], currency, since, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        currency = None
        request = {}
        coinId = None
        if code is not None:
            coinId = self.currencies[code]['id']
            request['coin_id'] = coinId
        if since is not None:
            request['startTime'] = since
        response = self.privatePostApiV1CoinWithdrawHistory(self.extend(request, params))
        return self.parse_transactions(response['data']['list'], currency, since, limit)

    def parse_transaction_status_by_type(self, status, type=None):
        if type is None:
            return status
        statuses = {
            'deposit': {
                '1': 'pending',
                '2': 'entering',
                '3': 'ok',
                '4': 'failed',
            },
            'withdrawal': {
                '1': 'pending',
                '2': 'entering',
                '3': 'ok',
                '4': 'failed',
                '5': 'not approved',
            },
        }
        return statuses[type][status] if (status in list(statuses[type].keys())) else status

    def parse_transaction(self, transaction, currency=None):
        prepayId = self.safe_string(transaction, 'prepay_id')
        withdrawId = self.safe_string(transaction, 'withdraw_id')
        id = prepayId is not prepayId if None else withdrawId
        address = self.safe_string(transaction, 'addr')
        tag = self.safe_string(transaction, 'tag')
        if tag is not None:
            if len(tag) < 1:
                tag = None
        txid = self.safe_value(transaction, 'tx_id')
        currencyId = self.safe_string(transaction, 'coin_id')
        code = self.currencies[currencyId]['code']
        timestamp = None
        insertTime = None
        applyTime = None
        if prepayId is not None:
            insertTime = self.safe_integer(transaction, 'arrive_time')
        if withdrawId is not None:
            applyTime = self.safe_integer(transaction, 'arrive_time')
        type = self.safe_string(transaction, 'type')
        if type is None:
            if (insertTime is not None) and (applyTime is None):
                type = 'deposit'
                timestamp = insertTime
            elif (insertTime is None) and (applyTime is not None):
                type = 'withdrawal'
                timestamp = applyTime
        status = self.parse_transaction_status_by_type(self.safe_string(transaction, 'status'), type)
        amount = self.safe_float(transaction, 'volume')
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
        request = {}
        if code is not None:
            coinId = self.currencies[code]['id']
            request = {
                'coin_id': coinId,
            }
        response = self.privatePostApiV1CoinPrepayAddr(self.extend(request, params))
        success = self.safe_value(response, 'ok')
        if (success is None) or not success:
            raise InvalidAddress(self.id + ' fetchDepositAddress returned an empty response – create the deposit address in the user settings first.')
        address = self.safe_string(self.safe_value(response, 'data', {}), 'addr')
        tag = self.safe_string(self.safe_value(response, 'data', {}), 'tag')
        self.check_address(address)
        return {
            'currency': code,
            'address': self.check_address(address),
            'tag': tag,
            'info': response,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        coinId = self.currencies[code]['id']
        request = {
            'coin_id': coinId,
            'addr': address,
            'volume': float(amount),
        }
        if tag is not None:
            request['addressTag'] = tag
        response = self.privatePostApiV1CoinWithdrawNew(self.extend(request, params))
        return {
            'info': response,
            'id': self.safe_string(response, 'withdraw_id'),
        }

    def sign_in(self, params={}):
        ip = self.safe_value(params, 'bind_ip', '0.0.0.0')
        date = self.Date()
        date = self.gmt(date)
        contentMd5 = ''
        contentType = 'application/json'
        canonicalizedHeaders = ''
        strToTokenSign = '\n'.join(['POST', contentMd5, contentType, date, canonicalizedHeaders]) + '/api/v1/token/new/'
        signature = self.hmac(self.encode(self.secret), self.encode(strToTokenSign), hashlib.sha1, 'base64')
        authToken = self.apiKey + ':' + signature
        tokenHeader = {
            'Content-Sha1': contentMd5,
            'Date': date,
            'Content-Type': contentType,
            'X-Real-IP-Proxy': ip,
            'Auth': authToken,
        }
        res = self.fetch('https://openapi.dragonex.co/api/v1/token/new/', 'POST', tokenHeader)
        token = self.safe_string(self.safe_value(res, 'data', {}), 'token', '')
        self.options['accessToken'] = token
        self.options['date'] = date
        self.options['ip'] = ip
        return {}

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if method == 'GET':
            if query is not None:
                request += '?' + self.urlencode(query)
        url = self.urls['api'][api] + request
        if api == 'private':
            body = self.json({})
            self.check_required_credentials()
            if method != 'GET':
                if query is not None:
                    body = self.json(query)
            contentMd5 = ''
            contentType = 'application/json'
            canonicalizedHeaders = ''
            date = self.options['date']
            token = self.options['accessToken']
            ip = self.options['ip']
            strToSign = '\n'.join([method.upper(), contentMd5, contentType, date, canonicalizedHeaders])
            strToSign += request
            signature = self.hmac(self.encode(self.secret), self.encode(strToSign), hashlib.sha1, 'base64')
            auth = self.apiKey + ':' + signature
            headers = {
                'Content-Sha1': contentMd5,
                'Date': date,
                'Content-Type': contentType,
                'X-Real-IP-Proxy': ip,
                'Auth': auth,
                'token': token,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if 'code' in response:
            if response['code'] != 1:
                error = self.safe_string(response, 'code')
                message = self.id + ' ' + self.json(response)
                if error in self.exceptions:
                    msg = self.exceptions[error]
                    return msg
                else:
                    return message
            else:
                return self.id + ' ' + self.json(response)
