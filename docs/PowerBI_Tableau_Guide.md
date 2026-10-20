# SoundPulse Streaming Inc. — Power BI & Tableau Implementation Guide
## Star Schema Data Model, DAX Measures, Visual Configurations & KPI Cards

This guide provides end-to-end instructions for importing the dimensional model created for **SoundPulse Streaming Inc.** into **Microsoft Power BI Desktop** or **Tableau Desktop**, configuring relationships, creating DAX measures, and assembling an executive dashboard.

---

## 1. Data Ingestion & Star Schema Relationship Configuration

### A. Files to Import
From `c:\dwm\ise\data\star_schema\`, import the following 6 CSV files into Power BI (`Home -> Get Data -> Text/CSV`):
1. `Dim_User.csv`
2. `Dim_Subscription.csv`
3. `Dim_Device.csv`
4. `Dim_Genre.csv`
5. `Dim_Date.csv`
6. `Fact_Music_Operations.csv`

### B. Relationship Model Configuration (Model View)
In Power BI **Model View**, establish the following relationships. All relationships must be **One-to-Many (1:*)**, with cross-filter direction set to **Single** (Dimension filters Fact):

| From Table (Dimension - 1) | Primary Key (PK) | To Table (Fact - *) | Foreign Key (FK) | Cardinality | Cross Filter Direction |
|---|---|---|---|---|---|
| `Dim_User` | `User_Key` | `Fact_Music_Operations` | `User_Key` | 1 to Many (1:*) | Single |
| `Dim_Subscription` | `Subscription_Key` | `Fact_Music_Operations` | `Subscription_Key` | 1 to Many (1:*) | Single |
| `Dim_Device` | `Device_Key` | `Fact_Music_Operations` | `Device_Key` | 1 to Many (1:*) | Single |
| `Dim_Genre` | `Genre_Key` | `Fact_Music_Operations` | `Genre_Key` | 1 to Many (1:*) | Single |
| `Dim_Date` | `Date_Key` | `Fact_Music_Operations` | `Date_Key` | 1 to Many (1:*) | Single |

---

## 2. Power BI DAX Measures Library

Create a dedicated Measures Table (`_KPI_Measures`) or add the following DAX calculations directly to `Fact_Music_Operations`:

### 1. Total Gross Revenue (INR)
```dax
Total Gross Revenue = 
SUM(Fact_Music_Operations[Monthly_Total_Revenue_INR])
```

### 2. Total Licensing Royalty Cost (INR)
```dax
Total Royalty Cost = 
SUM(Fact_Music_Operations[Monthly_Licensing_Cost_INR])
```

### 3. Total Monthly Gross Margin (INR)
```dax
Total Gross Margin = 
[Total Gross Revenue] - [Total Royalty Cost]
```

### 4. Gross Margin Percentage (%)
```dax
Gross Margin % = 
DIVIDE([Total Gross Margin], [Total Gross Revenue], 0)
```

### 5. Total User Count
```dax
Total Users = 
COUNTROWS(Fact_Music_Operations)
```

### 6. Active Subscribers Count
```dax
Active Listeners = 
CALCULATE(
    COUNTROWS(Fact_Music_Operations),
    Fact_Music_Operations[Churn_Binary] = 0
)
```

### 7. Churned Subscribers Count
```dax
Churned Listeners = 
CALCULATE(
    COUNTROWS(Fact_Music_Operations),
    Fact_Music_Operations[Churn_Binary] = 1
)
```

### 8. Cohort Churn Rate (%)
```dax
Cohort Churn Rate % = 
DIVIDE([Churned Listeners], [Total Users], 0)
```

### 9. Average Revenue Per User (ARPU)
```dax
ARPU = 
DIVIDE([Total Gross Revenue], [Total Users], 0)
```

### 10. Average Weekly Listening Hours
```dax
Avg Weekly Hours = 
AVERAGE(Fact_Music_Operations[Weekly_Listening_Hours])
```

### 11. Average Skip Rate (%)
```dax
Avg Skip Rate % = 
AVERAGE(Fact_Music_Operations[Skip_Rate_Pct])
```

### 12. Net Promoter Score (NPS)
```dax
NPS Score = 
VAR Promoters = CALCULATE(COUNTROWS(Fact_Music_Operations), Fact_Music_Operations[NPS_Category] = "Promoter")
VAR Detractors = CALCULATE(COUNTROWS(Fact_Music_Operations), Fact_Music_Operations[NPS_Category] = "Detractor")
VAR Total = [Total Users]
RETURN
    IF(Total > 0, ROUND(DIVIDE(Promoters - Detractors, Total, 0) * 100, 0), 0)
```

### 13. Ad Fatigue Index (Average Ads per Listening Hour)
```dax
Ad Fatigue Ratio = 
DIVIDE(
    SUM(Fact_Music_Operations[Weekly_Ad_Impressions]),
    SUM(Fact_Music_Operations[Weekly_Listening_Hours]),
    0
)
```

---

## 3. Power BI Dashboard Layout & Visual Setup

### Page Setup
- **Canvas Size:** 16:9 (1920 x 1080 px or default Widescreen)
- **Theme:** Dark Mode or Custom JSON (Canvas Background: `#0B0F17`, Visual Background: `#151C28`, Data Colors: `#1DB954`, `#38BDF8`, `#EF4444`, `#F59E0B`)

### A. Top Slicer Bar (Row 1)
1. **Region Slicer:** `Dim_User[Location_Region]` (Dropdown or Tile style)
2. **Subscription Tier Slicer:** `Dim_Subscription[Subscription_Tier]` (Tile style)
3. **User Demographic Segment Slicer:** `Dim_User[User_Segment]` (Dropdown style)
4. **Churn Status Slicer:** `Fact_Music_Operations[Churn_Binary]` (or degenerate status)

### B. Executive KPI Cards (Row 2)
Place 6 Card Visuals horizontally:
- **Card 1:** `[Total Gross Revenue]` (Format: Currency `₹#,##0.00`)
- **Card 2:** `[Active Listeners]` (Format: Integer `#,##0`)
- **Card 3:** `[Cohort Churn Rate %]` (Format: Percentage `0.0%`, Conditional Formatting: Red if > 25%)
- **Card 4:** `[Total Gross Margin]` (Format: Currency `₹#,##0.00`)
- **Card 5:** `[Avg Weekly Hours]` (Format: Decimal `0.0 hrs`)
- **Card 6:** `[NPS Score]` (Format: Integer `#,##0`, Accent Green if > 20)

### C. Core Analytical Visuals (Rows 3 & 4)

#### Visual 1: Clustered Column Chart (Plan Financials)
- **X-Axis:** `Dim_Subscription[Subscription_Tier]`
- **Y-Axis:** `[Total Gross Revenue]`, `[Total Royalty Cost]`, `[Total Gross Margin]`
- **Bar Colors:** Revenue (`#1DB954`), Royalty (`#EF4444`), Margin (`#38BDF8`)
- **Insight:** Demonstrates that Free tier generates low revenue while eating royalties; Family tier delivers highest margin.

#### Visual 2: 100% Stacked Bar or Donut Chart (Churn Vulnerability)
- **Legend:** `Dim_User[User_Segment]`
- **Values:** `[Churned Listeners]`
- **Tooltips:** `[Cohort Churn Rate %]`
- **Insight:** Highlights high student churn due to lack of graduation pricing.

#### Visual 3: Scatter Plot (Recommender Friction & Algorithmic Burnout)
- **X-Axis:** `Fact_Music_Operations[Weekly_Listening_Hours]`
- **Y-Axis:** `Fact_Music_Operations[Skip_Rate_Pct]`
- **Legend:** `Dim_Genre[Favorite_Genre]`
- **Size:** `Fact_Music_Operations[Customer_Support_Tickets]`
- **Reference Lines:** Add constant Y-line at 35% (Dissatisfaction Threshold) and X-line at 25 hrs/wk.
- **Insight:** Shows Indie/EDM power listeners trapped in high-skip frustration.

#### Visual 4: Horizontal Bar Chart (Primary Pain Points)
- **Y-Axis:** `Fact_Music_Operations[Primary_Pain_Point]`
- **X-Axis:** `[Total Users]`
- **Color Saturation:** `[Avg Skip Rate %]` or `[Cohort Churn Rate %]`
- **Insight:** Confirms audio ad saturation and app buffering as leading churn catalysts.

---

## 4. Tableau Desktop Equivalent Configuration

If utilizing Tableau Desktop instead of Power BI:
1. Connect to `Fact_Music_Operations.csv` as the central logical table.
2. Drag `Dim_User.csv`, `Dim_Subscription.csv`, `Dim_Device.csv`, `Dim_Genre.csv`, and `Dim_Date.csv` into the Data Source canvas and configure relationships using the matching `*_Key` fields.
3. Create Calculated Fields:
   - `Gross Revenue`: `SUM([Monthly Total Revenue INR])`
   - `Royalty Payouts`: `SUM([Monthly Licensing Cost INR])`
   - `Net Margin`: `[Gross Revenue] - [Royalty Payouts]`
   - `Churn Rate`: `SUM([Churn Binary]) / COUNT([Fact Music Operations])`
   - `ARPU`: `[Gross Revenue] / COUNT([Fact Music Operations])`
4. Assemble worksheets onto a 1200x800 dashboard layout with quick filters set to **"Apply to All Worksheets using this Data Source"**.
