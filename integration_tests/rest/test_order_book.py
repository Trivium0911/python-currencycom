import sys
import pytest


class TestOrderBook:

    def test_response_corresponds_swagger_schema(self, client):
        resp_keys = ['asks', 'bids', 'lastUpdateId']
        order_book = client.get_order_book('EUR/USD_LEVERAGE')
        assert type(order_book) is dict
        assert len(order_book) == 3
        assert all(dct in resp_keys for dct in order_book.keys())
        assert all(order_book[key] is not None for key in order_book.keys())

    @pytest.mark.parametrize('limit', [1, 2, 500, 999, 1000])
    def test_limit(self, client, limit):
        order_book = client.get_order_book('GBP/USD_LEVERAGE', limit=limit)
        assert len(order_book['asks']) == limit
        assert len(order_book['bids']) == limit

    @pytest.mark.parametrize('limit', [-sys.maxsize, -1, 0,
                                       1001, sys.maxsize])
    def test_invalid_limit(self, client, limit):
        with pytest.raises(ValueError):
            client.get_order_book('EUR/USD_LEVERAGE', limit=limit)

    def test_wrong_symbol(self, client):
        agg_trades = client.get_order_book(symbol="TEST123")
        assert agg_trades['code'] == -1128 and 'symbol not found ' \
               in agg_trades['msg']


