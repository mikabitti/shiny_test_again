import pandas as pd
from test_json import load_from_json, save_to_json

df: pd.DataFrame = pd.read_csv("./data/annual-enterprise-survey-2024-financial-year-provisional-size-bands.csv")

print(df.describe())

print(df.head())

print(df.columns)

unn = []

for col in df.columns:
    if "Unnamed" in col:
        unn.append(col)

print(unn)

print(df[unn].describe())

empty_cols = []

for col in df.columns:
    if df[col].isna().all():
        empty_cols.append(col)
        print(col)

df = df.drop(columns=empty_cols)

print(df.describe())

unn = []

for col in df.columns:
    if "Unnamed" in col:
        unn.append(col)
        df[col].describe()

print(unn)

print(df[df['Unnamed: 9'].notna()])




notna = df[df['Unnamed: 9'].notna()].index.tolist()
yesna = df[df['Unnamed: 9'].isna()].index.tolist()
print(notna)
#      name  status
# 0   Alice  active
# 2 Charlie  active
# 3   David  active

# Get just the indices
#print(df[df['Unnamed: 9'].notna()].index.tolist())

data = {
    "success": notna,
    "warning": [ 0 ],
    "error" : yesna
}

# print(data)

save_to_json(data, "row_status.json")
