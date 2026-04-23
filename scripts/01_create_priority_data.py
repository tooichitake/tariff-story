"""
Phase 1 P1: Create hardcoded viz3 and viz7 datasets (zero dependencies).
Also creates key_events.csv and country_mapping.csv reference tables.
"""
import pandas as pd
import os

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
JOINED = os.path.join(BASE, "data", "joined")
REF = os.path.join(BASE, "data", "reference")

# ============================================================
# viz3_who_pays.csv — THE CENTRAL VISUALIZATION
# Source: TPC Tariff Tracker + Yale Budget Lab distributional data
# ============================================================
viz3 = pd.DataFrame({
    "income_group": ["Bottom 20%", "Second 20%", "Middle 20%", "Fourth 20%", "Top 20%", "Top 1%"],
    "avg_tax_increase_usd": [400, 960, 1610, 2770, 7330, 39800],
    "fed_tax_rate_increase_pp": [1.9, 1.8, 1.6, 1.4, 1.3, 0.7],
    "share_of_income_lost_pct": [3.6, 2.8, 2.0, 1.6, 1.2, 1.1],
    "most_affected_goods": [
        "Apparel, shoes, food",
        "Clothing, household basics",
        "Electronics, furniture",
        "Vehicles, appliances",
        "Vehicles, luxury goods",
        "Financial assets, minimal goods impact",
    ],
    "source": ["TPC/Yale"] * 6,
})
viz3.to_csv(os.path.join(JOINED, "viz3_who_pays.csv"), index=False)
print(f"[OK] viz3_who_pays.csv — {viz3.shape}")
print(viz3.to_string(index=False))
print()

# ============================================================
# viz7_whatif.csv — Act IV What-If Scenarios
# Source: Yale Budget Lab + TPC estimates
# ============================================================
viz7 = pd.DataFrame({
    "scenario": [
        "Let S122 expire (Jul 24)",
        "Congress extends S122 at 10%",
        "Congress extends S122 at 15%",
        "Replace with targeted S232/S301",
        "Restore IEEPA-level rates (if new authority)",
    ],
    "eff_tariff_rate": [8.1, 10.5, 13.0, 12.0, 16.8],
    "gdp_impact_pct": [-0.1, -0.2, -0.3, -0.25, -0.4],
    "unemployment_increase_pp": [0.1, 0.2, 0.4, 0.3, 0.7],
    "price_increase_pct": [0.3, 0.4, 0.6, 0.5, 1.2],
    "household_cost_bottom20_usd": [150, 250, 400, 300, 700],
    "household_cost_top20_usd": [3000, 4500, 7330, 5500, 12000],
    "tariff_revenue_10yr_trillion": [1.2, 1.5, 2.0, 1.8, 2.5],
    "source": ["Yale/TPC", "Yale/TPC", "Yale/TPC", "Yale/TPC est.", "Yale Nov 2025"],
})
viz7.to_csv(os.path.join(JOINED, "viz7_whatif.csv"), index=False)
print(f"[OK] viz7_whatif.csv — {viz7.shape}")
print(viz7.to_string(index=False))
print()

# ============================================================
# key_events.csv — ~27 events from Tariff_Timeline_EN.md
# ============================================================
events = [
    ("2025-01-20", "President Trump inaugurated", "President Trump inaugurated as 47th President, executive orders on trade policy expected", "tariff_up", 2.5, "I"),
    ("2025-02-01", "IEEPA tariffs announced", "25% on Canada/Mexico, 10% on China under IEEPA emergency authority", "tariff_up", 5.0, "I"),
    ("2025-02-04", "China retaliates", "China announces 15% counter-tariffs on US agricultural products", "retaliation", 5.0, "I"),
    ("2025-02-12", "25% steel & aluminum", "Global 25% tariffs on steel and aluminum imports", "tariff_up", 7.0, "I"),
    ("2025-03-04", "Canada/Mexico tariffs active", "25% tariffs on Canada and Mexico take effect", "tariff_up", 10.0, "I"),
    ("2025-03-12", "EU counter-tariffs", "EU retaliates with tariffs on US bourbon, motorcycles, agricultural products", "retaliation", 10.0, "I"),
    ("2025-03-19", "Powell: transitory", "Fed Chair Powell says tariff inflation likely transitory, one-time price adjustment", "negotiation", 10.0, "I"),
    ("2025-04-02", "Liberation Day", "Sweeping reciprocal tariffs announced: 10% baseline + country-specific rates up to 49%", "tariff_up", 22.0, "I"),
    ("2025-04-04", "Powell walks back transitory", "Powell acknowledges tariff impact may be larger and more persistent than expected", "negotiation", 22.0, "I"),
    ("2025-04-09", "90-day pause (ex-China)", "90-day pause on reciprocal tariffs for all countries except China; 10% baseline remains", "tariff_down", 18.0, "I"),
    ("2025-04-10", "US-China 125% peak", "Tit-for-tat escalation reaches 125% US tariffs on China, 84% China on US", "tariff_up", 27.0, "I"),
    ("2025-05-14", "Geneva talks — mutual reduction", "US-China Geneva negotiations: mutual tariff reduction, China from 125% to 10% for 90 days", "negotiation", 17.0, "II"),
    ("2025-06-01", "TPC distributional data released", "Tax Policy Center publishes income quintile burden analysis showing regressive impact", "negotiation", 17.0, "II"),
    ("2025-07-09", "90-day pause expires", "Original 90-day pause on reciprocal tariffs expires, rates revert or renegotiate", "tariff_up", 20.0, "II"),
    ("2025-08-22", "Powell Jackson Hole", "Powell characterizes tariff inflation as one-time price level shift, not persistent inflation", "negotiation", 20.0, "II"),
    ("2025-08-25", "Federal Circuit rules vs IEEPA", "Federal Circuit Court rules IEEPA does not authorize tariffs, legal challenge escalates", "legal", 20.0, "II"),
    ("2025-09-15", "Reshoring investment surge", "Multiple manufacturers announce US factory investments totaling $50B+", "negotiation", 18.0, "III"),
    ("2025-10-30", "US-China Busan deal", "US-China Busan negotiations: tariffs reduced to 35-50% range on most goods", "tariff_down", 15.0, "III"),
    ("2025-11-15", "Manufacturing jobs data", "BLS reports 83,000 manufacturing jobs lost in 2025 despite reshoring announcements", "negotiation", 15.0, "III"),
    ("2025-12-10", "Powell: very unusual economy", "Powell acknowledges very unusual economy; Fed delivers 3rd rate cut of 2025", "negotiation", 14.0, "III"),
    ("2025-12-31", "2025 trade deficit widens", "Full-year data shows US trade deficit widened despite tariffs — deficit paradox confirmed", "negotiation", 14.0, "III"),
    ("2026-01-15", "SCOTUS accepts IEEPA case", "Supreme Court agrees to hear challenge to IEEPA tariff authority", "legal", 14.0, "IV"),
    ("2026-02-20", "SCOTUS strikes down IEEPA 6-3", "Supreme Court rules 6-3 that IEEPA does not authorize broad tariff authority", "legal", 14.0, "IV"),
    ("2026-02-24", "Section 122 takes effect", "Congress passes Section 122 authority as temporary replacement, 150-day window", "tariff_up", 13.0, "IV"),
    ("2026-03-11", "S301 investigations launched", "USTR launches Section 301 investigations as longer-term tariff mechanism", "tariff_up", 13.0, "IV"),
    ("2026-04-08", "Current date", "Section 122 tariffs in effect, July 24 expiration approaching, policy uncertainty high", "threat", 13.0, "IV"),
    ("2026-07-24", "S122 expires", "Section 122 authority expires — Congress must act, extend, or let tariffs lapse", "threat", 8.1, "IV"),
]

key_events = pd.DataFrame(events, columns=[
    "date", "event_short", "event_detail", "impact_type", "eff_tariff_rate_approx", "story_act"
])
key_events["date"] = pd.to_datetime(key_events["date"])
key_events.to_csv(os.path.join(REF, "key_events.csv"), index=False)
print(f"[OK] key_events.csv — {key_events.shape}")
print(key_events[["date", "event_short", "story_act"]].to_string(index=False))
print()

# ============================================================
# country_mapping.csv — ISO 3166 alpha-3 mapping
# ============================================================
countries = [
    ("China", "CHN", "China"), ("People's Republic of China", "CHN", "China"),
    ("United States", "USA", "United States"), ("US", "USA", "United States"),
    ("Canada", "CAN", "Canada"), ("Mexico", "MEX", "Mexico"),
    ("Japan", "JPN", "Japan"), ("South Korea", "KOR", "South Korea"),
    ("Korea, South", "KOR", "South Korea"), ("Republic of Korea", "KOR", "South Korea"),
    ("Taiwan", "TWN", "Taiwan"), ("Chinese Taipei", "TWN", "Taiwan"),
    ("India", "IND", "India"), ("Vietnam", "VNM", "Vietnam"), ("Viet Nam", "VNM", "Vietnam"),
    ("Thailand", "THA", "Thailand"), ("Indonesia", "IDN", "Indonesia"),
    ("Malaysia", "MYS", "Malaysia"), ("Philippines", "PHL", "Philippines"),
    ("Singapore", "SGP", "Singapore"), ("Bangladesh", "BGD", "Bangladesh"),
    ("Cambodia", "KHM", "Cambodia"), ("Sri Lanka", "LKA", "Sri Lanka"),
    ("Pakistan", "PAK", "Pakistan"), ("Myanmar", "MMR", "Myanmar"),
    ("European Union", "EUU", "European Union"), ("EU", "EUU", "European Union"),
    ("Germany", "DEU", "Germany"), ("France", "FRA", "France"),
    ("Italy", "ITA", "Italy"), ("Spain", "ESP", "Spain"),
    ("Netherlands", "NLD", "Netherlands"), ("Belgium", "BEL", "Belgium"),
    ("Ireland", "IRL", "Ireland"), ("Poland", "POL", "Poland"),
    ("Sweden", "SWE", "Sweden"), ("Austria", "AUT", "Austria"),
    ("United Kingdom", "GBR", "United Kingdom"), ("UK", "GBR", "United Kingdom"),
    ("Switzerland", "CHE", "Switzerland"),
    ("Australia", "AUS", "Australia"), ("New Zealand", "NZL", "New Zealand"),
    ("Brazil", "BRA", "Brazil"), ("Argentina", "ARG", "Argentina"),
    ("Colombia", "COL", "Colombia"), ("Chile", "CHL", "Chile"),
    ("Peru", "PER", "Peru"),
    ("Saudi Arabia", "SAU", "Saudi Arabia"), ("Israel", "ISR", "Israel"),
    ("Turkey", "TUR", "Turkey"), ("Türkiye", "TUR", "Turkey"),
    ("South Africa", "ZAF", "South Africa"), ("Nigeria", "NGA", "Nigeria"),
    ("Egypt", "EGY", "Egypt"), ("Kenya", "KEN", "Kenya"),
    ("Russia", "RUS", "Russia"), ("Russian Federation", "RUS", "Russia"),
    ("Norway", "NOR", "Norway"), ("Denmark", "DNK", "Denmark"),
    ("Finland", "FIN", "Finland"), ("Portugal", "PRT", "Portugal"),
    ("Greece", "GRC", "Greece"), ("Czech Republic", "CZE", "Czech Republic"),
    ("Czechia", "CZE", "Czech Republic"), ("Romania", "ROU", "Romania"),
    ("Hungary", "HUN", "Hungary"),
    ("Hong Kong", "HKG", "Hong Kong"), ("Laos", "LAO", "Laos"),
    ("Nicaragua", "NIC", "Nicaragua"), ("Madagascar", "MDG", "Madagascar"),
    ("Lesotho", "LSO", "Lesotho"), ("Botswana", "BWA", "Botswana"),
    ("Mauritius", "MUS", "Mauritius"), ("Libya", "LBY", "Libya"),
    ("Syria", "SYR", "Syria"), ("Iraq", "IRQ", "Iraq"),
    ("Falkland Islands", "FLK", "Falkland Islands"),
    ("Nauru", "NRU", "Nauru"), ("Norfolk Island", "NFK", "Norfolk Island"),
]
country_mapping = pd.DataFrame(countries, columns=["name_variant", "iso3", "name_standard"])
country_mapping.to_csv(os.path.join(REF, "country_mapping.csv"), index=False)
print(f"[OK] country_mapping.csv — {country_mapping.shape}")
print(f"  Unique countries: {country_mapping['iso3'].nunique()}")

print("\n=== All priority data created successfully ===")
