"""
SoundPulse Streaming Inc. - Preprocessing, Feature Engineering & Star Schema ETL Script
Extracts raw survey/operational data, cleans and validates, engineers analytical features,
and loads dimension and fact tables for Data Warehousing & Power BI / Tableau consumption.
"""

import pandas as pd
import numpy as np
import os

RAW_PATH = "data/raw_music_user_responses.csv"
CLEANED_PATH = "data/cleaned_music_data.csv"
STAR_SCHEMA_DIR = "data/star_schema"

os.makedirs(STAR_SCHEMA_DIR, exist_ok=True)

print("Starting ETL & Preprocessing Workflow...")
df = pd.read_csv(RAW_PATH)
print(f"Loaded raw dataset with {df.shape[0]} rows and {df.shape[1]} columns.")

# 1. Data Cleaning & Validation Checks
assert df.isnull().sum().sum() == 0, "Null values detected in dataset!"
assert (df['Age'] >= 18).all() and (df['Age'] <= 70).all(), "Age values outside normal range!"
assert (df['Satisfaction_Rating'].between(1, 5)).all(), "Satisfaction rating out of bounds!"
assert (df['NPS_Score'].between(0, 10)).all(), "NPS score out of bounds!"

# 2. Feature Engineering
# Age groups
bins_age = [17, 24, 34, 49, 100]
labels_age = ["18-24 (Gen Z)", "25-34 (Young Professionals)", "35-49 (Mid-Career)", "50+ (Mature)"]
df['Age_Group'] = pd.cut(df['Age'], bins=bins_age, labels=labels_age)

# Listening engagement tier
bins_eng = [0, 12, 25, 100]
labels_eng = ["Low (<12 hrs/wk)", "Medium (12-25 hrs/wk)", "High (25+ hrs/wk)"]
df['Engagement_Tier'] = pd.cut(df['Weekly_Listening_Hours'], bins=bins_eng, labels=labels_eng)

# NPS categorization (Industry standard: 0-6 Detractor, 7-8 Passive, 9-10 Promoter)
def categorize_nps(score):
    if score <= 6:
        return "Detractor"
    elif score <= 8:
        return "Passive"
    else:
        return "Promoter"

df['NPS_Category'] = df['NPS_Score'].apply(categorize_nps)

# Binary Churn indicator for aggregations in BI tools
df['Churn_Binary'] = (df['Churn_Status'] == 'Yes').astype(int)

# Ad Fatigue Index (Ad impressions per listening hour)
df['Ad_Fatigue_Index'] = np.where(
    df['Weekly_Listening_Hours'] > 0,
    np.round(df['Weekly_Ad_Impressions'] / df['Weekly_Listening_Hours'], 2),
    0.0
)

# Customer Lifetime Value (CLV estimated in INR)
df['Customer_Lifetime_Value_INR'] = np.round(df['Monthly_Total_Revenue_INR'] * df['Subscription_Duration_Months'], 2)

# Profitability flag
df['Is_Profitable'] = (df['Monthly_Gross_Margin_INR'] > 0).astype(int)

# Save Cleaned Master Dataset
df.to_csv(CLEANED_PATH, index=False)
print(f"Cleaned master dataset saved to: {CLEANED_PATH}")

# ==============================================================================
# 3. STAR SCHEMA DIMENSIONAL MODELING
# ==============================================================================

# A. Dim_User
dim_user = df[['User_ID', 'Customer_Name', 'Age', 'Age_Group', 'Gender', 'Location_Region', 'User_Segment']].drop_duplicates().reset_index(drop=True)
dim_user['User_Key'] = dim_user.index + 1
dim_user = dim_user[['User_Key', 'User_ID', 'Customer_Name', 'Age', 'Age_Group', 'Gender', 'Location_Region', 'User_Segment']]
dim_user.to_csv(f"{STAR_SCHEMA_DIR}/Dim_User.csv", index=False)
print(f"Created Dim_User: {len(dim_user)} rows")

# B. Dim_Subscription
sub_plans = [
    {
        "Subscription_Tier": "Free (Ad-Supported)",
        "Base_Monthly_Fee_INR": 0.00,
        "Target_Audience": "Mass Casual & Students",
        "Ad_Supported": "Yes",
        "Audio_Quality_Limit": "Standard (160 kbps)",
        "Offline_Downloads_Allowed": "No",
        "Max_Streams": 1
    },
    {
        "Subscription_Tier": "Student Premium",
        "Base_Monthly_Fee_INR": 399.00,
        "Target_Audience": "Verified University Students",
        "Ad_Supported": "No",
        "Audio_Quality_Limit": "High (320 kbps)",
        "Offline_Downloads_Allowed": "Yes",
        "Max_Streams": 1
    },
    {
        "Subscription_Tier": "Individual Premium",
        "Base_Monthly_Fee_INR": 879.00,
        "Target_Audience": "Individual Audiophiles & Professionals",
        "Ad_Supported": "No",
        "Audio_Quality_Limit": "Lossless HD (24-bit FLAC)",
        "Offline_Downloads_Allowed": "Yes",
        "Max_Streams": 1
    },
    {
        "Subscription_Tier": "Family Premium",
        "Base_Monthly_Fee_INR": 1359.00,
        "Target_Audience": "Households up to 6 members",
        "Ad_Supported": "No",
        "Audio_Quality_Limit": "Lossless HD (24-bit FLAC)",
        "Offline_Downloads_Allowed": "Yes",
        "Max_Streams": 6
    }
]
dim_subscription = pd.DataFrame(sub_plans)
dim_subscription['Subscription_Key'] = dim_subscription.index + 1
cols = ['Subscription_Key'] + [c for c in dim_subscription.columns if c != 'Subscription_Key']
dim_subscription = dim_subscription[cols]
dim_subscription.to_csv(f"{STAR_SCHEMA_DIR}/Dim_Subscription.csv", index=False)
print(f"Created Dim_Subscription: {len(dim_subscription)} rows")

# C. Dim_Device
device_data = [
    {"Primary_Device": "Smartphone (iOS)", "Platform_Type": "Mobile OS", "Manufacturer": "Apple", "Lossless_Hardware_Support": "High"},
    {"Primary_Device": "Smartphone (Android)", "Platform_Type": "Mobile OS", "Manufacturer": "Various (Samsung, Xiaomi, Pixel)", "Lossless_Hardware_Support": "Medium/Fragmented"},
    {"Primary_Device": "Desktop App/Web", "Platform_Type": "Desktop / PC", "Manufacturer": "Windows / MacOS / Linux", "Lossless_Hardware_Support": "Very High (DAC support)"},
    {"Primary_Device": "Smart Speaker/Home", "Platform_Type": "Connected IoT", "Manufacturer": "Amazon Echo, Google Nest, Sonos", "Lossless_Hardware_Support": "Moderate"}
]
dim_device = pd.DataFrame(device_data)
dim_device['Device_Key'] = dim_device.index + 1
cols = ['Device_Key'] + [c for c in dim_device.columns if c != 'Device_Key']
dim_device = dim_device[cols]
dim_device.to_csv(f"{STAR_SCHEMA_DIR}/Dim_Device.csv", index=False)
print(f"Created Dim_Device: {len(dim_device)} rows")

# D. Dim_Genre
genre_data = [
    {"Favorite_Genre": "Pop", "Royalty_Rate_Per_Stream_INR": 0.384, "Licensing_Complexity": "High (Major Labels)", "Average_Song_Length_Sec": 195},
    {"Favorite_Genre": "Hip-Hop", "Royalty_Rate_Per_Stream_INR": 0.360, "Licensing_Complexity": "High (Sample Clearances)", "Average_Song_Length_Sec": 180},
    {"Favorite_Genre": "Rock", "Royalty_Rate_Per_Stream_INR": 0.312, "Licensing_Complexity": "Medium (Catalogue Heritage)", "Average_Song_Length_Sec": 240},
    {"Favorite_Genre": "Indie/Alternative", "Royalty_Rate_Per_Stream_INR": 0.272, "Licensing_Complexity": "Low/Direct (Indie Distributors)", "Average_Song_Length_Sec": 215},
    {"Favorite_Genre": "Electronic/EDM", "Royalty_Rate_Per_Stream_INR": 0.288, "Licensing_Complexity": "Medium (Independent/Club)", "Average_Song_Length_Sec": 230},
    {"Favorite_Genre": "R&B/Soul", "Royalty_Rate_Per_Stream_INR": 0.328, "Licensing_Complexity": "Medium/High", "Average_Song_Length_Sec": 210},
    {"Favorite_Genre": "Classical/Jazz", "Royalty_Rate_Per_Stream_INR": 0.248, "Licensing_Complexity": "Low (Public Domain / Specialized)", "Average_Song_Length_Sec": 390}
]
dim_genre = pd.DataFrame(genre_data)
dim_genre['Genre_Key'] = dim_genre.index + 1
cols = ['Genre_Key'] + [c for c in dim_genre.columns if c != 'Genre_Key']
dim_genre = dim_genre[cols]
dim_genre.to_csv(f"{STAR_SCHEMA_DIR}/Dim_Genre.csv", index=False)
print(f"Created Dim_Genre: {len(dim_genre)} rows")

# E. Dim_Date (Snapshot calendar dimension)
dates_data = []
# Create a quarterly calendar dimension for operational reporting
dates_data.append({"Date_Key": 20261014, "Full_Date": "2026-10-14", "Day": 14, "Month_Name": "October", "Quarter": "Q4", "Year": 2026, "Fiscal_Period": "FY2026-Q4"})
dim_date = pd.DataFrame(dates_data)
dim_date.to_csv(f"{STAR_SCHEMA_DIR}/Dim_Date.csv", index=False)
print(f"Created Dim_Date: {len(dim_date)} rows")

# F. Fact_Music_Operations
# Merge surrogate keys into fact table
fact = df.copy()

# Merge User_Key
fact = fact.merge(dim_user[['User_ID', 'User_Key']], on='User_ID', how='left')

# Merge Subscription_Key
fact = fact.merge(dim_subscription[['Subscription_Tier', 'Subscription_Key']], on='Subscription_Tier', how='left')

# Merge Device_Key
fact = fact.merge(dim_device[['Primary_Device', 'Device_Key']], on='Primary_Device', how='left')

# Merge Genre_Key
fact = fact.merge(dim_genre[['Favorite_Genre', 'Genre_Key']], on='Favorite_Genre', how='left')

fact['Date_Key'] = 20261014
fact['Fact_Key'] = fact.index + 1

fact_columns = [
    'Fact_Key',
    'User_Key',
    'Subscription_Key',
    'Device_Key',
    'Genre_Key',
    'Date_Key',
    # Degenerate Dimensions
    'Payment_Method',
    'Preferred_Audio_Quality',
    'Offline_Downloads_Used',
    'Primary_Pain_Point',
    'NPS_Category',
    'Engagement_Tier',
    # Numerical Additive & Semi-Additive Measures
    'Weekly_Listening_Hours',
    'Daily_Stream_Count',
    'Monthly_Estimated_Streams',
    'Skip_Rate_Pct',
    'Weekly_Ad_Impressions',
    'Ad_Click_Rate_Pct',
    'Monthly_Ad_Revenue_INR',
    'Monthly_Subscription_Fee_INR',
    'Monthly_Total_Revenue_INR',
    'Monthly_Licensing_Cost_INR',
    'Monthly_Gross_Margin_INR',
    'Customer_Support_Tickets',
    'Satisfaction_Rating',
    'NPS_Score',
    'Churn_Risk_Score',
    'Churn_Binary',
    'Customer_Lifetime_Value_INR',
    'Ad_Fatigue_Index',
    'Is_Profitable'
]

fact_table = fact[fact_columns]
fact_table.to_csv(f"{STAR_SCHEMA_DIR}/Fact_Music_Operations.csv", index=False)
print(f"Created Fact_Music_Operations: {len(fact_table)} rows and {fact_table.shape[1]} columns.")
print("Star Schema generation complete! All tables exported to data/star_schema/.")
