import random
from faker import Faker
from datetime import datetime
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()


account_types = ['Savings', 'Checking', 'Credit Card', 'Loan']

def fetch_existing_client_nums():
    cursor.execute("SELECT Client_num FROM Client")
    existing_client_nums = [row[0] for row in cursor.fetchall()]
    return existing_client_nums


def fetch_existing_client_nums():
    cursor.execute("SELECT Client_num FROM Client")
    existing_client_nums = [row[0] for row in cursor.fetchall()]
    return existing_client_nums


def fetch_existing_bank_ids():
    cursor.execute("SELECT BankID FROM Bank")
    existing_bank_ids = [row[0] for row in cursor.fetchall()]
    return existing_bank_ids

# Generate fake data for account information
def generate_fake_accounts(num_records, client_nums, bank_ids):
    accounts = []
    generated_account_nums = set()
    for _ in range(num_records):
        account_no = random.randint(1, 1000000)
        while account_no in generated_account_nums:
            account_no = random.randint(1, 1000000)
        generated_account_nums.add(account_no)
        client_num = random.choice(client_nums)
        client_nums.remove(client_num)
        bank_id = random.choice(bank_ids)
        account_type = random.choice(account_types)
        balance = round(random.uniform(100, 100000), 2)
        open_date = fake.date_between(start_date='-5y', end_date='today')
        close_date = None 
        if random.random() < 0.2:
            close_date = fake.date_between(start_date=open_date, end_date='today')
        overdraft_limit = round(random.uniform(0, 1000), 2)

        account = {
            'AccountNo': account_no,
            'Client_num': client_num,
            'BankID': bank_id,
            'AccountType': account_type,
            'Balance': balance,
            'Open_date': open_date,
            'Close_date': close_date,
            'Overdraft_limit': overdraft_limit
        }
        accounts.append(account)
    return accounts

num_accounts = 5000

existing_client_nums = fetch_existing_client_nums()
existing_bank_ids = fetch_existing_bank_ids()
accounts_data = generate_fake_accounts(num_accounts, existing_client_nums, existing_bank_ids)
for account in accounts_data[:5]:
    print(account)

import csv

csv_file_path = 'csv_files/AccountInformation.csv'
headers = ['AccountNo', 'Client_num', 'BankID', 'AccountType', 'Balance', 'Open_date', 'Close_date', 'Overdraft_limit']
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for account in accounts_data:
        writer.writerow(account)

print('### Finished generating AccountInformation data. Sample:\n\n')


def insert_data_into_table(data):
    for account in data:
        cursor.execute("""
            INSERT INTO AccountInformation (
                AccountNo, Client_num, BankID, AccountType, Balance, Open_date, Close_date, Overdraft_limit)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            account ['AccountNo'], account ['Client_num'], account ['BankID'], account ['AccountType'], account ['Balance'], account ['Open_date'], account ['Close_date'], account ['Overdraft_limit']       ))

print('### Starting to insert AccountInformation data into Postgres DB.\n\n')

insert_data_into_table(accounts_data)
conn.commit()
print('### Successfully inserted AccountInformation data into Postgres DB! \n\n')

cursor.close()
conn.close()