from faker import Faker
import random
import datetime

fake = Faker()

def random_date(start_date, end_date):
    return fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')

def generate_phone_number():
    phone_formats = ['###-###-####', '###.###.####', '### ### ####', '(###)###-####']
    return fake.numerify(text=random.choice(phone_formats))

def generate_cardholder_data(num_records):
    cardholders = []
    card_types = ['Visa', 'Mastercard', 'American Express']
    account_statuses = ['Active', 'Closed', 'Suspended']
    employment_statuses = ['Employed', 'Unemployed', 'Self-employed']

    for i in range(num_records):
        cardholder = {
            'Cardholder ID': 'C' + str(fake.random_number(digits=5)),
            'Name': fake.name(),
            'Address': fake.address(),
            'Phone number': generate_phone_number(),
            'Email': fake.email(),
            'Date of Birth': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            'Social Security Number': fake.ssn(),
            'Income Level': random.randint(20000, 150000),
            'Employment Status': random.choice(employment_statuses),
            'Credit Score': random.randint(400, 850),
            'Credit Limit': random.randint(1000, 10000),
            'Account Status': random.choice(account_statuses),
            'Card Type': random.choice(card_types),
            'Card Issue Date': random_date(datetime.date(2015, 1, 1), datetime.date(2023, 1, 1)),
            'Card Expiry Date': random_date(datetime.date(2024, 1, 1), datetime.date(2030, 1, 1))
        }

        cardholders.append(cardholder)
    
    return cardholders


cardholder_data = generate_cardholder_data(100)

for cardholder in cardholder_data[:5]:
    print(cardholder)
    print("\n\n")

def generate_transaction_data(num_records, max_cardholder_id):
    transactions = []
    merchant_categories = ['grocery', 'restaurant', 'travel', 'electronics', 'clothing', 'healthcare']
    transaction_types = ['purchase', 'refund', 'cash advance']
    transaction_statuses = ['approved', 'pending', 'declined']
    for i in range(num_records):
        transaction = {
            'Transaction ID': 'T' + str(fake.random_number(digits=5)),
            'Cardholder ID': random.randint(1, max_cardholder_id),
            'Transaction Date': random_date(datetime.date(2020, 1, 1), datetime.date(2024, 1, 1)),
            'Transaction Amount': round(random.uniform(1.0, 1000.0), 2),
            'Merchant Name': fake.company(),
            'Merchant Category': random.choice(merchant_categories),
            'Transaction Type': random.choice(transaction_types),
            'Transaction Status': random.choice(transaction_statuses)
        }
        transactions.append(transaction)
    
    return transactions

transaction_data = generate_transaction_data(100, len(cardholder_data))

print("\n *** TRANSACTION DATA *** \n")
for transaction in transaction_data[:5]:
    print(transaction)
    print("\n\n")