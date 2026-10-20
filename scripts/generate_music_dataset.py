"""
SoundPulse Streaming Inc. - Synthetic Music Business & User Survey Dataset Generator
Generates realistic simulated data for 240 user survey responses & operations.
Domain: Music Streaming & Digital Audio Business Operations.
"""

import numpy as np
import pandas as pd
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

NUM_RESPONDENTS = 240

first_names = [
    "Aarav", "Liam", "Emma", "Sophia", "Noah", "Olivia", "Lucas", "Mia", "Mateo", "Isabella",
    "Priya", "Ethan", "Ava", "Rohan", "Charlotte", "Amelia", "Harper", "Kabir", "Evelyn", "Abigail",
    "Carlos", "Elena", "Ananya", "Oliver", "Emily", "Sebastian", "Camila", "Vikram", "Luna", "Jackson",
    "Aiden", "Chloe", "Dev", "Penelope", "Layla", "Henry", "Riley", "Diya", "Nora", "Alexander",
    "Gabriel", "Zoey", "Arjun", "Mila", "Daniel", "Hannah", "Aditi", "Matthew", "Kinsley", "Samuel"
]

last_names = [
    "Sharma", "Smith", "Johnson", "Patel", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
    "Verma", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres",
    "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell"
]

regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
region_weights = [0.35, 0.28, 0.25, 0.12]

segments = ["Student", "Young Professional", "Casual Listener", "Tech Audiophile"]

genres = ["Pop", "Hip-Hop", "Rock", "Indie/Alternative", "Electronic/EDM", "R&B/Soul", "Classical/Jazz"]

devices = ["Smartphone (iOS)", "Smartphone (Android)", "Desktop App/Web", "Smart Speaker/Home"]

quality_tiers = ["Standard (160 kbps)", "High (320 kbps)", "Lossless HD (24-bit FLAC)"]

payment_methods = ["Credit Card", "PayPal", "UPI / Digital Wallet", "App Store Billing"]

pain_points = [
    "Too many disruptive audio ads",
    "Poor personalized recommendations",
    "Subscription price too high",
    "App crashes & playback buffering",
    "Missing regional/niche songs",
    "None / Highly Satisfied"
]

rows = []

for i in range(1, NUM_RESPONDENTS + 1):
    user_id = f"SP-{1000 + i}"
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    # Region assignment
    region = np.random.choice(regions, p=region_weights)
    
    # Age & Segment correlation
    segment_prob = [0.30, 0.40, 0.20, 0.10]
    segment = np.random.choice(segments, p=segment_prob)
    
    if segment == "Student":
        age = int(np.random.randint(18, 25))
    elif segment == "Young Professional":
        age = int(np.random.randint(23, 38))
    elif segment == "Tech Audiophile":
        age = int(np.random.randint(26, 52))
    else: # Casual
        age = int(np.random.randint(22, 60))
        
    gender = np.random.choice(["Female", "Male", "Non-Binary"], p=[0.48, 0.48, 0.04])
    
    # Subscription Tier dynamics
    if segment == "Student":
        plan = np.random.choice(["Free (Ad-Supported)", "Student Premium"], p=[0.45, 0.55])
    elif segment == "Tech Audiophile":
        plan = np.random.choice(["Individual Premium", "Family Premium"], p=[0.70, 0.30])
    elif region == "Asia-Pacific":
        plan = np.random.choice(["Free (Ad-Supported)", "Student Premium", "Individual Premium", "Family Premium"], p=[0.55, 0.20, 0.18, 0.07])
    elif region == "North America":
        plan = np.random.choice(["Free (Ad-Supported)", "Student Premium", "Individual Premium", "Family Premium"], p=[0.25, 0.15, 0.42, 0.18])
    else:
        plan = np.random.choice(["Free (Ad-Supported)", "Student Premium", "Individual Premium", "Family Premium"], p=[0.35, 0.15, 0.35, 0.15])
        
    # Pricing setup (in Indian Rupees - INR)
    plan_pricing = {
        "Free (Ad-Supported)": 0.00,
        "Student Premium": 399.00,
        "Individual Premium": 879.00,
        "Family Premium": 1359.00
    }
    monthly_fee = plan_pricing[plan]
    
    # Subscription duration (months)
    tenure_months = int(np.random.geometric(p=0.07))
    tenure_months = max(1, min(tenure_months, 48))
    
    # Primary Device
    if segment == "Tech Audiophile":
        device = np.random.choice(["Desktop App/Web", "Smartphone (iOS)", "Smart Speaker/Home"], p=[0.50, 0.35, 0.15])
    else:
        device = np.random.choice(devices, p=[0.42, 0.38, 0.12, 0.08])
        
    # Preferred Quality
    if segment == "Tech Audiophile" or plan in ["Individual Premium", "Family Premium"]:
        quality = np.random.choice(quality_tiers, p=[0.10, 0.45, 0.45])
    else:
        quality = np.random.choice(quality_tiers, p=[0.60, 0.35, 0.05])
        
    # Payment method
    if plan == "Free (Ad-Supported)":
        payment = "None (Free Tier)"
    elif region == "Asia-Pacific":
        payment = np.random.choice(payment_methods, p=[0.20, 0.10, 0.60, 0.10])
    else:
        payment = np.random.choice(payment_methods, p=[0.55, 0.25, 0.05, 0.15])
        
    # Favorite Genre
    genre_weights = [0.28, 0.22, 0.16, 0.14, 0.10, 0.06, 0.04]
    favorite_genre = np.random.choice(genres, p=genre_weights)
    
    # Listening activity
    if segment == "Student":
        weekly_hours = round(float(np.random.normal(26.0, 7.5)), 1)
    elif segment == "Tech Audiophile":
        weekly_hours = round(float(np.random.normal(31.0, 6.0)), 1)
    elif segment == "Casual Listener":
        weekly_hours = round(float(np.random.normal(11.5, 4.5)), 1)
    else:
        weekly_hours = round(float(np.random.normal(19.0, 5.5)), 1)
    weekly_hours = max(2.5, min(weekly_hours, 55.0))
    
    daily_streams = int(weekly_hours * np.random.uniform(2.1, 2.9))
    daily_streams = max(5, min(daily_streams, 120))
    
    # Skip rate percentage (business friction indicator)
    # Indie & EDM have higher skip rates due to algorithm mismatches
    base_skip = 18.0
    if favorite_genre in ["Indie/Alternative", "Electronic/EDM"]:
        base_skip += 14.0
    if plan == "Free (Ad-Supported)":
        base_skip += 8.0 # forced shuffle / ad frustration skips
    skip_rate = round(float(np.clip(np.random.normal(base_skip, 6.0), 4.0, 62.0)), 1)
    
    # Offline downloads usage
    if plan == "Free (Ad-Supported)":
        offline_downloads = "No"
    else:
        offline_downloads = np.random.choice(["Yes", "No"], p=[0.78, 0.22])
        
    # Ad impressions & Ad revenue (Operations)
    if plan == "Free (Ad-Supported)":
        # Free users see ads proportional to weekly hours
        weekly_ad_impressions = int(weekly_hours * np.random.uniform(2.2, 3.4))
        ad_ctr = round(float(np.random.uniform(0.6, 3.8)), 2)
        # CPM is ~₹1,480 per 1000 impressions + CPC ₹28.00 per click
        monthly_impressions = weekly_ad_impressions * 4.2
        ad_revenue = round(float((monthly_impressions / 1000.0) * 1480.00 + (monthly_impressions * (ad_ctr / 100.0) * 28.00)), 2)
    else:
        weekly_ad_impressions = 0
        ad_ctr = 0.0
        ad_revenue = 0.00
        
    # Licensing royalty costs in INR per stream (avg ~₹0.30/stream, higher for Pop/Hip-hop)
    royalty_rates = {
        "Pop": 0.384,
        "Hip-Hop": 0.360,
        "Rock": 0.312,
        "Indie/Alternative": 0.272,
        "Electronic/EDM": 0.288,
        "R&B/Soul": 0.328,
        "Classical/Jazz": 0.248
    }
    monthly_streams = daily_streams * 30
    licensing_cost = round(float(monthly_streams * royalty_rates[favorite_genre]), 2)
    
    # Total operational revenue & gross profit
    total_rev = round(monthly_fee + ad_revenue, 2)
    gross_profit = round(total_rev - licensing_cost, 2)
    
    # Primary Pain Point & Churn Drivers
    if plan == "Free (Ad-Supported)" and weekly_ad_impressions > 55:
        pain_point = "Too many disruptive audio ads"
    elif device == "Smartphone (Android)" and quality == "Lossless HD (24-bit FLAC)":
        pain_point = np.random.choice(["App crashes & playback buffering", "Too many disruptive audio ads", "None / Highly Satisfied"], p=[0.60, 0.20, 0.20])
    elif skip_rate > 36.0:
        pain_point = "Poor personalized recommendations"
    elif segment == "Student" and plan == "Individual Premium":
        pain_point = "Subscription price too high"
    else:
        pain_point = np.random.choice(pain_points, p=[0.20, 0.25, 0.15, 0.15, 0.08, 0.17])
        
    # Satisfaction score (1-5) and NPS (0-10)
    if pain_point in ["Too many disruptive audio ads", "App crashes & playback buffering"]:
        satisfaction = int(np.random.choice([1, 2, 3], p=[0.40, 0.45, 0.15]))
        nps = int(np.random.choice([1, 2, 3, 4, 5, 6], p=[0.25, 0.25, 0.20, 0.15, 0.10, 0.05]))
    elif pain_point == "None / Highly Satisfied":
        satisfaction = int(np.random.choice([4, 5], p=[0.25, 0.75]))
        nps = int(np.random.choice([8, 9, 10], p=[0.15, 0.45, 0.40]))
    else:
        satisfaction = int(np.random.choice([2, 3, 4], p=[0.25, 0.50, 0.25]))
        nps = int(np.random.choice([4, 5, 6, 7, 8], p=[0.15, 0.25, 0.30, 0.20, 0.10]))
        
    # Support tickets
    if pain_point == "App crashes & playback buffering":
        support_tickets = int(np.random.choice([2, 3, 4, 5], p=[0.30, 0.40, 0.20, 0.10]))
    elif pain_point == "Subscription price too high" or satisfaction <= 2:
        support_tickets = int(np.random.choice([1, 2, 3], p=[0.55, 0.35, 0.10]))
    else:
        support_tickets = int(np.random.choice([0, 1], p=[0.82, 0.18]))
        
    # Churn status & Risk score
    # High churn risk if satisfaction <= 2, skip_rate > 35%, or heavy ads
    churn_score = 0.10
    if satisfaction <= 2:
        churn_score += 0.42
    if skip_rate > 35:
        churn_score += 0.20
    if support_tickets >= 2:
        churn_score += 0.18
    if plan == "Free (Ad-Supported)":
        churn_score += 0.12
    if plan in ["Individual Premium", "Family Premium"] and tenure_months > 12:
        churn_score -= 0.22
    churn_score = round(float(np.clip(churn_score, 0.04, 0.96)), 2)
    
    # Binary Churn Status
    is_churned = "Yes" if churn_score >= 0.62 else "No"
    
    rows.append({
        "User_ID": user_id,
        "Customer_Name": name,
        "Age": age,
        "Gender": gender,
        "Location_Region": region,
        "User_Segment": segment,
        "Subscription_Tier": plan,
        "Monthly_Subscription_Fee_INR": monthly_fee,
        "Subscription_Duration_Months": tenure_months,
        "Primary_Device": device,
        "Preferred_Audio_Quality": quality,
        "Payment_Method": payment,
        "Favorite_Genre": favorite_genre,
        "Weekly_Listening_Hours": weekly_hours,
        "Daily_Stream_Count": daily_streams,
        "Monthly_Estimated_Streams": monthly_streams,
        "Skip_Rate_Pct": skip_rate,
        "Offline_Downloads_Used": offline_downloads,
        "Weekly_Ad_Impressions": weekly_ad_impressions,
        "Ad_Click_Rate_Pct": ad_ctr,
        "Monthly_Ad_Revenue_INR": ad_revenue,
        "Monthly_Total_Revenue_INR": total_rev,
        "Monthly_Licensing_Cost_INR": licensing_cost,
        "Monthly_Gross_Margin_INR": gross_profit,
        "Customer_Support_Tickets": support_tickets,
        "Satisfaction_Rating": satisfaction,
        "NPS_Score": nps,
        "Primary_Pain_Point": pain_point,
        "Churn_Risk_Score": churn_score,
        "Churn_Status": is_churned
    })

df = pd.DataFrame(rows)

# Save Raw Datasets
raw_csv_path = "data/raw_music_user_responses.csv"
raw_xlsx_path = "data/raw_music_user_responses.xlsx"

df.to_csv(raw_csv_path, index=False)
df.to_excel(raw_xlsx_path, index=False, engine="openpyxl")

print(f"Generated {len(df)} records successfully.")
print(f"Saved: {raw_csv_path}")
print(f"Saved: {raw_xlsx_path}")
print("\nKey summary metrics:")
print(f"Total Active Users: {(df['Churn_Status'] == 'No').sum()} | Churned: {(df['Churn_Status'] == 'Yes').sum()}")
print(f"Average Monthly Gross Margin: Rs. {df['Monthly_Gross_Margin_INR'].mean():.2f}")
print(f"Average Weekly Listening Hours: {df['Weekly_Listening_Hours'].mean():.1f} hrs")
print(f"Overall Churn Rate: {(df['Churn_Status'] == 'Yes').mean() * 100:.1f}%")
