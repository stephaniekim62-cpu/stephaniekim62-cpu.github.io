# Run this to regenerate sample_transactions.csv (fictional data for the budget forecaster demo)
# Generates a SAMPLE student transaction history (synthetic, for demo only)
import numpy as np, pandas as pd
rng=np.random.default_rng(2027)
months=pd.period_range("2023-09","2026-10",freq="M")
rows=[]
def add(d,cat,amt,desc): rows.append([d.strftime("%Y-%m-%d"),cat,round(float(amt),2),desc])
for m in months:
    start=m.start_time; days=m.days_in_month; mo=m.month
    away = mo in (6,7)                # summer internship away from Pittsburgh (sublet covers part of rent)
    infl=(1.03)**((m-months[0]).n/12)
    add(start,"Rent",(1150 if not away else 700)*(1.04 if m>=pd.Period("2025-08","M") else 1)*(0.96 if m<pd.Period("2024-08","M") else 1),"Apartment rent")
    add(start+pd.Timedelta(days=4),"Utilities & phone",rng.normal(95,8)+(25 if mo in (1,2,7,8) else 0),"Electric, internet, phone")
    for _ in range(rng.poisson(4 if not away else 2)):
        add(start+pd.Timedelta(days=int(rng.integers(0,days))),"Groceries",rng.gamma(6,9)*infl,"Grocery store")
    semester= mo in (1,2,3,4,9,10,11,12)
    for _ in range(rng.poisson(9 if semester else 5)):
        add(start+pd.Timedelta(days=int(rng.integers(0,days))),"Dining out",rng.gamma(3,7)*infl,"Restaurant / cafe")
    for _ in range(rng.poisson(5)):
        add(start+pd.Timedelta(days=int(rng.integers(0,days))),"Transport",rng.gamma(2,6),"Rideshare / transit")
    shop=1.8 if mo in (11,12) else 1.3 if mo in (8,9) else 1
    for _ in range(rng.poisson(3*shop)):
        add(start+pd.Timedelta(days=int(rng.integers(0,days))),"Shopping",rng.gamma(2,22),"Clothes / online order")
    for _ in range(rng.poisson(2.5)):
        add(start+pd.Timedelta(days=int(rng.integers(0,days))),"Entertainment",rng.gamma(2,14),"Events / movies")
    add(start+pd.Timedelta(days=9),"Subscriptions",27.97 if m<pd.Period("2025-06","M") else 33.97,"Streaming, cloud storage")
    if mo in (12,5,8): add(start+pd.Timedelta(days=int(rng.integers(3,20))),"Travel",rng.normal(780 if mo==12 else 420,60),"Flights / trips home")
    if mo in (1,8): add(start+pd.Timedelta(days=12),"Books & school",rng.normal(240,40),"Textbooks, supplies")
df=pd.DataFrame(rows,columns=["date","category","amount","description"]).sort_values("date")
df.to_csv("sample_transactions.csv",index=False); print(len(df)); print(df.groupby(df.date.str[:7]).amount.sum().round(0).to_string())
