"""Fix Kaggle CSV files that use semicolons as delimiters."""
import pandas as pd
import os

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
RAW_KAGGLE = os.path.join(BASE, "data", "raw", "kaggle")
CLEANED = os.path.join(BASE, "data", "cleaned")
REF = os.path.join(BASE, "data", "reference")

# Fix semicolon-delimited files
for fname in ["Tariff Calculations.csv", "Tariff Calculations plus Population.csv"]:
    filepath = os.path.join(RAW_KAGGLE, fname)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, sep=";")
        print(f"{fname}: {df.shape}")
        print(f"  Columns: {df.columns.tolist()}")
        print(df.head(3).to_string())

        df.columns = [c.strip().lower().replace(" ", "_").replace("(%)", "pct") for c in df.columns]
        outname = fname.replace(" ", "_").lower()
        df.to_csv(os.path.join(CLEANED, f"kaggle_{outname}"), index=False)
        print(f"  -> Saved: kaggle_{outname}\n")

# Update country mapping with missing countries
country_map = pd.read_csv(os.path.join(REF, "country_mapping.csv"))
existing_iso3 = set(zip(country_map["name_variant"], country_map["iso3"]))

extra_countries = [
    ("Costa Rica", "CRI", "Costa Rica"), ("Jordan", "JOR", "Jordan"),
    ("Dominican Republic", "DOM", "Dominican Republic"),
    ("United Arab Emirates", "ARE", "United Arab Emirates"),
    ("Ecuador", "ECU", "Ecuador"), ("Guatemala", "GTM", "Guatemala"),
    ("Honduras", "HND", "Honduras"), ("Myanmar (Burma)", "MMR", "Myanmar"),
    ("Tunisia", "TUN", "Tunisia"), ("Kazakhstan", "KAZ", "Kazakhstan"),
    ("Algeria", "DZA", "Algeria"), ("Angola", "AGO", "Angola"),
    ("Bahamas", "BHS", "Bahamas"), ("Bahrain", "BHR", "Bahrain"),
    ("Barbados", "BRB", "Barbados"), ("Belarus", "BLR", "Belarus"),
    ("Belize", "BLZ", "Belize"), ("Benin", "BEN", "Benin"),
    ("Bhutan", "BTN", "Bhutan"), ("Bolivia", "BOL", "Bolivia"),
    ("Bosnia and Herzegovina", "BIH", "Bosnia and Herzegovina"),
    ("Brunei", "BRN", "Brunei"), ("Burkina Faso", "BFA", "Burkina Faso"),
    ("Burundi", "BDI", "Burundi"), ("Cameroon", "CMR", "Cameroon"),
    ("Cape Verde", "CPV", "Cape Verde"), ("Chad", "TCD", "Chad"),
    ("Comoros", "COM", "Comoros"), ("Congo", "COG", "Congo"),
    ("Cote d'Ivoire", "CIV", "Cote d'Ivoire"), ("Cuba", "CUB", "Cuba"),
    ("DR Congo", "COD", "DR Congo"), ("Djibouti", "DJI", "Djibouti"),
    ("El Salvador", "SLV", "El Salvador"), ("Equatorial Guinea", "GNQ", "Equatorial Guinea"),
    ("Eritrea", "ERI", "Eritrea"), ("Ethiopia", "ETH", "Ethiopia"),
    ("Fiji", "FJI", "Fiji"), ("Gabon", "GAB", "Gabon"),
    ("Gambia", "GMB", "Gambia"), ("Georgia", "GEO", "Georgia"),
    ("Ghana", "GHA", "Ghana"), ("Guyana", "GUY", "Guyana"),
    ("Haiti", "HTI", "Haiti"), ("Iceland", "ISL", "Iceland"),
    ("Iran", "IRN", "Iran"), ("Israel", "ISR", "Israel"),
    ("Ivory Coast", "CIV", "Cote d'Ivoire"), ("Jamaica", "JAM", "Jamaica"),
    ("Kosovo", "XKX", "Kosovo"), ("Kuwait", "KWT", "Kuwait"),
    ("Kyrgyzstan", "KGZ", "Kyrgyzstan"), ("Lebanon", "LBN", "Lebanon"),
    ("Liberia", "LBR", "Liberia"), ("Lithuania", "LTU", "Lithuania"),
    ("Luxembourg", "LUX", "Luxembourg"), ("Malawi", "MWI", "Malawi"),
    ("Maldives", "MDV", "Maldives"), ("Mali", "MLI", "Mali"),
    ("Malta", "MLT", "Malta"), ("Mauritania", "MRT", "Mauritania"),
    ("Moldova", "MDA", "Moldova"), ("Mongolia", "MNG", "Mongolia"),
    ("Montenegro", "MNE", "Montenegro"), ("Morocco", "MAR", "Morocco"),
    ("Mozambique", "MOZ", "Mozambique"), ("Namibia", "NAM", "Namibia"),
    ("Nepal", "NPL", "Nepal"), ("Nicaragua", "NIC", "Nicaragua"),
    ("Niger", "NER", "Niger"), ("North Macedonia", "MKD", "North Macedonia"),
    ("Oman", "OMN", "Oman"), ("Panama", "PAN", "Panama"),
    ("Papua New Guinea", "PNG", "Papua New Guinea"),
    ("Paraguay", "PRY", "Paraguay"), ("Qatar", "QAT", "Qatar"),
    ("Rwanda", "RWA", "Rwanda"), ("Samoa", "WSM", "Samoa"),
    ("Senegal", "SEN", "Senegal"), ("Serbia", "SRB", "Serbia"),
    ("Sierra Leone", "SLE", "Sierra Leone"),
    ("Slovakia", "SVK", "Slovakia"), ("Slovenia", "SVN", "Slovenia"),
    ("Solomon Islands", "SLB", "Solomon Islands"),
    ("Somalia", "SOM", "Somalia"), ("Sudan", "SDN", "Sudan"),
    ("Suriname", "SUR", "Suriname"), ("Tanzania", "TZA", "Tanzania"),
    ("Togo", "TGO", "Togo"), ("Tonga", "TON", "Tonga"),
    ("Trinidad and Tobago", "TTO", "Trinidad and Tobago"),
    ("Uganda", "UGA", "Uganda"), ("Ukraine", "UKR", "Ukraine"),
    ("Uruguay", "URY", "Uruguay"), ("Uzbekistan", "UZB", "Uzbekistan"),
    ("Vanuatu", "VUT", "Vanuatu"), ("Venezuela", "VEN", "Venezuela"),
    ("Yemen", "YEM", "Yemen"), ("Zambia", "ZMB", "Zambia"),
    ("Zimbabwe", "ZWE", "Zimbabwe"),
    ("Azerbaijan", "AZE", "Azerbaijan"), ("Armenia", "ARM", "Armenia"),
    ("Albania", "ALB", "Albania"), ("Afghanistan", "AFG", "Afghanistan"),
    ("Andorra", "AND", "Andorra"), ("Antigua and Barbuda", "ATG", "Antigua and Barbuda"),
    ("Bulgaria", "BGR", "Bulgaria"), ("Croatia", "HRV", "Croatia"),
    ("Cyprus", "CYP", "Cyprus"), ("Estonia", "EST", "Estonia"),
    ("Latvia", "LVA", "Latvia"), ("Liechtenstein", "LIE", "Liechtenstein"),
    ("Tajikistan", "TJK", "Tajikistan"), ("Turkmenistan", "TKM", "Turkmenistan"),
    ("Timor-Leste", "TLS", "Timor-Leste"),
]

new_rows = []
for nv, iso3, ns in extra_countries:
    if nv not in set(country_map["name_variant"]):
        new_rows.append({"name_variant": nv, "iso3": iso3, "name_standard": ns})

if new_rows:
    extra_df = pd.DataFrame(new_rows)
    country_map = pd.concat([country_map, extra_df], ignore_index=True)
    country_map.to_csv(os.path.join(REF, "country_mapping.csv"), index=False)
    print(f"Updated country_mapping.csv: added {len(new_rows)} new entries, total {len(country_map)} rows")

# Re-map Trump tariffs with updated mapping
name_to_iso3 = dict(zip(country_map["name_variant"], country_map["iso3"]))
trump_tariffs = pd.read_csv(os.path.join(RAW_KAGGLE, "Trump_tariffs_by_country.csv"))
trump_tariffs["iso3"] = trump_tariffs["Country"].map(name_to_iso3)
mapped = trump_tariffs["iso3"].notna().sum()
unmapped = trump_tariffs[trump_tariffs["iso3"].isna()]["Country"].unique()
print(f"\nTrump tariffs ISO3 mapped: {mapped}/{len(trump_tariffs)}")
if len(unmapped) > 0:
    print(f"Still unmapped ({len(unmapped)}): {list(unmapped[:15])}")

trump_tariffs.columns = [c.strip().lower().replace(" ", "_") for c in trump_tariffs.columns]
trump_tariffs.to_csv(os.path.join(CLEANED, "kaggle_trump_tariffs_by_country.csv"), index=False)
print("Saved updated kaggle_trump_tariffs_by_country.csv")
