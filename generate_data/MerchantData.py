import random
from faker import Faker
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()

merchant_categories = ['Electronics', 'Grocery', 'Clothing', 'Restaurant', 'Entertainment', 'Furniture']

def generate_fake_merchants(num_records):
    merchants = []
    generated_merchant_ids = set()
    for _ in range(num_records):
        name = fake.company()
        category = random.choice(merchant_categories)
        location = fake.address()
        merchant_id = random.randint(1000, 9999)
        while merchant_id in generated_merchant_ids:
            merchant_id = random.randint(1000, 9999)
        generated_merchant_ids.add(merchant_id)

        merchant = {
            'MerchantID': merchant_id,
            'Name': name,
            'Category': category,
            'Location': location
        }
        merchants.append(merchant)
    return merchants

num_merchants = 600
merchants_data = generate_fake_merchants(num_merchants)
for merchant in merchants_data:
    print(merchant)


import csv

csv_file_path = 'csv_files/MerchantsData.csv'
headers = [
    'MerchantID', 'Name', 'Category', 'Location'
]

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for merchant in merchants_data:
        writer.writerow(merchant)

print('### Finished generating Merchants data. Sample:\n\n')
for merchant in merchants_data:
    print(merchant)
    print("\n\n")


def insert_data_into_table(data):
    for merchant in merchants_data:
        cursor.execute("""
            INSERT INTO Merchant (
                MerchantID, Name, Category, Location
            ) VALUES (%s, %s, %s, %s)
        """, (
            merchant['MerchantID'], merchant['Name'], merchant['Category'], merchant['Location']
        ))

print('### Starting to insert Merchants data into Postgres DB.\n\n')
# Insert data into the table
insert_data_into_table(merchants_data)

# Commit your changes
conn.commit()
print('### Successfully inserted Merchants data into Postgres DB! \n\n')

# Close the cursor and connection
cursor.close()
conn.close()
