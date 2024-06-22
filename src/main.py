from src.utils1 import read_excel_to_dict_lict, filter_transactions_by_date, get_last_digits, get_total_spent, top_5_transactions
import pandas as pd



def get_card_number(transactions):
    card_number = []
    new_card = []
    for transaction in transactions:
        if pd.notnull(transaction['Номер карты']):
            card_number.append(transaction['Номер карты'])
    for card in card_number:
        if card not in new_card:
            new_card.append(card)
    return new_card


def get_card_info(transactions, card_number):
    """
    Возвращает информацию о карте.
    """
    list_dict = []
    for card in card_number:
        for transaction in transactions:
            if card == transaction['Номер карты']:
                last_digit = get_last_digits(card)
                total_spent = get_total_spent(transactions, card)
                cashback = total_spent // 100

                result = {
                        "last_digit": str(last_digit),
                        "total_spent ": total_spent,
                        "cashback": cashback
                }
        list_dict.append(result)
    print(list_dict)
    return list_dict

if __name__ == '__main__':
    file_path = '../data/operations.xls'
    transactions = filter_transactions_by_date(read_excel_to_dict_lict(file_path), '30.12.2021')
    card = get_card_number(transactions)
    card_info = get_card_info(transactions, card)
    top_5 = top_5_transactions(transactions)
    for num in top_5:

        print(num)


