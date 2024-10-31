from dal import autocomplete
from django.http import JsonResponse
from django.shortcuts import render

from .websocket_handler import binance_data, kraken_data


class PairAutocomplete(autocomplete.Select2ListView):
    def get(self, request, *args, **kwargs):
        exchange = request.GET.get('exchange')
        query = request.GET.get('q', '')
        if exchange:
            if exchange.lower() == 'binance':
                pairs = list(binance_data.keys())
            elif exchange.lower() == 'kraken':
                pairs = list(kraken_data.keys())
            else:
                pairs = []

            if query:
                pairs = [pair for pair in pairs if query.lower() in pair.lower()]

            return JsonResponse(pairs, safe=False)
        return JsonResponse([], safe=False)


def get_prices(request):
    exchange = request.GET.get('exchange')
    pair = request.GET.get('pair')

    if exchange:
        if exchange.lower() == 'binance':
            data = {pair: price for pair, price in binance_data.items()} if not pair else {pair: binance_data.get(pair)}
        elif exchange.lower() == 'kraken':
            data = {pair: price for pair, price in kraken_data.items()} if not pair else {pair: kraken_data.get(pair)}
        else:
            data = {"error": "Exchange not supported"}
    else:

        data = {}
        all_pairs = set(binance_data.keys()).union(set(kraken_data.keys()))

        for p in all_pairs:
            binance_price = binance_data.get(p)
            kraken_price = kraken_data.get(p)

            if binance_price and kraken_price:
                data[p] = (binance_price + kraken_price) / 2
            elif binance_price:
                data[p] = binance_price
            elif kraken_price:
                data[p] = kraken_price

    return JsonResponse(data, safe=False)


def index(request):
    return render(request, 'index.html')
