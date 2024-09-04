from faker import Faker
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()




def generate_fake_policies():
    insurance_policy_types = [
        {'PolicyID':1, 'PolicyType': 'Fraud Protection', 'Coverage_amount': 10000, 'Premium_amount': 50},
        {'PolicyID':2, 'PolicyType': 'Identity Theft Protection', 'Coverage_amount': 15000, 'Premium_amount': 75},
        {'PolicyID':3, 'PolicyType': 'Emergency Medical Coverage', 'Coverage_amount': 20000, 'Premium_amount': 100},
        {'PolicyID':4, 'PolicyType': 'Travel Insurance', 'Coverage_amount': 25000, 'Premium_amount': 125},
        {'PolicyID':5, 'PolicyType': 'Rental Car Insurance', 'Coverage_amount': 5000, 'Premium_amount': 25}
    ]
    return insurance_policy_types


insurance_policies = generate_fake_policies()
for policy in insurance_policies[:5]:
    print(policy)


import csv

csv_file_path = 'csv_files/PolicyTypes.csv'

headers = ['PolicyID', 'PolicyType', 'Coverage_amount', 'Premium_amount']

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()

    for policy in insurance_policies:
        writer.writerow(policy)

print('### Finished generating PolicyTypes data. Sample:\n\n')


def insert_data_into_table(data):
    for policy in data:
        cursor.execute("""
            INSERT INTO PolicyTypes (
                   PolicyID, PolicyType, Coverage_amount, Premium_amount)
                 VALUES (%s,%s, %s, %s)
        """, (policy['PolicyID'], policy['PolicyType'], policy['Coverage_amount'], policy['Premium_amount']))

print('### Starting to insert PolicyTypes data into Postgres DB.\n\n')

insert_data_into_table(insurance_policies)
conn.commit()
print('### Successfully inserted PolicyTypes data into Postgres DB! \n\n')

cursor.close()
conn.close()
