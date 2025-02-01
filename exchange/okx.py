import ccxt.async_support as ccxt

async def get_okx_orderbook(symbol, limit):
    client = ccxt.okx()
    try:
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