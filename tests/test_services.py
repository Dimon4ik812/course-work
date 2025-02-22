import json

import pytest

from src.services import (analyze_cashback, find_person_to_person_transactions, investment_bank,
                          search_transaction_by_mobile_phone, search_transactions_by_user_choice)


@pytest.mark.parametrize("transactions, year, month, expected_output", [
    (
            [
                {"Дата операции": "15.05.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -1000,
                 "Кэшбэк": 10},
                {"Дата операции": "15.05.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -2000,
                 "Кэшбэк": None},
                {"Дата операции": "15.05.2023 12:34:56", "Категория": "Развлечения", "Сумма операции": -500,
                 "Кэшбэк": 5},
                {"Дата операции": "15.04.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -1000,
                 "Кэшбэк": 10},
            ],
            2023,
            5,
            json.dumps({
                "Продукты": 30.0,
                "Развлечения": 5.0
            }, ensure_ascii=False, indent=4)
    ),
    (
            [
                {"Дата операции": "15.06.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -1000,
                 "Кэшбэк": None},
                {"Дата операции": "15.06.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -2000,
                 "Кэшбэк": 20},
                {"Дата операции": "15.06.2023 12:34:56", "Категория": "Развлечения", "Сумма операции": -500,
                 "Кэшбэк": 5},
                {"Дата операции": "15.04.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -1000,
                 "Кэшбэк": 10},
            ],
            2023,
            6,
            json.dumps({
                "Продукты": 30.0,
                "Развлечения": 5.0
            }, ensure_ascii=False, indent=4)
    ),
    (
            [
                {"Дата операции": "15.07.2023 12:34:56", "Категория": "Транспорт", "Сумма операции": -1500,
                 "Кэшбэк": 15},
                {"Дата операции": "15.07.2023 12:34:56", "Категория": "Транспорт", "Сумма операции": -500,
                 "Кэшбэк": None},
                {"Дата операции": "15.07.2023 12:34:56", "Категория": "Развлечения", "Сумма операции": -500,
                 "Кэшбэк": 5},
                {"Дата операции": "15.04.2023 12:34:56", "Категория": "Транспорт", "Сумма операции": -1000,
                 "Кэшбэк": 10},
            ],
            2023,
            7,
            json.dumps({
                "Транспорт": 20.0,
                "Развлечения": 5.0
            }, ensure_ascii=False, indent=4)
    )
])
def test_analyze_cashback(transactions, year, month, expected_output):
    result = analyze_cashback(transactions, year, month)
    assert result == expected_output


@pytest.mark.parametrize("transactions, date, limit, expected_output", [
    (
            [
                {"Дата операции": "15.05.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -1712},
                {"Дата операции": "16.05.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -3456},
                {"Дата операции": "17.05.2023 12:34:56", "Категория": "Развлечения", "Сумма операции": -789},
                {"Дата операции": "18.04.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -300},
            ],
            "2023.05",
            50,
            93
    ),
    (
            [
                {"Дата операции": "15.06.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -1024},
                {"Дата операции": "16.06.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -2024},
                {"Дата операции": "17.06.2023 12:34:56", "Категория": "Развлечения", "Сумма операции": -3050},
                {"Дата операции": "18.06.2023 12:34:56", "Категория": "Транспорт", "Сумма операции": -1500},
            ],
            "2023.06",
            100,
            302
    ),
    (
            [
                {"Дата операции": "15.07.2023 12:34:56", "Категория": "Транспорт", "Сумма операции": -1725},
                {"Дата операции": "16.07.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -150},
                {"Дата операции": "17.07.2023 12:34:56", "Категория": "Развлечения", "Сумма операции": -345},
                {"Дата операции": "18.07.2023 12:34:56", "Категория": "Продукты", "Сумма операции": -675},
            ],
            "2023.07",
            25,
            80
    )
])
def test_investment_bank(transactions, date, limit, expected_output):
    result = investment_bank(transactions, date, limit)
    assert result == expected_output


@pytest.mark.parametrize("transactions, search, expected_output", [
    (
            [
                {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000},
                {"Категория": "Развлечения", "Описание": "Кинотеатр", "Сумма операции": -500},
                {"Категория": "Транспорт", "Описание": "Такси", "Сумма операции": -300},
            ],
            "магазин",
            json.dumps([
                {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000}
            ], ensure_ascii=False, indent=4)
    ),
    (
            [
                {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000},
                {"Категория": "Развлечения", "Описание": "Кинотеатр", "Сумма операции": -500},
                {"Категория": "Транспорт", "Описание": "Такси", "Сумма операции": -300},
            ],
            "кино",
            json.dumps([
                {"Категория": "Развлечения", "Описание": "Кинотеатр", "Сумма операции": -500}
            ], ensure_ascii=False, indent=4)
    ),
    (
            [
                {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000},
                {"Категория": "Развлечения", "Описание": "Кинотеатр", "Сумма операции": -500},
                {"Категория": "Транспорт", "Описание": "Такси", "Сумма операции": -300},
            ],
            "транспорт",
            json.dumps([
                {"Категория": "Транспорт", "Описание": "Такси", "Сумма операции": -300}
            ], ensure_ascii=False, indent=4)
    ),
    (
            [
                {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000},
                {"Категория": "Развлечения", "Описание": "Кинотеатр", "Сумма операции": -500},
                {"Категория": "Транспорт", "Описание": "Такси", "Сумма операции": -300},
            ],
            "Продукты",
            json.dumps([
                {"Категория": "Продукты", "Описание": "Покупка в магазине", "Сумма операции": -1000}
            ], ensure_ascii=False, indent=4)
    ),
])
def test_search_transactions_by_user_choice(transactions, search, expected_output):
    result = search_transactions_by_user_choice(transactions, search)
    assert result == expected_output


def test_search_transaction_by_mobile_phone():
    transactions = [
        {"Описание": "Я МТС +7 921 11-22-33", "Сумма операции": -1000},
        {"Описание": "Тинькофф Мобайл +7 995 555-55-55", "Сумма операции": -1500},
        {"Описание": "Магазин", "Сумма операции": -500},
        {"Описание": "МТС Mobile +7 981 333-44-55", "Сумма операции": -2000},
        {"Описание": "Оплата по карте", "Сумма операции": -300}
    ]

    expected_output = json.dumps([
        {"Описание": "Я МТС +7 921 11-22-33", "Сумма операции": -1000},
        {"Описание": "Тинькофф Мобайл +7 995 555-55-55", "Сумма операции": -1500},
        {"Описание": "МТС Mobile +7 981 333-44-55", "Сумма операции": -2000}
    ], ensure_ascii=False, indent=4)

    result = search_transaction_by_mobile_phone(transactions)
    assert result == expected_output


def test_find_person_to_person_transactions():
    transactions = [
        {"Категория": "Переводы", "Описание": "Перевод Сергей А.", "Сумма операции": -1000},
        {"Категория": "Переводы", "Описание": "Перевод Навид Б.", "Сумма операции": -1500},
        {"Категория": "Магазин", "Описание": "Покупка в магазине", "Сумма операции": -500},
        {"Категория": "Переводы", "Описание": "Перевод Вероника Э.", "Сумма операции": -2000},
        {"Категория": "Переводы", "Описание": "Перевод Игорь С.", "Сумма операции": -300},
        {"Категория": "Переводы", "Описание": "Перевод Денис.", "Сумма операции": -700}
    ]

    expected_output = json.dumps([
        {"Категория": "Переводы", "Описание": "Перевод Сергей А.", "Сумма операции": -1000},
        {"Категория": "Переводы", "Описание": "Перевод Навид Б.", "Сумма операции": -1500},
        {"Категория": "Переводы", "Описание": "Перевод Вероника Э.", "Сумма операции": -2000},
        {"Категория": "Переводы", "Описание": "Перевод Игорь С.", "Сумма операции": -300}
    ], ensure_ascii=False, indent=4)

    result = find_person_to_person_transactions(transactions)
    assert result == expected_output