from pathlib import Path

from src.services.ratio_engine import DatasetBuilder
from src.screener.engine import ScreenerEngine
from src.analytics.peer import PeerEngine
from src.analytics.radar_chart import RadarChartEngine
from src.reports.peer_report import PeerReport


print("=" * 70)
print("SPRINT 3 TEST SUITE")
print("=" * 70)


# =====================================================
# Dataset Builder
# =====================================================

print("\n[1] Dataset Builder")

engine = DatasetBuilder()

df = engine.build_dataset()

assert len(df) > 0

assert "quality_score" in df.columns

assert "composite_score" in df.columns

print("PASS")


# =====================================================
# Screener
# =====================================================

print("\n[2] Screener")

screen = ScreenerEngine()

result = screen.screen(
    roe_min=15,
    debt_max=1,
    quality_min=70
)

assert len(result) > 0

print("PASS")


# =====================================================
# Peer Engine
# =====================================================

print("\n[3] Peer Engine")

peer = PeerEngine()

peer.calculate_percentiles()

assert "peer_group" in peer.df.columns

assert "composite_score_percentile" in peer.df.columns

print("PASS")


# =====================================================
# Radar Charts
# =====================================================

print("\n[4] Radar Charts")

RadarChartEngine().generate()

assert Path(
    "exports/radar_charts"
).exists()

print("PASS")


# =====================================================
# Peer Report
# =====================================================

print("\n[5] Peer Report")

PeerReport().generate()

assert Path(
    "exports/peer_comparison.xlsx"
).exists()

print("PASS")


# =====================================================
# CSV Reports
# =====================================================

print("\n[6] CSV Reports")

required = [

    "exports/final_financial_report.csv",

    "exports/cashflow_report.csv",

    "exports/cagr_report.csv",

    "exports/valuation_report.csv",

    "exports/sector_report.csv",

    "exports/screener_output.csv",

    "exports/peer_comparison.csv"

]

for file in required:

    assert Path(file).exists(), f"{file} Missing"

print("PASS")


# =====================================================
# Final
# =====================================================

print()

print("=" * 70)

print("ALL SPRINT 3 TESTS PASSED")

print("=" * 70)