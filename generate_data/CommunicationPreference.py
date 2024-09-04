import random
from faker import Faker
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()

preference_types = ['Marketing', 'Support']

def fetch_existing_client_nums():
    cursor.execute("SELECT Client_num FROM Client")
    existing_client_nums = [row[0] for row in cursor.fetchall()]
    return existing_client_nums

def generate_fake_preferences(num_records, client_nums):
    preferences = []
    generated_preference_ids = set()
    for _ in range(num_records):
        preference_id = random.randint(1, 1000000)
        while preference_id in generated_preference_ids:
            preference_id = random.randint(1, 1000000)
        generated_preference_ids.add(preference_id)
        client_num = random.choice(client_nums)
        client_nums.remove(client_num)
        preference_type = random.choice(preference_types)
        email_subscription = random.choice([True, False])
        sms_subscription = random.choice([True, False])
        phone_call_subscription = random.choice([True, False])

        preference = {
            'PreferenceID': preference_id,
            'Client_num': client_num,
            'PreferenceType': preference_type,
            'EmailSubscription': email_subscription,
            'SMSSubscription': sms_subscription,
            'PhoneCallSubscription': phone_call_subscription
        }
        preferences.append(preference)
    return preferences

num_preferences = 5000
existing_client_nums = fetch_existing_client_nums()

preferences_data = generate_fake_preferences(num_preferences, existing_client_nums)
for preference in preferences_data[:5]:
    print(preference)


import csv

csv_file_path = 'csv_files/CommunicationPreference.csv'

headers = [
    'PreferenceID', 'Client_num', 'PreferenceType', 'EmailSubscription','SMSSubscription','PhoneCallSubscription'
]

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for preference in preferences_data:
        writer.writerow(preference)

print('### Finished generating CommunicationPreferences data. Sample:\n\n')


def insert_data_into_table(data):
    for preference in data:
        cursor.execute("""
            INSERT INTO CommunicationPreference (
                PreferenceID, Client_num, PreferenceType, EmailSubscription,SMSSubscription,PhoneCallSubscription
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            preference['PreferenceID'], preference['Client_num'], preference['PreferenceType'], preference['EmailSubscription'], preference['SMSSubscription'], preference['PhoneCallSubscription']
        ))

print('### Starting to insert CommunicationPreferences data into Postgres DB.\n\n')
insert_data_into_table(preferences_data)
conn.commit()
print('### Successfully inserted CommunicationPreferences data into Postgres DB! \n\n')

cursor.close()
conn.close()