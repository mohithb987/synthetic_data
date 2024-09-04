import random
from faker import Faker
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()

def fetch_existing_card_nums():
    cursor.execute("SELECT cardnumber FROM CreditCard")
    existing_cardnumbers = [row[0] for row in cursor.fetchall()]
    return existing_cardnumbers


def fetch_merchant_ids():
    cursor.execute("SELECT merchantid FROM merchant")
    existing_merchant_ids = [row[0] for row in cursor.fetchall()]
    return existing_merchant_ids

def generate_fake_transactions(num_records, card_numbers, merchant_ids):
    transactions = []
    for _ in range(num_records):
        transaction_id = fake.random_number(digits=8)
        card_number = random.choice(card_numbers)
        merchant_id = random.choice(merchant_ids)
        transaction_amt = round(random.uniform(1, 3000), 2)
        transaction_time = fake.date_time_between(start_date="-1y", end_date="now")

        transaction = {
            'TransactionID': transaction_id,
            'CardNumber': card_number,
            'MerchantID': merchant_id,
            'Transaction_amt': transaction_amt,
            'Transaction_time': transaction_time,
        }
        transactions.append(transaction)
    return transactions

card_numbers = fetch_existing_card_nums()
merchant_ids = fetch_merchant_ids()

transactions_data = generate_fake_transactions(10000, card_numbers, merchant_ids)
for transaction in transactions_data[:5]:
    print(transaction)

import csv

csv_file_path = 'csv_files/TransactionsData.csv'
headers = ['TransactionID', 'CardNumber', 'MerchantID', 'Transaction_amt', 'Transaction_time']

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()

    for transaction in transactions_data:
        writer.writerow(transaction)

print('### Finished generating Merchants data. Sample:\n\n')
for transaction in transactions_data[:5]:
    print(transaction)
    print("\n\n")


def insert_data_into_table(data):
    for transaction in data:
        cursor.execute("""
            INSERT INTO Transaction (
                TransactionID, CardNumber, MerchantID, Transaction_amt, Transaction_time
            ) VALUES (%s, %s, %s, %s,%s)
        """, (
            transaction['TransactionID'], transaction['CardNumber'], transaction['MerchantID'], transaction['Transaction_amt'], transaction['Transaction_time']
        ))

print('### Starting to insert Merchants data into Postgres DB.\n\n')

insert_data_into_table(transactions_data)
conn.commit()
print('### Successfully inserted Merchants data into Postgres DB! \n\n')

cursor.close()
conn.close()
