import sqlite3
import pandas as pd

conn = sqlite3.connect("../vasuki.db")

df = pd.read_sql("""
SELECT concept,frequency
FROM concepts
""", conn)

print("Loaded:", len(df))

STOPWORDS = {
    "shall","under","same","only",
    "table","section","using",
    "through","without","must",
    "either","both","first",
    "during","above","these",
    "within","please"
}

df = df[
    ~df["concept"].str.lower().isin(STOPWORDS)
]

df = df[
    df["concept"].str.len() > 3
]

df = df.sort_values(
    "frequency",
    ascending=False
)

print("\nTOP CLEAN CONCEPTS\n")

print(df.head(100))

df.to_csv(
    "clean_concepts.csv",
    index=False
)

print("\nSaved clean_concepts.csv")
