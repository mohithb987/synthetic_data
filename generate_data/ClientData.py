from faker import Faker
import random
import datetime
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()

def random_date(start_date, end_date):
    return fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')

def generate_phone_number():
    return fake.numerify(text='(###) ###-####')

def generate_clients_data(num_records):
    clients = []
    generated_client_nums = set()
    for i in range(num_records):
        marital_status = random.choice(['Married', 'Single'])
        if marital_status == 'Married':
            dependent_count = random.randint(1, 4)
        elif marital_status == 'Single':
            dependent_count = random.randint(0, 2)
        else:
            dependent_count = random.randint(0, 3)

        income_category = random.choice(['Low', 'Medium', 'High'])
        if dependent_count >= 2:
            income_category = random.choice(['Medium', 'High'])

        client_num = random.randint(10000000, 99999999)
        while client_num in generated_client_nums:
            client_num = random.randint(10000000, 99999999)

        generated_client_nums.add(client_num)
        client = {
            'Client_num': client_num,
            'Customer_name': fake.name(),
            'Customer_age': random.randint(20, 70),
            'Gender': random.choice(['Male', 'Female']),
            'Dependent_count': dependent_count,
            'Education_level': random.choice(['High School', 'Bachelor\'s', 'Master\'s', 'Doctorate']),
            'Marital_status': marital_status,
            'Income_category': income_category,
            'Email': fake.email(),
            'Contact_number': generate_phone_number()
        }

        clients.append(client)
    
    return clients


clients_data = generate_clients_data(5000)

print('### Finished generating Clients data. Sample:\n\n')
for client in clients_data[:5]:
    print(client)
    print("\n\n")

import csv

csv_file_path = 'csv_files/ClientsData.csv'

headers = [
    'Client_num', 'Customer_name', 'Customer_age', 'Gender', 'Dependent_count',
    'Education_level', 'Marital_status', 'Income_category',
    'Email', 'Contact_number'
]

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)

    writer.writeheader()

    for client in clients_data:
        writer.writerow(client)

def insert_data_into_table(data):
    for client in data:
        cursor.execute("""
            INSERT INTO Client (
                Client_num, Customer_name, Customer_age, Gender, Dependent_count,
                Education_level, Marital_status, Income_category,
                Email, Contact_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            client['Client_num'], client['Customer_name'], client['Customer_age'], client['Gender'],
            client['Dependent_count'], client['Education_level'], client['Marital_status'],
            client['Income_category'], client['Email'], client['Contact_number']
        ))

print('### Starting to insert Clients data into Postgres DB.\n\n')
insert_data_into_table(clients_data)
conn.commit()
print('### Successfully inserted Clients data into Postgres DB! \n\n')

cursor.close()
conn.close()
