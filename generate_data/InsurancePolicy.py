from faker import Faker
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()

import random
from faker import Faker
import random
from datetime import datetime


policy_types = [
    'Fraud Protection',
    'Identity Theft Protection',
    'Emergency Medical Coverage',
    'Travel Insurance',
    'Rental Car Insurance',
]

def fetch_existing_card_nums():
    cursor.execute("SELECT cardnumber FROM CreditCard")
    existing_card_nums = [row[0] for row in cursor.fetchall()]
    return existing_card_nums

def fetch_existing_policies():
    cursor.execute("SELECT policyid, policytype FROM policytypes")
    return cursor.fetchall()

def generate_fake_insurance_policies(num_records, card_numbers):
    policies = []
    generated_policy_card_nums = set()
    policies_data = fetch_existing_policies()

    for _ in range(num_records):
        policy = random.choice(policies_data)
        policy_id = policy[0]
        policy_type = policy[1]
        card_number = random.choice(card_numbers)
        while (card_number,policy_id) in generated_policy_card_nums:
            policy = random.choice(policies_data)
            policy_id = policy[0]
            policy_type = policy[1]
            card_number = random.choice(card_numbers)
        generated_policy_card_nums.add((card_number,policy_id))
        policy_start_date = fake.date_time_between(start_date="-1y", end_date="now")
        policy_end_date = fake.date_time_between(start_date="+1d", end_date="+5y")

        policy = {
            'CardNumber': card_number,
            'PolicyID': policy_id,
            'PolicyType': policy_type,
            'Policy_start_date': policy_start_date,
            'Policy_end_date': policy_end_date
        }
        policies.append(policy)
    return policies

num_policies = 10000
card_numbers = fetch_existing_card_nums()

insurance_policies = generate_fake_insurance_policies(num_policies, card_numbers)
for policy in insurance_policies[:5]:
    print(policy)


import csv

csv_file_path = 'csv_files/InsurancePolicy.csv'

headers = ['CardNumber', 'PolicyID',  'PolicyType', 'Policy_start_date', 'Policy_end_date']

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for policy in insurance_policies:
        writer.writerow(policy)

print('### Finished generating InsurancePolicy data. Sample:\n\n')


def insert_data_into_table(data):
    for policy in data:
        cursor.execute("""
            INSERT INTO insurancepolicy (
                    CardNumber, PolicyID,  PolicyType, Policy_start_date, Policy_end_date)
                 VALUES (%s, %s, %s, %s, %s)
        """, (policy['CardNumber'], policy['PolicyID'], policy['PolicyType'], policy['Policy_start_date'], policy['Policy_end_date']))

print('### Starting to insert InsurancePolicy data into Postgres DB.\n\n')

insert_data_into_table(insurance_policies)
conn.commit()
print('### Successfully inserted InsurancePolicy data into Postgres DB! \n\n')

cursor.close()
conn.close()
