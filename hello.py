#%%
from time import sleep
import ccxt
import json
import arrow

#! ------ Staring info
binance = ccxt.binance({
    'apiKey': 'kfpbRZXI0dAOpVDlcZaVZBJvFzB0Yl8EanH3Eph9fyOVbeUcVDqqKfRFE18iq63t',
    'secret': '6rcXkDoa9LGsS75q3gxAx0rL5kw7M7oXfnPsnst7JT4wjafU5ElgEAJW3hVSE5ZV',
})
binance.set_sandbox_mode(True)

def avg(lst):
    return sum(lst) / len(lst)

def bprint(text):
    print(json.dumps(text, indent=4))

def show_balance(exchange,last_price):
    balance = exchange.fetch_balance()
    print(f"BTC: {balance['BTC']['total']}  USDT: {round(balance['USDT']['total'], 2)}$")
    print(f"Total USDT: {round(balance['BTC']['total'] * last_price + balance['USDT']['total'], 2)}$")
    
    
def get_price():
    prices = binance.fetchOHLCV('BTC/USDT', '1m', None, 5)
    fprices = [{
        PRICE_COL[idx]: arrow.get(item)
        .to('Asia/Ho_Chi_Minh')
        .format('YYYY-MM-DD HH:mm:ss')
        if idx == 0
        else item
        for idx, item in enumerate(sprice)
    } for sprice in prices]

    return [item['close'] for item in fprices]

    

PRICE_COL = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
TRADE_SIZE = 100

while True:
    close_price_list = get_price()
    last_price = close_price_list[4]
    quantity = TRADE_SIZE/last_price
    avg_price = avg(close_price_list)

    #TODO viet thuat toan buy-sell
    direction = 'sell' if last_price > avg_price else 'buy'
    mark = '>' if direction == 'sell' else '<'
    #direction = 'buy'
    print(f"lastprice: {last_price} {mark} avg: {avg_price} => {direction}")
    order = binance.create_market_order('BTC/USDT', direction, quantity)
    print(f'{direction} at price {last_price}')
    show_balance(binance, last_price)
    sleep(60)
    print("--------------------------------")



#TODO viet log to file + in ra
    #TODO don gian truoc
    #TODO ranh viet theo log luon
    
    
    
    if __name__ == '__main__':
        