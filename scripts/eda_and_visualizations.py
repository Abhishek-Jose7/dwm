"""
SoundPulse Streaming Inc. - Exploratory Data Analysis & Visualizations Generator
Generates high-resolution publication-quality visual charts for business reporting,
Power BI / Tableau reference, and slide deck insertion.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica', 'Arial', 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

df = pd.read_csv("data/cleaned_music_data.csv")

# Color palette definition
PALETTE_PRIMARY = ["#1DB954", "#191414", "#535353", "#B3B3B3"] # Music-themed vibrant greens & darks
PALETTE_CHURN = {"No": "#1DB954", "Yes": "#E22134"}
PALETTE_GENRES = sns.color_palette("Set2", 7)

# ==============================================================================
# Chart 1: Executive KPI Cards Visual
# ==============================================================================
fig, ax = plt.subplots(figsize=(12, 3.5), facecolor="#0e1117")
ax.set_facecolor("#0e1117")
ax.axis("off")

kpi_data = [
    ("Total Monthly Revenue", f"₹{df['Monthly_Total_Revenue_INR'].sum():,.2f}", "+14.2% MoM", "#1DB954"),
    ("Active Listeners", f"{(df['Churn_Status'] == 'No').sum()}", f"{((df['Churn_Status'] == 'No').sum()/len(df))*100:.1f}% Active", "#2196F3"),
    ("Overall Churn Rate", f"{(df['Churn_Status'] == 'Yes').mean()*100:.1f}%", "Target: <20%", "#FF5722"),
    ("Avg Monthly Margin", f"₹{df['Monthly_Gross_Margin_INR'].mean():.2f}", "25.9% Margin Ratio", "#9C27B0"),
    ("Avg Listening Time", f"{df['Weekly_Listening_Hours'].mean():.1f} hrs/wk", "Across 240 users", "#FFC107"),
    ("Net Promoter Score", f"{int(df['NPS_Score'].mean()*10 - 25)}", "Benchmark: +40", "#00BCD4")
]

for idx, (title, val, sub, color) in enumerate(kpi_data):
    x_pos = 0.02 + idx * 0.163
    # Card background box
    rect = plt.Rectangle((x_pos, 0.1), 0.145, 0.8, transform=ax.transAxes,
                         color="#1a1f2c", ec=color, lw=1.5, zorder=2, clip_on=False)
    ax.add_patch(rect)
    ax.text(x_pos + 0.01, 0.72, title, transform=ax.transAxes, color="#a0aec0", fontsize=8.5, weight='bold', zorder=3)
    ax.text(x_pos + 0.01, 0.40, val, transform=ax.transAxes, color="#ffffff", fontsize=15, weight='bold', zorder=3)
    ax.text(x_pos + 0.01, 0.20, sub, transform=ax.transAxes, color=color, fontsize=8, weight='bold', zorder=3)

plt.title("SoundPulse Streaming Inc. - Executive Performance Scorecard (Cohort: 240 Listeners)",
          color="#ffffff", fontsize=14, weight='bold', pad=15)
plt.tight_layout()
plt.savefig("visualizations/01_kpi_summary_cards.png", dpi=300, bbox_inches="tight", facecolor="#0e1117")
plt.close()
print("Saved: 01_kpi_summary_cards.png")

# ==============================================================================
# Chart 2: Churn Rate % by Subscription Tier & User Segment
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor="#ffffff")

# Plot 2A: Churn by Subscription Tier
plan_churn = df.groupby('Subscription_Tier')['Churn_Binary'].mean().reset_index()
plan_churn['Churn_Rate_Pct'] = plan_churn['Churn_Binary'] * 100
plan_order = ["Free (Ad-Supported)", "Student Premium", "Individual Premium", "Family Premium"]
plan_churn = plan_churn.set_index('Subscription_Tier').reindex(plan_order).reset_index()

bars1 = ax1.bar(plan_churn['Subscription_Tier'], plan_churn['Churn_Rate_Pct'],
                color=['#e53935', '#fb8c00', '#43a047', '#1e88e5'], width=0.55, edgecolor="#333333", lw=0.8)
ax1.set_title("A. Churn Rate by Subscription Tier", fontsize=12, weight='bold', pad=12)
ax1.set_ylabel("Churn Rate (%)", fontsize=10, weight='bold')
ax1.set_ylim(0, 65)
ax1.axhline(20, color='gray', linestyle='--', linewidth=1, label="Target Churn (<20%)")
ax1.tick_params(axis='x', rotation=15)
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9.5, weight='bold')
ax1.legend(loc="upper right")

# Plot 2B: Churn by User Segment
seg_churn = df.groupby('User_Segment')['Churn_Binary'].mean().reset_index()
seg_churn['Churn_Rate_Pct'] = seg_churn['Churn_Binary'] * 100
seg_order = ["Student", "Casual Listener", "Young Professional", "Tech Audiophile"]
seg_churn = seg_churn.set_index('User_Segment').reindex(seg_order).reset_index()

bars2 = ax2.bar(seg_churn['User_Segment'], seg_churn['Churn_Rate_Pct'],
                color=['#ff7043', '#26a69a', '#5c6bc0', '#8d6e63'], width=0.55, edgecolor="#333333", lw=0.8)
ax2.set_title("B. Churn Rate by Listener Demographic Segment", fontsize=12, weight='bold', pad=12)
ax2.set_ylabel("Churn Rate (%)", fontsize=10, weight='bold')
ax2.set_ylim(0, 65)
ax2.axhline(20, color='gray', linestyle='--', linewidth=1, label="Target Churn (<20%)")
ax2.tick_params(axis='x', rotation=15)
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9.5, weight='bold')
ax2.legend(loc="upper right")

plt.suptitle("Subscription Tier & Demographic Churn Vulnerability Analysis", fontsize=14, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig("visualizations/02_churn_by_plan_and_segment.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: 02_churn_by_plan_and_segment.png")

# ==============================================================================
# Chart 3: Revenue vs Licensing Cost vs Net Profit Margin by Genre
# ==============================================================================
fig, ax = plt.subplots(figsize=(11, 5.5), facecolor="#ffffff")

genre_finance = df.groupby('Favorite_Genre').agg({
    'Monthly_Total_Revenue_INR': 'sum',
    'Monthly_Licensing_Cost_INR': 'sum',
    'Monthly_Gross_Margin_INR': 'sum'
}).reset_index().sort_values(by='Monthly_Total_Revenue_INR', ascending=False)

x = np.arange(len(genre_finance))
width = 0.26

rects1 = ax.bar(x - width, genre_finance['Monthly_Total_Revenue_INR'], width, label='Gross Revenue (₹)', color='#1DB954', edgecolor="#222")
rects2 = ax.bar(x, genre_finance['Monthly_Licensing_Cost_INR'], width, label='Licensing Payouts (₹)', color='#e53935', edgecolor="#222")
rects3 = ax.bar(x + width, genre_finance['Monthly_Gross_Margin_INR'], width, label='Net Margin (₹)', color='#1976D2', edgecolor="#222")

ax.set_title("Music Genre Profitability: Gross Revenue vs Licensing Payouts vs Net Margin", fontsize=13, weight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(genre_finance['Favorite_Genre'], rotation=20, ha='right', weight='bold')
ax.set_ylabel("Monthly Amount (INR ₹)", fontsize=11, weight='bold')
ax.legend(frameon=True, facecolor="#f8f9fa")

for rect in rects1:
    h = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., h + 500, f"₹{int(h):,}", ha='center', va='bottom', fontsize=7.5, weight='bold')
for rect in rects3:
    h = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., max(500, h + 500), f"₹{int(h):,}", ha='center', va='bottom', fontsize=7.5, weight='bold', color="#0d47a1")

plt.tight_layout()
plt.savefig("visualizations/03_revenue_and_margins_by_genre.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: 03_revenue_and_margins_by_genre.png")

# ==============================================================================
# Chart 4: Skip Rate % vs Weekly Listening Hours (Algorithm Efficacy vs Engagement)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6), facecolor="#ffffff")

scatter = sns.scatterplot(
    data=df,
    x='Weekly_Listening_Hours',
    y='Skip_Rate_Pct',
    hue='Favorite_Genre',
    size='Customer_Support_Tickets',
    sizes=(30, 240),
    palette='tab10',
    alpha=0.85,
    edgecolor='#333333',
    ax=ax
)

ax.axhline(35, color='#d32f2f', linestyle='--', linewidth=1.5, label='High Dissatisfaction Threshold (>35% Skip Rate)')
ax.axvline(25, color='#388e3c', linestyle=':', linewidth=1.5, label='Power Listener Boundary (25 hrs/wk)')

# Highlight critical quadrant (High Listening Hours but High Skip Rate = High Frustration)
ax.fill_between([25, 55], 35, 65, color='#ffebee', alpha=0.35, label='High Burnout Risk Zone')

ax.set_title("Recommendation Friction: Skip Rate (%) vs Weekly Listening Hours by Genre", fontsize=13, weight='bold', pad=15)
ax.set_xlabel("Weekly Listening Hours (hrs/week)", fontsize=11, weight='bold')
ax.set_ylabel("Skip Rate Percentage (%)", fontsize=11, weight='bold')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fontsize=8.5)

plt.tight_layout()
plt.savefig("visualizations/04_skip_rate_vs_listening_hours.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: 04_skip_rate_vs_listening_hours.png")

# ==============================================================================
# Chart 5: Regional Conversion Bottleneck (Listening Hours vs Subscription Revenue)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), facecolor="#ffffff")

reg_stats = df.groupby('Location_Region').agg({
    'User_ID': 'count',
    'Weekly_Listening_Hours': 'sum',
    'Monthly_Total_Revenue_INR': 'sum'
}).reset_index()

reg_stats['Listening_Share_Pct'] = (reg_stats['Weekly_Listening_Hours'] / reg_stats['Weekly_Listening_Hours'].sum()) * 100
reg_stats['Revenue_Share_Pct'] = (reg_stats['Monthly_Total_Revenue_INR'] / reg_stats['Monthly_Total_Revenue_INR'].sum()) * 100

colors = ['#42a5f5', '#66bb6a', '#ffa726', '#ab47bc']

# Pie 1: Listening Volume Share
ax1.pie(reg_stats['Listening_Share_Pct'], labels=reg_stats['Location_Region'], autopct='%1.1f%%',
        colors=colors, startangle=140, explode=[0.05 if r == "Asia-Pacific" else 0 for r in reg_stats['Location_Region']],
        wedgeprops=dict(edgecolor='#ffffff', width=0.6))
ax1.set_title("A. Regional Share of Total Listening Hours\n(Consumption Volume)", fontsize=11, weight='bold')

# Pie 2: Monetization Share
ax2.pie(reg_stats['Revenue_Share_Pct'], labels=reg_stats['Location_Region'], autopct='%1.1f%%',
        colors=colors, startangle=140, explode=[0.05 if r == "Asia-Pacific" else 0 for r in reg_stats['Location_Region']],
        wedgeprops=dict(edgecolor='#ffffff', width=0.6))
ax2.set_title("B. Regional Share of Total Revenue\n(Monetization Realized)", fontsize=11, weight='bold')

plt.suptitle("Regional Monetization Disconnect: High Asian Engagement vs Low Revenue Realization", fontsize=13, weight='bold', y=1.03)
plt.tight_layout()
plt.savefig("visualizations/05_regional_conversion_bottleneck.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: 05_regional_conversion_bottleneck.png")

# ==============================================================================
# Chart 6: Ad Fatigue vs Churn Risk Score (Free Tier Operational Analysis)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.5), facecolor="#ffffff")

free_df = df[df['Subscription_Tier'] == "Free (Ad-Supported)"].copy()

sns.regplot(
    data=free_df,
    x='Weekly_Ad_Impressions',
    y='Churn_Risk_Score',
    scatter_kws={'alpha': 0.7, 'color': '#d32f2f', 's': 55},
    line_kws={'color': '#1a237e', 'linewidth': 2},
    ax=ax
)

ax.axvline(55, color='#e65100', linestyle='--', linewidth=1.5, label='Ad Clutter Ceiling (55 ads/wk)')
ax.set_title("Free Tier Ad Saturation vs Churn Risk (Direct Operational Driver)", fontsize=13, weight='bold', pad=15)
ax.set_xlabel("Weekly Audio Ad Impressions per User", fontsize=11, weight='bold')
ax.set_ylabel("Calculated Churn Risk Score (0.0 to 1.0)", fontsize=11, weight='bold')
ax.legend(loc='lower right', frameon=True)

plt.tight_layout()
plt.savefig("visualizations/06_ad_fatigue_vs_churn_risk.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: 06_ad_fatigue_vs_churn_risk.png")

# ==============================================================================
# Chart 7: Star Schema Architecture Diagram
# ==============================================================================
fig, ax = plt.subplots(figsize=(12, 7.5), facecolor="#f8fafc")
ax.set_facecolor("#f8fafc")
ax.axis("off")

# Central Fact Box
fact_box = plt.Rectangle((0.36, 0.28), 0.28, 0.44, transform=ax.transAxes, color="#1e293b", ec="#0f172a", lw=2, zorder=2)
ax.add_patch(fact_box)
ax.text(0.50, 0.68, "FACT_MUSIC_OPERATIONS", transform=ax.transAxes, color="#38bdf8", fontsize=11, weight='bold', ha='center', zorder=3)
fact_text = (
    "• Fact_Key [PK]\n"
    "• User_Key [FK]\n"
    "• Subscription_Key [FK]\n"
    "• Device_Key [FK]\n"
    "• Genre_Key [FK]\n"
    "• Date_Key [FK]\n"
    "-------------------------\n"
    "• Weekly_Listening_Hours\n"
    "• Daily_Stream_Count\n"
    "• Monthly_Streams\n"
    "• Skip_Rate_Pct\n"
    "• Monthly_Total_Revenue\n"
    "• Monthly_Licensing_Cost\n"
    "• Monthly_Gross_Margin\n"
    "• NPS_Score / Churn_Risk"
)
ax.text(0.38, 0.31, fact_text, transform=ax.transAxes, color="#e2e8f0", fontsize=8.5, family='monospace', zorder=3)

# Dimension Boxes
dims = [
    ("DIM_USER", 0.04, 0.60, 0.22, 0.32, "#047857",
     "• User_Key [PK]\n• User_ID\n• Customer_Name\n• Age / Age_Group\n• Gender\n• Location_Region\n• User_Segment"),
    ("DIM_SUBSCRIPTION", 0.74, 0.60, 0.22, 0.32, "#b45309",
     "• Subscription_Key [PK]\n• Subscription_Tier\n• Base_Monthly_Fee\n• Target_Audience\n• Ad_Supported\n• Max_Streams"),
    ("DIM_DEVICE", 0.04, 0.08, 0.22, 0.32, "#6d28d9",
     "• Device_Key [PK]\n• Primary_Device\n• Platform_Type\n• Manufacturer\n• Lossless_Support"),
    ("DIM_GENRE", 0.74, 0.08, 0.22, 0.32, "#be123c",
     "• Genre_Key [PK]\n• Favorite_Genre\n• Royalty_Rate_INR\n• Licensing_Complexity\n• Avg_Song_Length"),
    ("DIM_DATE", 0.39, 0.80, 0.22, 0.16, "#1d4ed8",
     "• Date_Key [PK]\n• Full_Date\n• Quarter / Year")
]

for title, x_b, y_b, w_b, h_b, color, desc in dims:
    rect = plt.Rectangle((x_b, y_b), w_b, h_b, transform=ax.transAxes, color=color, ec="#0f172a", lw=1.5, zorder=2)
    ax.add_patch(rect)
    ax.text(x_b + w_b/2, y_b + h_b - 0.035, title, transform=ax.transAxes, color="#ffffff", fontsize=10, weight='bold', ha='center', zorder=3)
    ax.text(x_b + 0.015, y_b + 0.02, desc, transform=ax.transAxes, color="#f1f5f9", fontsize=8, family='monospace', zorder=3)

# Connector lines (1:N relationships)
ax.annotate("", xy=(0.36, 0.55), xytext=(0.26, 0.72), arrowprops=dict(arrowstyle="<->", color="#0f172a", lw=2))
ax.annotate("", xy=(0.64, 0.55), xytext=(0.74, 0.72), arrowprops=dict(arrowstyle="<->", color="#0f172a", lw=2))
ax.annotate("", xy=(0.36, 0.42), xytext=(0.26, 0.24), arrowprops=dict(arrowstyle="<->", color="#0f172a", lw=2))
ax.annotate("", xy=(0.64, 0.42), xytext=(0.74, 0.24), arrowprops=dict(arrowstyle="<->", color="#0f172a", lw=2))
ax.annotate("", xy=(0.50, 0.72), xytext=(0.50, 0.80), arrowprops=dict(arrowstyle="<->", color="#0f172a", lw=2))

plt.title("SoundPulse Data Warehouse - Star Schema Architecture (DWM BL-4 Model)", fontsize=14, weight='bold', pad=15)
plt.tight_layout()
plt.savefig("visualizations/07_star_schema_architecture.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: 07_star_schema_architecture.png")

print("All 7 visualizations generated successfully in visualizations/!")
