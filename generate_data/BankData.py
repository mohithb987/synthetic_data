import random

from faker import Faker
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()

def generate_fake_bank(num_records):
    banks = []
    bank_names = ['Chase', 'Bank of America', 'Wells Fargo', 'Citibank', 'U.S. Bank', 'Goldman Sachs Bank', 'Capital One']
    branch_names = [fake.city() for _ in range(10)]
    bank_info = {}
    i=0
    while i < num_records:
        bank_name = random.choice(bank_names)
        branch_name = random.choice(branch_names)

        if (bank_name, branch_name) not in bank_info:
            bank_info[(bank_name, branch_name)] = {
                'BankID': random.randint(10000000, 99999999),
                'RoutingNumber': random.randint(100000000, 999999999)
            }
        else:
            continue
        bank_id = bank_info[(bank_name, branch_name)]['BankID']
        routing_number = bank_info[(bank_name, branch_name)]['RoutingNumber']

        bank = {
            'BankID': bank_id,
            'Name': bank_name,
            'BranchName': branch_name,
            'RoutingNumber': routing_number
        }
        banks.append(bank)
        i+=1

    return banks

bank_data = generate_fake_bank(60)

import csv

csv_file_path = 'csv_files/BanksData.csv'
headers = [
    'BankID', 'Name', 'BranchName', 'RoutingNumber'
]

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for bank in bank_data:
        writer.writerow(bank)

print('### Finished generating Bank data. Sample:\n\n')
for bank in bank_data:
    print(bank)
    print("\n\n")


def insert_data_into_table(data):
    for bank in bank_data:
        cursor.execute("""
            INSERT INTO Bank (
                BankID, Name, BranchName, RoutingNumber
            ) VALUES (%s, %s, %s, %s)
        """, (
            bank['BankID'], bank['Name'], bank['BranchName'], bank['RoutingNumber']
        ))

print('### Starting to insert Banks data into Postgres DB.\n\n')
insert_data_into_table(bank_data)

conn.commit()
print('### Successfully inserted Banks data into Postgres DB! \n\n')

cursor.close()
conn.close()
