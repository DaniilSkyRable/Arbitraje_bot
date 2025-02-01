import asyncio
import sys
from exchange import get_binance_orderbook,get_kucoin_orderbook,get_okx_orderbook

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def calculate_orderbook(orderbook, usdt_target, order_type='asks'):

    if order_type not in ['asks', 'bids']:
        raise ValueError("order_type must be 'asks' or 'bids'")

    total_cost = 0
    total_volume = 0
    orders_used = []

    for order in orderbook[order_type]:
        price, volume = order[0], order[1]
        cost = price * volume
        if total_cost + cost >= usdt_target:
            needed_volume = (usdt_target - total_cost) / price
            total_volume += needed_volume
            total_cost += needed_volume * price
            orders_used.append({'price': price, 'volume': needed_volume})
            break
        else:
            # Добавляем весь объем текущего ордера
            total_volume += volume
            total_cost += cost
            orders_used.append({'price': price, 'volume': volume})

    # Рассчитываем среднюю цену
    avg_price = total_cost / total_volume if total_volume > 0 else 0

    return {
        'usdt_target': usdt_target,
        'total_cost': total_cost,
        'total_volume': total_volume,
        'avg_price': avg_price,
        'orders_used': orders_used
    }

async def main():
    usdt_amount = 500

    kucoin_orderbook = await get_kucoin_orderbook("W/USDT", 20)
    binance_orderbook = await get_binance_orderbook("W/USDT", 10)
    okx_orderbook = await get_okx_orderbook("W/USDT", 10)

    print("\nKuCoin:")
    result_asks_kucoin = calculate_orderbook(kucoin_orderbook, usdt_amount, order_type='asks')
    result_bids_kucoin = calculate_orderbook(kucoin_orderbook, usdt_amount, order_type='bids')
    print("Аски:", result_asks_kucoin)
    print("Биды:", result_bids_kucoin)

    print("\nBinance:")
    result_asks_binance = calculate_orderbook(binance_orderbook, usdt_amount, order_type='asks')
    result_bids_binance = calculate_orderbook(binance_orderbook, usdt_amount, order_type='bids')
    print("Аски:", result_asks_binance)
    print("Биды:", result_bids_binance)
    
    print("\nOKX:")
    result_asks_okx = calculate_orderbook(okx_orderbook, usdt_amount, order_type='asks')
    result_bids_okx = calculate_orderbook(okx_orderbook, usdt_amount, order_type='bids')
    print("Аски:", result_asks_okx)
    print("Биды:", result_bids_okx)

if __name__ == "__main__":
    asyncio.run(main())