# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InvalidOrder
from ccxt.base.decimal_to_precision import TICK_SIZE


class btse(Exchange):
    def describe(self):
        return self.deep_extend(
            super(btse, self).describe(),
            {
                "id": "btse",
                "name": "BTSE",
                "countries": ["BVI"],
                "userAgent": "sdk_ccxt/btse",
                "rateLimit": 3000,
                "certified": False,
                "has": {
                    "CORS": True,
                    "cancelAllOrders": True,
                    "fetchClosedOrders": False,
                    "fetchCurrencies": False,
                    "fetchDepositAddress": True,
                    "fetchDeposits": True,
                    "fetchFundingFees": False,
                    "fetchMyTrades": True,
                    "fetchOHLCV": True,
                    "fetchOpenOrders": True,
                    "fetchOrder": True,
                    "fetchOrderBook": True,
                    "fetchOrders": False,
                    "fetchTicker": True,
                    "fetchTickers": False,
                    "fetchTrades": True,
                    "fetchTradingFees": True,
                    "fetchWithdrawals": False,
                    "withdraw": True,
                },
                "timeframes": {
                    "1m": "1",
                    "3m": "3",
                    "5m": "5",
                    "15m": "15",
                    "30m": "30",
                    "1h": "60",
                    "2h": "120",
                    "4h": "240",
                    "6h": "360",
                    "9h": "720",
                    "1d": "1440",
                    "1M": "43800",
                    "1w": "10080",
                    "1Y": "525600",
                },
                "urls": {
                    "test": "https://testnet.btse.io",
                    "logo": "",
                    "api": {
                        "web": "https://www.btse.com",
                        "api": "https://api.btse.com",
                        "spotv2": "https://api.btse.com/spot/api/v2",
                        "spotv3": "https://api.btse.com/spot/api/v3.2",
                        "spotv3private": "https://api.btse.com/spot/api/v3.2",
                        "futuresv2": "https://api.btse.com/futures/api/v2.1",
                        "futuresv2private": "https://api.btse.com/futures/api/v2.1",
                        "testnet": "https://testapi.btse.io",
                    },
                    "www": "https://www.btse.com",
                    "doc": [
                        "https://www.btse.com/apiexplorer/futures/",
                        "https://www.btse.com/apiexplorer/spot/",
                    ],
                    "fees": "https://support.btse.com/en/support/solutions/articles/43000064283-what-are-the-btse-trading-fees-",
                    "referral": "https://www.btse.com/ref?c=0Ze7BK",
                },
                "api": {
                    "spotv2": {
                        "get": [
                            "time",
                            "market_summary",
                            "ticker/{id}/",
                            "orderbook/{id}",
                            "trades",
                            "account",
                            "ohlcv",
                        ],
                    },
                    "spotv3": {
                        "get": [
                            "time",
                            "market_summary",
                            "orderbook/L2",
                            "trades",
                            "account",
                            "ohlcv",
                        ],
                    },
                    "spotv3private": {
                        "get": [
                            "user/fees",
                            "user/open_orders",
                            "user/trade_history",
                            "user/wallet",
                            "user/wallet_history",
                            "user/wallet/address",
                        ],
                        "post": [
                            "order",
                            "order/peg",
                            "order/cancelAllAfter",
                            "user/wallet/address",
                            "user/wallet/withdraw",
                        ],
                        "delete": [
                            "order",
                        ],
                    },
                    "futuresv2": {
                        "get": [
                            "time",
                            "market_summary",
                            "orderbook/L2",
                            "ohlcv",
                            "trades",
                        ],
                    },
                    "futuresv2private": {
                        "get": [
                            "user/fees",
                            "user/open_orders",
                            "user/positions",
                            "user/trade_history",
                            "user/wallet",
                            "user/wallet_history",
                        ],
                        "post": [
                            "user/wallet_transfer",
                            "order",
                            "order/peg",
                            "order/close_position",
                            "order/cancelAllAfter",
                            "leverage",
                            "risk_limit",
                        ],
                        "delete": [
                            "order",
                        ],
                    },
                },
                "fees": {
                    "trading": {
                        "tierBased": False,
                        "percentage": True,
                        "maker": 0.05 / 100,
                        "taker": 0.10 / 100,
                    },
                },
                "exceptions": {},
                "precisionMode": TICK_SIZE,
                "options": {
                    "timeDifference": 0,
                    "adjustTimeDifference": True,
                    "fetchTickerQuotes": True,
                },
            },
        )

    def nonce(self):
        return self.milliseconds() - self.options["timeDifference"]

    async def load_time_difference(self):
        type = self.safe_string_2(self.options, "fetchTime", "defaultType", "spot")
        method = "spotv3GetTime" if (type == "spot") else "futuresv2GetTime"
        response = await getattr(self, method)
        after = self.milliseconds()
        serverTime = int(response["epoch"] * 1000)
        self.options["timeDifference"] = int(after - serverTime)
        return self.options["timeDifference"]

    async def fetch_markets(self, params={}):
        defaultType = self.safe_string_2(
            self.options, "GetMarketSummary", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        query = self.omit(params, "type")
        method = (
            "spotv3GetMarketSummary"
            if (type == "spot")
            else "futuresv2GetMarketSummary"
        )
        response = await getattr(self, method)(query)
        results = []
        for i in range(0, len(response)):
            market = response[i]
            baseId = self.safe_string(market, "base")
            quoteId = self.safe_string(market, "quote")
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            marketType = "spot"
            active = self.safe_value(market, "active")
            settleTime = self.safe_integer(market, "contractEnd", 0)
            if type != "spot":
                marketType = "future" if (settleTime > 0) else "swap"
                active = (
                    not settleTime or self.seconds() < settleTime
                )  # for derivatives 'active' is always False
            lotSize = self.safe_float(market, "contractSize", 0)
            if not lotSize:
                lotSize = 1
            id = self.safe_value(market, "symbol")
            symbol = (base + "/" + quote) if (marketType != "future") else id
            results.append(
                {
                    "id": id,
                    "symbol": symbol,
                    "base": base,
                    "quote": quote,
                    "settle": None,
                    "baseId": baseId,
                    "quoteId": quoteId,
                    "settleId": None,
                    "type": marketType,
                    "spot": (marketType == "spot"),
                    "margin": False,
                    "swap": (marketType == "swap"),
                    "future": (marketType == "future"),
                    "option": False,
                    # "prediction": False,
                    "contract": False,
                    "linear": True,
                    "inverse": False,
                    "contractSize": None,
                    "expiry": None,
                    "expiryDatetime": None,
                    "strike": None,
                    "optionType": None,
                    "active": active,
                    "lotSize": lotSize,
                    "precision": {
                        "price": self.safe_float(market, "minPriceIncrement"),
                        "amount": self.safe_float(market, "minSizeIncrement"),
                        "cost": None,
                    },
                    "limits": {
                        "amount": {
                            "min": self.safe_float(market, "minOrderSize"),
                            "max": self.safe_float(market, "maxOrderSize"),
                        },
                        "price": {
                            "min": self.safe_float(market, "minValidPrice"),
                            "max": None,
                        },
                        "cost": {
                            "min": None,
                            "max": None,
                        },
                    },
                    "info": market,
                }
            )
        return results

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        defaultType = self.safe_string_2(
            self.options, "GetMarketSummary", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3GetMarketSummary"
            if (type == "spot")
            else "futuresv2GetMarketSummary"
        )
        request = {
            "symbol": market["id"],
        }
        response = await getattr(self, method)(self.extend(request, params))
        return self.parse_ticker(response[0])

    def parse_ticker(self, ticker):
        timestamp = self.safe_timestamp(ticker, "time", self.milliseconds())
        return {
            "symbol": self.safe_string(ticker, "symbol"),
            "timestamp": timestamp,
            "datetime": self.iso8601(timestamp),
            "high": self.safe_float(ticker, "high24Hr"),
            "low": self.safe_float(ticker, "low24Hr"),
            "bid": self.safe_float(ticker, "highestBid"),
            "bidVolume": None,
            "ask": self.safe_float(ticker, "lowestAsk"),
            "askVolume": None,
            "vwap": None,
            "open": None,
            "close": self.safe_float(ticker, "last"),
            "last": self.safe_float(ticker, "last"),
            "previousClose": None,
            "change": None,
            "percentage": self.safe_float(ticker, "percentageChange"),
            "average": None,
            "baseVolume": None,
            "quoteVolume": self.safe_float(ticker, "volume"),
            "info": ticker,
        }

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            "symbol": market["id"],
        }
        if limit is not None:
            request["depth"] = limit
        defaultType = self.safe_string_2(
            self.options, "GetOrderBookL2", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3GetOrderbookL2" if (type == "spot") else "futuresv2GetOrderbookL2"
        )
        response = await getattr(self, method)(self.extend(request, params))
        timestamp = response["timestamp"]
        orderbook = self.parse_order_book(
            response, symbol, timestamp, "buyQuote", "sellQuote", "price", "size"
        )
        orderbook["nonce"] = self.safe_integer(response, "timestamp")
        return orderbook

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            "symbol": market["id"],
        }
        if limit is not None:
            request["count"] = limit
        defaultType = self.safe_string_2(
            self.options, "GetTrades", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = "spotv3GetTrades" if (type == "spot") else "futuresv2GetTrades"
        response = await getattr(self, method)(self.extend(request, params))
        trades = self.parse_trades(response, market, since, limit)
        for i in range(0, len(trades)):
            trades[i]["cost"] = None
            trades[i]["takerOrMaker"] = None
            trades[i]["side"] = trades[i]["info"]["side"].lower()
        return trades

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            "symbol": market["id"],
        }
        if limit is not None:
            request["count"] = limit
        if since is not None:
            request["startTime"] = int(since / 1000)
        defaultType = self.safe_string_2(
            self.options, "GetUserTradeHistory", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3privateGetUserTradeHistory"
            if (type == "spot")
            else "futuresv2privateGetUserTradeHistory"
        )
        response = await getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_value(trade, "timestamp")
        price = self.safe_float(trade, "price")
        amount = self.safe_float(trade, "size")
        cost = None
        if price is not None and amount is not None:
            cost = price * amount
        return {
            "id": self.safe_string(trade, "serialId"),
            "order": self.safe_string(trade, "orderId"),
            "symbol": market["symbol"],
            "price": self.safe_float(trade, "price"),
            "amount": self.safe_float(trade, "size"),
            "cost": cost,
            "fee": self.safe_float(trade, "feeAmount"),
            "type": None,
            "side": self.safe_string(trade, "side"),
            "datetime": self.iso8601(timestamp),
            "timestamp": timestamp,
            "info": trade,
        }

    async def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        defaultType = self.safe_string_2(
            self.options, "GetWalletHistory", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3privateGetUserWalletHistory"
            if (type == "spot")
            else "futuresv2privateGetUserWalletHistory"
        )
        response = await getattr(self, method)(self.extend(params))
        result = []
        for i in range(0, len(response)):
            deposit = response[i]
            if deposit["type"] == "Deposit":
                result.append(deposit)
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        defaultType = self.safe_string_2(
            self.options, "GetWallet", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3privateGetUserWallet"
            if (type == "spot")
            else "futuresv2privateGetUserWallet"
        )
        response = await getattr(self, method)(self.extend(params))
        result = {}
        if type == "spot":
            for i in range(0, len(response)):
                balance = response[i]
                code = self.safe_currency_code(self.safe_string(balance, "currency"))
                account = self.account()
                account["total"] = self.safe_float(balance, "total")
                account["free"] = self.safe_float(balance, "available")
                account["used"] = account["total"] - self.safe_float(
                    balance, "available"
                )
                result[code] = account
        else:
            for i in range(0, len(response[0]["assets"])):
                balance = response[0]["assets"][i]
                code = self.safe_currency_code(self.safe_string(balance, "currency"))
                account = self.account()
                account["total"] = self.safe_float(balance, "balance")
                account["free"] = self.safe_float(balance, "balance")
                account["used"] = 0
                result[code] = account
        result["info"] = response
        return self.parse_balance(result)

    def parse_ohlcv(self, ohlcv, market=None, timeframe="1m", since=None, limit=None):
        return [
            self.safe_timestamp(ohlcv, 0),
            self.safe_float(ohlcv, 1),
            self.safe_float(ohlcv, 2),
            self.safe_float(ohlcv, 3),
            self.safe_float(ohlcv, 4),
            None,  # 5 is quoteVolume
        ]

    async def fetch_ohlcv(
        self, symbol, timeframe="1m", since=None, limit=None, params={}
    ):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            "symbol": market["id"],
            "end": self.seconds(),
            "resolution": self.timeframes[timeframe],
        }
        if since is not None:
            request["start"] = int(since / 1000)
        defaultType = self.safe_string_2(
            self.options, "GetOhlcv", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = "spotv3GetOhlcv" if (type == "spot") else "futuresv2GetOhlcv"
        response = await getattr(self, method)(self.extend(request, params))
        return self.parse_ohlcvs(
            response, market["id"].upper(), timeframe, since, limit
        )

    async def fetch_trading_fees(self, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol) if symbol else None
        request = {
            "symbol": market["id"].upper() if market else None,
        }
        defaultType = self.safe_string_2(
            self.options, "GetTradingFees", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3privateGetUserFees"
            if (type == "spot")
            else "futuresv2privateGetUserFees"
        )
        response = await getattr(self, method)(self.extend(request))
        if not symbol:
            return {
                "info": response,
            }
        else:
            return {
                "info": response,
                "maker": self.safe_float(response[0], "makerFee"),
                "taker": self.safe_float(response[0], "takerFee"),
            }

    async def create_order(self, symbol, orderType, side, size, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            "symbol": market["id"].upper(),
            "side": side.upper(),
            "size": float(size),
            "time_in_force": "GTC",
        }
        priceToPrecision = None
        if price is not None:
            priceToPrecision = float(price)
        oType = orderType.upper()
        if oType == "LIMIT":
            request["type"] = "LIMIT"
            request["txType"] = "LIMIT"
            request["price"] = priceToPrecision
        elif oType == "MARKET":
            request["type"] = "MARKET"
            if params["currency"]:
                request["currency"] = params["currency"]
        elif oType == "STOP":
            request["txType"] = "STOP"
            request["stopPrice"] = priceToPrecision
        elif oType == "TRAILINGSTOP":
            request["trailValue"] = priceToPrecision
        else:
            raise InvalidOrder(
                self.id
                + " createOrder() does not support order type "
                + orderType
                + ", only limit, market, stop, trailingStop, or takeProfit orders are supported"
            )
        defaultType = self.safe_string_2(
            self.options, "PostOrder", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3privatePostOrder"
            if (type == "spot")
            else "futuresv2privatePostOrder"
        )
        response = await getattr(self, method)(self.extend(request, params))
        return self.parse_order(response[0])

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        if symbol is None:
            raise ArgumentsRequired(
                self.id + " cancelOrder() requires a `symbol` argument"
            )
        market = self.market(symbol)
        request = {
            "symbol": market["id"],
            "orderID": id,
            "clOrderID": None,
        }
        defaultType = self.safe_string_2(
            self.options, "DeleteOrder", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3privateDeleteOrder"
            if (type == "spot")
            else "futuresv2privateDeleteOrder"
        )
        response = await getattr(self, method)(self.extend(request, params))
        if response[0]["message"] == "ALL_ORDER_CANCELLED_SUCCESS":
            return response[0]
        return self.parse_order(response[0])

    async def cancel_all_orders(self, symbol=None, params={}):
        await self.load_markets()
        request = {
            "timeout": params["timeout"] if params["timeout"] else 0,
        }
        if symbol is not None:
            return self.cancel_order(None, symbol)
        defaultType = self.safe_string_2(
            self.options, "OrderCancelAllAfter", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3privatePostOrderCancelAllAfter"
            if (type == "spot")
            else "futuresv2privatePostOrderCancelAllAfter"
        )
        response = await getattr(self, method)(self.extend(request, params))
        return self.safe_value(response, "result", {})

    def parse_order_status(self, status):
        statuses = {
            "2": "created",
            "4": "closed",
            "5": "open",
            "6": "canceled",
            "9": "created",
            "10": "open",
            "15": "rejected",
            "16": "rejected",
        }
        return self.safe_string(statuses, status, status)

    def parse_order_type(self, type):
        types = {
            "76": "limit",
            "77": "market",
            "80": "peg",
        }
        return self.safe_string(types, type, type)

    def find_symbol(self, marketId, market):
        if market is None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId][0]
            else:
                return marketId
        return market["symbol"]

    def parse_order(self, order, market=None):
        timestamp = self.safe_value(order, "timestamp")
        filled = self.safe_float(order, "fillSize")
        amount = self.safe_float(order, "size")
        remaining = amount - filled
        average = self.safe_float(order, "averageFillPrice")
        price = self.safe_float_2(order, "price", "triggerPrice", average)
        cost = None
        if filled != 0 and price is not None:
            cost = filled * price
        return {
            "id": self.safe_string(order, "orderID"),
            "timestamp": timestamp,
            "datetime": self.iso8601(timestamp),
            "lastTradeTimestamp": None,
            "symbol": self.find_symbol(self.safe_string(order, "symbol"), market),
            "type": self.parse_order_type(self.safe_string(order, "orderType")),
            "side": self.safe_string(order, "side"),
            "price": price,
            "amount": amount,
            "cost": cost,
            "average": average,
            "filled": filled,
            "remaining": remaining,
            "status": self.parse_order_status(self.safe_string(order, "status")),
            "fee": None,
            "trades": None,
            "info": order,
        }

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        if symbol is None:
            raise ArgumentsRequired(
                self.id + " cancelOrder() requires a `symbol` argument"
            )
        market = self.market(symbol)
        request["symbol"] = market["id"]
        if since is not None:
            request["orderID"] = since
        defaultType = self.safe_string_2(
            self.options, "GetUserOpenOrders", "defaultType", "spot"
        )
        type = self.safe_string(params, "type", defaultType)
        method = (
            "spotv3privateGetUserOpenOrders"
            if (type == "spot")
            else "futuresv2privateGetUserOpenOrders"
        )
        response = await getattr(self, method)(self.extend(request, params))
        length = len(response)
        return self.parse_order(response[0]) if length else []

    async def create_deposit_address(self, currency, params={}):
        await self.load_markets()
        request = {
            currency,
        }
        response = await self.spotv3privatePostUserWalletAddress(
            self.extend(request, params)
        )
        return {
            "currency": currency,
            "address": response[0]["address"].split(":")[0],
            "tag": response[0]["address"].split(":")[1],
            "info": response,
        }

    async def fetch_deposit_address(self, currency, params={}):
        await self.load_markets()
        request = {
            currency,
        }
        response = await self.spotv3privateGetUserWalletAddress(
            self.extend(request, params)
        )
        return {
            "currency": currency,
            "address": response[0]["address"].split(":")[0],
            "tag": response[0]["address"].split(":")[1],
            "info": response,
        }

    async def withdraw(self, code, amount, address, tag=None, params={}):
        await self.load_markets()
        self.check_address(address)
        currency = self.currency(code)
        request = {
            "currency": currency["id"],
            "amount": str(amount),
            "address": address,
        }
        if tag is not None:
            request["tag"] = tag
        response = await self.spotv3privatePostUserWalletWithdraw(
            self.extend(request, params)
        )
        return {
            "id": response["withdrawId:"],
            "info": response,
        }

    def sign(self, path, api="api", method="GET", params={}, headers=None, body=None):
        url = self.urls["api"][api] + "/" + self.implode_params(path, params)
        bodyText = None
        if method == "GET" or method == "DELETE":
            if params:
                url += "?" + self.urlencode(params)
        if api == "spotv3private" or api == "futuresv2private":
            self.check_required_credentials()
            bodyText = self.json(params)
            signaturePath = self.clean_signature_path(
                api, self.urls["api"][api] + "/" + path
            )
            headers = self.sign_headers(method, signaturePath, headers, bodyText)
        body = None if (method == "GET") else bodyText
        return {"url": url, "method": method, "body": body, "headers": headers}

    def sign_headers(self, method, signaturePath, headers={}, bodyText=None):
        nonce = self.nonce()
        signature = None
        if method == "GET" or method == "DELETE":
            signature = self.create_signature(self.secret, nonce, signaturePath)
        else:
            signature = self.create_signature(
                self.secret, nonce, signaturePath, bodyText
            )
        headers["btse-nonce"] = nonce
        headers["btse-api"] = self.apiKey
        headers["btse-sign"] = signature
        headers["Content-Type"] = "application/json"
        return headers

    def create_signature(self, key, nonce, path, body=None):
        content = (
            body is self.encode("/" + path + nonce)
            if None
            else self.encode("/" + path + nonce + body)
        )
        return self.hmac(content, key, hashlib.sha384)

    def clean_signature_path(self, api, url):
        if api == "spotv3private":
            return url.replace("https://api.btse.com/spot/", "")
        else:
            return url.replace("https://api.btse.com/futures/", "")
