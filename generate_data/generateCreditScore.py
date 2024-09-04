import pandas as pd
import numpy as np

data = pd.read_csv("csv_files/CreditCardData.csv")
score_ranges = {
    "Excellent": (750, 850),
    "Good": (700, 749),
    "Fair": (650, 699),
    "Poor": (300, 649)
}

def calculate_credit_score(card):
    weights = {
        "utilization_ratio": 0.4,
        "revolving_balance": 0.3,
        "card_category": 0.3
    }
    score = (
            weights["utilization_ratio"]*(1 - card["Avg_utilization_ratio"]) +
            weights["revolving_balance"]*(1 - card["Total_revolving_balance"]) +
            weights["card_category"]*(1 if card["Card_category"] == "Premium" else 0.5)
    )

    return score

data["Credit_Score"] = data.apply(calculate_credit_score, axis=1)
client_scores = data.groupby("Client_num")["Credit_Score"].mean()

normalized_scores = (client_scores - min(client_scores))/(max(client_scores) - min(client_scores))
score_categories = pd.cut(normalized_scores * 100, bins=[0, 25, 50, 75, 100], labels=["Poor", "Fair", "Good", "Excellent"])
data["Credit_Score_Category"] = data["Client_num"].map(score_categories)

def generate_random_score(category):
    lower, upper = score_ranges[category]
    return np.random.uniform(lower, upper)

data["Random_Credit_Score"] = data["Credit_Score_Category"].apply(generate_random_score)

data.to_csv("csv_files/creditCard_with_random_scores.csv", index=False)
print(data)
