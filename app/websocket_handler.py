import asyncio
import json
import threading

import requests
import websockets

binance_data = {}
kraken_data = {}


def get_all_kraken_pairs():
    url = "https://api.kraken.com/0/public/AssetPairs"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        formatted_pairs = [data['result'][pair]['wsname'] for pair in data['result']]
        return formatted_pairs
    else:
        print("Failed to fetch pairs from Kraken API")
        return []


class WebSocketHandler:

    async def get_binance_data(self):
        uri = "wss://stream.binance.com:9443/ws/!ticker@arr"
        try:
            async with websockets.connect(uri, ping_interval=20) as websocket:
                print(f"Connected to {uri}")
                while True:
                    data = await websocket.recv()
                    data = json.loads(data)
                    for ticker in data:
                        if 's' in ticker and 'b' in ticker and 'a' in ticker:
                            pair = ticker['s']
                            avg_price = (float(ticker['b']) + float(ticker['a'])) / 2
                            binance_data[pair] = avg_price
        except Exception as e:
            print(f"Error connecting to Binance: {e}")

    async def get_kraken_data(self, pairs):
        uri = "wss://ws.kraken.com"
        subscription_message = {
            "event": "subscribe",
            "pair": pairs,
            "subscription": {"name": "ticker"}
        }
        try:
            async with websockets.connect(uri, ping_interval=20) as websocket:
                print(f"Connected to {uri}")
                await websocket.send(json.dumps(subscription_message))
                while True:
                    data = await websocket.recv()
                    data = json.loads(data)
                    if isinstance(data, list) and len(data) > 3:
                        pair = data[3].replace('/', '')
                        price_info = data[1]
                        if 'c' in price_info:
                            avg_price = float(price_info['c'][0])
                            kraken_data[pair] = avg_price
        except Exception as e:
            print(f"Error connecting to Kraken: {e}")



def run_websocket_connections():
    handler = WebSocketHandler()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kraken_pairs = get_all_kraken_pairs()
    batch_size = 300
    kraken_tasks = [
        handler.get_kraken_data(kraken_pairs[i:i + batch_size])
        for i in range(0, len(kraken_pairs), batch_size)
    ]

    binance_task = handler.get_binance_data()

    tasks = [binance_task] + kraken_tasks

    loop.run_until_complete(asyncio.gather(*tasks))


thread = threading.Thread(target=run_websocket_connections, daemon=True)
thread.start()
