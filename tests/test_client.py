from datetime import datetime
from unittest.mock import MagicMock

import pytest

from client import Client, CurrencyComConstants, CandlesticksChartInervals


class TestClient(object):
    @pytest.fixture(autouse=True)
    def set_client(self, mock_requests):
        self.client = Client('', '')
        self.mock_get = mock_requests

    def test_not_called(self):
        self.mock_get.assert_not_called()

    def test_get_server_time(self, monkeypatch):
        self.client.get_server_time()
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.SERVER_TIME_ENDPOINT
        )

    def test_get_exchange_info(self):
        self.client.get_exchange_info()
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.EXCHANGE_INFORMATION_ENDPOINT
        )

    def test_get_order_book_default(self, monkeypatch):
        val_lim_mock = MagicMock()
        monkeypatch.setattr(self.client, '_validate_limit', val_lim_mock)
        symbol = 'TEST'
        self.client.get_order_book(symbol)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.ORDER_BOOK_ENDPOINT,
            params={'symbol': symbol, 'limit': 100}
        )
        val_lim_mock.assert_called_once_with(100)

    def test_get_order_book_with_limit(self, monkeypatch):
        val_lim_mock = MagicMock()
        limit = 500
        monkeypatch.setattr(self.client, '_validate_limit', val_lim_mock)
        symbol = 'TEST'
        self.client.get_order_book(symbol, limit)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.ORDER_BOOK_ENDPOINT,
            params={'symbol': symbol, 'limit': limit}
        )
        val_lim_mock.assert_called_once_with(limit)

    def test_get_agg_trades_default(self):
        symbol = 'TEST'
        self.client.get_agg_trades(symbol)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.AGGREGATE_TRADE_LIST_ENDPOINT,
            params={'symbol': symbol, 'limit': 500}
        )

    def test_get_agg_trades_limit_set(self):
        symbol = 'TEST'
        limit = 20
        self.client.get_agg_trades(symbol, limit=limit)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.AGGREGATE_TRADE_LIST_ENDPOINT,
            params={'symbol': symbol, 'limit': limit}
        )

    def test_get_agg_trades_max_limit(self):
        symbol = 'TEST'
        limit = CurrencyComConstants.AGG_TRADES_MAX_LIMIT
        self.client.get_agg_trades(symbol, limit=limit)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.AGGREGATE_TRADE_LIST_ENDPOINT,
            params={'symbol': symbol, 'limit': limit}
        )

    def test_get_agg_trades_exceed_limit(self):
        symbol = 'TEST'
        limit = CurrencyComConstants.AGG_TRADES_MAX_LIMIT + 1
        with pytest.raises(ValueError):
            self.client.get_agg_trades(symbol, limit=limit)
        self.mock_get.assert_not_called()

    def test_get_agg_trades_only_start_time_set(self):
        symbol = 'TEST'
        start_time = datetime(2019, 1, 1, 1, 1, 1)
        self.client.get_agg_trades(symbol, start_time=start_time)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.AGGREGATE_TRADE_LIST_ENDPOINT,
            params={'symbol': symbol, 'limit': 500,
                    'startTime': start_time.timestamp() * 1000}
        )

    def test_get_agg_trades_only_end_time_set(self):
        symbol = 'TEST'
        end_time = datetime(2019, 1, 1, 1, 1, 1)
        self.client.get_agg_trades(symbol, end_time=end_time)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.AGGREGATE_TRADE_LIST_ENDPOINT,
            params={'symbol': symbol, 'limit': 500,
                    'endTime': end_time.timestamp() * 1000}
        )

    def test_get_agg_trades_both_time_set(self):
        symbol = 'TEST'
        start_time = datetime(2019, 1, 1, 1, 1, 1)
        end_time = datetime(2019, 1, 1, 1, 1, 20)
        self.client.get_agg_trades(symbol,
                                   start_time=start_time,
                                   end_time=end_time)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.AGGREGATE_TRADE_LIST_ENDPOINT,
            params={'symbol': symbol, 'limit': 500,
                    'startTime': start_time.timestamp() * 1000,
                    'endTime': end_time.timestamp() * 1000}
        )

    def test_get_agg_trades_both_time_set_exceed_max_range(self):
        symbol = 'TEST'
        start_time = datetime(2019, 1, 1, 1, 1, 1)
        end_time = datetime(2019, 1, 1, 2, 2, 20)
        with pytest.raises(ValueError):
            self.client.get_agg_trades(symbol,
                                       start_time=start_time,
                                       end_time=end_time)
        self.mock_get.assert_not_called()

    def test_get_klines_default(self):
        symbol = 'TEST'
        self.client.get_klines(symbol, CandlesticksChartInervals.DAY)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.KLINES_DATA_ENDPOINT,
            params={'symbol': symbol,
                    'interval': CandlesticksChartInervals.DAY.value,
                    'limit': 500}
        )

    def test_get_klines_with_limit(self):
        symbol = 'TEST'
        limit = 123
        self.client.get_klines(symbol, CandlesticksChartInervals.DAY,
                               limit=limit)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.KLINES_DATA_ENDPOINT,
            params={'symbol': symbol,
                    'interval': CandlesticksChartInervals.DAY.value,
                    'limit': limit}
        )

    def test_get_klines_max_limit(self):
        symbol = 'TEST'
        limit = CurrencyComConstants.KLINES_MAX_LIMIT
        self.client.get_klines(symbol, CandlesticksChartInervals.DAY,
                               limit=limit)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.KLINES_DATA_ENDPOINT,
            params={'symbol': symbol,
                    'interval': CandlesticksChartInervals.DAY.value,
                    'limit': limit}
        )

    def test_get_klines_exceed_max_limit(self):
        symbol = 'TEST'
        limit = CurrencyComConstants.KLINES_MAX_LIMIT + 1
        with pytest.raises(ValueError):
            self.client.get_klines(symbol, CandlesticksChartInervals.DAY,
                                   limit=limit)
        self.mock_get.assert_not_called()

    def test_get_klines_with_startTime(self):
        symbol = 'TEST'
        start_date = datetime(2020, 1, 1)
        self.client.get_klines(symbol,
                               CandlesticksChartInervals.DAY,
                               start_time=start_date)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.KLINES_DATA_ENDPOINT,
            params={'symbol': symbol,
                    'interval': CandlesticksChartInervals.DAY.value,
                    'startTime': int(start_date.timestamp() * 1000),
                    'limit': 500}
        )

    def test_get_klines_with_endTime(self):
        symbol = 'TEST'
        end_time = datetime(2020, 1, 1)
        self.client.get_klines(symbol,
                               CandlesticksChartInervals.DAY,
                               end_time=end_time)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.KLINES_DATA_ENDPOINT,
            params={'symbol': symbol,
                    'interval': CandlesticksChartInervals.DAY.value,
                    'endTime': int(end_time.timestamp() * 1000),
                    'limit': 500}
        )

    def test_get_klines_with_startTime_and_endTime(self):
        symbol = 'TEST'
        start_time = datetime(2020, 1, 1)
        end_time = datetime(2021, 1, 1)
        self.client.get_klines(symbol,
                               CandlesticksChartInervals.DAY,
                               start_time=start_time,
                               end_time=end_time)
        self.mock_get.assert_called_once_with(
            CurrencyComConstants.KLINES_DATA_ENDPOINT,
            params={'symbol': symbol,
                    'interval': CandlesticksChartInervals.DAY.value,
                    'startTime': int(start_time.timestamp() * 1000),
                    'endTime': int(end_time.timestamp() * 1000),
                    'limit': 500}
        )