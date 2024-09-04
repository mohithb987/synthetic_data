import pandas as pd

client_data = pd.read_csv("csv_files/ClientsData copy.csv")
credit_data = pd.read_csv("csv_files/creditCard_with_random_scores.csv")
merged_data = pd.merge( client_data,credit_data[['Client_num', 'Random_Credit_Score']], on="Client_num", how="left")
merged_data.to_csv("client_with_credit_scores.csv", index=False)