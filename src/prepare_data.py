from pathlib import Path

import numpy as np
import pandas as pd



ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = ROOT / "data" / "raw" / "survey_results_public.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "selected_clean.csv"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)



selected_columns = [
    "ResponseId",
    "YearsCode",
    "NEWCollabToolsHaveWorkedWith",
    "AISelect",
    "AIToolCurrently Using",
    "AISent"
]



df = pd.read_csv(
    RAW_FILE,
    usecols=selected_columns,
    low_memory=False
)

print("Original selected dataset shape:")
print(df.shape)


df["YearsCodeNumeric"] = (
    df["YearsCode"]
    .replace({
        "Less than 1 year": 0.5,
        "More than 50 years": 51
    })
)

df["YearsCodeNumeric"] = pd.to_numeric(
    df["YearsCodeNumeric"],
    errors="coerce"
)



df["ExperienceGroup"] = pd.cut(
    df["YearsCodeNumeric"],
    bins=[-np.inf, 2, 9, np.inf],
    labels=[
        "Early Experience",
        "Mid Experience",
        "Long Experience"
    ]
)


def convert_ai_sentiment(value):

    if value in ["Very favorable", "Favorable"]:
        return "High"

    if value in ["Indifferent", "Unsure"]:
        return "Moderate"

    if value in ["Unfavorable", "Very unfavorable"]:
        return "Low"

    return "Unknown"


df["AIPreference"] = df["AISent"].apply(
    convert_ai_sentiment
)



def convert_ai_usage(value):

    if value == "Yes":
        return "Current User"

    if value == "No, but I plan to soon":
        return "Interested"

    if value == "No, and I don't plan to":
        return "Non-user"

    return "Unknown"


df["AIUsageGroup"] = df["AISelect"].apply(
    convert_ai_usage
)


ai_tasks = df["AIToolCurrently Using"].fillna("")

df["AI_Debugging"] = ai_tasks.str.contains(
    "Debugging and getting help",
    regex=False
)

df["AI_WritingCode"] = ai_tasks.str.contains(
    "Writing code",
    regex=False
)

df["AI_Testing"] = ai_tasks.str.contains(
    "Testing code",
    regex=False
)

df["AI_LearningCodebase"] = ai_tasks.str.contains(
    "Learning about a codebase",
    regex=False
)

df["AI_Documentation"] = ai_tasks.str.contains(
    "Documenting code",
    regex=False
)


df.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("Clean dataset saved to:")
print(OUTPUT_FILE)

print()
print("Final shape:")
print(df.shape)