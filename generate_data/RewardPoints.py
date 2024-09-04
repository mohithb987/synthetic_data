from faker import Faker
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()

import random
from faker import Faker
import random
from datetime import datetime


def fetch_existing_card_nums():
    cursor.execute("SELECT cardnumber FROM CreditCard")
    existing_card_nums = [row[0] for row in cursor.fetchall()]
    return existing_card_nums

def generate_fake_rewards(num_records, card_numbers):
    rewards = []
    generated_reward_ids=set()
    for _ in range(num_records):
        reward_id = random.randint(1, 100000)
        while reward_id in generated_reward_ids:
            reward_id = random.randint(1, 100000)
        generated_reward_ids.add(reward_id)
        card_number = random.choice(card_numbers)
        card_numbers.remove(card_number)
        reward_points_balance = random.randint(0, 10000)
        reward_points_consumed = random.randint(0, reward_points_balance)
        expiry_date = fake.date_time_between(start_date="+1d", end_date="+1y")

        reward = {
            'RewardID': reward_id,
            'CardNumber': card_number,
            'Reward_points_balance': reward_points_balance,
            'Reward_points_consumed': reward_points_consumed,
            'ExpiryDate': expiry_date
        }
        rewards.append(reward)
    return rewards

num_rewards = 7500
card_numbers = fetch_existing_card_nums()

rewards_data = generate_fake_rewards(num_rewards, card_numbers)
for reward in rewards_data[:5]:
    print(reward)


import csv

csv_file_path = 'csv_files/Rewards.csv'

headers = ['RewardID', 'CardNumber', 'Reward_points_balance', 'Reward_points_consumed', 'ExpiryDate']

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()

    for reward in rewards_data:
        writer.writerow(reward)

print('### Finished generating Rewards data. Sample:\n\n')

headers = ['RewardID', 'CardNumber', 'Reward_points_balance', 'Reward_points_consumed', 'ExpiryDate']

def insert_data_into_table(data):
    for reward in data:
        cursor.execute("""
            INSERT INTO Rewards (
                RewardID, CardNumber, Reward_points_balance, Reward_points_consumed, ExpiryDate)
                 VALUES (%s, %s, %s, %s, %s)
        """, (
            reward ['RewardID'], reward ['CardNumber'], reward ['Reward_points_balance'], reward ['Reward_points_consumed'], reward ['ExpiryDate']))

print('### Starting to insert Rewards data into Postgres DB.\n\n')

insert_data_into_table(rewards_data)
conn.commit()
print('### Successfully inserted Rewards data into Postgres DB! \n\n')

cursor.close()
conn.close()
