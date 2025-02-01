import asyncio
import sys
from exchange import get_binance_orderbook,get_kucoin_orderbook,get_okx_orderbook
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    
async def main():
    g = await get_kucoin_orderbook("BTC/USDT", 20)
    b = await get_binance_orderbook("BTC/USDT", 10)
    o = await get_okx_orderbook("BTC/USDT", 10)
    print(g)
    print(b)
    print(o)

if __name__ == "__main__":
    asyncio.run(main())
