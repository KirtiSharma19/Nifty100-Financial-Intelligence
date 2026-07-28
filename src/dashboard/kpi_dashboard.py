from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

print("\n========== KPI DASHBOARD ==========\n")

print(f"Total Companies      : {df['company_name'].nunique()}")
print(f"Total Records        : {len(df)}")
print(f"Average Quality      : {round(df['quality_score'].mean(),2)}")
print(f"Average ROE          : {round(df['return_on_equity_pct'].mean(),2)}")
print(f"Average ProfitMargin : {round(df['net_profit_margin_pct'].mean(),2)}")
print(f"Average DebtEquity   : {round(df['debt_to_equity'].mean(),2)}")