import random
from faker import Faker
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()

def fetch_existing_client_nums():
    cursor.execute("SELECT Client_num FROM Client")
    existing_client_nums = [row[0] for row in cursor.fetchall()]
    return existing_client_nums

def fetch_existing_bank_ids():
    cursor.execute("SELECT BankID FROM Bank")
    existing_bank_ids = [row[0] for row in cursor.fetchall()]
    return existing_bank_ids
def generate_fake_creditcard(existing_client_nums, existing_bank_ids, num_records):
    creditcards = []
    generated_card_nums = set()
    for i in range(num_records):
        card_category = random.choice(['Standard', 'Rewards', 'Premium', 'Business', 'Student'])
        credit_limit = random.uniform(1000, 10000)
        avg_utilization_ratio = random.uniform(0, 1)
        total_revolving_balance = random.uniform(0, credit_limit)
        open_to_buy = credit_limit - total_revolving_balance
        card_status = random.choice(['Active', 'Inactive'])
        expiry_date = fake.date_between(start_date='+1d', end_date='+5y')

        card_num = random.randint(1000000000, 9999999999)
        while card_num in generated_card_nums:
            card_num = random.randint(1000000000, 9999999999)
        generated_card_nums.add(card_num)
        client_num = random.choice(existing_client_nums) # 1 client can have more than 1 cards
        bank_id = random.choice(existing_bank_ids)
        creditcard = {
            'CardNumber': card_num,
            'BankID': bank_id,
            'Client_num': client_num,
            'Card_category': card_category,
            'Credit_limit': round(credit_limit, 2),
            'Avg_utilization_ratio': round(avg_utilization_ratio, 2),
            'Total_revolving_balance': round(total_revolving_balance, 2),
            'Open_to_buy': round(open_to_buy, 2),
            'Card_Status': card_status,
            'Expiry_Date': expiry_date,
        }
        creditcards.append(creditcard)
    return creditcards

existing_client_nums = fetch_existing_client_nums()
existing_bank_ids = fetch_existing_bank_ids()

creditcard_data = generate_fake_creditcard(existing_client_nums, existing_bank_ids, 7500)


print('### Finished generating CreditCard data. Sample:\n\n')
for creditcard in creditcard_data[:5]:
    print(creditcard)
    print("\n\n")

import csv

csv_file_path = 'csv_files/CreditCardData.csv'

headers = [
    'CardNumber', 'BankID', 'Client_num', 'Card_category', 'Credit_limit',
    'Avg_utilization_ratio', 'Total_revolving_balance', 'Open_to_buy',
    'Card_Status', 'Expiry_Date'
]
with open(csv_file_path, mode='w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for creditcard in creditcard_data:
        writer.writerow(creditcard)

def insert_data_into_table(data):
    for creditcard in data:
        cursor.execute("""
            INSERT INTO CreditCard (
                CardNumber, BankID, Client_num, Card_category, Credit_limit, Avg_utilization_ratio, Total_revolving_balance, Open_to_buy, Card_Status, Expiry_Date, Credit_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            creditcard['CardNumber'], creditcard['BankID'], creditcard['Client_num'], creditcard['Card_category'], creditcard['Credit_limit'], creditcard['Avg_utilization_ratio'], creditcard['Total_revolving_balance'], creditcard['Open_to_buy'], creditcard['Card_Status'], creditcard['Expiry_Date'], creditcard['Credit_score']
        ))

print('### Starting to insert CreditCard data into Postgres DB.\n\n')
insert_data_into_table(creditcard_data)

conn.commit()
print('### Successfully inserted CreditCard data into Postgres DB! \n\n')

cursor.close()
conn.close()
