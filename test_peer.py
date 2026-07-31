from src.analytics.peer import PeerEngine

engine = PeerEngine()

engine.calculate_percentiles()

engine.summary()

engine.export()

import pandas as pd

df = pd.read_excel("data/raw/peer_groups.xlsx")

print(df.columns.tolist())

print(df.head())