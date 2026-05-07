import sqlite3
import pytest
from unittest.mock import patch, MagicMock
import random
import datetime
import responses
from functions import neg, rev, rnd, greet, download, DownloadError
from app import Payment


def test_neg():
    assert neg(5) == -5
    assert neg(-3) == 3
    assert neg(0) == 0
    assert neg(15) == -15


def test_reversed():
    assert rev([1, 2, 3]) == [3, 2, 1]
    assert rev([]) == []
    assert rev([100, 100, 100]) == [100, 100, 100]


def test_rnd():
    random.seed(1000)
    assert rnd(10) == 6


def test_greet():
    real_datetime = datetime.datetime
    with patch('functions.datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = real_datetime(2024, 6, 1, 9, 0)
        assert greet("Alice") == "Good morning, Alice!"
        
        mock_datetime.now.return_value = real_datetime(2024, 6, 1, 15, 0)
        assert greet("Bob") == "Good afternoon, Bob!"
        
        mock_datetime.now.return_value = real_datetime(2024, 6, 1, 20, 0)
        assert greet("Charlie") == "Good evening, Charlie!"


@responses.activate
def test_download():
    responses.add(
        responses.GET,
        "https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt",
        body="01.05.2026\nUSD 22.345\nEUR 25.678",
        status=200
    )
    responses.add(
        responses.GET,
        "https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt2",
        body="Not Found",
        status=404
    )

    assert download("https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt")[:10] == "01.05.2026"
    with pytest.raises(DownloadError):
        download("https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt2")


def test_payment():
    sqlite = sqlite3.connect(":memory:")
    db = Payment(sqlite)
    db.add_payment(100, "Groceries")
    cursor = db.db.cursor()
    cursor.execute("SELECT amount, description FROM payments")
    result = cursor.fetchone()
    assert result == (100, "Groceries")


def test_payment_mock():
    mock_db = MagicMock()
    mock_db.cursor.return_value = MagicMock()
    payment = Payment(mock_db)
    payment.add_payment(50, "Books")
    mock_db.cursor().execute.assert_called_with("INSERT INTO payments (amount, description) VALUES (?, ?)", (50, "Books"))
    assert mock_db.commit.call_count == 2



