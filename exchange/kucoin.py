import ccxt.async_support as ccxt

async def get_kucoin_orderbook(symbol, limit):
    client = ccxt.kucoin()
    try:
        if limit not in [20, 100]:
            limit = 20
        orderbook = await client.fetch_order_book(symbol, limit=limit)
        return {
            'bids': orderbook['bids'],
            'asks': orderbook['asks']
        }
    except Exception as e:
        error_message = (
            f"Error fetching order book data from {client.name}:\n"
            f"Symbol: {symbol}, Limit: {limit}\n"
            f"Error message: {e}"
        )
        raise RuntimeError(error_message)
    finally:
        await client.close()