import random

from faker import Faker
from DbConnect import db_connect

conn = db_connect()
cursor = conn.cursor()
fake = Faker()

import random
from faker import Faker
import random
from datetime import datetime


issue_types = ['Technical', 'Billing', 'General']
statuses = ['Open', 'In Progress', 'Closed']

def fetch_existing_client_nums():
    cursor.execute("SELECT Client_num FROM Client")
    existing_client_nums = [row[0] for row in cursor.fetchall()]
    return existing_client_nums

def generate_fake_support_tickets(num_records, client_nums):
    support_tickets = []
    generated_support_ticket_ids = set()
    for _ in range(num_records):
        support_ticket_id = random.randint(1, 1000000)
        while support_ticket_id in generated_support_ticket_ids:
            support_ticket_id = random.randint(1, 1000000)
        generated_support_ticket_ids.add(support_ticket_id)
        client_num = random.choice(client_nums)
        issue_type = random.choice(issue_types)
        status = random.choice(statuses)
        support_ticket_date = fake.date_time_between(start_date="-1y", end_date="now")
        assigned_to = fake.name()

        support_ticket = {
            'SupportTicketID': support_ticket_id,
            'Client_num': client_num,
            'IssueType': issue_type,
            'Status': status,
            'SupportTicket_date': support_ticket_date,
            'Assigned_to': assigned_to
        }
        support_tickets.append(support_ticket)
    return support_tickets

num_support_tickets = 10000

existing_client_nums = fetch_existing_client_nums()
support_tickets_data = generate_fake_support_tickets(num_support_tickets, existing_client_nums)
for support_ticket in support_tickets_data[:5]:
    print(support_ticket)

import csv

csv_file_path = 'csv_files/CustomerSupport.csv'
headers = [
    'SupportTicketID', 'Client_num', 'IssueType', 'Status','SupportTicket_date','Assigned_to'
]

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()

    for support_ticket in support_tickets_data:
        writer.writerow(support_ticket)

print('### Finished generating CustomerSupport data. Sample:\n\n')


def insert_data_into_table(data):
    for support_ticket in data:
        cursor.execute("""
            INSERT INTO CustomerSupport (
                SupportTicketID, Client_num, IssueType, Status,SupportTicket_date,Assigned_to
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            support_ticket['SupportTicketID'], support_ticket['Client_num'], support_ticket['IssueType'], support_ticket['Status'], support_ticket['SupportTicket_date'], support_ticket['Assigned_to']
        ))

print('### Starting to insert CustomerSupport data into Postgres DB.\n\n')

insert_data_into_table(support_tickets_data)
conn.commit()
print('### Successfully inserted CustomerSupport data into Postgres DB! \n\n')

cursor.close()
conn.close()
